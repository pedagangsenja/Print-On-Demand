"""Tab FC > Design v1.2 dalam dashboard: carta aliran lettering Standard v1.2 (carta lorong / swimlane).

Lajur = siapa buat (Anda, Claude, Skrip Python, Model AI, Platform luar). Baris = turutan langkah 1 → 9.
Garisan: aliran utama, gelung ulang, tolak (kembali), suapan balik. Klik kotak untuk butiran penuh.

Sumber isi: docs/lettering-standard.md (v1 dipersetujui 25 Nov 2026; v1.2 diluluskan 26 Nov 2026; K7/K8 27 Nov)
dan tab Aliran (langkah 6–11). Status alat = keadaan 26–27 Nov 2026
(bukti: designs/lettering-v1/*, scripts/lettering/*, data/export/setup/*.json).

CARA UBAH (pengguna sebut ID kotak, cth. "ubah 5b: ..."):
  - Kotak  : senarai NODES. Setiap kotak = dict(id, lorong, baris, tajuk, butiran, alat, jenis).
             lorong = indeks dalam LANES; baris = kedudukan menegak (0 = atas). Dua kotak tidak boleh di lorong + baris sama.
             jenis "kep" = titik keputusan / kelulusan (bingkai berbeza).
  - Garisan: senarai EDGES. (dari, ke, jenis, label, bentuk[, gap]).
             jenis: utama | ulang | tolak | balik.  bentuk: v (lurus ke bawah), hv (melintang dahulu, kemudian turun),
             vh (turun dahulu, kemudian melintang), h (melintang, baris sama), back (gelung naik melalui lorong celah;
             gap = nombor celah, 0 = kiri lajur Anda, 5 = kanan lajur terakhir; jika tiada, dipilih automatik).
  - Fasa   : PHASES (nombor depan ID kotak menentukan fasa).

Guna: python3 scripts/build_fc_design.py <index.html> <folder keluar>
  Ubah index.html (butang tab FC, rangka seksyen, pautan fc.css / fc.js) dan tulis fc.css + fc.js ke folder keluar.
  Isi carta dan gaya dalam fail berasingan kerana stor dashboard menghadkan setiap dokumen kepada 256 KB.
"""
import html
import json
import re
import sys

E = html.escape
OK, PART, NO = ("ada", "ok"), ("sebahagian", "warn"), ("belum dibina", "bad")
TESTED = ("diuji 24 Nov", "warn")
GPU = ("belum diuji", "warn")

LANES = [("Anda", "lulus, tolak, pilih"), ("Claude", "baca, isi, semak"), ("Skrip Python", "bina, ukur, betulkan"),
         ("Model AI", "jana imej"), ("Platform luar", "Printify, Pinterest")]

PHASES = {"1": "Kad Gaya", "2": "Ayat", "3": "Prompt", "4": "Jana", "5": "QC hitam putih",
          "6": "Warna + kemasan", "7": "Lulus akhir", "8": "Simpan", "9": "Serahan"}

A, C, S, M, P = range(5)  # lorong

