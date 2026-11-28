#!/usr/bin/env python3
"""Bina data tab Etsy dashboard daripada analisis tangan + ukuran potongan.

Input:
  data/etsy/designs.txt        analisis setiap design (ditulis tangan, lihat kepala fail)
  data/etsy/designs_extra.txt  lapisan kedua: saiz baris, gaya ikon, kesan huruf, formula ayat, kunci gaya
  data/etsy/crop_metrics.json  ukuran potongan (scripts/etsy_crop.py)
  data/etsy/blobs.txt          id gambar yang dimuat naik ke dashboard
  data/etsy/font_calon.json    lesen font calon (disalin daripada senarai induk font dashboard)
Output (jangan ubah secara manual):
  data/export/etsy/designs.json, listing.json, fonts.json

Guna: python3 scripts/build_etsy.py [laluan fonts_master.json]
Jika laluan fonts_master diberi, data/etsy/font_calon.json dijana semula daripadanya.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "etsy")
OUT = os.path.join(ROOT, "data", "export", "etsy")
DIKEMAS = "2026-11-28"

# kod font -> (nama jenis, ciri, font calon ikut keutamaan)
FONT = {
    "SP": ("Sans padat", "Huruf besar tebal dan sempit, tinggi", ["Anton", "League Gothic", "Bebas Neue"]),
    "SL": ("Sans lebar", "Huruf besar tebal dan lebar", ["Archivo Black", "Dela Gothic One"]),
    "SB": ("Sans bulat", "Huruf besar tebal berbucu bulat", ["Bowlby One", "Titan One"]),
    "sn": ("Sans kecil", "Huruf besar kecil untuk kata sambung", ["Bebas Neue", "Oswald"]),
    "SLB": ("Slab", "Huruf besar berkaki tebal", ["Alfa Slab One", "Bevan"]),
    "VAR": ("Varsity", "Slab gaya kolej, pejal", ["Graduate", "Alfa Slab One"]),
    "VARO": ("Varsity bergaris luar", "Slab gaya kolej dengan garis luar berganda", ["Graduate", "Bungee Inline"]),
    "SKR": ("Skrip berus", "Tulisan sambung tebal, condong naik, berekor", ["Pacifico", "Lobster", "Kaushan Script"]),
    "SKN": ("Skrip nipis", "Tulisan sambung halus", ["Dancing Script", "Satisfy", "Sacramento"]),
    "BC": ("Berus condong", "Huruf besar sapuan berus, condong", ["Knewave", "Permanent Marker"]),
    "BK": ("Berus kering", "Huruf besar berus kering bertepi kasar", ["Permanent Marker", "Rock Salt"]),
    "HT": ("Huruf tangan", "Huruf besar tulisan tangan santai", ["Chewy", "Amatic SC"]),
    "RTK": ("Retak / kasar", "Huruf besar tebal bertekstur retak", ["Rubik Dirt", "Anton"]),
    "WST": ("Western berhias", "Huruf besar gaya koboi berhias", ["Rye", "Sancreek"]),
    "SRF": ("Serif huruf kecil", "Huruf kecil berkaki, tebal", ["Bevan", "Roboto Slab"]),
}
EXTRA_FONTS = ["Berkshire Swash", "Playball"]

RAWATAN = {
    "-": "biasa", "L": "lengkung naik", "S": "senget", "R": "reben hitam", "RG": "reben garis",
    "RS": "reben skrol", "KH": "kotak hitam", "KG": "kotak garis", "P": "pil",
    "B": "sapuan berus hitam", "PH": "plak hitam", "=": "sebaris dengan baris sebelumnya",
}
BUKAN_BEKAS = {"-", "L", "S", "=", "lengkung turun", "bergaris potong", "bergaris luar"}
PERANAN = {"H": "kata utama", "S": "sokongan", "K": "kata sambung"}
PERANAN_KOD = {"H": "U", "S": "S", "K": "K"}
SUSUNAN = {
    "reben-bertindan": "Reben bertindan", "bertindan": "Bertindan tanpa reben", "lencana-bulat": "Lencana bulat",
    "perisai": "Perisai", "ikon-tengah": "Ikon di tengah", "ikon-atas": "Ikon di atas", "ikon-sisi": "Ikon di sisi",
    "skrip-dominan": "Skrip dominan", "ikon-ganti-huruf": "Ikon dalam kata", "bingkai-ikon": "Ikon sebagai bingkai",
    "dua-baris": "Dua baris", "lengkung-atas": "Lengkung atas", "papan-tanda": "Papan tanda",
    "panel-ikon": "Panel ikon", "ikon-sahaja": "Ikon sahaja",
}
SILUET = {"segi4": "Segi empat", "bulat": "Bulat", "perisai": "Perisai", "bebas": "Bebas"}
TEMA = {"sindiran": "Sindiran", "football": "Football"}
LISTING = {
    "sindiran": "Sarcastic Quotes SVG Bundle",
    "football": "Bundle football (tajuk belum disahkan)",
}
FAIL = {1: "IMG_5856", 3: "IMG_5858", 4: "IMG_5857", 7: "IMG_5862", 8: "IMG_5865", 9: "IMG_5864", 10: "IMG_5863"}
ULANGAN = {1: "IMG_5859", 3: "IMG_5861", 4: "IMG_5860"}

# jenis hiasan: (kata kunci dalam teks hiasan, nama jenis); satu hiasan boleh sepadan dengan beberapa jenis
HIASAN = [
    ("pancar", "Pancar"), ("bintang", "Bintang"), ("hati", "Hati"), ("kilau", "Kilau 4 bucu"),
    ("halftone", "Titik halftone"), ("titik", "Titik"), ("garis ekor", "Garis ekor"), ("sapuan ekor", "Garis ekor"),
    ("sapuan berus", "Sapuan berus"), ("laju", "Garis laju"), ("lengkung gerak", "Garis laju"),
    ("garis apit", "Garis pemisah"), ("garis tiga", "Garis pemisah"), ("garis berganda", "Garis pemisah"),
    ("garis bawah", "Garis pemisah"), ("dengan garis", "Garis pemisah"), ("garis dan", "Garis pemisah"),
    ("garis jahitan", "Garis pemisah"), ("garis titik", "Garis pemisah"), ("garis bunyi", "Garis pemisah"),
    ("daun", "Daun"), ("anak panah", "Anak panah"), ("ukiran", "Ukiran pusar"), ("percikan", "Percikan"),
    ("titisan", "Percikan"), ("kilat", "Kilat"), ("jalur", "Jalur"), ("tanda petik", "Tanda petik"),
    ("bingkai", "Bingkai atau tapak"), ("bulatan", "Bingkai atau tapak"), ("bucu", "Bingkai atau tapak"),
    ("tapak", "Bingkai atau tapak"), ("panel", "Bingkai atau tapak"), ("lengkung atas", "Bingkai atau tapak"),
    ("lengkung bawah", "Bingkai atau tapak"), ("garis lengkung", "Bingkai atau tapak"), ("rajah taktik", "Rajah taktik"),
]
KESAN = [
    ("berus kering", "Berus kering"), ("hujung berus", "Hujung berus"), ("tebuk", "Tebuk (teks putih)"),
    ("garis luar", "Garis luar"), ("bergaris", "Garis luar"), ("garis dalam", "Garis dalam"), ("bayang", "Bayang"),
    ("kasar", "Tepi kasar"), ("koyak", "Tepi kasar"), ("retak", "Tepi kasar"), ("calar", "Tepi kasar"),
    ("bertakuk", "Tepi kasar"), ("bergerigi", "Tepi kasar"), ("berjalur", "Berjalur"), ("potong", "Potong serong"),
    ("kotak putih", "Bekas putih"), ("reben putih", "Bekas putih"), ("diapit", "Diapit reben"),
    ("letupan", "Letupan komik"), ("bucu serong", "Bucu serong"), ("condong", "Condong"),
]
KATEGORI_IKON = [
    (("bola", "helmet"), "Sukan"),
    (("kucing", "anjing", "itik", "ayam"), "Haiwan"),
    (("cawan", "garpu", "labu"), "Makanan dan minuman"),
    (("mata", "bulu mata", "tangan", "tapak kaki"), "Badan"),
    (("matahari", "bulan", "puting", "daun", "api"), "Alam"),
    (("hati", "bintang", "salib", "kilat", "mahkota", "amaran", "kuasa", "pin", "gelembung"), "Simbol"),
    (("jam", "mentol", "buku", "pensel", "dumbel", "kalendar", "stetoskop", "bumbung"), "Objek"),
]
GAYA_IKON = {"pejal": "pejal (siluet hitam)", "garis": "garis luar", "tebuk": "tebuk (putih dalam hitam)",
             "campur": "campur pejal dan garis"}
SAIZ_IKON = {"K": "kecil", "S": "sederhana", "B": "besar"}
SAYA = {"I", "I'M", "I'LL", "I'VE", "MY", "ME", "MYSELF"}
KAMI = {"WE'RE", "LET'S", "WE"}


def parse(path):
    out, cur = [], None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = re.match(r"^#(\d+-\d+) (\S+) (\S+) (\S+)(.*)$", line)
        if m:
            cur = {"id": m.group(1), "tema": m.group(2), "susunan": m.group(3), "siluet": m.group(4),
                   "flags": m.group(5).split(), "L": [], "I": [], "O": [], "M": {}}
            out.append(cur)
            continue
        if cur is None or not line.strip() or line.startswith("#"):
            continue
        tag, body = line[:2], line[2:].strip()
        if tag == "L:":
            for part in body.split(" | "):
                teks, font, rawat, peranan = part.rsplit("/", 3)
                kod, _, khas = font.partition(":")
                cur["L"].append({"teks": teks, "kod": kod, "khas": khas, "rawat": rawat.split("+"), "peranan": peranan})
        elif tag == "I:":
            for part in body.split(" | "):
                apa, kedudukan, peranan = [x.strip() for x in part.rsplit(",", 2)]
                cur["I"].append({"apa": apa, "kedudukan": kedudukan, "peranan": peranan})
        elif tag == "O:":
            cur["O"] = [x.strip() for x in body.split(",") if x.strip()]
        elif tag == "M:":
            parts = [x.strip() for x in body.split(" ; ")]
            cur["M"]["rasa"] = parts[0]
            for p in parts[1:]:
                k, _, v = p.partition(":")
                cur["M"][k.strip()] = v.strip()
    return out


def parse_extra(path):
    out = {}
    for raw in open(path, encoding="utf-8"):
        if raw.startswith("#") or not raw.strip():
            continue
        f = [x.strip() for x in raw.rstrip("\n").split(" | ")]
        assert len(f) == 9, raw
        out[f[0]] = {
            "sz": [] if f[1] == "-" else [int(x) for x in f[1].split()],
            "ik": [] if f[2] == "-" else [x.split() for x in f[2].split("; ")],
            "fx_raw": "" if f[3] == "-" else f[3], "tindih": f[4], "sudut": int(f[5]), "formula": f[6], "nada": f[7], "kunci": f[8],
        }
    return out


def parse_fx(raw, teks_list, did):
    """'KATA=kesan, KATA2=kesan' -> {kata: kesan}; kata boleh mengandungi koma."""
    marks = []
    for t in sorted(set(teks_list), key=len, reverse=True):
        for m in re.finditer(r"(?:^|, )" + re.escape(t) + "=", raw):
            if not any(a <= m.start() < b for a, b, _ in marks):
                marks.append((m.start(), m.end(), t))
    marks.sort()
    assert bool(marks) == bool(raw), (did, "kesan tidak dapat dipadankan", raw)
    out = {}
    for i, (a, b, t) in enumerate(marks):
        out[t] = raw[b:marks[i + 1][0] if i + 1 < len(marks) else len(raw)]
    assert not raw or marks[0][0] == 0, (did, raw)
    return out


def uniq(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def kelas(text, table):
    t = text.lower()
    return uniq(nama for kunci, nama in table if kunci in t)


def slot_teks(slot, lines):
    if slot == "b":
        return "membingkai teks"
    if slot == "s":
        return "di sisi"
    if slot == "0":
        return "paling atas"
    if slot[0] in "hx":
        n = int(slot[1:])
        kata = lines[n - 1]["teks"] if 0 < n <= len(lines) else "?"
        return (f"dalam huruf baris {n} ({kata})" if slot[0] == "h" else f"di belakang baris {n} ({kata})")
    n = int(slot)
    if n >= len(lines):
        return "paling bawah"
    return f"selepas baris {n} ({lines[n - 1]['teks']})"


def main():
    os.makedirs(OUT, exist_ok=True)
    designs = parse(os.path.join(SRC, "designs.txt"))
    extra = parse_extra(os.path.join(SRC, "designs_extra.txt"))
    metrics = {r["id"]: r for r in json.load(open(os.path.join(SRC, "crop_metrics.json")))}
    blobs = dict(l.split() for l in open(os.path.join(SRC, "blobs.txt")) if l.strip())

    calon_path = os.path.join(SRC, "font_calon.json")
    semua_font = uniq([f for v in FONT.values() for f in v[2]] + EXTRA_FONTS)
    if len(sys.argv) > 1:
        induk = {r["name"].lower(): r for r in json.load(open(sys.argv[1]))}
        lesen = {}
        for f in semua_font:
            r = induk.get(f.lower())
            lesen[f] = ({"src": r["src"], "lic": r["lic"], "risk": r["risk"], "url": r.get("url"), "lic_url": r.get("lic_url")}
                        if r else None)
        json.dump(lesen, open(calon_path, "w"), indent=1, ensure_ascii=False)
    lesen = json.load(open(calon_path))

    keluarga = {}
    for d in designs:
        keluarga.setdefault(extra[d["id"]]["formula"], []).append(d["id"])

    rows = []
    for d in designs:
        x = extra[d["id"]]
        assert d["tema"] in TEMA and d["susunan"] in SUSUNAN and d["siluet"] in SILUET, d["id"]
        assert len(x["sz"]) == len(d["L"]), (d["id"], "saiz", len(x["sz"]), len(d["L"]))
        assert len(x["ik"]) == len(d["I"]), (d["id"], "ikon", len(x["ik"]), len(d["I"]))
        x["fx"] = parse_fx(x["fx_raw"], [l["teks"] for l in d["L"]], d["id"])
        m = metrics[d["id"]]
        lines = []
        for l, sz in zip(d["L"], x["sz"]):
            assert l["kod"] in FONT and l["peranan"] in PERANAN, (d["id"], l)
            huruf = [c for c in l["teks"] if c.isalpha()]
            besar = sum(1 for c in huruf if c.isupper())
            kes = "–" if not huruf else "HURUF BESAR" if besar == len(huruf) else "huruf kecil" if besar == 0 else "Campur"
            lines.append({
                "teks": l["teks"], "font": FONT[l["kod"]][0], "calon": l["khas"] or FONT[l["kod"]][2][0],
                "saiz": sz, "kes": kes, "rawatan": ", ".join(RAWATAN.get(r, r) for r in l["rawat"]),
                "kesan": x["fx"].get(l["teks"], ""), "peranan": PERANAN[l["peranan"]],
                "_kod": l["kod"], "_r": l["rawat"], "_p": l["peranan"],
            })
        n = len(lines)
        ayat = " ".join(l["teks"] for l in lines)
        huruf = [c for c in ayat if c.isalpha()]
        jenis_font = uniq(l["font"] for l in lines)
        calon = uniq(f"{l['font']}: " + (d["L"][i]["khas"] or " / ".join(FONT[l["_kod"]][2][:2])) for i, l in enumerate(lines))
        bekas = uniq(RAWATAN.get(r, r) for l in lines for r in l["_r"] if r not in BUKAN_BEKAS)
        arah = uniq(("naik" if r == "L" else "turun") for l in lines for r in l["_r"] if r in ("L", "lengkung turun"))
        utama = [l for l in lines if l["_p"] == "H"]
        ked = uniq(("atas" if i < n / 3 else "tengah" if i < 2 * n / 3 else "bawah") for i, l in enumerate(lines) if l["_p"] == "H")
        sz = [l["saiz"] for l in lines]
        terbesar = [l["teks"] for l in lines if sz and l["saiz"] == max(sz)]
        tokens = {t.strip('.,"?!').upper() for t in ayat.split()}
        pandang = "Saya" if tokens & SAYA else "Kami" if tokens & KAMI else "Tiada (label atau seruan)"
        r1 = lines[0] if lines else None
        rawat1 = "–" if not r1 else next((RAWATAN.get(r, r) for r in r1["_r"] if r not in ("-", "S", "=")), "biasa")

        ikon = []
        for i, k in zip(d["I"], x["ik"]):
            gaya, saiz, slot = k
            assert gaya in GAYA_IKON and saiz in SAIZ_IKON, (d["id"], k)
            kat = next((nama for kunci, nama in KATEGORI_IKON if any(q in i["apa"].lower() for q in kunci)), "Lain")
            ikon.append({"apa": i["apa"], "kedudukan": i["kedudukan"], "peranan": i["peranan"], "gaya": GAYA_IKON[gaya],
                         "saiz": SAIZ_IKON[saiz], "slot": slot_teks(slot, lines), "kategori": kat})
        peranan_ikon = uniq(i["peranan"] for i in ikon)
        jenis_hiasan = uniq(j for o in d["O"] for j in (kelas(o, HIASAN) or ["Lain"]))
        kesan_jenis = uniq(j for v in x["fx"].values() for j in (kelas(v, KESAN) or ["Lain"]))
        kasar, senget, taksim = ("kasar" in d["flags"]), ("senget" in d["flags"]) or x["sudut"] >= 5, ("taksimetri" in d["flags"])
        rumit = any(p in ("ganti-huruf", "bingkai", "panel") for p in peranan_ikon)
        skor = n + len(jenis_font) + (2 if rumit else 0) + (1 if arah else 0) + (1 if kasar else 0) + (1 if len(bekas) >= 3 else 0)
        kesukaran = "Mudah" if skor <= 6 else "Sederhana" if skor <= 9 else "Sukar"
        baris_fizikal = sum(1 for l in lines if "=" not in l["_r"])

        langkah = "; ".join(
            f"{i + 1}) {l['teks']}: {l['font']} ({l['calon']}), saiz {l['saiz']}/5, {l['rawatan']}"
            + (f", {l['kesan']}" if l["kesan"] else "") for i, l in enumerate(lines))
        resipi = (f"{n} blok teks dalam {baris_fizikal} baris, tangga saiz {'-'.join(map(str, sz))}. " if n else "Tiada teks. ") \
            + (langkah + ". " if langkah else "") \
            + ("Ikon: " + "; ".join(f"{i['apa']} ({i['gaya']}, {i['saiz']}, {i['slot']})" for i in ikon) + ". " if ikon else "Tiada ikon. ") \
            + ("Hiasan: " + ", ".join(d["O"]) + ". " if d["O"] else "") \
            + f"Siluet {SILUET[d['siluet']].lower()}, senget kira-kira {x['sudut']} darjah. Kunci: {x['kunci']}."
        for l in lines:
            for k in ("_kod", "_r", "_p"):
                del l[k]
        g = m["gambar"]
        fam = keluarga[x["formula"]]
        rows.append({
            "id": d["id"], "img": f"/_blob/{blobs[d['id']]}", "tema": TEMA[d["tema"]], "listing": LISTING[d["tema"]],
            "penjual": "ArtfulCraftsCreators",
            # teks dan font
            "ayat": ayat or "(tiada teks)", "bil_perkataan": len(ayat.split()), "bil_aksara": len(huruf),
            "huruf_besar_pct": round(100 * sum(1 for c in huruf if c.isupper()) / len(huruf)) if huruf else 0,
            "bil_blok": n, "bil_baris": baris_fizikal,
            "kata_utama": ", ".join(l["teks"] for l in utama) or "–",
            "kedudukan_utama": ", ".join(ked) or "–",
            "baris_json": json.dumps(lines, ensure_ascii=False),
            "tangga_saiz": "-".join(map(str, sz)) or "–", "baris_terbesar": ", ".join(terbesar) or "–",
            "kontras_saiz": (max(sz) - min(sz)) if sz else 0,
            "corak_peranan": " › ".join(PERANAN_KOD[p["peranan"]] for p in d["L"]) or "–",
            "corak_font": " › ".join(l["font"] for l in lines) or "–",
            "jenis_font": ", ".join(jenis_font) or "–", "bil_font": len(jenis_font),
            "gandingan_font": " + ".join(sorted(f for f in jenis_font if f != "Sans kecil")) or "–",
            "font_kata_utama": ", ".join(uniq(l["font"] for l in utama)) or "–",
            "font_baris_pertama": lines[0]["font"] if lines else "–",
            "font_baris_akhir": lines[-1]["font"] if lines else "–",
            "rawatan_baris_pertama": rawat1,
            "font_calon": "; ".join(calon) or "–",
            "kesan_khas": ", ".join(kesan_jenis) or "Tiada",
            "kesan_butiran": "; ".join(f"{k}: {v}" for k, v in x["fx"].items()) or "Tiada",
            # ikon dan hiasan
            "ikon": "; ".join(f"{i['apa']} ({i['kedudukan']}; {i['gaya']}; {i['saiz']}; {i['slot']})" for i in ikon) or "Tiada",
            "ikon_json": json.dumps(ikon, ensure_ascii=False),
            "bil_ikon": len(ikon), "peranan_ikon": ", ".join(peranan_ikon) or "–",
            "gaya_ikon": ", ".join(uniq(i["gaya"] for i in ikon)) or "–",
            "saiz_ikon": ", ".join(uniq(i["saiz"] for i in ikon)) or "–",
            "kategori_ikon": ", ".join(uniq(i["kategori"] for i in ikon)) or "–",
            "hiasan": ", ".join(d["O"]) or "Tiada", "bil_hiasan": len(d["O"]),
            "jenis_hiasan": ", ".join(jenis_hiasan) or "Tiada", "bil_jenis_hiasan": len(jenis_hiasan),
            # susunan
            "susunan": SUSUNAN[d["susunan"]], "siluet": SILUET[d["siluet"]],
            "bekas": ", ".join(bekas) or "Tiada", "bil_bekas": len(bekas),
            "simetri": "Tidak" if taksim else "Ya", "senget": "Ya" if senget else "Tidak", "sudut_senget": x["sudut"],
            "lengkung": "Ya" if arah else "Tidak", "arah_lengkung": ", ".join(arah) or "–",
            "tindih": "Ya" if x["tindih"] == "ya" else "Tidak", "tekstur": "Kasar" if kasar else "Bersih",
            # ukuran piksel
            "lebar_px": m["lebar_px"], "tinggi_px": m["tinggi_px"], "nisbah": m["nisbah"], "dakwat_pct": m["dakwat_pct"],
            "simetri_pct": m["simetri_pct"], "dakwat_atas_pct": m["dakwat_atas_pct"],
            "dakwat_tengah_pct": m["dakwat_tengah_pct"], "dakwat_bawah_pct": m["dakwat_bawah_pct"],
            "pusat_x_pct": m["pusat_x_pct"], "pusat_y_pct": m["pusat_y_pct"], "kepingan": m["kepingan"],
            "lubang": m["lubang"], "tebal_pct": m["tebal_pct"], "isi_siluet_pct": m["isi_siluet_pct"],
            # ayat
            "formula": x["formula"], "bil_sekeluarga": len(fam),
            "sekeluarga": ", ".join(i for i in fam if i != d["id"]) or "–",
            "nada": x["nada"].capitalize(), "sudut_pandang": pandang,
            "rasa": d["M"].get("rasa", "–"), "khalayak": d["M"].get("khalayak", "–"), "isu_ayat": d["M"].get("isu", ""),
            # tiru
            "kunci_gaya": x["kunci"], "resipi": resipi, "skor_tiru": skor, "kesukaran": kesukaran,
            "status": "Belum diuji", "nota": d["M"].get("nota", ""),
            "fail_asal": FAIL[g] + (f" (ulangan: {ULANGAN[g]})" if g in ULANGAN else ""),
            "kedudukan": f"baris {m['baris']}, lajur {m['lajur']}", "dikemas": DIKEMAS,
        })
    assert len(rows) == len(metrics) == 130, len(rows)
    json.dump(rows, open(os.path.join(OUT, "designs.json"), "w"), ensure_ascii=False, indent=0)

    n = {t: sum(1 for r in rows if r["tema"] == TEMA[t]) for t in TEMA}
    listing = [
        {"listing": LISTING["sindiran"],
         "tajuk_penuh": "Sarcastic Quotes SVG Bundle, Funny Mom Sayings, Adult Humor Cut File (Digital Download)",
         "penjual": "ArtfulCraftsCreators", "platform": "Etsy", "harga_rm": 4.65, "harga_asal_rm": 15.46,
         "diskaun_pct": 70, "rating": 4.9, "bil_rating": 47, "format": "Digital (fail SVG)",
         "dilihat": "2026-11-28", "gambar": "IMG_5856, IMG_5858, IMG_5857", "bil_design": n["sindiran"],
         "bukti": "rasmi",
         "nota_bukti": "Tangkap layar halaman listing Etsy (IMG_5866) menunjukkan IMG_5856; dua gambar lain diandaikan daripada listing yang sama."},
        {"listing": LISTING["football"], "tajuk_penuh": "Belum diberi", "penjual": "ArtfulCraftsCreators",
         "platform": "Etsy", "harga_rm": None, "harga_asal_rm": None, "diskaun_pct": None, "rating": None,
         "bil_rating": None, "format": "Digital (fail SVG)", "dilihat": "2026-11-28",
         "gambar": "IMG_5862, IMG_5865, IMG_5864, IMG_5863", "bil_design": n["football"], "bukti": "lemah",
         "nota_bukti": "Penjual ikut kata pengguna; tiada tangkap layar listing football."},
    ]
    json.dump(listing, open(os.path.join(OUT, "listing.json"), "w"), ensure_ascii=False, indent=0)

    guna = {}
    for d in designs:
        for kod in {l["kod"] for l in d["L"]}:
            guna[kod] = guna.get(kod, 0) + 1
    fonts = []
    for kod, (nama, ciri, calon) in FONT.items():
        for i, f in enumerate(calon):
            info = lesen.get(f) or {}
            fonts.append({"kunci": f"{nama} / {f}", "jenis": nama, "ciri": ciri, "bil_design": guna.get(kod, 0),
                          "font": f, "pilihan": i + 1, "sumber": info.get("src", "tiada dalam senarai induk"),
                          "lesen": info.get("lic", "belum disemak"), "risiko": info.get("risk", "semak"),
                          "url": info.get("url") or ""})
    for f in EXTRA_FONTS:
        info = lesen.get(f) or {}
        fonts.append({"kunci": f"Skrip berus / {f}", "jenis": "Skrip berus", "ciri": "Calon khusus untuk beberapa design",
                      "bil_design": guna.get("SKR", 0), "font": f, "pilihan": 9,
                      "sumber": info.get("src", "tiada dalam senarai induk"), "lesen": info.get("lic", "belum disemak"),
                      "risiko": info.get("risk", "semak"), "url": info.get("url") or ""})
    fonts.sort(key=lambda r: (-r["bil_design"], r["jenis"], r["pilihan"]))
    json.dump(fonts, open(os.path.join(OUT, "fonts.json"), "w"), ensure_ascii=False, indent=0)
    print(f"{len(rows)} design x {len(rows[0])} medan, {len(listing)} listing, {len(fonts)} baris font -> {OUT}")


if __name__ == "__main__":
    main()
