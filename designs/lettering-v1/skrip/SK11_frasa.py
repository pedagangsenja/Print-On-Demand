"""SK11 Frasa daripada decode (Standard Lettering v1.2, langkah 1c dan 5 QC B). Versi 1.0, 28 Nov 2026.

Masalah yang dibaiki (audit 28 Nov): angka decode hampir tidak sampai ke prompt. Frasa Kad Gaya ditulis dengan mata,
jadi boleh bercanggah dengan ukuran. Contoh K24: rekod decode menunjuk tepi strok licin (4%), tetapi frasa mata ialah
"brush script", dan 6 imej pertama bertepi kasar.

Skrip ini ialah SATU jadual tetap (JADUAL) yang menukar ukuran kepada "tong" dan setiap tong kepada SATU frasa prompt:
  ciri(rekod)      -> senarai ciri terukur: medan, nilai, tong (BM), frasa (Inggeris), teras atau tidak
  draf_kad(rekod)  -> draf isi Kad Gaya (bentuk kad.BLOK) daripada ciri + medan mata; setiap medan bertanda sumbernya
Dipakai dua kali, dengan jadual yang SAMA:
  1. langkah 1c: gambar upload -> draf kad (frasa daripada angka; mata hanya menambah yang skrip tidak boleh ukur:
     jenis huruf (skrip / sans / serif), teks, hiasan);
  2. langkah 5 QC B: imej jana -> ciri yang sama; ciri LULUS jika imej jatuh dalam tong yang sama dengan upload,
     iaitu "imej ini akan dihuraikan dengan frasa yang sama". SK10 melaporkan ciri teras lulus n / m.
Sempadan tong diletak daripada ukuran 16 gambar rujukan (decode/IMG_*.json, 28 Nov 2026) dan pertimbangan Claude;
belum diuji dengan jana baharu. Jalur (toleransi di sempadan) mengelak lulus / gagal bertukar kerana beza kecil.
Peraturan "angka mengatasi mata": kata "brush" hanya dipakai bila tepi strok diukur kasar.
Had: jenis huruf, hiasan dan teks kekal daripada mata. Ruang tepi tidak diambil daripada upload (kebanyakan upload
dipotong rapat); ia keputusan cetak dalam kad. Tekstur tidak dijana dalam v1.2 (Cetak v1).

Guna: python3 SK11_frasa.py decode/IMG_5840.json [...]         -> decode/kad/<nama>.json + ringkasan
      python3 SK11_frasa.py decode/IMG_5840.json --lawan K24     -> banding frasa draf dengan kad tulisan tangan
"""
import json
import sys
from pathlib import Path

import numpy as np

VERSI = "SK11 v1.0 (jadual F1)"
HERE = Path(__file__).resolve().parent

