"""Langkah 5b penuh: ukur -> SK01 condong -> SK02 ruang tepi -> SK03 kedudukan -> SK04 hitam putih bersih -> ukur semula.
Standard Lettering v1.2. Versi 1, 26 Nov 2026.

Turutan tetap. Setiap pembetulan hanya jalan bila ukurannya tersasar melebihi had (asas.HAD) dan kad ada angka
rujukannya. Tiga pembetulan pertama digabung menjadi SATU matriks dan imej asal dilukis semula sekali sahaja
(kurang kabur). Imej asal tidak ditimpa. Imej yang gagal pintu G1-G3 tidak patut dihantar ke sini.
Semakan akhir: tiada dakwat menyentuh tepi kanvas; ukuran dalam had. Jika gagal: lulus=False -> jana semula.
Ejaan MESTI disemak semula pada imej hasil (standard 5b).

Guna: python3 betulkan.py <kad> <folder keluar> <imej> [<imej> ...] [--condong D] [--tepi P]
Hasil: <folder keluar>/<nama imej> + <folder keluar>/log_5b.jsonl (ukuran sebelum, tindakan, ukuran selepas).
"""
import json
import sys
from pathlib import Path

import numpy as np

import asas
import SK01_condong
import SK02_ruang_tepi
import SK03_kedudukan
import SK04_hitam_putih

VERSI = "5b v1.2"


def betulkan(rgb, ruj, had=asas.HAD):
    sebelum, M, tindakan, semasa = asas.ukur(rgb), np.eye(3), {}, rgb
    for sk in (SK01_condong, SK02_ruang_tepi, SK03_kedudukan):
        m, cat = sk.matriks(asas.ukur(semasa), ruj, had)
        tindakan[sk.ID] = cat
        if m is not None:
            M = m @ M
            semasa = asas.lukis(rgb, M, halus=False)
    ubah = any(t["jalan"] for t in tindakan.values())
    hasil = asas.lukis(rgb, M) if ubah else rgb
    hasil, tindakan["SK04"] = SK04_hitam_putih.betul(hasil, ruj, had, selepas_ubah=ubah)
    selepas = asas.ukur(hasil)
    gagal = []
    if selepas["sentuh_tepi"]:
        gagal.append("dakwat menyentuh tepi kanvas (huruf mungkin terpotong)")
    if abs(SK02_ruang_tepi.beza_tepi(selepas, ruj)[0]) > had["tepi"]:
        gagal.append(f"ruang tepi masih di luar had: beza {SK02_ruang_tepi.beza_tepi(selepas, ruj)[0]} mata")
    if ruj["kad_condong"] and ruj["condong_darjah"] is not None and \
            abs(selepas["condong_darjah"] - ruj["condong_darjah"]) > had["condong"]:
        gagal.append(f"condong {selepas['condong_darjah']} masih di luar had (rujukan {ruj['condong_darjah']})")
    return hasil, dict(versi=VERSI, rujukan=ruj, had=had, sebelum=sebelum, tindakan=tindakan, selepas=selepas,
                       lulus=not gagal, gagal=gagal)


if __name__ == "__main__":
    a = sys.argv[1:]
    pil = {}
    while len(a) >= 2 and a[-2].startswith("--"):
        pil[a[-2][2:]] = a[-1]
        a = a[:-2]
    if len(a) < 3:
        sys.exit(__doc__)
    kid, keluar, ruj = a[0], Path(a[1]), asas.rujukan(a[0], pil.get("condong"), pil.get("tepi"))
    for f in a[2:]:
        hasil, log = betulkan(asas.muat(f), ruj)
        asas.simpan(hasil, keluar / Path(f).name)
        with open(keluar / "log_5b.jsonl", "a") as fh:
            fh.write(json.dumps(dict(imej=f, kad=kid, **log), ensure_ascii=False) + "\n")
        t = {k: (v.get("putar_darjah") or v.get("skala") or v.get("alih_px") or "jalan") for k, v in log["tindakan"].items() if v["jalan"]}
        print(Path(f).name, "| tindakan:", t or "tiada", "| condong", log["sebelum"]["condong_darjah"], "->",
              log["selepas"]["condong_darjah"], "| tepi sisi", min(log["sebelum"]["tepi"]["kiri"], log["sebelum"]["tepi"]["kanan"]), "->",
              min(log["selepas"]["tepi"]["kiri"], log["selepas"]["tepi"]["kanan"]), "atas/bawah",
              min(log["sebelum"]["tepi"]["atas"], log["sebelum"]["tepi"]["bawah"]), "->",
              min(log["selepas"]["tepi"]["atas"], log["selepas"]["tepi"]["bawah"]),
              "| lulus" if log["lulus"] else f"| GAGAL: {log['gagal']}")
