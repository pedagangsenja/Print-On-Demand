# Standard Lettering: draf kerja (belum muktamad)

Nota kerja semasa menyemak cadangan standard langkah demi langkah (25 Nov 2026). Akan disusun semula selepas semua langkah disemak.
Asas: aliran S1–S6 (Lettering P9, `scripts/lettering/styles.py` dan `finish.py` di cawangan `claude/affectionate-wright-7y95k3`) dan SOP v3 (cawangan `claude/sharp-franklin-29eamk`).
Tahap bukti semua angka di bawah: lemah (ujian kecil, dinilai oleh Claude).

## Rangka cadangan

4 lapisan (Kad Gaya, pembina prompt, QC ikut kad, kemasan ikut kelas), 4 laluan ikut panjang ayat, 5 kunci gaya.

Laluan ikut panjang ayat baharu (bukan ayat rujukan):
1. Pendek, 1–4 perkataan: AI penuh, satu blok.
2. Sederhana, 5–8: AI penuh, hierarki wajib.
3. Panjang, 9–16: hibrid. AI lukis perkataan utama, font berlesen untuk baris lain.
4. Terlalu panjang, 17+: font dahulu. AI buat tajuk dan hiasan sahaja.

Lima kunci gaya: (1) Kad Gaya satu-satunya sumber; (2) QC sama untuk semua model; (3) model hanya untuk gaya yang ia lulus (jadual model × gaya); (4) skrip paksa warna, margin, tekstur; (5) peraturan ulang (ayat penegas + seed baharu, maks 4, kemudian model sandaran).

Perkara terbuka (dijumpai semasa semakan langkah 5): nota P9 (`docs/research/posters/08-lettering.md`) merekod bahawa pengguna menolak susunan font dengan kod pada 22 Nov kerana nampak "ditaip". Laluan 3 dan 4 bergantung pada baris font, jadi kedua-duanya mesti diuji dan diluluskan pengguna sebelum masuk standard.

## Pembetulan (25 Nov, selepas membaca cawangan sesi lain)

Beberapa kenyataan awal dalam semakan ini sudah lapuk. Kerja berkaitan ada di cawangan lain yang tidak dibaca pada mulanya:
- `claude/dazzling-cannon-5wzn6h` (P9b, 24 Nov): MOSS, ERNIE-Image-Turbo (GGUF Q8) dan FLUX.2 klein 4B diuji pada S1–S6 × 2 seed dengan prompt yang sama, text-to-image. Ejaan betul: MOSS 12/12, ERNIE 12/12, klein 6/12 (S3 dan S6 tiada seed betul). Purata masa: 438 s, 438 s, 93 s. Jadi jadual model × gaya sudah ada data pertama, dan "hanya MOSS diuji" tidak lagi benar.
- `claude/happy-davinci-hv0xb3` (24 Nov): 60 imej mentah MOSS (10 quote 4 perkataan × 6 gaya). Keputusan QC tidak direkod dalam cawangan itu. Jadi S1–S6 sudah dijana pada lebih daripada satu ayat, tetapi masih 4 perkataan sahaja.
- `claude/friendly-knuth-hkclbr` (25 Nov): rekod S dan C dalam Daftar S/C kini menyimpan `prompt` (terisi, dengan perkataan ujian) dan `asal` (imej rujukan). Jadi "prompt tidak disimpan" tidak lagi benar; yang masih tiada ialah ciri gaya berstruktur dan templat tanpa perkataan.
- Carta aliran yang dihantar pada 25 Nov masih membawa tiga tanda lapuk ini dan perlu dibetulkan semasa susunan akhir.

## Langkah 1: Kad Gaya (disemak 25 Nov; disimpan atas arahan pengguna)

Dapatan: prompt S1–S6 membawa 16 jenis maklumat; kad cadangan asal hanya ada tempat untuk 7.

