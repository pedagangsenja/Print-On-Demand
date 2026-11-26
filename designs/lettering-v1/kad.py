"""Standard Lettering v1: Kad Gaya (langkah 1), Spesifikasi Teks (langkah 2) dan pembina prompt (langkah 3).

5 kad daripada upload pengguna 25 Nov 2026 (design orang lain = rujukan gaya sahaja; ayat, susun atur tepat,
tandatangan dan logo tidak disalin). Setiap ciri = pasangan semakan QC (BM, ya / tidak) + frasa prompt (EN).
Peraturan v1 (keputusan pengguna 26 Nov 2026): AI jana HITAM PUTIH dahulu (dakwat putih atas latar hitam).
Warna C diletak oleh skrip kemasan selepas QC ejaan, ayat dan gaya lulus. Mod lalai pembina = "hp".
Mod "warna" (nama warna dalam prompt) dikekalkan hanya untuk mengulang ujian lama (prompts.json, AI Image Test 2).

Guna: python3 kad.py prompts_hp.json          -> prompt hitam putih (lalai) + semakan automatik
      python3 kad.py prompts.json warna       -> prompt berwarna lama (pembina v1.0)
"""
import json
import re
import sys

VERSI_PEMBINA = "v1.1"
TAIL = ("No other text, no letters except the quoted words, no signature, no watermark, no logo, "
        "no frame, no border, no mockup, flat graphic artwork.")

# Langkah 2: Spesifikasi Teks. Ayat sama untuk semua kad (seragam). Baris: (teks, peranan).
AYAT = {
    "P": dict(nama="pendek", laluan=1, ayat="Brave Hearts Begin Again",
              baris=[("Brave", "sokongan"), ("Hearts", "utama"), ("Begin", "sokongan"), ("Again", "utama")]),
    "D": dict(nama="sederhana", laluan=2, ayat="Every Small Step Builds a Bolder You",
              baris=[("Every Small", "sokongan"), ("Step", "utama"), ("Builds a", "penyambung"),
                     ("Bolder", "utama"), ("You", "sokongan")]),
    "L": dict(nama="panjang", laluan=3, ayat="Keep Showing Up on Hard Days Because Better Mornings Are Coming",
              baris=[("Keep Showing Up", "utama"), ("on hard days", "sokongan"), ("because", "penyambung"),
                     ("Better Mornings", "utama"), ("are coming", "penyambung")]),
}

