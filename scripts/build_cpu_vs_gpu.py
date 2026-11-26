"""Tab dashboard "CPU vs GPU": ujian K6 (Standard Lettering v1), 6 enjin x 3 ayat x 2 seed, di CPU dan Kaggle GPU.

Input:  designs/lettering-v1/raw/<folder>/<enjin>/log.jsonl dan qc/<qc>.json bagi setiap peranti dalam DEV,
        qc/k6_dashboard_blobs.json (url gambar). Peranti: cpu (container), gpu (Kaggle T4), hf (Space ZeroGPU).
Output: data/export/cpu_vs_gpu/{cvg_enjin,cvg_ayat,cvg_imej,cvg_peranti}.json, format {rows, meta}.
Lajur GPU kosong (null) selagi tiada log GPU: tiada angka direka.
"""
import json
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "designs/lettering-v1"
OUT = ROOT / "data/export/cpu_vs_gpu"
ENJIN = [("moss", "MOSS-Image SFT + LoRA 8 langkah"), ("ernie", "ERNIE-Image-Turbo"), ("zturbo", "Z-Image-Turbo"),
         ("klein4b", "FLUX.2 klein 4B"), ("schnell", "FLUX.1-schnell"), ("chroma_flash", "Chroma1-Flash")]
AYAT = {"P": "Pendek (4 perkataan)", "D": "Sederhana (7)", "L": "Panjang (11)"}
TEKS = {"P": "Brave Hearts Begin Again", "D": "Every Small Step Builds a Bolder You",
        "L": "Keep Showing Up on Hard Days Because Better Mornings Are Coming"}
# Nota gaya: semakan mata Claude pada helaian QC 25 Nov 2026 (CPU). Tahap bukti lemah.
GAYA = {"moss": "Paling serupa rujukan: swash atas, bawah dan celah, bintang, berus kering",
        "ernie": "Baik; bingkai kelabu di tepi perlu dipotong",
        "zturbo": "Baik; salah huruf besar ('small') dan titik tambahan",
        "klein4b": "Baik; paling laju",
        "schnell": "Lemah: tiada swash, tiada bintang; perkataan berulang",
        "chroma_flash": "Swash reben kuat tetapi huruf rosak, padat, teks rawak"}
DEV = {"cpu": ("k6-cpu", "k6_cpu"), "gpu": ("k6-gpu", "k6_gpu"), "hf": ("k6-gpu-hf", "k6_gpu_hf")}
SASARAN = {"cpu": 36, "gpu": 36, "hf": 6}
PERANTI = [
    dict(peranti="CPU", tempat="Container sesi Claude Code",
         butiran="Intel Xeon 2.1 GHz, 4 teras, AMX bf16, 15 GB RAM (lscpu / free, 25 Nov 2026)",
         status_awal="Siap"),
    dict(peranti="GPU", tempat="Kaggle notebook abdulazim1411/pod-lettering-k6-gpu",
         butiran="NVIDIA T4 x2, 16 GB setiap satu; kuota 30 jam seminggu (Kaggle API, 25 Nov 2026)",
         status_awal="Menunggu giliran GPU (queued); belum berjalan"),
    dict(peranti="GPU HF", tempat="Space awam Hugging Face (ZeroGPU): Z-Image-Turbo dan MOSS 8 langkah",
         butiran=("GPU dikongsi Hugging Face, jenis kad tidak dilaporkan; 2 enjin x 3 ayat x seed 42 sahaja; masa = jam "
                  "dinding termasuk barisan dan rangkaian; kuota akaun Free 5 minit GPU sehari (dokumen rasmi ZeroGPU)"),
         status_awal="Belum berjalan"),
]


