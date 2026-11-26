"""Tab FC > Design dalam dashboard: carta aliran lettering v1.2 (9 langkah x 3 lajur) + lajur Alat bagi setiap lajur.

Sumber isi: scripts/lettering_flowchart.py dan docs/lettering-standard.md (v1: 25 Nov 2026; lajur ketiga dikemas kini ke v1.2, 26 Nov 2026).
Status alat = keadaan 25 Nov 2026 (bukti: designs/lettering-v1/*, scripts/lettering/*, data/export/setup/*.json).

Guna: python3 scripts/build_fc_design.py <index.html> <folder keluar>
  Ubah index.html (butang tab FC, rangka seksyen, pautan fc.css / fc.js) dan tulis fc.css + fc.js ke folder keluar.
  Isi jadual dan gaya dalam fail berasingan kerana stor dashboard menghadkan setiap dokumen kepada 256 KB.
"""
import html
import re
import sys

E = html.escape
OK, PART, NO = ("ada", "ok"), ("sebahagian", "warn"), ("belum dibina", "bad")
TESTED = ("diuji 24 Nov", "warn")
GPU = ("belum diuji", "warn")

COLS = [("Sedia ada: S1–S6 (Lettering P9)", "fc-c1"), ("Cadangan pertama: 4 lapisan, 5 kunci", "fc-c2"),
        ("Standard v1.2: aliran terkini", "fc-c3")]

