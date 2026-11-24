"""Helaian semakan (contact sheet): satu imej untuk semakan ejaan + gaya (jimat token semakan mata).

Guna: python3 scripts/lettering/sheet.py <out.jpg> <tinggi_sel> <label=path> [label=path ...]
Sel disusun 6 satu baris; label ditulis di bawah setiap sel.
"""
import sys

from PIL import Image, ImageDraw


def main():
    out, h = sys.argv[1], int(sys.argv[2])
    cells = [a.split("=", 1) for a in sys.argv[3:]]
    w = h * 3 // 4
    cols = min(6, len(cells))
    rows = (len(cells) + cols - 1) // cols
    pad, lab = 8, 22
    sheet = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + lab + pad) + pad), "white")
    d = ImageDraw.Draw(sheet)
    for n, (label, path) in enumerate(cells):
        im = Image.open(path).convert("RGB")
        im.thumbnail((w, h), Image.LANCZOS)
        x = pad + (n % cols) * (w + pad)
        y = pad + (n // cols) * (h + lab + pad)
        sheet.paste(im, (x + (w - im.width) // 2, y + (h - im.height) // 2))
        d.text((x + 4, y + h + 4), label, fill="black")
    sheet.save(out, quality=85)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