def load(dev):
    raw, qc = V1 / "raw" / DEV[dev][0], V1 / "qc" / f"{DEV[dev][1]}.json"
    logs = {}
    for e, _ in ENJIN:
        f = raw / e / "log.jsonl"
        if f.exists():
            for line in f.read_text().splitlines():
                r = json.loads(line)
                logs[(e, f"{r['id']}_s{r['seed']}")] = r
    q = {(r["model"], r["id"]): r for r in json.loads(qc.read_text())} if qc.exists() else {}
    return logs, q


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bf = V1 / "qc/k6_dashboard_blobs.json"  # url gambar di dashboard (hasil muat naik)
    blobs = json.loads(bf.read_text()) if bf.exists() else {}
    data = {d: load(d) for d in DEV}
    imej, enjin, ayat = [], [], []
    for e, nama in ENJIN:
        per = {d: [] for d in data}
        for a in AYAT:
            for s in (42, 7):
                iid = f"K6{a}_s{s}"
                row = dict(kunci=f"{e}-{iid}", enjin=nama, ayat=AYAT[a], seed=s)
                for d, (logs, q) in data.items():
                    lg, qq = logs.get((e, iid)), q.get((e, iid))
                    row[f"{d}_saat"] = lg["saat"] if lg else None
                    row[f"{d}_ejaan"] = None if not qq else ("Lulus" if qq["ejaan"] else "Gagal")
                    row[f"{d}_sebab"] = qq.get("sebab") or None if qq else None
                    row[f"{d}_img"] = blobs.get(f"{d}_{e}_{iid}")
                    per[d].append((a, lg, qq))
                imej.append(row)
        r = dict(enjin=nama, gaya_cpu=GAYA[e])
        for d in data:
            ts = [lg["saat"] for _, lg, _ in per[d] if lg]
            ok = [qq for _, _, qq in per[d] if qq]
            r[f"{d}_imej"] = len(ts)
            r[f"{d}_ejaan"] = f"{sum(q['ejaan'] for q in ok)}/{len(ok)}" if ok else None
            r[f"{d}_ejaan_n"] = sum(q["ejaan"] for q in ok) if ok else None
            r[f"{d}_saat"] = round(st.mean(ts)) if ts else None
            r[f"{d}_minit"] = round(sum(ts) / 60, 1) if ts else None
        for d in ("gpu", "hf"):  # banding imej yang sama sahaja (id dan seed sama)
            pair = [(c[1]["saat"], g[1]["saat"]) for c, g in zip(per["cpu"], per[d]) if c[1] and g[1]]
            r[f"{d}_laju_x"] = round(st.mean(a for a, _ in pair) / st.mean(b for _, b in pair)) if pair else None
        enjin.append(r)
        ra = dict(enjin=nama)
        for d in data:
            for a in AYAT:
                ok = [qq for aa, _, qq in per[d] if aa == a and qq]
                ra[f"{d}_{a}"] = f"{sum(q['ejaan'] for q in ok)}/{len(ok)}" if ok else None
        ayat.append(ra)
    peranti = []
    for p in PERANTI:
        d = {"CPU": "cpu", "GPU": "gpu", "GPU HF": "hf"}[p["peranti"]]
        n = sum(1 for r in imej if r[f"{d}_saat"] is not None)
        st_ = p["status_awal"] if n == 0 else "Siap" if n == SASARAN[d] else f"{n}/{SASARAN[d]} imej"
        peranti.append(dict(p, imej=n, ref_img=blobs.get("ref_K6") if d == "cpu" else None, status=st_))
    code = Path(__file__).read_text()
    meta = [dict(label="build_cpu_vs_gpu.py", value=code, type="code", lang="python"),
            dict(label="Input", value="designs/lettering-v1/raw/k6-*/<enjin>/log.jsonl, designs/lettering-v1/qc/k6_*.json"),
            dict(label="Tahap bukti", value="lemah: 2 seed setiap ayat, ejaan disemak dengan mata oleh Claude"),
            dict(label="Ayat", value=" | ".join(f"{k}: {v}" for k, v in TEKS.items()))]
    for name, rows in (("cvg_enjin", enjin), ("cvg_ayat", ayat), ("cvg_imej", imej), ("cvg_peranti", peranti)):
        (OUT / f"{name}.json").write_text(json.dumps(dict(rows=rows, meta=meta), ensure_ascii=False, indent=1))
        print(name, len(rows), "baris")


if __name__ == "__main__":
    main()
