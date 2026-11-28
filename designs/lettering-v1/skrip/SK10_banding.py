"""SK10 Banding (Standard Lettering v1.2, langkah 5: QC bahagian B). Versi 1.1, 28 Nov 2026.
v1.1: dua profil. "baris lurus" pada kedua-dua rekod -> ciri baris dibanding (seperti v1.0). Jika salah satu
      "lettering bertaut" -> ciri baris TIDAK dibanding (pecahan baris tidak boleh dipercayai); yang dibanding
      ialah kumpulan 'seluruh' (indeks tebal, kontras strok, strok nipis, condong huruf, bersambung, gelung,
      tepi kasar, bintik) + bentuk dan kepadatan blok. Indeks tebal dan gelung perlukan ayat: --teks-jana.

Tugas: banding rekod decode IMEJ JANA dengan rekod decode GAMBAR UPLOAD (kedua-duanya daripada SK09), medan demi
       medan. Hasil: skor persamaan gaya (0-100), senarai medan sama / beza, dan SATU ubahan seterusnya (beza
       terbesar yang bukan kerja skrip 5b). Tujuan: jana seterusnya makin hampir dengan gambar upload.
Banding GAYA sahaja, bukan ayat: ayat jana lain daripada ayat rujukan, jadi baris tidak dibanding satu lawan satu.
       Yang dibanding ialah ciri blok, ciri baris utama, ciri baris kecil, elemen dan tekstur.
Mod: hp (lalai) = hitam putih v1.2, warna TIDAK dibanding; warna = tambah bilangan dakwat dan beza warna
     (untuk workflow Warna).
Had: 'had' setiap medan ialah cadangan Claude 28 Nov 2026, BELUM ditentukur daripada ujian (bukti lemah).
     Skor ini menanda dan menyusun; ia tidak meluluskan imej. Pintu wajib (ejaan, teks rawak, cacat) kekal QC
     bahagian A.

Guna: python3 SK10_banding.py <rujukan.json> <jana.json> [...] [--mod hp|warna] [--keluar fail.json]
      biasa:  python3 SK10_banding.py decode/<upload>.json <imej jana.png> [...] --kad K24t
      atau dengan gambar terus:  python3 SK10_banding.py --gambar <upload> <imej jana> [...]
                                 [--teks-rujukan "ayat pada upload"] [--teks-jana "ayat pada imej jana"]
"""
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

VERSI = "SK10 v1.2"