# ciri: (sempadan tong, label BM, frasa Inggeris, jalur toleransi di sempadan, teras)
JADUAL = {
    "tepi_strok": dict(unit="% tepi kasar", sempadan=[8, 16], jalur=2.0, teras=True,
                       tong=["licin", "sedikit kasar", "kasar / bertekstur"],
                       frasa=["smooth clean edges", "slightly rough hand-drawn edges", "rough textured edges"]),
    "condong_huruf_utama": dict(unit="darjah", sempadan=[5, 15, 28], jalur=3.0, teras=True,
                                tong=["tegak", "condong sedikit", "condong", "sangat condong"],
                                frasa=["upright", "slightly slanted to the right", "leaning to the right",
                                       "strongly slanted to the right"]),
    "condong_huruf_sokongan": dict(unit="darjah", sempadan=[5, 15, 28], jalur=3.0, teras=False,
                                   tong=["tegak", "condong sedikit", "condong", "sangat condong"],
                                   frasa=["upright", "slightly slanted to the right", "leaning to the right",
                                          "strongly slanted to the right"]),
    "condong_blok": dict(unit="darjah", sempadan=[3, 10], jalur=1.5, teras=True,
                         tong=["mendatar", "naik sedikit ke kanan", "naik jelas ke kanan"],
                         frasa=[None, "tilts slightly so each line rises toward the right",
                                "rises clearly toward the right"]),
    "tebal_utama_kata": dict(unit="indeks tebal", sempadan=[0.21, 0.29], jalur=0.02, teras=False,
                             tong=["ringan", "tebal", "sangat tebal"], frasa=["light", "bold", "very heavy"]),
    "tebal_utama_baris": dict(unit="% tinggi baris", sempadan=[10, 18], jalur=1.5, teras=False,
                              tong=["ringan", "tebal", "sangat tebal"], frasa=["light", "bold", "very heavy"]),
    "kontras_strok": dict(unit="nisbah tebal / nipis", sempadan=[1.7, 3.0], jalur=0.2, teras=False,
                          tong=["sekata", "kontras sederhana", "kontras tinggi"],
                          frasa=["an even stroke width", "moderate thick-and-thin contrast",
                                 "high thick-and-thin contrast"]),
    "hubungan_baris": dict(unit="% sela", sempadan=[0.3, 1.5], jalur=0.2, teras=False,
                           tong=["bertindih sedikit", "rapat", "terpisah"],
                           frasa=["sit close together and overlap slightly", "sit close together",
                                  "are clearly separated"]),
    "saiz_sokongan": dict(unit="nisbah tinggi sokongan / utama", sempadan=[0.6, 0.85, 1.15], jalur=0.05, teras=False,
                          tong=["jauh lebih kecil", "lebih kecil", "sama besar", "lebih tinggi"],
                          frasa=["medium", "large", "very large", "very large and taller than the main lines"]),
    "saiz_penyambung": dict(unit="nisbah tinggi penyambung / utama", sempadan=[0.5, 0.85], jalur=0.05, teras=False,
                            tong=["kecil", "lebih kecil", "sama besar"], frasa=["small", "smaller", "very large"]),
}
KATEGORI = {  # ciri kategori: nilai -> frasa; lulus = nilai sama
    "bekas": dict(teras=True, frasa={"pejal": "a small solid rectangular label", "garis luar": "a thin outlined box",
                                     "tiada": None}),
    "garis_sapuan": dict(teras=False, frasa={"ada": "a long swash or short dash strokes", "tiada": None}),
    "penjajaran": dict(teras=True, frasa={"rata kiri": "left-aligned", "tengah": "centered", "rata kanan": "right-aligned",
                                          "sama lebar (kiri dan kanan rata)": "every line stretched to the same width"}),
    "bentuk_blok": dict(teras=False, frasa={"segi empat": "one tight block", "bujur / membulat":
                                            "one tight block with a rounded outline", "tidak sekata": "one loose block"}),
}
# jenis huruf: daripada medan mata 'kelas' (BM, kata kunci) -> kata nama Inggeris. Angka boleh mengubahnya (lihat _nama).
JENIS = [("monoline", "monoline script lettering"), ("skrip", "script lettering"), ("serif", "serif letters"),
         ("sans", "sans-serif letters"), ("marker", "marker lettering"), ("potong", "cut-paper block letters"),
         ("gemuk", "chunky rounded block letters"), ("blok", "block letters"), ("lukisan tangan", "hand-drawn letters")]


def _wajaran(senarai, kunci):
    v = [(x.get(kunci), x.get("tinggi_px") or 1) for x in senarai if x.get(kunci) is not None]
    return float(np.average([a for a, _ in v], weights=[b for _, b in v])) if v else None


def _tong(nama, nilai):
    j = JADUAL[nama]
    i = int(np.searchsorted(j["sempadan"], abs(nilai) if nama.startswith("condong") else nilai, side="right"))
    return i, j["tong"][i], j["frasa"][i]


