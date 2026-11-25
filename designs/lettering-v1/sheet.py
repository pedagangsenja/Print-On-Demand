"""Helaian semakan QC v1: satu baris setiap kad = rujukan + 6 imej (P, D, L x seed 42, 7).
Guna: python3 sheet.py <model> [kad...]  -> out/<model>/sheet_<kad>.png (satu helaian setiap kad, untuk semakan dekat)
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

import kad

HERE = Path(__file__).resolve().parent
FONT = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 26)
TW, TH = 480, 640


def tile(path, label):
    im = Image.new("RGB", (TW, TH + 40), (255, 255, 255))
    if path.exists():
        src = Image.open(path).convert("RGB")
        src.thumbnail((TW, TH))
        im.paste(src, ((TW - src.width) // 2, 40))
    ImageDraw.Draw(im).text((8, 6), label, font=FONT, fill=(20, 20, 20))
    return im


def main(model, kads):
    out = HERE / "out" / model
    for k in kads or kad.KAD:
        tiles = [tile(HERE / "refs" / f"{kad.KAD[k]['ref']}.jpg", f"{k} rujukan")]
        for a in kad.AYAT:
            for s in (42, 7):
                tiles.append(tile(out / f"{k}{a}_s{s}.png", f"{k}{a} s{s}"))
        sheet = Image.new("RGB", (TW * 4 + 30, (TH + 40) * 2 + 10), (200, 200, 200))
        sheet.paste(tiles[0], (0, 0))  # lajur = ayat P, D, L; baris = seed 42, 7
        for i, t in enumerate(tiles[1:]):
            sheet.paste(t, ((i // 2 + 1) * (TW + 10), (i % 2) * (TH + 50)))
        sheet.save(out / f"sheet_{k}.png")
        print(out / f"sheet_{k}.png")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
