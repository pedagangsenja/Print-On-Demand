"""Dataset dashboard untuk Lettering P9 (pelan percuma + ujian 6 gaya, 23 Nov 2026).
Output: data/export/lettering_p9/{lettering_p9_test,lettering_p9_tools,lettering_p9_steps}.json
Sumber: designs/lettering/test-6gaya (times_<enjin>.json, raw/qc_p9b.txt) + semakan mata Claude (tahap bukti lemah).
Gambar = id blob artifact (MOSS dimuat naik 24 Nov pagi; ERNIE + FLUX.2 klein 24 Nov petang).
Output tambahan: lettering_p9_engines.json (ringkasan 3 enjin, quote dan seed sama).
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

ENGINES = {"moss": "MOSS-Image SFT (8 langkah)", "ernie": "ERNIE-Image-Turbo (GGUF Q8, 8 langkah)",
           "klein4b": "FLUX.2 klein 4B (4 langkah)"}
test = []
for sid in STYLES:
    for seed in (42, 7):
        key = f"steps_{sid}_moss_s{seed}"
        pick = PICK[sid] == seed
        test.append({"id": key, "engine": "moss", "engine_name": ENGINES["moss"],
                     "style": sid, "style_name": STYLES[sid]["name"], "ref": STYLES[sid]["ref"],
                     "seed": seed, "text": "Small steps every day", "words": 4, "wrong_n": 0, "extra_n": 0,
                     "seconds": times[key], "pick": pick, "gallery": pick, "note": NOTE[(sid, seed)],
                     "raw_img": f"/_blob/{IMG[sid][0]}" if pick else None,
                     "final_img": f"/_blob/{IMG[sid][1]}" if pick else None,
                     "level": "lemah"})

# ERNIE + FLUX.2 klein (24 Nov): prompt, seed dan saiz sama; designs/lettering-p9b/gen.py di CPU 4 teras
QC = {}  # id -> (salah eja, teks rawak, catatan)  dari raw/qc_p9b.txt (semakan mata Claude)
for line in open(os.path.join(T, "raw", "qc_p9b.txt"), encoding="utf-8"):
    if line.strip():
        k, w, x, n = line.rstrip("\n").split("|", 3)
        QC[k] = (int(w), int(x), n)
PICK2 = {"ernie": {s: 42 for s in STYLES}, "klein4b": {"S1": 7, "S2": 42, "S4": 42, "S5": 7}}
SHOW_FAIL = {("klein4b", "S3"): 42, ("klein4b", "S6"): 42}  # gaya tanpa seed betul: tunjuk imej mentah
IMG2 = {  # id -> (mentah, siap cetak)
    "steps_S1_ernie_s42": ("26d2cd304d2b87c35b7f9ce7896a20b2", "4c4749378fe0d30701999325d5eba190"),
    "steps_S2_ernie_s42": ("187d4321d3ff9264c26e51c8b3107c73", "6401589c681950a848822c0aad20c6a2"),
    "steps_S3_ernie_s42": ("784d508e3797761c895dd546ffa87936", "e8d3bca6af185e6d835fe5ad7c7cef2d"),
    "steps_S4_ernie_s42": ("a544cfb8753a2e3ff02b126ffdf31a13", "91c68040c85530ec060663a753a83ebc"),
    "steps_S5_ernie_s42": ("85a786e0b0fc7decf8a38f404b69f66d", "ffb022f0f03d676e28228490e5b07863"),
    "steps_S6_ernie_s42": ("38b53fc5abb694753e22340189ba30e4", "87cb77f09822b2a81ba12272fce97790"),
    "steps_S1_klein4b_s7": ("e08bd90bf4115e2fa43b4448c09c4291", "fec147bee292ff2736d2713e9ef2e7d5"),
    "steps_S2_klein4b_s42": ("d4276d72e682ee9768df6945c8f6dbb9", "617bae80a4c4c3de38034506cc67dd3f"),
    "steps_S3_klein4b_s42": ("7b1cecc5e9c851c04b98a71ca824bf9d", None),
    "steps_S4_klein4b_s42": ("17d7f9892a6f9e2c9650bd3b98fa2c21", "d76ff7c3bf7201cd6b80230e622a75eb"),
    "steps_S5_klein4b_s7": ("a964bd7a9682bff059aefa2358d8fe44", "c9185f06e7a2f03288069982ce37bea3"),
    "steps_S6_klein4b_s42": ("c11ea109b3c1d1b6f851f3948d2feddf", None),
}
for eng in ("ernie", "klein4b"):
    tm = json.load(open(os.path.join(T, "raw", f"times_{eng}.json")))
    for sid in STYLES:
        for seed in (42, 7):
            key = f"steps_{sid}_{eng}_s{seed}"
            w, x, n = QC[key]
            pick = PICK2[eng].get(sid) == seed
            show = pick or SHOW_FAIL.get((eng, sid)) == seed
            raw, fin = IMG2.get(key, (None, None))
            test.append({"id": key, "engine": eng, "engine_name": ENGINES[eng],
                         "style": sid, "style_name": STYLES[sid]["name"], "ref": STYLES[sid]["ref"],
                         "seed": seed, "text": "Small steps every day", "words": 4, "wrong_n": w, "extra_n": x,
                         "seconds": tm[key], "pick": pick, "gallery": show, "note": n,
                         "raw_img": f"/_blob/{raw}" if show and raw else None,
                         "final_img": f"/_blob/{fin}" if show and fin else None,
                         "level": "lemah"})

ENG_NOTE = {
    "moss": ("Huruf halus; skrip + swash S2/S3 paling hampir rujukan.", "Paling lambat bersama ERNIE (~7 min/imej). S1 kurang melantun."),
    "ernie": ("Semua imej betul; susun atur, warna dan hiasan paling hampir prompt (inline S6, noktah S5, swash S2).",
              "~7 min/imej di CPU. Dua seed hampir serupa (kurang variasi). 1 titik confetti terselit dalam STEPS (S1 s7)."),
    "klein4b": ("Paling laju: ~1.5 min/imej di CPU (4-5x lebih cepat).",
                "Kerap tertinggal huruf L dalam Small (Smal/Smail) pada skrip; tanda seru rawak (S5 s42). S3 dan S6 tiada seed betul."),
}
engines = []
for i, (eng, name) in enumerate(ENGINES.items()):
    rows = [r for r in test if r["engine"] == eng]
    ok = [r for r in rows if r["wrong_n"] == 0 and r["extra_n"] == 0]
    engines.append({"engine": eng, "engine_name": name, "order": i, "images": len(rows), "ok": len(ok),
                    "styles_ok": len({r["style"] for r in ok}), "styles": len(STYLES),
                    "avg_seconds": round(sum(r["seconds"] for r in rows) / len(rows), 1),
                    "finish": len([r for r in rows if r["pick"]]),
                    "strength": ENG_NOTE[eng][0], "weakness": ENG_NOTE[eng][1],
                    "license": "Apache 2.0",
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
for name, rows in (("lettering_p9_test", test), ("lettering_p9_tools", tools), ("lettering_p9_steps", steps),
                   ("lettering_p9_engines", engines)):
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n")
    print(name, len(rows))
