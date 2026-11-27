"""Gambar banding CPU vs GPU (HF) yang mudah dibaca: satu gambar setiap enjin, 2 baris (CPU, GPU) x 3 ayat.
Guna: python3 banding_gambar.py  -> qc/banding_<enjin>.jpg
"""
import json
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans{}.ttf"
font = lambda size, bold=False: ImageFont.truetype(F.format("-Bold" if bold else ""), size)
NAMA = {"zturbo": "Z-Image-Turbo", "moss": "MOSS-Image"}
AYAT = {"P": ("PENDEK", "Brave Hearts Begin Again"), "D": ("SEDERHANA", "Every Small Step Builds a Bolder You"),
        "L": ("PANJANG", "Keep Showing Up on Hard Days Because Better Mornings Are Coming")}
DEV = {"cpu": ("CPU", "komputer awan Claude", "out_cpu", "qc/k6_cpu.json"),
       "hf": ("GPU", "Hugging Face (kad grafik)", "out_gpu_hf", "qc/k6_gpu_hf.json")}
GREEN, RED, GREY, INK = (22, 128, 61), (190, 30, 45), (95, 95, 95), (20, 20, 20)
TW, TH, LW = 380, 507, 170


def masa(s):
    s = round(s)
    return f"{s // 60} min {s % 60} s" if s >= 60 else f"{s} saat"


def main():
    for m in NAMA:
        qc, t = {}, {}
        for dv, (_, _, out, qf) in DEV.items():
            qc.update({(dv, r["id"]): r for r in json.load(open(HERE / qf)) if r["model"] == m})
            for line in open(HERE / out / m / "log.jsonl"):
                r = json.loads(line)
                t[(dv, f"{r['id']}_s{r['seed']}")] = r["saat"]
        W, top, colh, rowh = LW + 3 * (TW + 20) + 20, 150, 110, TH + 95
        im = Image.new("RGB", (W, top + colh + 2 * rowh + 90), "white")
        d = ImageDraw.Draw(im)
        d.text((24, 22), f"{NAMA[m]}: CPU lawan GPU", font=font(44, True), fill=INK)
        d.text((24, 82), "Gaya K6, prompt dan seed sama (42). Atas = CPU, bawah = GPU.", font=font(24), fill=GREY)
        for j, a in enumerate("PDL"):
            x = LW + 20 + j * (TW + 20)
            d.text((x, top), AYAT[a][0], font=font(26, True), fill=INK)
            d.multiline_text((x, top + 34), "\n".join(textwrap.wrap(f'"{AYAT[a][1]}"', 30)), font=font(19), fill=GREY, spacing=4)
        cpu_t, gpu_t = [], []
        for i, dv in enumerate(DEV):
            y = top + colh + i * rowh
            d.text((24, y + TH // 2 - 40), DEV[dv][0], font=font(48, True), fill=INK)
            d.multiline_text((24, y + TH // 2 + 20), "\n".join(textwrap.wrap(DEV[dv][1], 12)), font=font(18), fill=GREY)
            for j, a in enumerate("PDL"):
                x, iid = LW + 20 + j * (TW + 20), f"K6{a}_s42"
                im.paste(Image.open(HERE / DEV[dv][2] / m / f"{iid}.png").convert("RGB").resize((TW, TH)), (x, y))
                s = t[(dv, iid)]; (cpu_t if dv == "cpu" else gpu_t).append(s)
                d.text((x, y + TH + 8), f"Masa: {masa(s)}", font=font(22, True), fill=INK)
                q = qc[(dv, iid)]
                ok = "✓ Ejaan betul" if q["ejaan"] else "✗ " + textwrap.shorten(q["sebab"], 34, placeholder="…")
                d.text((x, y + TH + 40), ok, font=font(20, True), fill=GREEN if q["ejaan"] else RED)
        kali = round(sum(cpu_t) / sum(gpu_t))
        nb = lambda dv: sum(qc[(dv, f"K6{a}_s42")]["ejaan"] for a in "PDL")
        d.text((24, top + colh + 2 * rowh + 20),
               f"GPU {kali} kali lebih laju.  Ejaan betul: CPU {nb('cpu')}/3, GPU {nb('hf')}/3.",
               font=font(30, True), fill=INK)
        im.save(HERE / f"qc/banding_{m}.jpg", quality=88)
        print(m, im.size, kali)


if __name__ == "__main__":
    main()
