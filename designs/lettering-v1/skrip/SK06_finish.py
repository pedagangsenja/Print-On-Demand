# SK06 Vektor + saiz cetak (Standard Lettering v1.2, langkah 6). Dibawa ke cawangan ini 26 Nov 2026.
# Asal: scripts/lettering/finish.py, cawangan claude/dazzling-cannon-5wzn6h (commit 23229f1, 24 Nov 2026).
# 27 Nov 2026: satu parameter ditambah, --palet <json> (hasil SK07 / SK08): latar dan dakwat tepat ikut peranan kad
# atau warna C; topeng diambil terus daripada warna tepat setiap piksel (segment_palet, tanpa k-means) dan
# dilembutkan sebelum surih. Tanpa --palet: kod asal.
# Tugas: imej yang lulus QC + 5b -> SVG induk (potrace) -> susun di tengah -> PNG 300 DPI + pratonton.
# Diperlukan oleh: semua kad (set asas kemasan). Diuji 26 Nov 2026 pada imej K3H sedia ada (gaya S3: satu dakwat putih).
# Had diketahui: palet, ruang tepi (76% x 78%) dan tekstur masih tetap ikut gaya S1-S6 dalam styles.py, belum dibaca
# daripada Kad Gaya. Warna ikut peranan = SK07, bayang = SK08 (dibina 27 Nov 2026; hantar --palet).
# 27 Nov 2026: VERSI dicatat dalam info.json (dibaca belajar_sk.py). Naikkan VERSI setiap kali kod berubah.
# v1.1 (27 Nov 2026, Belajar SK, ubahan tekstur_kad): --kad Kx = jenis dan kekuatan tekstur dibaca daripada
# kad.KAD[Kx]["tekstur"] (bukan tetap ikut gaya S1-S6); bahagian tekstur kad yang belum ada jenisnya dicatat
# sebagai amaran dalam info.json; jika ada gaya S1-S6 daripada gambar upload yang sama (cth. K8 dan S4: IMG_5735),
# tekstur gaya itu dipakai sebagai ganti. Tanpa --kad: tekstur gaya seperti v1.
# v1.2 (27 Nov 2026, Belajar SK, ubahan tepi_kad): dengan --kad, ruang tepi setiap saiz poster ikut kad, sama seperti
# SK02 (asas.rujukan: rujukan.tepi_sisi_pct / tepi_atas_bawah_pct / tepi_pct daripada SK05 pada gambar upload, atau
# ruang_tepi kad). Sisi yang mengehad = nilai kad; pusat optik 0.47 hanya jika ruang atas / bawah tidak kurang
# daripada kad. Ruang tepi diukur pada blok tulisan (topeng SK05, bintik hiasan kecil tidak dikira), sama seperti
# SK02 / SK05. Ruang tepi hasil dicatat dalam info.json. Tanpa --kad: 76% x 78% seperti v1.
# v1.4 (27 Nov 2026, Belajar SK, ubahan kata_tekstur, parameter): kata kad 'bintik' / 'berbintik' = jenis lusuh (worn);
# 'tiada (rata)' = tiada tekstur. Kad K9, K10, K13 (bintik lusuh) kini bertekstur; K11 'retak kasar' masih tidak dibuat.
# v1.3 (27 Nov 2026, Belajar SK, ubahan tekstur_marker): jenis tekstur 'marker' (tepi marker kering + butir latar)
# dengan parameter yang diukur pada gambar upload kad (--ukur-tekstur; disimpan di kad.BLOK[k]['rujukan']['tekstur']).
# Butir dijana pada skala rujukan (blok tulisan sama lebar), jadi rupa sama pada setiap saiz poster. Hasil diukur
# semula pada skala rujukan dan dicatat dalam info.json (amaran jika beza > 30%).
# v1.4 (27 Nov 2026, Belajar SK, ubahan tekstur_calar): jenis tekstur 'calar' (calar + bintik lusuh dalam dakwat,
# kad K23 (dahulu K12), IMG_5793) dengan parameter yang diukur pada gambar upload (ukur_calar: peratus lubang dalam sampul huruf,
# kongsi lubang memanjang = calar, panjang median calar), dijana pada skala rujukan; diukur semula selepas jana.
# Guna: python3 SK06_finish.py <imej> <S1..S6> <folder keluar> [--sizes 18x24,24x36] [--keep-color] [--palet <json>] [--kad Kx]
#       python3 SK06_finish.py --ukur-tekstur <gambar upload>   (v1.3: ukuran tekstur untuk kad)
"""Siapkan imej lettering AI untuk cetak (CPU sahaja).

Langkah: besarkan 4x -> asingkan warna (k-means Lab) -> bersihkan bintik -> surih vektor (potrace)
-> paksa palet gaya (styles.py) -> susun semula di tengah kanvas setiap saiz poster (margin seragam)
-> rasterkan 300 DPI (cairosvg) -> tekstur prosedur (grain / worn / chalk) -> PNG + SVG induk + pratonton.

Guna: python3 scripts/lettering/finish.py <raw.png> <style_id> <out_dir> [--sizes 18x24,24x36] [--keep-color]
  --keep-color : guna warna asal imej (bukan palet gaya).
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import cairosvg
import cv2
import numpy as np
from PIL import Image

VERSI = "SK06 v1.8 (28 Nov 2026)"
# v1.8 (28 Nov 2026, sesi hab): v1.7 + kata tekstur exciting-sagan ("berbintik", "bintik", "tiada (rata)").
# v1.7 (28 Nov 2026, sesi hab): gabung v1.4 nifty-lovelace (tekstur_calar, K23) + v1.4-v1.6 focused-allen (titik_halus,
# lusuh_saring_cop, nota_kurungan). Nombor versi focused-allen v1.4-v1.6 dikekalkan dalam sejarah di bawah.
# v1.6 (Belajar SK, ubahan nota_kurungan): nota dalam kurungan pada teks tekstur kad diabaikan (K14 'tiada (vektor rata)' = tiada).
# v1.5 (Belajar SK, ubahan lusuh_saring_cop): K16 'lusuh cetakan saring' dan K17 'lusuh cop kering' dipadan ke jenis worn.
# v1.4 (Belajar SK, ubahan titik_halus): komponen dakwat < AREA_MIN px (skala imej asal) dibuang; dahulu 30 px membuang
# garis titik dan bintik latar kad K4 (titik 8-30 px). 4 px masih membuang hingar 1-3 px.
AREA_MIN = 4
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, str(Path(__file__).resolve().parent))
from styles import STYLES  # noqa: E402

SIZES = {"8x10": (8, 10), "11x14": (11, 14), "16x20": (16, 20), "18x24": (18, 24), "24x36": (24, 36)}
DPI = 300
UP = 4            # skala naik sebelum surih
FIT_W, FIT_H = 0.76, 0.78   # lockup muat dalam 76% lebar / 78% tinggi kanvas
CENTER_Y = 0.47   # pusat optik sedikit di atas tengah

# Tekstur kad (teks bebas dalam kad.py) -> jenis prosedur. Turutan = keutamaan. Kekuatan: "halus" 0.6, lain 1.0.
TEKSTUR_KAD = [("kapur", "chalk"), ("lusuh", "worn"), ("grunge", "worn"), ("bintik", "worn"), ("butir", "grain"), ("grain", "grain")]
KUAT_KAD = {"halus": 0.6, "sederhana": 1.0}
SOKONG = ("tiada", "kapur", "lusuh", "grunge", "butir", "grain", "halus", "sederhana", "cetakan", "berus kering",
          "saring", "cop kering", "berbintik", "bintik")   # v1.5: lusuh cetakan saring (K11), lusuh cop kering (K12) = jenis worn


def tekstur_kad(teks):
    """Pulang dict(jenis, kuat, tidak_dibuat) daripada teks tekstur kad, ikut bahagian (pisah '+' atau ','). Bahagian
    tanpa padanan jenis, atau tekstur pada latar (SK06 hanya menekstur dakwat), masuk tidak_dibuat supaya
    belajar_sk.py menandanya (cth. K8 'tepi marker kering', 'butir latar')."""
    t = re.sub(r"\s*\([^)]*\)", "", (teks or "tiada").lower()).strip()   # v1.6: nota dalam kurungan diabaikan
    if t == "tiada":
        return dict(jenis="none", kuat=0.0, tidak_dibuat=[])
    jenis, kuat, tak = None, 1.0, []
    for bah in [b.strip() for b in re.split(r"\s*\+\s*|,", t) if b.strip()]:
        sisa = bah
        for kata in SOKONG:
            sisa = sisa.replace(kata, " ")
        j = next((j for kata, j in TEKSTUR_KAD if kata in bah), None)
        if sisa.strip() or "latar" in bah or not j:
            tak.append(bah)
        elif jenis is None:
            jenis, kuat = j, next((v for kata, v in KUAT_KAD.items() if kata in bah), 1.0)
    return dict(jenis=jenis or "none", kuat=kuat if jenis else 0.0, tidak_dibuat=tak)


def hex2rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


def rgb2hex(c):
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in c)


def to_lab(rgb):
    a = np.asarray(rgb, np.float32).reshape(-1, 1, 3) / 255.0
    return cv2.cvtColor(a, cv2.COLOR_RGB2LAB).reshape(-1, 3)


def segment(img, n_ink):
    """Dua peringkat: (1) topeng dakwat = jauh dari warna latar (ambang Otsu pada jarak Lab);
    (2) warna dakwat = k-means pada piksel teras (tepi anti-alias dibuang), kluster hampir digabung.
    Pulang (labels: -1 latar / 0..k-1 dakwat, pusat RGB dakwat, RGB latar) pada saiz besar."""
    big = cv2.resize(img, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    big = cv2.bilateralFilter(big, 9, 40, 9)
    lab = cv2.cvtColor(big.astype(np.float32) / 255.0, cv2.COLOR_RGB2LAB)
    b = max(4, lab.shape[0] // 40)
    border = np.concatenate([lab[:b].reshape(-1, 3), lab[-b:].reshape(-1, 3),
                             lab[:, :b].reshape(-1, 3), lab[:, -b:].reshape(-1, 3)])
    bg = np.median(border, 0)
    dist = np.sqrt(((lab - bg) ** 2).sum(-1))
    d8 = np.clip(dist * 255 / max(float(dist.max()), 1.0), 0, 255).astype(np.uint8)
    t, _ = cv2.threshold(d8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ink = d8 > t
    labels = np.full(ink.shape, -1, np.int32)
    if n_ink == 1:
        labels[ink] = 0
        centers = np.median(lab[ink], 0)[None]
    else:
        core = cv2.erode(ink.astype(np.uint8), np.ones((2 * UP + 1, 2 * UP + 1), np.uint8)).astype(bool)
        pts = lab[core]
        sample = pts[:: max(1, len(pts) // 200000)].astype(np.float32)
        crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 60, 0.2)
        _, _, centers = cv2.kmeans(sample, n_ink, None, crit, 5, cv2.KMEANS_PP_CENTERS)
        centers = list(centers)
        while len(centers) > 1:   # gabung kluster yang hampir sama (beza warna < 12)
            dd = [(np.linalg.norm(centers[i] - centers[j]), i, j)
                  for i in range(len(centers)) for j in range(i + 1, len(centers))]
            dmin, i, j = min(dd)
            if dmin >= 12:
                break
            centers[i] = (centers[i] + centers[j]) / 2
            centers.pop(j)
        centers = np.array(centers, np.float32)
        pix = lab[ink]
        labels[ink] = ((pix[:, None, :] - centers[None]) ** 2).sum(-1).argmin(1)
    conv = lambda c: cv2.cvtColor(np.asarray(c, np.float32).reshape(-1, 1, 3), cv2.COLOR_LAB2RGB).reshape(-1, 3) * 255
    return labels, conv(centers), conv(bg)[0]


def segment_palet(img, palet):
    """Imej rata SK07 / SK08 (tepi anti-alias = campuran latar + satu dakwat). Bagi setiap piksel: dakwat yang paling
    hampir dengan garis latar -> dakwat itu, dan kelegapan alfa di sepanjang garis itu. Alfa setiap dakwat dibesarkan
    4x (kubik) dan dilembutkan (Gaussian) supaya anak tangga piksel jadi lengkung; jumlah alfa > 0.5 = siluet, dan
    setiap piksel siluet ikut dakwat dengan nilai tertinggi (tiada celah atau tindih antara lapisan)."""
    bg = hex2rgb(palet["latar"])
    inks = np.array([hex2rgb(h) for h in palet["dakwat"]], np.float32)
    v = img.astype(np.float32) - bg
    e = inks - bg
    t = np.clip((v @ e.T) / np.maximum((e * e).sum(1), 1e-6), 0, 1)              # H x W x K
    resid = ((v[..., None, :] - t[..., None] * e[None, None]) ** 2).sum(-1)
    k = resid.argmin(-1)
    a = np.take_along_axis(t, k[..., None], -1)[..., 0]
    soft = []
    for i in range(len(inks)):
        m = cv2.resize(np.where(k == i, a, 0).astype(np.float32), None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
        soft.append(cv2.GaussianBlur(m, (0, 0), UP * 0.5))
    soft = np.stack(soft)
    ink = soft.sum(0) > 0.5
    labels = np.where(ink, soft.argmax(0), -1).astype(np.int32)
    return labels, inks, bg


def clean(mask, area_min):
    m = mask.astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= area_min
    return keep[lab]


def potrace_paths(mask, tmp):
    """Surih satu topeng -> (transform, [d path])."""
    pbm = Path(tmp) / "m.pbm"
    svg = Path(tmp) / "m.svg"
    Image.fromarray(np.where(mask, 0, 255).astype(np.uint8)).convert("1").save(pbm)
    subprocess.run(["potrace", str(pbm), "-s", "-o", str(svg), "--turdsize", "40", "--alphamax", "1.0",
                    "--opttolerance", "0.25", "--flat"], check=True)
    s = svg.read_text()
    tr = re.search(r'<g transform="([^"]+)"', s).group(1)
    return tr, re.findall(r'<path d="([^"]+)"', s)


def vectorize(img, n_ink, palet=None):
    labels, centers, bg_rgb = segment_palet(img, palet) if palet else segment(img, n_ink)
    H, W = labels.shape
    masks = {i: clean(labels == i, area_min=int(AREA_MIN * UP * UP)) for i in range(len(centers))}
    masks = {i: m for i, m in masks.items() if m.any()}
    union = np.zeros(labels.shape, bool)
    for m in masks.values():
        union |= m
    ys, xs = np.nonzero(union)
    bbox = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    # lapisan besar di bawah; lapisan bawah dikembangkan di bawah lapisan atas supaya tiada celah warna
    order = sorted(masks, key=lambda i: -masks[i].sum())
    layers = []
    with tempfile.TemporaryDirectory() as tmp:
        for n, i in enumerate(order):
            m = masks[i].copy()
            above = np.zeros_like(m)
            for j in order[n + 1:]:
                above |= masks[j]
            if above.any():   # isi bawah lapisan atas hanya di sempadan bersama (elak halo di tepi latar)
                near = cv2.dilate(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))).astype(bool)
                m |= above & near
            tr, paths = potrace_paths(m, tmp)
            layers.append({"cluster": int(i), "rgb": centers[i], "transform": tr, "paths": paths,
                           "area": int(masks[i].sum())})
    return {"W": W, "H": H, "bbox": [int(v) for v in bbox], "bg_rgb": bg_rgb, "layers": layers}


def map_palette(vec, style, keep_color):
    if keep_color:
        return rgb2hex(vec["bg_rgb"]), [rgb2hex(l["rgb"]) for l in vec["layers"]]
    pal = [hex2rgb(h) for h in style["inks"]]
    a = to_lab([l["rgb"] for l in vec["layers"]])
    b = to_lab(pal)
    cost = ((a[:, None, :] - b[None, :, :]) ** 2).sum(-1)
    rows, cols = linear_sum_assignment(cost)
    fills = [style["inks"][0]] * len(vec["layers"])
    for r, c in zip(rows, cols):
        fills[r] = style["inks"][c]
    return style["bg"], fills


def map_palet(vec, palet):
    """Lapisan -> dakwat palet yang paling hampir (Lab). Imej SK07 / SK08 sudah rata, jadi padanan terus."""
    ink = to_lab([hex2rgb(h) for h in palet["dakwat"]])
    lay = to_lab([l["rgb"] for l in vec["layers"]])
    return palet["latar"], [palet["dakwat"][int(((ink - c) ** 2).sum(-1).argmin())] for c in lay]


def letak(vec, W, H, tepi=None):
    """Skala dan kedudukan lockup pada kanvas W x H. tepi = dict(sisi, atas_bawah) dalam % lebar / tinggi (v1.2, kad);
    None = 76% x 78% (v1). Pulang (s, tx, ty, ruang tepi hasil dalam %)."""
    x0, y0, x1, y1 = vec["bbox_blok"] if tepi and vec.get("bbox_blok") else vec["bbox"]
    bw, bh = x1 - x0, y1 - y0
    if tepi:
        ts, ta = tepi["sisi"] / 100, tepi["atas_bawah"] / 100
        s = min(W * (1 - 2 * ts) / bw, H * (1 - 2 * ta) / bh)
        lo, hi = ta + s * bh / (2 * H), 1 - ta - s * bh / (2 * H)   # ruang atas / bawah tidak kurang daripada kad
        cy = min(max(CENTER_Y, lo), hi) if lo <= hi else 0.5
    else:
        s, cy = min(W * FIT_W / bw, H * FIT_H / bh), CENTER_Y
    tx = W / 2 - s * (x0 + x1) / 2
    ty = H * cy - s * (y0 + y1) / 2
    hasil = dict(kiri=round((tx + s * x0) / W * 100, 1), kanan=round((W - tx - s * x1) / W * 100, 1),
                 atas=round((ty + s * y0) / H * 100, 1), bawah=round((H - ty - s * y1) / H * 100, 1))
    return s, tx, ty, hasil


def compose_svg(vec, bg_hex, fills, W, H, tepi=None):
    s, tx, ty, _ = letak(vec, W, H, tepi)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
             f'<rect width="{W}" height="{H}" fill="{bg_hex}"/>',
             f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.5f})">']
    for layer, fill in zip(vec["layers"], fills):
        parts.append(f'<g transform="{layer["transform"]}" fill="{fill}" stroke="none">')
        parts += [f'<path d="{d}"/>' for d in layer["paths"]]
        parts.append("</g>")
    parts.append("</g></svg>")
    return "\n".join(parts)


def ukur_tekstur(rgb, lebar_blok=None):
    """v1.3: ukur tekstur gambar latar gelap + dakwat cerah (gambar upload kad, atau hasil SK06 untuk banding).
    lebar_blok = skala semula dahulu supaya blok tulisan selebar itu (piksel), jadi ukuran boleh dibanding pada
    skala rujukan. Pulang sd butir latar (halus < 1 px, sederhana 1-16 px, kasar > 16 px), sd dakwat, kekasaran tepi
    (perimeter / perimeter selepas licin 5 px) dan lebar blok (topeng SK05)."""
    from SK05_ukur import topeng
    blok, _ = topeng(rgb)
    ys, xs = np.nonzero(blok)
    bw = int(xs.max() - xs.min() + 1)
    if lebar_blok and abs(bw - lebar_blok) > 2:
        f = lebar_blok / bw
        rgb = cv2.resize(rgb, (max(1, int(rgb.shape[1] * f)), max(1, int(rgb.shape[0] * f))), interpolation=cv2.INTER_AREA)
        bw = lebar_blok
    g = rgb.astype(np.float32).mean(-1)
    t, _ = cv2.threshold(g.astype(np.uint8), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ink = (g > t).astype(np.uint8)
    teras = cv2.erode(ink, np.ones((5, 5), np.uint8)).astype(bool)
    lat = cv2.erode(1 - ink, np.ones((9, 9), np.uint8)).astype(bool)
    v = g.copy()
    v[~lat] = np.median(g[lat])
    sd = {sg: float((cv2.GaussianBlur(v, (0, 0), sg) if sg else v)[lat].std()) for sg in (0, 1, 16)}
    d = g.copy()
    d[~teras] = np.median(g[teras])
    d1 = float(cv2.GaussianBlur(d, (0, 0), 1)[teras].std())   # butir dakwat >= 1 px (bawah 1 px = mampatan JPEG)
    licin = cv2.morphologyEx(cv2.morphologyEx(ink, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    per = lambda m: sum(cv2.arcLength(c, True) for c in cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
                        if cv2.contourArea(c) > 200)
    return dict(latar_halus=round(max(0.0, sd[0] ** 2 - sd[1] ** 2) ** 0.5, 2), latar_sederhana=round(max(0.0, sd[1] ** 2 - sd[16] ** 2) ** 0.5, 2),
                latar_kasar=round(sd[16], 2), dakwat_sd=round(float(g[teras].std()), 2), dakwat_sd1=round(d1, 2), tepi_kasar=round(per(ink) / max(1.0, per(licin)), 3),
                latar_median=round(float(np.median(g[lat])), 1), lebar_blok=bw)


def ukur_calar(rgb, lebar_blok=None, bg=None):
    """v1.4: ukur calar + bintik lusuh di dalam huruf (lubang warna latar di dalam sampul dakwat). Latar = median tepi
    imej (atau bg). Skala semula dahulu supaya blok dakwat selebar lebar_blok. Pulang lubang_pct (lubang / sampul),
    calar_pct (kongsi lubang memanjang: nisbah >= 4 dan panjang >= 12 px), calar_panjang (median, px) dan lebar_blok."""
    rgb = rgb.astype(np.float32)
    b = np.array(bg, np.float32) if bg is not None else np.median(np.concatenate([rgb[:4].reshape(-1, 3), rgb[-4:].reshape(-1, 3),
                                                                                   rgb[:, :4].reshape(-1, 3), rgb[:, -4:].reshape(-1, 3)]), 0)
    ink = (np.abs(rgb - b).sum(-1) > 150).astype(np.uint8)
    ys, xs = np.nonzero(ink)
    bw = int(xs.max() - xs.min() + 1)
    if lebar_blok and abs(bw - lebar_blok) > 2:
        f = lebar_blok / bw
        ink = (cv2.resize(ink * 255, (max(1, int(ink.shape[1] * f)), max(1, int(ink.shape[0] * f))), interpolation=cv2.INTER_AREA) > 127).astype(np.uint8)
        bw = lebar_blok
    env = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    holes = ((env > 0) & (ink == 0)).astype(np.uint8)
    n, _, st, _ = cv2.connectedComponentsWithStats(holes, 8)
    a, w, h = st[1:, 4], st[1:, 2], st[1:, 3]
    pj = np.maximum(w, h)
    cal = (pj / np.maximum(1, np.minimum(w, h)) >= 4) & (pj >= 12)
    tot = max(1, int(holes.sum()))
    return dict(lubang_pct=round(100 * tot / max(1, int(env.sum())), 2), calar_pct=round(100 * float(a[cal].sum()) / tot, 1),
                calar_panjang=float(np.median(pj[cal])) if cal.any() else 0.0, lebar_blok=bw)


def noise(shape, sigma, rng):
    n = rng.standard_normal(shape).astype(np.float32)
    n = cv2.GaussianBlur(n, (0, 0), sigma) if sigma > 0 else n
    return n / (n.std() + 1e-6)


def tekstur_untuk(kid):
    """Tekstur bagi kad: ukuran gambar upload (rujukan.tekstur) dahulu; jika tiada, teks kad (tekstur_kad) dan ganti
    gaya daripada gambar upload yang sama. Dipakai oleh main() dan belajar_sk.py (liputan kad)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    import kad
    teks = kad.KAD[kid].get("tekstur", "tiada")
    ukur = (kad.BLOK.get(kid, {}).get("rujukan") or {}).get("tekstur")
    if ukur:
        return dict(kad=kid, teks=teks, jenis=ukur["jenis"], kuat=1.0, tidak_dibuat=[], ukur=ukur)
    tk = dict(kad=kid, teks=teks, **tekstur_kad(teks))
    ref = kad.KAD[kid].get("ref")
    sama = next((g for g, st in STYLES.items() if st.get("ref") == ref and st["texture"] != "none"), None)
    if tk["tidak_dibuat"] and tk["jenis"] == "none" and sama:   # ganti: gaya yang dibuat daripada gambar upload sama
        tk.update(jenis=STYLES[sama]["texture"], kuat=1.0, ganti=f"tekstur gaya {sama} (gambar rujukan sama, {ref})")
    return tk


