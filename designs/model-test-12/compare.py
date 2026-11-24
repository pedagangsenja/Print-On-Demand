"""Bina helaian perbandingan (satu bagi setiap gaya) dan semakan ejaan OCR awal.
Baris: imej rujukan + panduan + setiap model; lajur: T1 pendek, T2 sederhana, T3 panjang.
OCR (RapidOCR) hanya saringan awal: ia sendiri salah baca huruf grunge/skrip, jadi keputusan akhir disemak dengan mata.
Guna: python3 compare.py  -> <scratch>/sheets/S1.png..S3.png dan <scratch>/sheets/ocr.json"""
import json, os, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
S = Path(os.environ.get("POD_SCRATCH", "/tmp/claude-0/-home-user-Print-On-Demand/2d722db7-85d8-5f5a-9afd-4d1e293d123c/scratchpad"))
OUT, SH = S / "out", S / "sheets"
MODELS = [("guide_klein4b", "klein 4B"), ("guide_zturbo", "Z-Image-Turbo"), ("guide_ernie", "ERNIE-Turbo"),
          ("guide_schnell", "FLUX.1-schnell"), ("guide_chroma_flash", "Chroma1-Flash"), ("guide_kandinsky", "Kandinsky 2.2"),
          ("guide_moss", "MOSS SFT"), ("klein4b", "klein 4B (teks sahaja)")]
TW, TH, LW = 300, 400, 170


def img_path(folder, pid):
    for n in (f"{pid}.png", f"{pid}_moss_s42.png"):
        if (OUT / folder / n).exists():
            return OUT / folder / n
    return None


def words(s):
    return re.findall(r"[A-Z]+", s.upper())


def ocr_score(engine, path, lines):
    res, _ = engine(str(path))
    got = words(" ".join(x[1] for x in (res or [])))
    want = words(" ".join(lines))
    hit = sum(1 for w in want if w in got)
    return round(hit / len(want), 2), " / ".join(x[1] for x in (res or []))


def main():
    from rapidocr_onnxruntime import RapidOCR
    eng = RapidOCR()
    SH.mkdir(exist_ok=True)
    prompts = json.loads((HERE / "prompts.json").read_text())
    font = ImageFont.truetype(str(HERE / "fonts" / "Anton-Regular.ttf"), 26)
    ocr = {}
    for sid in ("S1", "S2", "S3"):
        ps = [p for p in prompts if p["style_id"] == sid]
        rows = [("ref", "Imej rujukan"), ("guide", "Panduan")] + MODELS
        sheet = Image.new("RGB", (LW + TW * 3, TH * len(rows)), (235, 235, 235))
        d = ImageDraw.Draw(sheet)
        for r, (key, label) in enumerate(rows):
            d.text((10, r * TH + TH // 2 - 15), label, font=font, fill=(20, 20, 20))
            for c, p in enumerate(ps):
                if key == "ref":
                    path = HERE / p["ref"] if c == 0 else None
                elif key == "guide":
                    path = HERE / "guides" / f"{p['id']}.png"
                else:
                    path = img_path(key, p["id"])
                if path is None:
                    continue
                im = Image.open(path).convert("RGB")
                im.thumbnail((TW - 8, TH - 8))
                sheet.paste(im, (LW + c * TW + 4, r * TH + 4))
                if key not in ("ref", "guide"):
                    ocr[f"{key}/{p['id']}"] = ocr_score(eng, path, p["lines"])
        sheet.save(SH / f"{sid}.png")
        print("helaian", sid)
    (SH / "ocr.json").write_text(json.dumps(ocr, indent=1, ensure_ascii=False))
    for key, label in MODELS:
        v = [s for k, (s, _) in ocr.items() if k.startswith(key + "/")]
        if v:
            print(f"{label:24s} OCR purata {sum(v) / len(v):.2f}  imej {len(v)}")


if __name__ == "__main__":
    main()