Medan kad (16):
1. Medium
2. Warna latar (dalam C)
3. Bentuk susunan
4. Bentuk huruf ikut peranan (utama / sokongan / penyambung)
5. Hierarki saiz
6. Hiasan (jenis, warna, letak)
7. Tekstur dan kelas kemasan (F1 vektor rata, F2 rata + tekstur, F3 raster)
8. Huruf besar / kecil ikut peranan
9. Peta warna ikut peranan (perkataan mana dapat dakwat mana)
10. Jarak dan hubungan baris (rapat, bertindih, bertaut, sama lebar)
11. Garis dasar dan condong (melantun, condong, melengkung)
12. Butiran garisan (inline, kontras tebal-nipis, tepi kasar)
13. Ruang tepi
14. Larangan khusus gaya (cth. tiada outline, bayang, gradien)
15. Tanda baca
16. Peraturan pecahan baris (sebagai peraturan, bukan baris tetap)

Tambahan yang disyorkan:
- Ciri teras: 2–3 daripada 8 ciri QC wajib lulus (S001 lulus walaupun "kurang melantun", iaitu ciri utama rujukannya).
- Unsur berisiko (cth. reben berteks menghasilkan huruf rawak).
- Senarai "jangan salin": ayat, susun atur tepat, tandatangan atau logo rujukan.
- Julat panjang ayat yang sesuai untuk gaya itu.

Tambahan daripada semakan langkah 3 (disimpan atas arahan pengguna):
- Setiap medan kad disimpan sebagai pasangan: semakan QC (BM) + frasa prompt (Inggeris). Satu sumber untuk prompt dan QC, seperti `build_prompts.py` v3.
- Setiap warna dalam C ada "nama warna untuk prompt" (cth. bright yellow), kerana kod hex tidak boleh masuk prompt.

Tambahan daripada semakan langkah 4 (disimpan atas arahan pengguna):
- Nisbah kanvas rujukan dicatat (cth. upload ke-3 segi empat sama); kad menyatakan cara susunan disesuaikan ke potret 3:4.
- Imej bukti 1e merekod enjin penuh yang menghasilkannya (model, varian fail, langkah, seed).

Tambahan daripada semakan langkah 5 (disimpan atas arahan pengguna):
- Setiap ciri QC dalam kad ditulis sebagai perkara yang boleh dilihat (ya / tidak), bukan kata sifat umum.
- Imej bukti 1e disimpan dalam kad sebagai imej sauh: QC membanding hasil dengan upload dan dengan imej sauh.

Tambahan daripada semakan langkah 6 (disimpan atas arahan pengguna):
- Kad membawa parameter kemasan yang boleh dibaca skrip: bilangan dakwat dijangka, ruang tepi (peratus kanvas), jenis dan kekuatan tekstur, dan sama ada butiran halus (percikan kecil, garis inline) ialah ciri teras yang mesti kekal.

Langkah kecil:
- 1a. Simpan imej rujukan di tempat kekal (sekarang hanya dalam container).
- 1b. Semak gaya sedia ada dalam S&C (elak pendua).
- 1c. Isi kad: medan tetap dengan pilihan tetap.
- 1d. Pengguna luluskan kad dan sahkan ciri teras (~2 minit).
- 1e. Imej bukti: satu ayat pendek, 2 seed, dibanding dengan upload. Kad aktif dan masuk S&C hanya selepas lulus.

## Langkah 2: Ayat, peranan dan laluan (disemak 25 Nov; disimpan atas arahan pengguna)

Dapatan: S1–S6 hanya menyimpan senarai 4 perkataan; baris, peranan dan huruf besar/kecil terkunci dalam templat. "Semak trademark" tiada kaedah bertulis.

Data ralat ejaan (51 imej lettering BM v1–v3; 535 perkataan, 33 salah dipadankan):
- Ikut panjang perkataan: 1–3 huruf 0/51; 4–6 huruf 20/387 (5.2%); 7+ huruf 13/97 (13.4%).
- Ikut jenis huruf: Huruf Awal 21/203 (10.3%); HURUF BESAR 10/277 (3.6%); kecil 2/55 (3.6%). Huruf Awal biasanya ditulis dalam skrip, jadi kesan huruf dan kesan skrip bercampur.