# Setiap baris: (sedia ada, alat), (cadangan pertama, alat), (standard v1, alat)
ROWS = [
    ((dict(title="1. Rujukan", body=["Upload rujukan", "Ambil ciri umum sahaja"],
           warn=["Ciri gaya hanya ada dalam ayat templat"]),
      [("Anda", "upload imej rujukan", OK), ("Claude", "baca imej, ambil ciri umum", OK)]),
     (dict(tag="LAPISAN 1", status="BAHARU", title="1. Kad Gaya",
           body=["Gaya lama: guna kad dalam S&C", "Gaya baharu: Claude isi kad daripada upload",
                 "Isi kad: medium, bentuk huruf ikut peranan, susunan, hierarki, hiasan, kelas kemasan, 8 ciri QC, julat panjang sesuai",
                 "Warna C berasingan: latar + dakwat 1–3"],
           keys=["Kunci 1: Kad Gaya satu-satunya sumber gaya"]),
      [("Claude", "isi kad daripada upload", OK), ("Tab Daftar S/C", "semak gaya lama", OK)]),
     (dict(tag="LAPISAN 1", status="DIKEMAS KINI", title="1. Kad Gaya",
           body=["1a simpan rujukan di tempat kekal; 1b semak pendua dalam S&C",
                 "1c isi kad 16 medan; setiap medan = semakan QC (ya / tidak) + frasa prompt",
                 "2–3 ciri teras wajib lulus; unsur berisiko; senarai jangan salin; julat panjang ayat",
                 "Warna C berasingan: peranan + nama warna untuk prompt",
                 "Ukuran rujukan (v1.2): nisbah tinggi baris, ruang tepi, saiz label dan sudut condong diukur daripada upload, bukan diteka",
                 "1d anda luluskan kad (~2 minit); 1e imej bukti (ayat pendek, 2 seed) jadi imej sauh"],
           keys=["Kunci 1: Kad Gaya satu-satunya sumber gaya"]),
      [("Tab Daftar S/C", "1a simpan rujukan, 1b semak pendua", OK),
       ("kad.py (Python)", "Kad Gaya K1–K6, ciri QC + frasa prompt", PART),
       ("Skrip ukuran rujukan (Python)", "ukur upload, simpan angka dalam kad (v1.2)", NO),
       ("Anda", "1d luluskan kad", OK), ("gen_moss.py / gen.py", "1e imej bukti, 2 seed", OK)])),

    ((dict(title="2. Ayat", body=["3–7 perkataan, semak trademark", "Tetapkan baris dan perkataan utama"],
           warn=["Diuji pada 4 perkataan sahaja", "Hanya 2 kelas: pendek ≤ 6, panjang ≥ 7"]),
      [("Claude", "pilih ayat, baris, perkataan utama", OK), ("Semak trademark", "tiada kaedah bertulis", NO)]),
     (dict(status="DIUBAH", title="2. Ayat + peranan + laluan",
           body=["Semak trademark", "Setiap perkataan: utama / sokongan / penyambung",
                 "Laluan ikut panjang ayat baharu, bukan ayat rujukan"],
           minis=[("Laluan 1", "Pendek (1–4 perkataan). AI penuh, satu blok"),
                  ("Laluan 2", "Sederhana (5–8). AI penuh, hierarki wajib"),
                  ("Laluan 3", "Panjang (9–16). Hibrid: AI lukis perkataan utama, font berlesen untuk baris lain"),
                  ("Laluan 4", "Terlalu panjang (17+). Font dahulu: AI buat tajuk dan hiasan sahaja")]),
      [("Claude", "peranan setiap perkataan, pilih laluan", OK), ("USPTO", "semak trademark (Setup s26: Belum)", NO),
       ("Font berlesen", "laluan 3–4", NO)]),
     (dict(status="DIKEMAS KINI", title="2. Ayat + peranan + laluan",
           body=["Ayat asal; saringan trademark bertulis, hasil direkod",
                 "Ukur kesukaran: bilangan perkataan, perkataan 7+ huruf, perkataan berulang",
                 "Kata isi = utama; kata fungsi = penyambung; perkataan 7+ huruf jadi utama",
                 "Sokongan dan penyambung HURUF BESAR kecuali kad wajibkan skrip",
                 "Hasil: Spesifikasi Teks (rujukan ejaan untuk QC)"],
           minis=[("Laluan 1: standard v1", "1–4 perkataan. AI penuh, satu blok"),
                  ("Laluan 2: standard v1", "5–8 perkataan. AI penuh, hierarki wajib"),
                  ("Laluan 3: percubaan", "9–16 perkataan. Hibrid. Belum diuji; perlu kelulusan anda"),
                  ("Laluan 4: percubaan", "17+ perkataan. Font dahulu. Belum diuji; perlu kelulusan anda")]),
      [("kad.py (Python)", "Spesifikasi Teks + ukur kesukaran", PART), ("Claude", "peranan, pilih laluan", OK),
       ("USPTO", "saringan bertulis, hasil direkod", NO), ("Font berlesen", "laluan 3–4 (percubaan)", NO)])),

    ((dict(title="3. Prompt: templat tetap", body=["styles.py: 6 ayat siap (S1–S6)", "Arahan setiap perkataan + ekor larangan"],
           warn=["Dikunci pada 4 perkataan", "Gaya, warna dan latar bercampur"]),
      [("styles.py (Python)", "6 prompt siap S1–S6", OK)]),
     (dict(tag="LAPISAN 2", status="BAHARU", title="3. Pembina prompt",
           body=["Kad Gaya + ayat + warna C + keluarga model",
                 "Peraturan: petikan sekali sahaja, tiada hex atau nombor, ayat hierarki wajib"],
           minis=[("Keluarga LLM", "MOSS, klein, Z-Image, ERNIE: prompt penuh"),
                  ("Keluarga T5", "schnell, Chroma: ringkas, teks di depan")]),
      [("Pembina prompt (Python)", "dibina sebagai kad.py dalam v1", PART)]),
     (dict(tag="LAPISAN 2", status="V1.2", title="3. Pembina prompt: satu isi, aturan ikut model",
           body=["Isi sama untuk semua model: Kad Gaya + Spesifikasi Teks (8 blok isi)",
                 "Cara menulis ikut aturan model; aturan tidak boleh menambah atau membuang ciri gaya",
                 "7 model ada aturan: 4 sudah diuji (r1), 3 daripada sumber rasmi sahaja dan belum diuji (r0)",
                 "Model tanpa aturan sendiri: rangka am 9 bahagian (pembina v1.1)",
                 "Hitam putih sahaja; tiada negative prompt; tiada nama warna, hex, nombor atau nama font",
                 "Semak automatik sebelum jana; prompt yang gagal tidak dijana",
                 "Aturan diubah hanya melalui kitaran QC, satu ubahan setiap pusingan; direkod dalam Catatan pembaikan",
                 "Bukti lemah (K3 × 1 ayat × 3 seed, 26 Nov): ejaan betul 6/12 dengan rangka am, 11/12 dengan aturan model"],
           minis=[("klein 4B", "Satu perenggan prosa; satu ayat setiap baris; gaya ditulis terus selepas perkataan; had dalam satu ayat di hujung"),
                  ("Z-Image Turbo", "Huraian panjang seperti kapsyen; baris bernombor; had ditulis sebagai ayat positif"),
                  ("ERNIE Turbo", "Prompt mentah pendek + penambah prompt rasmi sekali (seed 42); hasil disemak sebelum jana"),
                  ("MOSS + LoRA", "Satu objek JSON; satu butir dan satu kotak piksel bagi setiap baris"),
                  ("FLUX 3 Image Klein (r0, belum diuji)", "Kapsyen penuh satu perenggan + jadual kotak JSON grid 0–1000; penambah prompt dimatikan"),
                  ("Qwen-Image-2512 (r0, belum diuji)", "Kurang 200 perkataan; setiap baris = kedudukan, perkataan dalam petikan, gaya"),
                  ("GLM-Image (r0, belum diuji)", "Naratif bersambung tanpa senarai; setiap baris = kedudukan, fungsi, perkataan dalam petikan, gaya font")]),
      [("kad.py: bina() + semak() (Python)", "rangka am hitam putih (v1.1) + semakan automatik", PART),
       ("khas.py (Python)", "7 aturan sebagai contoh tulisan tangan (K3 × ayat H); 4 sudah dijana", PART),
       ("Pembina kod ikut model", "jana prompt setiap model daripada kad (v1.2)", NO),
       ("gen.py: PROFIL", "profil setiap model dikunci", PART)])),

    ((dict(title="4. Jana", body=["MOSS SFT + LoRA 8 langkah", "Text-to-image penuh, 768×1024", "2 seed (CPU)"],
           warn=["Tiada peraturan tukar model"]),
      [("MOSS-Image SFT + LoRA", "model, 8 langkah", OK), ("gen_moss.py (Python, diffusers)", "CPU, 2 seed", OK)]),
     (dict(status="DIUBAH", title="4. Jana",
           body=["Text-to-image penuh, 768×1024",
                 "Laluan 1–2: seluruh ayat. Laluan 3: perkataan utama sahaja. Laluan 4: tajuk + hiasan",
                 "Seed: 2 (laluan 1), 3–4 (laluan 2)", "Log: model, seed, prompt, masa"],
           keys=["Kunci 3: model hanya untuk gaya yang ia lulus"]),
      [("MOSS-Image, ERNIE-Image-Turbo", "keluarga LLM", OK), ("FLUX.2 klein 4B, Z-Image-Turbo", "keluarga LLM", OK),
       ("FLUX.1 schnell, Chroma", "keluarga T5", OK), ("diffusers (Python)", "enjin", OK)]),
     (dict(status="DIKEMAS KINI", title="4. Jana",
           body=["Jana hitam putih dahulu: dakwat putih atas latar hitam, tiada warna lain",
                 "Tetapan dikunci dalam profil model; enjin diffusers",
                 "Model utama: MOSS dan ERNIE (12/12 pada S1–S6); klein 4B 6/12",
                 "Profil dikunci v1.2: klein 4B, Z-Image Turbo, ERNIE Turbo, MOSS + LoRA; setiap satu dengan aturan prompt sendiri",
                 "Masa setiap imej di CPU (log 26 Nov, bukti lemah): klein 85–118 s, Z-Image kira-kira 260 s, ERNIE 305–373 s, MOSS 337–392 s",
                 "3 model tambahan melalui Space Hugging Face (GPU, kuota harian): FLUX 3 Image Klein, Qwen-Image-2512, GLM-Image; belum diuji",
                 "Tidak dipilih: FLUX.1 schnell (3/30 ejaan betul), Chroma1-Flash (0/6); simpanan: Ovis-Image-7B",
                 "Seed tetap 42, 7, 123, 2024: laluan 1 = 2 seed, laluan 2 = 3–4",
                 "Satu model besar pada satu masa; semak RAM dan disk dahulu",
                 "Log lengkap setiap imej; imej mentah disimpan sebelum sesi tamat"],
           keys=["Kunci 3: model hanya untuk gaya yang ia lulus"]),
      [("gen_moss.py", "MOSS SFT + LoRA", OK),
       ("gen.py", "ERNIE, klein 4B, Z-Image, schnell, Chroma, Kandinsky", OK),
       ("run_k6.py", "ujian 6 enjin, satu demi satu", OK), ("Kaggle GPU (GEN_DEVICE)", "banding CPU vs GPU", GPU),
       ("gen_hf_space.py", "profil Space untuk FLUX 3 Klein, Qwen-Image-2512, GLM-Image", NO)])),

    ((dict(title="5. QC", body=["Ejaan 100%, tiada teks rawak, tiada cacat", "9 ciri gaya (semak mata)",
                                "Gagal: seed baharu (maks 4)"]),
      [("Claude", "semak mata: ejaan + 9 ciri gaya", OK)]),
     (dict(tag="LAPISAN 3", status="DIUBAH", title="5. QC ikut kad",
           body=["OCR saring dahulu, kemudian semak mata",
                 "3 pintu wajib: ejaan 100%, tiada teks rawak, tiada cacat", "Gaya: sekurang-kurangnya 7/8 ciri kad",
                 "Gagal: tambah ayat penegas + seed baharu (maks 4), kemudian model sandaran"],
           keys=["Kunci 2: QC sama untuk semua model", "Kunci 5: peraturan ulang"]),
      [("RapidOCR", "saring ejaan", TESTED), ("Claude", "semak mata + ayat penegas", OK)]),
     (dict(tag="LAPISAN 3", status="DIKEMAS KINI", title="5. QC ikut kad",
           body=["QC pada imej hitam putih dahulu: ejaan, ayat, gaya",
                 "3 pintu wajib; ejaan huruf demi huruf ikut Spesifikasi Teks; OCR hanya menanda",
                 "Ciri kad ≥ 7/8 + ciri teras wajib; banding dengan upload dan imej sauh",
                 "Ciri sejagat: boleh dibaca kecil, tiada teks terpotong, margin cukup",
                 "QC dua kali: imej mentah hitam putih, dan selepas warna + kemasan",
                 "Kitaran QC (v1.2): cacat pada satu seed = tukar seed, prompt tidak diubah",
                 "Cacat sama pada 2 daripada 3 seed = reka semula prompt model itu, satu ubahan setiap pusingan, seed sama",
                 "Had 2 pusingan → tukar model → pendekkan ayat → lapor; pembaikan berjaya ditulis balik ke aturan model",
                 "5b Pembetulan skrip (v1.2), selepas 3 pintu lulus: condong, ruang tepi, kedudukan, hitam putih bersih",
                 "5b hanya jalan bila ukuran tersasar daripada ukuran rujukan kad; ejaan dan bentuk huruf mesti jana semula"],
           keys=["Kunci 2: QC sama untuk semua model", "Kunci 5: kitaran QC tetap; pembetulan skrip bila perlu sahaja"]),
      [("Claude + helaian semakan", "3 pintu, ciri kad ≥ 7/8", OK),
       ("Skrip pembetulan 5b (Python)", "ukur, betulkan, ukur semula; had toleransi belum ditetapkan", NO),
       ("RapidOCR", "hanya menanda (skor 0.33–0.88 pada ejaan betul)", TESTED),
       ("qc/<model>.json", "rekod QC setiap imej", PART)])),

    ((dict(title="6. Kemasan: finish.py", body=["Vektor → palet gaya → margin seragam", "300 DPI, 8×10 hingga 24×36",
                                                "Tekstur: grain / worn / chalk"],
           warn=["Dakwat rata atas latar satu warna sahaja"]),
      [("finish.py (Python)", "paksa palet gaya, margin seragam, tekstur (k-means, potrace, cairosvg)", OK)]),
     (dict(tag="LAPISAN 4", status="DIUBAH", title="6. Kemasan ikut kelas",
           body=["Palet C dipaksa di sini", "F1 dan F2: 1 imej → beberapa warna",
                 "Laluan 3–4: skrip gabung baris font ikut kad, kemudian semak 8 ciri sekali lagi"],
           minis=[("F1", "Vektor rata (finish.py)"), ("F2", "Rata + tekstur"), ("F3", "Raster: gaya bergambar, gradien")],
           keys=["Kunci 4: skrip paksa warna, margin, tekstur"]),
      [("finish.py", "F1 / F2; paksa palet C dan margin", OK), ("Alat F3 raster", "belum dipilih", NO),
       ("Skrip gabung baris font", "laluan 3–4", NO)]),
     (dict(tag="LAPISAN 4", status="DIKEMAS KINI", title="6. Kemasan ikut kad",
           body=["Bermula hanya selepas QC hitam putih lulus",
                 "Parameter daripada kad: margin, tekstur, bilangan dakwat, butiran halus",
                 "Semak automatik: bilangan lapisan dan dakwat yang hilang",
                 "Warna C diletak oleh skrip ikut peranan: 1 imej → beberapa warna C",
                 "Seed tekstur berbeza setiap design",
                 "Simpan SVG induk; PNG besar dijana semula bila perlu"],
           minis=[("F1: v1", "Vektor rata"), ("F2: v1", "Rata + tekstur"), ("F3: ditangguh", "Raster; belum wujud")],
           keys=["Kunci 4: AI jana hitam putih; skrip letak warna, margin, tekstur selepas QC lulus"]),
      [("finish.py", "F1 / F2; palet, margin dan tekstur masih tetap dalam skrip", PART),
       ("Kemasan ikut kad (Python)", "baca warna, margin dan tekstur daripada kad", NO)])),

    ((dict(title="7. Anda lulus atau tolak", body=["~5 minit"]),
      [("Anda", "~5 minit", OK)]),
     (dict(title="7. Anda lulus atau tolak", body=["~5 minit"]),
      [("Anda", "~5 minit", OK)]),
     (dict(status="DIKEMAS KINI", title="7. Anda lulus atau tolak",
           body=["Mata anda pintu terakhir (v1.2): imej lulus QC tetapi nampak buruk = gagal",
                 "Papar upload, imej sauh dan hasil sebelah-menyebelah + skor QC; anda pilih daripada satu helaian",
                 "Sebab tolak daripada senarai tetap; disalur balik ke kad, aturan model, jadual model × gaya atau ulangan",
                 "4 titik kelulusan: kad, contoh pertama laluan 3–4, hitam putih lulus QC, hasil akhir berwarna",
                 "Had bilangan imej setiap helaian"]),
      [("Anda", "4 titik kelulusan", OK), ("Paparan sebelah-menyebelah", "upload, imej sauh, hasil + skor QC", NO),
       ("Tab AI Image Test / Daftar S/C", "pilih A atau SNC selepas setiap jana", OK)])),

    ((dict(title="8. Simpan dalam S&C", body=["Nama, nota, imej contoh, imej asal, prompt terisi"],
           warn=["Prompt terisi sahaja; tiada ciri gaya berstruktur"]),
      [("Tab Daftar S/C", "stor data/gaya + data/warna", OK)]),
     (dict(status="DIUBAH", title="8. Simpan dalam S&C", body=["Kad Gaya + prompt + model + seed + imej",
                                                               "Gaya boleh dijana semula"]),
      [("Tab Daftar S/C", "rekod S dan C", OK), ("Kad Gaya berstruktur dalam stor", "", NO)]),
     (dict(status="DIKEMAS KINI", title="8. Simpan dalam S&C",
           body=["Rekod S: Kad Gaya + templat prompt tanpa perkataan + model lulus + versi kad",
                 "Rekod C: peranan + nama warna; satu sumber kod hex",
                 "Daftar design lulus: ayat, S, C, model, seed, fail induk", "Semua fail disimpan sebelum sesi tamat"]),
      [("Tab Daftar S/C", "rekod S dan C", OK), ("Kad Gaya berstruktur dalam stor", "templat, model lulus, versi", NO),
       ("Daftar design", "ayat, S, C, model, seed, fail induk", NO)])),

    ((dict(title="9. Mockup → pin → upload", body=[]),
      [("Skrip mockup", "Workflow w03", NO), ("Printify API", "w04; akaun Printify: Sedang (Setup s09)", PART),
       ("Pinterest API", "w05; Setup s15–s18: Belum", NO)]),
     (dict(title="9. Mockup → pin → upload", body=[]),
      [("Skrip mockup", "Workflow w03", NO), ("Printify API", "w04; Setup s09: Sedang", PART),
       ("Pinterest API", "w05; Setup s15–s18: Belum", NO)]),
     (dict(status="DIKEMAS KINI", title="9. Serahan → mockup → pin → upload",
           body=["Standard berhenti di serahan kepada Workflow",
                 "Serahan: fail cetak setiap saiz, pratonton, ayat, kod S dan C, hasil trademark",
                 "Produk dan pin ditanda kod S / C → tab Prestasi",
                 "Jualan kembali ke S&C: gaya menang dapat lebih ayat dan warna"]),
      [("USPTO", "w02 hasil saringan dalam serahan", NO), ("Skrip mockup", "w03", NO),
       ("Printify API", "w04; Setup s09: Sedang", PART), ("Pinterest API", "w05; Setup s15–s18: Belum", NO),
       ("Prestasi (kod S / C)", "tiada dalam dashboard semasa", NO)])),

    ((dict(title="Tukar model", body=["Tiada peraturan bertulis.",
                                      "Ujian P9b (24 Nov) pada S1–S6: MOSS 12/12, ERNIE 12/12, klein 4B 6/12 imej ejaan betul."]),
      [("Ujian P9b", "MOSS, ERNIE, klein 4B pada S1–S6", OK)]),
     (dict(title="Tukar model", body=["Ujian kelayakan sekali bagi setiap model baharu, direkod dalam jadual model × gaya.",
                                      "Setiap gaya × ayat pendek dan sederhana × 2 seed.",
                                      "Lulus: ≥ 90% imej ejaan betul, gaya ≥ 7/8, tiada teks liar."]),
      [("Jadual model × gaya", "", NO)]),
     (dict(title="Tukar model", body=["Standard v1.2 (v1 dipersetujui 25 Nov; v1.2 diluluskan pengguna 26 Nov): laluan 1–2, kemasan F1–F2. Belum dibina sepenuhnya.",
                                      "Ujian kelayakan seperti cadangan, sah untuk gabungan tetapan yang dikunci sahaja.",
                                      "Model baharu perlu aturan prompt sendiri, diuji banding dengan rangka am pada seed 42, 7, 123.",
                                      "Menunggu ujian kelayakan: FLUX 3 Image Klein, Qwen-Image-2512, GLM-Image (aturan r0).",
                                      "Tahap bukti angka: lemah."]),
      [("gen.py + run_k6.py", "ujian kelayakan setiap enjin", OK),
       ("qc/<model>.json", "hasil → jadual model × gaya", PART)])),
]


