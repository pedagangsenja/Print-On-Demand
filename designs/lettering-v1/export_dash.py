"""Standard Lettering v1: eksport hasil ujian 5 model ke tab dashboard "AI Image Test 2".
Baca qc/<model>.json, raw/<model>/log.jsonl, kad.py dan dash_blobs.txt (id gambar yang dimuat naik ke artifact).
Tulis data/export/ai_test2/{ai2_images,ai2_models,ai2_refs}.json.
Guna: python3 export_dash.py
"""
import json
from pathlib import Path

import kad

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "data" / "export" / "ai_test2"
MODELS = [  # turutan ujian (laju dahulu); status ikut keputusan pengguna 25 Nov 2026
    dict(model="klein4b", p="kl", model_name="FLUX.2 klein 4B", status="Diuji"),
    dict(model="schnell", p="sc", model_name="FLUX.1-schnell", status="Diuji"),
    dict(model="chroma_flash", p=None, model_name="Chroma1-Flash", status="Dilangkau",
         note="Terlalu perlahan di CPU; anda minta langkau"),
    dict(model="zturbo", p="zt", model_name="Z-Image-Turbo", status="Diuji"),
    dict(model="ernie", p="er", model_name="ERNIE-Image-Turbo", status="Diuji"),
    dict(model="moss", p="mo", model_name="MOSS-Image-SFT + LoRA 8 langkah", status="Diuji"),
    dict(model="kandinsky", p=None, model_name="Kandinsky 2.2", status="Tidak diuji",
         note="Keputusan anda: 6 model sahaja"),
]
AYAT_NAMA = {"P": "Pendek", "D": "Sederhana", "L": "Panjang"}


def main():
    blob = dict(l.split() for l in (HERE / "dash_blobs.txt").read_text().splitlines() if l.strip())
    OUT.mkdir(parents=True, exist_ok=True)
    images, models = [], []
    for order, m in enumerate(MODELS, 1):
        row = dict(model=m["model"], model_name=m["model_name"], model_order=order, status=m["status"],
                   note=m.get("note", ""), repo=None, versi=None)
        if m["p"]:
            logs = {}
            for l in (HERE / "raw" / m["model"] / "log.jsonl").read_text().splitlines():
                if l.strip():
                    r = json.loads(l); logs[f"{r['id']}_s{r['seed']}"] = r
            first = next(iter(logs.values()))
            row.update(repo=first["repo"], versi=f"{first['varian']} · {first['langkah']} langkah"
                       + (f" · LoRA {first['lora'].split()[-1]}" if first.get("lora") else ""))
            for q in json.loads((HERE / "qc" / f"{m['model']}.json").read_text()):
                k, a, s = q["id"][:2], q["id"][2], int(q["id"].split("_s")[1])
                images.append(dict(
                    key=f"{m['model']}|{q['id']}", model=m["model"], model_name=m["model_name"], model_order=order,
                    id=q["id"], kad=k, kad_name=kad.KAD[k]["nama"], ayat=a, ayat_name=AYAT_NAMA[a],
                    text=kad.AYAT[a]["ayat"], seed=s, img=f"/_blob/{blob[m['p'] + '_' + q['id']]}",
                    w=600, h=800, lulus=q["lulus"], g1=q["g1_ejaan"], g2=q["g2_tiada_teks_rawak"],
                    g3=q["g3_tiada_cacat"], teras=q["teras"], gaya=q["gaya"], gaya_n=int(q["gaya"].split("/")[0]),
                    sebab=q["sebab"], saat=logs[q["id"]]["saat"]))
        models.append(row)
    refs = [dict(kad=k, kad_name=v["nama"], ref=v["ref"], ref_img=f"/_blob/{blob['ref_' + k]}",
                 teras="; ".join(c for c, t in v["qc"] if t), ciri_lain="; ".join(c for c, t in v["qc"] if not t))
            for k, v in kad.KAD.items()]
    for name, rows in [("ai2_images", images), ("ai2_models", models), ("ai2_refs", refs)]:
        (OUT / f"{name}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n")
        print(name, len(rows))


if __name__ == "__main__":
    main()
