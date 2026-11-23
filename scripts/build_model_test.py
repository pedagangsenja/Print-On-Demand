"""Ujian 3 model (23 Nov 2026) -> data/export/models/model_test.json + model_test_models.json.

Guna:
  python3 scripts/build_model_test.py thumbs   # gambar kecil JPEG untuk dashboard -> designs/model-test/thumb/
  python3 scripts/build_model_test.py refs     # gambar rujukan pengguna -> designs/model-test/refs/up/ (potong ikut REFS)
  python3 scripts/build_model_test.py          # bina dataset (perlu designs/model-test/assets.json: nama thumb -> /_blob/<id>)

Sumber: designs/model-test/prompts.json (prompt), out/<model>/times.json (masa diukur),
review.json (semakan ejaan dengan mata oleh Claude). Satu seed (42) setiap prompt: tahap bukti lemah.
Gambar rujukan = muat naik pengguna dalam chat 23 Nov (design orang lain, rujukan gaya sahaja); asal di
designs/model-test/refs/orig/ dan TIDAK di-commit.
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
# design -> (fail asal rujukan, kotak potong x0,y0,x1,y1 atau None = seluruh gambar)
REFS = {
    "01_stack": ("A3", (128, 0, 268, 142)), "02_icon": ("A2", (328, 182, 498, 359)),
    "03_circle": ("A1", (0, 355, 180, 532)), "04_ribbon": ("A1", (178, 4, 356, 180)),
    "05_frame": ("A4", (778, 322, 908, 416)),
    "06_ornate": ("B4", None), "07_chalk": ("B5", None), "08_color": ("B3", None),
    "09_badge": ("B2", None), "10_illus": ("B1", None),
}
REF_FROM = {"A1": "Bundle SVG jururawat", "A2": "Bundle SVG kebersihan", "A3": "Bundle SVG bunco",
            "A4": "Bundle SVG sarcasm", "B1": "Poster lettering", "B2": "Poster lettering", "B3": "Poster lettering",
            "B4": "Poster lettering", "B5": "Poster lettering"}


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


def refs():
    from PIL import Image
    orig, up = T / "refs/orig", T / "refs/up"; up.mkdir(parents=True, exist_ok=True)
    for f in orig.iterdir():  # gambar penuh (untuk dibesarkan)
        im = Image.open(f).convert("RGB"); im.thumbnail((1400, 1400)); im.save(up / f"full_{f.stem}.jpg", quality=88)
    for pid, (src, box) in REFS.items():
        im = Image.open(next(orig.glob(src + ".*"))).convert("RGB")
        if box:
            im = im.crop(box); im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
        im.thumbnail((THUMB, THUMB)); im.save(up / f"ref_{pid}.jpg", quality=88)
    print(up, len(list(up.glob("*.jpg"))))


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
    ref_rows = [{"id": pid, "ref_img": assets[f"ref_{pid}"], "ref_full": assets[f"full_{src}"],
                 "ref_from": REF_FROM[src], "cropped": box is not None, "note": "Muat naik anda 23 Nov; design orang lain, rujukan gaya sahaja"}
                for pid, (src, box) in REFS.items()]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "model_test_refs.json").write_text(json.dumps(ref_rows, ensure_ascii=False, indent=1) + "\n")
    (OUT / "model_test.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n")
    (OUT / "model_test_models.json").write_text(json.dumps(models, ensure_ascii=False, indent=1) + "\n")
    print(len(rows), len(models))


if __name__ == "__main__":
    {"thumbs": thumbs, "refs": refs}.get((sys.argv[1:] or [""])[0], build)()
