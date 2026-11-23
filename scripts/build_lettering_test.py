"""Ujian lettering ayat panjang (23 Nov 2026) -> data/export/models/lettering_*.json untuk tab Model AI.

Guna:
  python3 scripts/build_lettering_test.py thumbs   # gambar kecil JPEG -> designs/lettering-test/thumb/
  python3 scripts/build_lettering_test.py          # bina dataset (perlu designs/lettering-test/assets.json)
  python3 scripts/build_lettering_test.py thumbs2  # ujian v2 (ERNIE + penambah, ayat baharu, 2 seed): gambar kecil
  python3 scripts/build_lettering_test.py v2       # ujian v2: dataset lettering_v2*, lettering_standard
  python3 scripts/build_lettering_test.py thumbs3  # ujian v3 (SOP + QC + redo): gambar kecil
  python3 scripts/build_lettering_test.py v3       # ujian v3: lettering_v3*, lettering_ref_elements, lettering_qc_rubric, lettering_sop

Sumber: designs/lettering-test/prompts.json, out/<model>/times.json (masa diukur), review.json (semakan
ejaan dengan mata oleh Claude: perkataan salah eja; '+X' = teks rawak tambahan). Satu seed (42): tahap bukti lemah.
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
     "Prompt ditulis semula dahulu oleh model penambah ERNIE (73-101 s, tidak termasuk dalam masa), kemudian dijana seperti ERNIE",
     "Apache 2.0", HF + "baidu/ERNIE-Image-Turbo", "", "", ""),
    ("moss", "MOSS-Image SFT (8 langkah)",
     "CPU komputer awan, bf16 + LoRA 8 langkah lodestones (kekuatan 0.7), tanpa CFG",
     "Apache 2.0", HF + "OpenMOSS-Team/MOSS-Image-SFT", "", "", ""),
    ("qwen2512", "Qwen-Image-2512", "Space Hugging Face rasmi (GPU percuma), 50 langkah, guidance 4; masa = tunggu Space, bukan CPU",
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


def verdict(items):
    """Senarai semakan -> (perkataan salah, teks rawak, nota). Item '+X' = teks rawak tambahan."""
    wrong = [w for w in items if not w.startswith("+")]
    extra = [w[1:] for w in items if w.startswith("+")]
    note = ", ".join(wrong) + ("; " if wrong and extra else "") + ("teks rawak tambahan: " + ", ".join(extra) if extra else "")
    return wrong, extra, note


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
            items = review[m][p["id"]]
            wrong, extra, note = verdict(items)
            rows.append({"model": m, "model_name": name, "model_order": order, "no": i, "id": p["id"], "type": p["type"],
                         "text": p["text"], "words": p["words"], "ok": not items, "wrong": note,
                         "wrong_n": len(wrong), "extra_n": len(extra), "seconds": times[p["id"]]["seconds"], "img": assets[key],
                         "w": p["w"], "h": p["h"], "seed": 42, "level": "lemah"})
    refs = [{"id": p["id"], "ref_img": ref_assets[REF_ASSET[p["ref"]]], "ref_full": ref_assets[REF_ASSET[p["ref"]]],
             "ref_from": "Poster lettering (contoh kedua anda)", "cropped": False} for p in prompts()]
    gaps = json.loads((T / "gaps.json").read_text())
    for name, data in (("lettering_test", rows), ("lettering_test_models", models), ("lettering_test_refs", refs),
                       ("lettering_gaps", gaps)):
        (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    print(len(rows), len(models), len(refs), len(gaps))


V2 = T / "v2"  # 23 Nov (petang): ayat baharu + prompt ikut ciri rujukan, ERNIE + penambah, 2 seed
V2_SEEDS = [42, 7]


def thumbs_v2():
    from PIL import Image
    d = V2 / "thumb"; d.mkdir(exist_ok=True)
    for f in sorted((V2 / "out/ernie_pe").glob("*.png")):
        im = Image.open(f).convert("RGB"); im.thumbnail((THUMB, THUMB))
        im.save(d / f"{f.stem}.jpg", quality=85, optimize=True)
    print(d, len(list(d.glob("*.jpg"))))


def build_v2():
    ps = json.loads((V2 / "prompts.json").read_text())
    review = json.loads((V2 / "review.json").read_text())
    assets = json.loads((V2 / "assets.json").read_text())
    times = json.loads((V2 / "out/ernie_pe/times.json").read_text())
    ref_assets = json.loads((ROOT / "designs/model-test/assets.json").read_text())
    models = [{"model": f"s{sd}", "model_name": f"ERNIE + penambah, seed {sd}", "model_order": o,
               "missing_note": "Belum dijana", "level": "lemah"} for o, sd in enumerate(V2_SEEDS)]
    rows = []
    for i, p in enumerate(ps, 1):
        for o, sd in enumerate(V2_SEEDS):
            key = f"{p['id']}_s{sd}"
            if key not in assets or key not in review:
                continue
            items = review[key]
            wrong, extra, note = verdict(items)
            rows.append({"model": f"s{sd}", "model_name": models[o]["model_name"], "model_order": o, "no": i, "id": p["id"],
                         "type": p["type"], "text": p["text"], "words": p["words"], "ok": not items, "wrong": note,
                         "wrong_n": len(wrong), "extra_n": len(extra), "seconds": times[key]["seconds"], "img": assets[key],
                         "w": p["w"], "h": p["h"], "seed": sd, "level": "lemah"})
    refs = [{"id": p["id"], "ref_img": ref_assets[REF_ASSET[p["ref"]]], "ref_full": ref_assets[REF_ASSET[p["ref"]]],
             "ref_from": "Poster lettering (contoh kedua anda)", "cropped": False} for p in ps]
    std = json.loads((V2 / "standard.json").read_text())
    for name, data in (("lettering_v2", rows), ("lettering_v2_models", models), ("lettering_v2_refs", refs),
                       ("lettering_standard", std)):
        (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    print(len(rows), len(models), len(refs), len(std))


V3 = T / "v3"  # SOP + QC: 10 design (2 setiap rujukan), redo sehingga lulus, maks 4 cubaan
V3_SEEDS = [42, 7, 123, 2024]
STYLE_MIN = 7  # unsur gaya yang mesti lulus daripada 8


def thumbs_v3():
    from PIL import Image
    d = V3 / "thumb"; d.mkdir(exist_ok=True)
    for f in sorted((V3 / "out/ernie_pe").glob("*.png")):
        im = Image.open(f).convert("RGB"); im.thumbnail((THUMB, THUMB))
        im.save(d / f"{f.stem}.jpg", quality=85, optimize=True)
    print(d, len(list(d.glob("*.jpg"))))


def qc_verdict(q, words, n_el):
    """Keputusan QC satu imej: pintu wajib (ejaan, teks rawak, cacat) + skor gaya."""
    wrong, extra, _ = verdict(q.get("wrong", []))
    defects, el_fail = q.get("defects", []), q.get("el_fail", {})
    score = n_el - len(el_fail)
    ok = not wrong and not extra and not defects and score >= STYLE_MIN
    why = []
    if wrong:
        why.append("ejaan: " + ", ".join(wrong))
    if extra:
        why.append("teks rawak: " + ", ".join(extra))
    if defects:
        why.append("cacat: " + ", ".join(defects))
    if el_fail:
        why.append(f"gaya {score}/{n_el}: " + ", ".join(el_fail.values()))
    text = (f"✓ Lulus QC: ejaan {words}/{words}, gaya {score}/{n_el}" if ok else "✗ Gagal QC: " + "; ".join(why))
    return ok, wrong, extra, defects, score, text


def build_v3():
    ps = json.loads((V3 / "prompts.json").read_text())
    rubric = json.loads((V3 / "rubric.json").read_text())
    qc = json.loads((V3 / "qc.json").read_text()) if (V3 / "qc.json").exists() else {}
    assets = json.loads((V3 / "assets.json").read_text()) if (V3 / "assets.json").exists() else {}
    tf = V3 / "out/ernie_pe/times.json"
    times = json.loads(tf.read_text()) if tf.exists() else {}
    ref_assets = json.loads((ROOT / "designs/model-test/assets.json").read_text())
    models = [{"model": f"a{n}", "model_name": f"Cubaan {n} (seed {sd})", "model_order": n - 1,
               "missing_note": "Tiada cubaan: sudah lulus, atau belum sampai giliran", "level": "lemah"}
              for n, sd in enumerate(V3_SEEDS, 1)]
    rows, final = [], []
    for i, p in enumerate(ps, 1):
        n_el = len(rubric["styles"][p["ref"]]["elements"])
        for n, sd in enumerate(V3_SEEDS, 1):
            key = f"{p['id']}_s{sd}"
            if key not in assets or key not in qc:
                continue
            ok, wrong, extra, defects, score, text = qc_verdict(qc[key], p["words"], n_el)
            row = {"model": f"a{n}", "model_name": models[n - 1]["model_name"], "model_order": n - 1, "no": i,
                   "id": p["id"], "ref": p["ref"], "type": p["type"], "text": p["text"], "words": p["words"],
                   "fonts": p["fonts"], "attempt": n, "seed": sd, "prompt_rev": qc[key].get("rev", 1),
                   "ok": ok, "wrong": text, "verdict_text": text, "wrong_n": len(wrong), "extra_n": len(extra),
                   "defects_n": len(defects), "style_score": score, "style_max": n_el,
                   "action": qc[key].get("action", "Final" if ok else ""), "seconds": times[key]["seconds"],
                   "img": assets[key], "w": p["w"], "h": p["h"], "level": "lemah"}
            rows.append(row)
            if ok:
                final.append({**row, "model": "final", "model_name": f"Final (cubaan {n})", "model_order": 0})
    refs = [{"id": p["id"], "ref_img": ref_assets[REF_ASSET[p["ref"]]], "ref_full": ref_assets[REF_ASSET[p["ref"]]],
             "ref_from": "Poster lettering (contoh kedua anda)", "cropped": False} for p in ps]
    final_models = [{"model": "final", "model_name": "Final", "model_order": 0,
                     "missing_note": "Belum lulus QC", "level": "lemah"}]
    rub = [{"ref": "Semua", "ref_name": "Semua gaya", "kind": "Wajib", "code": g["code"], "check": g["check"]}
           for g in rubric["gates"]]
    rub += [{"ref": r, "ref_name": st["name"], "kind": "Gaya", "code": e["code"], "check": e["check"]}
            for r, st in rubric["styles"].items() for e in st["elements"]]
    out = {"lettering_v3": rows, "lettering_v3_models": models, "lettering_v3_refs": refs,
           "lettering_v3_final": final, "lettering_v3_final_models": final_models,
           "lettering_ref_elements": json.loads((V3 / "refs_deepdive.json").read_text()),
           "lettering_qc_rubric": rub, "lettering_sop": json.loads((V3 / "sop.json").read_text())}
    for name, data in out.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    print({k: len(v) for k, v in out.items()})


if __name__ == "__main__":
    {"thumbs": thumbs, "thumbs2": thumbs_v2, "v2": build_v2, "thumbs3": thumbs_v3, "v3": build_v3}.get(
        (sys.argv[1:] or [""])[0], build)()
