#!/usr/bin/env python3
"""Potong setiap design daripada gambar grid rujukan Etsy dan ukur bentuknya.

Guna:
  python3 scripts/etsy_crop.py 1=IMG_5856.jpg:4x4 3=IMG_5858.jpg:4x4 ...

Setiap argumen: <no gambar>=<laluan fail>:<lajur>x<baris>.
Hasil:
  data/etsy/crops/etsy-<gambar>-<nn>.jpg   (tidak dikomit: karya penjual lain)
  data/etsy/crop_metrics.json              (kotak potong, nisbah, liputan dakwat)

Cara potong: piksel gelap (kelabu < 110) dikira dakwat. Baris grid dipisah pada
jalur kosong mendatar yang paling lebar, kemudian lajur pada jalur kosong
menegak yang paling lebar dalam baris itu. Piksel asal tidak diubah.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "data", "etsy", "crops")
METRICS = os.path.join(ROOT, "data", "etsy", "crop_metrics.json")
INK = 110      # kelabu di bawah nilai ini = dakwat
PAD = 12       # jidar sekeliling design (piksel)


def runs_of_zero(profile):
    """Senarai (mula, tamat) jalur kosong dalam profil 1D."""
    out, start = [], None
    for i, v in enumerate(profile):
        if v == 0 and start is None:
            start = i
        elif v != 0 and start is not None:
            out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(profile)))
    return out


def split(profile, n):
    """Pecah julat berdakwat kepada n bahagian pada n-1 jalur kosong terlebar."""
    idx = np.nonzero(profile)[0]
    lo, hi = int(idx[0]), int(idx[-1]) + 1
    gaps = [(a, b) for a, b in runs_of_zero(profile[lo:hi])]
    gaps = sorted(gaps, key=lambda g: g[1] - g[0], reverse=True)[: n - 1]
    if len(gaps) != n - 1:
        raise SystemExit(f"jumpa {len(gaps)} jalur kosong, perlu {n - 1}")
    gaps = sorted((a + lo, b + lo) for a, b in gaps)
    edges = [lo] + [x for g in gaps for x in g] + [hi]
    return [(edges[i], edges[i + 1]) for i in range(0, len(edges), 2)]


def main(argv):
    os.makedirs(OUT_DIR, exist_ok=True)
    rows_out = []
    for arg in argv:
        no, rest = arg.split("=", 1)
        path, grid = rest.rsplit(":", 1)
        ncol, nrow = (int(x) for x in grid.split("x"))
        im = Image.open(path).convert("RGB")
        W, H = im.size
        ink = np.asarray(im.convert("L")) < INK
        # hingar JPEG: abaikan baris/lajur dengan kurang daripada 2 piksel dakwat
        rp = ink.sum(axis=1)
        rp[rp < 2] = 0
        n = 0
        for (y0, y1) in split(rp, nrow):
            cp = ink[y0:y1].sum(axis=0)
            cp[cp < 2] = 0
            for (x0, x1) in split(cp, ncol):
                n += 1
                sub = ink[y0:y1, x0:x1]
                ys = np.nonzero(sub.any(axis=1))[0]
                ty0, ty1 = y0 + int(ys[0]), y0 + int(ys[-1]) + 1
                bw, bh = x1 - x0, ty1 - ty0
                box = (max(0, x0 - PAD), max(0, ty0 - PAD), min(W, x1 + PAD), min(H, ty1 + PAD))
                name = f"etsy-{no}-{n:02d}.jpg"
                im.crop(box).save(os.path.join(OUT_DIR, name), quality=95, subsampling=0)
                rows_out.append({
                    "id": f"{no}-{n:02d}",
                    "gambar": int(no),
                    "fail_asal": os.path.basename(path),
                    "baris": (n - 1) // ncol + 1,
                    "lajur": (n - 1) % ncol + 1,
                    "crop": name,
                    "kotak": list(box),
                    "lebar_px": bw,
                    "tinggi_px": bh,
                    "nisbah": round(bw / bh, 2),
                    "dakwat_pct": round(100 * float(ink[ty0:ty1, x0:x1].mean()), 1),
                })
        print(f"gambar {no}: {n} design ({ncol}x{nrow})")
    with open(METRICS, "w") as f:
        json.dump(rows_out, f, indent=1)
    print(f"{len(rows_out)} design -> {OUT_DIR}")


if __name__ == "__main__":
    main(sys.argv[1:])
