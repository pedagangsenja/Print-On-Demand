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
# Guna: python3 SK06_finish.py <imej> <S1..S6> <folder keluar> [--sizes 18x24,24x36] [--keep-color] [--palet <json>]
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

VERSI = "SK06 v1 (27 Nov 2026)"
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, str(Path(__file__).resolve().parent))
from styles import STYLES  # noqa: E402

SIZES = {"8x10": (8, 10), "11x14": (11, 14), "16x20": (16, 20), "18x24": (18, 24), "24x36": (24, 36)}
DPI = 300
UP = 4            # skala naik sebelum surih
FIT_W, FIT_H = 0.76, 0.78   # lockup muat dalam 76% lebar / 78% tinggi kanvas
CENTER_Y = 0.47   # pusat optik sedikit di atas tengah


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
    masks = {i: clean(labels == i, area_min=int(30 * UP * UP)) for i in range(len(centers))}
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


def compose_svg(vec, bg_hex, fills, W, H):
    x0, y0, x1, y1 = vec["bbox"]
    s = min(W * FIT_W / (x1 - x0), H * FIT_H / (y1 - y0))
    tx = W / 2 - s * (x0 + x1) / 2
    ty = H * CENTER_Y - s * (y0 + y1) / 2
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
             f'<rect width="{W}" height="{H}" fill="{bg_hex}"/>',
             f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.5f})">']
    for layer, fill in zip(vec["layers"], fills):
        parts.append(f'<g transform="{layer["transform"]}" fill="{fill}" stroke="none">')
        parts += [f'<path d="{d}"/>' for d in layer["paths"]]
        parts.append("</g>")
    parts.append("</g></svg>")
    return "\n".join(parts)


def noise(shape, sigma, rng):
    n = rng.standard_normal(shape).astype(np.float32)
    n = cv2.GaussianBlur(n, (0, 0), sigma) if sigma > 0 else n
    return n / (n.std() + 1e-6)


def texture(png_rgb, bg_hex, kind, seed=7):
    """Tekstur prosedur pada saiz akhir (skala ikut 300 DPI)."""
    if kind == "none":
        return png_rgb
    rng = np.random.default_rng(seed)
    img = png_rgb.astype(np.float32)
    bg = hex2rgb(bg_hex)
    ink = (np.abs(img - bg).sum(-1) > 60).astype(np.float32)   # topeng dakwat
    shape = ink.shape
    if kind == "grain":
        hole = (noise(shape, 1.2, rng) * 0.6 + noise(shape, 6, rng) * 0.4) > 2.1
        a = ink * (1 - hole * 0.85)
        g = noise(shape, 0.8, rng) * 5
        out = bg + (img - bg) * a[..., None]
        out += g[..., None] * 0.6
    elif kind == "worn":
        n = noise(shape, 1.5, rng) * 0.5 + noise(shape, 5, rng) * 0.35 + noise(shape, 18, rng) * 0.35
        hole = np.clip((n - 1.35) / 0.25, 0, 1)
        a = ink * (1 - hole)
        out = bg + (img - bg) * a[..., None]
    elif kind == "chalk":
        streak = cv2.GaussianBlur(rng.standard_normal(shape).astype(np.float32), (0, 0), sigmaX=6, sigmaY=0.8)
        streak /= streak.std() + 1e-6
        fine = noise(shape, 0.9, rng)
        dens = np.clip(0.93 + 0.07 * streak + 0.05 * fine, 0, 1)
        holes = (fine * 0.7 + streak * 0.5) < -1.6
        a = ink * dens * (1 - holes)
        cloud = noise(shape, 120, rng) * 2.0 + noise(shape, 1.5, rng) * 1.5
        base = bg + cloud[..., None]
        out = base + (img - bg) * a[..., None]
    else:
        raise ValueError(kind)
    return np.clip(out, 0, 255).astype(np.uint8)


def main():
    args = sys.argv[1:]
    raw, sid, out = Path(args.pop(0)), args.pop(0), Path(args.pop(0))
    sizes = ["18x24"]
    keep = False
    palet = None
    while args:
        a = args.pop(0)
        if a == "--sizes":
            sizes = args.pop(0).split(",")
        elif a == "--keep-color":
            keep = True
        elif a == "--palet":
            palet = json.loads(Path(args.pop(0)).read_text())
    style = STYLES[sid]
    out.mkdir(parents=True, exist_ok=True)
    img = np.array(Image.open(raw).convert("RGB"))
    vec = vectorize(img, len(palet["dakwat"]) if palet else len(style["inks"]), palet)
    bg_hex, fills = map_palet(vec, palet) if palet else map_palette(vec, style, keep)
    info = {"versi": VERSI, "raw": raw.name, "style": sid, "palet": palet and palet.get("sumber"), "bg": bg_hex, "fills": fills, "layers": len(vec["layers"]),
            "ink_px": [l["area"] for l in vec["layers"]], "sizes": {}}
    master = compose_svg(vec, bg_hex, fills, 1800, 2400)
    (out / "master.svg").write_text(master)
    for sz in sizes:
        wi, hi = SIZES[sz]
        W, H = wi * DPI, hi * DPI
        png = cairosvg.svg2png(bytestring=compose_svg(vec, bg_hex, fills, W, H).encode(), output_width=W, output_height=H)
        arr = np.array(Image.open(__import__("io").BytesIO(png)).convert("RGB"))
        arr = texture(arr, bg_hex, style["texture"])
        im = Image.fromarray(arr)
        im.save(out / f"{sz}.png", dpi=(DPI, DPI))
        im.resize((W * 1000 // H, 1000) if H > W else (1000, H * 1000 // W), Image.LANCZOS).save(
            out / f"{sz}_preview.jpg", quality=88)
        info["sizes"][sz] = [W, H]
    (out / "info.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))


if __name__ == "__main__":
    main()