def ciri(r):
    """Ciri terukur satu rekod decode. Pulang {nama: dict(nilai, tong, frasa, teras, asas)}."""
    s, g, B = r["susunan"], r.get("seluruh") or {}, r["baris"]
    K = [k for k in r.get("kata") or [] if k.get("tinggi_px")]
    U = [k for k in K if k.get("peranan") == "utama"]
    S = [k for k in K if k.get("peranan") == "sokongan"]
    P = [k for k in K if k.get("peranan") == "penyambung"]
    bu = [b for b in B if b["peranan_saiz"] == "utama"]
    lurus = s.get("jenis_susunan", "baris lurus") == "baris lurus"
    asas_u = ("kata utama", U) if U else ("baris utama", bu) if (lurus and bu) else ("seluruh blok", None)
    c = {}

    def tambah(nama, nilai, asas, jadual=None):
        if nilai is None:
            return
        i, t, f = _tong(jadual or nama, nilai)
        j = JADUAL[jadual or nama]
        if nama.startswith("condong") and nilai < -j["sempadan"][0] and f:
            f = f.replace("right", "left")
        c[nama] = dict(nilai=round(float(nilai), 3), tong=t, indeks_tong=i, frasa=f, teras=j["teras"], asas=asas,
                       jadual=jadual or nama)

    ambil = lambda kunci, kg=None: (_wajaran(asas_u[1], kunci) if asas_u[1] else g.get(kg or kunci))
    tambah("tepi_strok", ambil("tepi_kasar_pct"), asas_u[0])
    tambah("condong_huruf_utama", ambil("condong_huruf_darjah"), asas_u[0])
    if S:
        tambah("condong_huruf_sokongan", _wajaran(S, "condong_huruf_darjah"), "kata sokongan")
    tambah("condong_blok", s["condong_darjah"], "blok")
    if U:
        tambah("tebal_utama", _wajaran(U, "indeks_tebal"), "kata utama", "tebal_utama_kata")
    elif lurus and bu:
        tambah("tebal_utama", _wajaran(bu, "tebal_strok_pct"), "baris utama", "tebal_utama_baris")
    elif g.get("indeks_tebal") is not None:
        tambah("tebal_utama", g["indeks_tebal"], "seluruh blok", "tebal_utama_kata")
    if c.get("tepi_strok", {}).get("indeks_tong", 2) < 2:              # tekstur merosakkan ukuran kontras
        tambah("kontras_strok", ambil("kontras_strok"), asas_u[0])
    if s.get("sela_baris_pct"):
        tambah("hubungan_baris", float(np.median(s["sela_baris_pct"])), "blok")
    tu = _wajaran(U, "tinggi_px")
    if tu and S:
        tambah("saiz_sokongan", _wajaran(S, "tinggi_px") / tu, "kata")
    if tu and P:
        tambah("saiz_penyambung", _wajaran(P, "tinggi_px") / tu, "kata")
    kat = dict(
        bekas=("pejal" if any(b.get("bekas") == "pejal" for b in B) else
               "garis luar" if any(b.get("bekas") == "garis luar" for b in B) else "tiada"),
        garis_sapuan="ada" if any(e["jenis"].startswith("garis") for e in r["elemen"]) else "tiada",
        bentuk_blok=g.get("bentuk_blok"))
    if lurus:
        kat["penjajaran"] = s["penjajaran"]
    for n, v in kat.items():
        if v is not None:
            c[n] = dict(nilai=v, tong=v, frasa=KATEGORI[n]["frasa"].get(v), teras=KATEGORI[n]["teras"], asas="blok", jadual=n)
    return c


