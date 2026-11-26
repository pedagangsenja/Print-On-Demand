# Standard Lettering v1 (25 Nov 2026; dikemas kini 26 Nov 2026)

Status: dipersetujui pengguna 25 Nov 2026; **belum dibina**. Liputan v1: laluan 1–2 (ayat 1–8 perkataan), kemasan F1–F2. Laluan 3–4 = percubaan (belum diuji); F3 ditangguh.
Bukti, ukuran dan sebab setiap peraturan: `docs/lettering-standard-handover.md` (tahap bukti angka: lemah, kecuali lesen: rasmi). Carta 3 lajur: `docs/lettering-aliran.png` (`scripts/lettering_flowchart.py`).

## Urutan tetap: hitam putih dahulu, warna akhir sekali (keputusan pengguna 26 Nov 2026)
1. AI menjana hitam putih sahaja: dakwat putih atas latar hitam; tiada warna lain, tiada kelabu.
2. QC pada imej hitam putih, ikut turutan: ejaan, ayat (baris, susunan, tanda baca ikut Spesifikasi Teks), gaya (ciri kad). Gagal = ulang (langkah 5).
3. Hanya imej yang lulus QC masuk kemasan. Warna C diletak oleh skrip, bukan oleh AI.
4. QC akhir selepas warna: ejaan tidak berubah, warna betul ikut peranan.

Sebab (bukti lemah): AI Image Test 2, 150 imej: gaya satu dakwat (K1, K4) 40/60 imej lulus; gaya 2–3 warna (K2, K3) 25/60. Gayanya berbeza, jadi ini bukan banding terus; ujian banding gaya yang sama belum dibuat. Aliran 12 langkah (tab Aliran dashboard, 24 Nov) sudah memakai urutan yang sama.

## Lima kunci gaya
1. Kad Gaya satu-satunya sumber gaya.
2. QC yang sama untuk semua model.
3. Model hanya dipakai untuk gaya yang ia lulus (jadual model × gaya).
4. AI jana hitam putih sahaja; skrip meletak warna, margin, tekstur selepas QC lulus.
5. Peraturan ulang tetap (langkah 5).

## Langkah 1: Kad Gaya
- 1a. Simpan imej rujukan di tempat kekal.
- 1b. Semak gaya sedia ada dalam S&C (elak pendua). Gaya lama: guna kad sedia ada.
- 1c. Isi kad, 16 medan: medium; warna latar (dalam C); bentuk susunan; bentuk huruf ikut peranan; hierarki saiz; hiasan; tekstur dan kelas kemasan (F1 / F2 / F3); huruf besar / kecil ikut peranan; peta warna ikut peranan; jarak dan hubungan baris; garis dasar dan condong; butiran garisan; ruang tepi; larangan khusus gaya; tanda baca; peraturan pecahan baris.
- Setiap medan disimpan sebagai pasangan: semakan QC (BM, boleh dilihat, ya / tidak) + frasa prompt (Inggeris).
- Kad juga membawa: 8 ciri QC dengan 2–3 ciri teras wajib lulus; unsur berisiko; senarai "jangan salin" (ayat, susun atur tepat, tandatangan, logo); julat panjang ayat yang sesuai; nisbah kanvas rujukan dan cara disesuaikan ke potret 3:4; parameter kemasan (bilangan dakwat, ruang tepi dalam peratus, jenis dan kekuatan tekstur, butiran halus teras atau tidak).
- Warna C berasingan: latar + dakwat 1–3, setiap warna ada peranan dan kod hex. Nama warna tidak masuk prompt (jana hitam putih); peta warna ikut peranan dipakai oleh skrip kemasan.
- Frasa prompt hitam putih: semua dakwat = putih; perkataan dalam kotak atau label = hitam dalam kotak putih; bayang kelabu tidak dijana (ditambah oleh skrip jika kad memerlukan).
- 1d. Pengguna luluskan kad dan sahkan ciri teras (~2 minit).
- 1e. Imej bukti (hitam putih): satu ayat pendek, 2 seed, dibanding dengan upload. Lulus = kad aktif, masuk S&C; imej itu jadi imej sauh, dengan enjin penuh direkod (model, varian fail, langkah, seed).

