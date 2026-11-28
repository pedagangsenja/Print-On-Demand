"""SK12 Semakan ejaan automatik (Standard Lettering v1.2, langkah 5 QC A). Versi 1.0, 28 Nov 2026.

Tugas: baca teks pada imej jana dengan OCR (RapidOCR) dan banding dengan ayat yang dijangka (kad.AYAT).
Hasil setiap imej, SATU daripada tiga:
  "lulus auto"  = setiap perkataan dijangka dibaca tepat, dan tiada perkataan tambahan;
  "tanda"       = OCR membaca perkataan TAMBAHAN, perkataan BERULANG, atau dua perkataan BERCANTUM;
  "semak mata"  = selebihnya (OCR tidak dapat membaca semua perkataan, biasa pada tulisan skrip; atau baris berbilang
                  perkataan tidak dibaca dalam satu kotak).
OCR TIDAK pernah menggagalkan imej; ia hanya menyusun kerja mata. Sama ada "lulus auto" boleh dipercayai tanpa mata
diukur oleh --uji pada imej yang sudah ada keputusan QC mata (qc/*.json); lihat banding/ejaan_ujian.json.
Had: huruf besar / kecil dan tanda baca tidak disemak (banding huruf dan angka sahaja, tanpa beza huruf besar).
     Tulisan skrip jarang dibaca betul. Cacat bentuk huruf (G3) tidak dikesan.

Guna: python3 SK12_ejaan.py --kad K24t <imej> [...]     -> satu baris JSON bagi setiap imej
      python3 SK12_ejaan.py --uji                       -> ujian pada semua imej yang ada QC mata
"""
import glob
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

VERSI = "SK12 v1.2"
HERE = Path(__file__).resolve().parent
AKAR = HERE.parent
YAKIN = 0.6          # keyakinan minimum OCR untuk mengira satu perkataan sebagai "dibaca"
_enjin = None


def _ocr(rgb):
    global _enjin
    if _enjin is None:
        from rapidocr_onnxruntime import RapidOCR
        _enjin = RapidOCR()
    r, _ = _enjin(rgb)
    return [(x[1], float(x[2])) for x in (r or [])]


