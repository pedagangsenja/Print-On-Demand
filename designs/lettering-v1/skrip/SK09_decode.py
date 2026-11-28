"""SK09 Decode (Standard Lettering v1.2, langkah 1: decode gambar upload). Versi 1.0, 28 Nov 2026.

Tugas: baca SATU gambar dan tulis SATU rekod decode (JSON) dengan lima kumpulan: susunan, baris (huruf), elemen,
       warna, tekstur. Rekod ini disimpan SEBELUM prompt ditulis; Kad Gaya diisi daripada rekod, bukan ditaip tangan.
Dipakai dua cara:
  1. Langkah 1: decode GAMBAR UPLOAD (rujukan)           -> decode/<nama>.json
  2. Langkah 5 (QC bahagian B): decode IMEJ JANA yang sama cara, kemudian SK10 membanding dua rekod itu.
Setiap medan bertanda sumbernya: semua medan di sini = "diukur skrip"; medan "mata" = diisi Claude dengan mata
(decode/mata/<nama>.json: nama gaya, kelas huruf, teks, hiasan) kerana skrip tidak boleh menamakan font.
Diuji pada: 4 gambar upload saiz penuh (IMG_5796, IMG_5797, IMG_5804, IMG_5810). Satu ujian sahaja: bukti lemah.
Had: latar mesti hampir satu warna. Baris yang bertindih rapat boleh tergabung (lihat 'amaran'). Kelas huruf
     (sans / serif / skrip) ialah anggaran daripada bentuk; nama font TIDAK boleh dikenal pasti oleh skrip ini.
     Gambar bawah 600 piksel lebar ditanda 'ukuran kasar'.

Guna: python3 SK09_decode.py <gambar> [...] [--keluar DIR] [--semak]
      --keluar DIR  folder rekod (lalai: ../decode);  --semak = simpan gambar semakan (kotak baris dan elemen)
"""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from SK05_ukur import _skor  # noqa: E402

VERSI = "SK09 v1.0"
HERE = Path(__file__).resolve().parent
KELUAR = HERE.parent / "decode"


def muat(path):
    return np.array(Image.open(path).convert("RGB"))


def lab(rgb):
    """CIELAB sebenar (L 0-100) supaya jarak warna = Delta E."""
    return cv2.cvtColor(rgb.astype(np.float32) / 255.0, cv2.COLOR_RGB2LAB)


def hexa(v):
    return "#%02x%02x%02x" % tuple(int(round(x)) for x in v)


def tepi_piksel(a):
    h, w = a.shape[:2]
    t = max(2, int(min(h, w) * 0.03))
    return np.concatenate([a[:t].reshape(-1, 3), a[-t:].reshape(-1, 3), a[:, :t].reshape(-1, 3),
                           a[:, -t:].reshape(-1, 3)])


def topeng(L, bg):
    """Dakwat = piksel yang jauh daripada warna latar (Delta E). Ambang dicari sendiri (Otsu), dihadkan 18-45."""
    d = np.sqrt(((L - bg) ** 2).sum(axis=2))
    d8 = np.clip(d * 2, 0, 255).astype(np.uint8)
    otsu, _ = cv2.threshold(d8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    amb = float(np.clip(otsu / 2 * 0.6, 18, 45))
    m = (d > amb).astype(np.uint8)
    n, lb, st, _ = cv2.connectedComponentsWithStats(m, 8)
    simpan = np.zeros(n, bool)
    simpan[1:] = st[1:, cv2.CC_STAT_AREA] >= 0.00005 * m.size      # buang butir latar yang sangat kecil
    return simpan[lb].astype(np.uint8), d, round(amb, 1)


def palet(rgb, L, k=6):
    """Warna utama gambar: k-means dalam Lab, kelompok yang hampir sama (Delta E < 12) digabung."""
    s = 220 / max(rgb.shape[:2])
    kecil = cv2.resize(L, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).reshape(-1, 3).astype(np.float32)
    cv2.setRNGSeed(7)
    _, lbl, pusat = cv2.kmeans(kecil, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.5), 4,
                               cv2.KMEANS_PP_CENTERS)
    kira = np.bincount(lbl.ravel(), minlength=k).astype(float)
    kump = [dict(lab=pusat[i], n=kira[i]) for i in np.argsort(-kira) if kira[i] > 0]
    gab = []
    for c in kump:
        for g in gab:
            if np.linalg.norm(g["lab"] - c["lab"]) < 12:
                g["lab"] = (g["lab"] * g["n"] + c["lab"] * c["n"]) / (g["n"] + c["n"])
                g["n"] += c["n"]
                break
        else:
            gab.append(dict(lab=c["lab"].copy(), n=c["n"]))
    gab = [g for g in gab if g["n"] / kira.sum() >= 0.004]
    pusat = np.array([g["lab"] for g in gab], np.float32)
    peta = np.argmin(((L[:, :, None, :] - pusat[None, None]) ** 2).sum(axis=3), axis=2)
    return pusat, peta