## Langkah 2: Ayat, peranan dan laluan
- 2a. Ayat asal (bukan ayat rujukan, lirik atau petikan terkenal); bahasa direkod. Saringan trademark dengan kaedah bertulis, hasil direkod (saringan, bukan pengesahan undang-undang).
- 2b. Ukur kesukaran: bilangan perkataan, perkataan berisiko (7+ huruf), perkataan berulang. Pilih laluan ikut panjang ayat baharu:

| Laluan | Panjang | Cara | Status v1 |
|---|---|---|---|
| 1 | 1–4 perkataan | AI penuh, satu blok, 2 seed | Standard |
| 2 | 5–8 | AI penuh, hierarki wajib, 3–4 seed | Standard |
| 3 | 9–16 | Hibrid: AI lukis 2–4 perkataan utama; baris lain font berlesen | Percubaan; perlu ujian dan kelulusan pengguna |
| 4 | 17+ | Font dahulu: AI buat tajuk 1–3 perkataan dan hiasan | Percubaan; perlu ujian dan kelulusan pengguna |

- 2c. Padan dengan kad: ayat mesti dalam julat panjang gaya; jika tidak, pendekkan atau tukar laluan.
- 2d. Peranan: kata isi = utama; kata fungsi = penyambung; selebihnya sokongan. Perkataan 7+ huruf dijadikan utama jika boleh. Sokongan dan penyambung dalam HURUF BESAR kecuali kad mewajibkan skrip. Perkataan utama dapat baris sendiri; maksimum 5–6 blok teks; susunan bacaan ditulis jelas. Tanda baca ditulis jelas; elak jika kad tidak memerlukan.
- 2e. Hasil: Spesifikasi Teks (baris, perkataan, peranan, huruf, tanda baca, laluan, perkataan berisiko). Ini rujukan ejaan untuk QC.

## Langkah 3: Pembina prompt
- Pembina ialah kod: kad + Spesifikasi Teks yang sama mesti menghasilkan prompt yang sama.
- Rangka tetap 9 bahagian: medium + portrait; latar; susunan; teks ("The text reads exactly, N lines:" + arahan setiap baris); hierarki; hiasan; ruang tepi; had hitam putih + larangan khusus; ekor tetap.
- Mod lalai = hitam putih (`designs/lettering-v1/kad.py`, pembina v1.1, `prompts_hp.json`): nama warna kad ditukar kepada white / black, bayang kelabu dibuang, kad berbilang warna dapat ayat "Black and white only, no gray". Kad satu dakwat (K1, K5, K6) kekal sama seperti prompt yang sudah diuji. Mod `warna` hanya untuk mengulang ujian lama.
- Semakan automatik sebelum jana: setiap petikan muncul sekali; petikan sama tepat dengan Spesifikasi Teks; tiada angka, hex, nama font atau jenama; tiada nama warna selain black dan white; bilangan baris betul; dalam had token.
- Had token setiap model (diffusers lalai: klein 4B, Z-Image, Chroma 512; schnell 256; CLIP 77). Turutan potong: teks, bentuk huruf, susunan, hierarki, hiasan, ruang tepi, ekor.
- Profil model: format (penuh / ringkas), pembalut, penambah prompt hidup / mati, sokongan negative prompt. Format untuk keluarga T5 diuji A/B dalam ujian kelayakan; format menang direkod.
- Ayat penegas diambil daripada perpustakaan yang terikat pada ciri QC; `rev` direkod. Jika rev yang sama selalu diperlukan, kad dikemas kini.
- Simpan bersama imej: prompt, versi pembina, versi kad, rev.
- Syarat pakai: pembina mesti menghasilkan semula S1–S6 (ayat 4 perkataan) dengan imej yang tidak lebih buruk.

