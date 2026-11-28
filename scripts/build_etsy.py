#!/usr/bin/env python3
"""Bina data tab Etsy dashboard daripada analisis tangan + ukuran potongan.

Input:
  data/etsy/designs.txt        analisis setiap design (ditulis tangan, lihat kepala fail)
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
    "-": "biasa", "L": "lengkung", "S": "senget", "R": "reben hitam", "RG": "reben garis",
    "RS": "reben skrol", "KH": "kotak hitam", "KG": "kotak garis", "P": "pil",
    "B": "sapuan berus hitam", "PH": "plak hitam",
}
BEKAS = {"R", "RG", "RS", "KH", "KG", "P", "B", "PH"}  # rawatan yang menjadi bekas teks
PERANAN = {"H": "kata utama", "S": "sokongan", "K": "kata sambung"}
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


def uniq(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    designs = parse(os.path.join(SRC, "designs.txt"))
    metrics = {r["id"]: r for r in json.load(open(os.path.join(SRC, "crop_metrics.json")))}
    blobs = dict(l.split() for l in open(os.path.join(SRC, "blobs.txt")) if l.strip())

    # lesen font calon
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

    rows = []
    for d in designs:
        for k in (d["tema"], ):
            assert k in TEMA, (d["id"], k)
        assert d["susunan"] in SUSUNAN, (d["id"], d["susunan"])
        assert d["siluet"] in SILUET, (d["id"], d["siluet"])
        m = metrics[d["id"]]
        lines = []
        for l in d["L"]:
            assert l["kod"] in FONT, (d["id"], l["kod"])
            assert l["peranan"] in PERANAN, (d["id"], l["peranan"])
            rawat = [RAWATAN.get(x, x) for x in l["rawat"]]
            lines.append({
                "teks": l["teks"], "font": FONT[l["kod"]][0], "calon": l["khas"] or FONT[l["kod"]][2][0],
                "rawatan": ", ".join(rawat), "peranan": PERANAN[l["peranan"]],
            })
        ayat = " ".join(l["teks"] for l in d["L"])
        jenis_font = uniq(FONT[l["kod"]][0] for l in d["L"])
        calon = uniq(f"{FONT[l['kod']][0]}: " + (l["khas"] or " / ".join(FONT[l["kod"]][2][:2])) for l in d["L"])
        bekas = uniq(RAWATAN.get(x, x) for l in d["L"] for x in l["rawat"]
                     if x in BEKAS or (x not in RAWATAN))
        ada_lengkung = any("L" in l["rawat"] for l in d["L"])
        peranan_ikon = uniq(i["peranan"] for i in d["I"])
        kasar, senget, taksim = ("kasar" in d["flags"]), ("senget" in d["flags"]), ("taksimetri" in d["flags"])
        rumit = any(p in ("ganti-huruf", "bingkai", "panel") for p in peranan_ikon)
        skor = len(lines) + len(jenis_font) + (2 if rumit else 0) + (1 if ada_lengkung else 0) \
            + (1 if kasar else 0) + (1 if len(bekas) >= 3 else 0)
        kesukaran = "Mudah" if skor <= 6 else "Sederhana" if skor <= 9 else "Sukar"
        g = m["gambar"]
        rows.append({
            "id": d["id"],
            "img": f"/_blob/{blobs[d['id']]}",
            "tema": TEMA[d["tema"]],
            "listing": LISTING[d["tema"]],
            "penjual": "ArtfulCraftsCreators",
            "ayat": ayat or "(tiada teks)",
            "bil_perkataan": len(ayat.split()),
            "bil_baris": len(lines),
            "kata_utama": ", ".join(l["teks"] for l in d["L"] if l["peranan"] == "H") or "–",
            "baris_json": json.dumps(lines, ensure_ascii=False),
            "jenis_font": ", ".join(jenis_font) or "–",
            "bil_font": len(jenis_font),
            "font_calon": "; ".join(calon) or "–",
            "ikon": "; ".join(f"{i['apa']} ({i['kedudukan']})" for i in d["I"]) or "Tiada",
            "bil_ikon": len(d["I"]),
            "peranan_ikon": ", ".join(peranan_ikon) or "–",
            "bekas": ", ".join(bekas) or "Tiada",
            "bil_bekas": len(bekas),
            "hiasan": ", ".join(d["O"]) or "Tiada",
            "bil_hiasan": len(d["O"]),
            "susunan": SUSUNAN[d["susunan"]],
            "siluet": SILUET[d["siluet"]],
            "simetri": "Tidak" if taksim else "Ya",
            "senget": "Ya" if senget else "Tidak",
            "lengkung": "Ya" if ada_lengkung else "Tidak",
            "tekstur": "Kasar" if kasar else "Bersih",
            "lebar_px": m["lebar_px"],
            "tinggi_px": m["tinggi_px"],
            "nisbah": m["nisbah"],
            "dakwat_pct": m["dakwat_pct"],
            "rasa": d["M"].get("rasa", "–"),
            "khalayak": d["M"].get("khalayak", "–"),
            "isu_ayat": d["M"].get("isu", ""),
            "skor_tiru": skor,
            "kesukaran": kesukaran,
            "status": "Belum diuji",
            "nota": d["M"].get("nota", ""),
            "fail_asal": FAIL[g] + (f" (ulangan: {ULANGAN[g]})" if g in ULANGAN else ""),
            "kedudukan": f"baris {m['baris']}, lajur {m['lajur']}",
            "dikemas": DIKEMAS,
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
    print(f"{len(rows)} design, {len(listing)} listing, {len(fonts)} baris font -> {OUT}")


if __name__ == "__main__":
    main()