NODES = [
    # ---------- 1. Kad Gaya ----------
    dict(id="1a", lorong=A, baris=0, tajuk="Upload imej rujukan",
         butiran=["Upload imej rujukan gaya", "1a simpan rujukan di tempat kekal"],
         alat=[("Tab Daftar S/C", "1a simpan rujukan", OK)]),
    dict(id="1b", lorong=C, baris=1, tajuk="Semak pendua dalam S&C",
         butiran=["1b semak pendua dalam S&C", "Gaya lama: guna kad dalam S&C; gaya baharu: isi kad (1c)"],
         alat=[("Tab Daftar S/C", "1b semak pendua", OK)]),
    dict(id="1u", lorong=S, baris=1, tajuk="Ukur gambar upload",
         butiran=["Ukuran rujukan (v1.2): nisbah tinggi baris, ruang tepi, saiz label dan sudut condong diukur daripada upload, bukan diteka",
                  "Rujukan diukur daripada upload: K3 condong 7.6°, K7 12.4°, K8 7.4°; ruang tepi sisi dan atas / bawah berasingan",
                  "Angka disimpan dalam Kad Gaya dan dipakai oleh pembetulan skrip (5b)"],
         alat=[("skrip/SK05_ukur.py (Python)", "ukur gambar upload dan imej mentah: ruang tepi, kedudukan, condong, kelabu", PART),
               ("Skrip ukuran rujukan (Python)", "simpan angka dalam kad (v1.2)", NO)]),
    dict(id="1c", lorong=C, baris=2, tajuk="Isi Kad Gaya (16 medan)",
         butiran=["1c isi kad 16 medan; setiap medan = semakan QC (ya / tidak) + frasa prompt",
                  "2–3 ciri teras wajib lulus; unsur berisiko; senarai jangan salin; julat panjang ayat",
                  "Warna C berasingan: peranan + nama warna untuk prompt",
                  "Kunci 1: Kad Gaya satu-satunya sumber gaya"],
         alat=[("kad.py (Python)", "Kad Gaya K1–K6, ciri QC + frasa prompt", PART)]),
    dict(id="1d", lorong=A, baris=3, jenis="kep", tajuk="Lulus Kad Gaya?",
         butiran=["1d anda luluskan kad (~2 minit)", "Titik kelulusan 1 daripada 4",
                  "Tolak: kad kembali kepada Claude (1c)"],
         alat=[]),
    dict(id="1e", lorong=M, baris=4, tajuk="Imej bukti → imej sauh",
         butiran=["1e imej bukti (ayat pendek, 2 seed) jadi imej sauh",
                  "Imej sauh dipakai sebagai banding semasa QC (5a) dan helaian kelulusan (5d)"],
         alat=[("gen_moss.py / gen.py", "1e imej bukti, 2 seed", OK)]),

    # ---------- 2. Ayat ----------
    dict(id="2a", lorong=C, baris=5, tajuk="Ayat asal + saringan trademark",
         butiran=["Ayat asal; saringan trademark bertulis, hasil direkod"],
         alat=[("USPTO", "saringan bertulis, hasil direkod", NO)]),
    dict(id="2b", lorong=S, baris=6, tajuk="Spesifikasi Teks + ukur kesukaran",
         butiran=["Ukur kesukaran: bilangan perkataan, perkataan 7+ huruf, perkataan berulang",
                  "Hasil: Spesifikasi Teks (rujukan ejaan untuk QC)"],
         alat=[("kad.py (Python)", "Spesifikasi Teks + ukur kesukaran", PART)]),
    dict(id="2c", lorong=C, baris=7, tajuk="Peranan perkataan + pilih laluan",
         butiran=["Kata isi = utama; kata fungsi = penyambung; perkataan 7+ huruf jadi utama",
                  "Sokongan dan penyambung HURUF BESAR kecuali kad wajibkan skrip",
                  "Laluan 1 (standard v1): 1–4 perkataan. AI penuh, satu blok",
                  "Laluan 2 (standard v1): 5–8 perkataan. AI penuh, hierarki wajib",
                  "Laluan 3 (percubaan): 9–16 perkataan. Hibrid. Belum diuji; perlu kelulusan anda",
                  "Laluan 4 (percubaan): 17+ perkataan. Font dahulu. Belum diuji; perlu kelulusan anda"],
         alat=[("Font berlesen", "laluan 3–4 (percubaan)", NO)]),

    # ---------- 3. Prompt ----------
    dict(id="3c", lorong=C, baris=8, tajuk="Model baharu: tulis aturan r0",
         butiran=["Kaedah model baharu (3.12): kaji sumber rasmi → jawab borang 10 soalan → tulis aturan r0 → simpan untuk model itu sahaja → ujian kelayakan",
                  "Setiap model ada standard prompt sendiri dalam daftar aturan; model belum berdaftar memakai rangka am (rev am)",
                  "Ujian kelayakan sekali bagi setiap model baharu: setiap gaya × ayat pendek dan sederhana × 2 seed; sah untuk gabungan tetapan yang dikunci sahaja",
                  "Lulus: ≥ 90% imej ejaan betul, gaya ≥ 7/8, tiada teks liar",
                  "Diuji banding dengan rangka am pada seed 42, 7, 123",
                  "Menunggu ujian kelayakan: FLUX 3 Image Klein, Qwen-Image-2512, GLM-Image (aturan r0)"],
         alat=[("Borang 10 soalan model baharu", "standard 3.12; aturan baharu disimpan di 3.14", OK),
               ("gen.py + run_k6.py", "ujian kelayakan setiap enjin", OK)]),
    dict(id="3a", lorong=S, baris=8, tajuk="Bina prompt ikut aturan model",
         butiran=["Isi sama untuk semua model: Kad Gaya + Spesifikasi Teks (8 blok isi)",
                  "Cara menulis ikut aturan model; aturan tidak boleh menambah atau membuang ciri gaya",
                  "7 model ada aturan: 4 sudah diuji (r1), 3 daripada sumber rasmi sahaja dan belum diuji (r0)",
                  "Model tanpa aturan sendiri: rangka am 9 bahagian (pembina v1.1)",
                  "Hitam putih sahaja; tiada negative prompt; tiada nama warna, hex, nombor atau nama font",
                  "Aturan belajar selepas setiap batch (3.15): QC, ♥ dan tolak anda menentukan ubahan; ubahan yang menang terus naik rev; direkod dalam Catatan pembaikan",
                  "Bukti lemah (K3 × 1 ayat × 3 seed, 26 Nov): ejaan betul 6/12 dengan rangka am, 11/12 dengan aturan model",
                  "Larian v1.2 pertama (26 Nov malam, 3 design × 5 model × 3 seed, CPU): 33/45 imej lulus ejaan; bukti lemah",
                  "klein 4B: satu perenggan prosa; satu ayat setiap baris; gaya ditulis terus selepas perkataan; had dalam satu ayat di hujung",
                  "Z-Image Turbo: huraian panjang seperti kapsyen; baris bernombor; had ditulis sebagai ayat positif",
                  "ERNIE Turbo: prompt mentah pendek + penambah prompt rasmi sekali (seed 42); hasil disemak sebelum jana",
                  "MOSS + LoRA: satu objek JSON; satu butir dan satu kotak piksel bagi setiap baris",
                  "FLUX 3 Image Klein (r0, diuji di CPU: 9/9; lesen diterima 27 Nov 2026): kapsyen penuh + jadual kotak JSON grid 0–1000; boleh dipakai untuk design jualan ikut syarat lesen",
                  "Qwen-Image-2512 (r0, belum diuji): kurang 200 perkataan; setiap baris = kedudukan, perkataan dalam petikan, gaya",
                  "GLM-Image (r0, belum diuji): naratif bersambung tanpa senarai; setiap baris = kedudukan, fungsi, perkataan dalam petikan, gaya font"],
         alat=[("pembina.py (Python)", "prompt 7 model daripada 8 kad + semakan 3.11; larian pertama: 33/45 imej lulus ejaan", OK),
               ("pembina.py --daftar", "daftar aturan setiap model: bahagian standard, rev, status, sumber", OK),
               ("khas.py (Python)", "7 aturan sebagai contoh tulisan tangan (K3 × ayat H); rekod ujian pertama sahaja", PART)]),
    dict(id="3b", lorong=S, baris=9, tajuk="Semak prompt sebelum jana",
         butiran=["Semak automatik sebelum jana; prompt yang gagal tidak dijana"],
         alat=[("kad.py: bina() + semak() (Python)", "rangka am hitam putih (v1.1) + semakan automatik", PART)]),

    # ---------- 4. Jana ----------
    dict(id="4b", lorong=S, baris=10, tajuk="Langkau model bermasalah",
         butiran=["Peraturan langkau (26 Nov): turutan MOSS → ERNIE → Z-Image → klein 4B; model terlalu lama atau gagal 3 cubaan dilangkau, model seterusnya terus jalan",
                  "Terlalu lama = lebih 20 minit muat turun + 13 minit setiap imej (disahkan anda 26 Nov)",
                  "Setiap langkau direkod (langkau.jsonl) dan dilaporkan dalam chat; langkau bukan gagal QC"],
         alat=[("run_v12.sh", "jana ikut pembina, satu model satu masa, dengan langkau; dipakai untuk larian pertama", OK)]),
    dict(id="4a", lorong=M, baris=10, tajuk="Jana hitam putih",
         butiran=["Jana hitam putih dahulu: dakwat putih atas latar hitam, tiada warna lain",
                  "Tetapan dikunci dalam profil model; enjin diffusers",
                  "Profil dikunci v1.2: klein 4B, Z-Image Turbo, ERNIE Turbo, MOSS + LoRA; setiap satu dengan aturan prompt sendiri",
                  "Model utama: MOSS dan ERNIE (12/12 pada S1–S6); klein 4B 6/12",
                  "Kunci 3: model hanya untuk gaya yang ia lulus",
                  "Seed tetap 42, 7, 123, 2024: laluan 1 = 2 seed, laluan 2 = 3–4",
                  "Satu model besar pada satu masa; semak RAM dan disk dahulu",
                  "Log lengkap setiap imej; imej mentah disimpan sebelum sesi tamat",
                  "Masa setiap imej di CPU (log 26 Nov, bukti lemah): klein 85–118 s, Z-Image kira-kira 260 s, ERNIE 305–373 s, MOSS 337–392 s",
                  "Larian pertama: MOSS 6/9, ERNIE 8/9, Z-Image 4/9, klein 4B 6/9, FLUX 3 Klein 9/9 (CPU, 357 s setiap imej); Qwen-2512 dan GLM-Image dilangkau: tidak muat RAM 15 GB",
                  "3 model tambahan melalui Space Hugging Face (GPU, kuota harian): FLUX 3 Image Klein, Qwen-Image-2512, GLM-Image",
                  "Tidak dipilih: FLUX.1 schnell (3/30 ejaan betul), Chroma1-Flash (0/6); simpanan: Ovis-Image-7B"],
         alat=[("gen_moss.py", "MOSS SFT + LoRA", OK),
               ("gen.py", "ERNIE, klein 4B, Z-Image, schnell, Chroma, Kandinsky", OK),
               ("gen_flux3.py", "FLUX 3 Image Klein di CPU (pipeline modular diffusers)", OK),
               ("gen.py: PROFIL", "profil setiap model dikunci", PART),
               ("Kaggle GPU (GEN_DEVICE)", "banding CPU vs GPU", GPU),
               ("gen_hf_space.py", "profil Space untuk FLUX 3 Klein, Qwen-Image-2512, GLM-Image", NO)]),

    # ---------- 5. QC hitam putih ----------
    dict(id="5c", lorong=A, baris=11, jenis="kep", tajuk="Masih gagal: anda putuskan",
         butiran=["Had 2 pusingan → tukar model → pendekkan ayat → lapor kepada anda",
                  "Anda putuskan langkah seterusnya"],
         alat=[]),
    dict(id="5a", lorong=C, baris=11, tajuk="QC: ejaan, ayat, gaya",
         butiran=["QC pada imej hitam putih dahulu: ejaan, ayat, gaya",
                  "3 pintu wajib; ejaan huruf demi huruf ikut Spesifikasi Teks; OCR hanya menanda",
                  "Ciri kad ≥ 7/8 + ciri teras wajib; banding dengan upload dan imej sauh",
                  "Ciri sejagat: boleh dibaca kecil, tiada teks terpotong, margin cukup",
                  "Kitaran QC (v1.2): cacat pada satu seed = tukar seed, prompt tidak diubah",
                  "Cacat sama pada 2 daripada 3 seed = reka semula prompt model itu, satu ubahan setiap pusingan, seed sama",
                  "Had 2 pusingan → tukar model → pendekkan ayat → lapor; pembaikan berjaya ditulis balik ke aturan model",
                  "Selepas SETIAP batch (termasuk semua lulus): belajar.py baca QC, ♥ dan tolak → satu ubahan seterusnya bagi setiap model (3.15)",
                  "Kunci 2: QC sama untuk semua model",
                  "Kunci 5: kitaran QC tetap; pembetulan skrip bila perlu sahaja"],
         alat=[("Claude + helaian semakan", "3 pintu, ciri kad ≥ 7/8", OK),
               ("RapidOCR", "hanya menanda (skor 0.33–0.88 pada ejaan betul)", TESTED),
               ("qc/<model>.json", "rekod QC setiap imej; hasil → jadual model × gaya", PART),
               ("belajar.py", "belajar selepas setiap batch; TINDAKAN setiap model (3.15)", OK)]),
    dict(id="5b", lorong=S, baris=12, tajuk="Pembetulan skrip (SK01–SK04)",
         butiran=["5b Pembetulan skrip (v1.2), selepas 3 pintu lulus: condong, ruang tepi, kedudukan, hitam putih bersih",
                  "5b hanya jalan bila ukuran tersasar daripada ukuran rujukan kad; ejaan dan bentuk huruf mesti jana semula",
                  "Daftar skrip: SK01 condong, SK02 ruang tepi, SK03 kedudukan, SK04 hitam putih bersih, SK05 ukuran (26 Nov); SK06 finish.py (dibawa masuk, --palet 27 Nov); SK07 warna ikut peranan, SK08 bayang (dibina 27 Nov)",
                  "Larian pertama: 33 imej dibetulkan (condong, ruang tepi, kedudukan, hitam putih), 0 gagal semakan akhir",
                  "Skrip baharu: bila gambar upload ada ciri yang tiada skrip → tulis, simpan di skrip/<ID>_<nama>.py, uji pada imej sedia ada, daftar, kemas kini standard + dashboard, beritahu anda"],
         alat=[("skrip/betulkan.py: SK01–SK04 (Python)", "ukur, betulkan, ukur semula; dipakai pada 33 imej larian pertama; had toleransi diluluskan 27 Nov", OK),
               ("Daftar skrip + kaedah skrip baharu", "dalam standard, selepas langkah 6", OK)]),
    dict(id="5d", lorong=A, baris=13, jenis="kep", tajuk="Lulus design hitam putih?",
         butiran=["Mata anda pintu terakhir (v1.2): imej lulus QC tetapi nampak buruk = gagal",
                  "Papar upload, imej sauh dan hasil sebelah-menyebelah + skor QC; anda pilih daripada satu helaian",
                  "Sebab tolak daripada senarai tetap; disalur balik ke kad, aturan model, jadual model × gaya atau ulangan",
                  "Had bilangan imej setiap helaian",
                  "Titik kelulusan: hitam putih lulus QC (4 titik: kad, contoh pertama laluan 3–4, hitam putih, hasil akhir berwarna)"],
         alat=[("Paparan sebelah-menyebelah", "upload, imej sauh, hasil + skor QC", NO)]),

    # ---------- 6. Warna + kemasan ----------
    dict(id="6a", lorong=C, baris=14, tajuk="Pilih warna C + latar",
         butiran=["Bermula hanya selepas QC hitam putih lulus",
                  "Pilih warna C dan warna latar yang padan dengan jenis ayat, ikon dan gaya S (tab Aliran)"],
         alat=[]),
    dict(id="6b", lorong=S, baris=15, tajuk="Vektor + warna C + kemasan",
         butiran=["Urutan (27 Nov): SK07 warna ikut peranan → SK08 bayang → SK06 vektor + tekstur + saiz cetak; satu arahan: skrip/kemasan.py",
                  "SK07: setiap baris ikut peranan Spesifikasi Teks (utama, sokongan, label, hiasan); baris bertaut dibelah; GAGAL = kekal hitam putih",
                  "SK08: bayang 3D dalam huruf ikut ukuran gambar upload (K3: bawah setiap strok skrip kelabu cerah, IMG_5775)",
                  "Parameter daripada kad: margin, tekstur, bilangan dakwat, butiran halus",
                  "Warna C diletak oleh skrip ikut peranan: 1 imej → beberapa warna C (--warna Cxxx)",
                  "Seed tekstur berbeza setiap design",
                  "Simpan SVG induk; PNG besar dijana semula bila perlu",
                  "F1 (v1): vektor rata · F2 (v1): rata + tekstur · F3: raster, ditangguh",
                  "Kunci 4: AI jana hitam putih; skrip letak warna, margin, tekstur selepas QC lulus",
                  "Selepas SETIAP batch (Belajar SK, 27 Nov): belajar_sk.py baca log SK, semakan Claude, ♥ dan tolak → baiki SK, tambah parameter kad, atau cipta SK baharu terus"],
         alat=[("belajar_sk.py", "belajar SK selepas 5b + langkah 6; ubahan pertama SK07 v1.1 belah_leher MENANG (13/15 → 15/15); seterusnya parameter tekstur SK06", OK),
               ("skrip/SK07_warna.py", "v1.1: warna ikut peranan; huruf bertaut dibelah pada leher; 14 imej K3K: 13 lulus, 1 GAGAL dikesan betul (tiada label)", OK),
               ("skrip/SK08_bayang.py", "bayang dalam huruf K3, diukur pada IMG_5775; bayang lembut K1 belum", PART),
               ("skrip/SK06_finish.py", "F1 / F2; palet tepat dengan --palet; margin dan tekstur masih tetap dalam skrip", PART),
               ("skrip/kemasan.py", "SK07 → SK08 → SK06 satu arahan", OK)]),
    dict(id="6c", lorong=C, baris=16, tajuk="QC kali kedua (berwarna)",
         butiran=["QC dua kali: imej mentah hitam putih, dan selepas warna + kemasan",
                  "Semak automatik: bilangan lapisan dan dakwat yang hilang"],
         alat=[]),

    # ---------- 7. Lulus akhir ----------
    dict(id="7a", lorong=A, baris=17, jenis="kep", tajuk="Lulus design berwarna?",
         butiran=["Titik kelulusan: hasil akhir berwarna", "Tolak: kembali ke pilihan warna (6a)"],
         alat=[]),
    dict(id="7b", lorong=A, baris=18, jenis="kep", tajuk="Simpan: A atau SNC",
         butiran=["Selepas setiap jana imej: A = simpan di tab AI Image Test (image_log)",
                  "SNC = daftar di tab Daftar S/C: gaya S + warna C",
                  "Anda padam sendiri yang tidak mahu dalam Daftar S/C"],
         alat=[("Tab AI Image Test / Daftar S/C", "pilih A atau SNC selepas setiap jana", OK)]),

    # ---------- 8. Simpan ----------
    dict(id="8a", lorong=C, baris=19, tajuk="Simpan rekod S, C + design",
         butiran=["Rekod S: Kad Gaya + templat prompt tanpa perkataan + model lulus + versi kad",
                  "Rekod C: peranan + nama warna; satu sumber kod hex",
                  "Daftar design lulus: ayat, S, C, model, seed, fail induk",
                  "Semua fail disimpan sebelum sesi tamat",
                  "Kad K7 dan K8 diluluskan 27 Nov; 24 imej lulus didaftar sebagai S012–S035, warna C009 dan C010"],
         alat=[("Tab Daftar S/C", "rekod S dan C", OK),
               ("Kad Gaya berstruktur dalam stor", "templat, model lulus, versi", NO),
               ("Daftar design", "ayat, S, C, model, seed, fail induk", NO)]),

    # ---------- 9. Serahan ----------
    dict(id="9a", lorong=C, baris=20, tajuk="Serahan ke Workflow",
         butiran=["Standard berhenti di serahan kepada Workflow",
                  "Serahan: fail cetak setiap saiz, pratonton, ayat, kod S dan C, hasil trademark"],
         alat=[("USPTO", "w02 hasil saringan dalam serahan", NO)]),
    dict(id="9b", lorong=S, baris=21, tajuk="Mockup produk",
         butiran=["Skrip mockup: Workflow w03"],
         alat=[("Skrip mockup", "w03", NO)]),
    dict(id="9c", lorong=P, baris=22, tajuk="Upload Printify + pin Pinterest",
         butiran=["Printify API: w04; Setup s09: Sedang", "Pinterest API: w05; Setup s15–s18: Belum",
                  "Produk dan pin ditanda kod S / C"],
         alat=[("Printify API", "w04; Setup s09: Sedang", PART), ("Pinterest API", "w05; Setup s15–s18: Belum", NO)]),
    dict(id="9d", lorong=P, baris=23, tajuk="Prestasi ikut kod S / C",
         butiran=["Produk dan pin ditanda kod S / C → tab Prestasi",
                  "Jualan kembali ke S&C: gaya menang dapat lebih ayat dan warna"],
         alat=[("Prestasi (kod S / C)", "tiada dalam dashboard semasa", NO)]),
]