Yang perlu ditambah:
1. Sumber dan keaslian ayat: ayat asal, bukan ayat rujukan, lirik atau petikan terkenal; bahasa direkod.
2. Saringan trademark dengan kaedah bertulis dan hasil direkod (saringan, bukan pengesahan undang-undang).
3. Ukuran kesukaran: bilangan perkataan + perkataan berisiko (7+ huruf) + perkataan berulang.
4. Padanan dengan kad: ayat mesti dalam julat panjang gaya; jika tidak, pendekkan atau tukar laluan.
5. Peraturan memilih perkataan utama: kata isi = utama; kata fungsi = penyambung; bilangan utama ikut laluan.
6. Peraturan huruf: sokongan dan penyambung dalam HURUF BESAR kecuali kad mewajibkan skrip; perkataan 7+ huruf dijadikan perkataan utama jika boleh.
7. Peraturan baris dan blok: perkataan utama dapat baris sendiri; maksimum 5–6 blok teks; susunan bacaan ditulis jelas.
8. Tanda baca ditulis jelas; elak jika kad tidak memerlukan.
9. Laluan 3–4: tetapkan di sini bahagian AI dan bahagian font.
10. Hasil langkah: Spesifikasi Teks berstruktur (baris, perkataan, peranan, huruf, tanda baca, laluan, perkataan berisiko). Ini rujukan ejaan untuk QC.

Langkah kecil: 2a ayat dan saringan; 2b ukur dan pilih laluan; 2c padan dengan kad; 2d peranan, baris, huruf, tanda baca; 2e Spesifikasi Teks.

## Langkah 3: Pembina prompt (disemak 25 Nov; disimpan atas arahan pengguna)

Dapatan: prompt S1–S6 ialah 6 ayat templat tulisan tangan + ekor tetap, sama untuk semua model (hanya MOSS diuji), tanpa semakan automatik dan tanpa versi. SOP v3 sudah ada reka bentuk yang lebih baik (setiap unsur gaya = semakan QC + ayat prompt; `rev` naik bila prompt dibaiki) tetapi tidak dibawa ke S1–S6.

Ukuran (25 Nov):
- Prompt S1–S6 (4 perkataan): 87–124 kata, 143–197 token T5, 129–177 token CLIP.
- Format S6 dengan 8 perkataan: 154 kata, 258 token T5 (melebihi had schnell 256).
- Had lalai diffusers: klein 4B, Z-Image dan Chroma 512 token; schnell 256; CLIP 77.
- ERNIE: penambah prompt (`use_pe`) hidup secara lalai; ujian 23–24 Nov mematikannya. Ujian v1: ERNIE 0/5 design betul, ERNIE + penambah 2/5.

Yang perlu ditambah:
1. Rangka tetap 9 bahagian, setiap satu dipetakan daripada medan kad: medium + portrait; latar; susunan; teks ("The text reads exactly, N lines:" + arahan setiap baris); hierarki; hiasan; ruang tepi; had warna + larangan khusus; ekor tetap.
2. Pembina ialah kod, bukan tulisan bebas: kad + Spesifikasi Teks yang sama mesti menghasilkan prompt yang sama.
3. Semakan automatik sebelum jana: setiap petikan muncul sekali; petikan sama tepat dengan Spesifikasi Teks; tiada angka, hex, nama font atau jenama; bilangan baris betul; dalam had token.
4. Had token setiap model + turutan potong: teks, bentuk huruf, susunan, hierarki, hiasan, ruang tepi, ekor.
5. Profil model: format (penuh / ringkas), pembalut (cth. MOSS guna templat chat), penambah prompt hidup / mati, sokongan negative prompt.
6. Format tidak diandaikan: "T5 ringkas, teks di depan" ialah hipotesis; diuji A/B dalam ujian kelayakan dan format menang direkod dalam profil.
7. Templat ikut laluan: laluan 1–2 seluruh ayat; laluan 3 perkataan utama sahaja; laluan 4 tajuk + hiasan tanpa teks.
8. Perpustakaan ayat penegas terikat pada ciri QC; nombor `rev` direkod. Jika rev yang sama selalu diperlukan, kad dikemas kini.
9. Simpanan: prompt + versi pembina + versi kad + rev disimpan bersama imej.
10. Ujian setara: pembina mesti menghasilkan semula S1–S6 (ayat 4 perkataan) dengan imej yang tidak lebih buruk, sebelum dipakai untuk gaya baharu.