def lab_ke_rgb(v):
    return cv2.cvtColor(np.float32([[v]]), cv2.COLOR_LAB2RGB)[0, 0] * 255


def condong(blok, julat=30):
    """Sudut garis dasar baris (darjah, positif = naik ke kanan). Kaedah SK05, julat diluaskan ke +-30."""
    s = 400 / blok.shape[1]
    m = cv2.resize(blok * 255, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32)
    pad = int(max(m.shape) * 0.2)
    m = cv2.copyMakeBorder(m, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    a0 = max(np.arange(-julat, julat + 0.01, 1.0), key=lambda a: _skor(m, a))
    a1 = max(np.arange(a0 - 1, a0 + 1.01, 0.2), key=lambda a: _skor(m, a))
    return round(-float(a1), 1)


def putar(a, sudut, nearest=False):
    h, w = a.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -sudut, 1)
    return cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_NEAREST if nearest else cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def isi_lubang(m):
    """Isi lubang dalam setiap bentuk (kaunter huruf, teks tembus dalam kotak)."""
    h, w = m.shape
    f = cv2.copyMakeBorder((1 - m).astype(np.uint8), 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=1)
    cv2.floodFill(f, None, (0, 0), 2)
    return (f[1:-1, 1:-1] != 2).astype(np.uint8)


def jalur(m, peta_d):
    """Pecah blok kepada jalur baris: (1) lembah unjuran baris, (2) pertukaran warna dakwat utama."""
    H = m.shape[0]
    p = isi_lubang(m).sum(axis=1).astype(float)
    k = max(3, int(H * 0.006)) | 1
    ps = np.convolve(p, np.ones(k) / k, mode="same")
    ada = ps > 0.06 * ps.max()
    seg, mula = [], None
    for y, v in enumerate(list(ada) + [False]):
        if v and mula is None:
            mula = y
        elif not v and mula is not None:
            seg.append([mula, y])
            mula = None

    def belah(a, b, dalam=0):
        if dalam > 6 or b - a < 0.06 * H:
            return [[a, b]]
        q = ps[a:b]
        pin = max(2, int((b - a) * 0.18))
        best, by = None, None
        for y in range(pin, len(q) - pin):
            kiri, kanan = q[:y].max(), q[y:].max()
            nis = q[y] / max(1e-6, min(kiri, kanan))
            if nis < 0.42 and (best is None or nis < best):
                best, by = nis, y
        if by is None:
            return [[a, b]]
        return belah(a, a + by, dalam + 1) + belah(a + by, b, dalam + 1)

    seg = [s for a, b in seg for s in belah(a, b)]
    # pertukaran warna: label dakwat paling banyak pada setiap baris piksel
    keluar = []
    for a, b in seg:
        dom = []
        for y in range(a, b):
            v = peta_d[y][m[y] > 0]
            dom.append(np.bincount(v).argmax() if len(v) else -1)
        dom = np.array(dom)
        minr = max(3, int(0.03 * H))
        potong, y0 = [], 0
        for y in range(1, len(dom) + 1):
            if y == len(dom) or dom[y] != dom[y0]:
                potong.append([y0, y, dom[y0]])
                y0 = y
        besar = [r for r in potong if r[1] - r[0] >= minr]
        if len(besar) >= 2:
            sempadan = [a] + [a + (besar[i][1] + besar[i + 1][0]) // 2 for i in range(len(besar) - 1)
                              if besar[i][2] != besar[i + 1][2]] + [b]
            keluar += [[sempadan[i], sempadan[i + 1]] for i in range(len(sempadan) - 1)]
        else:
            keluar.append([a, b])
    return keluar