# medan: (kumpulan, berat, had, jenis, tindakan jika beza)
#   jenis: 'mutlak' = beza nilai; 'nisbah' = beza peratus; 'kategori' = sama / tidak
#   had = beza yang masih dikira SAMA; skor turun lurus ke 0 pada 3 x had
MEDAN = [
    ("condong blok (darjah)",      "susunan", 2, 1.5,  "mutlak",   "skrip 5b (SK01)"),
    ("ruang tepi paling sempit (%)", "susunan", 0, 2.0, "mutlak",  "skrip 5b (SK02)"),   # berat 0: kad menetapkan
    ("nisbah blok (lebar / tinggi)", "susunan", 1, 0.15, "nisbah", "prompt: bentuk susunan"),
    ("penjajaran",                 "susunan", 3, None, "kategori", "prompt: bentuk susunan"),
    ("serakan penjajaran (%)",     "susunan", 1, 3.0,  "mutlak",   "prompt: bentuk susunan"),
    ("sela antara baris (%)",      "susunan", 2, 1.5,  "mutlak",   "prompt: jarak dan hubungan baris"),
    ("isian blok (%)",             "susunan", 1, 6.0,  "mutlak",   "prompt: hierarki saiz"),
    ("utama: kelas huruf",         "huruf",   4, None, "kategori", "prompt: bentuk huruf ikut peranan"),
    ("utama: tebal strok (%)",     "huruf",   4, 3.0,  "mutlak",   "prompt: bentuk huruf ikut peranan"),
    ("utama: lebar huruf (nisbah)", "huruf",  2, 0.08, "mutlak",   "prompt: bentuk huruf ikut peranan"),
    ("utama: condong huruf (darjah)", "huruf", 2, 5.0, "mutlak",   "prompt: garis dasar dan condong"),
    ("utama: huruf besar / campur", "huruf",  3, None, "kategori", "prompt: huruf besar / kecil ikut peranan"),
    ("utama: kontras strok",       "huruf",   1, 0.5,  "mutlak",   "prompt: butiran garisan"),
    ("utama: tepi kasar (%)",      "huruf",   2, 6.0,  "mutlak",   "prompt: tekstur dan kelas kemasan"),
    ("baris kecil: ada",           "huruf",   2, None, "kategori", "prompt: hierarki saiz"),
    ("baris kecil: kelas huruf",   "huruf",   2, None, "kategori", "prompt: bentuk huruf ikut peranan"),
    ("hierarki (tertinggi / terendah)", "huruf", 1, 0.35, "nisbah", "prompt: hierarki saiz"),
    ("bekas (kotak / label)",      "elemen",  4, None, "kategori", "prompt: hiasan (bekas pejal dahulu, perkataan kemudian)"),
    ("garis / sapuan: ada",        "elemen",  2, None, "kategori", "prompt: hiasan"),
    ("hiasan lain: ada",           "elemen",  1, None, "kategori", "prompt: hiasan"),
    ("tekstur huruf",              "tekstur", 2, None, "kategori", "prompt: tekstur dan kelas kemasan"),
    ("tekstur latar",              "tekstur", 1, None, "kategori", "prompt: tekstur dan kelas kemasan"),
]
# Berat (larian K24t, 28 Nov 2026): indeks tebal 2 (ditarik oleh ekor panjang, kurang dipercayai); tepi kasar 3
# (beza paling jelas di mata: berus kering lawan strok licin). Pertimbangan Claude, belum ditentukur.
# medan yang bergantung pada pecahan baris: hanya untuk "baris lurus"
PERLU_BARIS = {"penjajaran", "serakan penjajaran (%)", "sela antara baris (%)", "hierarki (tertinggi / terendah)"}
MEDAN_SELURUH = [
    ("bentuk blok",                "susunan", 2, None, "kategori", "prompt: bentuk susunan"),
    ("kepadatan blok (%)",         "susunan", 2, 8.0,  "mutlak",   "prompt: jarak dan hubungan baris"),
    ("seluruh: indeks tebal",      "huruf",   2, 0.12, "nisbah",   "prompt: bentuk huruf ikut peranan"),
    ("seluruh: kontras strok",     "huruf",   2, 0.6,  "mutlak",   "prompt: butiran garisan"),
    ("seluruh: strok nipis (%)",   "huruf",   2, 8.0,  "mutlak",   "prompt: hiasan (ekor dan sapuan nipis)"),
    ("seluruh: condong huruf (darjah)", "huruf", 3, 6.0, "mutlak", "prompt: garis dasar dan condong"),
    ("seluruh: bersambung (kongsi bentuk terbesar)", "huruf", 3, 0.2, "mutlak", "prompt: jarak dan hubungan baris"),
    ("seluruh: gelung setiap huruf", "huruf", 2, 0.25, "mutlak",   "prompt: bentuk huruf ikut peranan"),
    ("seluruh: tepi kasar (%)",    "huruf",   3, 8.0,  "mutlak",   "prompt: bentuk huruf (tepi strok licin atau kasar)"),
    ("bintik / percikan",          "elemen",  1, None, "kategori", "prompt: hiasan"),
]
# ciri setiap kata ikut peranan (rekod yang ada kumpulan 'kata': kotak mata pada upload, baris = spesifikasi pada jana)
MEDAN_KATA = [
    ("kata utama: indeks tebal",          "huruf", 3, 0.12, "nisbah", "prompt: bentuk huruf ikut peranan (utama)"),
    ("kata utama: condong huruf (darjah)", "huruf", 3, 6.0, "mutlak", "prompt: bentuk huruf ikut peranan (utama)"),
    ("kata utama: lebar setiap huruf",    "huruf", 2, 0.25, "nisbah", "prompt: bentuk huruf ikut peranan (utama)"),
    ("kata sokongan: indeks tebal",       "huruf", 2, 0.12, "nisbah", "prompt: bentuk huruf ikut peranan (sokongan)"),
    ("kata sokongan: condong huruf (darjah)", "huruf", 2, 6.0, "mutlak", "prompt: bentuk huruf ikut peranan (sokongan)"),
    ("kata sokongan / utama: nisbah tinggi", "huruf", 2, 0.2, "nisbah", "prompt: hierarki saiz"),
    ("kata penyambung / utama: nisbah tinggi", "huruf", 2, 0.25, "nisbah", "prompt: hierarki saiz"),
]
MEDAN_WARNA = [
    ("bilangan dakwat",            "warna",   3, 0.0,  "mutlak",   "warna C: bilangan dakwat"),
    ("warna latar (beza Delta E)", "warna",   2, 10.0, "mutlak",   "warna C: latar"),
    ("dakwat utama (beza Delta E)", "warna",  3, 12.0, "mutlak",   "warna C: dakwat ikut peranan"),
]