# Langkah 1: Kad Gaya. huruf[peranan] = (kes, frasa bentuk huruf, nama warna untuk prompt)
KAD = {
    "K1": dict(
        nama="Skrip swash tebal bertaut (putih atas hitam)", ref="IMG_5818", snc="baharu",
        kelas="F2", dakwat=1, ruang_tepi=14, tekstur="grain halus", julat="4-8 perkataan",
        warna=dict(latar=("hitam", "#0c0c0c", "black"), dakwat=[("putih", "#f2f2ee", "white")]),
        medium="Bold hand-lettered script typography poster, portrait.",
        latar="Solid black background with a very subtle fine fabric grain.",
        susunan=("All words are stacked into one tight egg-shaped oval lockup in the center; lines interlock and slant to the right."),
        huruf={"utama": ("title", "very large heavy connected brush script with big looping capitals", "white"),
               "sokongan": ("title", "large heavy connected brush script", "white"),
               "penyambung": ("lower", "small heavy brush script", "white")},
        hierarki="Small words sit in the gaps between the large words.",
        hiasan="Thick curling swash tails fill the empty spaces around the oval; soft dark shadow under the strokes.",
        margin="Wide empty black margins.",
        larangan="White on black only, no other colors, no outline.",
        risiko=["swash boleh jadi huruf rawak", "skrip Huruf Awal: kadar salah ejaan lebih tinggi"],
        jangan_salin=["ayat The smarter you get the less you speak", "susunan baris tepat rujukan"],
        qc=[("Semua perkataan dalam skrip berus tebal bersambung", True),
            ("Keseluruhan teks membentuk satu blok bujur (oval)", True),
            ("Ekor swash bergulung keluar daripada huruf dan mengisi ruang kosong", True),
            ("Perkataan kecil diselit di celah perkataan besar", False),
            ("Putih satu warna atas hitam", False),
            ("Huruf condong ke kanan", False),
            ("Baris rapat dan bertindih / bertaut", False),
            ("Bayang lembut di bawah garisan huruf", False)]),
    "K2": dict(
        nama="Blok sans pekat lusuh + jalur kuning", ref="IMG_5792", snc="baharu",
        kelas="F2", dakwat=3, ruang_tepi=8, tekstur="grunge lusuh sederhana", julat="3-8 perkataan",
        warna=dict(latar=("hitam", "#0a0a0a", "black"),
                   dakwat=[("putih lusuh", "#ecebe6", "white"), ("kuning mustard", "#e0a526", "mustard yellow"),
                           ("hitam atas kuning", "#0a0a0a", "black")]),
        medium="Bold distressed typographic quote poster, portrait.",
        latar="Solid black background.",
        susunan="A thin mustard yellow bar across the top; below it every line is stretched to the same full width, forming one tight justified block.",
        huruf={"utama": ("upper", "heavy condensed bold sans-serif capitals in black inside a full-width solid mustard yellow box", "black"),
               "sokongan": ("upper", "heavy condensed bold sans-serif capitals", "white"),
               "penyambung": ("upper", "heavy condensed bold sans-serif capitals", "white")},
        hierarki="All lines share the same width, so shorter lines have taller letters.",
        hiasan="No icons, no illustrations.",
        margin="Moderate black margins on all sides.",
        larangan="Gritty grunge texture on the white letters and yellow boxes. Only white, mustard yellow and black. No outline, no shadow.",
        risiko=["perkataan dalam jalur kuning boleh jadi putih, bukan hitam"],
        jangan_salin=["ayat Sometimes later becomes never", "noktah besar selepas perkataan akhir"],
        qc=[("Semua huruf besar sans pekat sempit", True),
            ("Setiap baris sama lebar (blok rata kiri-kanan)", True),
            ("Perkataan utama hitam dalam kotak kuning penuh lebar", True),
            ("Tekstur lusuh grunge pada putih dan kuning", False),
            ("Jalur kuning nipis di bahagian atas", False),
            ("Tiada condong atau lengkung", False),
            ("Jarak baris rapat", False),
            ("Hanya putih, kuning dan hitam", False)]),
    "K3": dict(
        nama="Campuran sans kuning + skrip putih + label", ref="IMG_5775", snc="baharu",
        kelas="F1", dakwat=3, ruang_tepi=12, tekstur="tiada", julat="4-8 perkataan",
        warna=dict(latar=("hitam", "#0b0b0b", "black"),
                   dakwat=[("kuning keemasan", "#f5b51c", "golden yellow"), ("putih", "#f7f7f5", "white"),
                           ("kelabu bayang", "#3a3a3a", "dark gray")]),
        medium="Modern mixed-font hand-lettering quote poster, flat vector, portrait.",
        latar="Solid black background.",
        susunan="Centered stacked lines of different sizes, alternating between two lettering styles; the top line is gently arched.",
        huruf={"utama": ("upper", "huge heavy rounded bold sans-serif capitals", "golden yellow"),
               "sokongan": ("title", "large bold brush script with a dark gray drop shadow", "white"),
               "penyambung": ("upper", "small bold sans-serif capitals in black inside a small golden yellow "
                                       "rectangular label", "black")},
        hierarki="Strong size contrast: sans lines biggest, script lines large, labels small.",
        hiasan="A few short golden yellow sparkle strokes beside the top line and next to one script word.",
        margin="Generous black margins.",
        larangan="Only golden yellow, white, dark gray and black. No gradient, no texture.",
        risiko=["label berteks boleh menambah huruf rawak", "warna bertukar antara peranan"],
        jangan_salin=["ayat Success grows where excuses end"],
        qc=[("Baris berselang: sans tebal kuning dan skrip putih", True),
            ("Perkataan penyambung dalam label kotak kuning kecil", True),
            ("Kontras saiz kuat antara baris", True),
            ("Skrip putih ada bayang gelap", False),
            ("Garis percikan kecil kuning di sisi", False),
            ("Baris atas sans sedikit melengkung", False),
            ("Latar hitam rata, tiada tekstur", False),
            ("Maksimum 3 warna dakwat", False)]),
    "K4": dict(
        nama="Serif vintaj dekoratif + hiasan bertitik (krim atas hitam)", ref="IMG_5764", snc="baharu",
        kelas="F2", dakwat=1, ruang_tepi=12, tekstur="lusuh cetakan", julat="4-12 perkataan",
        warna=dict(latar=("hitam arang", "#1b1918", "charcoal black"), dakwat=[("krim", "#eadfcb", "cream")]),
        medium="Vintage Victorian hand-lettered typographic poster, portrait.",
        latar="Solid charcoal black background with tiny scattered cream specks.",
        susunan=("A tall centered column of lines; lines are separated by thin ornamental rules made of "
                 "dotted lines and small curled scrolls."),
        huruf={"utama": ("upper", "very large decorative vintage serif capitals with an oversized first letter "
                                  "and slightly playful letter heights", "cream"),
               "sokongan": ("upper", "medium decorative vintage serif capitals", "cream"),
               "penyambung": ("upper", "small serif capitals tucked between the ornamental rules", "cream")},
        hierarki="Main lines are much larger than the small connecting words.",
        hiasan="Symmetrical Victorian flourish ornaments above the top line and below the bottom line.",
        margin="Wide empty margins.",
        larangan="Worn distressed print texture on the letters. Cream on black only, one ink color.",
        risiko=["model meniru logo / tandatangan di bawah", "huruf awal besar boleh tersalah eja"],
        jangan_salin=["logo landasan besi dan nama jenama di bawah", "tanda (R)", "ayat rujukan"],
        qc=[("Serif vintaj dekoratif huruf besar", True),
            ("Baris dipisah garis hiasan bertitik dan gulungan", True),
            ("Hiasan flourish simetri di atas dan di bawah", True),
            ("Huruf pertama perkataan utama lebih besar", False),
            ("Tekstur lusuh pada huruf", False),
            ("Satu warna krim atas hitam", False),
            ("Percikan titik kecil di latar", False),
            ("Lajur tegak di tengah", False)]),
    "K5": dict(
        nama="Blok huruf tangan lusuh (S005)", ref="IMG_5730", snc="S005 sedia ada (rujukan sama); kad ditambah",
        kelas="F2", dakwat=1, ruang_tepi=10, tekstur="kapur lusuh", julat="3-8 perkataan",
        warna=dict(latar=("hitam", "#0a0a0a", "black"), dakwat=[("putih pudar", "#f1f2ed", "white")]),
        medium="Hand-drawn typographic quote poster, portrait.",
        latar="Solid black background.",
        susunan=("The lines form one tight rectangular block; every line is stretched to the same width and the "
                 "letters of neighbouring lines touch and interlock."),
        huruf={"utama": ("upper", "chunky bold hand-drawn capitals with a bouncy uneven baseline", "white"),
               "sokongan": ("upper", "chunky bold hand-drawn capitals with a bouncy uneven baseline", "white"),
               "penyambung": ("lower", "smaller bouncy hand-drawn lowercase letters squeezed in", "white")},
        hierarki="Main lines are the largest; small lowercase words fill the gaps.",
        hiasan="Some letters end in long playful tails that hook under the next letters.",
        margin="Wide black margins.",
        larangan="Rough chalky distressed texture on the white letters. White on black only.",
        risiko=["huruf bertaut boleh menggabung perkataan"],
        jangan_salin=["ayat Catch your breath take your time"],
        qc=[("Huruf tangan tebal dengan garis dasar melantun", True),
            ("Baris sama lebar membentuk satu blok rapat", True),
            ("Huruf antara baris bersentuh / bertaut", True),
            ("Perkataan kecil huruf kecil diselit", False),
            ("Tekstur kapur lusuh", False),
            ("Putih satu warna atas hitam", False),
            ("Ekor huruf memanjang", False),
            ("Tiada hiasan lain", False)]),
    "K6": dict(
        nama="Skrip berus tirus + swash reben + bintik bintang (putih atas hitam)", ref="IMG_5734", snc="baharu",
        kelas="F2", dakwat=1, ruang_tepi=10, tekstur="butir berus kering halus", julat="4-8 perkataan",
        warna=dict(latar=("hitam", "#0a0a0a", "black"), dakwat=[("putih", "#f4f4f0", "white")]),
        medium="Hand-lettered brush calligraphy poster, portrait.",
        latar="Solid black background with a few tiny white star dots.",
        susunan=("All lines are stacked into one tall centered block of equal-width lines that interlock and "
                 "rise slightly to the right."),
        huruf={"utama": ("title", "large flowing brush calligraphy script with thick downstrokes, thin "
                                  "upstrokes and looping capitals", "white"),
               "sokongan": ("title", "flowing connected brush script", "white"),
               "penyambung": ("lower", "small lowercase brush script", "white")},
        hierarki="Large words span the full block width; small words tuck in beside them.",
        hiasan=("Long ribbon-like swashes curl above the first line and below the last line; swash tails fill "
                "the gaps; dry-brush grain in the white strokes."),
        margin="Moderate black margins.",
        larangan="White on black only, no other colors, no outline.",
        risiko=["swash boleh dibaca sebagai huruf tambahan", "bintik bintang boleh jadi titik huruf rawak",
                "skrip huruf kecil bersambung: salah ejaan lebih tinggi"],
        jangan_salin=["ayat Master your mind master your life", "struktur ayat berulang", "susunan baris tepat rujukan"],
        qc=[("Skrip berus bersambung: garisan turun tebal, garisan naik halus", True),
            ("Semua baris membentuk satu blok tegak sama lebar di tengah", True),
            ("Swash panjang seperti reben di atas baris pertama dan di bawah baris akhir", True),
            ("Ekor swash keluar dari huruf akhir dan mengisi celah", False),
            ("Tekstur berus kering / butir dalam garisan putih", False),
            ("Bintik bintang putih kecil di latar", False),
            ("Huruf condong ke kanan, baris naik sedikit ke kanan", False),
            ("Putih satu warna atas hitam", False)]),
}