def condong_huruf(t):
    """Condong italik huruf dalam satu baris (darjah, positif = huruf rebah ke kanan): ricih yang menjadikan
    unjuran lajur paling tajam."""
    h, w = t.shape
    s = min(1.0, 160 / max(1, h))
    m = cv2.resize(t * 255, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32)
    h, w = m.shape
    m = cv2.copyMakeBorder(m, 0, 0, 2 * h, 2 * h, cv2.BORDER_CONSTANT, value=0)

    def skor(a):
        k = np.tan(np.radians(a))
        M = np.float32([[1, k, -k * h / 2], [0, 1, 0]])
        c = cv2.warpAffine(m, M, (m.shape[1], h)).sum(axis=0)
        return float((c ** 2).sum())

    a0 = max(np.arange(-45, 45.01, 2.5), key=skor)
    a1 = max(np.arange(a0 - 2.5, a0 + 2.51, 0.5), key=skor)
    return round(float(a1), 1)


def ukur_baris(t, blok_w, blok_h, x_blok):
    """Ciri huruf satu baris daripada topeng teks 't' (1 = huruf). Semua nisbah dibanding tinggi baris."""
    ys, xs = np.nonzero(t)
    if len(xs) < 20:
        return None
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    c = np.ascontiguousarray(t[y0:y1, x0:x1])
    hh, ww = c.shape
    n, lb, st, _ = cv2.connectedComponentsWithStats(c, 8)
    besar = [i for i in range(1, n) if st[i, cv2.CC_STAT_HEIGHT] >= 0.45 * hh]
    dt = cv2.distanceTransform(c, cv2.DIST_L2, 5)
    rabung = dt[(dt >= cv2.dilate(dt, np.ones((3, 3), np.uint8)) - 1e-6) & (dt >= 1.0)]
    tebal = float(2 * np.median(rabung)) if len(rabung) else 0.0
    kontras = float(np.percentile(rabung, 90) / max(1e-6, np.percentile(rabung, 25))) if len(rabung) else 0.0
    kb = max(3, int(hh * 0.03)) | 1
    licin = (cv2.medianBlur(c * 255, kb) > 127).astype(np.uint8)
    per = lambda a: sum(cv2.arcLength(k, True) for k in cv2.findContours(a, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0])
    kasar = per(c) / max(1.0, per(licin)) - 1
    tutup = cv2.morphologyEx(c, cv2.MORPH_CLOSE, np.ones((kb, kb), np.uint8))
    pecah = 1 - c.sum() / max(1, tutup.sum())
    jangka = ww / (0.62 * hh)                                    # anggaran bilangan huruf jika tidak bersambung
    sambung = len(besar) < 0.5 * jangka and ww > 1.5 * hh
    tinggi = np.array([st[i, cv2.CC_STAT_HEIGHT] for i in besar], float)
    seragam = float(tinggi.std() / tinggi.mean()) if len(tinggi) >= 2 else None
    nl = float(np.median([st[i, cv2.CC_STAT_WIDTH] / st[i, cv2.CC_STAT_HEIGHT] for i in besar])) \
        if besar and not sambung else None
    slant = condong_huruf(c)
    tp = tebal / hh * 100
    if sambung or (abs(slant) >= 8 and ((seragam or 0) > 0.12 or len(besar) < 0.75 * jangka)):
        kelas = "skrip / tulisan sambung"
    elif abs(slant) >= 8:
        kelas = "blok condong (italik)"
    elif tp >= 15:
        kelas = "blok pekat"
    elif tp >= 8:
        kelas = "blok sederhana"
    else:
        kelas = "nipis"
    return dict(
        kotak_blok_pct=[round((x0 - x_blok) / blok_w * 100, 1), round((x1 - x_blok) / blok_w * 100, 1)],
        tinggi_px=int(hh), lebar_px=int(ww), ukuran_kasar=bool(hh < 40),
        lebar_pct=round(ww / blok_w * 100, 1),
        tebal_strok_pct=round(tp, 1), kontras_strok=round(kontras, 2), isian_pct=round(c.mean() * 100, 1),
        condong_huruf_darjah=slant, komponen=int(n - 1), komponen_besar=len(besar), bersambung=bool(sambung),
        nisbah_lebar_huruf=None if nl is None else round(nl, 2),
        beza_tinggi_huruf=None if seragam is None else round(seragam, 3),
        huruf=("tidak pasti" if seragam is None else "HURUF BESAR (tinggi seragam)" if seragam < 0.09
               else "huruf campur (tinggi tidak seragam)"),
        tepi_kasar_pct=round(kasar * 100, 1), pecah_pct=round(pecah * 100, 1), kelas_anggaran=kelas)


