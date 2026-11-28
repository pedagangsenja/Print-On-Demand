"""Langkah 6 penuh bagi satu kad: SK07 warna ikut peranan -> SK08 bayang (jika kad ada rujukan bayang) -> SK06
vektor + saiz cetak dengan palet tepat. Standard Lettering v1.2. Versi 1, 27 Nov 2026.

Input = imej hitam putih yang lulus QC + 5b (folder betul/). Imej yang GAGAL SK07 dilangkau dan dilapor (kekal
hitam putih atau jana semula). Tekstur ikut kad (SK06 v1.1 --kad); gaya S1-S6 untuk palet lalai sahaja.

Guna: python3 kemasan.py <kad> <ayat> <gaya S1..S6> <folder keluar> <imej> [<imej> ...] [--warna Cxxx] [--sizes 18x24]
Hasil: <folder keluar>/peranan/ (SK07, SK08: peta, imej berwarna, palet, log_6.jsonl) dan
       <folder keluar>/<model>_<nama imej>[_<warna C>]/ (SK06: master.svg, PNG 300 DPI, pratonton, info.json).
       Nama model = nama folder imej (cth. betul/v12-cpu/moss/K3K_s42.png -> moss_K3K_s42).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

import SK07_warna as sk07
import SK08_bayang as sk08
from SK05_ukur import muat

SINI = Path(__file__).resolve().parent

if __name__ == "__main__":
    a = sys.argv[1:]
    pil = {}
    while len(a) >= 2 and a[-2].startswith("--"):
        pil[a[-2][2:]] = a[-1]
        a = a[:-2]
    if len(a) < 5:
        sys.exit(__doc__)
    kid, aid, gaya, keluar = a[0], a[1], a[2], Path(a[3])
    pal = sk07.palet(kid, pil.get("warna"))
    ada_bayang = bool(sk07.kad.BLOK.get(kid, {}).get("rujukan", {}).get("bayang"))
    folder = keluar / "peranan"
    for f in map(Path, a[4:]):
        stem = f"{f.parent.name}_{f.stem}" + (f"_{pil['warna']}" if pil.get("warna") else "")   # folder = model
        im = muat(f)
        peta, cat = sk07.peranan(im, kid, aid, pil.get("warna"))
        a_ = sk07.alfa(im)
        if not sk07.tulis(folder, stem, peta, pal, dict(imej=str(f), kad=kid, ayat=aid, **cat), a_):
            print(stem, "| SK07 GAGAL:", "; ".join(cat["gagal"]), "-> dilangkau")
            continue
        akhir = stem
        if ada_bayang:
            peta, cb = sk08.bayang(peta, kid, cat["condong_darjah"])
            sk07.tulis(folder, stem + "_bayang", peta, pal, dict(imej=str(folder / f"{stem}_peranan.png"), kad=kid, **cb),
                       a_)
            akhir = stem + "_bayang"
        r = subprocess.run([sys.executable, str(SINI / "SK06_finish.py"), str(folder / f"{akhir}_warna.png"), gaya,
                            str(keluar / stem), "--sizes", pil.get("sizes", "18x24"),
                            "--palet", str(folder / f"{akhir}_palet.json"), "--kad", kid], capture_output=True, text=True)
        info = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 else None
        print(stem, "| SK07 " + ("amaran: " + "; ".join(cat["amaran"]) if cat["amaran"] else "lulus"),
              f"| SK08 bayang {cb['kongsi_bayang_pct']}%" if ada_bayang else "",
              f"| SK06 lapisan {info['layers']} {info['fills']}" if info else f"| SK06 GAGAL: {r.stderr[-300:]}")