def banding_ciri(ruj, jana):
    """QC B ikut ciri: lulus = tong sama (atau nilai dalam jalur sempadan tong rujukan)."""
    a, b = ciri(ruj), ciri(jana)
    keluar = []
    for n, x in a.items():
        y = b.get(n)
        if y is None or x.get("jadual") != y.get("jadual"):
            continue
        # Ujian 384 imej (banding/ciri_ujian.json, 28 Nov 2026):
        #  - tepi kasar pada rujukan biasanya TEKSTUR (grunge, kapur, bayang) yang v1.2 sengaja tidak jana (Cetak v1),
        #    jadi tepi_strok hanya dibanding bila rujukan licin atau sedikit kasar;
        #  - saiz_penyambung tidak membezakan (lulus 38% dengan rujukan sendiri, 45% dengan rujukan lain): maklumat.
        if n == "tepi_strok" and x["indeks_tong"] == 2 and not (ruj.get("mata") or {}).get("tepi_kasar_dijana"):
            keluar.append(dict(ciri=n, teras=False, kira=False, rujukan=x["nilai"], tong_rujukan=x["tong"], frasa_rujukan=x["frasa"],
                               jana=y["nilai"], tong_jana=y["tong"], lulus=None, hampir=False,
                               catatan="tidak dibanding: tekstur rujukan ditambah oleh skrip (Cetak v1), bukan dijana"))
            continue
        kira = n != "saiz_penyambung"
        if n in KATEGORI:
            lulus, hampir = x["nilai"] == y["nilai"], False
        else:
            j = JADUAL[x["jadual"]]
            lulus = x["indeks_tong"] == y["indeks_tong"]
            hampir = False
            if not lulus and abs(x["indeks_tong"] - y["indeks_tong"]) == 1:
                sem = j["sempadan"][min(x["indeks_tong"], y["indeks_tong"])]
                v = abs(y["nilai"]) if n.startswith("condong") else y["nilai"]
                hampir = abs(v - sem) <= j["jalur"]                  # jatuh di tepi sempadan: dikira lulus (hampir)
        keluar.append(dict(ciri=n, teras=x["teras"] and kira, kira=kira, rujukan=x["nilai"], tong_rujukan=x["tong"],
                           frasa_rujukan=x["frasa"], jana=y["nilai"], tong_jana=y["tong"], lulus=bool(lulus or hampir),
                           hampir=bool(hampir)))
    return keluar


def _nama(kelas, tepi_idx):
    """Kata nama jenis huruf daripada medan mata; angka mengatasi mata bagi kata 'brush'."""
    k = (kelas or "").lower()
    nama = next((en for bm, en in JENIS if bm in k), "lettering")
    catatan = "mata"
    if "berus" in k and "skrip" in k:
        if tepi_idx >= 1:
            nama, catatan = "brush script lettering", "mata + angka (tepi kasar: 'brush' dibenarkan)"
        else:
            catatan = "mata + angka (tepi licin: kata 'brush' dibuang)"
    return nama, catatan


def _kes(teks):
    t = "".join(ch for ch in teks if ch.isalpha())
    return "upper" if t.isupper() else "lower" if t.islower() else "title"