def decode(path, semak=None):
    rgb = muat(path)
    h, w = rgb.shape[:2]
    L = lab(rgb)
    bg = np.median(tepi_piksel(L), axis=0)
    m, d, amb = topeng(L, bg)
    amaran = []
    if w < 600:
        amaran.append("gambar kecil (lebar %d px): ukuran kasar; upload semula saiz penuh" % w)
    if m.sum() == 0:
        return dict(versi=VERSI, fail=Path(path).name, kosong=True)
    pusat, peta = palet(rgb, L)
    ibg = int(np.argmin(((pusat - bg) ** 2).sum(axis=1)))

    # ---- susunan
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()) + 1, int(ys.min()), int(ys.max()) + 1
    sudut = condong(m)
    mr = putar(m, sudut, True)
    pr = putar((peta + 1).astype(np.uint8), sudut, True).astype(int) - 1      # -1 = luar gambar
    rr = putar(rgb, sudut)
    Lr = lab(rr)
    ysr, xsr = np.nonzero(mr)
    bx0, bx1, by0, by1 = int(xsr.min()), int(xsr.max()) + 1, int(ysr.min()), int(ysr.max()) + 1
    bw, bh = bx1 - bx0, by1 - by0

    # ---- baris
    baris, elemen = [], []
    for a, b in jalur(mr, pr):
        band = mr[a:b]
        yy, xx = np.nonzero(band)
        if len(xx) == 0:
            continue
        ax0, ax1, ay0, ay1 = xx.min(), xx.max() + 1, a + yy.min(), a + yy.max() + 1
        jh, jw = ay1 - ay0, ax1 - ax0
        kot = mr[ay0:ay1, ax0:ax1]
        lbl = pr[ay0:ay1, ax0:ax1]
        if jh < 0.012 * bh:
            continue
        n, lb, st, _ = cv2.connectedComponentsWithStats(kot, 8)
        v = lbl[kot > 0]
        v = v[v >= 0]
        dom = int(np.bincount(v).argmax())
        # sapuan / garis yang berdiri sebagai satu jalur (cth. garis bawah berus)
        if jw / jh >= 4 and n - 1 <= 2 and jh < 0.2 * bh:
            elemen.append(dict(jenis="garis / sapuan", kotak_pct=_kpct(ax0, ay0, ax1, ay1, bx0, by0, bw, bh),
                               warna=hexa(lab_ke_rgb(pusat[dom]))))
            continue
        # bekas (kotak / label): SATU bentuk pejal selebar jalur, dengan teks di dalamnya
        bekas, bekas_jenis = False, None
        if n > 1:
            i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
            penuh = isi_lubang((lb == i).astype(np.uint8))
            pejal = penuh.sum() / float(jw * jh)
            if st[i, cv2.CC_STAT_WIDTH] >= 0.9 * jw and st[i, cv2.CC_STAT_HEIGHT] >= 0.9 * jh and pejal > 0.8:
                e = max(2, int(jh * 0.035))
                gelang = (penuh > 0) & (cv2.erode(penuh, np.ones((2 * e + 1, 2 * e + 1), np.uint8)) == 0) & (kot > 0)
                vb = lbl[gelang]
                vb = vb[vb >= 0]
                if len(vb):
                    domb = int(np.bincount(vb).argmax())
                    jarak = np.sqrt(((Lr[ay0:ay1, ax0:ax1] - pusat[domb]) ** 2).sum(axis=2))
                    dalam = cv2.erode(penuh, np.ones((2 * e + 1, 2 * e + 1), np.uint8))
                    t = ((jarak > 30) & (dalam > 0)).astype(np.uint8)
                    t = cv2.morphologyEx(t, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
                    # garis luar sahaja: tepat di dalam sempadan bukan warna sempadan, dan kawasan bukan-sempadan
                    # ialah SATU kawasan besar (latar dalam kotak), bukan beberapa huruf
                    k3 = np.ones((6 * e + 1, 6 * e + 1), np.uint8)
                    dalam_ring = (dalam > 0) & (cv2.erode(penuh, k3) == 0)
                    nt, lt, stt, _ = cv2.connectedComponentsWithStats(t, 8)
                    terbesar = stt[1:, cv2.CC_STAT_AREA].max() / max(1, t.sum()) if nt > 1 else 0
                    garis_luar = dalam_ring.any() and t[dalam_ring].mean() > 0.6 and terbesar > 0.8
                    if garis_luar:
                        bekas_jenis = "garis luar"
                        t2 = ((jarak <= 30) & (cv2.erode(penuh, k3) > 0)).astype(np.uint8)
                        if t2.sum() > 20:
                            kot = t2                      # teks = warna sempadan, di dalam garis luar
                    elif t.sum() > 0.1 * jw * jh:
                        bekas, dom, bekas_jenis = True, domb, "pejal"
                        vt = lbl[t > 0]
                        wt = int(np.bincount(vt[vt >= 0]).argmax()) if (vt >= 0).any() else ibg
        if not bekas:
            # hiasan sisi: komponen leper (garis), atau warna yang jauh berbeza daripada teks jalur itu
            t = kot.copy()
            if bekas_jenis == "garis luar":
                n, lb, st, _ = cv2.connectedComponentsWithStats(kot, 8)
                elemen.append(dict(jenis="bekas garis luar", kotak_pct=_kpct(ax0, ay0, ax1, ay1, bx0, by0, bw, bh),
                                   warna=hexa(lab_ke_rgb(pusat[dom])), baris=len(baris) + 1))
            for i in range(1, n):
                cw, ch = st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT]
                vv = lbl[lb == i]
                vv = vv[vv >= 0]
                li = int(np.bincount(vv).argmax()) if len(vv) else dom
                leper = cw / max(1, ch) >= 4 and ch <= 0.9 * jh and st[i, cv2.CC_STAT_AREA] / (cw * ch) > 0.4
                lain = np.linalg.norm(pusat[li] - pusat[dom]) > 40 and st[i, cv2.CC_STAT_AREA] > 0.002 * jw * jh
                if leper or lain:
                    cx, cy = st[i, cv2.CC_STAT_LEFT], st[i, cv2.CC_STAT_TOP]
                    elemen.append(dict(jenis="garis" if leper else "hiasan warna lain",
                                       kotak_pct=_kpct(ax0 + cx, ay0 + cy, ax0 + cx + cw, ay0 + cy + ch,
                                                       bx0, by0, bw, bh),
                                       warna=hexa(lab_ke_rgb(pusat[li]))))
                    t[lb == i] = 0
            vt = lbl[t > 0]
            wt = int(np.bincount(vt[vt >= 0]).argmax()) if (vt >= 0).any() else dom
        u = ukur_baris(t, bw, bh, bx0 - ax0)
        if u is None:
            continue
        ty, _ = np.nonzero(t)
        rekod = dict(n=len(baris) + 1, atas_pct=round((ay0 - by0) / bh * 100, 1),
                     tinggi_pct=round((ty.max() + 1 - ty.min()) / bh * 100, 1),
                     jalur_tinggi_pct=round(jh / bh * 100, 1), warna_teks=hexa(lab_ke_rgb(pusat[wt])),
                     dalam_bekas=bekas, bekas=bekas_jenis, **u)
        if bekas:
            rekod["warna_bekas"] = hexa(lab_ke_rgb(pusat[dom]))
            rekod["bekas_lebar_pct"] = round(jw / bw * 100, 1)
            elemen.append(dict(jenis="bekas (kotak / label)", kotak_pct=_kpct(ax0, ay0, ax1, ay1, bx0, by0, bw, bh),
                               warna=rekod["warna_bekas"], baris=rekod["n"]))
        rekod["_y"] = [int(ay0), int(ay1)]
        rekod["_x"] = [int(ax0), int(ax1)]
        baris.append(rekod)

    # ---- hierarki, jarak, penjajaran
    tg = [r["tinggi_pct"] for r in baris]
    utama = [r for r in baris if r["tinggi_pct"] >= 0.6 * max(tg)] if baris else []
    for r in baris:
        r["peranan_saiz"] = "utama" if r in utama else "kecil"
    sela = [round((baris[i + 1]["_y"][0] - baris[i]["_y"][1]) / bh * 100, 1) for i in range(len(baris) - 1)]
    jajar, serak = "satu baris", None
    if len(baris) >= 2:
        ki = np.array([r["kotak_blok_pct"][0] for r in baris])
        ka = np.array([r["kotak_blok_pct"][1] for r in baris])
        sd = dict(kiri=ki.std(), kanan=ka.std(), tengah=((ki + ka) / 2).std())
        if max(sd["kiri"], sd["kanan"]) < 4:
            jajar = "sama lebar (kiri dan kanan rata)"
        else:
            kecil = min(sd, key=sd.get)
            jajar = "rata " + kecil if kecil != "tengah" else "tengah"
        serak = round(float(min(sd.values())), 1)
    if len(baris) <= 1 and bh / h > 0.3:
        amaran.append("hanya %d baris dikesan pada blok tinggi: baris mungkin bertindih dan tergabung" % len(baris))

    # ---- warna
    kong = np.bincount(peta.ravel(), minlength=len(pusat)) / peta.size * 100
    teks_hex = {r["warna_teks"] for r in baris}
    bekas_hex = {r.get("warna_bekas") for r in baris} - {None}
    pal = []
    for i in np.argsort(-kong):
        hx = hexa(lab_ke_rgb(pusat[i]))
        de = float(np.linalg.norm(pusat[i] - bg))
        if i == ibg:
            per = "latar"
        elif hx in bekas_hex:
            per = "bekas (kotak / label)"
        elif hx in teks_hex:
            per = "teks"
        elif de < 30:
            per = "ton latar (bayang atau tekstur latar)"
        else:
            per = "dakwat lain (hiasan, bayang atau tekstur huruf)"
        pal.append(dict(hex=hx, kongsi_pct=round(float(kong[i]), 1), peranan=per, beza_dari_latar=round(de, 1)))
    for p in pal:
        if p["peranan"].startswith("dakwat lain") and p["kongsi_pct"] < 1.5:
            p["peranan"] = "peralihan tepi (antialias)"
    # dakwat = warna teks / bekas; ton yang sama (beza a,b < 25) dikira SATU dakwat bertekstur
    hx2i = {hexa(lab_ke_rgb(pusat[i])): i for i in range(len(pusat))}
    kump = []
    for p in pal:
        if p["peranan"] in ("teks", "bekas (kotak / label)") or p["peranan"].startswith("dakwat lain"):
            i = hx2i[p["hex"]]
            if i == ibg:
                continue
            for g in kump:
                if np.linalg.norm(pusat[g["ahli"][0]][1:] - pusat[i][1:]) < 25 and \
                        abs(pusat[g["ahli"][0]][0] - pusat[i][0]) < 45:
                    g["ahli"].append(i)
                    g["kongsi_pct"] = round(g["kongsi_pct"] + p["kongsi_pct"], 1)
                    break
            else:
                if not p["peranan"].startswith("dakwat lain"):
                    kump.append(dict(hex=p["hex"], kongsi_pct=p["kongsi_pct"], peranan=p["peranan"], ahli=[i]))
    bil_dakwat = len(kump)

    # ---- tekstur
    luar = cv2.erode(1 - m, np.ones((9, 9), np.uint8)) > 0
    dlm = cv2.erode(m, np.ones((5, 5), np.uint8)) > 0
    sd_latar = float(L[..., 0][luar].std()) if luar.any() else 0.0
    sds, berat = [], []
    for g in kump:
        px = L[..., 0][dlm & np.isin(peta, g["ahli"])]
        if len(px) > 50:
            sds.append(float(px.std()))
            berat.append(len(px))
        g["ton"] = len(g["ahli"])
        del g["ahli"]
    sd_dakwat = float(np.average(sds, weights=berat)) if sds else 0.0
    antara = float(((d > amb * 0.45) & (d <= amb) & (cv2.dilate(m, np.ones((15, 15), np.uint8)) > 0) &
                    (cv2.dilate(m, np.ones((3, 3), np.uint8)) == 0)).mean() * 100)
    kelas_t = lambda s: "rata" if s < 2.5 else "berbutir halus" if s < 6 else "kasar / grunge"
    pecah_utama = float(np.mean([r["pecah_pct"] for r in utama])) if utama else 0.0

    rekod = dict(
        versi=VERSI, fail=Path(path).name, sha1=hashlib.sha1(Path(path).read_bytes()).hexdigest()[:12],
        tarikh=str(date.today()), sumber_medan="diukur skrip (kecuali kumpulan 'mata' = mata Claude)",
        kanvas=dict(w=w, h=h, nisbah=round(w / h, 3)), amaran=amaran,
        susunan=dict(
            condong_darjah=sudut, kotak_blok=[x0, y0, x1, y1],
            tepi_pct=dict(kiri=round(x0 / w * 100, 1), kanan=round((w - x1) / w * 100, 1),
                          atas=round(y0 / h * 100, 1), bawah=round((h - y1) / h * 100, 1)),
            tepi_min_pct=round(min(x0, w - x1) / w * 100 if min(x0, w - x1) / w < min(y0, h - y1) / h
                               else min(y0, h - y1) / h * 100, 1),
            pusat_dx_pct=round(((x0 + x1) / 2 - w / 2) / w * 100, 1),
            pusat_dy_pct=round(((y0 + y1) / 2 - h / 2) / h * 100, 1),
            nisbah_blok=round((x1 - x0) / (y1 - y0), 3), liputan_dakwat_pct=round(float(m.mean()) * 100, 1),
            isian_blok_pct=round(float(m[y0:y1, x0:x1].mean()) * 100, 1),
            bil_baris=len(baris), penjajaran=jajar, serakan_penjajaran_pct=serak, sela_baris_pct=sela,
            hierarki_nisbah=round(max(tg) / min(tg), 2) if tg else None,
            baris_tertinggi=int(np.argmax(tg)) + 1 if tg else None, ambang_dakwat=amb),
        baris=[{k: v for k, v in r.items() if not k.startswith("_")} for r in baris],
        elemen=elemen,
        warna=dict(latar=hexa(lab_ke_rgb(bg)), bil_dakwat=bil_dakwat, dakwat=kump, palet=pal),
        tekstur=dict(latar_sd=round(sd_latar, 2), latar=kelas_t(sd_latar), dakwat_sd=round(sd_dakwat, 2),
                     dakwat=kelas_t(sd_dakwat), huruf_pecah_pct=round(pecah_utama, 1),
                     bayang_lembut_pct=round(antara, 2)),
        mata={})
    if semak:
        _lukis_semak(rr, baris, elemen, (bx0, by0, bw, bh), semak)
    return rekod