TONE_LABEL = {"ok": "ada", "warn": "separuh", "bad": "belum"}
HEAD = [("Sedia ada", "S1–S6 · Lettering P9", ""), ("Cadangan pertama", "4 lapisan · 5 kunci", ""),
        ("Standard v1.2", "aliran terkini · 26 Nov", "TERKINI")]


# Susunan (layout huruf) dan warna: dua faktor utama design; ditonjolkan dalam jadual.
SUS = re.compile(r"susun|baris|hierarki|margin|ruang tepi|bentuk huruf|perkataan utama|utama /|kata isi|huruf besar|satu blok|tajuk", re.I)
WAR = re.compile(r"warna|palet|dakwat|latar|Rekod C", re.I)
IC = {"s": '<i class="fc-ic-s" aria-hidden="true"></i>', "w": '<i class="fc-ic-w" aria-hidden="true"></i>'}


def fl(text):
    return ("s" if SUS.search(text) else "") + ("w" if WAR.search(text) else "")


def hc(f):
    return " ".join({"s": "fc-hs", "w": "fc-hw"}[c] for c in f)


def tagchips(f):
    return "".join(f'<span class="fc-tg fc-tg-{c}">{IC[c]}{"Susunan" if c == "s" else "Warna"}</span>' for c in f)