## Langkah 4: Jana
- Text-to-image penuh, hitam putih sahaja (dakwat putih atas latar hitam), 768×1024 (laluan 1–2, F1 / F2). Enjin: diffusers; versi perpustakaan direkod.
- Tetapan dikunci dalam profil model: model, varian fail, langkah, guidance, LoRA dan kekuatan, penambah prompt. Kelayakan sah untuk gabungan itu sahaja.
- Model utama: MOSS-Image SFT + LoRA 8 langkah, dan ERNIE-Image-Turbo (kedua-duanya 12/12 ejaan betul pada S1–S6). FLUX.2 klein 4B: 6/12; hanya untuk gaya yang ia lulus. Model lain: selepas ujian kelayakan.
- Seed: senarai tetap 42, 7, 123, 2024. Laluan 1: 2 seed terus. Laluan 2: 3–4 seed. Ulangan dijana satu demi satu.
- Susunan kerja: ikut model (muat sekali, jana semua); satu model besar pada satu masa; semak RAM dan disk sebelum muat turun; boleh disambung semula. Anggaran masa dinyatakan sebelum mula.
- Log setiap imej: model, varian, langkah, guidance, LoRA, seed, saiz, versi, masa, prompt.
- Imej mentah disimpan di tempat kekal sebelum sesi tamat.

## Langkah 5: QC ikut kad
- QC mentah dibuat pada imej hitam putih, sebelum sebarang warna. Turutan: ejaan, ayat, gaya.
- Tiga pintu wajib: G1 ejaan 100%; G2 tiada teks rawak; G3 tiada cacat.
- Ejaan: banding dengan Spesifikasi Teks huruf demi huruf (huruf besar / kecil, tanda baca, susunan baris, perkataan tertinggal atau berulang), pada potongan besar. OCR hanya menanda, tidak meluluskan.
- Teks rawak: semak tepi, sudut, hiasan dan bekas teks.
- Ciri kad: lulus ≥ 7/8 dan semua ciri teras lulus; dibanding dengan upload dan imej sauh.
- Ciri kad tentang warna (cth. "kotak kuning", "hanya putih, kuning dan hitam"): dalam QC mentah disemak sebagai bentuk (kotak ada; dakwat hitam / putih di tempat betul); warnanya disemak dalam QC akhir.
- Ciri sejagat: boleh dibaca pada lakaran kecil, tiada teks terpotong, margin mencukupi, imej mentah hanya hitam dan putih.
- QC dua kali: imej mentah hitam putih, dan imej akhir selepas warna dan kemasan (ejaan tidak berubah, warna ikut peranan, bilangan dakwat betul).
- Rekod setiap imej: pintu, setiap ciri lulus / gagal + sebab, cubaan, tindakan. Hasil mengisi jadual model × gaya.
- Peraturan ulang (maksimum 4 cubaan): ejaan = seed baharu, kemudian huruf besar untuk baris kecil; gaya = ayat penegas ciri yang gagal; teks rawak = buang unsur berisiko. Selepas 4 cubaan: model sandaran, kemudian pendekkan ayat, kemudian lapor.
- Pilihan antara imej yang lulus: skor ciri kad, kemudian keterbacaan.
- Kalibrasi: jika pengguna menolak imej yang lulus QC, sebabnya ditambah ke kad.

