"""SK05 Ukuran (Standard Lettering v1.2, langkah 1 dan 5b). Versi 1.1, 26 Nov 2026.
v1.1: 'sentuh_tepi' kini hanya blok tulisan; bintik latar di tepi (kad K6, K8) dilapor sebagai 'bintik_tepi' dan
      tidak lagi menggagalkan imej (ditemui pada larian pertama, ERNIE K8G seed 123).

Tugas: ukur blok tulisan pada satu gambar: ruang tepi, kedudukan, sudut condong, kelabu, baris.
Dipakai dua cara:
  1. Langkah 1: ukur GAMBAR UPLOAD (rujukan) -> angka rujukan Kad Gaya (bukan tekaan).
  2. Langkah 5b: ukur imej mentah hitam putih sebelum dan selepas skrip pembetulan SK01-SK04.
Diperlukan oleh: semua kad (set asas). Diuji pada: upload IMG_5775 (K3), IMG_5734 (K6) dan 24 imej K3H sedia ada.
Parameter kad: tiada (skrip ini yang menghasilkan parameter).
Had: latar mesti rata (satu warna). Sudut = arah garis dasar baris (unjuran baris), bukan condong italik huruf.
     Baris yang bertindih tidak dapat diasingkan; 'baris' ialah anggaran sahaja.

Guna: python3 SK05_ukur.py <gambar> [...]      -> satu baris JSON bagi setiap gambar
"""
import json
import sys

import cv2
import numpy as np
from PIL import Image

VERSI = "SK05 v1.1"


def muat(path):
    return np.array(Image.open(path).convert("RGB"))


def latar(rgb):
    """Warna latar = median jalur 3% di keempat-empat tepi."""
    h, w = rgb.shape[:2]
    t = max(2, int(min(h, w) * 0.03))
    tepi = np.concatenate([rgb[:t].reshape(-1, 3), rgb[-t:].reshape(-1, 3), rgb[:, :t].reshape(-1, 3),
                           rgb[:, -t:].reshape(-1, 3)])
    return np.median(tepi, axis=0)


def topeng(rgb, ambang=60, min_bahagian=0.0005):
    """Topeng dakwat (beza daripada latar). Pulang (blok, semua): 'blok' membuang bintik kecil (bintang, percikan)
    supaya kotak blok tidak ditarik oleh hiasan latar; 'semua' = setiap piksel dakwat."""
    d = np.abs(rgb.astype(np.int16) - latar(rgb).astype(np.int16)).max(axis=2)
    semua = (d > ambang).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(semua, 8)
    simpan = np.zeros(n, bool)
    simpan[1:] = st[1:, cv2.CC_STAT_AREA] >= min_bahagian * semua.size
    return simpan[lab].astype(np.uint8), semua


def _skor(m, a):
    h, w = m.shape
    r = cv2.warpAffine(m, cv2.getRotationMatrix2D((w / 2, h / 2), a, 1), (w, h))
    p = r.sum(axis=1)
    return float(((p[1:] - p[:-1]) ** 2).sum())


def condong(blok):
    """Sudut garis dasar baris dalam darjah; positif = baris naik ke kanan. Kaedah unjuran baris (cari putaran
    yang menjadikan baris paling mendatar), langkah 0.5 kemudian 0.1 darjah, julat +-15."""
    s = 400 / blok.shape[1]
    m = cv2.resize(blok * 255, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32)
    pad = int(max(m.shape) * 0.15)
    m = cv2.copyMakeBorder(m, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    a0 = max(np.arange(-15, 15.01, 0.5), key=lambda a: _skor(m, a))
    a1 = max(np.arange(a0 - 0.5, a0 + 0.51, 0.1), key=lambda a: _skor(m, a))
    return round(-float(a1), 1)


def baris(blok, sudut):
    """Anggaran jalur baris selepas blok diluruskan: senarai tinggi jalur sebagai % tinggi blok."""
    h, w = blok.shape
    r = cv2.warpAffine(blok, cv2.getRotationMatrix2D((w / 2, h / 2), -sudut, 1), (w, h))
    p = r.sum(axis=1).astype(float)
    if p.max() == 0:
        return []
    ada = p > 0.08 * p.max()
    jalur, mula = [], None
    for y, v in enumerate(list(ada) + [False]):
        if v and mula is None:
            mula = y
        elif not v and mula is not None:
            jalur.append([mula, y])
            mula = None
    gab = []
    for j in jalur:  # gabung sela kurang 1% tinggi
        if gab and j[0] - gab[-1][1] < 0.01 * h:
            gab[-1][1] = j[1]
        else:
            gab.append(j)
    gab = [j for j in gab if j[1] - j[0] >= 0.02 * h]
    jumlah = gab[-1][1] - gab[0][0] if gab else 0
    return [round((b - a) / jumlah * 100, 1) for a, b in gab] if jumlah else []


def ukur(rgb, min_bahagian=0.0005):
    """Semua ukuran satu gambar. Peratus ruang tepi dikira daripada lebar (kiri, kanan) dan tinggi (atas, bawah)."""
    h, w = rgb.shape[:2]
    blok, semua = topeng(rgb, min_bahagian=min_bahagian)
    ys, xs = np.nonzero(blok)
    if len(xs) == 0:
        return dict(w=w, h=h, kosong=True)
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()) + 1, int(ys.min()), int(ys.max()) + 1
    bw, bh = x1 - x0, y1 - y0
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    kelabu = (g > 40) & (g < 215)
    julat = cv2.dilate(g, np.ones((5, 5), np.uint8)).astype(np.int16) - cv2.erode(g, np.ones((5, 5), np.uint8))
    sudut = condong(blok)
    return dict(
        w=w, h=h, kotak=[x0, y0, x1, y1],
        tepi=dict(kiri=round(x0 / w * 100, 1), kanan=round((w - x1) / w * 100, 1), atas=round(y0 / h * 100, 1),
                  bawah=round((h - y1) / h * 100, 1)),
        # ruang tepi blok jika dipusatkan: sisi yang paling sempit (lebar atau tinggi)
        tepi_pct=round(min((1 - bw / w) / 2, (1 - bh / h) / 2) * 100, 1),
        pusat_dx_pct=round(((x0 + x1) / 2 - w / 2) / w * 100, 1), pusat_dy_pct=round(((y0 + y1) / 2 - h / 2) / h * 100, 1),
        condong_darjah=sudut,
        kelabu_pct=round(float(kelabu.mean()) * 100, 2),
        kelabu_rata_pct=round(float((kelabu & (julat < 50)).mean()) * 100, 2),
        latar=[int(v) for v in latar(rgb)],
        # huruf / blok menyentuh tepi kanvas (mungkin terpotong). Bintik latar kecil (bintang, titik) dikira berasingan.
        sentuh_tepi=bool(blok[0].any() or blok[-1].any() or blok[:, 0].any() or blok[:, -1].any()),
        bintik_tepi=bool(semua[0].any() or semua[-1].any() or semua[:, 0].any() or semua[:, -1].any()),
        baris=baris(blok, sudut), versi=VERSI)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(json.dumps(dict(fail=f, **ukur(muat(f))), ensure_ascii=False))