def pill(text, tone, cls=""):
    t = f' data-tone="{tone}"' if tone else ""
    return f'<span class="pod-pill {cls}"{t}>{E(text)}</span>'


def badge(title):
    m = re.match(r"(\d+)\.\s*(.*)", title)
    return (m.group(1), m.group(2)) if m else ("⇄", title)


def cell(s):
    num, title = badge(s["title"])
    texts = s["body"] + [h + " " + t for h, t in s.get("minis", [])] + s.get("keys", []) + s.get("warn", [])
    cf = "".join(c for c in "sw" if any(c in fl(x) for x in texts))
    o = []
    if s.get("tag") or s.get("status") or cf:
        o.append('<div class="fc-meta">')
        if s.get("tag"):
            o.append(f'<span class="fc-tag">{E(s["tag"])}</span>')
        if s.get("status"):
            o.append(f'<span class="fc-st">{E(s["status"])}</span>')
        if cf:
            o.append(f'<span class="fc-tgs">{tagchips(cf)}</span>')
        o.append("</div>")
    o.append(f'<div class="fc-title"><span class="fc-num">{E(num)}</span><b>{E(title)}</b></div>')
    det = []
    if s["body"]:
        det.append('<ul class="fc-body">' + "".join(f'<li class="{hc(fl(b))}">{E(b)}</li>' for b in s["body"]) + "</ul>")
    if s.get("minis"):
        det.append('<div class="fc-minis">' + "".join(
            f'<div class="fc-mini {hc(fl(h + " " + t))}"><b>{E(h)}</b><span>{E(t)}</span></div>' for h, t in s["minis"]) + "</div>")
    chips = [f'<span class="fc-chip fc-key {hc(fl(k))}"><i>K</i>{E(k)}</span>' for k in s.get("keys", [])]
    chips += [f'<span class="fc-chip fc-warn {hc(fl(w))}"><i>!</i>{E(w)}</span>' for w in s.get("warn", [])]
    if chips:
        det.append('<div class="fc-chips">' + "".join(chips) + "</div>")
    if det:
        o.append('<div class="fc-det">' + "".join(det) + "</div>")
    return "".join(o)


