"""Helaian semakan K3W: rujukan + 3 enjin x 3 seed, dengan keputusan QC (qc/k3w_cpu.json).
Guna: python3 sheet_k3w.py <imej_rujukan> <keluar.jpg>"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).resolve().parent
qc = {(r["model"], r["seed"]): r for r in json.load(open(HERE / "qc/k3w_cpu.json"))}
NAMA = {"zturbo": "Z-Image-Turbo", "ernie": "ERNIE-Image-Turbo", "moss": "MOSS + LoRA"}
w, h, top, pad = 300, 400, 34, 8
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
sheet = Image.new("RGB", (4 * (w + pad) + pad, 3 * (h + top + pad) + pad), "#2a2a2a")
d = ImageDraw.Draw(sheet)
ref = Image.open(sys.argv[1]).convert("RGB").resize((w, h))
sheet.paste(ref, (pad, pad + top)); d.text((pad, pad + 8), "Rujukan (gaya sahaja)", fill="white", font=f)
for r, m in enumerate(NAMA):
    for c, s in enumerate((42, 7, 123)):
        x, y = pad + (c + 1) * (w + pad), pad + r * (h + top + pad)
        sheet.paste(Image.open(HERE / f"raw/k3w-cpu/{m}/K3W_s{s}.png").convert("RGB").resize((w, h)), (x, y + top))
        q = qc[(m, s)]
        ok = q["keputusan"] == "lulus"
        d.rectangle([x, y, x + w - 1, y + top - 4], fill="#1f7a3a" if ok else "#a12c2c")
        d.text((x + 6, y + 8), f"{NAMA[m]} s{s}  {'LULUS' if ok else 'GAGAL'} {q['gaya'] if q['G2_tiada_teks_rawak'] else 'teks rawak'}", fill="white", font=f)
sheet.save(sys.argv[2], quality=88)
