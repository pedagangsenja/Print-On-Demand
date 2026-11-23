"""Ujian lettering ayat panjang (23 Nov 2026) -> data/export/models/lettering_*.json untuk tab Model AI.

Guna:
  python3 scripts/build_lettering_test.py thumbs   # gambar kecil JPEG -> designs/lettering-test/thumb/
  python3 scripts/build_lettering_test.py          # bina dataset (perlu designs/lettering-test/assets.json)

Sumber: designs/lettering-test/prompts.json, out/<model>/times.json (masa diukur), review.json (semakan
ejaan dengan mata oleh Claude: senarai perkataan salah/tertinggal). Satu seed (42): tahap bukti lemah.
Rujukan = poster lettering yang pengguna upload 23 Nov (sudah ada sebagai aset dashboard, lihat
designs/model-test/assets.json kunci full_B1..B5); design orang lain, rujukan gaya sahaja.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "designs/lettering-test"
OUT = ROOT / "data/export/models"
HF = "https://huggingface.co/"
THUMB = 720

# kunci, nama, cara jana, lesen, sumber, kekuatan, kelemahan, nota jika tiada imej
MODELS = [
    ("ernie", "ERNIE-Image-Turbo", "CPU komputer awan, GGUF Q8, 8 langkah, tanpa penambah prompt",
     "Apache 2.0", HF + "baidu/ERNIE-Image-Turbo", "", "", ""),
    ("ernie_pe", "ERNIE-Image-Turbo + penambah prompt",
     "Prompt ditulis semula dahulu oleh model penambah ERNIE (3B), kemudian dijana seperti ERNIE",
     "Apache 2.0", HF + "baidu/ERNIE-Image-Turbo", "", "", ""),
    ("moss", "MOSS-Image SFT (8 langkah)",
     "CPU komputer awan, bf16 + LoRA 8 langkah lodestones (kekuatan 0.7), tanpa CFG",
     "Apache 2.0", HF + "OpenMOSS-Team/MOSS-Image-SFT", "", "", ""),
    ("qwen2512", "Qwen-Image-2512", "Space Hugging Face rasmi (GPU percuma), 50 langkah, guidance 4",
     "Apache 2.0", HF + "Qwen/Qwen-Image-2512", "", "",
     "Tidak dijana: kuota GPU percuma Space habis (perlu 240 s setiap imej)"),
]
REF_ASSET = {"B1": "full_B1", "B2": "full_B2", "B3": "full_B3", "B4": "full_B4", "B5": "full_B5"}
NOTES = json.loads((T / "notes.json").read_text()) if (T / "notes.json").exists() else {}


def prompts():
    return json.loads((T / "prompts.json").read_text())


def thumbs():
    from PIL import Image
    d = T / "thumb"; d.mkdir(exist_ok=True)
    for m, *_ in MODELS:
        for p in prompts():
            f = T / "out" / m / f"{p['id']}.png"
            if f.exists():
                im = Image.open(f).convert("RGB"); im.thumbnail((THUMB, THUMB))
                im.save(d / f"{m}_{p['id']}.jpg", quality=85, optimize=True)
    print(d, len(list(d.glob("*.jpg"))))


def build():
    review = json.loads((T / "review.json").read_text())
    assets = json.loads((T / "assets.json").read_text())
    ref_assets = json.loads((ROOT / "designs/model-test/assets.json").read_text())
    rows, models = [], []
    for order, (m, name, how, lic, src, strength, weak, missing) in enumerate(MODELS):
        n = NOTES.get(m, {})
        models.append({"model": m, "model_name": name, "model_order": order, "how": how, "license": lic, "source": src,
                       "strength": n.get("strength", strength), "weakness": n.get("weakness", weak),
                       "missing_note": n.get("missing_note", missing), "level": "lemah"})
        tf = T / "out" / m / "times.json"
        times = json.loads(tf.read_text()) if tf.exists() else {}
        for i, p in enumerate(prompts(), 1):
            key = f"{m}_{p['id']}"
            if key not in assets or p["id"] not in review.get(m, {}):
                continue
            wrong = review[m][p["id"]]
            rows.append({"model": m, "model_name": name, "model_order": order, "no": i, "id": p["id"], "type": p["type"],
                         "text": p["text"], "words": p["words"], "ok": not wrong, "wrong": ", ".join(wrong),
                         "wrong_n": len(wrong), "seconds": times[p["id"]]["seconds"], "img": assets[key],
                         "w": p["w"], "h": p["h"], "seed": 42, "level": "lemah"})
    refs = [{"id": p["id"], "ref_img": ref_assets[REF_ASSET[p["ref"]]], "ref_full": ref_assets[REF_ASSET[p["ref"]]],
             "ref_from": "Poster lettering (contoh kedua anda)", "cropped": False} for p in prompts()]
    gaps = json.loads((T / "gaps.json").read_text())
    for name, data in (("lettering_test", rows), ("lettering_test_models", models), ("lettering_test_refs", refs),
                       ("lettering_gaps", gaps)):
        (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    print(len(rows), len(models), len(refs), len(gaps))


if __name__ == "__main__":
    {"thumbs": thumbs}.get((sys.argv[1:] or [""])[0], build)()