def tools(ts):
    return '<ul class="fc-tools">' + "".join(
        f'<li class="fc-tool {hc(fl(n + " " + d))}" data-tone="{st[1]}"><div class="fc-tool-top"><b>{E(n)}'
        f'{"".join(IC[c] for c in fl(n + " " + d))}</b>'
        f'<span class="fc-stat">{E(st[0])}</span></div>{f"<span class=fc-desc>{E(d)}</span>" if d else ""}</li>'
        for n, d, st in ts) + "</ul>"


def summary(i):
    c = {"ok": 0, "warn": 0, "bad": 0}
    for row in ROWS:
        for _, _, st in row[i][1]:
            c[st[1]] += 1
    n = sum(c.values())
    bar = "".join(f'<span data-tone="{k}" style="flex:{v}"></span>' for k, v in c.items() if v)
    txt = " · ".join(f"{v} {TONE_LABEL[k]}" for k, v in c.items() if v)
    return (f'<span class="fc-bar" role="img" aria-label="{n} alat: {E(txt)}">{bar}</span>'
            f'<span class="fc-count">{E(txt)}</span>')


def table():
    head = ""
    for i, ((name, sub, flag), (_, c)) in enumerate(zip(HEAD, COLS)):
        fl = f'<span class="fc-flag">{E(flag)}</span>' if flag else ""
        head += (f'<th class="{c}" scope="col"><span class="fc-hname">{E(name)}{fl}</span>'
                 f'<span class="fc-hsub">{E(sub)}</span></th>'
                 f'<th class="{c} fc-alat" scope="col"><span class="fc-hname">Alat</span>{summary(i)}</th>')
    body = []
    for row in ROWS:
        tds = "".join(f'<td class="{COLS[i][1]}">{cell(s)}</td><td class="{COLS[i][1]} fc-alat">{tools(t)}</td>'
                      for i, (s, t) in enumerate(row))
        body.append(f"<tr>{tds}</tr>")
    return (f'<div class="fc-wrap"><table class="fc-table"><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')


def content():
    legend = "".join(f'<span><i class="fc-dot" data-tone="{t}"></i>{E(l)}</span>' for t, l in (
        ("ok", "ada: alat wujud dan dipakai"), ("warn", "separuh siap / sedang diuji"), ("bad", "belum dibina")))
    legend += ('<span><span class="fc-chip fc-key"><i>K</i>Kunci</span> 5 kunci gaya</span>'
               '<span><span class="fc-chip fc-warn"><i>!</i>Kelemahan</span> aliran sedia ada</span>')
    focus = ('<div class="fc-focus"><p><b>Dua faktor utama design:</b></p>'
             f'<span class="fc-tg fc-tg-s">{IC["s"]}Susunan</span><span>bentuk huruf, baris, hierarki, perkataan utama, margin</span>'
             f'<span class="fc-tg fc-tg-w">{IC["w"]}Warna</span><span>warna C, palet, latar, dakwat</span></div>')
    return f"""<div class="fc-intro">
<h2>Aliran kerja lettering: 3 versi, 9 langkah</h2>
<p class="fc-how"><b>Cara baca:</b> setiap baris satu langkah (1 → 9). Ke kanan: aliran lama → cadangan → standard terkini. Lajur <b>Alat</b> di sebelah setiap versi menunjukkan alat yang dipakai dan statusnya. Poin bertanda <b class="fc-t-s">oren</b> = susunan, <b class="fc-t-w">merah jambu</b> = warna.</p>
{focus}
<p class="pod-muted">Sumber: carta v1 (scripts/lettering_flowchart.py) dan docs/lettering-standard.md. Standard v1 dipersetujui 25 Nov 2026; v1.2 diluluskan pengguna 26 Nov 2026 (aturan prompt untuk 7 model, kitaran QC, ukuran rujukan, pembetulan skrip); belum dibina sepenuhnya. Laluan 3–4 percubaan, F3 ditangguh. Status alat = keadaan 26 Nov 2026.</p>
</div>
<div class="fc-bar-top">
<div class="fc-legend">{legend}</div>
<div class="fc-ctl"><div class="fc-mode fc-hlset" role="group" aria-label="Tonjolkan"><span>Tonjol</span><button type="button" data-hl="semua" aria-pressed="true">Kedua-dua</button><button type="button" data-hl="susunan" aria-pressed="false">Susunan</button><button type="button" data-hl="warna" aria-pressed="false">Warna</button><button type="button" data-hl="tiada" aria-pressed="false">Tiada</button></div>
<div class="fc-mode fc-modeset" role="group" aria-label="Paparan"><button type="button" data-mode="penuh" aria-pressed="true">Penuh</button><button type="button" data-mode="ringkas" aria-pressed="false">Ringkas</button></div></div>
</div>
<div class="fc-frame" data-mode="penuh" data-hl="semua">{table()}</div>"""


SECTION = """<!-- FC:TAB START -->
<section id="tab-fc" class="pod-tab" role="tabpanel" aria-labelledby="btn-fc" hidden>
<div class="fc-subbar" role="tablist" aria-label="Sub tab FC">
  <button type="button" class="fc-sub-btn" role="tab" id="btn-fc-design" data-sub="fc-design" aria-controls="fc-design" aria-selected="true">Design</button>
</div>
<section id="fc-design" class="pod-section pod-first fc-sub" role="tabpanel" aria-labelledby="btn-fc-design"><p class="pod-muted">Memuatkan carta…</p></section>
</section>
<!-- FC:TAB END -->"""

TAB_S, TAB_E = "<!-- FC:TAB START -->", "<!-- FC:TAB END -->"
CSS_S, CSS_E = "/* FC:CSS START */", "/* FC:CSS END */"
JS_S, JS_E = "<!-- FC:JS START -->", "<!-- FC:JS END -->"

