"""Ujian 3 model (23 Nov 2026) -> data/export/models/model_test.json + model_test_models.json.

Guna:
  python3 scripts/build_model_test.py thumbs   # gambar kecil JPEG untuk dashboard -> designs/model-test/thumb/
  python3 scripts/build_model_test.py          # bina dataset (perlu designs/model-test/assets.json: nama thumb -> /_blob/<id>)

Sumber: designs/model-test/prompts.json (prompt), out/<model>/times.json (masa diukur),
review.json (semakan ejaan dengan mata oleh Claude). Satu seed (42) setiap prompt: tahap bukti lemah.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "designs/model-test"
OUT = ROOT / "data/export/models"
HF = "https://huggingface.co/"

# kunci, nama, lesen, sumber lesen, kekuatan, kelemahan (dari semakan mata 30 imej)
MODELS = [
    ("klein4b", "FLUX.2 klein 4B", "Apache 2.0", HF + "black-forest-labs/FLUX.2-klein-4B",
     "Paling laju. Bentuk dan susun atur kemas.",
     "Kerap salah eja, terutama perkataan Melayu (Janna, Bermimpo, Aidup)."),
    ("zimage", "Z-Image-Turbo", "Apache 2.0", HF + "Tongyi-MAI/Z-Image-Turbo",
     "Garis tebal dan bersih. Kuat untuk gaya SVG Inggeris.",
     "Salah eja pada 4 imej (Patiance, Janban, Alimat, PENKGATI)."),
    ("ernie", "ERNIE-Image-Turbo", "Apache 2.0", HF + "baidu/ERNIE-Image-Turbo",
     "Semua ejaan betul. Gaya vintage, kapur dan emblem paling hampir dengan contoh.",
     "Paling perlahan. Garis bingkai imej 5 sedikit bersepah."),
]
SET_NAME = {"A": "Gaya SVG Inggeris", "B": "Lettering vintage Melayu"}
THUMB = 720  # sisi panjang, piksel


def prompts():
    return json.loads((T / "prompts.json").read_text())


def thumbs():
    from PIL import Image
    d = T / "thumb"; d.mkdir(exist_ok=True)
    for m, *_ in MODELS:
        for p in prompts():
            im = Image.open(T / "out" / m / f"{p['id']}.png").convert("RGB")
            im.thumbnail((THUMB, THUMB))
            im.save(d / f"{m}_{p['id']}.jpg", quality=85, optimize=True)
    print(d, len(list(d.glob("*.jpg"))))


def build():
    review = json.loads((T / "review.json").read_text())
    assets = json.loads((T / "assets.json").read_text())
    rows = []
    for order, (m, name, *_ ) in enumerate(MODELS):
        times = json.loads((T / "out" / m / "times.json").read_text())
        for i, p in enumerate(prompts(), 1):
            wrong = review[m][p["id"]]
            rows.append({
                "model": m, "model_name": name, "model_order": order, "no": i, "id": p["id"],
                "set": p["set"][0], "set_name": SET_NAME[p["set"][0]], "type": p["type"], "text": p["text"],
                "ok": not wrong, "wrong": ", ".join(wrong), "seconds": times[p["id"]]["seconds"],
                "img": assets[f"{m}_{p['id']}"], "w": p["w"], "h": p["h"],
                "seed": 42, "level": "lemah",
            })
    models = [{"model": m, "model_name": n, "model_order": i, "license": lic, "source": src, "strength": s, "weakness": w,
               "level": "lemah", "tested": "23 Nov 2026, CPU 4 teras, seed 42, 1 cubaan setiap design"}
              for i, (m, n, lic, src, s, w) in enumerate(MODELS)]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "model_test.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n")
    (OUT / "model_test_models.json").write_text(json.dumps(models, ensure_ascii=False, indent=1) + "\n")
    print(len(rows), len(models))


if __name__ == "__main__":
    thumbs() if sys.argv[1:] == ["thumbs"] else build()