# Jadual asal (cadangan Claude, sebelum tentukur) disimpan untuk skrip/tentukur_sk10.py.
MEDAN_ASAL, MEDAN_SELURUH_ASAL, MEDAN_KATA_ASAL = list(MEDAN), list(MEDAN_SELURUH), list(MEDAN_KATA)
TENTUKUR = None


def _muat_tentukur():
    """Jika skrip/sk10_had.json ada (hasil tentukur_sk10.py), had dan berat setiap medan diambil daripadanya.
    SK10_ASAL=1 dalam persekitaran = guna jadual asal."""
    global MEDAN, MEDAN_SELURUH, MEDAN_KATA, TENTUKUR
    import os
    f = Path(__file__).resolve().parent / "sk10_had.json"
    if os.environ.get("SK10_ASAL") or not f.exists():
        return
    d = json.loads(f.read_text())
    TENTUKUR = d.get("sumber")
    def tukar(jadual):
        keluar = []
        for nama, kump, berat, had, jenis, tindakan in jadual:
            m = d["medan"].get(nama)
            if m and berat != 0:
                berat, had = m["berat"], (m["had"] if m["had"] is not None else had)
            keluar.append((nama, kump, berat, had, jenis, tindakan))
        return keluar
    MEDAN, MEDAN_SELURUH, MEDAN_KATA = tukar(MEDAN_ASAL), tukar(MEDAN_SELURUH_ASAL), tukar(MEDAN_KATA_ASAL)


_muat_tentukur()


def _purata(baris, kunci):
    v = [(r[kunci], r["tinggi_pct"]) for r in baris if r.get(kunci) is not None]
    return round(float(np.average([a for a, _ in v], weights=[b for _, b in v])), 2) if v else None


def _undi(baris, kunci):
    c = Counter()
    for r in baris:
        if r.get(kunci):
            c[r[kunci]] += r["tinggi_pct"]
    return c.most_common(1)[0][0] if c else None


def _lab(hx):
    import cv2
    rgb = np.float32([[[int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]]])
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)[0, 0]