CSS = """.fc-c1 { --fc-accent: #64748b; } .fc-c2 { --fc-accent: #0d9488; } .fc-c3 { --fc-accent: #6366f1; }
#tab-fc { --fc-on: #fff; --fc-ok: var(--color-ok, #1a7f37); --fc-warn: var(--color-warn, #9a6700); --fc-bad: var(--color-bad, #cf222e); --fc-key: #2563eb; }
@media (prefers-color-scheme: dark) { .fc-c1 { --fc-accent: #94a3b8; } .fc-c2 { --fc-accent: #2dd4bf; } .fc-c3 { --fc-accent: #a5b4fc; } #tab-fc { --fc-on: #111; --fc-key: #60a5fa; } }
.fc-subbar { display: flex; gap: var(--cds-gap-xs); border-bottom: 1px solid var(--color-border-line); }
.fc-sub-btn { appearance: none; background: none; border: 0; border-bottom: 2px solid transparent; margin-bottom: -1px; padding: 4px var(--cds-pad-md); font: inherit; font-size: var(--cds-font-size-caption); color: var(--color-fg-muted); cursor: pointer; }
.fc-sub-btn[aria-selected="true"] { color: var(--color-fg); border-bottom-color: var(--color-fg); font-weight: var(--cds-font-weight-medium); }
.fc-sub-btn:focus-visible, .fc-mode button:focus-visible { outline: 2px solid var(--color-fg); outline-offset: 2px; }
.fc-sub[hidden] { display: none !important; }
.fc-intro { display: grid; gap: 6px; max-width: 900px; }
.fc-intro h2 { margin: 0; }
.fc-how { margin: 0; padding: 8px 12px; border-left: 3px solid var(--fc-key); background: color-mix(in srgb, var(--fc-key) 7%, transparent); border-radius: 0 var(--cds-radius) var(--cds-radius) 0; }
.fc-bar-top { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; margin: 12px 0 8px; }
.fc-legend { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: var(--cds-font-size-caption); color: var(--color-fg-muted); }
.fc-legend > span { display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; }
.fc-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.fc-dot[data-tone="ok"], .fc-bar [data-tone="ok"] { background: var(--fc-ok); }
.fc-dot[data-tone="warn"], .fc-bar [data-tone="warn"] { background: var(--fc-warn); }
.fc-dot[data-tone="bad"], .fc-bar [data-tone="bad"] { background: var(--fc-bad); }
#tab-fc { --fc-sus: #ea580c; --fc-war: #db2777; }
@media (prefers-color-scheme: dark) { #tab-fc { --fc-sus: #fb923c; --fc-war: #f472b6; } }
.fc-t-s { color: var(--fc-sus); } .fc-t-w { color: var(--fc-war); }
.fc-ic-s, .fc-ic-w { display: inline-block; flex: none; width: 12px; height: 10px; vertical-align: -1px; margin-left: 5px; }
.fc-ic-s { background: linear-gradient(var(--fc-sus), var(--fc-sus)) 0 0 / 100% 2px no-repeat, linear-gradient(var(--fc-sus), var(--fc-sus)) 0 4px / 60% 2px no-repeat, linear-gradient(var(--fc-sus), var(--fc-sus)) 0 8px / 85% 2px no-repeat; }
.fc-ic-w { width: 11px; height: 11px; border-radius: 50%; background: conic-gradient(#ef4444, #f59e0b, #22c55e, #3b82f6, #a855f7, #ec4899, #ef4444); }
.fc-tg .fc-ic-s, .fc-tg .fc-ic-w { margin: 0 5px 0 0; }
.fc-tg { display: inline-flex; align-items: center; font-size: 10px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; padding: 2px 8px; border-radius: 999px; white-space: nowrap; }
.fc-tg-s { color: var(--fc-sus); background: color-mix(in srgb, var(--fc-sus) 13%, transparent); }
.fc-tg-w { color: var(--fc-war); background: color-mix(in srgb, var(--fc-war) 13%, transparent); }
.fc-tgs { display: inline-flex; gap: 4px; margin-left: auto; }
.fc-focus { display: grid; grid-template-columns: auto 1fr; align-items: center; gap: 6px 10px; padding: 10px 12px; border-radius: var(--cds-radius); border: 1px solid var(--color-border-line); background: linear-gradient(90deg, color-mix(in srgb, var(--fc-sus) 7%, transparent), color-mix(in srgb, var(--fc-war) 7%, transparent)); }
.fc-focus p { grid-column: 1 / -1; margin: 0; }
.fc-how, .fc-focus { max-width: 900px; }
.fc-frame:is([data-hl="semua"], [data-hl="susunan"]) .fc-chip.fc-hs { box-shadow: inset 0 0 0 1.5px var(--fc-sus); }
.fc-frame:is([data-hl="semua"], [data-hl="warna"]) .fc-chip.fc-hw { box-shadow: inset 0 0 0 1.5px var(--fc-war); }
.fc-focus .fc-tg { justify-self: start; font-size: 11px; }
.fc-ctl { display: flex; flex-wrap: wrap; gap: 8px; }
.fc-hlset > span { align-self: center; padding: 0 6px 0 10px; font-size: var(--cds-font-size-caption); color: var(--color-fg-muted); }
.fc-hlset button[data-hl="susunan"][aria-pressed="true"] { background: var(--fc-sus); color: #fff; }
.fc-hlset button[data-hl="warna"][aria-pressed="true"] { background: var(--fc-war); color: #fff; }
.fc-body li.fc-hs, .fc-body li.fc-hw { border-radius: 4px; padding-top: 1px; padding-bottom: 1px; }
.fc-frame:is([data-hl="semua"], [data-hl="susunan"]) .fc-body li.fc-hs { background: color-mix(in srgb, var(--fc-sus) 13%, transparent); }
.fc-frame:is([data-hl="semua"], [data-hl="susunan"]) .fc-body li.fc-hs::before { background: var(--fc-sus); width: 7px; height: 7px; left: 1px; top: .5em; }
.fc-frame:is([data-hl="semua"], [data-hl="warna"]) .fc-body li.fc-hw { background: color-mix(in srgb, var(--fc-war) 12%, transparent); }
.fc-frame:is([data-hl="semua"], [data-hl="warna"]) .fc-body li.fc-hw::before { background: var(--fc-war); width: 7px; height: 7px; left: 1px; top: .5em; }
.fc-frame[data-hl="semua"] .fc-body li.fc-hs.fc-hw { background: linear-gradient(90deg, color-mix(in srgb, var(--fc-sus) 15%, transparent), color-mix(in srgb, var(--fc-war) 15%, transparent)); }
.fc-frame:is([data-hl="semua"], [data-hl="susunan"]) .fc-mini.fc-hs { box-shadow: inset 0 0 0 2px var(--fc-sus); }
.fc-frame:is([data-hl="semua"], [data-hl="warna"]) .fc-mini.fc-hw { box-shadow: inset 0 0 0 2px var(--fc-war); }
.fc-frame:is([data-hl="semua"], [data-hl="susunan"]) .fc-tool.fc-hs { box-shadow: 0 0 0 2px color-mix(in srgb, var(--fc-sus) 55%, transparent); }
.fc-frame:is([data-hl="semua"], [data-hl="warna"]) .fc-tool.fc-hw { box-shadow: 0 0 0 2px color-mix(in srgb, var(--fc-war) 55%, transparent); }
.fc-frame[data-hl="tiada"] :is(.fc-tgs, .fc-ic-s, .fc-ic-w), .fc-frame[data-hl="susunan"] :is(.fc-tg-w, .fc-tool .fc-ic-w), .fc-frame[data-hl="warna"] :is(.fc-tg-s, .fc-tool .fc-ic-s) { display: none; }
.fc-frame[data-hl="susunan"] :is(.fc-body li, .fc-mini, .fc-tool, .fc-chip):not(.fc-hs), .fc-frame[data-hl="warna"] :is(.fc-body li, .fc-mini, .fc-tool, .fc-chip):not(.fc-hw) { opacity: .35; }
.fc-mode { display: inline-flex; border: 1px solid var(--color-border-line); border-radius: 999px; padding: 2px; }
.fc-mode button { appearance: none; border: 0; background: none; font: inherit; font-size: var(--cds-font-size-caption); padding: 3px 14px; border-radius: 999px; color: var(--color-fg-muted); cursor: pointer; }
.fc-mode button[aria-pressed="true"] { background: var(--color-fg); color: var(--color-bg); }
.fc-wrap { overflow: auto; border: 1px solid var(--color-border-line); border-radius: calc(var(--cds-radius) * 1.5); }
@media (min-width: 700px) { .fc-wrap { max-height: 82vh; } }
.fc-sub, .fc-frame, .fc-wrap, .fc-intro, .fc-bar-top { min-width: 0; max-width: 100%; }
.pod .fc-table { min-width: 1560px; table-layout: fixed; border-collapse: separate; border-spacing: 0; font-size: var(--cds-font-size-caption); }
.pod .fc-table th, .pod .fc-table td { width: 19%; padding: 12px; border-bottom: 1px solid var(--color-border-line); vertical-align: top; }
.pod .fc-table .fc-alat { width: 14.33%; }
.pod .fc-table th { position: sticky; top: 0; z-index: 2; white-space: normal; color: var(--color-fg); border-top: 4px solid var(--fc-accent); border-bottom: 1px solid var(--color-border-line);
  background: linear-gradient(color-mix(in srgb, var(--fc-accent) 16%, transparent), color-mix(in srgb, var(--fc-accent) 16%, transparent)) var(--color-bg); }
.pod .fc-table td { background: var(--color-bg); }
.pod .fc-table td.fc-alat { background: color-mix(in srgb, var(--fc-accent) 7%, var(--color-bg)); }
.pod .fc-table th.fc-c2:not(.fc-alat), .pod .fc-table th.fc-c3:not(.fc-alat), .pod .fc-table td.fc-c2:not(.fc-alat), .pod .fc-table td.fc-c3:not(.fc-alat) { border-left: 6px solid var(--color-panel); }
.pod .fc-table tbody tr:hover td { background: color-mix(in srgb, var(--fc-accent) 5%, var(--color-bg)); }
.pod .fc-table tbody tr:hover td.fc-alat { background: color-mix(in srgb, var(--fc-accent) 12%, var(--color-bg)); }
.pod .fc-table tbody tr:last-child td { border-bottom: 0; border-top: 2px dashed var(--color-border-line); }
.fc-hname { display: flex; align-items: center; gap: 8px; font-size: var(--cds-font-size-body); font-weight: var(--cds-font-weight-medium); }
.fc-hsub { display: block; color: var(--color-fg-muted); font-weight: 400; margin-top: 2px; }
.fc-flag { font-size: 10px; letter-spacing: .06em; padding: 1px 7px; border-radius: 999px; background: var(--fc-accent); color: var(--fc-on); }
.fc-bar { display: flex; height: 6px; border-radius: 3px; overflow: hidden; margin: 8px 0 4px; gap: 2px; }
.fc-count { display: block; color: var(--color-fg-muted); font-weight: 400; font-size: 11px; }
.fc-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-bottom: 6px; }
.fc-tag { font-size: 10px; font-weight: var(--cds-font-weight-medium); letter-spacing: .06em; color: var(--fc-accent); }
.fc-st { font-size: 10px; letter-spacing: .04em; padding: 1px 7px; border-radius: 999px; border: 1px solid var(--fc-accent); color: var(--fc-accent); }
.fc-title { display: flex; align-items: center; gap: 8px; font-size: var(--cds-font-size-body); line-height: 1.3; }
.fc-num { flex: none; width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center; background: var(--fc-accent); color: var(--fc-on); font-size: 13px; font-weight: 700; }
.fc-det { display: grid; gap: 8px; margin-top: 8px; }
.pod .fc-table ul.fc-body { list-style: none; margin: 0; padding: 0; display: grid; gap: 5px; line-height: 1.45; }
.fc-body li { position: relative; padding-left: 14px; }
.fc-body li::before { content: ""; position: absolute; left: 2px; top: .55em; width: 5px; height: 5px; border-radius: 50%; background: var(--fc-accent); }
.fc-minis { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
.fc-mini { border-radius: var(--cds-radius); padding: 6px 8px; display: grid; gap: 2px; background: color-mix(in srgb, var(--fc-accent) 9%, transparent); line-height: 1.35; }
.fc-mini b { color: var(--fc-accent); }
.fc-chips { display: flex; flex-wrap: wrap; gap: 5px; }
.fc-chip { display: inline-flex; align-items: flex-start; gap: 6px; padding: 3px 9px 3px 3px; border-radius: 12px; font-size: 12px; line-height: 1.4; }
.fc-chip i { flex: none; font-style: normal; font-weight: 700; font-size: 10px; width: 16px; height: 16px; border-radius: 50%; display: grid; place-items: center; margin-top: 1px; }
.fc-key { background: color-mix(in srgb, var(--fc-key) 12%, transparent); color: var(--fc-key); }
.fc-key i { background: var(--fc-key); color: var(--fc-on); }
.fc-warn { background: color-mix(in srgb, var(--fc-warn) 14%, transparent); color: var(--fc-warn); }
.fc-warn i { background: var(--fc-warn); color: var(--fc-on); }
.pod .fc-table ul.fc-tools { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
.fc-tool { --t: var(--fc-ok); background: var(--color-bg); border: 1px solid var(--color-border-line); border-left: 4px solid var(--t); border-radius: var(--cds-radius); padding: 6px 8px; display: grid; gap: 2px; line-height: 1.35; }
.fc-tool[data-tone="warn"] { --t: var(--fc-warn); } .fc-tool[data-tone="bad"] { --t: var(--fc-bad); }
.fc-tool-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 6px; }
.fc-tool-top b { overflow-wrap: anywhere; }
.fc-stat { flex: none; font-size: 10px; font-weight: var(--cds-font-weight-medium); color: var(--t); white-space: nowrap; }
.fc-stat::before { content: ""; display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: var(--t); margin-right: 4px; vertical-align: 1px; }
.fc-desc { color: var(--color-fg-muted); }
.fc-frame[data-mode="ringkas"] .fc-det, .fc-frame[data-mode="ringkas"] .fc-desc { display: none; }
.pod .fc-frame[data-mode="ringkas"] .fc-table { min-width: 1150px; }
"""