def kes(teks, k):
    return {"upper": teks.upper(), "lower": teks.lower(), "title": teks.title()}[k]


ORD = ["first", "second", "third", "fourth", "fifth", "sixth"]
LABEL = {"utama": "large", "sokongan": "medium", "penyambung": "small"}


WARNA_LAIN = re.compile(r"\b(?:(?:golden|mustard|dark|light|pale|warm|deep|bright|antique|charcoal) )*"
                        r"(yellow|gold|golden|mustard|cream|ivory|beige|gray|grey|red|orange|pink|blue|navy|green|"
                        r"teal|purple|brown|tan|silver)\b", re.I)


def hitam_putih(teks, k):
    """Tukar frasa kad kepada hitam putih: semua dakwat = white, latar = black, tiada kelabu, tiada bayang."""
    teks = re.sub(r",? with an? [a-z ]*\b(?:gray|grey)\b[a-z ]*shadow", "", teks)
    teks = re.sub(r"Only [^.]*\.\s*", "", teks)
    nama = {w[2] for w in k["warna"]["dakwat"]} | {k["warna"]["latar"][2]}
    for n in sorted(nama - {"white", "black"}, key=len, reverse=True):
        ganti = "black" if "black" in n else "white"
        teks = teks.replace(n, ganti).replace(n.capitalize(), ganti.capitalize())
    teks = WARNA_LAIN.sub("white", teks)
    return re.sub(r"\b(white|black)(?:,? (?:and )?\1\b)+", r"\1", teks, flags=re.I)