def tanda(r):
    """Tandatangan gaya satu rekod decode: nilai yang dibanding, bebas daripada ayat."""
    s, b = r["susunan"], r["baris"]
    utama = [x for x in b if x["peranan_saiz"] == "utama"]
    kecil = [x for x in b if x["peranan_saiz"] == "kecil"]
    jenis = Counter(e["jenis"] for e in r["elemen"])
    t = {
        "condong blok (darjah)": s["condong_darjah"],
        "ruang tepi paling sempit (%)": s["tepi_min_pct"],
        "nisbah blok (lebar / tinggi)": s["nisbah_blok"],
        "penjajaran": s["penjajaran"],
        "sela antara baris (%)": round(float(np.median(s["sela_baris_pct"])), 1) if s["sela_baris_pct"] else None,
        "serakan penjajaran (%)": s.get("serakan_penjajaran_pct"),
        "isian blok (%)": s["isian_blok_pct"],
        "utama: kelas huruf": _undi(utama, "kelas_anggaran"),
        "utama: tebal strok (%)": _purata(utama, "tebal_strok_pct"),
        "utama: lebar huruf (nisbah)": _purata(utama, "nisbah_lebar_huruf"),
        "utama: condong huruf (darjah)": _purata(utama, "condong_huruf_darjah"),
        "utama: huruf besar / campur": _undi(utama, "huruf"),
        "utama: kontras strok": _purata(utama, "kontras_strok"),
        "utama: tepi kasar (%)": _purata(utama, "tepi_kasar_pct"),
        "baris kecil: ada": "ada" if kecil else "tiada",
        "baris kecil: kelas huruf": _undi(kecil, "kelas_anggaran"),
        "hierarki (tertinggi / terendah)": s["hierarki_nisbah"],
        "bekas (kotak / label)": ("pejal" if any(x.get("bekas") == "pejal" for x in b) else
                                  "garis luar" if any(x.get("bekas") == "garis luar" for x in b) else "tiada"),
        "garis / sapuan: ada": "ada" if jenis["garis"] + jenis["garis / sapuan"] else "tiada",
        "hiasan lain: ada": "ada" if jenis["hiasan warna lain"] else "tiada",
        "tekstur huruf": r["tekstur"]["dakwat"],
        "tekstur latar": r["tekstur"]["latar"],
        "bilangan dakwat": r["warna"]["bil_dakwat"],
        "_jenis": s.get("jenis_susunan", "baris lurus"),
        "_latar": r["warna"]["latar"],
        "_dakwat": r["warna"]["dakwat"][0]["hex"] if r["warna"]["dakwat"] else None,
    }
    g = r.get("seluruh") or {}
    t.update({
        "bentuk blok": g.get("bentuk_blok"),
        "kepadatan blok (%)": g.get("kepadatan_blok_pct"),
        "seluruh: indeks tebal": g.get("indeks_tebal"),
        "seluruh: kontras strok": g.get("kontras_strok"),
        "seluruh: strok nipis (%)": g.get("strok_nipis_pct"),
        "seluruh: condong huruf (darjah)": g.get("condong_huruf_darjah"),
        "seluruh: bersambung (kongsi bentuk terbesar)": g.get("kongsi_komponen_terbesar"),
        "seluruh: gelung setiap huruf": g.get("gelung_setiap_huruf"),
        "seluruh: tepi kasar (%)": g.get("tepi_kasar_pct"),
        "bintik / percikan": None if not g else ("banyak" if g["komponen_kecil"] >= 10 else "sedikit / tiada"),
    })
    kt = [k for k in r.get("kata") or [] if k.get("tinggi_px")]
    def pur(per, kunci):
        v = [(k[kunci], k["tinggi_px"]) for k in kt if k.get("peranan") == per and k.get(kunci) is not None]
        return round(float(np.average([x for x, _ in v], weights=[y for _, y in v])), 3) if v else None
    tu, ts, tp = pur("utama", "tinggi_px"), pur("sokongan", "tinggi_px"), pur("penyambung", "tinggi_px")
    t.update({
        "kata utama: indeks tebal": pur("utama", "indeks_tebal"),
        "kata utama: condong huruf (darjah)": pur("utama", "condong_huruf_darjah"),
        "kata utama: lebar setiap huruf": pur("utama", "lebar_setiap_huruf"),
        "kata sokongan: indeks tebal": pur("sokongan", "indeks_tebal"),
        "kata sokongan: condong huruf (darjah)": pur("sokongan", "condong_huruf_darjah"),
        "kata sokongan / utama: nisbah tinggi": round(ts / tu, 2) if tu and ts else None,
        "kata penyambung / utama: nisbah tinggi": round(tp / tu, 2) if tu and tp else None,
    })
    return t


