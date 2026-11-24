"""Lukis panduan susun atur: teks baharu dalam susun atur, warna dan jenis huruf yang hampir sama dengan 3 imej gaya.
Font Google Fonts berlesen SIL OFL 1.1 (hasil cetakan boleh dijual; font itu sendiri tidak boleh dijual).
Hasil: guides/<T>_<S>.png (768x1024) dan guides/sheet.png. Guna: python3 make_guides.py"""
import json, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
F = HERE / "fonts"
G = HERE / "guides"
W, H = 768, 1024
YEL, WHITE, BEIGE, BLACK = (246, 190, 0), (245, 245, 240), (205, 189, 160), (8, 8, 8)

# Peranan setiap baris untuk gaya S1: (teks, saiz relatif, warna)
S1_ROLES = {
    "T1": [("PROGRESS", 3, WHITE), ("OVER", 1.2, WHITE), ("PERFECTION", 4, YEL)],
    "T2": [("SMALL STEPS", 3, WHITE), ("EVERY DAY", 1.2, WHITE), ("LEAD TO", 1.2, WHITE), ("BIG RESULTS", 4, YEL)],
    "T3": [("YOUR ONLY LIMIT", 2.2, WHITE), ("IS THE ONE YOU SET", 1.1, WHITE), ("GET UP", 2.2, YEL), ("SHOW UP", 2.2, WHITE),
           ("NEVER GIVE UP", 2.2, YEL), ("THE BEST VIEW COMES", 1.1, WHITE), ("AFTER THE HARDEST CLIMB", 2.2, YEL)],
}


def text_img(txt, font, fill):
    """Teks pada kanvas lutsinar yang dipotong rapat."""
    l, t, r, b = font.getbbox(txt)
    im = Image.new("RGBA", (r - l + 20, b - t + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - l, 10 - t), txt, font=font, fill=fill)
    return im.crop(im.getbbox())


def grunge(im, rnd, density=0.012):
    """Bintik dan calar hitam atas huruf (tekstur cetakan lusuh)."""
    m = Image.new("L", im.size, 255)
    d = ImageDraw.Draw(m)
    for _ in range(int(im.size[0] * im.size[1] * density / 40)):
        x, y = rnd.randrange(im.size[0]), rnd.randrange(im.size[1])
        r = rnd.choice([1, 1, 2, 3])
        d.ellipse((x - r, y - r, x + r, y + r), fill=0)
    for _ in range(60):
        x, y = rnd.randrange(im.size[0]), rnd.randrange(im.size[1])
        d.line((x, y, x + rnd.randint(-40, 40), y + rnd.randint(-6, 6)), fill=0, width=1)
    a = im.getchannel("A")
    im.putalpha(Image.composite(a, Image.new("L", im.size, 0), m))
    return im


def s1(tid, rnd):
    im = Image.new("RGB", (W, H), BLACK)
    rows = S1_ROLES[tid]
    font = ImageFont.truetype(str(F / "Anton-Regular.ttf"), 220)
    x0, x1, top, bot, gap = 70, W - 70, 70, H - 190, 12
    unit = (bot - top - gap * (len(rows) - 1)) / sum(r[1] for r in rows)
    y = top
    first_small = True
    for txt, wgt, col in rows:
        h = int(unit * wgt)
        small = wgt < 2
        t = text_img(txt, font, col)
        w = int(min((x1 - x0) * (0.62 if small else 1.0), t.size[0] * h / t.size[1] * 1.15))  # kekal condensed
        t = t.resize((w, h), Image.LANCZOS)
        t = grunge(t, rnd)
        xs = x1 - w if small else x0 + ((x1 - x0) - w) // 2 * 0
        im.paste(t, (xs, y), t)
        if small and first_small:  # jalur amaran kuning + bar putih seperti imej rujukan
            d = ImageDraw.Draw(im)
            d.rectangle((x0, y + h * 0.15, xs - 22, y + h * 0.85), fill=YEL)
            for k in range(3):
                bx = x0 + 18 + k * 34
                d.polygon([(bx, y + h * 0.85), (bx + 14, y + h * 0.85), (bx + 34, y + h * 0.15), (bx + 20, y + h * 0.15)], fill=BLACK)
            d.rectangle((xs, y - gap + 2, x1, y - 2), fill=WHITE)
            first_small = False
        y += h + gap
    d = ImageDraw.Draw(im)  # kurungan gelembung kata di bawah
    yb = bot + 40
    d.line([(x0 + 60, yb), (x1, yb), (x1, yb + 40), (x0 + 330, yb + 40), (x0 + 300, yb + 85), (x0 + 280, yb + 40)], fill=WHITE, width=9)
    for k in range(4):
        d.line([(x0 + k * 14, yb + 60), (x0 + 10 + k * 14, yb + 40)], fill=WHITE, width=6)
    return im


