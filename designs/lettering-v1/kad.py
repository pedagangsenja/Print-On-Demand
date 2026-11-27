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
    # 26 Nov 2026: ayat baharu untuk kad K3 (dipilih pengguna); hanya dijana dengan K3 (id K3W).
    "W": dict(nama="sederhana", laluan=2, ayat="Winners Act While Others Wait",
              baris=[("Winners", "utama"), ("Act", "sokongan"), ("While", "penyambung"), ("Others", "sokongan"),
                     ("Wait", "utama")]),
    # 26 Nov 2026: ayat dipilih Claude (pengguna serah pilihan) untuk ujian 6 model pada kad K3 (id K3H).
    # Kesukaran: 5 perkataan, 1 perkataan 7+ huruf (Patience, dijadikan utama), tiada perkataan berulang.
    "H": dict(nama="sederhana", laluan=2, ayat="Patience Builds What Hurry Breaks",
              baris=[("Patience", "utama"), ("Builds", "sokongan"), ("What", "penyambung"), ("Hurry", "sokongan"),
                     ("Breaks", "utama")]),
    # 26 Nov 2026 (malam): tiga ayat baharu untuk ujian v1.2 pada tiga gambar upload; cadangan Claude, diluluskan
    # pengguna. Setiap ayat dijana dengan SATU kad sahaja: K (K3, id K3K), M (K7, id K7M), G (K8, id K8G).
    "K": dict(nama="sederhana", laluan=2, ayat="Kindness Stays After Words Fade",
              baris=[("Kindness", "utama"), ("Stays", "sokongan"), ("After", "penyambung"), ("Words", "sokongan"),
                     ("Fade", "utama")]),
    "M": dict(nama="pendek", laluan=1, ayat="Make Room for Wonder",
              baris=[("Make", "sokongan"), ("Room", "utama"), ("for", "penyambung"), ("Wonder", "utama")]),
    "G": dict(nama="sederhana", laluan=2, ayat="Keep Going You Are Almost There",
              baris=[("Keep Going", "sokongan"), ("You Are", "penyambung"), ("Almost", "utama"), ("There", "sokongan")]),
    # Kitaran QC pusingan 1 (26 Nov 2026), MOSS x K8 sahaja: 'ALMOST' salah eja pada 3/3 seed. Ubahan tunggal ikut
    # jadual kitaran QC: tukar peranan perkataan itu (Almost: utama -> sokongan; There: sokongan -> utama). Ayat sama.
    # Keputusan: TIDAK berjaya ('ALMiST' 3/3). Disimpan sebagai rekod imej raw/v12-cpu-p1/moss sahaja.
    "J": dict(nama="sederhana", laluan=2, ayat="Keep Going You Are Almost There",
              baris=[("Keep Going", "sokongan"), ("You Are", "penyambung"), ("Almost", "sokongan"), ("There", "utama")]),
    # 27 Nov 2026: enam ayat baharu untuk ujian v1.2 pada enam gambar upload (IMG_5845, 5846, 5840, 5792, 5793, 5764);
    # dipilih Claude (pengguna serah pilihan). Setiap ayat dijana dengan SATU kad sahaja: A (K9), B (K10), C (K11),
    # E (K2), F (K12), Q (K4). Ayat rujukan tidak disalin.
    "A": dict(nama="sederhana", laluan=2, ayat="Strong Moms Raise Brave Kids",
              baris=[("Strong", "sokongan"), ("Moms", "utama"), ("Raise", "utama"), ("Brave Kids", "sokongan")]),
    "B": dict(nama="sederhana", laluan=2, ayat="Every Single Day Spreading Kindness Teacher Life",
              baris=[("Every Single Day", "penyambung"), ("Spreading", "sokongan"), ("Kindness", "utama"),
                     ("Teacher Life", "penyambung")]),
    "C": dict(nama="pendek", laluan=1, ayat="Trust Your Timing",
              baris=[("Trust", "utama"), ("Your", "sokongan"), ("Timing", "utama")]),
    "E": dict(nama="pendek", laluan=1, ayat="Comfort Zones Kill Dreams",
              baris=[("Comfort", "sokongan"), ("Zones", "sokongan"), ("Kill", "sokongan"), ("Dreams", "utama")]),
    "F": dict(nama="sederhana", laluan=2, ayat="Build Your Habits Not Your Excuses",
              baris=[("Build Your", "sokongan"), ("Habits", "utama"), ("Not Your", "sokongan"), ("Excuses", "sokongan")]),
    "Q": dict(nama="sederhana", laluan=2, ayat="Quiet Work Builds Loud Results",
              baris=[("Quiet Work", "sokongan"), ("Builds", "penyambung"), ("Loud", "utama"), ("Results", "utama")]),
}