# (dari, ke, jenis, label, bentuk[, gap])
EDGES = [
    ("1a", "1b", "utama", "", "hv"),
    ("1a", "1u", "utama", "gambar upload", "hv"),
    ("1b", "1c", "utama", "", "v"),
    ("1u", "1c", "balik", "angka ukuran", "vh"),
    ("1c", "1d", "utama", "", "hv"),
    ("1d", "1c", "tolak", "tolak", "back"),
    ("1d", "1e", "utama", "lulus", "hv"),
    ("1e", "2a", "utama", "", "hv"),
    ("2a", "2b", "utama", "", "hv"),
    ("2b", "2c", "utama", "", "hv"),
    ("2c", "3a", "utama", "", "hv"),
    ("3a", "3c", "ulang", "tiada aturan", "h"),
    ("3c", "3a", "ulang", "aturan r0", "h"),
    ("3a", "3b", "utama", "", "v"),
    ("3b", "3a", "ulang", "gagal semak", "back"),
    ("3b", "4a", "utama", "lulus", "hv"),
    ("4a", "4b", "ulang", "terlalu lama", "h"),
    ("4b", "4a", "ulang", "model lain", "h"),
    ("4a", "5a", "utama", "", "vh"),
    ("5a", "4a", "ulang", "tukar seed / model", "back"),
    ("5a", "3a", "ulang", "reka semula prompt (maks 2)", "back"),
    ("5a", "5c", "ulang", "masih gagal", "h"),
    ("5a", "5b", "utama", "3 pintu lulus", "vh"),
    ("5b", "5d", "utama", "", "hv"),
    ("5d", "1c", "tolak", "tolak: kad", "back"),
    ("5d", "3a", "tolak", "tolak: aturan model", "back"),
    ("5d", "4a", "tolak", "tolak: jana semula", "back"),
    ("5d", "6a", "utama", "lulus", "vh"),
    ("6a", "6b", "utama", "", "hv"),
    ("6b", "6c", "utama", "", "hv"),
    ("6c", "6b", "ulang", "gagal", "back"),
    ("6c", "7a", "utama", "", "hv"),
    ("7a", "6a", "tolak", "tolak", "back"),
    ("7a", "7b", "utama", "lulus", "v"),
    ("7b", "8a", "utama", "", "hv"),
    ("8a", "9a", "utama", "", "v"),
    ("9a", "9b", "utama", "", "hv"),
    ("9b", "9c", "utama", "", "hv"),
    ("9c", "9d", "utama", "", "v"),
    ("9d", "2a", "balik", "gaya menang: lebih ayat + warna", "back", 5),
]

