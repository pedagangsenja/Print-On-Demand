"""Asas bersama skrip pembetulan SK01-SK04 (Standard Lettering v1.2, langkah 5b). Versi 1, 26 Nov 2026.

Rujukan = angka kad yang dibandingkan dengan ukuran imej. Sumber, ikut keutamaan:
  1. hujah baris arahan (--condong, --tepi): untuk kad yang baru dibuat daripada gambar upload;
  2. kad.BLOK[kad]["rujukan"]: angka yang diukur SK05 daripada gambar upload;
  3. kad.KAD[kad]["ruang_tepi"]: angka kad (ruang tepi sahaja).
Tiada angka rujukan = pembetulan itu TIDAK dijalankan (standard 5b).
HAD = had toleransi SEMENTARA (cadangan Claude 26 Nov 2026, belum ditetapkan daripada ujian; standard 5b).
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kad  # noqa: E402
from SK05_ukur import latar, muat, ukur  # noqa: E402,F401

HAD = dict(condong=1.5, tepi=2.0, pusat=1.5, kelabu_rata=0.3, latar=4)   # darjah, mata %, % kanvas, % piksel, aras 0-255


def rujukan(kid, condong=None, tepi=None):
    b = kad.BLOK[kid]
    r = dict(tepi_pct=kad.KAD[kid]["ruang_tepi"], condong_darjah=None, kad_condong=bool(b.get("condong")),
             kad_bayang="shadow" in b.get("tepi", ""), sumber="kad")
    if b.get("rujukan"):
        r.update(b["rujukan"])
    if condong is not None:
        r.update(condong_darjah=float(condong), sumber="baris arahan")
    if tepi is not None:
        r.update(tepi_pct=float(tepi), sumber="baris arahan")
    return r


def tiga(m):
    return np.vstack([m, [0, 0, 1]])


def lukis(rgb, M, halus=True):
    """Guna satu matriks affine 3x3 pada imej; bucu diisi warna latar."""
    h, w = rgb.shape[:2]
    return cv2.warpAffine(rgb, M[:2], (w, h), flags=cv2.INTER_LANCZOS4 if halus else cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=[float(v) for v in latar(rgb)])


def simpan(rgb, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgb).save(path)


def cli(modul):
    """Jalankan SATU skrip pembetulan: python3 SKxx_nama.py <imej> <kad> <keluar.png> [--condong D] [--tepi P]"""
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(cli.__doc__)
    pil = {a[i][2:]: a[i + 1] for i in range(3, len(a) - 1, 2)}
    rgb, ruj = muat(a[0]), rujukan(a[1], pil.get("condong"), pil.get("tepi"))
    hasil, cat = modul.betul(rgb, ruj)
    simpan(hasil, a[2])
    print(json.dumps(dict(skrip=modul.ID, **cat, selepas=ukur(hasil)), ensure_ascii=False))