# Langkah 1: Kad Gaya. huruf[peranan] = (kes, frasa bentuk huruf, nama warna untuk prompt)
KAD = {
    "K1": dict(
        nama="Skrip swash tebal bertaut (putih atas hitam)", ref="IMG_5818", snc="S007 + C003 (didaftar 26 Nov 2026)",
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
        nama="Blok sans pekat lusuh + jalur kuning", ref="IMG_5792", snc="S008 + C007 (didaftar 26 Nov 2026)",
        kelas="F2", dakwat=3, ruang_tepi=8, tekstur="grunge lusuh sederhana", julat="3-8 perkataan",
        peta_warna=dict(utama=1, sokongan=0, penyambung=0, hiasan=1),   # kotak kuning, huruf putih, jalur atas kuning
        skrip_kemasan=["SK07", "SK06"],
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
        nama="Campuran sans kuning + skrip putih + label", ref="IMG_5775", snc="S009 + C008 (didaftar 26 Nov 2026)",
        versi="v1.2 (26 Nov 2026: kajian semula IMG_5775, diluluskan pengguna)",
        kelas="F1", dakwat=3, ruang_tepi=15, tekstur="tiada", julat="4-8 perkataan",
        warna=dict(latar=("hitam", "#0b0b0b", "black"),
                   dakwat=[("kuning keemasan", "#f5b51c", "golden yellow"), ("putih", "#f7f7f5", "white"),
                           ("kelabu bayang cerah", "#b2b3b5", "light gray")]),
        # 27 Nov 2026: kelabu bayang diukur SK08 --ukur pada IMG_5775 (#b2b3b5). Sebelum itu #3a3a3a "di bawah /
        # kanan skrip" = tekaan tanpa ukuran; gambar upload menunjukkan kelabu CERAH di DALAM huruf.
        kemasan=("Bayang 3D dalam huruf: bahagian bawah setiap strok skrip putih berwarna kelabu cerah (SK08); "
                 "AI tidak menjananya. Warna ikut peranan oleh SK07."),
        peta_warna=dict(utama=0, sokongan=1, penyambung=0, hiasan=0, bayang=2),   # peranan -> nombor dakwat (SK07)
        skrip_kemasan=["SK07", "SK08", "SK06"],
        medium="Modern mixed-font hand-lettering quote poster, flat vector, portrait.",
        latar="Solid black background.",
        susunan=("One tight centered block of lines alternating two lettering styles; lines touch and slightly "
                 "overlap; the whole block is tilted slightly so every line rises to the right."),
        huruf={"utama": ("upper", "huge heavy condensed bold sans-serif capitals", "golden yellow"),
               "sokongan": ("title", "large bold flowing brush script, big looping capitals, with a dark gray "
                                     "drop shadow", "white"),
               "penyambung": ("upper", "small bold sans-serif capitals in black inside a small golden yellow "
                                       "rectangular label", "black")},
        hierarki="Sans lines frame the top and the bottom; the bottom line is the tallest; the label is small.",
        hiasan="Three short golden yellow sparkle strokes on each side of the label line.",
        margin="Wide black margins.",
        larangan="Only golden yellow, white, dark gray and black. No gradient, no texture.",
        risiko=["label berteks boleh menambah huruf rawak", "warna bertukar antara peranan",
                "baris bertindih boleh menutup huruf", "blok condong boleh memotong huruf di tepi"],
        jangan_salin=["ayat Success grows where excuses end", "susunan perkataan rujukan (kata kerja + WHERE)"],
        qc=[("Sans tebal huruf besar di baris atas dan baris bawah mengapit baris skrip", True),
            ("Perkataan penyambung dalam label kotak kecil, huruf gelap atas kotak", True),
            ("Baris tengah skrip berus tebal bersambung, huruf awal besar bergelung", True),
            ("Kontras saiz kuat; baris sans bawah paling besar", False),
            ("Seluruh blok condong naik ke kanan", False),
            ("Baris rapat, bersentuh atau bertindih sedikit", False),
            ("Garis percikan kecil di sisi kiri dan kanan baris label", False),
            ("Latar hitam rata, tiada tekstur, ruang tepi luas", False)]),
    "K3_lama": dict(  # v1.0 (26 Nov 2026) disimpan untuk mengulang ujian lama sahaja
        nama="Campuran sans kuning + skrip putih + label (v1.0)", ref="IMG_5775", snc="S009 + C008",
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
        nama="Serif vintaj dekoratif + hiasan bertitik (krim atas hitam)", ref="IMG_5764", snc="S010; warna hampir C002 (didaftar 26 Nov 2026)",
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
        nama="Skrip berus tirus + swash reben + bintik bintang (putih atas hitam)", ref="IMG_5734", snc="S011 + C003 (didaftar 26 Nov 2026)",
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
    # K7, K8: dibuat Claude 26 Nov 2026 (malam) daripada upload pengguna; diluluskan pengguna 27 Nov 2026.
    # Ruang tepi dan condong diukur skrip SK05.
    "K7": dict(
        nama="Skrip berus kontras + huruf kecil besar + swash bawah (krim atas hitam)", ref="IMG_5765",
        snc="S023-S031 + C009 (didaftar 27 Nov 2026)", versi="v1.0 (26 Nov 2026; diluluskan pengguna 27 Nov 2026)",
        kelas="F2", dakwat=1, ruang_tepi=6, tekstur="butir cetakan halus", julat="3-6 perkataan",
        warna=dict(latar=("hitam", "#0c0c0c", "black"), dakwat=[("krim", "#ece6d8", "white")]),
        medium="Hand-lettered script quote poster, portrait.",
        latar="Solid black background.",
        susunan=("All lines are stacked into one tight centered block; the lines nest closely and the whole block "
                 "rises clearly to the right."),
        huruf={"utama": ("title", "very large bold flowing brush script with thick and thin strokes and big swash capitals", "white"),
               "sokongan": ("title", "large bold flowing brush script with a swash capital", "white"),
               "penyambung": ("upper", "small bold sans-serif capitals with wide letter spacing", "white")},
        hierarki="Script words are large; the small capital words sit in the gaps between them.",
        hiasan="One long flourish swash sweeps under the last line; curled swash tails extend from the first and last letters.",
        margin="Moderate black margins.",
        larangan="Subtle fine print grain in the white letters. White on black only, no other colors, no outline.",
        risiko=["swash boleh dibaca sebagai huruf tambahan", "skrip bersambung: salah ejaan lebih tinggi",
                "perkataan kecil boleh hilang atau berulang"],
        jangan_salin=["enam ayat rujukan (Stay hungry stay foolish dan lain-lain)", "susunan baris tepat rujukan"],
        qc=[("Perkataan utama dalam skrip berus tebal bersambung, kontras tebal nipis", True),
            ("Perkataan penyambung dalam huruf besar kecil tanpa kait, jarak huruf lebar", True),
            ("Satu swash panjang di bawah baris akhir", True),
            ("Huruf awal besar dengan swash", False),
            ("Blok rapat di tengah, baris bersarang", False),
            ("Baris naik jelas ke kanan", False),
            ("Butir cetakan halus pada huruf", False),
            ("Satu warna cerah atas hitam", False)]),
    "K8": dict(
        nama="Berus marker melantun tebal + bintik latar (putih atas hitam)", ref="IMG_5735",
        snc="S032-S035 + C010 (didaftar 27 Nov 2026)", versi="v1.0 (26 Nov 2026; diluluskan pengguna 27 Nov 2026)",
        kelas="F2", dakwat=1, ruang_tepi=12, tekstur="tepi marker kering + butir latar", julat="4-7 perkataan",
        warna=dict(latar=("hitam arang", "#1f1f1f", "black"), dakwat=[("putih", "#f3f3f1", "white")]),
        medium="Hand-drawn brush lettering quote poster, portrait.",
        latar="Solid black background with a few small scattered white dots.",
        susunan=("All lines are stacked into one tight centered block; the lines sit close together and the whole "
                 "block tilts so each line rises to the right."),
        huruf={"utama": ("upper", "very large thick round brush-marker capitals with a bouncy uneven baseline", "white"),
               "sokongan": ("upper", "large thick round brush-marker capitals with a bouncy uneven baseline", "white"),
               "penyambung": ("lower", "smaller thick round brush-marker lowercase letters", "white")},
        hierarki="One word is clearly the largest; the small words tuck in tightly.",
        hiasan="No swashes, no icons.",
        margin="Wide empty black margins.",
        larangan="Slightly rough dry-marker edges on the white letters. White on black only, no other colors, no outline.",
        risiko=["huruf melantun boleh menukar huruf besar / kecil", "bintik latar boleh jadi titik huruf rawak",
                "baris rapat boleh menggabung perkataan"],
        jangan_salin=["ayat We'll make this dream come true", "susunan baris tepat rujukan"],
        qc=[("Huruf marker berus tebal, hujung bulat, satu ketebalan", True),
            ("Garis dasar melantun, saiz huruf tidak sekata", True),
            ("Satu perkataan paling besar di tengah blok", True),
            ("Blok rapat, baris hampir bersentuh", False),
            ("Seluruh blok condong naik ke kanan", False),
            ("Bintik putih kecil bertabur di latar", False),
            ("Tepi huruf sedikit kasar (marker kering)", False),
            ("Putih satu warna atas hitam, tiada swash", False)]),
    "K9": dict(
        nama="Skrip melantun + sans bulat pekat + hati bertabur (putih atas hitam)", ref="IMG_5845",
        snc="belum didaftar", versi="v1.0 (27 Nov 2026; belum diluluskan pengguna)",
        kelas="F1", dakwat=1, ruang_tepi=4, tekstur="tiada", julat="4-7 perkataan",
        warna=dict(latar=("hitam", "#000000", "black"), dakwat=[("putih", "#ffffff", "white")]),
        medium="Playful hand-lettered quote poster, portrait.",
        latar="Solid black background with small white hearts scattered on both sides of the text.",
        susunan="All lines are stacked into one tight centered block; the lines sit close together and stay level.",
        huruf={"utama": ("upper", "huge heavy rounded bold sans-serif capitals", "white"),
               "sokongan": ("title", "large bold bouncy connected script with a looping capital", "white"),
               "penyambung": ("lower", "small bold bouncy connected script", "white")},
        hierarki="The capital words are the widest lines; the script lines are slightly narrower.",
        hiasan="Small white hearts are scattered on the left and right of the block, and one long swash tail sweeps under the last line.",
        margin="Narrow black margins at the sides, wider at the top and bottom.",
        larangan="Flat clean white on black only, no outline, no shadow, no texture.",
        risiko=["hati boleh jadi titik huruf i atau huruf rawak", "skrip bersambung: salah ejaan lebih tinggi",
                "huruf besar bulat boleh bercantum"],
        jangan_salin=["ayat Having a weird mom builds character", "titik i berbentuk hati", "susunan baris tepat rujukan"],
        qc=[("Perkataan utama dalam sans bulat pekat huruf besar", True),
            ("Perkataan sokongan dalam skrip melantun bersambung", True),
            ("Hati putih kecil bertabur di kiri dan kanan blok", True),
            ("Swash panjang di bawah baris akhir", False),
            ("Blok rapat di tengah, baris lurus", False),
            ("Baris huruf besar paling lebar", False),
            ("Rata bersih tanpa tekstur", False),
            ("Satu warna putih atas hitam", False)]),
    "K10": dict(
        nama="Lencana bulat: teks lengkung sans + skrip berus tengah + bintang (putih atas hitam)", ref="IMG_5846",
        snc="belum didaftar", versi="v1.0 (27 Nov 2026; belum diluluskan pengguna)",
        kelas="F1", dakwat=1, ruang_tepi=8, tekstur="tiada", julat="5-8 perkataan",
        warna=dict(latar=("hitam", "#000000", "black"), dakwat=[("putih", "#ffffff", "white")]),
        medium="Round badge typography design, portrait.",
        latar="Solid black background.",
        susunan=("One round badge: the first line curves along the top of an invisible circle, the last line curves "
                 "along the bottom of the circle, and the middle lines sit straight in the center."),
        huruf={"utama": ("title", "huge flowing brush script with tall loops", "white"),
               "sokongan": ("title", "medium thin brush script", "white"),
               "penyambung": ("upper", "bold condensed sans-serif capitals following the curve", "white")},
        hierarki="The center script word is by far the largest; the curved lines are small.",
        hiasan="Small four-pointed sparkle stars are spaced around the inside of the circle, and two small hearts sit under the large word.",
        margin="Wide black margins around the round badge.",
        larangan="Flat clean white on black only, no outline, no circle line, no shadow.",
        risiko=["teks lengkung: ejaan dan jarak huruf mudah rosak", "bintang boleh jadi huruf rawak",
                "model boleh melukis garis bulatan"],
        jangan_salin=["ayat Today tomorrow and always / Making a difference / Healthcare squad", "logo dan teks SVG & PNG",
                      "tanda pagar"],
        qc=[("Baris pertama melengkung di atas, baris akhir melengkung di bawah", True),
            ("Perkataan utama skrip berus besar di tengah", True),
            ("Bintang empat bucu kecil di sekeliling", True),
            ("Teks lengkung dalam sans sempit huruf besar", False),
            ("Dua hati kecil di bawah perkataan utama", False),
            ("Tiada garis bulatan", False),
            ("Rata bersih tanpa tekstur", False),
            ("Satu warna putih atas hitam", False)]),
    "K11": dict(
        nama="Skrip berus tebal bertangga + swash ekor (putih atas hitam)", ref="IMG_5840",
        snc="belum didaftar", versi="v1.0 (27 Nov 2026; belum diluluskan pengguna)",
        kelas="F1", dakwat=1, ruang_tepi=11, tekstur="tiada", julat="2-4 perkataan",
        warna=dict(latar=("hitam", "#111111", "black"), dakwat=[("putih", "#ffffff", "white")]),
        medium="Hand-lettered script quote poster, portrait.",
        latar="Solid black background.",
        susunan="Each word sits on its own line, stacked into one tight centered block; the lines interlock and rise slightly to the right.",
        huruf={"utama": ("title", "very large bold connected brush script with thick and thin strokes and a big looping capital", "white"),
               "sokongan": ("title", "large bold connected brush script with thick and thin strokes", "white"),
               "penyambung": ("lower", "medium bold connected brush script", "white")},
        hierarki="All words are similar in size; the first and last words are the widest.",
        hiasan="Long curled swash tails extend from the first letter and from the last letter, and one swash underlines the last word.",
        margin="Moderate black margins.",
        larangan="Flat clean white on black only, no outline, no shadow, no texture.",
        risiko=["swash boleh dibaca sebagai huruf tambahan", "skrip bersambung: salah ejaan lebih tinggi"],
        jangan_salin=["ayat Know your worth", "susunan baris tepat rujukan"],
        qc=[("Skrip berus tebal bersambung, kontras tebal nipis", True),
            ("Satu perkataan satu baris, baris bertaut", True),
            ("Swash ekor panjang pada huruf pertama dan akhir", True),
            ("Swash di bawah perkataan akhir", False),
            ("Blok naik sedikit ke kanan", False),
            ("Saiz perkataan hampir sama", False),
            ("Rata bersih tanpa tekstur", False),
            ("Satu warna putih atas hitam", False)]),
    "K12": dict(
        nama="Blok sans sempit pekat calar + satu perkataan gergasi (hitam atas koral)", ref="IMG_5793",
        snc="belum didaftar", versi="v1.0 (27 Nov 2026; belum diluluskan pengguna)",
        kelas="F2", dakwat=1, ruang_tepi=15, tekstur="calar dan bintik lusuh kuat", julat="4-8 perkataan",
        warna=dict(latar=("koral", "#e06455", "coral red"), dakwat=[("hitam", "#0a0a0a", "black")]),
        medium="Bold distressed typographic quote poster, portrait.",
        latar="Solid black background.",
        susunan="One tight justified block: every line is stretched to the same full width and the lines almost touch.",
        huruf={"utama": ("upper", "gigantic ultra condensed heavy sans-serif capitals filling about half the block height", "white"),
               "sokongan": ("upper", "heavy condensed bold sans-serif capitals", "white"),
               "penyambung": ("upper", "heavy condensed bold sans-serif capitals", "white")},
        hierarki="All lines share the same width; the main word is far taller than every other line.",
        hiasan="No icons, no illustrations.",
        margin="Wide black margins on all sides.",
        larangan="Heavy scratched and speckled distressed texture on the letters, white on black only, no outline, no shadow.",
        risiko=["huruf sempit pekat boleh bercantum", "calar boleh dibaca sebagai huruf"],
        jangan_salin=["ayat Follow your plan not your mood", "tera air", "bingkai hitam di luar panel"],
        qc=[("Semua huruf besar sans sempit pekat", True),
            ("Setiap baris sama lebar (blok rata kiri-kanan)", True),
            ("Satu perkataan gergasi kira-kira separuh tinggi blok", True),
            ("Tekstur calar dan bintik lusuh pada huruf", False),
            ("Baris hampir bersentuh", False),
            ("Tiada condong", False),
            ("Ruang tepi lebar", False),
            ("Satu dakwat atas latar rata", False)]),
}


# v1.2 (26 Nov 2026): blok isi 3.2 (A-H) sebagai FRASA, hitam putih, untuk pembina ikut model (pembina.py).
# Diambil daripada kad di atas; tiada ciri baharu. Frasa disambung oleh aturan model, jadi tiada noktah di hujung.
# huruf[peranan]: penuh = sebutan pertama, ringkas = sebutan ulangan ("the same ..."); atau bekas + nama + dalam
# bagi perkataan yang duduk dalam bekas (label / kotak). sisi = hiasan di kiri dan kanan baris berbekas.
# hiasan_kotak = hiasan yang ada kotak sendiri (MOSS, FLUX 3 Klein): pada = atas / bawah blok.
# ukuran (piksel, kanvas 768x1024, lebar x tinggi): hanya K3 ada nilai contoh (khas.py, percubaan); kad lain pakai
# lalai pembina sehingga ukuran rujukan diukur daripada upload.
# rujukan = angka yang diukur skrip SK05 daripada gambar upload (sudut condong, ruang tepi); dipakai langkah 5b.
_SANS = dict(penuh="heavy condensed bold sans-serif capitals", ringkas="heavy condensed sans-serif capitals")
_K5 = dict(penuh="chunky bold hand-drawn capitals with a bouncy uneven baseline", ringkas="chunky hand-drawn capitals")
BLOK = {
    "K1": dict(
        medium="script typography poster", gaya="bold hand-lettered", latar_warna="solid black",
        latar_isi="a very subtle fine fabric grain", tepi="a soft dark shadow under the strokes",
        bentuk="one tight egg-shaped oval lockup", condong="slants to the right", sentuh="interlock",
        margin="wide empty black margins",
        huruf={"utama": dict(penuh="very large heavy connected brush script with big looping capitals",
                             ringkas="heavy connected brush script"),
               "sokongan": dict(penuh="large heavy connected brush script", ringkas="heavy connected brush script"),
               "penyambung": dict(penuh="small heavy brush script", ringkas="small heavy brush script")},
        tertinggi=None, hierarki="Small words sit in the gaps between the large words.",
        hiasan="Thick curling swash tails fill the empty spaces around the oval.", sisi=None, hiasan_kotak=[],
        tiada=["other colors", "outline"], ada="solid white strokes on a clean black background", sama_lebar=False),
    "K2": dict(
        medium="typographic quote poster", gaya="bold distressed", latar_warna="solid black", latar_isi=None,
        tepi="a gritty grunge texture",
        bentuk="one tight justified block in which every line is stretched to the same full width",
        condong=None, sentuh=None, margin="moderate black margins",
        huruf={"utama": dict(bekas="full-width solid white box", nama="box",
                             dalam="heavy condensed bold black sans-serif capitals"),
               "sokongan": _SANS, "penyambung": _SANS},
        tertinggi=None, hierarki="All lines share the same width, so shorter lines have taller letters.",
        hiasan="A thin white bar runs across the top, above the block.", sisi=None,
        hiasan_kotak=[dict(pada="atas", nama="bar", frasa="a thin solid white bar across the full width",
                           ayat="A thin white bar runs across the top, above the block")],
        tiada=["gray", "outline", "shadow"], ada="gritty textured fills on a clean black background",
        sama_lebar=True),
    "K3": dict(
        medium="hand-lettering quote poster", gaya="flat vector", latar_warna="solid black", latar_isi=None,
        tepi="crisp clean vector edges", bentuk="one tight block",
        condong="tilts slightly so each line rises toward the right", sentuh="touch and slightly overlap",
        margin="wide empty black margins",
        huruf={"utama": dict(penuh="huge heavy condensed bold sans-serif capitals",
                             ringkas="heavy condensed sans-serif capitals"),
               "sokongan": dict(penuh="large bold flowing brush script with a big looping initial capital",
                                ringkas="bold brush script"),
               "penyambung": dict(bekas="small solid white rectangular label", nama="label",
                                  dalam="small bold black sans-serif capitals")},
        tertinggi="akhir", hierarki=None, hiasan=None,
        sisi=dict(nama="sparkle", frasa="three short white sparkle strokes"), hiasan_kotak=[],
        tiada=["gray", "shadow", "texture"], ada="flat fills, sharp edges, and a clean empty background",
        sama_lebar=False,
        ukuran=dict(utama=(608, 168), tertinggi=(624, 216), sokongan=(512, 168), penyambung=(224, 80),
                    sisi=(72, 64)),
        # Diukur skrip SK05 daripada gambar upload IMG_5775 (salinan dashboard 236x354), 26 Nov 2026. Satu gambar.
        rujukan=dict(condong_darjah=7.6, tepi_pct=13.6, tepi_sisi_pct=13.6, tepi_atas_bawah_pct=15.5,
                     sumber="SK05 pada IMG_5775",
                     # Diukur SK08 --ukur pada IMG_5775 (236x354), 27 Nov 2026. Satu gambar, resolusi rendah:
                     # anggaran. IoU model dengan kelabu gambar = 0.389; kongsi kelabu dalam huruf 28.6% (model 35.3%).
                     bayang=dict(jenis="dalam", peranan=["sokongan"], arah_relatif_darjah=250, nisbah=0.4,
                                 warna_ukur="#b2b3b5", putih_ukur="#f1f1f3", iou=0.389, kongsi_ruj_pct=28.6,
                                 kongsi_model_pct=35.3, sumber="SK08 --ukur pada IMG_5775"))),
    "K4": dict(
        medium="typographic poster", gaya="vintage Victorian hand-lettered", latar_warna="solid black",
        latar_isi="tiny scattered white specks", tepi="a worn distressed print texture", bentuk="one tall column",
        condong=None, sentuh=None, margin="wide empty black margins",
        huruf={"utama": dict(penuh="very large decorative vintage serif capitals with an oversized first letter "
                                   "and slightly playful letter heights", ringkas="decorative vintage serif capitals"),
               "sokongan": dict(penuh="medium decorative vintage serif capitals",
                                ringkas="medium decorative vintage serif capitals"),
               "penyambung": dict(penuh="small serif capitals", ringkas="small serif capitals")},
        tertinggi=None, hierarki="Main lines are much larger than the small connecting words.",
        hiasan=("Thin ornamental rules made of dotted lines and small curled scrolls separate the lines, and "
                "symmetrical Victorian flourish ornaments sit above the top line and below the bottom line."),
        sisi=None,
        hiasan_kotak=[dict(pada="atas", nama="flourish", frasa="a symmetrical Victorian flourish ornament",
                           ayat="A symmetrical Victorian flourish ornament sits above the top line"),
                      dict(pada="bawah", nama="flourish", frasa="a symmetrical Victorian flourish ornament",
                           ayat="A matching flourish ornament sits below the bottom line")],
        hiasan_baki="Thin ornamental rules made of dotted lines and small curled scrolls separate the lines.",
        tiada=["other colors"], ada="one white ink on a clean black background", sama_lebar=False),
    "K5": dict(
        medium="typographic quote poster", gaya="hand-drawn", latar_warna="solid black", latar_isi=None,
        tepi="a rough chalky distressed texture",
        bentuk="one tight rectangular block in which every line is stretched to the same width",
        condong=None, sentuh="touch and interlock", margin="wide empty black margins",
        huruf={"utama": _K5, "sokongan": _K5,
               "penyambung": dict(penuh="smaller bouncy hand-drawn lowercase letters",
                                  ringkas="bouncy hand-drawn lowercase letters")},
        tertinggi=None, hierarki="Main lines are the largest, and small lowercase words fill the gaps.",
        hiasan="Some letters end in long playful tails that hook under the next letters.", sisi=None,
        hiasan_kotak=[], tiada=["other colors"], ada="white chalky letters on a clean black background",
        sama_lebar=True),
    "K6": dict(
        medium="brush calligraphy poster", gaya="hand-lettered", latar_warna="solid black",
        latar_isi="a few tiny white star dots", tepi="a fine dry-brush grain in the strokes",
        bentuk="one tall block of equal-width lines", condong="rises slightly to the right", sentuh="interlock",
        margin="moderate black margins",
        huruf={"utama": dict(penuh="large flowing brush calligraphy script with thick downstrokes, thin upstrokes "
                                   "and looping capitals", ringkas="flowing brush calligraphy script"),
               "sokongan": dict(penuh="flowing connected brush script", ringkas="flowing connected brush script"),
               "penyambung": dict(penuh="small lowercase brush script", ringkas="small lowercase brush script")},
        tertinggi=None, hierarki="Large words span the full block width, and small words tuck in beside them.",
        hiasan=("Long ribbon-like swashes curl above the first line and below the last line, and swash tails fill "
                "the gaps."), sisi=None,
        hiasan_kotak=[dict(pada="atas", nama="swash", frasa="a long ribbon-like swash",
                           ayat="A long ribbon-like swash curls above the first line"),
                      dict(pada="bawah", nama="swash", frasa="a long ribbon-like swash",
                           ayat="A second ribbon-like swash curls below the last line")],
        hiasan_baki="Swash tails fill the gaps.",
        tiada=["other colors", "outline"], ada="solid white strokes on a clean black background", sama_lebar=True),
    "K7": dict(
        medium="script lettering quote poster", gaya="hand-lettered", latar_warna="solid black", latar_isi=None,
        tepi="a subtle fine print grain", bentuk="one tight block",
        condong="rises clearly toward the right", sentuh="nest closely", margin="moderate black margins",
        huruf={"utama": dict(penuh="very large bold flowing brush script with thick and thin strokes and big swash capitals",
                             ringkas="bold flowing brush script"),
               "sokongan": dict(penuh="large bold flowing brush script with a swash capital",
                                ringkas="bold flowing brush script"),
               "penyambung": dict(penuh="small bold sans-serif capitals with wide letter spacing",
                                  ringkas="small bold sans-serif capitals")},
        tertinggi=None, hierarki="Script words are large, and the small capital words sit in the gaps between them.",
        hiasan=("One long flourish swash sweeps under the last line, and curled swash tails extend from the first "
                "and last letters."), sisi=None,
        hiasan_kotak=[dict(pada="bawah", nama="swash", frasa="a long flourish swash",
                           ayat="One long flourish swash sweeps under the last line")],
        hiasan_baki="Curled swash tails extend from the first and last letters.",
        tiada=["other colors", "outline"], ada="solid white strokes on a clean black background", sama_lebar=False,
        # Diukur SK05 daripada 6 panel IMG_5765 (400x600 setiap satu), 26 Nov 2026: median; julat condong 10.1-14.5,
        # ruang tepi 5.4-10.3.
        rujukan=dict(condong_darjah=12.4, tepi_pct=6.2, tepi_sisi_pct=6.2, tepi_atas_bawah_pct=11.3,
                     sumber="SK05 pada IMG_5765, median 6 panel")),
    "K8": dict(
        medium="brush lettering quote poster", gaya="hand-drawn", latar_warna="solid black",
        latar_isi="a few small scattered white dots", tepi="slightly rough dry-marker edges", bentuk="one tight block",
        condong="tilts so each line rises toward the right", sentuh="sit close together", margin="wide empty black margins",
        huruf={"utama": dict(penuh="very large thick round brush-marker capitals with a bouncy uneven baseline",
                             ringkas="thick round brush-marker capitals"),
               "sokongan": dict(penuh="large thick round brush-marker capitals with a bouncy uneven baseline",
                                ringkas="thick round brush-marker capitals"),
               "penyambung": dict(penuh="smaller thick round brush-marker lowercase letters",
                                  ringkas="thick round brush-marker lowercase letters")},
        tertinggi=None, hierarki="One word is clearly the largest, and the small words tuck in tightly.",
        hiasan=None, sisi=None, hiasan_kotak=[], tiada=["other colors", "outline", "swashes"],
        ada="solid white strokes on a clean black background", sama_lebar=False,
        # Diukur SK05 daripada IMG_5735 (600x449, melintang; latar bertekstur), 26 Nov 2026. Satu gambar.
        rujukan=dict(condong_darjah=7.4, tepi_pct=12.2, sumber="SK05 pada IMG_5735")),
    "K9": dict(
        medium="hand-lettered quote poster", gaya="playful", latar_warna="solid black",
        latar_isi="small white hearts scattered on the left and right sides", tepi="crisp clean vector edges",
        bentuk="one tight block", condong=None, sentuh="sit close together", margin="narrow black margins",
        huruf={"utama": dict(penuh="huge heavy rounded bold sans-serif capitals", ringkas="heavy rounded sans-serif capitals"),
               "sokongan": dict(penuh="large bold bouncy connected script with a looping capital",
                                ringkas="bold bouncy connected script"),
               "penyambung": dict(penuh="small bold bouncy connected script", ringkas="small bouncy script")},
        tertinggi=None, hierarki="The capital words are the widest lines, and the script lines are slightly narrower.",
        hiasan="One long swash tail sweeps under the last line.", sisi=None,
        hiasan_kotak=[dict(pada="bawah", nama="swash", frasa="a long swash tail",
                           ayat="One long swash tail sweeps under the last line")],
        tiada=["gray", "outline", "shadow", "texture"], ada="flat solid white fills on a clean black background",
        sama_lebar=False,
        rujukan=dict(condong_darjah=0.0, tepi_pct=3.8, tepi_sisi_pct=3.8, tepi_atas_bawah_pct=14.8,
                     sumber="SK05 pada IMG_5845 (1199x1799); condong 11.4 diukur tetapi dibaca 0 kerana ekor swash")),
    "K10": dict(
        medium="round badge typography design", gaya="clean hand-lettered", latar_warna="solid black", latar_isi=None,
        tepi="crisp clean vector edges",
        bentuk="one round badge layout whose first line arcs over the top and whose last line arcs under the bottom",
        condong=None, sentuh=None, margin="wide black margins",
        huruf={"utama": dict(penuh="huge flowing brush script with tall loops", ringkas="flowing brush script"),
               "sokongan": dict(penuh="medium thin brush script", ringkas="thin brush script"),
               "penyambung": dict(penuh="bold condensed sans-serif capitals bent along the curve",
                                  ringkas="condensed sans-serif capitals bent along the curve")},
        tertinggi=None, hierarki="The center script word is by far the largest, and the curved lines are small.",
        hiasan=("Small four-pointed sparkle stars are spaced around the inside of the circle, and two small hearts sit "
                "under the large word."), sisi=None, hiasan_kotak=[],
        tiada=["gray", "outline", "circle line", "shadow"], ada="flat solid white fills on a clean black background",
        sama_lebar=False,
        rujukan=dict(condong_darjah=0.0, tepi_pct=7.0, sumber="SK05 pada IMG_5846 (1200x1200); lencana bulat, condong dibaca 0")),
    "K11": dict(
        medium="script lettering quote poster", gaya="hand-lettered", latar_warna="solid black", latar_isi=None,
        tepi="crisp clean edges", bentuk="one tight block with one word on each line",
        condong="rises slightly toward the right", sentuh="interlock", margin="moderate black margins",
        huruf={"utama": dict(penuh="very large bold connected brush script with thick and thin strokes and a big looping capital",
                             ringkas="bold connected brush script"),
               "sokongan": dict(penuh="large bold connected brush script with thick and thin strokes",
                                ringkas="bold connected brush script"),
               "penyambung": dict(penuh="medium bold connected brush script", ringkas="bold connected brush script")},
        tertinggi=None, hierarki="All words are similar in size, and the first and last words are the widest.",
        hiasan="Long curled swash tails extend from the first letter and the last letter, and one swash underlines the last word.",
        sisi=None,
        hiasan_kotak=[dict(pada="bawah", nama="swash", frasa="a long curled swash",
                           ayat="One long curled swash underlines the last word")],
        hiasan_baki="Long curled swash tails extend from the first letter and the last letter.",
        tiada=["gray", "outline", "shadow", "texture"], ada="solid white strokes on a clean black background",
        sama_lebar=False,
        rujukan=dict(condong_darjah=1.9, tepi_pct=11.0, tepi_sisi_pct=11.0, tepi_atas_bawah_pct=13.2,
                     sumber="SK05 pada IMG_5840 (736x981)")),
    "K12": dict(
        medium="typographic quote poster", gaya="bold distressed", latar_warna="solid black", latar_isi=None,
        tepi="a heavy scratched and speckled distressed texture",
        bentuk="one tight justified block in which every line is stretched to the same full width",
        condong=None, sentuh="almost touch", margin="wide black margins",
        huruf={"utama": dict(penuh="gigantic ultra condensed heavy sans-serif capitals filling about half the block height",
                             ringkas="ultra condensed heavy sans-serif capitals"),
               "sokongan": _SANS, "penyambung": _SANS},
        tertinggi=None, hierarki="All lines share the same width, and the main word is far taller than every other line.",
        hiasan=None, sisi=None, hiasan_kotak=[],
        tiada=["gray", "outline", "shadow"], ada="gritty scratched white letters on a clean black background",
        sama_lebar=True,
        rujukan=dict(condong_darjah=0.0, tepi_pct=15.4, tepi_sisi_pct=15.5, tepi_atas_bawah_pct=16.6,
                     sumber="SK05 pada IMG_5793 (1170x1691), panel koral sahaja dianggap kanvas: anggaran")),
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