EDGE_LABEL = {"utama": "aliran utama", "ulang": "gelung ulang / cuba lagi", "tolak": "tolak: kembali ke langkah awal",
              "balik": "suapan balik data"}
TONE_LABEL = {"ok": "ada", "warn": "separuh", "bad": "belum"}

# Geometri (piksel)
PH_W, LANE_W, NW, NH, ROW, TOP = 116, 280, 196, 84, 118, 18
PAD = (LANE_W - NW) // 2
SLOTS = [0, -12, 12, -22, 22, -6, 6]

# Susunan (layout huruf) dan warna: dua faktor utama design; ditonjolkan dalam carta.
SUS = re.compile(r"susun|baris|hierarki|margin|ruang tepi|bentuk huruf|perkataan utama|utama /|kata isi|huruf besar|satu blok|tajuk|condong|kedudukan", re.I)
WAR = re.compile(r"warna|palet|dakwat|latar|Rekod C", re.I)
IC = {"s": '<i class="fc-ic-s" aria-hidden="true"></i>', "w": '<i class="fc-ic-w" aria-hidden="true"></i>'}


def fl(text):
    return ("s" if SUS.search(text) else "") + ("w" if WAR.search(text) else "")


def node_flags(n):
    t = " ".join([n["tajuk"]] + n["butiran"] + [a + " " + b for a, b, _ in n["alat"]])
    return fl(t)


def check():
    ids = [n["id"] for n in NODES]
    assert len(ids) == len(set(ids)), "ID kotak berulang"
    seen = set()
    for n in NODES:
        k = (n["lorong"], n["baris"])
        assert k not in seen, f"dua kotak di lorong + baris sama: {n['id']}"
        seen.add(k)
        assert n["id"][0] in PHASES, f"fasa tiada untuk {n['id']}"
    for e in EDGES:
        assert e[0] in ids and e[1] in ids, f"garisan ke kotak tiada: {e}"
        assert e[2] in EDGE_LABEL, f"jenis garisan tidak dikenal: {e}"


# ---------------- Susun atur garisan ----------------
def box(n):
    x = PH_W + n["lorong"] * LANE_W + PAD
    y = TOP + n["baris"] * ROW
    return x, y


def gap_x(g):
    return PH_W + g * LANE_W


def layout():
    N = {n["id"]: n for n in NODES}
    cx = lambda n: box(n)[0] + NW / 2
    plan = []
    for e in EDGES:
        a, b, typ, lab, shape = e[:5]
        na, nb = N[a], N[b]
        la, lb = na["lorong"], nb["lorong"]
        g = e[5] if len(e) > 5 else None
        if shape == "v":
            ss, ts = "B", "T"
        elif shape == "hv":
            ss, ts = ("R" if lb > la else "L"), ("T" if nb["baris"] > na["baris"] else "B")
        elif shape == "vh":
            ss, ts = ("B" if nb["baris"] > na["baris"] else "T"), ("L" if la < lb else "R")
        elif shape == "h":
            ss, ts = ("R" if lb > la else "L"), ("L" if lb > la else "R")
        else:  # back
            if g is None:
                g = lb if la < lb else lb + 1
            tx = gap_x(g)
            ss = "R" if tx > cx(na) else "L"
            ts = "L" if tx < cx(nb) else "R"
        plan.append(dict(a=a, b=b, typ=typ, lab=lab, shape=shape, gap=g, ss=ss, ts=ts))

    # Agih port pada setiap sisi kotak
    ports = {}
    for i, p in enumerate(plan):
        ports.setdefault((p["a"], p["ss"]), []).append((i, "s", p["b"]))
        ports.setdefault((p["b"], p["ts"]), []).append((i, "t", p["a"]))
    pos = {}
    for (nid, side), lst in ports.items():
        n = N[nid]
        x, y = box(n)
        if side in "LR":
            lst.sort(key=lambda t: (N[t[2]]["baris"], N[t[2]]["lorong"]))
            span, base = NH - 24, y + 12
        else:
            lst.sort(key=lambda t: (N[t[2]]["lorong"], N[t[2]]["baris"]))
            span, base = NW - 60, x + 30
        k = len(lst)
        for j, (i, end, _) in enumerate(lst):
            off = base + span * (j + 1) / (k + 1)
            if side == "L":
                pt = (x, off)
            elif side == "R":
                pt = (x + NW, off)
            elif side == "T":
                pt = (off, y)
            else:
                pt = (off, y + NH)
            pos[(i, end)] = pt

    # Agih trek dalam lorong celah untuk gelung (elak bertindih)
    used = {}
    for i, p in enumerate(plan):
        if p["shape"] != "back":
            continue
        r0, r1 = sorted((N[p["a"]]["baris"], N[p["b"]]["baris"]))
        taken = used.setdefault(p["gap"], [])
        for si, off in enumerate(SLOTS):
            if all(not (r0 <= q1 and q0 <= r1) for (q0, q1, s) in taken if s == si):
                taken.append((r0, r1, si))
                p["track"] = gap_x(p["gap"]) + off
                break
        else:
            p["track"] = gap_x(p["gap"])

    paths = []
    for i, p in enumerate(plan):
        (sx, sy), (tx, ty) = pos[(i, "s")], pos[(i, "t")]
        sh = p["shape"]
        if sh == "v":
            my = (sy + ty) / 2
            pts = [(sx, sy), (sx, my), (tx, my), (tx, ty)] if abs(sx - tx) > 1 else [(sx, sy), (tx, ty)]
        elif sh == "hv":
            pts = [(sx, sy), (tx, sy), (tx, ty)]
        elif sh == "vh":
            pts = [(sx, sy), (sx, ty), (tx, ty)]
        elif sh == "h":
            mx = (sx + tx) / 2
            pts = [(sx, sy), (mx, sy), (mx, ty), (tx, ty)] if abs(sy - ty) > 1 else [(sx, sy), (tx, ty)]
        else:
            k = p["track"]
            pts = [(sx, sy), (k, sy), (k, ty), (tx, ty)]
        pts = [q for j, q in enumerate(pts) if j == 0 or q != pts[j - 1]]
        paths.append((p, pts))
    return paths


