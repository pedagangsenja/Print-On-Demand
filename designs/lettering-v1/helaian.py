"""Helaian semakan QC (Standard Lettering v1.2, langkah 5 dan 7): satu design (id), baris = model, lajur = seed.
Guna: python3 helaian.py <folder hasil> <id> <keluar.jpg> [--lebar 360] [model ...]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

a = sys.argv[1:]
lebar = 360
if "--lebar" in a:
    i = a.index("--lebar"); lebar = int(a[i + 1]); del a[i:i + 2]
d, idd, out = Path(a[0]), a[1], a[2]
model = a[3:] or sorted(p.name for p in d.iterdir() if p.is_dir())
seed = sorted({int(f.stem.split("_s")[1]) for m in model for f in (d / m).glob(f"{idd}_s*.png")},
              key=lambda s: [42, 7, 123, 2024].index(s) if s in (42, 7, 123, 2024) else 99)
w, h = lebar, lebar * 4 // 3
sh = Image.new("RGB", (w * max(1, len(seed)), h * len(model)), (60, 60, 60))
for r, m in enumerate(model):
    for c, s in enumerate(seed):
        f = d / m / f"{idd}_s{s}.png"
        if not f.exists():
            continue
        im = Image.open(f).convert("RGB").resize((w, h))
        dr = ImageDraw.Draw(im)
        dr.rectangle([0, 0, w - 1, h - 1], outline=(90, 90, 90))
        dr.rectangle([0, 0, 150, 16], fill=(0, 0, 0)); dr.text((4, 3), f"{m} {idd} s{s}", fill=(255, 80, 80))
        sh.paste(im, (c * w, r * h))
Path(out).parent.mkdir(parents=True, exist_ok=True)
sh.save(out, quality=86)
print(out, sh.size, model, seed)