JS = """(() => {
  const box = document.getElementById('fc-design');
  if (box) box.innerHTML = HTML;
  const btns = [...document.querySelectorAll('.fc-sub-btn')];
  const open = (id) => btns.forEach((b) => {
    const on = b.dataset.sub === id;
    b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1;
    const p = document.getElementById(b.dataset.sub); if (p) p.hidden = !on;
  });
  btns.forEach((b) => b.addEventListener('click', () => open(b.dataset.sub)));
  const frame = document.querySelector('#tab-fc .fc-frame');
  const mb = [...document.querySelectorAll('#tab-fc .fc-modeset button')];
  const hb = [...document.querySelectorAll('#tab-fc .fc-hlset button')];
  const setHl = (h) => {
    if (!frame) return;
    frame.dataset.hl = h;
    hb.forEach((b) => b.setAttribute('aria-pressed', b.dataset.hl === h ? 'true' : 'false'));
    try { localStorage.setItem('fc-hl', h); } catch (e) {}
  };
  hb.forEach((b) => b.addEventListener('click', () => setHl(b.dataset.hl)));
  try { const h = localStorage.getItem('fc-hl'); if (['semua', 'susunan', 'warna', 'tiada'].includes(h)) setHl(h); } catch (e) {}
  const setMode = (m) => {
    if (!frame) return;
    frame.dataset.mode = m;
    mb.forEach((b) => b.setAttribute('aria-pressed', b.dataset.mode === m ? 'true' : 'false'));
    try { localStorage.setItem('fc-mode', m); } catch (e) {}
  };
  mb.forEach((b) => b.addEventListener('click', () => setMode(b.dataset.mode)));
  try { const m = localStorage.getItem('fc-mode'); if (m === 'ringkas' || m === 'penuh') setMode(m); } catch (e) {}
})();
"""

