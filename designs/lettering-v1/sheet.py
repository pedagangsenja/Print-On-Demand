"""Helaian semakan QC: imej K6 satu enjin (3 ayat x 2 seed) dalam satu grid, untuk semakan mata."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
d, out = Path(sys.argv[1]), sys.argv[2]
ids = [f"K6{a}_s{s}" for a in "PDL" for s in (42, 7)]
w, h = 384, 512
sheet = Image.new("RGB", (w * 3, h * 2), "gray")
for i, n in enumerate(ids):
    f = d / f"{n}.png"
    if not f.exists():
        continue
    im = Image.open(f).convert("RGB").resize((w, h))
    ImageDraw.Draw(im).text((6, 6), n, fill="red")
    sheet.paste(im, ((i // 2) * w, (i % 2) * h))
sheet.save(out, quality=88)