## Langkah 6: Kemasan ikut kad
- Bermula hanya selepas QC mentah (hitam putih) lulus. Urutan: vektor, warna C ikut peranan, bayang / tekstur, saiz cetak, QC akhir.
- Kelas: F1 vektor rata; F2 rata + tekstur. F3 raster: ditangguh.
- Parameter dibaca daripada kad (ruang tepi, tekstur, bilangan dakwat, butiran halus), bukan tetap dalam skrip.
- Semakan automatik: bilangan lapisan = bilangan dakwat dijangka; peratus dakwat hilang berbanding imej mentah; amaran jika melebihi ambang. Ambang butiran halus ikut gaya.
- Warna C diletak oleh skrip ikut peta peranan kad; satu imej lulus boleh jadi beberapa varian warna C tanpa jana semula.
- Had: perkataan yang hurufnya bertaut merentas baris tidak boleh diasingkan untuk warna berbeza, jadi gaya itu kekal satu dakwat. Bayang lembut dan tekstur dibina semula oleh skrip.
- Tekstur: seed berbeza setiap design; jenis dan kekuatan ikut kad.
- Cetak: 300 DPI (Printify, rasmi), saiz 8×10, 11×14, 16×20, 18×24, 24×36. Bleed, kawasan selamat, had saiz fail dan profil warna: belum disemak.
- Simpan SVG induk + info; PNG besar dijana semula bila perlu; versi `finish.py` direkod.

## Langkah 7: Pengguna lulus atau tolak
- Paparan tetap: upload asal, imej sauh dan hasil sebelah-menyebelah, dengan skor QC dan ejaan.
- Keputusan direkod dengan sebab daripada senarai tetap: ejaan; gaya kurang serupa; terlalu serupa rujukan; tidak cantik; lain-lain.
- Sebab tolak disalurkan balik: ke kad (ciri baharu), ke jadual model × gaya, atau ke ulangan.
- Empat titik kelulusan: kad (1d); contoh pertama laluan 3–4; design hitam putih yang lulus QC (sebelum warna); hasil akhir berwarna.
- Had bilangan imej setiap helaian (angka belum ditetapkan).
- Selepas setiap jana imej: pengguna pilih A atau SNC (peraturan `CLAUDE.md`).

## Langkah 8: Simpan
- Rekod S: Kad Gaya berstruktur, templat prompt tanpa perkataan, imej asal, imej sauh, model yang lulus untuk gaya itu, versi kad dan tarikh.
- Rekod C: peranan setiap warna, nama warna untuk prompt; satu sumber kod hex.
- Daftar design yang diluluskan: ayat, S, C, model, seed, fail induk, status produk.
- Fail disimpan sebelum sesi tamat: imej mentah, SVG induk, log.

## Langkah 9: Serahan, mockup, pin, upload
- Standard lettering berhenti di serahan kepada Workflow (w02–w05).
- Serahan: fail cetak setiap saiz, pratonton, ayat, kod S dan C, hasil saringan trademark.
- Setiap produk dan pin ditanda kod S dan C, supaya tab Prestasi menunjukkan gaya dan warna yang menang.
- Maklum balas jualan kembali ke S&C: gaya menang dapat lebih banyak ayat dan varian warna.
- Belum disemak: dasar platform tentang kandungan janaan AI dan design yang serupa rujukan.

## Tukar model
Ujian kelayakan sekali bagi setiap model baharu (dan setiap gabungan tetapan): setiap gaya × ayat pendek dan sederhana × 2 seed. Lulus: ≥ 90% imej ejaan betul, gaya ≥ 7/8, tiada teks liar. Hasil direkod dalam jadual model × gaya.

## Belum selesai
- Belum dibina: struktur Kad Gaya, pembina prompt, rekod QC, kemasan ikut kad, daftar design.
- Skrip warna ikut peranan belum dibina; `finish.py` masih memaksa palet tetap.
- Prompt hitam putih K2, K3 dan K4 (pembina v1.1) belum diuji pada model utama. K3 hitam putih: 2 imej GLM-Image sahaja (26 Nov), kedua-dua gagal QC (perkataan berulang).
- Ujian banding gaya yang sama: hitam putih lawan berwarna.
- Ujian laluan 3 pada satu ayat ~12 perkataan.
- PyTorch, diffusers dan OCR dalam skrip setup environment.
- Kerja lettering masih di 7 cawangan (tidak digabung, keputusan pengguna 25 Nov); peta: handover bahagian 6.