LINK = '<link rel="stylesheet" href="fc.css">'
SCRIPT = JS_S + '\n<script src="fc.js"></script>\n' + JS_E

BTN = ('    <button type="button" class="pod-tab-btn" role="tab" id="btn-fc" data-tab="tab-fc" aria-controls="tab-fc" '
       'aria-selected="false" tabindex="-1">FC</button>\n')

# Blok versi pertama (26 Nov) tanpa penanda: dikenal dan diganti sekali.
OLD_CSS = re.compile(r"/\* FC tab \*/.*?(?=</style>)", re.S)
OLD_TAB = re.compile(r'<section id="tab-fc".*?<!-- FC:DESIGN END -->\n</section>\n</section>\n', re.S)
OLD_JS = re.compile(r"<script>\n\(\(\) => \{\n  const btns = \[\.\.\.document\.querySelectorAll\('\.fc-sub-btn'\)\];.*?</script>\n", re.S)


def put(s, a, b, new, old=None, insert=None):
    """Ganti blok antara penanda a..b; jika tiada, ganti blok lama (old) atau sisip (insert(s, new))."""
    if a in s:
        return re.sub(re.escape(a) + ".*?" + re.escape(b), lambda m: new, s, count=1, flags=re.S)
    if old and old.search(s):
        return old.sub(lambda m: new + "\n", s, count=1)
    return insert(s, new)


def ins_before(anchor):
    def f(s, new):
        a = s.index(anchor)
        return s[:a] + new + "\n" + s[a:]
    return f


def ins_after_last_script(s, new):
    a = s.rindex("</script>") + len("</script>")
    return s[:a] + "\n" + new + s[a:]


def main(path, out):
    import json
    import os
    s = open(path, encoding="utf-8").read()
    if 'id="btn-fc"' not in s:
        a = s.index('data-tab="tab-daftar"')
        a = s.index("\n", a) + 1
        s = s[:a] + BTN + s[a:]
    if "#tab-fc { break-before" not in s and "#tab-fc," not in s:
        s = s.replace("#tab-daftar { break-before", "#tab-daftar, #tab-fc { break-before", 1)
    s = OLD_CSS.sub("", s, count=1)
    s = re.sub(re.escape(CSS_S) + ".*?" + re.escape(CSS_E) + "\n?", "", s, count=1, flags=re.S)
    if LINK not in s:
        a = s.index('<link rel="stylesheet"')
        s = s[:a] + LINK + "\n" + s[a:]
    s = put(s, TAB_S, TAB_E, SECTION, OLD_TAB, ins_before("</div>\n\n<script>\nwindow.POD = window.POD || {};"))
    s = put(s, JS_S, JS_E, SCRIPT, OLD_JS, ins_after_last_script)
    open(path, "w", encoding="utf-8").write(s)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "fc.css"), "w", encoding="utf-8").write(CSS)
    open(os.path.join(out, "fc.js"), "w", encoding="utf-8").write(
        "/* Dijana oleh scripts/build_fc_design.py; jangan ubah secara manual. */\n(() => {\nconst HTML = "
        + json.dumps(content(), ensure_ascii=False) + ";\n" + JS.split("\n", 1)[1])
    print(f"ok: {path} ({len(s.encode())} bait), fc.css, fc.js; {len(ROWS)} baris x 6 lajur")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