def texture(png_rgb, bg_hex, kind, seed=7, kuat=1.0, p=None, k=1.0):
    """Tekstur prosedur pada saiz akhir (skala ikut 300 DPI). kuat 1.0 = v1; < 1 = lebih halus (kurang lubang)."""
    if kind == "none":
        return png_rgb
    rng = np.random.default_rng(seed)
    img = png_rgb.astype(np.float32)
    bg = hex2rgb(bg_hex)
    ink = (np.abs(img - bg).sum(-1) > 60).astype(np.float32)   # topeng dakwat
    shape = ink.shape
    if kind == "grain":
        hole = (noise(shape, 1.2, rng) * 0.6 + noise(shape, 6, rng) * 0.4) > 2.1 + (1 - kuat) * 0.6
        a = ink * (1 - hole * 0.85)
        g = noise(shape, 0.8, rng) * 5 * kuat
        out = bg + (img - bg) * a[..., None]
        out += g[..., None] * 0.6
    elif kind == "worn":
        n = noise(shape, 1.5, rng) * 0.5 + noise(shape, 5, rng) * 0.35 + noise(shape, 18, rng) * 0.35
        hole = np.clip((n - 1.35 - (1 - kuat) * 0.4) / 0.25, 0, 1)
        a = ink * (1 - hole)
        out = bg + (img - bg) * a[..., None]
    elif kind == "chalk":
        streak = cv2.GaussianBlur(rng.standard_normal(shape).astype(np.float32), (0, 0), sigmaX=6, sigmaY=0.8)
        streak /= streak.std() + 1e-6
        fine = noise(shape, 0.9, rng)
        dens = np.clip(0.93 + 0.07 * streak + 0.05 * fine, 0, 1)
        holes = (fine * 0.7 + streak * 0.5) < -1.6 - (1 - kuat) * 0.5
        a = ink * dens * (1 - holes)
        cloud = (noise(shape, 120, rng) * 2.0 + noise(shape, 1.5, rng) * 1.5) * kuat
        base = bg + cloud[..., None]
        out = base + (img - bg) * a[..., None]
    elif kind == "marker":   # v1.3: tepi marker kering + butir latar; p diukur pada gambar upload, k = px hasil / px rujukan
        H, W = shape
        hs, ws = max(8, int(round(H / k))), max(8, int(round(W / k)))

        def nz(sg):   # hingar pada skala rujukan, dibesarkan ke saiz akhir
            n = cv2.resize(noise((hs, ws), sg, rng), (W, H), interpolation=cv2.INTER_CUBIC)
            return n / (n.std() + 1e-6)
        # Hanya skala yang boleh diukur pada gambar upload (>= 1 px rujukan); butir bawah 1 px dan kekasaran tepi pada
        # JPEG kecil = mampatan, jadi tidak ditiru (tepi kekal ikut imej AI).
        lat = nz(3) * p["g_sederhana"] + nz(30) * p["g_kasar"]
        a = ink
        dk = nz(3) * p["g_dakwat"]
        out = (bg + lat[..., None]) * (1 - a[..., None]) + (img + dk[..., None]) * a[..., None]
    elif kind == "calar":   # v1.4: calar + bintik lusuh dalam dakwat; p diukur pada gambar upload, k = px hasil / px rujukan
        H, W = shape
        hs, ws = max(8, int(round(H / k))), max(8, int(round(W / k)))
        m = np.zeros((hs, ws), np.uint8)
        nc = int(p["g_bil_calar"] * hs * ws / 1e6)
        for _ in range(nc):   # calar: garis nipis, sudut rawak, panjang lognormal sekitar median rujukan
            L = float(np.clip(rng.lognormal(np.log(p["g_panjang"]), 0.6), 6, 12 * p["g_panjang"]))
            t = rng.uniform(0, np.pi)
            x, y = rng.uniform(0, ws), rng.uniform(0, hs)
            dx, dy = np.cos(t) * L / 2, np.sin(t) * L / 2
            cv2.line(m, (int(x - dx), int(y - dy)), (int(x + dx), int(y + dy)), 1, 1)
        n = noise((hs, ws), 1.0, rng) * 0.7 + noise((hs, ws), 4, rng) * 0.5
        bintik = n > p["g_ambang_bintik"]
        hole = cv2.resize(((m > 0) | bintik).astype(np.uint8) * 255, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255
        a = ink * (1 - hole)
        out = bg + (img - bg) * a[..., None]
    else:
        raise ValueError(kind)
    return np.clip(out, 0, 255).astype(np.uint8)


def main():
    args = sys.argv[1:]
    if args and args[0] == "--ukur-tekstur":   # v1.3: ukur tekstur gambar upload kad
        print(json.dumps(dict(gambar=Path(args[1]).name, **ukur_tekstur(np.array(Image.open(args[1]).convert("RGB")))), ensure_ascii=False))
        return
    raw, sid, out = Path(args.pop(0)), args.pop(0), Path(args.pop(0))
    sizes = ["18x24"]
    keep = False
    palet = None
    kid = None
    tepi = None
    while args:
        a = args.pop(0)
        if a == "--sizes":
            sizes = args.pop(0).split(",")
        elif a == "--keep-color":
            keep = True
        elif a == "--palet":
            palet = json.loads(Path(args.pop(0)).read_text())
        elif a == "--kad":
            kid = args.pop(0)
    style = STYLES[sid]
    tk = dict(jenis=style["texture"], kuat=1.0, tidak_dibuat=[])
    if kid:   # v1.1: tekstur ikut kad (v1.3: ukuran gambar upload dahulu)
        tk = tekstur_untuk(kid)
        import asas
        ruj = asas.rujukan(kid)   # sama seperti SK02 (5b)
        tepi = dict(sisi=float(ruj.get("tepi_sisi_pct", ruj["tepi_pct"])), atas_bawah=float(ruj.get("tepi_atas_bawah_pct", ruj["tepi_pct"])),
                    sumber=ruj.get("sumber", "kad"))
    out.mkdir(parents=True, exist_ok=True)
    img = np.array(Image.open(raw).convert("RGB"))
    vec = vectorize(img, len(palet["dakwat"]) if palet else len(style["inks"]), palet)
    if tepi:   # blok tulisan seperti SK05 / SK02 (bintik hiasan kecil di luar blok tidak dikira dalam ruang tepi)
        from SK05_ukur import topeng
        blok, _ = topeng(img)
        ys, xs = np.nonzero(blok)
        if len(ys):
            vec["bbox_blok"] = [int(xs.min()) * UP, int(ys.min()) * UP, (int(xs.max()) + 1) * UP, (int(ys.max()) + 1) * UP]
    bg_hex, fills = map_palet(vec, palet) if palet else map_palette(vec, style, keep)
    info = {"versi": VERSI, "raw": raw.name, "style": sid, "palet": palet and palet.get("sumber"), "bg": bg_hex, "fills": fills, "layers": len(vec["layers"]),
            "ink_px": [l["area"] for l in vec["layers"]], "sizes": {},
            "tekstur": tk, "amaran": [f"tekstur kad '{b}' belum ada jenisnya dalam SK06: " + (f"diganti {tk['ganti']}" if tk.get("ganti") else "tidak dibuat")
                                      for b in tk["tidak_dibuat"]]}
    if tepi:
        info["tepi"] = dict(sasaran=tepi, hasil={})
    master = compose_svg(vec, bg_hex, fills, 1800, 2400, tepi)
    (out / "master.svg").write_text(master)
    for sz in sizes:
        wi, hi = SIZES[sz]
        W, H = wi * DPI, hi * DPI
        png = cairosvg.svg2png(bytestring=compose_svg(vec, bg_hex, fills, W, H, tepi).encode(), output_width=W, output_height=H)
        if tepi:
            h_ = letak(vec, W, H, tepi)[3]
            info["tepi"]["hasil"][sz] = h_
            had = min(abs(min(h_["kiri"], h_["kanan"]) - tepi["sisi"]), abs(min(h_["atas"], h_["bawah"]) - tepi["atas_bawah"]))
            if had > 2.0:   # sisi yang mengehad mesti sama dengan kad (HAD tepi 5b = 2 mata)
                info["amaran"].append(f"ruang tepi {sz} di luar had: beza {round(had, 1)} mata daripada kad")
            s_, tx_, ty_, _ = letak(vec, W, H, tepi)   # semua dakwat (termasuk bintik hiasan) mesti dalam kanvas
            x0, y0, x1, y1 = vec["bbox"]
            luar = min(tx_ + s_ * x0, W - tx_ - s_ * x1, ty_ + s_ * y0, H - ty_ - s_ * y1)
            info["tepi"]["dakwat_min_pct"] = round(float(luar) / min(W, H) * 100, 2)
            if luar < 0.005 * min(W, H):
                info["amaran"].append(f"dakwat menyentuh tepi kanvas {sz} (hiasan mungkin terpotong)")
        arr = np.array(Image.open(__import__("io").BytesIO(png)).convert("RGB"))
        k_ = 1.0
        if tk.get("ukur"):   # skala: lebar blok tulisan hasil / lebar blok gambar upload
            s_, _, _, _ = letak(vec, W, H, tepi)
            bb = vec.get("bbox_blok") or vec["bbox"]
            k_ = s_ * (bb[2] - bb[0]) / tk["ukur"]["lebar_blok"]
        arr = texture(arr, bg_hex, tk["jenis"], kuat=tk["kuat"] or 1.0, p=tk.get("ukur"), k=k_)
        if tk.get("ukur"):   # ukur semula pada skala rujukan
            calar = tk["jenis"] == "calar"
            h_ = ukur_calar(arr, tk["ukur"]["lebar_blok"], hex2rgb(bg_hex)) if calar else ukur_tekstur(arr, tk["ukur"]["lebar_blok"])
            info["tekstur"].setdefault("hasil_ukur", {})[sz] = h_
            for m in (("lubang_pct", "calar_pct") if calar else ("latar_sederhana", "latar_kasar", "dakwat_sd1")):   # skala yang diukur dengan yakin sahaja
                if abs(h_[m] - tk["ukur"][m]) > 0.3 * abs(tk["ukur"][m]):
                    info["amaran"].append(f"tekstur {sz}: {m} {h_[m]} lawan rujukan {tk['ukur'][m]} (beza > 30%)")
        im = Image.fromarray(arr)
        im.save(out / f"{sz}.png", dpi=(DPI, DPI))
        im.resize((W * 1000 // H, 1000) if H > W else (1000, H * 1000 // W), Image.LANCZOS).save(
            out / f"{sz}_preview.jpg", quality=88)
        info["sizes"][sz] = [W, H]
    (out / "info.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))


if __name__ == "__main__":
    main()