def _norma(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


CACHE = AKAR / "out" / "ocr"


def baca(path):
    """Dua laluan (imej asal dan warna disongsang). Pulang senarai laluan; setiap laluan = senarai (teks kotak, yakin)."""
    import hashlib
    CACHE.mkdir(parents=True, exist_ok=True)
    cf = CACHE / (hashlib.sha1(Path(path).read_bytes()).hexdigest()[:16] + ".json")
    if cf.exists():
        return json.loads(cf.read_text())
    rgb = np.array(Image.open(path).convert("RGB"))
    laluan = [_ocr(im) for im in (rgb, 255 - rgb)]
    cf.write_text(json.dumps(laluan, ensure_ascii=False))
    return laluan


def semak(path, ayat, baris=None):
    """baris = teks setiap baris Spesifikasi Teks (pilihan): baris berbilang perkataan mesti dibaca dalam SATU kotak."""
    jangka = [_norma(w) for w in ayat.split() if _norma(w)]
    cj = Counter(jangka)
    laluan = baca(path)
    # laluan terbaik = yang membaca paling banyak perkataan dijangka dengan yakin
    def token(l):
        return [(_norma(w), y) for teks, y in l for w in teks.split() if _norma(w)]
    terbaik = max(laluan, key=lambda l: len({w for w, y in token(l) if y >= YAKIN and w in cj}))
    tok = token(terbaik)
    yakin = Counter(w for w, y in tok if y >= YAKIN)
    semua = {}
    for l in laluan:
        for w, y in token(l):
            semua[w] = max(semua.get(w, 0.0), y)
    hilang = [w for w in cj if yakin[w] == 0]
    berulang = [w for w in cj if yakin[w] > cj[w]]
    cantum = {"".join(jangka[i:j]) for i in range(len(jangka)) for j in range(i + 2, len(jangka) + 1)}
    bercantum = [w for w in yakin if w in cantum and w not in cj]
    gabung = "".join(jangka)
    # v1.2: bacaan yang HAMPIR sama dengan perkataan dijangka (cth. 'woids' bagi 'words') ialah salah baca OCR, bukan
    # teks tambahan: 52 daripada 56 amaran palsu dalam ujian pertama datang daripada ini.
    import difflib
    mirip = lambda w: max(difflib.SequenceMatcher(None, w, j).ratio() for j in cj) >= 0.6
    tambahan = [w for w in yakin if w not in cj and len(w) >= 3 and w not in gabung and not mirip(w)]
    pecah = []
    for b in baris or []:
        kb = [_norma(w) for w in b.split() if _norma(w)]
        if len(kb) >= 2 and not any(all(k in _norma(teks) for k in kb) for teks, y in terbaik):
            pecah.append(b)
    if tambahan or berulang or bercantum:
        hasil = "tanda"
    elif hilang or pecah:
        hasil = "semak mata"
    else:
        hasil = "lulus auto"
    return dict(versi=VERSI, imej=str(path), hasil=hasil, dijangka=jangka, dibaca={w: round(y, 2) for w, y in semua.items()},
                hilang=hilang, tambahan=tambahan, berulang=berulang, bercantum=bercantum, baris_pecah=pecah)


def _qc_mata():
    """(batch, model, kunci) -> (lulus mata, catatan) daripada qc/*.json berformat batch > model > imej."""
    keluar = {}
    for f in sorted(glob.glob(str(AKAR / "qc/*.json"))):
        try:
            d = json.loads(Path(f).read_text())
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        for b, v in d.items():
            if not isinstance(v, dict):
                continue
            for m, imgs in v.items():
                if not isinstance(imgs, dict):
                    continue
                for k, r in imgs.items():
                    if isinstance(r, list) and len(r) >= 2 and isinstance(r[0], bool):
                        keluar[(b, m, k)] = (r[0], r[1])
    return keluar


def uji():
    sys.path.insert(0, str(AKAR))
    import kad
    baris, kira = [], Counter()
    for (b, m, k), (ok, cat) in sorted(_qc_mata().items()):
        mm = re.fullmatch(r"(K\d+)(\w)_s(\d+)", k)
        f = AKAR / "raw" / b / m / (k + ".png")
        if not mm or mm.group(2) not in kad.AYAT or not f.exists():
            kira["dilangkau (tiada fail atau kunci lain)"] += 1
            continue
        r = semak(f, kad.AYAT[mm.group(2)]["ayat"], [t for t, _ in kad.AYAT[mm.group(2)]["baris"]])
        skrip = any(w in str(kad.BLOK.get(mm.group(1), {}).get("huruf", "")).lower() for w in ("script",))
        c = cat.lower()
        jenis = ("gaya" if "ciri teras" in c else
                 "perkataan" if any(w in c for w in ("eja", "rosak", "berulang", "tertinggal", "hilang", "bercantum", "tiada jarak", "huruf kecil", "huruf besar", "jadi '")) else
                 "tanda / garis" if any(w in c for w in ("titik", "tanda", "koma", "garis", "bintik", "petikan", "noktah", "bingkai", "label tambahan", "teks rawak")) else
                 "baris" if "baris" in c else "lain")
        baris.append(dict(batch=b, model=m, imej=k, kad=mm.group(1), ada_skrip=skrip, mata_lulus=ok, catatan_mata=cat,
                          jenis_cacat=None if ok else jenis, auto=r["hasil"], hilang=r["hilang"], tambahan=r["tambahan"],
                          berulang=r["berulang"], bercantum=r["bercantum"], baris_pecah=r["baris_pecah"]))
    def jadual(rows):
        t = Counter((r["auto"], r["mata_lulus"]) for r in rows)
        n = len(rows)
        la, lg = t[("lulus auto", True)], t[("lulus auto", False)]
        gagal = sum(1 for r in rows if not r["mata_lulus"])
        return dict(imej=n, gagal_mata=gagal,
                    lulus_auto=la + lg, lulus_auto_betul=la, lulus_auto_tetapi_mata_gagal=lg,
                    tanda=t[("tanda", True)] + t[("tanda", False)], tanda_dan_mata_gagal=t[("tanda", False)],
                    semak_mata=t[("semak mata", True)] + t[("semak mata", False)],
                    kerja_mata_dijimat_pct=round((la + lg) / n * 100, 1) if n else None,
                    ketepatan_lulus_auto_pct=round(la / (la + lg) * 100, 1) if la + lg else None,
                    gagal_mata_yang_terlepas_pct=round(lg / gagal * 100, 1) if gagal else None)
    hasil = dict(versi=VERSI, tarikh="2026-11-28", yakin=YAKIN,
                 nota=("Ujian pada imej raw/ yang ada keputusan QC mata Claude (ok = G1 ejaan + G2 tiada teks rawak; sesetengah "
                       "batch juga G3). 'lulus auto tetapi mata gagal' = kes yang akan terlepas jika lulus auto dipercayai."),
                 dilangkau=dict(kira), semua=jadual(baris),
                 tanpa_skrip=jadual([r for r in baris if not r["ada_skrip"]]),
                 ada_skrip=jadual([r for r in baris if r["ada_skrip"]]),
                 ikut_jenis_cacat={j: dict(gagal_mata=sum(1 for r in baris if r["jenis_cacat"] == j),
                                           terlepas=sum(1 for r in baris if r["jenis_cacat"] == j and r["auto"] == "lulus auto"))
                                   for j in ("perkataan", "tanda / garis", "baris", "gaya", "lain")},
                 terlepas=[r for r in baris if r["auto"] == "lulus auto" and not r["mata_lulus"]])
    (AKAR / "banding").mkdir(exist_ok=True)
    (AKAR / "banding" / "ejaan_ujian.json").write_text(json.dumps(hasil, ensure_ascii=False, indent=1) + "\n")
    for k in ("semua", "tanpa_skrip", "ada_skrip", "ikut_jenis_cacat"):
        print(k, json.dumps(hasil[k], ensure_ascii=False))
    for r in hasil["terlepas"][:25]:
        print("TERLEPAS", r["batch"], r["model"], r["imej"], "|", r["catatan_mata"][:110])


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--uji" in a:
        uji()
    elif "--kad" in a:
        sys.path.insert(0, str(AKAR))
        import kad
        kod = a[a.index("--kad") + 1]
        for f in [x for i, x in enumerate(a) if not x.startswith("--") and a[i - 1] != "--kad"]:
            print(json.dumps(semak(f, kad.AYAT[kod[-1]]["ayat"], [t for t, _ in kad.AYAT[kod[-1]]["baris"]]), ensure_ascii=False))
    else:
        sys.exit(__doc__)
