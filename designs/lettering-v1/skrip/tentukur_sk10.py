"""Tentukur SK10 (QC bahagian B) daripada imej sedia ada, tanpa jana baharu. Versi 1.0, 28 Nov 2026.

Soalan: adakah skor SK10 benar-benar mengenal gaya? Ujian yang boleh diukur: setiap imej jana ada SATU gambar rujukan
yang betul (rujukan kadnya). Skor yang baik memberi markah LEBIH TINGGI kepada rujukan sendiri daripada kepada rujukan
kad lain. Jadi:
  1. decode semua gambar rujukan yang ada failnya (upload/, rujukan/) dan semua imej betul/<batch>/<model>/K..png;
  2. pasangan PADAN = (imej, rujukan kadnya); pasangan TAK PADAN = (imej, rujukan kad lain);
  3. bagi setiap medan: had baharu = persentil ke-75 beza pasangan padan (sebaran biasa jana yang betul gayanya);
     kuasa beza = AUC (kebarangkalian beza pasangan padan lebih kecil daripada pasangan tak padan; 0.5 = tidak berguna);
     berat baharu = 0 jika AUC < 0.55, jika tidak 1-4 ikut AUC;
  4. ukur ketepatan "rujukan sendiri mendapat skor tertinggi" (top-1) dan kedudukan purata, dengan had / berat lama dan
     baharu. Had / berat baharu dikira pada separuh kad dan diuji pada separuh lagi (dua lipatan), supaya angka ujian
     bukan daripada kad yang sama.
Had kaedah: "padan" bermaksud kad yang sama, bukan "nampak serupa pada mata"; imej yang gagal gaya tetap dikira padan.
Jadi ini menentukur keupayaan MEMBEZAKAN gaya, bukan menggantikan mata pengguna. Bukti: sederhana (ratusan imej,
tetapi satu ukuran sahaja).

Keputusan larian 28 Nov 2026 (384 imej, 26 rujukan, 30 kad): tetapan baharu TIDAK lebih baik pada kad yang tidak
dilihat (top-1 19.3% lawan 24.0% tetapan asal; kedudukan purata 8.45 lawan 7.23 daripada 26). Jadi jadual asal SK10
dikekalkan dan skrip/sk10_had.json tidak ditulis. Hasil yang berguna ialah AUC setiap medan dan angka asas itu sendiri.

Guna: python3 skrip/tentukur_sk10.py            -> banding/tentukur_sk10.json (termasuk kad pendua)
      python3 skrip/tentukur_sk10.py --tulis    -> juga tulis skrip/sk10_had.json, HANYA jika tetapan baharu menang ujian
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
AKAR = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(AKAR))
import kad  # noqa: E402
import SK09_decode as sk9  # noqa: E402
import SK10_banding as sk10  # noqa: E402

CACHE = AKAR / "out" / "tentukur"


def _ruj_kad():
    """kad -> (nama rujukan, fail) bagi kad yang rujukannya ada dalam repo."""
    ada = {}
    for f in sorted(glob.glob(str(AKAR / "upload/*")) + glob.glob(str(AKAR / "rujukan/*"))):
        nama = Path(f).stem
        if re.fullmatch(r"IMG_\d+", nama):
            ada.setdefault(nama, f)
    keluar = {}
    for k, v in kad.KAD.items():
        m = re.findall(r"IMG_\d+", str(v.get("ref", "")))
        if m and m[0] in ada and str(v.get("ref", "")).startswith("IMG_"):
            keluar[k] = (m[0], ada[m[0]])
    return keluar


def _teks_ruj(nama, kid):
    f = AKAR / "decode" / "mata" / (nama + ".json")
    if f.exists():
        m = json.loads(f.read_text())
        return (" ".join(m["teks_rujukan"]) if m.get("teks_rujukan") else None), m.get("kata")
    for j in kad.KAD[kid].get("jangan_salin", []):
        if j.startswith("ayat "):
            return j[5:], None
    return None, None


def _kerja(a):
    jenis, kunci, fail, teks, kata, spec = a
    st = os.stat(fail)                                    # saiz + masa ubah dalam nama: imej yang berubah diukur semula
    cf = CACHE / ("%s_%s_%d_%d_%s.json" % (jenis, re.sub(r"[^A-Za-z0-9_.-]", "_", kunci), st.st_size, int(st.st_mtime),
                                             sk9.VERSI.replace(" ", "")))
    if cf.exists():
        return kunci, json.loads(cf.read_text())
    try:
        r = sk9.decode(fail, None, teks, kata, spec)
    except Exception as e:  # imej rosak / kosong: direkod, tidak menghentikan larian
        r = dict(ralat=str(e))
    cf.write_text(json.dumps(r, ensure_ascii=False))
    return kunci, r


def muat():
    CACHE.mkdir(parents=True, exist_ok=True)
    rk = _ruj_kad()
    tugas, kad_imej = [], {}
    for nama, fail in sorted({v for v in rk.values()}):
        kid = next(k for k, v in rk.items() if v[0] == nama)
        teks, kata = _teks_ruj(nama, kid)
        tugas.append(("ruj", nama, fail, teks, kata, None))
    for f in sorted(glob.glob(str(AKAR / "betul/*/*/*.png"))):
        m = re.fullmatch(r"(K\d+)(\w)_s(\d+)\.png", Path(f).name)
        if not m or m.group(1) not in rk or m.group(2) not in kad.AYAT:
            continue
        a = kad.AYAT[m.group(2)]
        kunci = str(Path(f).relative_to(AKAR / "betul"))
        kad_imej[kunci] = m.group(1)
        tugas.append(("jana", kunci, f, a["ayat"], None, [(t, r) for t, r in a["baris"]]))
    with Pool(4) as p:
        hasil = dict(p.map(_kerja, tugas, chunksize=4))
    ruj = {n: hasil[n] for n, _ in {v for v in rk.values()} if "susunan" in hasil.get(n, {})}
    jana = {k: hasil[k] for k in kad_imej if "susunan" in hasil.get(k, {})}
    return rk, ruj, jana, kad_imej


def medan_pasangan(a_rek, b_rek):
    """Senarai medan yang SK10 akan banding untuk pasangan ini (ikut profil), dengan nilai kedua-dua pihak."""
    a, b = sk10.tanda(a_rek), sk10.tanda(b_rek)
    bertaut = "lettering bertaut" in (a["_jenis"], b["_jenis"])
    if bertaut:
        medan = [m for m in sk10.MEDAN if not (m[0].startswith(("utama:", "baris kecil:")) or m[0] in sk10.PERLU_BARIS)]
        medan = medan + sk10.MEDAN_SELURUH
    else:
        medan = list(sk10.MEDAN)
    if a_rek.get("kata") and b_rek.get("kata"):
        medan = medan + sk10.MEDAN_KATA
    keluar = {}
    for nama, _k, _b, _h, jenis, _t in medan:
        x, y = a.get(nama), b.get(nama)
        if x is None or y is None:
            continue
        if jenis == "kategori":
            keluar[nama] = ("k", 0.0 if x == y else 1.0)
        else:
            keluar[nama] = ("n", abs(y - x) / max(1e-6, abs(x)) if jenis == "nisbah" else abs(y - x))
    return keluar


def skor(beza, tetapan):
    """Skor 0-100 daripada beza setiap medan dan tetapan {medan: (berat, had)}."""
    jum = dapat = 0.0
    for nama, (jenis, d) in beza.items():
        berat, had = tetapan.get(nama, (0, None))
        if not berat:
            continue
        if jenis == "k":
            s = 1.0 - d
        else:
            s = 1.0 if d <= had else max(0.0, 1 - (d - had) / (2 * had)) if had else 0.0
        jum += berat
        dapat += berat * s
    return dapat / jum * 100 if jum else None


def tetapan_lama():
    t = {}
    for nama, _k, berat, had, _j, _t in sk10.MEDAN_ASAL + sk10.MEDAN_SELURUH_ASAL + sk10.MEDAN_KATA_ASAL:
        t[nama] = (0 if nama in ("tekstur huruf", "tekstur latar") else berat, had)
    return t


def auc(padan, tak):
    """Kebarangkalian beza pasangan padan < beza pasangan tak padan (seri = 0.5)."""
    if not len(padan) or not len(tak):
        return None
    p, t = np.sort(np.asarray(padan, float)), np.sort(np.asarray(tak, float))
    kurang = np.searchsorted(t, p, side="left")           # bil. tak padan yang lebih kecil daripada setiap padan
    sama = np.searchsorted(t, p, side="right") - kurang
    return float(((len(t) - kurang - sama) + 0.5 * sama).sum() / (len(p) * len(t)))


def tentukur(pasangan_padan, pasangan_tak):
    """{medan: (berat, had, auc, n)} daripada beza pasangan padan dan tak padan."""
    kumpul_p, kumpul_t, jenis = defaultdict(list), defaultdict(list), {}
    for b in pasangan_padan:
        for n, (j, d) in b.items():
            kumpul_p[n].append(d)
            jenis[n] = j
    for b in pasangan_tak:
        for n, (j, d) in b.items():
            kumpul_t[n].append(d)
    lama, keluar = tetapan_lama(), {}
    for n in kumpul_p:
        a = auc(kumpul_p[n], kumpul_t[n])
        if jenis[n] == "k":
            had = None
        else:
            had = float(np.percentile(kumpul_p[n], 75))
            had = max(had, 1e-3)
        berat = 0 if (a is None or a < 0.55) else 1 if a < 0.62 else 2 if a < 0.70 else 3 if a < 0.78 else 4
        if lama.get(n, (1, None))[0] == 0:                 # medan maklumat (ruang tepi, tekstur dalam mod hp) kekal 0
            berat = 0
        keluar[n] = (berat, None if had is None else round(had, 3), None if a is None else round(a, 3), len(kumpul_p[n]))
    return keluar


def nilai(jana, ruj, kad_imej, rk, tetapan, kad_uji=None):
    """Top-1 dan kedudukan purata rujukan sendiri di kalangan semua rujukan."""
    ruj_kad = {k: v[0] for k, v in rk.items()}
    betul = n = 0
    kedudukan, margin = [], []
    for kunci, rek in jana.items():
        kid = kad_imej[kunci]
        if kad_uji is not None and kid not in kad_uji:
            continue
        sendiri = ruj_kad[kid]
        if sendiri not in ruj:
            continue
        sk = {}
        for nama, rr in ruj.items():
            s = skor(BEZA[(kunci, nama)], tetapan)
            if s is not None:
                sk[nama] = s
        if sendiri not in sk or len(sk) < 2:
            continue
        susun = sorted(sk, key=lambda x: -sk[x])
        n += 1
        betul += susun[0] == sendiri
        kedudukan.append(susun.index(sendiri) + 1)
        margin.append(sk[sendiri] - np.mean([v for k2, v in sk.items() if k2 != sendiri]))
    return dict(n=n, top1_pct=round(betul / n * 100, 1) if n else None, kedudukan_purata=round(float(np.mean(kedudukan)), 2) if n else None,
                bil_rujukan=len(ruj), beza_skor_sendiri_lawan_lain=round(float(np.mean(margin)), 1) if n else None)


BEZA = {}

if __name__ == "__main__":
    rk, ruj, jana, kad_imej = muat()
    ruj_kad = {k: v[0] for k, v in rk.items()}
    for kunci, rek in jana.items():
        for nama, rr in ruj.items():
            BEZA[(kunci, nama)] = medan_pasangan(rr, rek)
    padan = lambda kads: [BEZA[(k, ruj_kad[kad_imej[k]])] for k in jana if kad_imej[k] in kads and ruj_kad[kad_imej[k]] in ruj]
    tak = lambda kads: [BEZA[(k, n)] for k in jana if kad_imej[k] in kads for n in ruj if n != ruj_kad[kad_imej[k]]]
    semua_kad = sorted({kad_imej[k] for k in jana}, key=lambda k: int(k[1:]))
    lama = tetapan_lama()
    # dua lipatan ikut kad (kad pendua rujukan sama diletak dalam lipatan yang sama)
    ruj_susun = sorted({ruj_kad[k] for k in semua_kad})
    lipat = [{k for k in semua_kad if ruj_susun.index(ruj_kad[k]) % 2 == i} for i in (0, 1)]
    uji = []
    for i in (0, 1):
        t = tentukur(padan(lipat[1 - i]), tak(lipat[1 - i]))
        tb = {n: (v[0], v[1]) for n, v in t.items()}
        uji.append(dict(lipatan=i, kad_uji=sorted(lipat[i]), lama=nilai(jana, ruj, kad_imej, rk, lama, lipat[i]),
                        baharu=nilai(jana, ruj, kad_imej, rk, tb, lipat[i])))
    def gabung(kunci):
        n = sum(u[kunci]["n"] for u in uji)
        return dict(n=n, top1_pct=round(sum(u[kunci]["top1_pct"] * u[kunci]["n"] for u in uji) / n, 1),
                    kedudukan_purata=round(sum(u[kunci]["kedudukan_purata"] * u[kunci]["n"] for u in uji) / n, 2))
    gl, gb = gabung("lama"), gabung("baharu")
    menang = gb["top1_pct"] > gl["top1_pct"] and gb["kedudukan_purata"] < gl["kedudukan_purata"]
    penuh = tentukur(padan(set(semua_kad)), tak(set(semua_kad)))
    tb = {n: (v[0], v[1]) for n, v in penuh.items()}
    hasil = dict(
        versi="tentukur_sk10 v1.0", tarikh="2026-11-28", bil_imej=len(jana), bil_rujukan=len(ruj), bil_kad=len(semua_kad),
        nota=("Padan = imej dengan rujukan kadnya; tak padan = imej dengan rujukan kad lain. Had baharu = persentil ke-75 "
              "beza pasangan padan; berat ikut AUC. Ujian dua lipatan ikut kad: tetapan dikira pada separuh kad, diuji pada "
              "separuh lagi. 'Padan' bukan bermaksud serupa pada mata."),
        ujian_dua_lipatan=uji,
        ujian_pada_kad_tidak_dilihat=dict(tetapan_asal=gl, tetapan_baharu=gb, rawak=dict(top1_pct=round(100 / len(ruj), 1),
                                                                                         kedudukan_purata=(len(ruj) + 1) / 2)),
        keputusan=("Tetapan baharu menang ujian: boleh dipakai (--tulis)" if menang else
                   "Tetapan baharu TIDAK menang pada kad yang tidak dilihat: jadual asal SK10 dikekalkan"),
        semua_data=dict(lama=nilai(jana, ruj, kad_imej, rk, lama), baharu=nilai(jana, ruj, kad_imej, rk, tb)),
        medan=[dict(medan=n, berat_lama=lama.get(n, (None, None))[0], had_lama=lama.get(n, (None, None))[1], berat_baharu=v[0],
                    had_baharu=v[1], auc=v[2], n_padan=v[3]) for n, v in sorted(penuh.items(), key=lambda x: -(x[1][2] or 0))])
    (AKAR / "banding").mkdir(exist_ok=True)
    (AKAR / "banding" / "tentukur_sk10.json").write_text(json.dumps(hasil, ensure_ascii=False, indent=1) + "\n")
    kump = defaultdict(list)
    for k in semua_kad:
        kump[ruj_kad[k]].append(k)
    hasil["kad_pendua"] = [dict(rujukan=nama, kad=k, imej=len([x for x in jana if kad_imej[x] == k]),
                                skor_purata=round(float(np.mean([skor(BEZA[(x, nama)], lama) for x in jana if kad_imej[x] == k])), 1))
                           for nama, ks in sorted(kump.items()) if len(ks) > 1 for k in ks]
    (AKAR / "banding" / "tentukur_sk10.json").write_text(json.dumps(hasil, ensure_ascii=False, indent=1) + "\n")
    if menang and "--tulis" in sys.argv:
        (HERE / "sk10_had.json").write_text(json.dumps(dict(
        sumber="skrip/tentukur_sk10.py v1.0, 28 Nov 2026: %d imej, %d rujukan, %d kad" % (len(jana), len(ruj), len(semua_kad)),
        medan={n: dict(berat=v[0], had=v[1], auc=v[2]) for n, v in sorted(penuh.items())}), ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(dict(imej=len(jana), rujukan=len(ruj), kad=len(semua_kad), dua_lipatan=uji, semua=hasil["semua_data"]), ensure_ascii=False))
    for m in hasil["medan"]:
        print("%-46s auc %-6s berat %s -> %s  had %s -> %s  n %d" % (m["medan"][:46], m["auc"], m["berat_lama"], m["berat_baharu"],
                                                                 m["had_lama"], m["had_baharu"], m["n_padan"]))
    print(hasil["keputusan"], "| asal", gl, "| baharu", gb)
    for r in hasil["kad_pendua"]:
        print("PENDUA", r)