def bina(kid, aid, drop=(), mod="hp"):
    """Rangka 9 bahagian. Bentuk huruf setiap peranan diterangkan sekali; setiap baris hanya membawa label peranan.
    mod="hp" (lalai): hitam putih sahaja. mod="warna": nama warna kad masuk prompt (pembina v1.0, ujian lama)."""
    k, a = KAD[kid], AYAT[aid]
    if mod == "hp":
        k = dict(k, huruf={r: (kes_, hitam_putih(f, k), "black" if w == "black" else "white")
                           for r, (kes_, f, w) in k["huruf"].items()},
                 **{f: hitam_putih(k[f], k) for f in ("medium", "latar", "susunan", "hierarki", "hiasan", "margin",
                                                      "larangan")})
        if "on black only" not in k["larangan"].lower():  # kad satu dakwat sudah ada had ini; prompt kekal seperti diuji
            k["larangan"] = (k["larangan"].strip() + " Black and white only, no gray" +
                             ("." if "no shadow" in k["larangan"].lower() else ", no shadow.")).strip()
    n = len(a["baris"])
    used = [r for r in ("utama", "sokongan", "penyambung") if any(r == b[1] for b in a["baris"])]
    gaya = " ".join(f"{LABEL[r].capitalize()} words: {k['huruf'][r][1]}" +
                    ("" if k["huruf"][r][2] in k["huruf"][r][1] else f", {k['huruf'][r][2]}") + "." for r in used)
    lines, quotes = [], []
    for i, (t, r) in enumerate(a["baris"]):
        q = kes(t, k["huruf"][r][0])
        quotes.append(q)
        lines.append(f'{ORD[i]} line "{q}" ({LABEL[r]})')
    words = ["one", "two", "three", "four", "five", "six"][n - 1]
    teks = f"The text reads exactly, {words} lines: " + ", ".join(lines) + "."
    parts = [("medium", k["medium"]), ("latar", k["latar"]), ("susunan", k["susunan"]), ("teks", teks),
             ("gaya", gaya), ("hierarki", k["hierarki"]), ("hiasan", k["hiasan"]), ("margin", k["margin"]),
             ("larangan", k["larangan"]), ("tail", TAIL)]
    return " ".join(v for n, v in parts if n not in drop), quotes


