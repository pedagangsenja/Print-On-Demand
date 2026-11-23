"""Semak ejaan dengan Tesseract + buat lembaran banding (contact sheet). Guna: python3 -I score.py"""
import json, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
P = json.loads((HERE / "prompts.json").read_text())
MODELS = [m for m in ["klein4b", "zimage", "ernie"] if (HERE / "out" / m).exists()]


def words(s):
    return re.findall(r"[A-Z']+", s.upper().replace("’", "'"))


def ocr(png):
    img = Image.open(png).convert("L")
    txt = ""
    for inv in (False, True):  # cuba teks gelap atas cerah dan sebaliknya
        im = ImageOps.invert(img) if inv else img
        tmp = png.with_suffix(".ocr.png"); im.save(tmp)
        r = subprocess.run(["tesseract", str(tmp), "-", "--psm", "11"], capture_output=True, text=True)
        tmp.unlink()
        txt += " " + r.stdout
    return txt


def main():
    res = {}
    for m in MODELS:
        times = json.loads((HERE / "out" / m / "times.json").read_text()) if (HERE / "out" / m / "times.json").exists() else {}
        for p in P:
            png = HERE / "out" / m / f"{p['id']}.png"
            if not png.exists():
                continue
            want = words(p["text"]); got = set(words(ocr(png)))
            hit = [w for w in want if w in got]
            res.setdefault(m, {})[p["id"]] = {"ocr_hit": len(hit), "ocr_total": len(want), "missing": [w for w in want if w not in got],
                                                "seconds": times.get(p["id"], {}).get("seconds")}
    (HERE / "scores.json").write_text(json.dumps(res, indent=1))
    # lembaran: baris = prompt, lajur = model
    tw, pad, lab = 300, 10, 34
    font = ImageFont.load_default(size=16)
    for half, ids in (("A", P[:5]), ("B", P[5:])):
        rows = len(ids); cols = len(MODELS)
        th = max(int(tw * p["h"] / p["w"]) for p in ids)
        sheet = Image.new("RGB", (220 + cols * (tw + pad) + pad, lab + rows * (th + pad + 20) + pad), "white")
        d = ImageDraw.Draw(sheet)
        for j, m in enumerate(MODELS):
            d.text((220 + pad + j * (tw + pad), 8), m, fill="black", font=font)
        for i, p in enumerate(ids):
            y = lab + i * (th + pad + 20)
            d.multiline_text((8, y + 4), p["id"] + "\n" + "\n".join(p["text"].split(" / ")), fill="black", font=ImageFont.load_default(size=13))
            for j, m in enumerate(MODELS):
                png = HERE / "out" / m / f"{p['id']}.png"
                x = 220 + pad + j * (tw + pad)
                if png.exists():
                    im = Image.open(png).convert("RGB"); im.thumbnail((tw, th)); sheet.paste(im, (x, y))
                    r = res[m][p["id"]]
                    d.text((x, y + th + 2), f"OCR {r['ocr_hit']}/{r['ocr_total']}  {r['seconds']} s", fill="black", font=ImageFont.load_default(size=13))
        sheet.save(HERE / f"sheet_{half}.png")
    print(json.dumps({m: sum(v['ocr_hit'] for v in r.values()) for m, r in res.items()}))


if __name__ == "__main__":
    main()