def draf_kad(r):
    """Draf isi Kad Gaya (bentuk kad.BLOK) daripada rekod decode. Setiap medan ada sumbernya."""
    c, mata, s = ciri(r), r.get("mata") or {}, r["susunan"]
    K = [k for k in r.get("kata") or [] if k.get("tinggi_px")]
    sumber = {}
    f = lambda n: c.get(n, {}).get("frasa")
    ti = c.get("tepi_strok", {}).get("indeks_tong", 0)
    huruf, kes = {}, {}
    for per, saiz_lalai, cond in (("utama", "very large", "condong_huruf_utama"),
                                  ("sokongan", f("saiz_sokongan") or "large", "condong_huruf_sokongan"),
                                  ("penyambung", f("saiz_penyambung") or "smaller", None)):
        kk = [k for k in K if k.get("peranan") == per]
        if not kk and per != "utama":
            continue
        km = mata.get("kelas_huruf")
        if isinstance(km, dict):                              # format lama: kelas setiap baris; ambil baris pertama
            km = next(iter(km.values()), None)
        kelas = (kk[0].get("kelas_mata") if kk else None) or km
        nama, cat = _nama(kelas if isinstance(kelas, str) else "", ti)
        # "connected" hanya untuk skrip: kata sans kecil beresolusi rendah boleh nampak bersambung pada skrip ukur
        bersambung = (all(k.get("bersambung") for k in kk) if kk else
                      (r.get("seluruh") or {}).get("kongsi_komponen_terbesar", 0) > 0.3)
        sambung = "connected " if ("script" in nama and bersambung) else ""
        tebal = f("tebal_utama") if per == "utama" else None
        if per != "utama" and kk:
            it = _wajaran(kk, "indeks_tebal")
            tebal = _tong("tebal_utama_kata", it)[2] if it is not None else None
        teks_semua = " ".join(mata.get("teks_rujukan") or [])
        kes[per] = (max((_kes(k["teks"]) for k in kk), key=["lower", "title", "upper"].index) if kk
                    else _kes(teks_semua) if teks_semua else "title")
        if kes[per] == "upper" and "letters" in nama:
            nama = nama.replace("letters", "capitals")
        slant = f(cond) if cond else None
        if per == "sokongan" and slant is None:
            slant = f("condong_huruf_utama")
        lebih_tinggi = "taller than the main lines" in saiz_lalai
        saiz = saiz_lalai.replace(" and taller than the main lines", "")
        bahagian = [saiz, tebal, (sambung + nama).strip()]
        penuh = " ".join(x for x in bahagian if x) + " with " + (f("tepi_strok") or "clean edges")
        if lebih_tinggi:
            penuh += ", taller than the main lines"
        if slant and slant != "upright":
            penuh += ", " + slant
        if kes[per] == "title":
            penuh += ", with a big capital"
        huruf[per] = dict(penuh=penuh, ringkas=" ".join(x for x in [tebal, (sambung + nama).strip()] if x))
        sumber["huruf." + per] = ("angka: saiz, tebal, tepi, condong; jenis huruf: " + cat + "; huruf besar / kecil: teks (mata)")
    amaran = []
    for per in ("utama", "sokongan"):
        jenis = {_nama(k.get("kelas_mata") or "", ti)[0] for k in K if k.get("peranan") == per}
        if len(jenis) > 1:
            amaran.append("kata %s berlainan jenis huruf (%s): satu frasa tidak cukup; tetapkan peranan ikut jenis huruf"
                          % (per, ", ".join(sorted(jenis))))
    hier = ("All the words are about the same size." if c.get("saiz_sokongan", {}).get("tong", "sama besar") == "sama besar"
            and c.get("saiz_penyambung", {}).get("tong", "sama besar") == "sama besar"
            else "The main words are larger than the small connecting words.")
    blok = dict(
        medium="lettering quote poster", gaya="hand-lettered", latar_warna="solid black", latar_isi=None,
        tepi=f("tepi_strok"), bentuk=f("bentuk_blok") or "one tight block", condong=f("condong_blok"),
        sentuh=f("hubungan_baris") or "sit close together", margin="wide empty black margins", huruf=huruf,
        tertinggi=None, hierarki=hier, hiasan=None, sisi=None, hiasan_kotak=[],
        tiada=["other colors", "outline", "shadow"], ada="solid white strokes on a clean black background",
        sama_lebar=c.get("penjajaran", {}).get("nilai") == "sama lebar (kiri dan kanan rata)",
        rujukan=dict(condong_darjah=s["condong_darjah"], tepi_pct=s["tepi_min_pct"], tepi_sisi_pct=min(s["tepi_pct"]["kiri"], s["tepi_pct"]["kanan"]),
                     tepi_atas_bawah_pct=min(s["tepi_pct"]["atas"], s["tepi_pct"]["bawah"]), sumber=r["versi"] + " pada " + r["fail"]))
    for n, kunci in (("tepi", "tepi_strok"), ("bentuk", "bentuk_blok"), ("condong", "condong_blok"), ("sentuh", "hubungan_baris")):
        x = c.get(kunci)
        sumber[n] = ("angka: %s = %s -> %s" % (kunci, x["nilai"], x["tong"])) if x else "lalai (tiada ukuran)"
    sumber["hierarki"] = "angka: nisbah tinggi kata ikut peranan" if K else "lalai (tiada kotak kata)"
    sumber["medium, latar, margin, tiada, ada"] = "tetap v1.2 (hitam putih; ruang tepi ialah keputusan cetak dalam kad)"
    sumber["hiasan"] = "mata (senarai hiasan); skrip hanya mengesan ada / tiada"
    # kotak baris (piksel, kanvas 768 x 1024) daripada kotak kata
    if K:
        n_baris = max(1, len(mata.get("teks_rujukan") or K))
        tinggi_blok = (100 - s["tepi_pct"]["atas"] - s["tepi_pct"]["bawah"]) / 100 * 1024
        bul = lambda v: int(max(8, round(v / 8) * 8))
        uk = {}
        for per, nis in (("utama", 1.0), ("sokongan", c.get("saiz_sokongan", {}).get("nilai", 1.0)),
                         ("penyambung", c.get("saiz_penyambung", {}).get("nilai", 0.5))):
            kk = [k for k in K if k.get("peranan") == per]
            if kk:
                lebar = float(np.mean([(k["kotak"][2] - k["kotak"][0]) for k in kk])) / 100 * 768
                uk[per] = (bul(min(lebar, 624)), bul(tinggi_blok / n_baris * min(1.0, float(nis))))
        blok["ukuran"] = uk
        sumber["ukuran"] = "angka: kotak kata (mata menanda kotak, skrip mengukur) dan tinggi blok / bilangan baris"
    return dict(versi=VERSI, rekod=r["fail"], jenis_susunan=s.get("jenis_susunan"), amaran=amaran, blok=blok, sumber=sumber,
                ciri={n: {k: v for k, v in x.items() if k != "indeks_tong"} for n, x in c.items()},
                ciri_teras=[n for n, x in c.items() if x["teras"]],
                mata=dict(nama_gaya=mata.get("nama_gaya"), hiasan=mata.get("hiasan"), jangan_salin=mata.get("jangan_salin")),
                nota="Draf: frasa daripada angka decode (jadual F1). Semak hiasan dan jenis huruf dengan mata sebelum jadi kad.")


