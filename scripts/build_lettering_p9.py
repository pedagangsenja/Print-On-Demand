"""Dataset dashboard untuk Lettering P9 (pelan percuma + ujian 6 gaya, 23 Nov 2026).
Output: data/export/lettering_p9/{lettering_p9_test,lettering_p9_tools,lettering_p9_steps}.json
Sumber: designs/lettering/test-6gaya (times_moss.json, info.json) + semakan mata Claude (tahap bukti lemah).
Gambar = id blob artifact (dimuat naik 24 Nov).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "lettering"))
from styles import STYLES  # noqa: E402

T = os.path.join(ROOT, "designs", "lettering", "test-6gaya")
OUT = os.path.join(ROOT, "data", "export", "lettering_p9")
times = json.load(open(os.path.join(T, "raw", "times_moss.json")))

PICK = {"S1": 42, "S2": 42, "S3": 42, "S4": 42, "S5": 42, "S6": 7}
IMG = {  # (mentah, siap cetak) untuk seed pilihan
    "S1": ("561c84014ca13054003f2ea0ce7e281d", "f399ff19c4407ba78fd18754a1d37d67"),
    "S2": ("308c2543f626a076af2bb339d75869fc", "80736ed1e680ab05cf4a99da073d80c4"),
    "S3": ("d7f2b7b96cb85b784821e59b1654ea75", "399bac24391a770e3c3d78c25a8defa9"),
    "S4": ("ffa09024414682bf85c50c4e99780528", "1514f70c5c0d4198cdfa582c365ac3bd"),
    "S5": ("437474dbae9544e02355e821129b0560", "5132b0722a3107866cb3c0412066aa56"),
    "S6": ("241a6f6fcccca64e90651bf10139c060", "130d87bc61087606e237ea72ef59236b"),
}
NOTE = {
    ("S1", 42): "Huruf bulat macam font, kurang melantun berbanding rujukan",
    ("S1", 7): "EVERY DAY terlalu rapat (dibaca EVERYDAY jika satu warna)",
    ("S2", 42): "Paling hampir rujukan: skrip berswash + huruf kecil berselang",
    ("S2", 7): "Baik; swash sedikit kurang",
    ("S3", 42): "Swash panjang + percikan baik; semua baris hampir sama besar",
    ("S3", 7): "Baik; sama seperti s42",
    ("S4", 42): "Tekstur kapur dibina semula oleh finish.py",
    ("S4", 7): "Baik",
    ("S5", 42): "Blok rata + noktah; tekstur lusuh prosedur",
    ("S5", 7): "Baik",
    ("S6", 42): "Warna inline tercantum dengan putih semasa vektor",
    ("S6", 7): "Inline kekal; percikan kuning seimbang",
}

test = []
for sid in STYLES:
    for seed in (42, 7):
        key = f"steps_{sid}_moss_s{seed}"
        pick = PICK[sid] == seed
        test.append({"id": key, "style": sid, "style_name": STYLES[sid]["name"], "ref": STYLES[sid]["ref"],
                     "seed": seed, "text": "Small steps every day", "words": 4, "wrong_n": 0,
                     "seconds": times[key], "pick": pick, "note": NOTE[(sid, seed)],
                     "raw_img": f"/_blob/{IMG[sid][0]}" if pick else None,
                     "final_img": f"/_blob/{IMG[sid][1]}" if pick else None,
                     "level": "lemah"})

tools = [
    {"job": "Jana utama", "tool": "Qwen-Image-2512 + LoRA Lightning 8 langkah", "license": "Apache 2.0", "where": "GPU T4 Kaggle (percuma)", "status": "Tunggu anda sahkan telefon Kaggle"},
    {"job": "Jana sandaran", "tool": "MOSS-Image-SFT 5B + LoRA 8 langkah lodestones", "license": "Apache 2.0", "where": "CPU container, ~7 min/imej", "status": "Dipasang, diuji 23 Nov"},
    {"job": "Imej hero", "tool": "Space rasmi Qwen-Image-2512", "license": "Apache 2.0", "where": "ZeroGPU percuma", "status": "1 imej/hari (Space minta 240 s, kuota 300 s)"},
    {"job": "Betulkan 1 perkataan salah", "tool": "Qwen-Image-Edit-2511", "license": "Apache 2.0", "where": "GPU Kaggle", "status": "Tunggu telefon Kaggle"},
    {"job": "QC ejaan + gaya", "tool": "sheet.py + semakan mata Claude", "license": "-", "where": "container", "status": "Siap"},
    {"job": "Vektor (ganti upscale)", "tool": "potrace 1.16 dalam finish.py", "license": "GPL-2.0 (alat sahaja)", "where": "container", "status": "Siap"},
    {"job": "Palet, susun, tekstur, PNG 300 DPI 5 saiz", "tool": "finish.py (OpenCV, scipy, cairosvg)", "license": "Apache 2.0 / BSD / LGPL-3.0", "where": "container", "status": "Siap"},
    {"job": "Mockup + pin", "tool": "Skrip Pillow/OpenCV", "license": "-", "where": "container", "status": "Belum"},
]

steps = [
    ("Sekali", "Anda", "Sahkan nombor telefon Kaggle (Settings → Phone verification), ~2 min", "Belum"),
    ("Sekali", "Claude", "Uji job GPU Kaggle: Qwen-Image-2512 4-bit + Lightning; sandaran MOSS di T4", "Tunggu langkah 1"),
    ("Sekali", "Claude", "Skrip setup container (potrace + pip) disimpan dalam environment", "Siap"),
    ("Setiap batch", "Claude", "Tulis 10 quote Inggeris 3–7 perkataan, semak trademark, tetapkan baris + perkataan utama", "Sedia"),
    ("Setiap batch", "Claude", "Bina prompt ikut gaya S1–S6 (styles.py)", "Sedia"),
    ("Setiap batch", "Claude", "Jana 4 seed setiap quote (GPU Kaggle; sandaran CPU 2 seed)", "Sedia (CPU)"),
    ("Setiap batch", "Claude", "QC: ejaan 100%, tiada teks rawak, tiada cacat + 9 ciri gaya; gagal = seed baharu (maks 4)", "Sedia"),
    ("Setiap batch", "Claude", "finish.py: SVG induk + PNG 300 DPI 8×10 hingga 24×36 + pratonton", "Sedia"),
    ("Setiap batch", "Anda", "Lulus / tolak design (~5 min)", "Sedia"),
    ("Setiap batch", "Claude", "Mockup, pin, upload (Workflow sedia ada)", "Belum"),
]
steps = [{"no": i, "phase": p, "who": w, "step": s, "status": st} for i, (p, w, s, st) in enumerate(steps, 1)]

os.makedirs(OUT, exist_ok=True)
for name, rows in (("lettering_p9_test", test), ("lettering_p9_tools", tools), ("lettering_p9_steps", steps)):
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n")
    print(name, len(rows))
