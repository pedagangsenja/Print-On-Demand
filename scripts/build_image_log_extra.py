"""Baris tambahan Daftar ujian imej AI (dataset dashboard `image_log`) daripada ujian Standard Lettering v1.

Input:  designs/lettering-v1/raw/<folder>/<enjin>/log.jsonl  (tetapan dan masa setiap imej)
        designs/lettering-v1/qc/<qc>.json                    (semakan mata + id aset imej; tiada angka direka)
Output: data/export/models/image_log_extra.json              (baris baharu sahaja)
        data/export/models/image_log.json                    (hanya jika --asas diberi: baris sedia ada + baharu)
Guna:   python3 scripts/build_image_log_extra.py [--asas <image_log.json semasa dari dashboard>]
Format baris sama dengan scripts/build_image_log.py (cawangan claude/vigilant-knuth-0bmbio).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "designs/lettering-v1"
OUT = ROOT / "data/export/models"
ENJIN = {"klein4b": ("FLUX.2 klein 4B", ""), "zturbo": ("Z-Image-Turbo", ""), "ernie": ("ERNIE-Image-Turbo", ""),
         "moss": ("MOSS-Image SFT", "LoRA 8 langkah")}
# (fail qc, folder raw, awalan id, tarikh, tujuan, variasi prompt, gaya)
SET = [
    ("k3h_cpu", "k3h-cpu", "k3h-am", "2026-11-26", "Standard v1.2: K3 × ayat H, rangka am (pembanding)",
     "rangka am, pembina v1.1", "K3 campuran sans + skrip + label, hitam putih"),
    ("k3h_cpu", "k3h-khas-cpu", "k3h-khas", "2026-11-26", "Standard v1.2: K3 × ayat H, aturan ikut model r1",
     "aturan model r1 (khas.py)", "K3 campuran sans + skrip + label, hitam putih"),
    ("v12_pembina_cpu", "v12-pembina-cpu", "v12-pembina", "2026-11-26",
     "Standard v1.2: pembina kod ikut model (K3H ulangan, K6P kad lain)", "pembina kod v1.2-p1",
     {"K3H": "K3 campuran sans + skrip + label, hitam putih", "K6P": "K6 skrip berus + swash reben, hitam putih"}),
]
TEKS = {"K3H": "PATIENCE / Builds / WHAT / Hurry / BREAKS", "K6P": "Brave / Hearts / Begin / Again"}


def baris():
    out = []
    for qc_fail, folder, awalan, tarikh, tujuan, variasi, gaya in SET:
        f = V1 / "qc" / f"{qc_fail}.json"
        if not f.exists():
            continue
        qc = json.loads(f.read_text()).get(folder, {})
        for enjin, imej in qc.items():
            log = {}
            lf = V1 / "raw" / folder / enjin / "log.jsonl"
            for ln in (lf.read_text().splitlines() if lf.exists() else []):
                r = json.loads(ln)
                log[(r["id"], str(r["seed"]))] = r
            nama, var = ENJIN[enjin]
            for kunci, (ok, salah, img) in imej.items():
                idd, seed = kunci.split("_s") if "_s" in kunci else ("K3H", kunci)
                r = log.get((idd, seed), {})
                v = "; ".join(x for x in (var, variasi, "penambah prompt" if "hidup" in str(r.get("penambah")) and enjin == "ernie" else "") if x)
                w, h = r.get("w"), r.get("h")
                out.append(dict(id=f"{awalan}-{idd}-{enjin}-s{seed}", date=tarikh, engine=nama, variant=v,
                                where="Container CPU (4 teras)", purpose=tujuan, text=TEKS[idd],
                                style=gaya[idd] if isinstance(gaya, dict) else gaya, seed=int(seed), w=w, h=h,
                                seconds=r.get("saat"), wrong=salah, img=img, source=f"lettering-v1/{folder}",
                                level="lemah", steps=r.get("langkah"), size=f"{w}×{h}" if w and h else "—",
                                result="Lulus" if ok else "Tolak", tone="ok" if ok else "bad"))
    return out


def main():
    rows = baris()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "image_log_extra.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n")
    print("image_log_extra:", len(rows), "baris;", sum(r["result"] == "Lulus" for r in rows), "lulus")
    if "--asas" in sys.argv:
        asas = json.loads(Path(sys.argv[sys.argv.index("--asas") + 1]).read_text())
        baru = {r["id"] for r in rows}
        semua = [r for r in asas["rows"] if r["id"] not in baru] + rows
        semua.sort(key=lambda r: (r["date"], r["engine"], r["id"]))
        meta = [m for m in asas.get("meta", []) if m.get("label") != "Tambahan"]
        meta.append({"label": "Tambahan", "value": "scripts/build_image_log_extra.py (ujian Standard Lettering v1)"})
        (OUT / "image_log.json").write_text(json.dumps({"rows": semua, "meta": meta}, ensure_ascii=False, indent=2) + "\n")
        print("image_log:", len(semua), "imej;", sum(r["result"] == "Lulus" for r in semua), "lulus")


if __name__ == "__main__":
    main()