## Langkah 4: Jana (disemak 25 Nov; disimpan atas arahan pengguna)

Dapatan: S1–S6 dijana dengan satu gabungan sahaja (MOSS SFT bf16 + LoRA 8 langkah kekuatan 0.7, 768×1024, seed 42 dan 7). Log hanya menyimpan masa. Ujian 24 Nov memakai fail GGUF Q8 untuk model lain; kesan Q8 berbanding bf16 belum dibanding.

Ukuran:
- Masa CPU setiap imej: MOSS 439 s (P9, 12 imej); ERNIE + penambah 561 s (v3, 25 imej); klein 4B 68–81 s.
- v3: purata 2.5 cubaan setiap design (julat 1–4).
- P9: 12/12 ejaan betul; 5 daripada 6 pilihan ialah seed 42. Seed kedua berguna untuk pilihan rupa, bukan ejaan.
- Enjin: stable-diffusion.cpp 676 s berbanding diffusers 68 s untuk imej klein yang sama (24 Nov).
- Kegagalan 24 Nov: schnell Q8 (12.7 GB) kehabisan RAM 15 GB; disk penuh dua kali bila dua model besar dimuat turun serentak.

Yang perlu ditambah:
1. Tetapan dikunci dalam profil model: model, varian fail (bf16 / Q8 / Q6), langkah, guidance, LoRA dan kekuatan, penambah prompt. Kelayakan sah untuk gabungan itu sahaja.
2. Enjin dikunci: diffusers (bf16 + AMX); versi perpustakaan direkod.
3. Anggaran masa sebelum mula dan had cubaan setiap design.
4. Strategi seed: senarai tetap (42, 7, 123, 2024). Laluan 1: 2 seed terus. Laluan 2: 3–4 seed. Ulangan dijana satu demi satu.
5. Susunan kerja: ikut model (muat sekali, jana semua); kod prompt dahulu; satu model besar pada satu masa; semak RAM dan disk sebelum muat turun; boleh disambung semula.
6. Saiz kanvas ikut laluan dan kelas kemasan: 768×1024 untuk laluan 1–2 dengan F1/F2; laluan 3–4 dan F3 perlu saiz sendiri (belum ditetapkan, belum diuji).
7. Log lengkap setiap imej: model, varian, langkah, guidance, LoRA, seed, saiz, versi, masa, prompt.
8. Imej mentah disimpan di tempat kekal sebelum sesi tamat (container sementara).
9. Pemasangan: skrip setup environment belum ada PyTorch, diffusers dan OCR; model dimuat turun semula setiap sesi (MOSS 28 GB).

## Langkah 5: QC (disemak 25 Nov; disimpan atas arahan pengguna)

Dapatan: QC S1–S6 (P9) = 3 pintu wajib + 9 ciri gaya UMUM yang sama untuk semua gaya (lulus ≥ 8/9), disemak pada helaian semakan sebelum kemasan. Ciri itu tidak diambil daripada upload (cth. "latar gelap rata", "maksimum 2 jenis huruf"), sebab itu S001 lulus walaupun kurang melantun. SOP v3 pula memakai 8 ciri khusus setiap rujukan (lulus ≥ 7/8) dan merekod setiap keputusan.

Ukuran (v3, 25 imej): gagal teks rawak 8; gagal ejaan 6; gaya < 7/8 5; cacat 1; lulus semua 9. Teks rawak ialah kegagalan paling kerap.
OCR (RapidOCR, 24 Nov): panduan yang ejaannya betul hanya dapat skor 0.33–0.88, jadi OCR tidak boleh meluluskan imej; ia hanya menanda.