def s2(lines, rnd):
    im = Image.new("RGB", (W, H), BLACK)
    font = ImageFont.truetype(str(F / "KaushanScript-Regular.ttf"), 200)
    n = len(lines)
    band = (H - 140) / n
    for i, txt in enumerate(lines):
        t = text_img(txt, font, WHITE)
        s = min((W - 90) / t.size[0], band * 1.25 / t.size[1])
        t = t.resize((int(t.size[0] * s), int(t.size[1] * s)), Image.LANCZOS).rotate(8, expand=True, resample=Image.BICUBIC)
        x = (W - t.size[0]) // 2 + rnd.randint(-25, 25)
        y = int(70 + i * band + band / 2 - t.size[1] / 2)
        im.paste(t, (x, y), t)
    d = ImageDraw.Draw(im)
    for _ in range(3 + n):  # garisan swash nipis
        pts, x, y = [], rnd.randint(-40, 120), rnd.randint(80, H - 80)
        for k in range(40):
            pts.append((x + k * 18, y - 60 * math.sin(k / 6.0) - k * 2))
        d.line(pts, fill=WHITE, width=rnd.choice([2, 3, 4]))
    for _ in range(70):  # percikan dakwat
        x, y, r = rnd.randrange(W), rnd.randrange(H), rnd.choice([2, 3, 4, 6])
        d.ellipse((x - r, y - r, x + r, y + r), fill=WHITE)
    return im


def s3(lines, rnd):
    im = Image.effect_noise((W, H), 18).point(lambda v: 6 + v // 18).convert("RGB")
    font = ImageFont.truetype(str(F / "CinzelDecorative-Black.ttf"), 200)
    n = len(lines)
    top, bot = 110, H - 110
    wts = [0.8 if len(t) > 12 else 1.25 for t in lines]
    unit = (bot - top) / sum(wts)
    d = ImageDraw.Draw(im)
    y = top
    for txt, wt in zip(lines, wts):
        h = unit * wt
        t = text_img(txt.replace(" ", "   "), font, BEIGE)
        s = min((W - 160) / t.size[0], h * 0.62 / t.size[1])
        t = t.resize((int(t.size[0] * s), int(t.size[1] * s)), Image.LANCZOS)
        tex = Image.effect_noise(t.size, 60).point(lambda v: 255 if v > 70 else 120)  # tekstur letterpress
        t.putalpha(Image.composite(t.getchannel("A"), Image.new("L", t.size, 0), tex))
        cy = int(y + h / 2)
        im.paste(t, ((W - t.size[0]) // 2, cy - t.size[1] // 2), t)
        for sgn in (-1, 1):  # garisan reben melengkung + daun kecil
            yy = cy + sgn * (t.size[1] // 2 + 10)
            d.arc((60, yy - 30, W - 60, yy + 30), 200 if sgn < 0 else 20, 340 if sgn < 0 else 160, fill=BEIGE, width=3)
            for k in range(2):
                lx = rnd.randint(140, W - 140)
                d.ellipse((lx, yy - 5, lx + 20, yy + 5), fill=BEIGE)
        y += h
    return im.filter(ImageFilter.GaussianBlur(0.4))


def main():
    G.mkdir(exist_ok=True)
    prompts = json.loads((HERE / "prompts.json").read_text())
    thumbs = []
    for p in prompts:
        rnd = random.Random(42)
        sid, tid = p["style_id"], p["text_id"]
        im = s1(tid, rnd) if sid == "S1" else s2(p["lines"], rnd) if sid == "S2" else s3(p["lines"], rnd)
        im.save(G / f"{p['id']}.png")
        thumbs.append(im.resize((256, 341)))
    sheet = Image.new("RGB", (256 * 3, 341 * 3), (40, 40, 40))
    for i, t in enumerate(thumbs):  # baris = gaya, lajur = teks
        sheet.paste(t, ((i % 3) * 256, (i // 3) * 341))
    sheet.save(G / "sheet.png")
    print("siap", len(thumbs))


if __name__ == "__main__":
    main()