def rounded(pts, r=9):
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for j in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[j - 1], pts[j], pts[j + 1]
        l1 = max(abs(x1 - x0), abs(y1 - y0))
        l2 = max(abs(x2 - x1), abs(y2 - y1))
        rr = min(r, l1 / 2, l2 / 2)
        ax = x1 - rr * ((x1 > x0) - (x1 < x0))
        ay = y1 - rr * ((y1 > y0) - (y1 < y0))
        bx = x1 + rr * ((x2 > x1) - (x2 < x1))
        by = y1 + rr * ((y2 > y1) - (y2 < y1))
        d += f" L{ax:.1f},{ay:.1f} Q{x1:.1f},{y1:.1f} {bx:.1f},{by:.1f}"
    d += f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    return d


def label_pos(p, pts):
    """Label di tengah segmen: gelung = segmen keluar (melintang); lain = segmen terpanjang."""
    segs = list(zip(pts, pts[1:]))
    hl = lambda q: abs(q[1][0] - q[0][0])
    if p["shape"] == "back":
        s = max((segs[0], segs[-1]), key=hl)
        if hl(s) < 70:
            s = segs[1]
    else:
        s = max(segs, key=lambda q: abs(q[1][0] - q[0][0]) + abs(q[1][1] - q[0][1]))
    return (s[0][0] + s[1][0]) / 2, (s[0][1] + s[1][1]) / 2


# ---------------- HTML ----------------
def dots(alat):
    return "".join(f'<i data-tone="{st[1]}"></i>' for _, _, st in alat)


def node_html(n):
    x, y = box(n)
    f = node_flags(n)
    cls = " ".join(filter(None, ["fd-n", "fd-kep" if n.get("jenis") == "kep" else "",
                                 "fc-hs" if "s" in f else "", "fc-hw" if "w" in f else ""]))
    tools = (f'<span class="fd-dots">{dots(n["alat"])}</span><span>{len(n["alat"])} alat</span>'
             if n["alat"] else '<span class="fd-none">tiada alat berasingan</span>')
    icons = "".join(IC[c] for c in f)
    return (f'<button type="button" class="{cls}" data-id="{n["id"]}" data-l="{n["lorong"]}" '
            f'style="left:{x}px;top:{y}px;width:{NW}px;height:{NH}px" aria-label="{E(n["id"] + " " + n["tajuk"])}">'
            f'<span class="fd-top"><b class="fd-id">{E(n["id"])}</b><span class="fd-who">{E(LANES[n["lorong"]][0])}</span>{icons}</span>'
            f'<span class="fd-t">{E(n["tajuk"])}</span><span class="fd-tl">{tools}</span></button>')


