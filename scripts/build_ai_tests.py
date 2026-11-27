"""Satukan semua ujian & generation imej AI ke satu senarai standard.

Input : data/ai_tests/raw/*.json  (salinan dataset lama dashboard, 27 Nov 2026)
        data/ai_tests/rows/*.json (ujian baharu, sudah dalam skema standard)
Output: data/export/ai_tests/ai_all.json  -> dataset dashboard `ai_all`

Satu baris = satu imej. Lulus/Gagal ikut keputusan asal setiap ujian
(lajur `standard` menyatakan syarat yang dipakai). Design siap: lulus = null.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/ai_tests/raw"
NEW = ROOT / "data/ai_tests/rows"
OUT = ROOT / "data/export/ai_tests/ai_all.json"

MODELS = {  # kunci asas -> nama paparan (untuk jadual banding)
    "klein4b": "FLUX.2 klein 4B", "schnell": "FLUX.1-schnell", "zturbo": "Z-Image-Turbo",
    "ernie": "ERNIE-Image-Turbo", "moss": "MOSS-Image SFT", "qwen2512": "Qwen-Image-2512",
    "chroma": "Chroma1-Flash", "warna": "Warna semula (bukan AI)",
}

TESTS = {
    "U01": ("Ujian 3 model: 10 design sama", "Ujian", "Ejaan sahaja",
            "FLUX.2 klein 4B, Z-Image-Turbo, ERNIE-Image-Turbo; 10 design rujukan (set A bundle SVG, set B poster); seed 42, satu cubaan."),
    "U02": ("Generation: poster motivasi (30 design)", "Generation", "Design siap (ejaan disemak dan dibaiki)",
            "Design siap dijual: 3:4, cetak 18×24 in, hitam atas putih. Tarikh = tarikh disimpan ke dashboard."),
    "U03": ("Lettering ayat panjang (L1–L5)", "Ujian", "Ejaan + teks rawak",
            "Ayat Melayu 11–14 perkataan; ERNIE, ERNIE + penambah prompt, MOSS, Qwen-Image-2512 (Space). Seed 42."),
    "U04": ("ERNIE v2: ayat baharu, prompt ikut rujukan", "Ujian", "Ejaan + teks rawak",
            "ERNIE + penambah prompt, 5 ayat Melayu baharu, seed 42 dan 7."),
    "U05": ("Generation: design sarkastik (30 design + versi warna)", "Generation", "Design siap (ejaan disemak dan dibaiki)",
            "Hitam putih (SVG, FLUX.2 klein 4B) dan versi warna 5 palet (bukan imej AI baharu). Tarikh = tarikh disimpan ke dashboard."),
    "U06": ("QC v3: ulang sehingga ikut rujukan", "Ujian", "QC v3: ejaan, teks rawak, cacat, gaya ≥ 7/8",
            "ERNIE + penambah prompt; sehingga 4 cubaan (seed 42, 7, 123, 2024) setiap design. ★ = gambar final."),
    "U07": ("Lettering P9: 6 gaya, 3 enjin", "Ujian", "Ejaan + teks rawak",
            "Quote 'Small steps every day', 6 gaya × 2 seed × 3 enjin di CPU. MOSS 23 Nov, ERNIE dan klein 24 Nov. ★ = pilihan."),
    "U08": ("Standard Lettering v1: 5 model × 5 gaya", "Ujian", "Lettering v1: ejaan, teks rawak, cacat, ciri teras, gaya ≥ 7/8",
            "5 model × K1–K5 × 3 ayat × 2 seed, CPU, 768×1024."),
    "U09": ("CPU lawan GPU (gaya K6, 6 enjin)", "Ujian", "Ejaan ketat V1",
            "Ayat dan seed sama di CPU container dan GPU Space Hugging Face (ZeroGPU, masa termasuk barisan). Kaggle T4 belum berjalan. Tarikh = tarikh disimpan."),
    "U10": ("Standard v1.2: K3 × ayat H", "Ujian", "Lettering v1.2",
            "4 enjin × 3 seed; rangka am (pembanding) lawan aturan ikut model r1. CPU container 4 teras."),
}


def rows(name):
    d = json.loads((RAW / f"{name}.json").read_text())
    return d.get("rows", d) if isinstance(d, dict) else d


def blob(v):
    if not v or v == "None":
        return None
    return v if str(v).startswith("/_blob/") else f"/_blob/{v}"


def num(v):
    try:
        return None if v in (None, "", "None") else float(v)
    except (TypeError, ValueError):
        return None


OUTROWS = []


def add(u, n, **kw):
    nama, jenis, standard, nota = TESTS[u]
    r = {"key": f"{u}|{n}", "ujian": u, "ujian_nama": nama, "jenis": jenis, "standard": standard,
         "ujian_nota": nota, "ai": True, "bukti": "lemah", "tempat": "—", "kad": "", "kad_name": "",
         "kad_nota": "", "ref_img": None, "ref_nota": "", "baris": "", "teks": "", "seed": None,
         "saat": None, "img": None, "img_siap": None, "w": None, "h": None, "lulus": None,
         "ejaan": None, "rawak": None, "cacat": None, "teras": None, "gaya": "", "sebab": "",
         "nota": "", "tanda": "", "varian": "", "urut": len(OUTROWS)}
    r.update(kw)
    r["model_name"] = MODELS[r["model"]]
    OUTROWS.append(r)


def wrongs(x):
    out = []
    if x.get("wrong"):
        out.append(f"Salah eja: {x['wrong']}")
    if int(x.get("extra_n") or 0):
        out.append(f"teks rawak ×{x['extra_n']}")
    return "; ".join(out)


# U01 ujian 3 model
refs = {x["id"]: x for x in rows("model_test_refs")}
for x in rows("model_test"):
    ok = bool(x["ok"])
    add("U01", f"{x['model']}|{x['id']}", tarikh="2026-11-23", model={"zimage": "zturbo"}.get(x["model"], x["model"]), label=x["model_name"],
        lajur=x["model_name"], tempat="CPU", kad=x["id"], kad_name=f"{x['type']} ({x['set_name']})",
        ref_img=blob(refs.get(x["id"], {}).get("ref_img")), baris="seed 42", teks=x["text"],
        seed=42, saat=num(x["seconds"]), img=blob(x["img"]), w=x["w"], h=x["h"], lulus=ok, ejaan=ok,
        sebab="" if ok else f"Salah eja: {x['wrong']}")

# U02 poster motivasi
for x in rows("design_motiv"):
    add("U02", x["id"], tarikh="2026-11-23", model="klein4b", label="FLUX.2 klein 4B",
        lajur="FLUX.2 klein 4B", kad="motiv", kad_name="Poster motivasi", baris=f"#{x['no']} · {x['id']}",
        teks=x["quote"], img=blob(x["img"]), nota=("Ejaan dibaiki" if x.get("repaired") else "") + f" · {x['format']}",
        jenis_baris="design")

# U03 lettering ayat panjang
refs = {x["id"]: x for x in rows("lettering_test_refs")}
base = {"ernie": "ernie", "ernie_pe": "ernie", "moss": "moss", "qwen2512": "qwen2512"}
var = {"ernie_pe": "+ penambah prompt", "moss": "+ LoRA 8 langkah"}
for x in rows("lettering_test"):
    add("U03", f"{x['model']}|{x['id']}", tarikh="2026-11-23", model=base[x["model"]], label=x["model_name"],
        lajur=x["model_name"], varian=var.get(x["model"], ""), tempat="HF Space" if x["model"] == "qwen2512" else "—",
        kad=x["id"], kad_name=x["type"], ref_img=blob(refs.get(x["id"], {}).get("ref_img")), baris="seed 42",
        teks=x["text"], seed=42, saat=num(x["seconds"]), img=blob(x["img"]), w=x["w"], h=x["h"],
        lulus=bool(x["ok"]), ejaan=int(x["wrong_n"] or 0) == 0, rawak=int(x["extra_n"] or 0) > 0, sebab=wrongs(x))

# U04 ERNIE v2
refs = {x["id"]: x for x in rows("lettering_v2_refs")}
for x in rows("lettering_v2"):
    add("U04", f"{x['model']}|{x['id']}", tarikh="2026-11-23", model="ernie", label="ERNIE + penambah prompt",
        lajur=f"seed {x['seed']}", varian="+ penambah prompt", kad=x["id"], kad_name=x["type"],
        ref_img=blob(refs.get(x["id"], {}).get("ref_img")), baris="", teks=x["text"], seed=x["seed"],
        saat=num(x["seconds"]), img=blob(x["img"]), w=x["w"], h=x["h"], lulus=bool(x["ok"]),
        ejaan=int(x["wrong_n"] or 0) == 0, rawak=int(x["extra_n"] or 0) > 0, sebab=wrongs(x))

# U05 design sarkastik + versi warna
warna = {x["id"]: x for x in rows("design_sarkas_warna")}
for x in rows("design_sarkas"):
    add("U05", f"bw|{x['id']}", tarikh="2026-11-23", model="klein4b", label="FLUX.2 klein 4B",
        lajur="Hitam putih", kad=x.get("theme") or "Umum", kad_name=x.get("theme") or "Umum",
        baris=f"#{x['no']} · {x['id']}", teks=x["quote"], img=blob(x["img"]),
        nota=("Ejaan dibaiki" if x.get("repaired") else "") + f" · {x['format']}", jenis_baris="design")
    c = warna.get(x["id"])
    if c:
        add("U05", f"warna|{x['id']}", tarikh="2026-11-24", model="warna", ai=False, label=f"Warna · {c['palette']}",
            lajur="Warna (bukan AI)", kad=x.get("theme") or "Umum", kad_name=x.get("theme") or "Umum",
            baris=f"#{x['no']} · {x['id']}", teks=x["quote"], img=blob(c["img"]), nota=c["format"], jenis_baris="design")

# U06 QC v3
refs = {x["id"]: x for x in rows("lettering_v3_refs")}
final = {x["img"] for x in rows("lettering_v3_final")}
for x in rows("lettering_v3"):
    why = (x.get("verdict_text") or "").replace("✗ Gagal QC: ", "").replace("✓ Lulus QC", "").strip(" :;")
    add("U06", f"{x['model']}|{x['id']}", tarikh="2026-11-23", model="ernie", label="ERNIE + penambah prompt",
        lajur=x["model_name"], varian="+ penambah prompt", kad=x["id"], kad_name=x["type"],
        ref_img=blob(refs.get(x["id"], {}).get("ref_img")), baris="", teks=x["text"], seed=x["seed"],
        saat=num(x["seconds"]), img=blob(x["img"]), w=x["w"], h=x["h"], lulus=bool(x["ok"]),
        ejaan=int(x["wrong_n"] or 0) == 0, rawak=int(x["extra_n"] or 0) > 0, cacat=int(x["defects_n"] or 0) > 0,
        gaya=f"{x['style_score']}/{x['style_max']}", sebab="" if x["ok"] else why,
        tanda="★ Final" if x["img"] in final else "")

# U07 P9 (rujukan: hanya kod; gambar ada jika sama dengan rujukan K1–K5)
refimg = {x["ref"]: x["ref_img"] for x in rows("ai2_refs")}
pbase = {"moss": "moss", "ernie": "ernie", "klein": "klein4b", "klein4b": "klein4b"}
for x in rows("lettering_p9_test"):
    ok = int(x["wrong_n"] or 0) == 0 and int(x["extra_n"] or 0) == 0
    add("U07", x["id"], tarikh="2026-11-23" if x["engine"] == "moss" else "2026-11-24", model=pbase[x["engine"]],
        label=x["engine_name"], lajur=x["engine_name"], varian="+ LoRA 8 langkah" if x["engine"] == "moss" else "",
        tempat="CPU", kad=x["style"], kad_name=x["style_name"], ref_img=blob(refimg.get(x["ref"])),
        ref_nota=f"Rujukan {x['ref']}", baris=f"seed {x['seed']}", teks=x["text"], seed=int(x["seed"]),
        saat=num(x["seconds"]), img=blob(x["raw_img"]), img_siap=blob(x["final_img"]), lulus=ok,
        ejaan=int(x["wrong_n"] or 0) == 0, rawak=int(x["extra_n"] or 0) > 0,
        sebab="" if ok else wrongs({"wrong": f"{x['wrong_n']} perkataan" if int(x["wrong_n"] or 0) else "", "extra_n": x["extra_n"]}),
        nota=x.get("note") or "", tanda="★ Pilihan" if str(x.get("pick")) == "True" else "")

# U08 Standard Lettering v1 (AI Image Test 2)
refs = {x["kad"]: x for x in rows("ai2_refs")}
lab = {"klein4b": "FLUX.2 klein 4B", "schnell": "FLUX.1-schnell", "zturbo": "Z-Image-Turbo",
       "ernie": "ERNIE-Image-Turbo", "moss": "MOSS + LoRA"}
for x in rows("ai2_images"):
    ref = refs.get(x["kad"], {})
    add("U08", f"{x['model']}|{x['id']}", tarikh="2026-11-25", model=x["model"], label=lab[x["model"]],
        lajur=lab[x["model"]], varian="+ LoRA" if x["model"] == "moss" else "", tempat="CPU", kad=x["kad"],
        kad_name=x["kad_name"], kad_nota=f"Ciri teras: {ref.get('teras', '')}", ref_img=blob(ref.get("ref_img")),
        baris=f"{x['ayat_name']} · seed {x['seed']}", teks=x["text"], seed=int(x["seed"]), saat=num(x["saat"]),
        img=blob(x["img"]), w=x["w"], h=x["h"], lulus=bool(x["lulus"]), ejaan=bool(x["g1"]), rawak=not x["g2"],
        cacat=not x["g3"], teras=bool(x["teras"]), gaya=x["gaya"], sebab=x["sebab"] or "")

# U09 CPU lawan GPU
teks = {}
for x in rows("cvg_banding"):
    teks[x["ayat"]] = x["teks"]
k6ref = next((x["ref_img"] for x in rows("cvg_peranti") if x["peranti"] == "CPU"), None)
cbase = {"MOSS": "moss", "ERNIE": "ernie", "Z-Image": "zturbo", "FLUX.2": "klein4b", "FLUX.1": "schnell", "Chroma": "chroma"}
for x in rows("cvg_imej"):
    m = next(v for k, v in cbase.items() if x["enjin"].startswith(k))
    ay = x["ayat"].split(" (")[0]
    for t, lbl in (("cpu", "CPU"), ("gpu", "GPU Kaggle T4"), ("hf", "GPU HF")):
        img = blob(x[f"{t}_img"])
        if not img:
            continue
        ok = x[f"{t}_ejaan"] == "Lulus"
        name = x["enjin"].replace("MOSS-Image SFT + LoRA 8 langkah", "MOSS + LoRA")
        add("U09", f"{t}|{x['kunci']}", tarikh="2026-11-26", model=m, label=f"{name} · {lbl}",
            lajur=name if t == "cpu" else f"{name} · {lbl}", varian="+ LoRA 8 langkah" if m == "moss" else "",
            tempat=lbl, kad="K6", kad_name="Gaya K6 (ujian CPU lawan GPU)", ref_img=blob(k6ref),
            baris=f"{ay} · seed {x['seed']}", teks=teks.get(ay, ""), seed=int(x["seed"]), saat=num(x[f"{t}_saat"]),
            img=img, lulus=ok, ejaan=ok, sebab="" if ok or x[f"{t}_sebab"] in (None, "None") else x[f"{t}_sebab"])

# U10 Standard v1.2 K3H (hanya dalam image_log)
k3 = refs.get("K3", {})
ebase = {"ERNIE": "ernie", "FLUX.2": "klein4b", "MOSS": "moss", "Z-Image": "zturbo"}
for x in rows("image_log"):
    if not x["source"].startswith("lettering-v1/k3h"):
        continue
    khas = "khas" in x["source"]
    m = next(v for k, v in ebase.items() if x["engine"].startswith(k))
    ok = x["result"] == "Lulus"
    add("U10", x["id"], tarikh=x["date"], model=m, label=x["engine"], lajur=x["engine"], varian=x["variant"],
        tempat="CPU", kad="K3H-khas" if khas else "K3H-am",
        kad_name="Aturan ikut model r1" if khas else "Rangka am (pembanding)", ref_img=blob(k3.get("ref_img")),
        baris=f"seed {x['seed']}", teks=x["text"], seed=x["seed"], saat=num(x["seconds"]), img=blob(x["img"]),
        w=x["w"], h=x["h"], lulus=ok, sebab="" if ok else (x["wrong"] or ""))

# Ujian baharu (skema standard), cth. data/ai_tests/rows/U11.json = [ {...}, ... ]
for f in sorted(NEW.glob("*.json")) if NEW.exists() else []:
    for r in json.loads(f.read_text()):
        r.setdefault("urut", len(OUTROWS))
        r.setdefault("model_name", MODELS.get(r["model"], r["model"]))
        OUTROWS.append(r)

for r in OUTROWS:
    r["nota"] = (r.get("nota") or "").strip(" ·")
    r.pop("jenis_baris", None)

keys = [r["key"] for r in OUTROWS]
assert len(keys) == len(set(keys)), "kunci berulang"
OUT.parent.mkdir(parents=True, exist_ok=True)
meta = [
    {"label": "build_ai_tests.py", "value": Path(__file__).read_text(), "type": "code", "lang": "python"},
    {"label": "Input", "value": "data/ai_tests/raw/*.json (salinan dataset dashboard 27 Nov 2026) + data/ai_tests/rows/*.json"},
]
OUT.write_text(json.dumps({"rows": OUTROWS, "meta": meta}, ensure_ascii=False, separators=(",", ":")))
print(len(OUTROWS), "baris ->", OUT.relative_to(ROOT), f"{OUT.stat().st_size // 1024} KB")