Yang perlu ditambah:
1. Dua jenis ciri: ciri kad (khusus, daripada upload, dengan ciri teras wajib) dan ciri sejagat (sama untuk semua gaya).
2. Ciri sejagat diambil daripada P9: boleh dibaca pada lakaran kecil Pinterest (~236 px lebar; angka daripada nota P9, sumber tidak dinyatakan), tiada teks terpotong, margin mencukupi.
3. Prosedur ejaan: banding dengan Spesifikasi Teks huruf demi huruf, termasuk huruf besar / kecil, tanda baca, susunan baris, perkataan tertinggal atau berulang; disemak pada potongan besar, bukan lakaran kecil.
4. Prosedur teks rawak: semak tepi, sudut, hiasan dan bekas teks; OCR menanda teks tambahan.
5. QC dua kali: imej mentah (sebelum kemasan) dan imej akhir (selepas kemasan), untuk semua laluan. Nota P9: inline S6 tercantum semasa vektor.
6. Rekod berstruktur setiap imej: pintu, setiap ciri lulus / gagal + sebab, cubaan, tindakan.
7. Peraturan ulang ikut jenis gagal: ejaan = seed baharu, kemudian huruf besar untuk baris kecil; gaya = ayat penegas ciri yang gagal; teks rawak = buang unsur berisiko; selepas 4 cubaan = model sandaran, kemudian pendekkan ayat, kemudian lapor.
8. Peraturan memilih antara imej yang lulus (skor ciri kad, kemudian keterbacaan).
9. Kalibrasi dengan pengguna: keputusan lulus / tolak pengguna dibanding dengan skor Claude; jika pengguna menolak imej yang lulus, sebabnya ditambah ke kad.
10. Hasil QC mengisi jadual model × gaya (kadar lulus).

## Langkah 6: Kemasan (disemak 25 Nov; disimpan atas arahan pengguna)

Dapatan: `finish.py` (S1–S6) membesarkan 4×, mengasingkan dakwat, membersih, menyurih ke vektor (potrace), memaksa palet gaya, menyusun satu blok di tengah (76% lebar, 78% tinggi, pusat 47%), merender 300 DPI untuk 5 saiz dan menambah tekstur prosedur (grain / worn / chalk). Semua tetapan ini tetap dalam skrip, bukan ikut gaya.

Ukuran dan kes (P9):
- S6 seed 42: 2 lapisan warna terhasil sedangkan 3 dijangka (garis inline tercantum dengan putih); seed 7 dapat 3. Boleh dikesan automatik.
- S4: tekstur kapur asal dibuang semasa vektor dan dibina semula secara prosedur.
- Pembersihan membuang objek di bawah ~30 piksel sumber (kira-kira titik 6 piksel pada imej 768 lebar), jadi percikan kecil dan garis rambut boleh hilang.
- Masa: 7–10 s setiap saiz untuk gaya rata; S2 (grain) 5 saiz dalam 82 s. PNG 24×36: 50 MB.
- 768×1024 ke 24×36 in pada 300 DPI (7200×10800) = pembesaran 9.4 kali; vektor mengekalkan tepi tajam untuk dakwat rata sahaja.
- Seed tekstur tetap (7): corak lusuh yang sama pada setiap poster.

Yang perlu ditambah:
1. Parameter kemasan dibaca daripada kad (ruang tepi, tekstur, bilangan dakwat, butiran halus), bukan tetap dalam skrip.
2. Semakan automatik selepas kemasan: bilangan lapisan = bilangan dakwat dijangka; peratus dakwat yang hilang berbanding imej mentah; amaran jika melebihi ambang.
3. Ambang butiran halus ikut gaya; gaya yang ciri terasnya percikan atau inline perlu tetapan lebih halus atau imej mentah lebih besar (belum diuji).
4. Pemetaan warna ikut peranan (bukan warna terdekat sahaja), supaya varian warna C lain boleh dibuat daripada satu imej.
5. Tekstur: seed berbeza setiap design; jenis dan kekuatan ikut kad; jenis baharu ditambah bila gaya memerlukan.
6. Spesifikasi cetak pembekal sebagai senarai semak: 300 DPI (Printify, rasmi); bleed, kawasan selamat, had saiz fail dan profil warna belum disemak.
7. F3 (raster) belum wujud: perlu pembesar imej; di CPU perlahan dan belum dipasang. Ditangguh atau dihadkan saiz sehingga diuji.
8. Gabungan baris font untuk laluan 3–4 belum wujud dan perlu kelulusan pengguna (lihat perkara terbuka).
9. Simpanan: SVG induk + info disimpan kekal; PNG besar dijana semula bila perlu; versi `finish.py` direkod.
10. QC akhir selepas kemasan (lihat langkah 5).

