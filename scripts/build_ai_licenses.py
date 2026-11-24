"""Jadual besar model jana imej di Hugging Face: lesen komersial, kuota GPU Space, VRAM.

Riset 24 Nov 2026 (API Hugging Face, fail LICENSE / model card, app.py setiap Space,
dokumen ZeroGPU rasmi). Output:
  data/export/models/ai_licenses.json       (dataset dashboard `ai_licenses`)
  data/export/models/hf_zerogpu_quota.json  (dataset dashboard `hf_zerogpu_quota`)
  docs/research/08-ai-licenses.md
Jalankan: python3 scripts/build_ai_licenses.py
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/export/models"
DOC = ROOT / "docs/research/08-ai-licenses.md"
CHECKED = "2026-11-24"

# Dokumen rasmi: https://huggingface.co/docs/hub/spaces-zerogpu ("Usage Tiers", "GPU size")
QUOTA = [
    {"tier": "Tanpa log masuk", "minutes": 2, "note": "Keutamaan barisan rendah"},
    {"tier": "Free", "minutes": 5, "note": "Akaun anda. Diset semula 24 jam selepas kali pertama guna"},
    {"tier": "PRO", "minutes": 40, "note": "$9/bulan. Boleh lebih guna kredit: $1 setiap 10 minit"},
    {"tier": "Team", "minutes": 40, "note": "Ahli organisasi Team"},
    {"tier": "Enterprise", "minutes": 60, "note": "Ahli organisasi Enterprise"},
]
DEFAULT_GPU_S = 60  # @spaces.GPU tanpa duration = 60 s (dokumen ZeroGPU)
SIZE_MULT = {"large": 1, "xlarge": 2}  # xlarge kira 2x kuota

HF = "https://huggingface.co/"

# kategori: A = bebas komersial, B = komersial bersyarat, C = bukan komersial
# gpu_s = masa GPU maksimum yang Space minta untuk 1 gambar 1024x1024 (dari app.py);
# None = tiada Space ZeroGPU khusus. VRAM "agg." = anggaran 2 GB setiap 1B parameter (BF16).
MODELS = [
    # ---- A. Bebas komersial ----
    dict(model="ERNIE-Image-Turbo", size="8B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Poster, infografik, teks padat dan panjang. 8 langkah",
         space="baidu/ERNIE-Image-Turbo (CPU + API Baidu, maks 10 serentak). Alternatif: akhaliq/ERNIE-Image-Turbo 120 s",
         gpu_s=None, gpu_note="Tiada kuota GPU HF (Space rasmi)", vram="24 GB",
         verdict="Pilihan utama", tone="ok", repo="baidu/ERNIE-Image-Turbo"),
    dict(model="ERNIE-Image", size="8B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Versi penuh 50 langkah, ikut arahan lebih tepat", space="Tiada Space khusus",
         gpu_s=None, gpu_note="—", vram="24 GB", verdict="Boleh guna", tone="", repo="baidu/ERNIE-Image"),
    dict(model="Z-Image-Turbo", size="6B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Laju (8 langkah), teks Inggeris dan Cina", space="Tongyi-MAI/Z-Image-Turbo, mrfakename/Z-Image-Turbo",
         gpu_s=DEFAULT_GPU_S, size_gpu="large", vram="16 GB", verdict="Sandaran terbaik", tone="ok",
         repo="Tongyi-MAI/Z-Image-Turbo"),
    dict(model="Z-Image", size="6B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Versi penuh Z-Image (bukan Turbo)", space="Tongyi-MAI/Z-Image",
         gpu_s=DEFAULT_GPU_S, size_gpu="large", vram="~16 GB (agg., saiz sama Turbo)", verdict="Boleh guna", tone="",
         repo="Tongyi-MAI/Z-Image"),
    dict(model="Qwen-Image-2512", size="20B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Teks dalam gambar lebih tepat (Dis 2025), poster", space="Qwen/Qwen-Image-2512",
         gpu_s=120, size_gpu="xlarge", vram="~40 GB+ (agg.)", verdict="Kualiti tinggi, kuota mahal", tone="warn",
         repo="Qwen/Qwen-Image-2512"),
    dict(model="Qwen-Image", size="20B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Teks kompleks dalam gambar (Cina/Inggeris), edit", space="Qwen/Qwen-Image",
         gpu_s=120, size_gpu="large", vram="~40 GB+ (agg.)", verdict="Boleh guna", tone="", repo="Qwen/Qwen-Image"),
    dict(model="Qwen-Image-Fast (Qwen-Image + Lightning LoRA)", size="20B", cat="A",
         license="Apache 2.0 (semua komponen)", terms="Tiada", use="Versi laju Qwen-Image",
         space="mcp-tools/Qwen-Image-Fast", gpu_s=40, size_gpu="xlarge", vram="~40 GB+ (agg.)",
         verdict="Qwen paling jimat kuota", tone="warn", repo="lightx2v/Qwen-Image-Lightning"),
    dict(model="Qwen-Image-Edit-2511", size="20B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Edit gambar", space="Qwen/Qwen-Image-Edit-2511", gpu_s=180, size_gpu="large",
         vram="~40 GB+ (agg.)", verdict="Boleh guna", tone="", repo="Qwen/Qwen-Image-Edit-2511"),
    dict(model="MOSS-Image (SFT)", size="5B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Kawal letak teks guna JSON", space="OpenMOSS-Team/MOSS-Image", gpu_s=80, size_gpu="large",
         vram="~10 GB+ (agg.)", verdict="Boleh guna", tone="", repo="OpenMOSS-Team/MOSS-Image-SFT"),
    dict(model="MOSS-Image 8 langkah (DMD)", size="5B", cat="A", license="Apache 2.0",
         terms="Model masih dalam ujian (work-in-progress)", use="Versi laju MOSS-Image",
         space="hugging-apps/moss-image-8-step-dmd", gpu_s=16, size_gpu="large",
         vram="~20 GB+ (agg., transformer wajib FP32)", verdict="Paling banyak gambar/hari, masih ujian", tone="warn",
         repo="lodestones/MOSS-Image-SFT-8-steps-dmd"),
    dict(model="FLUX.2 [klein] 4B", size="4B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Sangat laju (4 langkah), edit guna beberapa gambar rujukan", space="black-forest-labs/FLUX.2-klein-4B",
         gpu_s=95, size_gpu="large", vram="13 GB", verdict="Laju, VRAM paling rendah", tone="warn",
         repo="black-forest-labs/FLUX.2-klein-4B"),
    dict(model="FLUX.1 [schnell]", size="12B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Laju (4 langkah)", space="black-forest-labs/FLUX.1-schnell", gpu_s=70, size_gpu="large",
         vram="~24 GB+ (agg.)", verdict="Boleh guna", tone="", repo="black-forest-labs/FLUX.1-schnell"),
    dict(model="GLM-Image", size="7B decoder", cat="A", license="MIT", terms="Tiada",
         use="Pengekod khas huruf (Glyph Encoder), teks tepat", space="multimodalart/GLM-Image",
         gpu_s=120, size_gpu="large", vram="~23 GB (dengan offload CPU)", verdict="Alternatif untuk teks", tone="warn",
         repo="zai-org/GLM-Image"),
    dict(model="HiDream-I1-Full", size="17B", cat="A", license="MIT",
         terms="Perlu terima lesen Llama 3.1 juga (pengekod teks)", use="Jana imej umum",
         space="Tiada Space khusus", gpu_s=None, gpu_note="—", vram="~34 GB+ (agg.)", verdict="Boleh guna", tone="",
         repo="HiDream-ai/HiDream-I1-Full"),
    dict(model="Chroma", size="8.9B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Seni, anime, foto. Tiada penapis kandungan", space="gokaygokay/Chroma", gpu_s=DEFAULT_GPU_S,
         size_gpu="large", vram="~18 GB (agg.)", verdict="Boleh guna", tone="", repo="lodestones/Chroma"),
    dict(model="Flex.1-alpha", size="8B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Model asas untuk latih LoRA", space="ostris/Flex.1-alpha", gpu_s=75, size_gpu="large",
         vram="~16 GB+ (agg.)", verdict="Boleh guna", tone="", repo="ostris/Flex.1-alpha"),
    dict(model="AuraFlow", size="6.8B", cat="A", license="Apache 2.0", terms="Tiada", use="Jana imej umum (2024)",
         space="gokaygokay/AuraFlow-with-Captioner", gpu_s=100, size_gpu="large", vram="~14 GB+ (agg.)",
         verdict="Boleh guna", tone="", repo="fal/AuraFlow"),
    dict(model="FireRed-Image-Edit-1.0", size="20B", cat="A", license="Apache 2.0", terms="Tiada",
         use="Edit gambar", space="Tiada Space rasmi", gpu_s=None, gpu_note="—", vram="~40 GB+ (agg.)",
         verdict="Boleh guna", tone="", repo="FireRedTeam/FireRed-Image-Edit-1.0"),
    dict(model="SDXL base 1.0 / SDXL-Lightning", size="2.6B", cat="A", license="OpenRAIL++",
         terms="Dilarang guna untuk tujuan berbahaya", use="Jana imej umum. Teks lemah",
         space="ByteDance/SDXL-Lightning", gpu_s=DEFAULT_GPU_S, size_gpu="large", vram="~6 GB+ (agg.)",
         verdict="Boleh guna", tone="", repo="stabilityai/stable-diffusion-xl-base-1.0"),
    # ---- B. Komersial bersyarat ----
    dict(model="FLUX 3 Image Klein", size="5.5B", cat="B", license="FLUX Kommunity v1.0",
         terms="Hasil < US$5 juta setahun. Wajib penapis atau semak hasil. Label AI jika undang-undang mewajibkan. "
               "Jangan guna hasil untuk latih model lain. Lesen boleh ditarik",
         use="Edit dan jana, teks dalam gambar, susun atur kotak", space="black-forest-labs/flux-3-image-klein",
         gpu_s=33, size_gpu="large", vram="31 GB BF16 / 26 GB FP8 / 25 GB NVFP4 (+28 GB alat prompt)",
         verdict="Boleh: semak hasil + label AI", tone="warn", repo="black-forest-labs/flux-3-image-klein"),
    dict(model="SD 3.5 Large / Large Turbo / Medium", size="8.1B / 8.1B / 2.5B", cat="B",
         license="Stability Community",
         terms="Hasil < US$1 juta setahun. Wajib daftar dengan Stability. Jangan guna hasil untuk latih model asas lain",
         use="Jana imej umum", space="stabilityai/stable-diffusion-3.5-large (Turbo 60 s)", gpu_s=65,
         size_gpu="large", vram="Large ~16 GB+, Medium ~5 GB+ (agg.)", verdict="Boleh, ikut syarat", tone="warn",
         repo="stabilityai/stable-diffusion-3.5-large"),
    dict(model="SDXL-Turbo", size="2.6B", cat="B", license="Stability Community (label HF: sai-nc-community)",
         terms="Hasil < US$1 juta setahun. Wajib daftar dengan Stability", use="Sangat laju (1–4 langkah)",
         space="diffusers/unofficial-SDXL-Turbo-i2i-t2i", gpu_s=60, size_gpu="large", vram="~6 GB+ (agg.)",
         verdict="Boleh, ikut syarat", tone="warn", repo="stabilityai/sdxl-turbo"),
    dict(model="Krea 2 (Turbo / Raw)", size="12B", cat="B", license="Krea 2 Community",
         terms="Hasil < US$1 juta (12 bulan lepas). Notis atribusi jika edar model. Raw tidak disyorkan untuk jana",
         use="Gaya estetik, ada koleksi LoRA", space="krea/Krea-2 (8 langkah)", gpu_s=41, size_gpu="xlarge",
         vram="~24 GB+ (agg.)", verdict="Boleh, ikut syarat", tone="warn", repo="krea/Krea-2-Turbo"),
    dict(model="Kolors", size="2.6B", cat="B", license="Apache 2.0 + Model License",
         terms="Wajib isi borang dan emel Kuaishou sebelum guna komersial. > 100 juta pengguna sebulan perlu lesen",
         use="Foto realistik, teks Cina dan Inggeris", space="Kwai-Kolors/Kolors", gpu_s=DEFAULT_GPU_S,
         size_gpu="large", vram="~5 GB+ (agg.)", verdict="Boleh selepas daftar", tone="warn", repo="Kwai-Kolors/Kolors"),
    dict(model="Playground v2.5", size="2.6B", cat="B", license="Playground Community",
         terms="Perlu lesen jika jana imej bisnes teras DAN > 1 juta pengguna sebulan. Jangan guna hasil untuk latih model lain",
         use="Gambar estetik", space="playgroundai/playground-v2.5", gpu_s=DEFAULT_GPU_S, size_gpu="large",
         vram="~6 GB+ (agg.)", verdict="Boleh, ikut syarat", tone="warn",
         repo="playgroundai/playground-v2.5-1024px-aesthetic"),
    dict(model="HunyuanImage 3.0", size="80B MoE (13B aktif)", cat="B", license="Tencent Hunyuan Community",
         terms="Tidak sah di EU, UK dan Korea Selatan. > 100 juta pengguna sebulan perlu lesen",
         use="Jana imej kualiti tinggi", space="akhaliq/HunyuanImage-3.0 (CPU, perlu akaun PRO)", gpu_s=None,
         gpu_note="Perlu PRO", vram="~160 GB (agg., README guna 4 GPU)", verdict="Terlalu besar untuk anda",
         tone="warn", repo="tencent/HunyuanImage-3.0"),
    dict(model="HunyuanImage 2.1", size="—", cat="B", license="Tencent Hunyuan Community",
         terms="Tidak sah di EU, UK dan Korea Selatan. > 100 juta pengguna sebulan perlu lesen",
         use="Jana imej 2K", space="Tiada Space khusus", gpu_s=None, gpu_note="—", vram="24 GB (FP8, gambar 2K)",
         verdict="Boleh, ikut syarat", tone="warn", repo="tencent/HunyuanImage-2.1"),
    # ---- C. Bukan komersial ----
    dict(model="FLUX.2 [dev]", size="32B", cat="C", license="FLUX Non-Commercial v2.1",
         terms="Model hanya untuk bukan komersial (jual hasil = bayaran tidak langsung). Lesen komersial: bfl.ai/licensing",
         use="Jana dan edit", space="black-forest-labs/FLUX.2-dev", gpu_s=75, size_gpu="xlarge",
         vram="RTX 4090 dengan 4-bit + pengekod teks jauh", verdict="Elak untuk jualan", tone="bad",
         repo="black-forest-labs/FLUX.2-dev"),
    dict(model="FLUX.2 [klein] 9B", size="9B", cat="C", license="FLUX Non-Commercial v2.1",
         terms="Model hanya untuk bukan komersial", use="Jana dan edit, laju", space="black-forest-labs/FLUX.2-klein-9B",
         gpu_s=95, size_gpu="xlarge", vram="29 GB", verdict="Elak untuk jualan", tone="bad",
         repo="black-forest-labs/FLUX.2-klein-9B"),
    dict(model="FLUX.1 [dev]", size="12B", cat="C", license="FLUX.1 Non-Commercial",
         terms="Model hanya untuk bukan komersial", use="Jana imej", space="black-forest-labs/FLUX.1-dev",
         gpu_s=75, size_gpu="large", vram="~24 GB+ (agg.)", verdict="Elak untuk jualan", tone="bad",
         repo="black-forest-labs/FLUX.1-dev"),
    dict(model="FLUX.1 Kontext [dev]", size="12B", cat="C", license="FLUX.1 Non-Commercial",
         terms="Model hanya untuk bukan komersial", use="Edit gambar", space="black-forest-labs/FLUX.1-Kontext-Dev",
         gpu_s=70, size_gpu="large", vram="~24 GB+ (agg.)", verdict="Elak untuk jualan", tone="bad",
         repo="black-forest-labs/FLUX.1-Kontext-dev"),
    dict(model="Qwen-Image-2.1", size="7B", cat="C", license="Qwen Research",
         terms="Penyelidikan dan penilaian sahaja. Komersial perlu lesen berasingan",
         use="Gambar latar lutsinar (RGBA), jana dan edit", space="Qwen/Qwen-Image-2.1", gpu_s=25,
         size_gpu="large", vram="~14 GB+ (agg.)", verdict="Elak untuk jualan", tone="bad", repo="Qwen/Qwen-Image-2.1"),
    dict(model="Ideogram 4", size="9.3B", cat="C", license="Ideogram Non-Commercial",
         terms="Jelas melarang guna hasil untuk produk berbayar atau iklan",
         use="Teks terbaik antara model terbuka (dakwaan pembuat)", space="ideogram-ai/ideogram4 (minimum 60 s)",
         gpu_s=60, size_gpu="xlarge", vram="~9 GB+ FP8 (agg.)", verdict="Elak untuk jualan", tone="bad",
         repo="ideogram-ai/ideogram-4-fp8"),
    dict(model="Bria Fibo 2.0 dev", size="8B", cat="C", license="CC BY-NC 4.0",
         terms="Bukan komersial", use="Edit dan jana dalam satu model", space="briaai/Fibo-2.0-T2I",
         gpu_s=120, size_gpu="large", vram="~16 GB+ (agg.)", verdict="Elak untuk jualan", tone="bad",
         repo="briaai/Fibo-2.0-dev"),
]

CAT = {"A": ("Ya", "ok", "A. Bebas komersial"), "B": ("Ya", "warn", "B. Komersial bersyarat"),
       "C": ("Tidak", "bad", "C. Bukan komersial")}


def free_seconds():
    return next(q["minutes"] for q in QUOTA if q["tier"] == "Free") * 60


def build_rows():
    rows = []
    for m in MODELS:
        commercial, ctone, group = CAT[m["cat"]]
        if m["gpu_s"] is None:
            gpu, img = m["gpu_note"], None
        else:
            mult = SIZE_MULT[m["size_gpu"]]
            gpu = f'{m["gpu_s"]} s · {m["size_gpu"]}' + (f" ({mult}×)" if mult > 1 else "")
            img = math.floor(free_seconds() / (m["gpu_s"] * mult))
        rows.append({
            "model": m["model"], "group": group, "size": m["size"], "commercial": commercial,
            "commercial_tone": ctone, "license": m["license"], "terms": m["terms"], "use": m["use"],
            "space": m["space"], "gpu": gpu, "img_free": img, "vram": m["vram"],
            "verdict": m["verdict"], "tone": m["tone"], "level": "rasmi", "source": HF + m["repo"],
            "checked": CHECKED,
        })
    return rows


def write_md(rows):
    out = [
        "# Lesen komersial, kuota GPU dan VRAM: model jana imej di Hugging Face",
        "",
        f"Semakan {CHECKED}. Dijana oleh `scripts/build_ai_licenses.py` (jangan ubah manual).",
        "Sumber: fail LICENSE / model card di HF (rasmi), `app.py` setiap Space (rasmi), "
        "dokumen ZeroGPU https://huggingface.co/docs/hub/spaces-zerogpu (rasmi).",
        "",
        "## Kuota ZeroGPU sehari",
        "",
    ]
    out += [f"- {q['tier']}: {q['minutes']} minit. {q['note']}" for q in QUOTA]
    out += [
        "- Saiz `large` (48 GB) kira 1×, `xlarge` (96 GB) kira 2×. Tanpa `duration`, Space minta 60 s.",
        f"- Gambar/hari = paling kurang gambar 1024² untuk akaun Free ({free_seconds()} s) "
        "= kuota ÷ (masa GPU maksimum Space × saiz). Kuota ditolak ikut masa sebenar, jadi biasanya lebih.",
        "- VRAM \"agg.\" = anggaran 2 GB setiap 1B parameter (BF16); lain-lain daripada model card.",
        "",
        "## Jadual",
        "",
        "| Model | Saiz | Komersial? | Lesen | Had / syarat | Kegunaan | Space | GPU / gambar | Gambar/hari (Free) | VRAM | Cadangan |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    group = None
    for r in rows:
        if r["group"] != group:
            group = r["group"]
            out.append(f"| **{group}** | | | | | | | | | | |")
        img = "–" if r["img_free"] is None else f"≥{r['img_free']}"
        out.append(" | ".join([
            f"| [{r['model']}]({r['source']})", r["size"], r["commercial"], r["license"], r["terms"], r["use"],
            r["space"], r["gpu"], img, r["vram"], r["verdict"] + " |",
        ]))
    DOC.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    code = Path(__file__).read_text(encoding="utf-8")
    meta = [
        {"label": "build_ai_licenses.py", "value": code, "type": "code", "lang": "python"},
        {"label": "Disemak", "value": CHECKED},
        {"label": "Sumber", "value": "LICENSE / model card HF, app.py Space, dokumen ZeroGPU HF"},
    ]
    (OUT / "ai_licenses.json").write_text(
        json.dumps({"rows": rows, "meta": meta}, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "hf_zerogpu_quota.json").write_text(json.dumps({"rows": QUOTA, "meta": [
        {"label": "Sumber", "value": "https://huggingface.co/docs/hub/spaces-zerogpu"},
        {"label": "Disemak", "value": CHECKED},
    ]}, ensure_ascii=False, indent=1), encoding="utf-8")
    write_md(rows)
    print(f"{len(rows)} baris -> {OUT / 'ai_licenses.json'}, {DOC}")


if __name__ == "__main__":
    main()