def canvas():
    rows = max(n["baris"] for n in NODES) + 1
    W = PH_W + len(LANES) * LANE_W + 40
    H = TOP + rows * ROW
    o = []
    # Jalur fasa
    ph = {}
    for n in NODES:
        r = ph.setdefault(n["id"][0], [n["baris"], n["baris"]])
        r[0], r[1] = min(r[0], n["baris"]), max(r[1], n["baris"])
    for k, (r0, r1) in sorted(ph.items()):
        y0 = TOP + r0 * ROW - 14
        h = (r1 - r0 + 1) * ROW
        o.append(f'<div class="fd-ph" data-odd="{int(k) % 2}" style="top:{y0}px;height:{h}px;width:{W}px">'
                 f'<span><b>{E(k)}</b>{E(PHASES[k])}</span></div>')
    for i in range(len(LANES)):
        o.append(f'<div class="fd-lane" data-l="{i}" style="left:{PH_W + i * LANE_W}px;width:{LANE_W}px;height:{H}px"></div>')
    # Garisan
    paths = layout()
    svg, lbl = [], []
    for k, (p, pts) in enumerate(paths):
        attrs = f'data-a="{p["a"]}" data-b="{p["b"]}"'
        svg.append(f'<path class="fd-e fd-{p["typ"]}" {attrs} d="{rounded(pts)}" marker-end="url(#fd-ar-{p["typ"]})"/>')
        if p["lab"]:
            lx, ly = label_pos(p, pts)
            lbl.append(f'<span class="fd-lb fd-{p["typ"]}" {attrs} style="left:{lx:.0f}px;top:{ly:.0f}px">{E(p["lab"])}</span>')
    marks = "".join(f'<marker id="fd-ar-{t}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                    f'orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" class="fd-ah fd-{t}"/></marker>' for t in EDGE_LABEL)
    o.append(f'<svg class="fd-svg" width="{W}" height="{H}" aria-hidden="true"><defs>{marks}</defs>{"".join(svg)}</svg>')
    o.extend(lbl)
    o.extend(node_html(n) for n in NODES)
    head = "".join(f'<div class="fd-lh" data-l="{i}" style="width:{LANE_W}px"><b>{E(a)}</b><span>{E(b)}</span></div>'
                   for i, (a, b) in enumerate(LANES))
    return (f'<div class="fd-scroll"><div class="fd-head" style="width:{W}px"><div class="fd-lh0" style="width:{PH_W}px">Fasa</div>{head}</div>'
            f'<div class="fd-cv" style="width:{W}px;height:{H}px">{"".join(o)}<div class="fd-pop" hidden></div></div></div>')


def summary():
    c = {"ok": 0, "warn": 0, "bad": 0}
    for n in NODES:
        for _, _, st in n["alat"]:
            c[st[1]] += 1
    n = sum(c.values())
    bar = "".join(f'<span data-tone="{k}" style="flex:{v}"></span>' for k, v in c.items() if v)
    txt = " · ".join(f"{v} {TONE_LABEL[k]}" for k, v in c.items() if v)
    return (f'<div class="fd-sum"><b>{n} alat</b><span class="fc-bar" role="img" aria-label="{n} alat: {E(txt)}">{bar}</span>'
            f'<span class="fc-count">{E(txt)}</span></div>')


def data_json():
    lanes = [a for a, _ in LANES]
    return {"nodes": {n["id"]: dict(t=n["tajuk"], l=lanes[n["lorong"]], li=n["lorong"], f=PHASES[n["id"][0]],
                                    k=n.get("jenis", ""), b=n["butiran"],
                                    a=[[x, y, s[0], s[1]] for x, y, s in n["alat"]]) for n in NODES},
            "edges": [[e[0], e[1], e[2], e[3]] for e in EDGES], "elabel": EDGE_LABEL}


def content():
    legend_t = "".join(f'<span><svg width="30" height="8" aria-hidden="true"><line x1="0" y1="4" x2="30" y2="4" class="fd-e fd-{t}"/></svg>{E(l)}</span>'
                       for t, l in EDGE_LABEL.items())
    legend_s = "".join(f'<span><i class="fc-dot" data-tone="{t}"></i>{E(l)}</span>' for t, l in (
        ("ok", "alat ada dan dipakai"), ("warn", "separuh siap / sedang diuji"), ("bad", "belum dibina")))
    legend_s += '<span><i class="fd-kep-ic"></i>titik keputusan / kelulusan</span>'
    return f"""<div class="fc-intro">
<h2>Design v1.2: aliran kerja lettering</h2>
<p class="fc-how"><b>Cara baca:</b> mula di atas (1a), ikut garisan ke bawah hingga 9d. Setiap <b>lajur = siapa buat</b>. Garisan kelabu = aliran utama; <b class="fd-t-ulang">oren putus-putus</b> = gelung ulang; <b class="fd-t-tolak">merah putus-putus</b> = tolak, kembali ke langkah awal; <b class="fd-t-balik">biru bertitik</b> = suapan balik data. Halakan tetikus pada kotak untuk lihat garisannya sahaja; <b>klik kotak</b> untuk butiran penuh, alat dan sambungan. Mahu ubah? Sebut ID kotak dalam chat (cth. "ubah 5b: …").</p>
<p class="pod-muted">Sumber: docs/lettering-standard.md (v1 dipersetujui 25 Nov 2026; v1.2 diluluskan pengguna 26 Nov 2026; K7 dan K8 diluluskan 27 Nov) dan tab Aliran. Laluan 3–4 percubaan, F3 ditangguh. Status alat = keadaan 26–27 Nov 2026.</p>
</div>
<div class="fc-bar-top">
<div class="fd-legends"><div class="fc-legend">{legend_t}</div><div class="fc-legend">{legend_s}</div></div>
<div class="fc-ctl">{summary()}<div class="fc-mode fc-hlset" role="group" aria-label="Tonjolkan"><span>Tonjol</span><button type="button" data-hl="tiada" aria-pressed="true">Tiada</button><button type="button" data-hl="susunan" aria-pressed="false">Susunan</button><button type="button" data-hl="warna" aria-pressed="false">Warna</button></div></div>
</div>
<div class="fc-frame" data-hl="tiada">{canvas()}</div>"""


SECTION = """<!-- FC:TAB START -->
<section id="tab-fc" class="pod-tab" role="tabpanel" aria-labelledby="btn-fc" hidden>
<div class="fc-subbar" role="tablist" aria-label="Sub tab FC">
  <button type="button" class="fc-sub-btn" role="tab" id="btn-fc-design" data-sub="fc-design" aria-controls="fc-design" aria-selected="true">Design v1.2</button>
</div>
<section id="fc-design" class="pod-section pod-first fc-sub" role="tabpanel" aria-labelledby="btn-fc-design"><div class="fc-host" data-draw="fc-design">—</div></section>
</section>
<!-- FC:TAB END -->"""

TAB_S, TAB_E = "<!-- FC:TAB START -->", "<!-- FC:TAB END -->"
CSS_S, CSS_E = "/* FC:CSS START */", "/* FC:CSS END */"
JS_S, JS_E = "<!-- FC:JS START -->", "<!-- FC:JS END -->"

CSS = """#tab-fc { --fc-on: #fff; --fc-ok: var(--color-ok, #1a7f37); --fc-warn: var(--color-warn, #9a6700); --fc-bad: var(--color-bad, #cf222e); --fc-key: #2563eb;
  --fc-sus: #ea580c; --fc-war: #db2777;
  --fd-l0: #2563eb; --fd-l1: #7c3aed; --fd-l2: #15803d; --fd-l3: #0e7490; --fd-l4: #475569;
  --fd-utama: #6b7280; --fd-ulang: #d97706; --fd-tolak: #dc2626; --fd-balik: #2563eb; }
@media (prefers-color-scheme: dark) { #tab-fc { --fc-on: #111; --fc-key: #60a5fa; --fc-sus: #fb923c; --fc-war: #f472b6;
  --fd-l0: #60a5fa; --fd-l1: #a78bfa; --fd-l2: #4ade80; --fd-l3: #22d3ee; --fd-l4: #94a3b8;
  --fd-utama: #9ca3af; --fd-ulang: #fbbf24; --fd-tolak: #f87171; --fd-balik: #60a5fa; } }
.fc-subbar { display: flex; gap: var(--cds-gap-xs); border-bottom: 1px solid var(--color-border-line); }
.fc-sub-btn { appearance: none; background: none; border: 0; border-bottom: 2px solid transparent; margin-bottom: -1px; padding: 4px var(--cds-pad-md); font: inherit; font-size: var(--cds-font-size-caption); color: var(--color-fg-muted); cursor: pointer; }
.fc-sub-btn[aria-selected="true"] { color: var(--color-fg); border-bottom-color: var(--color-fg); font-weight: var(--cds-font-weight-medium); }
.fc-sub-btn:focus-visible, .fc-mode button:focus-visible, .fd-n:focus-visible { outline: 2px solid var(--color-fg); outline-offset: 2px; }
.fc-sub[hidden] { display: none !important; }
.fc-intro { display: grid; gap: 6px; max-width: 900px; }
.fc-intro h2 { margin: 0; }
.fc-how { margin: 0; padding: 8px 12px; border-left: 3px solid var(--fc-key); background: color-mix(in srgb, var(--fc-key) 7%, transparent); border-radius: 0 var(--cds-radius) var(--cds-radius) 0; }
.fd-t-ulang { color: var(--fd-ulang); } .fd-t-tolak { color: var(--fd-tolak); } .fd-t-balik { color: var(--fd-balik); }
.fc-bar-top { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 10px; margin: 12px 0 8px; }
.fd-legends { display: grid; gap: 6px; }
.fc-legend { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: var(--cds-font-size-caption); color: var(--color-fg-muted); }
.fc-legend > span { display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; }
.fc-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.fc-dot[data-tone="ok"], .fc-bar [data-tone="ok"], .fd-dots [data-tone="ok"] { background: var(--fc-ok); }
.fc-dot[data-tone="warn"], .fc-bar [data-tone="warn"], .fd-dots [data-tone="warn"] { background: var(--fc-warn); }
.fc-dot[data-tone="bad"], .fc-bar [data-tone="bad"], .fd-dots [data-tone="bad"] { background: var(--fc-bad); }
.fd-kep-ic { width: 10px; height: 10px; transform: rotate(45deg); border: 2px solid var(--color-fg); display: inline-block; margin: 0 2px; }
.fc-ctl { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; }
.fd-sum { display: flex; align-items: center; gap: 8px; font-size: var(--cds-font-size-caption); }
.fd-sum .fc-bar { width: 120px; }
.fc-bar { display: flex; height: 6px; border-radius: 3px; overflow: hidden; gap: 2px; }
.fc-count { color: var(--color-fg-muted); font-size: 11px; }
.fc-ic-s, .fc-ic-w { display: inline-block; flex: none; width: 12px; height: 10px; vertical-align: -1px; margin-left: 4px; }
.fc-ic-s { background: linear-gradient(var(--fc-sus), var(--fc-sus)) 0 0 / 100% 2px no-repeat, linear-gradient(var(--fc-sus), var(--fc-sus)) 0 4px / 60% 2px no-repeat, linear-gradient(var(--fc-sus), var(--fc-sus)) 0 8px / 85% 2px no-repeat; }
.fc-ic-w { width: 11px; height: 11px; border-radius: 50%; background: conic-gradient(#ef4444, #f59e0b, #22c55e, #3b82f6, #a855f7, #ec4899, #ef4444); }
.fc-mode { display: inline-flex; border: 1px solid var(--color-border-line); border-radius: 999px; padding: 2px; }
.fc-mode button { appearance: none; border: 0; background: none; font: inherit; font-size: var(--cds-font-size-caption); padding: 3px 14px; border-radius: 999px; color: var(--color-fg-muted); cursor: pointer; }
.fc-mode button[aria-pressed="true"] { background: var(--color-fg); color: var(--color-bg); }
.fc-hlset > span { align-self: center; padding: 0 6px 0 10px; font-size: var(--cds-font-size-caption); color: var(--color-fg-muted); }
.fc-hlset button[data-hl="susunan"][aria-pressed="true"] { background: var(--fc-sus); color: #fff; }
.fc-hlset button[data-hl="warna"][aria-pressed="true"] { background: var(--fc-war); color: #fff; }
.fc-sub, .fc-frame, .fc-intro, .fc-bar-top { min-width: 0; max-width: 100%; }
/* Kanvas */
.fd-scroll { overflow: auto; border: 1px solid var(--color-border-line); border-radius: calc(var(--cds-radius) * 1.5); background: var(--color-bg); }
@media (min-width: 700px) { .fd-scroll { max-height: 84vh; } }
.fd-head { display: flex; position: sticky; top: 0; z-index: 6; background: var(--color-bg); border-bottom: 1px solid var(--color-border-line); }
.fd-lh0 { flex: none; padding: 10px 12px; font-size: 11px; color: var(--color-fg-muted); text-transform: uppercase; letter-spacing: .06em; align-self: center; }
.fd-lh { flex: none; padding: 8px 12px; display: grid; gap: 1px; border-top: 4px solid var(--lc); background: color-mix(in srgb, var(--lc) 10%, var(--color-bg)); }
.fd-lh b { color: var(--lc); font-size: 14px; }
.fd-lh span { font-size: 11px; color: var(--color-fg-muted); }
[data-l="0"] { --lc: var(--fd-l0); } [data-l="1"] { --lc: var(--fd-l1); } [data-l="2"] { --lc: var(--fd-l2); } [data-l="3"] { --lc: var(--fd-l3); } [data-l="4"] { --lc: var(--fd-l4); }
.fd-cv { position: relative; }
.fd-ph { position: absolute; left: 0; border-top: 1px dashed var(--color-border-line); }
.fd-ph[data-odd="1"] { background: color-mix(in srgb, var(--color-fg) 2.5%, transparent); }
.fd-ph > span { position: absolute; left: 10px; top: 10px; width: 92px; display: grid; gap: 2px; font-size: 12px; font-weight: var(--cds-font-weight-medium); color: var(--color-fg-muted); line-height: 1.25; }
.fd-ph b { width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; background: var(--color-fg); color: var(--color-bg); font-size: 12px; }
.fd-lane { position: absolute; top: 0; border-left: 1px solid color-mix(in srgb, var(--lc) 22%, transparent); background: color-mix(in srgb, var(--lc) 3%, transparent); }
.fd-svg { position: absolute; left: 0; top: 0; overflow: visible; pointer-events: none; z-index: 1; }
.fd-e { fill: none; stroke-width: 2; transition: opacity .15s, stroke-width .15s; }
.fd-e.fd-utama { stroke: var(--fd-utama); }
.fd-e.fd-ulang { stroke: var(--fd-ulang); stroke-dasharray: 7 4; }
.fd-e.fd-tolak { stroke: var(--fd-tolak); stroke-dasharray: 7 4; }
.fd-e.fd-balik { stroke: var(--fd-balik); stroke-dasharray: 2 4; stroke-linecap: round; stroke-width: 2.4; }
.fd-ah.fd-utama { fill: var(--fd-utama); } .fd-ah.fd-ulang { fill: var(--fd-ulang); } .fd-ah.fd-tolak { fill: var(--fd-tolak); } .fd-ah.fd-balik { fill: var(--fd-balik); }
.fd-lb { position: absolute; z-index: 4; transform: translate(-50%, -50%); font-size: 10.5px; line-height: 1.3; padding: 0 6px; border-radius: 9px; background: var(--color-bg); border: 1px solid currentColor; white-space: nowrap; pointer-events: none; transition: opacity .15s; }
.fd-lb.fd-utama { color: var(--color-fg-muted); } .fd-lb.fd-ulang { color: var(--fd-ulang); } .fd-lb.fd-tolak { color: var(--fd-tolak); } .fd-lb.fd-balik { color: var(--fd-balik); }
.fd-n { position: absolute; z-index: 3; appearance: none; font: inherit; text-align: left; color: var(--color-fg); cursor: pointer; display: grid; grid-template-rows: auto 1fr auto; gap: 2px;
  padding: 6px 10px 6px 12px; border-radius: 8px; border: 1px solid color-mix(in srgb, var(--lc) 45%, var(--color-border-line)); border-left: 5px solid var(--lc);
  background: color-mix(in srgb, var(--lc) 6%, var(--color-bg)); box-shadow: 0 1px 2px rgba(0,0,0,.06); transition: opacity .15s, box-shadow .15s; }
.fd-n:hover, .fd-n.fd-sel { box-shadow: 0 0 0 2px var(--lc); }
.fd-kep { border-style: dashed; border-left-style: solid; background: repeating-linear-gradient(135deg, color-mix(in srgb, var(--lc) 8%, var(--color-bg)) 0 8px, color-mix(in srgb, var(--lc) 3%, var(--color-bg)) 8px 16px); }
.fd-kep .fd-id::after { content: ""; width: 7px; height: 7px; transform: rotate(45deg); border: 1.5px solid currentColor; display: inline-block; margin-left: 6px; vertical-align: 1px; }
.fd-top { display: flex; align-items: center; gap: 6px; font-size: 11px; }
.fd-id { color: var(--lc); font-size: 12px; }
.fd-who { color: var(--color-fg-muted); }
.fd-top .fc-ic-s { margin-left: auto; }
.fd-top .fc-ic-s + .fc-ic-w { margin-left: 4px; }
.fd-top .fd-who + .fc-ic-w { margin-left: auto; }
.fd-t { font-size: 13px; font-weight: var(--cds-font-weight-medium); line-height: 1.25; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.fd-tl { display: flex; align-items: center; gap: 6px; font-size: 10.5px; color: var(--color-fg-muted); }
.fd-dots { display: inline-flex; gap: 3px; }
.fd-dots i { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.fd-none { font-style: italic; }
/* Fokus: halakan tetikus / pilih kotak */
.fc-frame.fd-focus .fd-e:not(.on), .fc-frame.fd-focus .fd-lb:not(.on) { opacity: .12; }
.fc-frame.fd-focus .fd-n:not(.on) { opacity: .45; }
.fc-frame.fd-focus .fd-e.on { stroke-width: 3; }
.fc-frame[data-hl="susunan"] .fd-n:not(.fc-hs), .fc-frame[data-hl="warna"] .fd-n:not(.fc-hw) { opacity: .3; }
.fc-frame[data-hl="susunan"] .fd-n.fc-hs { box-shadow: 0 0 0 2px var(--fc-sus); }
.fc-frame[data-hl="warna"] .fd-n.fc-hw { box-shadow: 0 0 0 2px var(--fc-war); }
/* Panel butiran */
.fd-pop { position: absolute; z-index: 8; width: 360px; max-height: 460px; overflow: auto; background: var(--cds-surface-popover, var(--color-bg)); border: 1px solid var(--color-border-line); border-top: 4px solid var(--lc);
  border-radius: var(--cds-radius); box-shadow: var(--cds-shadow-popover, 0 8px 24px rgba(0,0,0,.18)); padding: 12px 14px; font-size: 12.5px; line-height: 1.45; display: grid; gap: 8px; }
.fd-pop[hidden] { display: none; }
.fd-pop h3 { margin: 0; font-size: 14px; display: flex; gap: 8px; align-items: baseline; padding-right: 24px; }
.fd-pop h3 b { color: var(--lc); }
.fd-pop .fd-x { position: absolute; right: 8px; top: 6px; appearance: none; border: 0; background: none; font-size: 18px; line-height: 1; cursor: pointer; color: var(--color-fg-muted); padding: 4px; }
.fd-pop .fd-who2 { color: var(--color-fg-muted); font-size: 11.5px; }
.fd-pop h4 { margin: 2px 0 0; font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--color-fg-muted); }
.fd-pop ul { margin: 0; padding-left: 16px; display: grid; gap: 3px; }
.fd-pop .fd-tool { display: grid; grid-template-columns: auto 1fr; gap: 0 6px; align-items: baseline; list-style: none; margin-left: -16px; }
.fd-pop .fd-tool i { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.fd-pop .fd-tool small { grid-column: 2; color: var(--color-fg-muted); }
.fd-pop .fd-tool em { font-style: normal; font-size: 10.5px; color: var(--color-fg-muted); }
.fd-pop .fd-link { appearance: none; border: 1px solid currentColor; background: none; font: inherit; font-size: 11px; padding: 0 6px; border-radius: 9px; cursor: pointer; margin: 0 2px; }
.fd-pop .fd-link.fd-utama { color: var(--color-fg-muted); } .fd-pop .fd-link.fd-ulang { color: var(--fd-ulang); } .fd-pop .fd-link.fd-tolak { color: var(--fd-tolak); } .fd-pop .fd-link.fd-balik { color: var(--fd-balik); }
.fd-pop .fd-con { list-style: none; margin-left: -16px; }
@media print { .fd-scroll { max-height: none; overflow: visible; } }
"""

JS = """(() => {
const setup = (box) => {
  box.innerHTML = HTML;
  const btns = [...document.querySelectorAll('.fc-sub-btn')];
  const open = (id) => btns.forEach((b) => {
    const on = b.dataset.sub === id;
    b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1;
    const p = document.getElementById(b.dataset.sub); if (p) p.hidden = !on;
  });
  btns.forEach((b) => b.addEventListener('click', () => open(b.dataset.sub)));
  const frame = document.querySelector('#tab-fc .fc-frame');
  if (!frame) return;
  const hb = [...document.querySelectorAll('#tab-fc .fc-hlset button')];
  const setHl = (h) => {
    frame.dataset.hl = h;
    hb.forEach((b) => b.setAttribute('aria-pressed', b.dataset.hl === h ? 'true' : 'false'));
    try { localStorage.setItem('fc-hl2', h); } catch (e) {}
  };
  hb.forEach((b) => b.addEventListener('click', () => setHl(b.dataset.hl)));
  try { const h = localStorage.getItem('fc-hl2'); if (['tiada', 'susunan', 'warna'].includes(h)) setHl(h); } catch (e) {}

  const cv = frame.querySelector('.fd-cv'), pop = frame.querySelector('.fd-pop');
  const nodes = [...frame.querySelectorAll('.fd-n')], els = [...frame.querySelectorAll('.fd-e, .fd-lb')];
  let sel = null;
  const focus = (id) => {
    if (!id) { frame.classList.remove('fd-focus'); [...nodes, ...els].forEach((x) => x.classList.remove('on')); return; }
    frame.classList.add('fd-focus');
    const near = new Set([id]);
    els.forEach((x) => { const on = x.dataset.a === id || x.dataset.b === id; x.classList.toggle('on', on); if (on) { near.add(x.dataset.a); near.add(x.dataset.b); } });
    nodes.forEach((n) => n.classList.toggle('on', near.has(n.dataset.id)));
  };
  const el = (t, cls, txt) => { const e = document.createElement(t); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  const TONE = { ok: 'ok', warn: 'warn', bad: 'bad' };
  const show = (id) => {
    const d = DATA.nodes[id], n = nodes.find((x) => x.dataset.id === id);
    if (!d || !n) return;
    sel = id; nodes.forEach((x) => x.classList.toggle('fd-sel', x === n)); focus(id);
    pop.replaceChildren(); pop.dataset.l = d.li;
    const x = el('button', 'fd-x', '×'); x.type = 'button'; x.setAttribute('aria-label', 'Tutup'); x.onclick = close; pop.append(x);
    const h = el('h3'); h.append(el('b', '', id), el('span', '', d.t)); pop.append(h);
    pop.append(el('div', 'fd-who2', 'Siapa: ' + d.l + ' · Fasa ' + id[0] + ': ' + d.f + (d.k === 'kep' ? ' · titik keputusan' : '')));
    const con = (title, list, key) => {
      if (!list.length) return;
      const u = el('ul'); const li = el('li', 'fd-con'); li.append(el('b', '', title + ' '));
      list.forEach((e) => { const b = el('button', 'fd-link fd-' + e[2], e[key] + (e[3] ? ': ' + e[3] : '')); b.type = 'button'; b.title = DATA.elabel[e[2]]; b.onclick = () => show(e[key]); li.append(b); });
      u.append(li); pop.append(u);
    };
    con('Dari:', DATA.edges.filter((e) => e[1] === id), 0);
    con('Ke:', DATA.edges.filter((e) => e[0] === id), 1);
    if (d.b.length) { pop.append(el('h4', '', 'Butiran')); const u = el('ul'); d.b.forEach((t) => u.append(el('li', '', t))); pop.append(u); }
    pop.append(el('h4', '', 'Alat'));
    const u = el('ul');
    if (!d.a.length) u.append(el('li', 'fd-tool', 'Tiada alat berasingan'));
    d.a.forEach(([nm, ds, st, tone]) => { const li = el('li', 'fd-tool'); const i = el('i'); i.dataset.tone = TONE[tone]; i.style.background = 'var(--fc-' + tone + ')'; const b = el('b', '', nm + ' '); b.append(el('em', '', st)); li.append(i, b); if (ds) li.append(el('small', '', ds)); u.append(li); });
    pop.append(u);
    pop.hidden = false;
    const nx = n.offsetLeft, ny = n.offsetTop, W = cv.offsetWidth, pw = pop.offsetWidth;
    let left = nx + n.offsetWidth + 12; if (left + pw > W - 8) left = nx - pw - 12; if (left < 8) left = Math.min(nx, W - pw - 8);
    pop.style.left = left + 'px'; pop.style.top = Math.max(8, ny - 8) + 'px';
    x.focus({ preventScroll: true });
  };
  function close() { const was = sel; sel = null; pop.hidden = true; nodes.forEach((x) => x.classList.remove('fd-sel')); focus(null); const n = nodes.find((x) => x.dataset.id === was); if (n) n.focus({ preventScroll: true }); }
  nodes.forEach((n) => {
    n.addEventListener('mouseenter', () => { if (!sel) focus(n.dataset.id); });
    n.addEventListener('mouseleave', () => { if (!sel) focus(null); });
    n.addEventListener('click', () => (sel === n.dataset.id ? close() : show(n.dataset.id)));
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && sel) close(); });
  cv.addEventListener('click', (e) => { if (sel && !e.target.closest('.fd-n, .fd-pop')) close(); });
};
dash.draw('fc-design', { mount: (el) => { setup(el); }, update: () => {} });
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
    import os
    check()
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
        "/* Dijana oleh scripts/build_fc_design.py; jangan ubah secara manual. Dibungkus dalam dash.draw('fc-design') "
        "(27 Nov 2026, disamakan dengan versi live). */\n(() => {\nconst HTML = "
        + json.dumps(content(), ensure_ascii=False) + ";\nconst DATA = " + json.dumps(data_json(), ensure_ascii=False)
        + ";\n" + JS.split("\n", 1)[1])
    print(f"ok: {path} ({len(s.encode())} bait), fc.css, fc.js; {len(NODES)} kotak, {len(EDGES)} garisan")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