def banding(ruj, jana, mod="hp"):
    a, b = tanda(ruj), tanda(jana)
    bertaut = "lettering bertaut" in (a["_jenis"], b["_jenis"])
    if bertaut:
        medan = [m for m in MEDAN if not (m[0].startswith(("utama:", "baris kecil:")) or m[0] in PERLU_BARIS)]
        medan = medan + MEDAN_SELURUH
    else:
        medan = list(MEDAN)
    if ruj.get("kata") and jana.get("kata"):
        medan = medan + MEDAN_KATA
    if mod == "hp":
        # v1.2 hitam putih: tekstur ditambah oleh skrip kemudian (Cetak v1), jadi ditunjuk sebagai maklumat sahaja
        medan = [(n, k, 0 if n in ("tekstur huruf", "tekstur latar") else b, h, j, t) for n, k, b, h, j, t in medan]
    if mod == "warna":
        de = lambda x, y: None if not (x and y) else round(float(np.linalg.norm(_lab(x) - _lab(y))), 1)
        a["warna latar (beza Delta E)"], b["warna latar (beza Delta E)"] = 0.0, de(a["_latar"], b["_latar"])
        a["dakwat utama (beza Delta E)"], b["dakwat utama (beza Delta E)"] = 0.0, de(a["_dakwat"], b["_dakwat"])
    baris, jum, dapat = [], 0.0, 0.0
    for nama, kump, berat, had, jenis, tindakan in medan + (MEDAN_WARNA if mod == "warna" else []):
        x, y = a.get(nama), b.get(nama)
        if x is None or y is None:
            # medan tiada pada satu pihak (cth. tiada baris kecil): tidak dikira, tetapi ditunjuk
            baris.append(dict(medan=nama, kumpulan=kump, rujukan=x, jana=y, hasil="tidak dibanding", skor=None,
                              berat=berat))
            continue
        if jenis == "kategori":
            sk, beza = (1.0 if x == y else 0.0), None
        else:
            beza = abs(y - x) / max(1e-6, abs(x)) if jenis == "nisbah" else abs(y - x)
            sk = 1.0 if beza <= had else max(0.0, 1 - (beza - had) / (2 * had)) if had else 0.0
            beza = round(float(beza), 2)
        if berat == 0:
            baris.append(dict(medan=nama, kumpulan=kump, rujukan=x, jana=y, beza=beza, had=had,
                              hasil="maklumat (tidak dikira; kad menetapkan)", skor=None, berat=0))
            continue
        jum += berat
        dapat += berat * sk
        baris.append(dict(medan=nama, kumpulan=kump, rujukan=x, jana=y, beza=beza, had=had,
                          hasil="sama" if sk >= 0.999 else "hampir" if sk >= 0.5 else "beza", skor=round(sk, 2),
                          berat=berat, rugi=round(berat * (1 - sk), 2), tindakan=None if sk >= 0.999 else tindakan))
    beza = sorted([r for r in baris if r.get("rugi")], key=lambda r: -r["rugi"])
    prompt = [r for r in beza if not r["tindakan"].startswith("skrip")]
    return dict(
        versi=VERSI, tentukur=TENTUKUR or "tiada (jadual asal)", mod=mod, profil="lettering bertaut (ciri seluruh blok)" if bertaut else "baris lurus (ciri baris)",
        rujukan=ruj["fail"], jana=jana["fail"],
        skor=round(dapat / jum * 100, 1) if jum else None,
        sama=sum(r["hasil"] == "sama" for r in baris), hampir=sum(r["hasil"] == "hampir" for r in baris),
        beza=sum(r["hasil"] == "beza" for r in baris),
        beza_terbesar=[dict(medan=r["medan"], rujukan=r["rujukan"], jana=r["jana"], tindakan=r["tindakan"])
                       for r in beza[:3]],
        ubahan_seterusnya=(dict(medan=prompt[0]["medan"], dari=prompt[0]["jana"], ke=prompt[0]["rujukan"],
                                di=prompt[0]["tindakan"]) if prompt else None),
        skrip_5b=[r["medan"] for r in beza if r["tindakan"].startswith("skrip")],
        medan=baris, nota="had belum ditentukur (bukti lemah); skor menanda, tidak meluluskan")


if __name__ == "__main__":
    a = sys.argv[1:]
    mod = a[a.index("--mod") + 1] if "--mod" in a else "hp"
    keluar = a[a.index("--keluar") + 1] if "--keluar" in a else None
    langkau = {i + 1 for i, x in enumerate(a) if x in ("--mod", "--keluar", "--teks-jana", "--teks-rujukan", "--kad")}
    tj = a[a.index("--teks-jana") + 1] if "--teks-jana" in a else None
    tr = a[a.index("--teks-rujukan") + 1] if "--teks-rujukan" in a else None
    fail = [x for i, x in enumerate(a) if not x.startswith("--") and i not in langkau]
    if len(fail) < 2:
        sys.exit(__doc__)
    # setiap hujah: rekod .json (dibaca terus) atau gambar (di-decode di sini). Imej jana dengan --kad K24t:
    # ayat dan peranan baris daripada kad.AYAT, supaya kumpulan 'kata' diisi sendiri.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from SK09_decode import decode, spec_kad
    spec = None
    if "--kad" in a:
        tj, spec = spec_kad(a[a.index("--kad") + 1])
    rekod = [json.loads(Path(f).read_text()) if f.endswith(".json")
             else decode(f, None, tr if i == 0 else tj, None, None if i == 0 else spec) for i, f in enumerate(fail)]
    hasil = [banding(rekod[0], r, mod) for r in rekod[1:]]
    if keluar:
        Path(keluar).write_text(json.dumps(hasil, ensure_ascii=False, indent=1) + "\n")
    for h in hasil:
        print(json.dumps({k: h[k] for k in ("jana", "profil", "skor", "sama", "hampir", "beza", "ubahan_seterusnya",
                                            "skrip_5b")}, ensure_ascii=False))