if __name__ == "__main__":
    a = sys.argv[1:]
    lawan = a[a.index("--lawan") + 1] if "--lawan" in a else None
    fail = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] != "--lawan")]
    if not fail:
        sys.exit(__doc__)
    for f in fail:
        r = json.loads(Path(f).read_text())
        d = draf_kad(r)
        keluar = Path(f).resolve().parent / "kad"
        keluar.mkdir(exist_ok=True)
        (keluar / (Path(f).stem + ".json")).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
        print("==", r["fail"], "|", d["jenis_susunan"])
        for per, h in d["blok"]["huruf"].items():
            print("  %-10s %s" % (per, h["penuh"]))
        print("  blok       tepi: %s | condong: %s | baris: %s | bentuk: %s" % (d["blok"]["tepi"], d["blok"]["condong"],
                                                                              d["blok"]["sentuh"], d["blok"]["bentuk"]))
        if lawan:
            sys.path.insert(0, str(HERE.parent))
            import kad
            b = kad.BLOK[lawan]
            print("  -- kad tulisan tangan", lawan)
            for per, h in b["huruf"].items():
                print("  %-10s %s" % (per, h.get("penuh") or h.get("dalam")))
            print("  blok       tepi: %s | condong: %s | baris: %s | bentuk: %s" % (b.get("tepi"), b.get("condong"), b.get("sentuh"), b.get("bentuk")))
