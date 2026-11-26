"""Tab dashboard "CPU vs GPU": ujian K6 (Standard Lettering v1), 6 enjin x 3 ayat x 2 seed, di CPU dan Kaggle GPU.

Input:  designs/lettering-v1/raw/<folder>/<enjin>/log.jsonl dan qc/<qc>.json bagi setiap peranti dalam DEV,
        qc/k6_dashboard_blobs.json (url gambar). Peranti: cpu (container), gpu (Kaggle T4), hf (Space ZeroGPU).
Output: data/export/cpu_vs_gpu/{cvg_enjin,cvg_banding,cvg_imej,cvg_peranti}.json, format {rows, meta}.
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
AYAT_LABEL = {"P": "Pendek", "D": "Sederhana", "L": "Panjang"}
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
    imej, enjin, banding = [], [], []
    for e, nama in ENJIN:
        per = {d: [] for d in data}
        ids = []
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
                ids.append((a, s, iid))
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
        for d in ("gpu", "hf"):  # banding imej yang sama sahaja (ayat dan seed sama di CPU dan GPU)
            sama = [(i, c, g) for i, c, g in zip(ids, per["cpu"], per[d]) if c[1] and g[1] and c[2] and g[2]]
            r[f"{d}_n"] = len(sama)
            r[f"{d}_cpu_saat"] = round(st.mean(c[1]["saat"] for _, c, _ in sama)) if sama else None
            r[f"{d}_saat_sama"] = round(st.mean(g[1]["saat"] for _, _, g in sama), 1) if sama else None
            r[f"{d}_cpu_ejaan"] = f"{sum(c[2]['ejaan'] for _, c, _ in sama)}/{len(sama)}" if sama else None
            r[f"{d}_ejaan_sama"] = f"{sum(g[2]['ejaan'] for _, _, g in sama)}/{len(sama)}" if sama else None
            r[f"{d}_laju_x"] = round(r[f"{d}_cpu_saat"] / r[f"{d}_saat_sama"]) if sama else None
            for (a, sd, iid), c, g in sama:
                banding.append(dict(kunci=f"{d}-{e}-{iid}", gpu={"gpu": "GPU Kaggle", "hf": "GPU HF"}[d], enjin=nama,
                                    ayat=AYAT_LABEL[a], teks=TEKS[a], seed=sd, cpu_saat=c[1]["saat"], gpu_saat=g[1]["saat"],
                                    kali=round(c[1]["saat"] / g[1]["saat"]),
                                    cpu_ejaan="Lulus" if c[2]["ejaan"] else "Gagal", gpu_ejaan="Lulus" if g[2]["ejaan"] else "Gagal",
                                    cpu_sebab=c[2].get("sebab") or None, gpu_sebab=g[2].get("sebab") or None,
                                    cpu_img=blobs.get(f"cpu_{e}_{iid}"), gpu_img=blobs.get(f"{d}_{e}_{iid}")))
        enjin.append(r)
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
    for name, rows in (("cvg_enjin", enjin), ("cvg_banding", banding), ("cvg_imej", imej), ("cvg_peranti", peranti)):
        (OUT / f"{name}.json").write_text(json.dumps(dict(rows=rows, meta=meta), ensure_ascii=False, indent=1))
        print(name, len(rows), "baris")


if __name__ == "__main__":
    main()