def semak(prompt, quotes, spec, mod="hp"):
    err = []
    if mod == "hp" and WARNA_LAIN.search(re.sub(r'"[^"]*"|no gray', "", prompt)):
        err.append("ada nama warna selain black / white: " + WARNA_LAIN.search(re.sub(r'"[^"]*"|no gray', "", prompt)).group(0))
    for q in quotes:
        if prompt.count(f'"{q}"') != 1:
            err.append(f"petikan {q!r} bukan sekali")
    if " ".join(quotes).lower().split() != spec.lower().split():
        err.append("petikan tidak sama dengan Spesifikasi Teks")
    if re.search(r"#[0-9a-fA-F]{3,6}|\d", prompt):
        err.append("ada angka / hex")
    if len(prompt.split()) > 170:
        err.append("terlalu panjang")
    return err


def main(out, mod="hp"):
    rows = []
    for kid in KAD:
        for aid in AYAT:
            p, q = bina(kid, aid, mod=mod)
            e = semak(p, q, AYAT[aid]["ayat"], mod)
            rows.append(dict(id=f"{kid}{aid}", kad=kid, ayat=aid, laluan=AYAT[aid]["laluan"], prompt=p, petikan=q,
                             kata=len(p.split()), pembina=VERSI_PEMBINA if mod == "hp" else "v1.0", mod=mod,
                             w=768, h=1024, semak=e or "lulus"))
            if e:
                print(kid, aid, e)
    json.dump(rows, open(out, "w"), indent=1, ensure_ascii=False)
    print(len(rows), "prompt;", "kata min/maks", min(r["kata"] for r in rows), max(r["kata"] for r in rows))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "hp")
