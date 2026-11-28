"""SK10 Ringkas: sambung QC B ke "belajar selepas setiap jana" (Standard Lettering v1.2, 3.15). Versi 1.0, 28 Nov 2026.

Tugas: kumpul hasil QC B (ciri lulus / gagal lawan gambar upload, jadual SK11) bagi SEMUA imej betul/ yang kadnya ada
gambar rujukan, kemudian cari ciri yang gagal BERULANG, dan tukar setiap satu kepada calon ubahan seterusnya:
  - gagal berulang pada kebanyakan model untuk satu kad  -> ubah FRASA KAD kepada frasa sasaran (ciri gaya);
  - gagal berulang pada satu model sahaja                -> ubah ATURAN MODEL itu, atau tukar model untuk kad itu;
  - condong blok                                         -> bukan prompt: skrip 5b (SK01).
"Berulang" = gagal pada sekurang-kurangnya 2 imej DAN sekurang-kurangnya 2 / 3 imej gabungan kad x model itu
(sama dengan takrif cacat sistematik dalam kitaran QC).
Calon sahaja: belajar.py memaparkannya; Claude dan pengguna memutuskan. Tidak mengubah kad atau aturan sendiri.
Had: ciri "tepi_strok" dan "tebal_utama" lemah sebagai ukuran (banding/ciri_ujian.json), jadi ditanda "ukuran lemah".

Guna: python3 skrip/SK10_ringkas.py      -> banding/qcb_ringkasan.json + ringkasan di skrin
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
AKAR = HERE.parent
sys.path.insert(0, str(HERE))
VERSI = "SK10_ringkas v1.0"
# Kekuatan setiap ciri sebagai ukuran, daripada ujian 384 imej (banding/ciri_ujian.json): beza antara kadar lulus
# dengan rujukan sendiri dan dengan rujukan lain. kuat = 20 mata ke atas; sederhana = 10-20; lemah = bawah 10.
KUAT = {"condong_huruf_utama", "penjajaran", "saiz_sokongan", "condong_huruf_sokongan", "kontras_strok"}
LEMAH = {"tepi_strok", "tebal_utama", "hubungan_baris"}
SKRIP = {"condong_blok": "skrip 5b (SK01), bukan prompt"}


def ringkas():
    import SK11_frasa as F
    import tentukur_sk10 as T
    rk, ruj, jana, kad_imej = T.muat()
    ruj_kad = {k: v[0] for k, v in rk.items()}
    kump = defaultdict(lambda: dict(imej=0, gagal=defaultdict(int), sasaran={}, dapat={}))
    for kunci, rek in jana.items():
        kid = kad_imej[kunci]
        nama = ruj_kad[kid]
        if nama not in ruj:
            continue
        model = kunci.split("/")[1]
        g = kump[(kid, model)]
        g["imej"] += 1
        for c in F.banding_ciri(ruj[nama], rek):
            if c.get("kira", True) and c["lulus"] is False:
                g["gagal"][c["ciri"]] += 1
                g["sasaran"][c["ciri"]] = (c["tong_rujukan"], c["frasa_rujukan"])
                g["dapat"][c["ciri"]] = c["tong_jana"]
    berulang = []
    for (kid, model), g in sorted(kump.items(), key=lambda x: (int(re.sub(r"\D", "", x[0][0])), x[0][1])):
        for ciri, n in g["gagal"].items():
            if n >= 2 and n >= 2 / 3 * g["imej"]:
                berulang.append(dict(kad=kid, model=model, ciri=ciri, gagal=n, imej=g["imej"], dapat=g["dapat"][ciri],
                                     sasaran=g["sasaran"][ciri][0], frasa_sasaran=g["sasaran"][ciri][1]))
    ikut_kad = defaultdict(list)
    for b in berulang:
        ikut_kad[(b["kad"], b["ciri"])].append(b)
    model_kad = defaultdict(set)
    for (kid, model) in kump:
        model_kad[kid].add(model)
    calon = []
    for (kid, ciri), bs in ikut_kad.items():
        n_model = len(model_kad[kid])
        if ciri in SKRIP:
            jenis, teks = "skrip", SKRIP[ciri]
        elif len(bs) >= max(2, round(0.6 * n_model)):
            jenis = "kad"
            teks = "ubah frasa kad %s: %s -> %s" % (kid, ciri, bs[0]["frasa_sasaran"] or bs[0]["sasaran"])
        else:
            jenis = "model"
            teks = "kad %s: %s gagal pada %s sahaja -> ubah aturan model itu atau tukar model" % (
                kid, ciri, ", ".join(b["model"] for b in bs))
        calon.append(dict(kad=kid, ciri=ciri, jenis=jenis, model_gagal=[b["model"] for b in bs], bil_model=n_model,
                          dapat=bs[0]["dapat"], sasaran=bs[0]["sasaran"], frasa_sasaran=bs[0]["frasa_sasaran"],
                          kekuatan="lemah" if ciri in LEMAH else "kuat" if ciri in KUAT else "sederhana",
                          ukuran_lemah=ciri in LEMAH, tindakan=teks))
    hasil = dict(versi=VERSI, tarikh="2026-11-28", imej=sum(g["imej"] for g in kump.values()), gabungan_kad_model=len(kump),
                 nota=("Calon ubahan daripada QC B (ciri gagal berulang lawan gambar upload). Calon sahaja; ukuran_lemah = ciri "
                       "yang ujian 384 imej tunjuk lemah sebagai ukuran. Dikira daripada imej betul/ sedia ada."),
                 ringkasan=dict(calon=len(calon), kad=sum(c["jenis"] == "kad" for c in calon),
                                model=sum(c["jenis"] == "model" for c in calon), skrip=sum(c["jenis"] == "skrip" for c in calon),
                                ukuran_lemah=sum(c["ukuran_lemah"] for c in calon),
                                kad_ukuran_kuat=sum(c["jenis"] == "kad" and c["kekuatan"] == "kuat" for c in calon)),
                 calon=sorted(calon, key=lambda c: (["kuat", "sederhana", "lemah"].index(c["kekuatan"]), c["jenis"] != "kad",
                                                    int(re.sub(r"\D", "", c["kad"])))))
    (AKAR / "banding").mkdir(exist_ok=True)
    (AKAR / "banding" / "qcb_ringkasan.json").write_text(json.dumps(hasil, ensure_ascii=False, indent=1) + "\n")
    return hasil


def cetak(hasil, had=12):
    r = hasil["ringkasan"]
    print("\nQC B (%s): %d imej, %d gabungan kad x model; %d calon ubahan (%d kad, %d model, %d skrip; %d ukuran lemah)" % (
        VERSI, hasil["imej"], hasil["gabungan_kad_model"], r["calon"], r["kad"], r["model"], r["skrip"], r["ukuran_lemah"]))
    for c in [c for c in hasil["calon"] if c["jenis"] == "kad" and c["kekuatan"] == "kuat"][:had]:
        print("  CALON [kad, ukuran kuat]: %s (dapat: %s; rujukan: %s; gagal pada %d / %d model)" % (
            c["tindakan"], c["dapat"], c["sasaran"], len(c["model_gagal"]), c["bil_model"]))


if __name__ == "__main__":
    cetak(ringkas(), had=40)