def _kpct(ax0, ay0, ax1, ay1, bx0, by0, bw, bh):
    return [round((ax0 - bx0) / bw * 100, 1), round((ay0 - by0) / bh * 100, 1),
            round((ax1 - bx0) / bw * 100, 1), round((ay1 - by0) / bh * 100, 1)]


def _lukis_semak(rr, baris, elemen, blok, path):
    bx0, by0, bw, bh = blok
    im = rr.copy()
    cv2.rectangle(im, (bx0, by0), (bx0 + bw, by0 + bh), (0, 160, 255), 2)
    for r in baris:
        col = (255, 0, 200) if r["dalam_bekas"] else (0, 200, 0)
        cv2.rectangle(im, (r["_x"][0], r["_y"][0]), (r["_x"][1], r["_y"][1]), col, 3)
        cv2.putText(im, "%d %s" % (r["n"], r["kelas_anggaran"][:10]), (r["_x"][0] + 4, r["_y"][0] + 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, col, 2)
    for e in elemen:
        if e["jenis"] != "bekas (kotak / label)":
            k = e["kotak_pct"]
            cv2.rectangle(im, (int(bx0 + k[0] * bw / 100), int(by0 + k[1] * bh / 100)),
                          (int(bx0 + k[2] * bw / 100), int(by0 + k[3] * bh / 100)), (255, 60, 60), 3)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(im).save(path, quality=85)


def gabung_mata(rekod, folder):
    f = Path(folder) / "mata" / (Path(rekod["fail"]).stem + ".json")
    if f.exists():
        rekod["mata"] = json.loads(f.read_text())
        rekod["mata"]["sumber"] = "mata Claude"
    return rekod


if __name__ == "__main__":
    a = sys.argv[1:]
    keluar = Path(a[a.index("--keluar") + 1]) if "--keluar" in a else KELUAR
    semak = "--semak" in a
    fail = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] != "--keluar")]
    if not fail:
        sys.exit(__doc__)
    keluar.mkdir(parents=True, exist_ok=True)
    for f in fail:
        r = decode(f, keluar / "semak" / (Path(f).stem + ".jpg") if semak else None)
        r = gabung_mata(r, keluar)
        (keluar / (Path(f).stem + ".json")).write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n")
        s = r.get("susunan", {})
        print(json.dumps(dict(fail=r["fail"], baris=s.get("bil_baris"), condong=s.get("condong_darjah"),
                              jajar=s.get("penjajaran"), dakwat=r.get("warna", {}).get("bil_dakwat"),
                              amaran=r.get("amaran")), ensure_ascii=False))