## Langkah 7, 8 dan 9 (cadangan 25 Nov; menunggu semakan pengguna)

### Langkah 7: Pengguna lulus atau tolak
Sedia ada: "lulus / tolak (~5 minit)"; Workflow w07 memperuntukkan 15 minit sehari untuk design, produk dan pin. Selepas setiap jana imej, pengguna memilih A atau SNC dan memadam sendiri yang tidak dimahukan. Sebab penolakan tidak direkod.
Yang perlu ditambah:
1. Paparan tetap: upload asal, imej sauh dan hasil sebelah-menyebelah, dengan skor QC dan ejaan.
2. Keputusan direkod dengan sebab daripada senarai tetap (ejaan, gaya kurang serupa, terlalu serupa rujukan, tidak cantik, lain-lain).
3. Sebab tolak disalurkan balik: ke kad (ciri baharu), ke jadual model × gaya, atau ke ulangan.
4. Tiga titik kelulusan: kad (1d), contoh pertama laluan 3–4, dan hasil akhir.
5. Had setiap sesi kelulusan (bilangan imej setiap helaian) supaya masa semakan realistik.

### Langkah 8: Simpan
Sedia ada (25 Nov): rekod S = nama, jenis, panjang, enjin, imej contoh, imej asal, prompt terisi, nota. Rekod C = nama, latar, senarai hex huruf, gaya, imej, prompt terisi, nota. `image_log` = satu baris setiap imej ujian (skrip di cawangan `claude/vigilant-knuth-0bmbio`).
Yang perlu ditambah:
1. Kad Gaya berstruktur dan templat prompt tanpa perkataan disimpan dalam rekod S (sekarang hanya prompt terisi).
2. Rekod C: peranan setiap warna dan nama warna untuk prompt; satu sumber kod hex (C001 `#f4f1eb` berbanding `styles.py` `#f4f1ea`).
3. Daftar design yang diluluskan (ayat, S, C, model, seed, fail induk, status produk); S&C hanya mendaftar gaya dan warna.
4. Hasil kelayakan model disambung ke rekod S (enjin mana lulus untuk gaya itu).
5. Satu sumber kerja: skrip dan data lettering kini berselerak di sekurang-kurangnya 7 cawangan; perlu digabung ke satu cawangan supaya setiap sesi nampak kerja sesi lain.
6. Fail disimpan sebelum sesi tamat: imej mentah, SVG induk, log.
7. Versi kad dan tarikh kemas kini.

### Langkah 9: Mockup, pin, upload
Sedia ada: diserah kepada Workflow (w02 semak trademark, w03 mockup, w04 upload Printify / WooCommerce, w05 jadual pin). Dalam salinan repo senarai Setup, 26 daripada 30 langkah masih "Belum"; skrip mockup belum dibuat.
Yang perlu ditambah:
1. Spesifikasi serahan daripada lettering ke Workflow: fail cetak setiap saiz ikut senarai semak pembekal, pratonton, ayat, kod S dan C, hasil saringan trademark.
2. Setiap produk dan pin ditanda dengan kod S dan C, supaya tab Prestasi boleh menunjukkan gaya dan warna mana yang menang.
3. Maklum balas jualan kembali ke S&C (gaya menang dapat lebih banyak ayat dan varian warna).
4. Dasar platform tentang kandungan janaan AI dan design yang serupa rujukan: belum disemak.
5. Langkah 9 bergantung pada Setup kedai yang belum siap; standard lettering boleh berhenti di serahan.
