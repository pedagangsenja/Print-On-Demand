# Standard Lettering v1.2 (v1: 25 Nov 2026; v1.2: 26 Nov 2026)

Status: v1 dipersetujui pengguna 25 Nov 2026; v1.2 diluluskan pengguna sebagai standard 26 Nov 2026 (menggantikan v1); **sebahagian dibina**: pembina prompt ikut model siap (3.13); selebihnya lihat "Belum selesai". Liputan: laluan 1–2 (ayat 1–8 perkataan), kemasan F1–F2. Laluan 3–4 = percubaan (belum diuji); F3 ditangguh.

## Apa berubah dalam v1.2
1. **Prompt ikut model** (langkah 3): isi gaya tetap daripada Kad; cara menulis berbeza bagi setiap model. Tujuh model: 3.4 klein 4B, 3.5 Z-Image Turbo, 3.6 ERNIE Turbo, 3.7 MOSS, 3.8 FLUX 3 Image Klein (diuji), dan 3.9 Qwen-Image-2512, 3.10 GLM-Image (belum diuji).
2. **Kitaran QC** (langkah 5): tukar seed dahulu; reka semula prompt model itu hanya untuk cacat sistematik; had 2 pusingan; pembaikan ditulis balik ke aturan model.
3. **Ukuran rujukan dalam Kad** (langkah 1): angka diukur daripada gambar upload, bukan diteka.
4. **Pembetulan selepas jana oleh skrip** (langkah 5b): ruang tepi, kedudukan, condong, hitam putih bersih; hanya bila ukuran tersasar.
5. **Mata pengguna pintu terakhir** (langkah 7): imej yang lulus QC tetapi nampak buruk = gagal; sebabnya masuk Kad.
6. **Kaedah model baharu** (3.12, arahan pengguna 26 Nov 2026): model yang belum ada aturan dikaji dahulu ikut borang 10 soalan; aturannya ditulis dan disimpan untuk model itu sahaja, supaya setiap model ada standard prompt sendiri.
7. **Daftar skrip dan kaedah skrip baharu** (selepas langkah 6, arahan pengguna 26 Nov 2026): empat skrip pembetulan + skrip kemasan didaftar; skrip baharu dibina bila gambar upload memerlukannya, kemudian disimpan, didaftar dan dimasukkan ke dashboard.
8. **Peraturan langkau model** (langkah 4, arahan pengguna 26 Nov 2026): model yang terlalu lama atau bermasalah dilangkau, model seterusnya dijalankan, dan hal itu dilaporkan dalam chat.
9. **Belajar selepas setiap jana** (3.15, keputusan pengguna 27 Nov 2026): `belajar.py` dijalankan selepas setiap batch; aturan prompt setiap model dikemas kini sendiri ikut QC, ♥ dan tolak pengguna.
10. **Belajar SK selepas setiap batch** ("Belajar SK", keputusan pengguna 27 Nov 2026): `belajar_sk.py` dijalankan selepas 5b dan langkah 6; skrip SK dibaiki, diberi parameter kad, atau SK baharu dicipta terus ikut log SK, semakan Claude, ♥ dan tolak pengguna.

Yang kekal daripada v1: hitam putih dahulu dan warna oleh skrip; pintu G1–G3; seed tetap; Kad Gaya satu-satunya sumber gaya; 768×1024.
Bukti, ukuran dan sebab setiap peraturan: `docs/lettering-standard-handover.md` (tahap bukti angka: lemah, kecuali lesen: rasmi). Carta 3 lajur: `docs/lettering-aliran.png` (`scripts/lettering_flowchart.py`).

## Urutan tetap: hitam putih dahulu, warna akhir sekali (keputusan pengguna 26 Nov 2026)
1. AI menjana hitam putih sahaja: dakwat putih atas latar hitam; tiada warna lain, tiada kelabu.
2. QC pada imej hitam putih, ikut turutan: ejaan, ayat (baris, susunan, tanda baca ikut Spesifikasi Teks), gaya (ciri kad). Gagal = ulang (langkah 5).
3. Hanya imej yang lulus QC masuk kemasan. Warna C diletak oleh skrip, bukan oleh AI.
4. QC akhir selepas warna: ejaan tidak berubah, warna betul ikut peranan.

Sebab (bukti lemah): AI Image Test 2, 150 imej: gaya satu dakwat (K1, K4) 40/60 imej lulus; gaya 2–3 warna (K2, K3) 25/60. Gayanya berbeza, jadi ini bukan banding terus; ujian banding gaya yang sama belum dibuat. Aliran 12 langkah (tab Aliran dashboard, 24 Nov) sudah memakai urutan yang sama.

## Lima kunci gaya
1. Kad Gaya satu-satunya sumber gaya.
2. QC yang sama untuk semua model. Prompt ditulis ikut aturan model (langkah 3); isi gayanya sama, daripada kad.
3. Model hanya dipakai untuk gaya yang ia lulus (jadual model × gaya).
4. AI jana hitam putih sahaja; skrip meletak warna, margin, tekstur selepas QC lulus.
5. Kitaran QC tetap (langkah 5); pembetulan skrip hanya bila ukuran tersasar (langkah 5b).

## Langkah 1: Kad Gaya
- 1a. Simpan imej rujukan di tempat kekal.
- 1b. Semak gaya sedia ada dalam S&C (elak pendua). Gaya lama: guna kad sedia ada.
- 1c. Isi kad, 16 medan: medium; warna latar (dalam C); bentuk susunan; bentuk huruf ikut peranan; hierarki saiz; hiasan; tekstur dan kelas kemasan (F1 / F2 / F3); huruf besar / kecil ikut peranan; peta warna ikut peranan; jarak dan hubungan baris; garis dasar dan condong; butiran garisan; ruang tepi; larangan khusus gaya; tanda baca; peraturan pecahan baris.
- Setiap medan disimpan sebagai pasangan: semakan QC (BM, boleh dilihat, ya / tidak) + frasa prompt (Inggeris).
- Kad juga membawa: 8 ciri QC dengan 2–3 ciri teras wajib lulus; unsur berisiko; senarai "jangan salin" (ayat, susun atur tepat, tandatangan, logo); julat panjang ayat yang sesuai; nisbah kanvas rujukan dan cara disesuaikan ke potret 3:4; parameter kemasan (bilangan dakwat, ruang tepi dalam peratus, jenis dan kekuatan tekstur, butiran halus teras atau tidak).
- **Ukuran rujukan (v1.2):** diukur oleh skrip daripada imej upload, disimpan dalam kad sebagai angka: tinggi setiap baris sebagai nisbah kepada tinggi blok (ikut peranan); ruang tepi atas, bawah, kiri, kanan sebagai peratus kanvas; lebar dan tinggi label sebagai nisbah kepada blok; sudut condong blok dalam darjah. Angka ini dipakai oleh pembina prompt (kotak MOSS, 3.7), QC dan skrip pembetulan (5b). Angka tidak boleh diteka; kad tanpa ukuran = pembetulan 5b tidak dijalankan untuk kad itu.
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

## Langkah 3: Pembina prompt (v1.2: satu isi, satu aturan menulis bagi setiap model)

### 3.1 Prinsip
- Isi prompt datang daripada dua sumber sahaja: Kad Gaya (gaya) dan Spesifikasi Teks (perkataan).
- Aturan model hanya menentukan CARA MENULIS isi itu. Aturan model tidak boleh menambah, membuang atau menukar ciri gaya.
- Pembina ialah kod: kad + Spesifikasi Teks + model yang sama mesti menghasilkan prompt yang sama.
- Model yang ada aturan sendiri (3.4–3.10) WAJIB memakai aturan itu. Model tanpa aturan memakai rangka am (3.3) sehingga aturannya ditulis (3.12).
- Tujuh model ada aturan: lima sudah diuji (3.4–3.8, rev r1 / r2; FLUX 3 Image Klein lulus ujian kelayakan 27 Nov 2026) dan dua ditulis daripada sumber rasmi sahaja, belum diuji (3.9–3.10, rev r0). Aturan r0 mesti lulus ujian kelayakan (3.12) sebelum dipakai untuk design sebenar.
- Semua aturan belajar selepas setiap batch imej (3.15): hasil QC, ♥ dan tolak pengguna menentukan ubahan seterusnya; ubahan yang menang terus menaikkan rev.
- Sebab (bukti lemah: kad K3 × ayat H "Patience Builds What Hurry Breaks", 3 seed, CPU, semakan mata, 26 Nov 2026). Imej ejaan betul:

| Model | Rangka am (3.3) | Aturan model |
|---|---|---|
| FLUX.2 klein 4B | 0/3 | 3/3 |
| Z-Image Turbo | 3/3 | 3/3 |
| ERNIE-Image-Turbo | 0/3 | 2/3 |
| MOSS-Image SFT + LoRA | 3/3 | 3/3 |
| Jumlah | 6/12 | 11/12 |

Had bukti: satu kad, satu ayat. Imej: `designs/lettering-v1/raw/k3h-cpu/` (rangka am) dan `raw/k3h-khas-cpu/` (aturan model).

### 3.2 Bahan yang sama untuk semua model
Pembina menyediakan lapan blok isi daripada kad + Spesifikasi Teks. Setiap aturan model mesti memuatkan KESEMUA blok ini, tidak lebih dan tidak kurang:

| Blok | Isi | Contoh (K3 × ayat H) |
|---|---|---|
| A | Medium dan kanvas | hand-lettering quote poster, flat vector, portrait |
| B | Latar | solid black background |
| C | Susunan blok | lima baris, satu blok rapat di tengah; baris bersentuhan; blok condong naik ke kanan |
| D | Baris teks, atas ke bawah: perkataan tepat + peranan + frasa bentuk huruf peranan itu | "PATIENCE" = utama = huge heavy condensed bold sans-serif capitals |
| E | Hierarki saiz | baris bawah paling tinggi; label kecil |
| F | Hiasan dan kedudukannya | tiga garis percikan pendek di kiri dan di kanan label |
| G | Ruang tepi | wide black margins |
| H | Had | hanya perkataan itu, sekali setiap satu; hitam dan putih sahaja; tiada kelabu, bayang, tekstur |

Peraturan sejagat (semua model):
1. Setiap perkataan Spesifikasi Teks ditulis tepat SEKALI dalam petikan berganda `"…"` (MOSS: dalam medan `text`), ejaan dan huruf besar / kecil sama. Tiada perkataan lain dalam petikan.
2. Bahasa Inggeris. Tiada angka, kod hex, nama font, jenama, atau nama warna selain black dan white.
3. Perkataan dalam label ditulis sebagai: hitam, di dalam label segi empat putih pekat.
4. Negative prompt tidak dipakai. Model suling (klein 4B, Z-Image Turbo, ERNIE Turbo, MOSS + LoRA, FLUX 3 Image Klein) jalan tanpa CFG, jadi negative prompt tidak dibaca. Qwen-Image-2512 dan GLM-Image memakai CFG, tetapi Space yang dipakai tidak menerima negative prompt dan lalai rasmi Qwen-Image ialah kosong. Larangan ditulis di dalam prompt ikut aturan model.
5. Tiada kata kualiti kosong ("masterpiece", "best quality", "8k").

### 3.3 Rangka am (pembina v1.1, `kad.bina`)
Dipakai untuk model tanpa aturan sendiri, dan sebagai pembanding dalam ujian kelayakan.
- Rangka tetap 9 bahagian: medium + portrait; latar; susunan; teks ("The text reads exactly, N lines:" + arahan setiap baris); hierarki; hiasan; ruang tepi; had hitam putih + larangan khusus; ekor tetap.
- Mod lalai = hitam putih (`designs/lettering-v1/kad.py`, pembina v1.1, `prompts_hp.json`): nama warna kad ditukar kepada white / black, bayang kelabu dibuang, kad berbilang warna dapat ayat "Black and white only, no gray". Kad satu dakwat (K1, K5, K6) kekal sama seperti prompt yang sudah diuji. Mod `warna` hanya untuk mengulang ujian lama.
- Semakan automatik sebelum jana: setiap petikan muncul sekali; petikan sama tepat dengan Spesifikasi Teks; tiada angka, hex, nama font atau jenama; tiada nama warna selain black dan white; bilangan baris betul; dalam had token.
- Had token setiap model (diffusers lalai: klein 4B, Z-Image, Chroma 512; schnell 256; CLIP 77). Turutan potong: teks, bentuk huruf, susunan, hierarki, hiasan, ruang tepi, ekor.
- Profil model: format (penuh / ringkas), pembalut, penambah prompt hidup / mati, sokongan negative prompt. Format untuk keluarga T5 diuji A/B dalam ujian kelayakan; format menang direkod.
- Ayat penegas diambil daripada perpustakaan yang terikat pada ciri QC; `rev` direkod. Jika rev yang sama selalu diperlukan, kad dikemas kini.
- Simpan bersama imej: prompt, versi pembina, versi kad, rev.
- Syarat pakai: pembina mesti menghasilkan semula S1–S6 (ayat 4 perkataan) dengan imej yang tidak lebih buruk.

### 3.4 Aturan FLUX.2 klein 4B (rev r3: hiasan sisi di luar label; baris berbilang perkataan 'side by side on one line', 28 Nov 2026)
### 3.4 Aturan FLUX.2 klein 4B (rev r2)
- **Sumber:** kad model: "Prompt following is heavily influenced by the prompting style" (rasmi). Panduan BFL: prosa mengalir, tiada penambah prompt (lemah: petikan carian sahaja, laman tidak dapat dibuka).
- **Bentuk:** SATU perenggan prosa, ayat penuh. Bukan senarai kata kunci, bukan "nama: nilai", bukan baris bernombor.
- **Turutan ayat:**
  1. Pembuka: blok A + B. `A black-and-white hand-lettering quote poster in portrait format, flat vector artwork on a solid black background.`
  2. Blok C + G: bilangan baris, satu blok di tengah, ruang tepi, condong.
  3. Blok D + E + F: satu ayat bagi setiap baris, dari atas ke bawah, dimulakan dengan kata tempat: `At the top`, `Directly beneath it`, `In the middle of the block`, `Below the label`, `At the bottom`.
  4. Hubungan baris: `The lines touch and slightly overlap.`
  5. Penutup: blok H.
- **Gaya ditulis DI DALAM ayat baris itu, terus selepas perkataannya:** `the word "PATIENCE" is written in huge heavy condensed bold sans-serif capitals`. Dilarang memisahkan gaya ke senarai lain ("Large words: …"); rangka am berbuat begitu dan gagal 0/3.
- **Baris kedua dengan gaya sama:** rujuk baris terdahulu: `in the same bold brush script`, `in the same heavy condensed sans-serif capitals as the top line`.
- **Label:** bekas dahulu, perkataan kemudian: `sits a small solid white rectangular label, and inside that label the word "WHAT" is printed in small bold black sans-serif capitals`.
- **Had (blok H):** SATU ayat di hujung: `The poster shows only these five words, each of them once, in pure white and black with no gray, no shadow, no texture, and nothing below the last line.` Dilarang senarai panjang "no signature, no watermark, no logo, no frame…" (andaian, belum diuji berasingan: perkataan itu mengundang label tambahan di bawah).
- **Panjang:** dalam had 512 token. Contoh yang lulus: 203 perkataan.
- **Tetapan:** bf16 asal, 4 langkah, guidance 1.0, tiada penambah prompt.
- **Cacat diketahui (r1):** garis percikan dilukis di dalam label pada 2/3 imej. Ubahan pertama untuk dicuba: nyatakan `in the black space to the left and to the right of the label`.
- **r2 (27 Nov 2026, kitaran QC larian v1.2 kedua): tukar peranan perkataan yang salah eja berulang.** K43i: "LOOSELY" jadi "LOSELY" 3/3 sebagai baris utama; sebagai baris sokongan (HOLD jadi utama) 2/3 dieja betul. Dalam kod: `pembina.TUKAR["klein4b"]`, bagi design yang sudah diuji sahaja (K43i). K41g ("FEWER" jadi "FEVER") tidak berubah dengan tukar peranan (0/3 → 0/3), jadi tidak ditulis. Bukti lemah: satu design, 3 seed, CPU.

### 3.5 Aturan Z-Image Turbo (rev r2 versi lucid-galileo, 28 Nov 2026; had positif versi nifty-lovelace kalah atas rekod gabungan)
- **Sumber:** perbincangan rasmi pasukan Z-Image di Hugging Face dan templat penambah prompt mereka (`pe.py`): prompt panjang dan terperinci; teks tepat dalam petikan berganda; untuk poster, huraikan font dan susun atur; tiada negative prompt; had 512 token (rasmi). Julat 80–250 perkataan (pihak ketiga).
- **Bentuk:** huraian objektif yang panjang, seperti kapsyen gambar. Ayat penyata ("The poster contains…", "Line two reads…"), bukan arahan ("make", "draw").
- **Turutan ayat:**
  1. Jenis karya + orientasi (blok A).
  2. Latar (B), kemudian warna dakwat dan tepi: `All lettering is pure white with crisp clean vector edges.`
  3. Bilangan perkataan, bentuk blok, bahagian kanvas yang diisi, ruang tepi (C + G): `the block occupies the middle two thirds of the width and leaves wide empty black margins on all four sides`.
  4. Condong dan hubungan baris (C).
  5. Setiap baris BERNOMBOR (D + E): `Line one, at the top, reads "PATIENCE" in very large, heavy, condensed bold sans-serif capital letters.` … `Line five, at the bottom, reads "BREAKS" …, and it is the tallest line of the poster.`
  6. Hiasan dengan kedudukan tepat (F): `three short white dash strokes radiate from the left side of the label and three from the right side`.
  7. Penutup (H).
- **Had ditulis sebagai ayat POSITIF, bukan "no …" (r2, `had_positif`):** `The image shows exactly these five words, each appearing once and spelled exactly as quoted, in pure white on pure black, and every other area is plain empty black` + (` apart from <isi latar kad>`) + `.` Tiada perkataan berisiko (label, logo, signature). r1: `The only text in the image is these five words, each appearing once. The image uses only pure white and pure black, …`
- **Panjang:** 80–250 perkataan. Contoh yang lulus: 249 perkataan.
- **Tetapan:** GGUF Q8_0, 9 langkah, guidance 0.0, tiada penambah prompt.
- **Cacat diketahui (r1):** percikan hanya di kanan label; ruang tepi sempit (dibetulkan skrip, 5b). Rangka am juga lulus ejaan 3/3, jadi aturan ini mengemaskan hiasan, bukan ejaan.

### 3.6 Aturan ERNIE-Image-Turbo (rev r3, 28 Nov 2026 = r2 ketebalan huruf sleepy-edison + hiasan_tepat lucid-galileo; gabungan belum diuji bersama)
- **Sumber:** dokumen diffusers: penambah prompt (PE) hidup secara lalai dan "may reduce instruction-following accuracy" (rasmi). Kad model: skor teks OneIG-EN 0.9488 tanpa PE lawan 0.9666 dengan PE; GENEval keseluruhan 0.8667 tanpa PE lawan 0.8510 dengan PE (rasmi).
- **Dua peringkat:** (a) pembina menulis prompt mentah yang pendek; (b) PE rasmi mengembangkannya; imej dijana daripada prompt yang dikembangkan.
- **Prompt mentah, satu perenggan pendek (contoh yang lulus: 94 perkataan):**
  1. Blok A: `A black and white hand-lettering quote poster, portrait.`
  2. Blok B: `Solid black background, white lettering.`
  3. Blok C, kemudian titik bertindih, kemudian blok D + E + F sebagai senarai dipisah koma bernoktah, satu butir setiap baris, bentuk `"PERKATAAN" in <frasa bentuk huruf>`: `Five stacked lines in one tight centered block that tilts up to the right: "PATIENCE" in huge heavy condensed bold sans-serif capitals; "Builds" in large bold brush script; …`
  4. Blok I (r2, 28 Nov 2026): `Every letter is drawn with a thick, heavy, fully filled stroke, never thin, scratchy or dry-brushed.`
  5. Blok H + G: `Only these five words, no other text, pure black and white, flat vector style, wide black margins.`
- **PE dijalankan SEKALI bagi setiap prompt, seed 42.** Hasil yang sama dipakai untuk semua seed imej, supaya seed hanya mengubah imej, bukan prompt. PE boleh menulis dalam bahasa Cina; itu dibenarkan.
- **Semakan WAJIB pada hasil PE sebelum jana:** setiap perkataan Spesifikasi Teks ada, ejaan dan huruf besar / kecil tepat; turutan baris sama; tiada perkataan Latin lain dalam petikan. PE boleh menyebut semula sesuatu perkataan sebagai rujukan (contoh K3H: 'PATIENCE' dua kali); itu dibenarkan.
- **Jika semakan gagal:** jalankan PE semula dengan seed 7, kemudian 123. Masih gagal: PE dimatikan, rangka am (3.3) dipakai, dan hal ini direkod.
- **Ayat hiasan tepat (r2, `hiasan_tepat`), sebelum blok H + G:** `Clean empty background` + (` apart from <isi latar kad>`) + `, no other shapes, lines or borders than those described.`
- **Log:** prompt mentah, prompt dikembangkan, seed PE.
- **Tetapan:** GGUF Q8_0, 8 langkah, guidance 1.0. PE dimuat dan dijalankan berasingan sebelum model imej (jimat RAM); penjanaan memakai `use_pe=False` dengan prompt yang sudah dikembangkan.
- **Cacat diketahui (r1):** seed 123 meragukan pada "Builds"; bintang yang tidak diminta; label lebih besar daripada rujukan. Rangka am tanpa PE mengulang perkataan label ("WHAT WHAT") pada 3/3 imej.

### 3.7 Aturan MOSS-Image SFT + LoRA 8 langkah (rev r1)
- **Sumber:** kad model: menerima prosa, tag dan susun atur JSON untuk kedudukan teks (rasmi). Panduan pengguna MOSS: Layout JSON bertanda percubaan dan ditulis untuk model Base (rasmi). Kad LoRA 8 langkah: "Trained on compact-JSON `scene_graph` captions" (kad LoRA, pihak ketiga).
- **Bentuk:** SATU objek JSON, dihantar sebagai `json.dumps(layout, ensure_ascii=False)`. Tiada teks di luar JSON.
- **Kunci wajib:**
  - `summary`: `{"meta": ["poster"], "canvas": "single", "caption": "…"}`
  - `items`: senarai butir, ikut turutan atas ke bawah
  - `bbox_coord_space`: `"abs_centralized"`; `bbox_format`: `"yxyx"`
- **`summary.caption`:** satu perenggan pendek tentang seluruh poster: blok A, B, C, G, E dan H. Perkataan Spesifikasi Teks TIDAK ditulis di sini; ia hanya dalam medan `text`.
- **Butir teks, satu bagi setiap baris:** `{"label": "text", "caption": "<frasa bentuk huruf peranan>, white, flat vector. <kedudukan baris>.", "text": "<perkataan tepat>", "bbox": [...]}`. Label: `caption` = `Small bold sans-serif capitals in black inside a small solid white rectangular label, centered.`
- **Butir hiasan:** `{"label": "object", "caption": "Three short white sparkle strokes left of the label.", "bbox": [...]}`, tanpa `text`. Satu butir bagi setiap sisi.
- **`bbox`:** `[y_atas, x_kiri, y_bawah, x_kanan]`, integer, piksel, asalan di TENGAH kanvas. Kanvas 768×1024: x dari −384 hingga 384, y dari −512 hingga 512.
- **Cara mengira kotak:**
  1. Kawasan blok = kanvas tolak ruang tepi kad.
  2. Tinggi setiap baris = tinggi blok × nisbah baris itu dalam ukuran rujukan kad.
  3. Baris disusun atas ke bawah; jika kad kata baris bersentuhan, kotak bersebelahan bertemu atau bertindih beberapa piksel.
  4. Lebar: baris utama paling lebar; sokongan lebih sempit; label kecil di tengah; semua kotak dipusatkan pada x = 0.
  5. Kotak hiasan diletak di kiri dan kanan label, pada ketinggian label.
- **Sehingga ukuran rujukan kad diukur:** pakai nilai contoh K3H dalam `designs/lettering-v1/khas.py` (percubaan): utama atas 608×168, sokongan 512×168, label 224×80, utama bawah 624×216, percikan 72×64 (lebar × tinggi, piksel).
- **Tetapan:** bf16 asal, 8 langkah, tanpa CFG, LoRA `lodestones/MOSS-Image-SFT-8-steps-dmd` × 0.7, templat sembang "thinking" hidup.
- **Cacat diketahui (r1):** blok tidak condong, kerana kotak JSON tegak. Condong dibuat oleh skrip (5b), bukan oleh prompt.

### 3.8 Aturan FLUX 3 Image Klein (rev r2, 28 Nov 2026; r1: lulus ujian kelayakan 27 Nov 2026)
- **Rev r0 → r1:** Ujian kelayakan (27 Nov 2026, K3K, K7M, K8G, seed 42, 7, 123, CPU, semakan mata, bukti lemah): aturan 3.8 9/9 lawan rangka am 6/9 (rangka am: 'KEEP GOING' tanpa jarak pada 3/3 seed K8G). Teks aturan tidak berubah; hanya rev naik (3.15).
- **Sumber (rasmi):** kad model `black-forest-labs/flux-3-image-klein` dan arahan penambah prompt rasminya (`flux-3-image-klein-pup`, `system_prompts.json`).
  - "Always run a prompt upsampler… trained on full scene captions… a short prompt sent as typed gives generic output."
  - Untuk prompt yang sudah berupa kapsyen penuh, langkah penambah dibuang "so the caption is not expanded twice".
  - Kapsyen: satu blok prosa; medium dan gaya dahulu; kedudukan relatif bingkai; teks disalin tepat dalam petikan berganda dengan tipografi, warna dan kedudukan; "state negations as what is present"; 100–350 perkataan.
  - Susun atur kotak: senarai JSON selepas kapsyen; `bbox` = `[y_min, x_min, y_max, x_max]` pada grid 0–1000, asalan kiri atas; kotak membimbing kedudukan dan saiz, bukan topeng keras.
- **Keputusan standard:** pembina MENULIS kapsyen penuh sendiri dan penambah prompt DIMATIKAN (`prompt_upsampling=False`). Sebab: ejaan dan isi mesti dikawal oleh kad, dan sumber rasmi sendiri membenarkannya untuk kapsyen penuh.
- **Bentuk:** SATU baris: kapsyen global (satu perenggan), satu ruang, kemudian SATU senarai JSON (jadual unsur).
- **Kapsyen global, turutan ayat:**
  1. Medium dan gaya dahulu (blok A): `Flat vector hand-lettering quote poster in black and white, portrait format.`
  2. Latar, ruang tepi dan susunan blok (B, G, C), dengan id: `A solid black background <background_1> fills the frame with wide empty margins.`
  3. Setiap baris dari atas ke bawah, dimulakan dengan sauh kedudukan (`At the top,` `Directly below it,` `In the center,` `Below the label,` `At the bottom,`), menyebut baris itu pada tahap identiti sahaja dan memetik id-nya: `a line of huge heavy condensed sans-serif capitals <En_Text_1>`.
  4. Penutup (H) sebagai apa yang ADA: `The poster holds only these five lines of lettering, in pure white and pure black with flat fills and crisp edges.`
- **Lebar bekas (r2, `hiasan_kedudukan`):** baris berbekas (reben, label) dalam kapsyen ditambah ` spanning the full width of the block`, kecuali bekas yang disebut `small`.
- **Dalam kapsyen DILARANG:** perkataan Spesifikasi Teks, petikan, koordinat, pertimbangan mutu atau emosi. Semua itu duduk dalam jadual.
- **Jadual unsur:** satu baris bagi setiap baris teks, satu bagi latar, satu bagi setiap hiasan. Kunci ikut turutan: `id`, `bbox`, `desc`.
  - `id` baris teks: `En_Text_1`, `En_Text_2`… dari atas ke bawah. Unsur lain: kata nama + indeks dari kiri ke kanan (`background_1`, `sparkle_1`, `sparkle_2`). Setiap id unik, dan setiap id disebut sekali dalam kapsyen.
  - `desc`: bermula dengan identiti unsur, tanpa kedudukan; baris teks membawa perkataan tepat dalam petikan berganda serta tipografinya: `Huge heavy condensed bold sans-serif capitals in pure white reading "PATIENCE", flat vector.`
  - Label: `Small solid white rectangular label carrying small bold black sans-serif capitals reading "WHAT".`
- **`bbox` daripada ukuran kad:** y = piksel_y ÷ tinggi kanvas × 1000; x = piksel_x ÷ lebar kanvas × 1000; integer; tinggalkan sedikit ruang di sekeliling teks. Daripada kotak MOSS (asalan tengah): y = (y + 512) ÷ 1024 × 1000, x = (x + 384) ÷ 768 × 1000.
- **Panjang kapsyen:** 100–350 perkataan (rasmi). Contoh K3H: kapsyen + jadual 303 perkataan.
- **Tetapan:** checkpoint suling, 16 langkah, tanpa guidance (Space: mod "Distilled (16 steps)", `guidance_scale` 1.0), `prompt_upsampling` False, 768×1024, seed tetap.
- **Tempat jalan:** CPU boleh (diukur 26 Nov 2026: 357 s setiap imej, 768×1024, 16 langkah, bf16; `gen_flux3.py`, pipeline modular diffusers, pengekod teks dan transformer dimuat berasingan; perlu torchvision). Space rasmi `black-forest-labs/flux-3-image-klein` (GPU, kuota harian) tidak dipakai.
- **Lesen (rasmi):** FLUX Kommunity v1.0: hasil komersial dibenarkan untuk pengguna dengan hasil kasar di bawah US$5 juta setahun, tertakluk kepada syarat lesen. Berbeza daripada enam model lain (Apache 2.0 / MIT).
- **Status pemakaian (keputusan pengguna 27 Nov 2026, dikemas kini petang yang sama):** lesen DITERIMA oleh pengguna. Model boleh dipakai untuk design jualan dan imejnya boleh didaftar dalam Daftar S/C, tertakluk kepada syarat lesen (rasmi, fail LICENSE.md model): hasil kasar di bawah US$5 juta setahun; setiap imej disemak dahulu supaya tiada kandungan haram atau yang melanggar hak orang lain (QC + saringan trademark); imej dilabel buatan AI jika undang-undang mewajibkan; BFL boleh menarik balik lesen dengan notis. Sebelum keputusan ini lesen belum diterima, sebab itu 9 imej ujian 26 Nov tidak didaftar dalam Daftar S/C. Turutan model lalai (`run_v12.sh`, keputusan pengguna 27 Nov 2026): moss, ernie, klein3, zturbo, klein4b. 9 imej ujian 26 Nov tidak didaftar dalam Daftar S/C (keputusan pengguna 27 Nov 2026: sudah ada dalam AI Image Test). Akses repo berpagar Hugging Face: akaun pengguna sudah boleh memuat turun fail (disemak 27 Nov 2026).
- **Cara jana prompt:** `python3 designs/lettering-v1/pembina.py <id> klein3` (contoh `K3K`); jana: `IDS="<id>" bash run_v12.sh klein3`.
- **Borang 10 soalan (3.12 B), dijawab daripada kad model rasmi (dibaca 26 Nov 2026):**

| # | Jawapan |
|---|---|
| 1 | Pengekod teks Qwen3-VL-4B-Instruct; had lalai diffusers 8192 token. Prompt kita 560–640 token |
| 2 | Kapsyen adegan penuh. "A short prompt sent as typed gives generic output" |
| 3 | Teks disalin tepat dalam petikan berganda, dengan tipografi, warna dan kedudukan. Contoh rasmi: `a cream banner embroidered "KNITTED ICEBERG VILLAGE"` |
| 4 | Ada penambah prompt rasmi (`flux-3-image-klein-pup`, 9B, 18.8 GB), hidup secara lalai. Untuk kapsyen yang sudah penuh, blok `prompt_upsampler` dibuang. Hasilnya boleh dibaca (`output=["images", "prompt"]`) |
| 5 | Model suling: 16 langkah, tanpa guidance, tiada negative prompt. Larangan ditulis sebagai apa yang ADA |
| 6 | Kotak disokong: tag `<id>` dalam kapsyen + senarai JSON; `bbox` = [atas, kiri, bawah, kanan] pada grid 0–1000. Kotak membimbing kedudukan dan saiz, bukan topeng keras. Gambar rujukan: hingga 10 |
| 7 | 16 langkah, tiada guidance; lalai 1024×1024. Kita: 768×1024 |
| 8 | Transformer 5.6B = 11.1 GB bf16; pengekod teks 8.3 GB; VAE 0.3 GB. CPU 15 GB boleh jika pengekod teks dan transformer dimuat berasingan; 357 s setiap imej (diukur). Perlu torchvision |
| 9 | FLUX Kommunity v1.0; repo berpagar (perlu setuju syarat). Pengguna menerima lesen 27 Nov 2026 |
| 10 | Rasmi: teks boleh tidak tepat; unsur boleh melepasi kotak; unsur kecil mungkin tidak muncul. Ujian kita: 9/9 ejaan betul |
- **Cacat diketahui (ujian pertama, 26 Nov 2026, 9 imej, 3 kad):** blok tidak condong (kotak tegak; dibetulkan SK01); lorekan kelabu pada huruf K7 (dibersih SK04). Ejaan 9/9. Kad model: teks boleh tidak tepat; unsur kecil yang diminta mungkin tidak muncul; unsur boleh melepasi kotaknya.

### 3.9 Aturan Qwen-Image-2512 (rev r0: sumber rasmi sahaja, BELUM diuji dengan aturan ini)
- **Sumber (rasmi):** kad model `Qwen/Qwen-Image` dan `Qwen/Qwen-Image-2512`; skrip penulis semula prompt rasmi (`QwenLM/Qwen-Image`, `prompt_utils.py`).
  - "If the input requires rendering text in the image, enclose specific text in quotation marks, specify its position… and style. This text should remain unaltered and not translated."
  - "ensure that the Rewritten Prompt is less than 200 words"; padankan dengan satu gaya yang tepat dan khusus.
  - Contoh rasmi poster: `Art poster design: Handwritten calligraphy title "Art Design" in dissolving particle font, small signature "QwenImage", …`
  - Tetapan rasmi: 50 langkah, `true_cfg_scale` 4.0; negative prompt lalai kosong.
- **Bentuk:** satu perenggan, KURANG daripada 200 perkataan, ayat dan frasa pendek.
- **Turutan:**
  1. Jenis karya dan gaya khusus dahulu (blok A): `Typography poster design, flat vector hand-lettering, black and white, portrait.`
  2. Latar dan ruang tepi (B, G); kemudian susunan blok (C).
  3. Setiap baris dari atas ke bawah. Setiap satu WAJIB ada tiga perkara, ikut turutan: kedudukan, perkataan dalam petikan, gaya. `At the top, the title word "PATIENCE" in huge heavy condensed bold sans-serif capitals.`
  4. Hiasan (F) bersama baris yang berkaitan.
  5. Penutup: gaya ringkas + had (H): `Clean minimalist graphic design, flat fills, crisp edges, pure black and white only. No other text, no people, no objects.` Ayat "No …" dibenarkan untuk model ini (contoh rasmi memakainya).
- **Akhiran rasmi `, Ultra HD, 4K, cinematic composition.` TIDAK ditambah dalam r0** (andaian: ia untuk rupa fotografi, bukan vektor rata). Ujian kelayakan mesti membandingkan dengan dan tanpa akhiran itu.
- **Penambah prompt Space DIMATIKAN** (`prompt_enhance=False`): hasilnya tidak dapat disemak sebelum jana.
- **Tetapan:** 50 langkah, guidance 4.0, nisbah 3:4 (Space tidak menerima saiz piksel; saiz sebenar direkod), seed tetap.
- **Qwen-Image-Fast** (Qwen-Image + LoRA Lightning, 8 langkah, guidance 1.0): aturan menulis sama, tetapi profil berasingan dengan ujian kelayakan sendiri.
- **Tempat jalan:** Space sahaja (41 GB, tidak muat di CPU 15 GB). Kuota percuma: kira-kira 1 imej sehari untuk 2512 (diukur 22–23 Nov), kira-kira 3 sehari untuk Fast (dikira daripada saat GPU).
- **Lesen:** Apache 2.0 (rasmi).
- **Cacat diketahui:** ujian lama dengan prompt lain: 11/14 perkataan betul pada satu ayat panjang (1 imej). Belum diuji dengan aturan ini.

### 3.10 Aturan GLM-Image (rev r0: sumber rasmi sahaja, BELUM diuji dengan aturan ini)
- **Sumber (rasmi):** kad model `zai-org/GLM-Image` dan skrip penambah prompt rasminya (`zai-org/GLM-Image`, `examples/prompt_utils.py`).
  - "ensure that all text intended to be rendered in the image is enclosed in quotation marks"; "strongly recommend using GLM-4.7 to enhance prompts".
  - Peraturan penambah rasmi: bahasa naratif yang bersambung, tanpa senarai, nombor atau tajuk; HANYA teks yang dilukis berada dalam petikan; gaya visual keseluruhan mesti dinyatakan; untuk teks: salin tepat (huruf besar / kecil, tanda baca, pecahan baris), nyatakan kedudukan dan pembawanya, gaya font, warna, cara persembahan, dan fungsinya (tajuk, keterangan, label, hiasan).
  - Resolusi mesti boleh dibahagi 32; penjana autoregresif bersampel (suhu 0.9), jadi hasil lebih berubah antara seed.
- **Keputusan standard:** penambah GLM-4.7 tidak dipakai (perkhidmatan luar). Pembina menulis prompt penuh ikut peraturan penambah itu sendiri. Penyimpangan ini direkod dan dinilai dalam ujian kelayakan.
- **Bentuk:** SATU perenggan naratif, ayat penuh yang bersambung. DILARANG: senarai, baris bernombor ("Line one…"), tajuk, titik bertindih diikuti senarai.
- **Turutan ayat:**
  1. Gaya visual keseluruhan dan pembawa (blok A): `A graphic design poster in flat vector hand-lettering style, portrait format, printed in pure black and white.`
  2. Latar, ruang tepi, cara teks dipersembahkan dan susunan blok (B, G, C): `…all lettering is flat white print with crisp edges, arranged as five stacked lines in one tight block at the center…`
  3. Setiap baris dari atas ke bawah, satu ayat setiap baris, dengan EMPAT perkara: kedudukan, fungsi, perkataan dalam petikan selepas "reads", gaya font dan warna. `At the top of the block, the main title reads "PATIENCE" in huge heavy condensed bold sans-serif capital letters.`
  4. Fungsi ikut peranan kad: utama = `main title` / `closing title`; sokongan = `supporting line`; penyambung = `connecting word`.
  5. Hiasan sebagai hiasan (F): `with three short white sparkle strokes as decoration on the left and on the right of the label`.
  6. Penutup (H): `Only these five words appear on the poster, and the overall look is clean, bold and minimal.`
- **Petikan:** tiada apa-apa selain perkataan Spesifikasi Teks berada dalam petikan.
- **Tetapan:** 50 langkah, guidance 1.5, 768×1024 (kedua-duanya boleh dibahagi 32), seed tetap.
- **Tempat jalan:** Space `multimodalart/GLM-Image` (36 GB, tiada GGUF; tidak muat di CPU). Kuota percuma: kira-kira 2 imej sehari (dikira daripada saat GPU).
- **Lesen:** MIT (rasmi).
- **Cacat diketahui:** 2 imej K3 hitam putih (26 Nov, rangka am) kedua-duanya gagal: perkataan berulang. Forum Hugging Face: perlahan, huruf rawak salah (pihak ketiga). Dahulu ditanda "Tolak" dalam jadual induk; kini calon yang mesti lulus ujian kelayakan dengan aturan ini.

### 3.11 Semakan automatik sebelum jana (semua model)
Prompt yang gagal mana-mana semakan TIDAK dijana.
- Semua model: perkataan dalam petikan (MOSS: senarai `text`) sama tepat dengan Spesifikasi Teks, ikut turutan, sekali setiap satu; tiada angka, hex, nama font, jenama, atau nama warna selain black dan white; dalam had token model.
- klein 4B: satu perenggan; tiada senarai gaya terpisah; tiada senarai larangan selepas ayat had (no signature, no watermark, no logo, no frame…).
- Z-Image Turbo: bilangan ayat "Line …" sama dengan bilangan baris; tiada frasa "no …" dalam ayat penutup.
- ERNIE Turbo: semakan pada prompt mentah DAN pada hasil PE (3.6).
- FLUX 3 Image Klein: satu baris; kapsyen tanpa petikan dan tanpa koordinat; setiap id dalam jadual disebut sekali dalam kapsyen dan sebaliknya; id unik; setiap `bbox` dalam grid 0–1000 dengan y_min < y_max, x_min < x_max; bilangan baris `En_Text` sama dengan bilangan baris teks.
- Qwen-Image-2512: kurang daripada 200 perkataan; setiap petikan diikuti gaya dan didahului kedudukan.
- GLM-Image: satu perenggan; tiada senarai, nombor baris atau tajuk; tiada petikan selain perkataan Spesifikasi Teks; lebar dan tinggi boleh dibahagi 32.
- MOSS: JSON sah; kunci wajib ada; setiap `bbox` di dalam kanvas dan y_atas < y_bawah, x_kiri < x_kanan; bilangan butir teks sama dengan bilangan baris.

### 3.12 Kaedah model baharu, dan mengubah aturan model (arahan pengguna 26 Nov 2026)
**Tujuan:** setiap model ada standard prompt sendiri. Bila model itu dipakai semula kelak, aturannya sudah ada dan tidak perlu dikaji lagi.

**Bila dipakai:** model tiada dalam daftar aturan (`python3 pembina.py --daftar`). Sehingga aturannya siap, model itu memakai rangka am (3.3) dan direkod sebagai rev `am`.

**A. Kaji sumber, ikut keutamaan:**
1. Kad model rasmi.
2. Repo rasmi pembuat: panduan prompt, skrip atau arahan penambah prompt (system prompt), contoh prompt.
3. Dokumen pipeline (diffusers) dan kod Space rasmi: tetapan lalai, penambah prompt hidup atau mati.
4. Perbincangan pasukan pembuat (Hugging Face, GitHub).
5. Pihak ketiga: hanya jika 1–4 tiada; ditanda bukti lemah.

Sumber yang tidak dapat dibuka dicatat. Tiada jawapan rasmi = tulis "tiada sumber rasmi"; jangan teka.

**B. Borang 10 soalan (dijawab dengan petikan sumber):**

| # | Soalan | Menentukan |
|---|---|---|
| 1 | Pengekod teks apa, dan berapa had token? | Panjang prompt |
| 2 | Bentuk prompt yang dilatih atau dianjurkan: prosa, kapsyen panjang, kata kunci, JSON, kotak? | Bentuk |
| 3 | Bagaimana teks yang dilukis ditulis (petikan, medan khas)? Ada contoh rasmi poster atau teks? | Cara tulis teks dan gaya |
| 4 | Ada penambah prompt rasmi? Hidup secara lalai? Hasilnya boleh disemak sebelum jana? | Hidup, mati, atau dua peringkat |
| 5 | Model suling atau memakai CFG? Negative prompt dibaca? | Cara tulis had |
| 6 | Sokong susun atur: kotak, koordinat, gambar rujukan? | Kotak daripada ukuran kad |
| 7 | Tetapan rasmi: langkah, guidance, syarat resolusi | Profil dikunci |
| 8 | Saiz fail dan RAM; boleh jalan di CPU atau perlu Space? Masa setiap imej? | Tempat jalan, had masa langkau |
| 9 | Lesen untuk hasil komersial | Boleh dipakai atau tidak |
| 10 | Kelemahan diketahui (kad model, ujian orang lain) | Cacat diketahui |

**C. Tulis aturan (rev r0)** dengan tujuh medan yang sama seperti 3.4–3.10: sumber, bentuk, turutan ayat, cara tulis teks dan gaya, cara tulis had, tetapan, cacat diketahui. Aturan mesti memuatkan kesemua lapan blok isi (3.2) dan mematuhi peraturan sejagat.

**D. Simpan untuk model itu SAHAJA** (aturan model lain tidak disentuh):
1. Bahagian baharu dalam dokumen ini, di bawah "3.14 Aturan model tambahan" (3.14.1, 3.14.2, …), bersama jawapan borang.
2. `pembina.py`: satu baris dalam `DAFTAR`, satu fungsi aturan, dan semakan khusus model itu dalam `semak` (3.11).
3. Profil dikunci dalam `gen.py` (`PROFIL`) atau `gen_hf_space.py`, dan satu baris dalam jadual profil langkah 4.
4. Dashboard: tab FC › Design (langkah 3) dan tab Aliran (langkah 6), dalam sesi yang sama.
5. Satu baris dalam "Catatan pembaikan aturan model". Nombor versi standard kekal v1.2.

**E. Semak tanpa jana:** `python3 pembina.py` mesti lulus bagi semua kad × ayat untuk model baharu itu.

**F. Ujian kelayakan (perlu izin jana daripada pengguna):** rangka am lawan aturan baharu; kad sama, ayat sama, seed 42, 7, 123. Aturan diterima (r0 → r1) jika bilangan imej lulus tidak kurang daripada rangka am. Jika gagal: model ditanda "tidak layak" bersama sebabnya, dan aturannya tetap disimpan supaya tidak dikaji semula.

**Mengubah aturan sedia ada:** hanya melalui kitaran QC (langkah 5), SATU ubahan setiap pusingan. Setiap ubahan, berjaya atau tidak, direkod dalam "Catatan pembaikan aturan model"; ubahan yang berjaya menaikkan rev aturan (r1 → r2).

**Rekod bersama setiap imej:** prompt, model, rev aturan, versi kad, versi pembina.

- **Status (26 Nov 2026):** pembina kod bagi ketujuh-tujuh model sudah dibina (3.13). Contoh tulisan tangan `khas.py` (khas-v0) disimpan sebagai rekod ujian pertama sahaja; prompt baharu mesti datang daripada pembina.

### 3.13 Pembina kod (`designs/lettering-v1/pembina.py`, versi v1.2-p1, 26 Nov 2026)
- **Guna:** `python3 pembina.py` (semak semua), `python3 pembina.py K3H klein4b` (cetak satu prompt), `python3 pembina.py --banding` (banding dengan `khas.py`). Jana: `GEN_VARIAN=pembina` dalam `gen.py` / `gen_moss.py`; larian penuh `run_v12.sh`.
- **Sumber isi:** `kad.BLOK` (blok A–H setiap kad sebagai frasa hitam putih, diambil daripada Kad Gaya; tiada ciri baharu) + `kad.AYAT`. Enam kad ada blok: K1–K6.
- **Satu frasa bagi setiap peranan:** `penuh` pada sebutan pertama, `the same <ringkas>` pada ulangan. Semua model memakai frasa yang sama; aturan model hanya menyusun ayat.
- **Semakan 3.11 dalam kod:** `pembina.semak` (semua model) dan `pembina.semak_pe` (hasil PE ERNIE; gagal → seed PE 7, kemudian 123, kemudian rangka am tanpa PE). 210 prompt (6 kad × 5 ayat × 7 model) lulus semakan.
- **Beza dengan contoh tulisan tangan (K3 × ayat H):** perkataan sama 93% (klein 4B), 84% (Z-Image), 79% (ERNIE mentah), 95% (MOSS), 87% (FLUX 3 Klein), 89% (Qwen), 89% (GLM). Sebab beza: contoh tulisan tangan memakai frasa gaya yang berlainan antara model ("thick, connected", "very large"); pembina memakai satu frasa kad. Kotak MOSS: satu kotak berbeza 8 piksel.
- **Keputusan pembina yang tidak tertulis dalam 3.4–3.10 (direkod di sini):**
  1. Ayat had klein 4B: kad yang ada hiasan di bawah baris akhir (K4, K6) mendapat `no other lettering below the last line`, bukan `nothing below the last line`.
  2. Hiasan sisi label (K3) hanya ditulis jika ayat ada baris berlabel; ayat tanpa penyambung tidak mendapat percikan.
  3. Baris tertinggi (K3) = baris utama yang terakhir, dan hanya jika ada lebih daripada satu baris utama.
  4. Kotak MOSS / FLUX 3 Klein bagi kad tanpa ukuran: lebar blok = kanvas tolak ruang tepi kad; tinggi baris lalai 168 (utama), 136 (sokongan), 80 (penyambung) piksel; baris bersentuhan; bekas diberi sela 8 piksel; blok dipusatkan. Ini nilai sementara sehingga ukuran rujukan diukur.
  5. Kata fungsi GLM: `main title`, `second title`, `closing title`, `supporting line`, `connecting word` / `connecting phrase`.
  6. Kata sifat yang bukan daripada kad dibuang daripada rangka ("minimalist", "bold and minimal").
- **Model tanpa aturan:** `pembina.bina` memulangkan rangka am (3.3) dan rev `am`, sehingga aturannya ditulis ikut 3.12.
- **Syarat pakai:** hasil pembina pada K3 × ayat H tidak lebih buruk daripada contoh tulisan tangan (11/12 ejaan betul). Ujian pertama 26 Nov dihentikan dan 6 imejnya dipadam atas arahan pengguna. **Larian v1.2 pertama (26 Nov malam):** K3 × ayat baharu 11/12 ejaan betul dengan pembina (bukti lemah; lihat "Larian v1.2 pertama").

### 3.14 Aturan model tambahan
Tempat menyimpan aturan model baharu yang ditulis ikut 3.12 (3.14.1, 3.14.2, …). Belum ada.

### 3.15 Belajar selepas setiap jana: aturan prompt dikemas kini sendiri (keputusan pengguna 27 Nov 2026)
**Tujuan:** aturan setiap model terus belajar daripada hasil sebenar. Aturan r0 datang daripada bacaan sumber rasmi sahaja; selepas itu setiap batch imej menambah bukti, dan aturan berubah ikut bukti itu, bukan tekaan.

**Bila:** selepas SETIAP batch imej AI yang sudah di-QC (langkah 5), termasuk batch yang semua imejnya lulus. Tiada jana tambahan tanpa izin pengguna.

**Langkah (Claude, dalam sesi yang sama, tanpa tanya):**
1. Salin stor dashboard dengan ArtifactData `list` dan `out_dir=designs/lettering-v1/belajar/stor`: `data/likes/items` (♥), `data/gaya/items` dan `data/warna/items` (Daftar S/C). Folder `stor/` tidak disimpan dalam git.
2. Rekod keputusan pengguna langkah 7 dalam `belajar/pengguna.jsonl`, satu baris setiap imej: `{"imej": "<batch>/<model>/<ID>_s<seed>", "keputusan": "lulus" atau "tolak", "sebab": "..."}`.
3. Jalan `python3 belajar.py` (dalam `designs/lettering-v1/`). Hasil: `belajar/log.jsonl` (satu baris = satu imej), `belajar/ringkasan.json` (setiap model), `data/export/ai_tests/aturan_belajar.json` (dashboard), dan senarai TINDAKAN bagi setiap model.
4. Laksana setiap TINDAKAN terus, kemudian lapor dalam jadual jawapan:
   - **MENANG:** tulis ubahan ke fungsi aturan model dalam `pembina.py` dan ke bahagian aturannya (3.4–3.10); naikkan rev (cth. r1 → r2) dalam `DAFTAR` dan tajuk bahagian; buang calon daripada `UJI`; tambah baris dalam `belajar/ubahan.json` dan "Catatan pembaikan aturan model".
   - **KALAH:** buang calon daripada `UJI`; catat dalam `ubahan.json` dan Catatan, supaya tidak diulang.
   - **CUBA:** tulis ubahan calon dalam `pembina.py` (`UJI`, nama `<model>_<id>`, cth. `zturbo_had_positif`). Ia dipakai pada jana seterusnya model itu, bersama aturan semasa, pada kad, ayat dan seed yang sama.
   - **KELAYAKAN / NAIK / TIDAK LAYAK:** ujian kelayakan aturan r0 (3.12 F). Lulus: r0 → r1.
   - **HABIS:** semua pilihan ubahan sudah dicuba: tukar model ikut jadual model × gaya, kemudian pendekkan ayat, kemudian lapor.
5. Muat naik `aturan_belajar.json` ke dashboard (dataset `aturan_belajar`, tab AI Image Test) dan simpan semua fail dalam git.

**Peraturan belajar (kod: `belajar.py`, versi b1; b1.2 pada 28 Nov 2026: seri lulus dan ♥ dipecah oleh bilangan imej dengan kelas cacat sasaran ubahan, keputusan pengguna):**
- **Isyarat:** QC G1–G2; ♥ pengguna; tolak pengguna (`pengguna.jsonl`, atau kod yang dipadam daripada Daftar S/C). Imej lulus = lulus QC dan tidak ditolak. Imej yang ditolak dikira cacat.
- **Kelas cacat** ikut jadual kitaran QC (langkah 5): berulang, rawak, luar label, hiasan lebih, hiasan di tempat salah, baris, ejaan, bentuk, ditolak. Cacat "bukan prompt" (condong, ruang tepi, kedudukan, kelabu, warna, bayang, tekstur, vektor: kelas `KELAS_SK`) diabaikan, kerana itu kerja skrip SK; ia dipelajari oleh `belajar_sk.py` ("Belajar SK", selepas Daftar skrip). b1.1: senarai ini dibaca terus daripada `belajar_sk.py`.
- **Cacat berulang** = kelas yang sama pada sekurang-kurangnya 2 imej, sama ada pada 2 design atau lebih, atau pada 2 seed atau lebih dalam satu design. Bagi ejaan: hanya jika PERKATAAN yang sama salah.
- **Satu ubahan setiap kali** bagi setiap model. Cacat yang membuat imej gagal didahulukan; cacat gaya pada imej yang lulus kemudian.
- **Tiada ulangan:** ubahan yang pernah dicuba (`ubahan.json`) tidak dicuba lagi. "Huruf besar" dilangkau jika perkataan yang salah sudah huruf besar.
- **Menang** = lebih banyak imej lulus pada kad, ayat dan seed yang sama, tanpa kelas cacat baharu. Seri dipecahkan oleh bilangan ♥, kemudian bilangan imej **bersih** (lulus tanpa kelas cacat prompt). Pemecah seri kedua ditambah 28 Nov 2026 (b1.1): tanpanya ubahan bagi cacat yang tidak menggagalkan imej (bentuk huruf) tidak boleh menang.
- **Cacat pepijat kod** (nota QC mengandungi "pepijat kod"): tidak dikira sebagai cacat prompt (28 Nov 2026).
- **Had 3.1 kekal:** ubahan hanya mengubah cara menulis; ia tidak boleh menambah atau membuang ciri gaya kad.
- **Log jana** mencatat `rev` dan `uji` (ubahan calon) bagi setiap imej (`gen.py`). Pusingan kitaran QC lama (batch `-p1`) tanpa `uji` dipadankan dengan `ubahan.json`.

**Gabung cawangan sesi (keputusan pengguna 28 Nov 2026):** beberapa sesi Claude bekerja serentak pada cawangan berlainan, dan setiap sesi dahulu memuat naik jadual belajar daripada rekod cawangannya sahaja. Kini, sebelum `belajar.py` dan `belajar_sk.py`, jalan `python3 gabung_cawangan.py origin/claude/<cawangan> ...` (selepas `git fetch`). Skrip menyalin rekod sahaja (qc, log jana, log 5b / 6, ubahan, semakan; bukan imej) ke `cawangan/<sesi>/`. Nama batch, kad dan imej sesi lain ditanda `<sesi>:` kerana ID kad yang sama dipakai untuk gaya berlainan. Ujian calon dinilai ikut sesi masing-masing; liputan kad (belajar SK) hanya kad cawangan ini. Ubahan sesi lain dibaca jika menang / kalah / tidak berkenaan sahaja. Nota QC perihal ("G1-G3 lulus; ...") pada imej lulus tidak dikira cacat. Dataset `ai_all`: sebelum muat naik, ambil fail `data/ai_tests/rows/U*.json` terbaharu daripada semua cawangan dan semak tiada baris dashboard hilang; nombor ujian baharu = nombor selepas yang terbesar di dashboard.

**Had:** ini bukan AI yang belajar sendiri. Ia peraturan tetap yang dijalankan Claude selepas setiap batch. Bukti kecil (3 seed) mudah tersilap; sebab itu hanya satu ubahan setiap kali, dan banding pada seed yang sama.

**Keputusan pertama (27 Nov 2026; 117 imej daripada 8 batch; ♥ 0; tolak 0; bukti lemah):**
- klein 4B r1 (6/9 lulus): cuba `klein4b_hiasan_kedudukan` (percikan di dalam label, 3 imej K3K).
- Z-Image Turbo r1 (4/9): cuba `zturbo_had_positif` (teks dan tanda baca rawak, 4 imej, K7M dan K8G).
- ERNIE Turbo r1 (8/9): cuba `ernie_frasa_bentuk` (skrip lebih nipis dan label lebih besar daripada kad, 6 imej lulus).
- MOSS + LoRA r1 (6/9): 'ALMOST' salah pada 3/3 seed K8G; dua pilihan sudah dicuba atau tidak berkenaan → tukar model bagi ayat itu.
- FLUX 3 Image Klein r0 (9/9): perlu ujian kelayakan. **Dijalankan pada hari yang sama:** rangka am 6/9 lawan aturan 9/9 → LULUS, r0 → r1 (3.8). Lesen diterima pengguna (27 Nov 2026).
- Qwen-Image-2512 r0, GLM-Image r0: belum diuji.

## Langkah 4: Jana
- Text-to-image penuh, hitam putih sahaja (dakwat putih atas latar hitam), 768×1024 (laluan 1–2, F1 / F2). Enjin: diffusers; versi perpustakaan direkod.
- Tetapan dikunci dalam profil model: model, varian fail, langkah, guidance, LoRA dan kekuatan, penambah prompt. Kelayakan sah untuk gabungan itu sahaja.
- Model utama: MOSS-Image SFT + LoRA 8 langkah, dan ERNIE-Image-Turbo (kedua-duanya 12/12 ejaan betul pada S1–S6). FLUX.2 klein 4B: 6/12; hanya untuk gaya yang ia lulus. Model lain: selepas ujian kelayakan.
- Profil dikunci v1.2 (CPU; masa setiap imej daripada log 26 Nov 2026, kad K3 × ayat H, bukti lemah):

| Model | Varian | Langkah | Guidance | Penambah prompt | Aturan | Masa / imej |
|---|---|---|---|---|---|---|
| FLUX.2 klein 4B | bf16 asal | 4 | 1.0 | tiada | 3.4 | 85–118 s |
| Z-Image Turbo | GGUF Q8_0 | 9 | 0.0 | tiada | 3.5 | kira-kira 260 s |
| ERNIE-Image-Turbo | GGUF Q8_0 | 8 | 1.0 | PE rasmi, sekali, seed 42 | 3.6 | 305–373 s |
| MOSS-Image SFT + LoRA × 0.7 | bf16 asal | 8 | tanpa CFG | templat "thinking" hidup | 3.7 | 337–392 s |
| FLUX 3 Image Klein (suling) | bf16 asal | 16 | tiada | dibuang (kapsyen penuh daripada pembina) | 3.8 (r1) | kira-kira 357 s |

- Tiga model tambahan (26 Nov 2026), dijalankan melalui Space Hugging Face (GPU, kuota harian) kerana tidak muat atau belum diukur di CPU. Belum diuji dengan aturan sendiri; perlu ujian kelayakan dahulu:

| Model | Tempat jalan | Langkah | Guidance | Penambah prompt | Aturan | Lesen | Kuota percuma |
|---|---|---|---|---|---|---|---|
| FLUX 3 Image Klein | Space `black-forest-labs/flux-3-image-klein` | 16 | tiada | dimatikan | 3.8 | FLUX Kommunity v1.0 (bersyarat) | kira-kira 9 imej sehari |
| Qwen-Image-2512 | Space `Qwen/Qwen-Image-2512` | 50 | 4.0 | dimatikan | 3.9 | Apache 2.0 | kira-kira 1 imej sehari |
| GLM-Image | Space `multimodalart/GLM-Image` | 50 | 1.5 | tidak dipakai | 3.10 | MIT | kira-kira 2 imej sehari |

Kuota: daripada jadual induk model dalam dashboard (2512 diukur 22–23 Nov; yang lain dikira daripada saat GPU setiap imej; bukti lemah).

### Peraturan langkau model (v1.2, arahan pengguna 26 Nov 2026)
- **Turutan model (CPU):** MOSS → ERNIE Turbo → Z-Image Turbo → klein 4B. Asas: lulus QC dalam AI Image Test 2 (23/30, 21/30, 13/30, 7/30; bukti lemah). Tiga model Space GPU tidak dijalankan (keputusan pengguna 26 Nov 2026: tiada Space GPU).
- **Langkau bila terlalu lama:** masa satu model melebihi 20 minit (muat turun) + 13 minit bagi setiap imej. 13 minit ialah kira-kira dua kali masa paling perlahan yang direkod (392 s, MOSS). Disahkan pengguna 26 Nov 2026.
- **Langkau bila bermasalah:** gagal 3 cubaan berturut-turut (muat turun, RAM, ralat kod), prompt gagal semakan 3.11, atau kuota Space habis.
- **Tindakan:** model itu dihentikan dan model seterusnya terus dijalankan. Model yang dilangkau tidak diulang dalam sesi yang sama kecuali diminta pengguna.
- **Rekod:** `langkau.jsonl` dalam folder hasil (model, sebab, saat). Claude menulis dalam chat sebaik sahaja berlaku, dan sekali lagi dalam jadual akhir: model apa, sebab, dan berapa imej sempat siap.
- **Langkau bukan gagal QC:** model yang dilangkau tidak ditanda "tidak layak"; ia hanya tidak dijalankan pada sesi itu.
- **Alat:** `designs/lettering-v1/run_v12.sh` (logik langkau diuji dengan arahan palsu, 26 Nov; belum diuji pada larian jana sebenar).

### Pemilihan tujuh model (semakan 26 Nov 2026)
Hasil lama dengan rangka am, AI Image Test 2 (150 imej, 5 gaya × 3 ayat × 2 seed, CPU, semakan mata, bukti lemah):

| Model | Lulus QC | Ejaan betul | Keputusan |
|---|---|---|---|
| MOSS-Image SFT + LoRA | 23/30 | 30/30 | Kekal |
| ERNIE-Image-Turbo | 21/30 | 29/30 | Kekal |
| Z-Image Turbo | 13/30 | 26/30 | Kekal |
| FLUX.2 klein 4B | 7/30 | 14/30 | Kekal; aturan sendiri menaikkan ejaan 0/3 → 3/3 pada K3 |
| FLUX.1 schnell | 1/30 | 3/30 | Tidak dipilih |

Dinilai dan tidak dipilih:
- FLUX.1 schnell: 3/30 ejaan betul; perkataan berulang.
- Chroma1-Flash: 0/6 ejaan betul pada ujian K6, kira-kira 562 saat setiap imej di CPU.
- Ovis-Image-7B: skor teks pembuat kuat (CVTG-2K 0.920), tetapi 50 langkah terlalu perlahan di CPU dan tiada Space yang disambungkan. Simpanan: calon kelapan jika GLM-Image gagal ujian kelayakan.
- HiDream-O1-Image-Dev: perlu GPU Kaggle; belum ada laluan jalan.
- ERNIE-Image dan Z-Image penuh (50 langkah): keluarga yang sama dengan versi Turbo, terlalu perlahan di CPU.

Sebab tiga yang dipilih:
- FLUX 3 Image Klein: ujian bebas 30 poster, 18 tepat, tertinggi dalam ujian itu (pihak ketiga); menyokong kotak susun atur dan gambar rujukan.
- Qwen-Image-2512: rupa paling kaya dalam ujian lama kita; kemas kini Disember memperbaik teks (kad model, rasmi).
- GLM-Image: pengekod huruf khas (Glyph Encoder, kad model, rasmi); hasil lama lemah, jadi ia paling berisiko antara tiga.
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
- Peraturan ulang: lihat "Kitaran QC" di bawah (v1.2; menggantikan peraturan 4 cubaan v1).
- Pilihan antara imej yang lulus: skor ciri kad, kemudian keterbacaan.
- Kalibrasi: jika pengguna menolak imej yang lulus QC, sebabnya ditambah ke kad.

### Kitaran QC (v1.2)
Turutan semakan setiap imej: pintu wajib G1–G3 → ukur dan betulkan (5b) → ciri kad → pengguna (langkah 7).

1. **Pusingan 0:** jana seed ikut laluan (laluan 1: 42, 7; laluan 2: 42, 7, 123), dengan prompt ikut aturan model (langkah 3).
2. **Ada imej lulus:** terus ke langkah 7. Kitaran tamat, tetapi belajar 3.15 tetap dijalankan (cacat pada imej lain dan ciri gaya masih dipelajari).
3. **Tiada imej lulus:** kelaskan cacat.
   - **Cacat rawak** (cacat pada satu seed sahaja, atau cacat berbeza-beza): jana seed seterusnya dalam senarai tetap (123, kemudian 2024). Prompt TIDAK diubah.
   - **Cacat sistematik** (cacat yang SAMA pada sekurang-kurangnya 2 daripada 3 seed; laluan 1 menjana seed 123 dahulu untuk memutuskan): reka semula prompt model itu (butir 4).
4. **Reka semula prompt:** SATU ubahan setiap pusingan, pada bahagian aturan model yang berkaitan dengan cacat itu. Jana semula dengan seed yang sama (42, 7, 123) supaya boleh dibanding. Had: 2 pusingan bagi setiap model untuk satu design.

| Cacat sistematik | Ubahan pertama untuk dicuba |
|---|---|
| Perkataan berulang atau tertinggal | Cara menulis baris teks ikut aturan model (klein: satu ayat prosa setiap baris; ERNIE: PE hidup) |
| Teks rawak atau label tambahan | Buang perkataan berisiko daripada ayat had (label, logo, signature, watermark); tulis had sebagai ayat positif |
| Perkataan tidak di dalam label | Tulis bekas dahulu, perkataan kemudian ("a small white label, and inside that label the word …") |
| Hiasan yang tidak diminta | Nyatakan hiasan yang dibenarkan dengan tepat, tambah "clean empty background" |
| Hiasan di tempat salah | Nyatakan kedudukan (kiri dan kanan, di luar label) |
| Satu perkataan salah eja berulang | Huruf besar untuk baris itu jika kad membenarkan; kemudian tukar peranan perkataan itu |
| Ruang tepi, kedudukan, condong, kelabu | Bukan prompt: skrip pembetulan (5b) |
| Bentuk huruf hodoh atau nisbah baris salah | Frasa bentuk huruf atau hierarki dalam aturan model; jika masih gagal, tukar model |

5. **Ubahan berjaya** (lebih banyak seed lulus daripada sebelumnya, tiada cacat baharu): ditulis balik terus, tanpa tanya (3.15), ke aturan model itu (3.4–3.10), rev naik, dicatat dalam "Catatan pembaikan aturan model". Design seterusnya terus memakai aturan yang sudah dibaiki.
6. **Ubahan tidak berjaya:** dibuang, dan dicatat juga supaya tidak diulang.
7. **Selepas 2 pusingan masih tiada imej lulus:** tukar ke model seterusnya ikut jadual model × gaya; kemudian pendekkan ayat; kemudian lapor kepada pengguna.
8. **Had imej:** paling banyak 10 imej bagi setiap model untuk satu design (4 seed + 2 pusingan × 3 seed).
9. **Penolakan pengguna** ("tidak cantik", langkah 7) pada imej yang lulus QC dikira cacat. Sebabnya ditambah ke kad sebagai ciri QC atau ukuran. Jika sebab yang sama berulang pada 2 design dengan model yang sama, ia masuk ke aturan model itu.

## Langkah 5b: Pembetulan selepas jana oleh skrip (v1.2)
- **Tempat dalam QC:** selepas pintu wajib G1–G3 lulus, sebelum semakan ciri kad. Imej yang gagal G1–G3 tidak dibetulkan; ia dijana semula.
- **Prinsip:** ukur dahulu. Hanya ukuran yang tersasar daripada ukuran rujukan kad (langkah 1) melebihi had dibetulkan. Ukuran dalam had: imej tidak disentuh.
- **Hanya ciri yang ada pada kad:** kad yang menyatakan "tiada condong" tidak pernah diputar. Kad tanpa ukuran rujukan: tiada pembetulan dijalankan.
- **Empat pembetulan, turutan tetap:**
  1. Condong: putar seluruh blok ke sudut rujukan kad; bucu diisi hitam.
  2. Ruang tepi: skala blok supaya ruang tepi sama dengan nilai kad.
  3. Kedudukan: pusatkan blok pada kanvas.
  4. Hitam putih bersih: tukar kelabu dan tepi kabur kepada hitam dan putih tulen. Dibuat akhir sekali, kerana putar dan skala menghasilkan tepi kelabu.
- **Selepas pembetulan:** ukur semula; pastikan tiada dakwat menyentuh tepi kanvas (huruf terpotong); semak semula ejaan pada imej yang dibetulkan. Masih tersasar atau ada huruf terpotong: jana semula.
- **Ditangguh (berisiko):** membuang hiasan yang tidak diminta. Skrip boleh tersilap membuang titik huruf atau hiasan yang memang diminta.
- **Tidak boleh dibetulkan skrip (masuk kitaran QC):** ejaan, perkataan berulang, bentuk huruf, nisbah saiz antara baris yang bertindih.
- **Log:** ukuran sebelum, pembetulan yang dijalankan, ukuran selepas. Imej mentah asal tidak ditimpa; imej yang dibetulkan disimpan berasingan.
- **Skrip (dibina 26 Nov 2026):** `designs/lettering-v1/skrip/betulkan.py` menjalankan SK01 → SK02 → SK03 → SK04 dan menulis `log_5b.jsonl`. Tiga pembetulan pertama digabung menjadi satu putaran + skala + alihan, supaya imej dilukis semula sekali sahaja.
- **Angka rujukan:** diukur skrip SK05 daripada gambar upload dan disimpan pada kad (`kad.BLOK[..]["rujukan"]`). K3: condong 7.6°, ruang tepi 13.6% (IMG_5775, satu gambar). Kad lain belum diukur; tanpa sudut rujukan, SK01 tidak jalan.
- **Had toleransi (cadangan Claude, diluluskan pengguna 27 Nov 2026):** condong ±1.5°; ruang tepi ±2 mata peratus; kedudukan ±1.5% kanvas; kelabu rata 0.3% piksel. Belum ditentukur daripada ujian; boleh diubah bila ada data.
- **Ujian (26 Nov 2026, tanpa jana baharu):** 12 imej K3H sedia ada (aturan model) dibetulkan; kesemuanya sampai ke condong 7.5–7.7° dan ruang tepi 13.2–13.7%, tiada dakwat menyentuh tepi. Semakan mata pada 4 imej: ejaan tidak berubah. Bukti lemah (satu kad).
- **Had skrip:** SK04 tidak menyentuh kad yang memang ada bayang lembut (K1). Sudut diukur daripada garis dasar baris, bukan condong italik huruf.
- Ruang tepi untuk cetak kekal urusan kemasan (langkah 6); pembetulan di sini hanya supaya imej mentah menepati kad.

## Langkah 6: Kemasan ikut kad
- Bermula hanya selepas QC mentah (hitam putih) lulus. Urutan skrip (27 Nov 2026): SK07 warna C ikut peranan → SK08 bayang → SK06 vektor + tekstur + saiz cetak → QC akhir. Warna dan bayang dibuat pada imej rata (resolusi asal, tepi anti-alias dikekalkan) sebelum vektor, kerana peta peranan dan bayang perlukan piksel; SK06 menyurih semua lapisan sekali dengan palet tepat (`--palet`).
- Jalan penuh: `python3 skrip/kemasan.py <kad> <ayat> <gaya S1..S6> <folder keluar> <imej…> [--warna Cxxx] [--sizes 18x24]`. Imej yang GAGAL SK07 dilangkau dan dilapor.
- Kelas: F1 vektor rata; F2 rata + tekstur. F3 raster: ditangguh.
- Parameter dibaca daripada kad (ruang tepi, tekstur, bilangan dakwat, butiran halus), bukan tetap dalam skrip.
- Semakan automatik: bilangan lapisan = bilangan dakwat dijangka; peratus dakwat hilang berbanding imej mentah; amaran jika melebihi ambang. Ambang butiran halus ikut gaya.
- Warna C diletak oleh skrip ikut peta peranan kad; satu imej lulus boleh jadi beberapa varian warna C tanpa jana semula.
- Had: perkataan yang hurufnya bertaut merentas baris tidak selalu boleh diasingkan untuk warna berbeza. SK07 membelah baris bertaut pada garis mendatar yang paling sedikit dakwat (amaran); jika label tidak segi empat atau baris masuk teras baris lain > 30%, SK07 GAGAL dan imej itu kekal hitam putih atau dijana semula. Bayang 3D dalam huruf (K3) dibina semula oleh SK08; bayang lembut K1 belum boleh (lihat SK08). Tekstur oleh SK06.
- Tekstur: seed berbeza setiap design; jenis dan kekuatan ikut kad.
- Cetak: 300 DPI (Printify, rasmi), saiz 8×10, 11×14, 16×20, 18×24, 24×36. Bleed, kawasan selamat, had saiz fail dan profil warna: belum disemak.
- Simpan SVG induk + info; PNG besar dijana semula bila perlu; versi `finish.py` direkod.

## Daftar skrip dan kaedah skrip baharu (v1.2, arahan pengguna 26 Nov 2026)
Skrip di sini ialah kerja SELEPAS jana (pembetulan 5b dan kemasan langkah 6). Alat prompt dan jana ada dalam 3.13 dan langkah 4.

| ID | Skrip | Langkah | Tugas | Parameter daripada kad | Status (26 Nov 2026) |
|---|---|---|---|---|---|
| SK01 | Condong (`SK01_condong.py`) | 5b | Putar blok ke sudut rujukan kad | sudut condong | Dibina; diuji pada 12 imej K3H sedia ada |
| SK02 | Ruang tepi (`SK02_ruang_tepi.py`) | 5b | Skala blok supaya ruang tepi sama dengan kad | ruang tepi (%) | Dibina; diuji pada 12 imej K3H sedia ada. **5b v1.2 (27 Nov 2026, Belajar SK, ubahan `ukur_semula_selepas_SK04`, MENANG):** selepas SK04 ruang tepi diukur semula; jika masih di luar had, SK02 dijalankan sekali lagi (matriks gabungan pada imej asal). 55 imej v12c-cpu: 52/55 → 54/55 **5b v1.3 (28 Nov 2026, gabungan cawangan):** bersama SK01 `ukur_semula` (sleepy-edison); v12c 55/55, v12b 47/48 |
| SK03 | Kedudukan (`SK03_kedudukan.py`) | 5b | Pusatkan blok pada kanvas | – | Dibina; diuji pada 12 imej K3H sedia ada |
| SK04 | Hitam putih bersih (`SK04_hitam_putih.py`) | 5b | Tukar kelabu dan tepi kabur kepada hitam dan putih tulen | – | Dibina; diuji pada 12 imej K3H sedia ada |
| SK05 | Ukuran (`SK05_ukur.py`) | 1, 5b | Ukur ruang tepi, kedudukan, sudut condong dan kelabu pada gambar upload atau imej mentah | – | Dibina; diuji pada 2 gambar upload (K3, K6) dan 24 imej K3H. Nisbah baris: anggaran sahaja (baris bertindih tidak dapat diasingkan) |
| SK06 | Vektor + saiz cetak (`SK06_finish.py` + `styles.py`) | 6 | SVG induk, susun di tengah, PNG 300 DPI | ruang tepi, tekstur | Dibawa dari `claude/dazzling-cannon-5wzn6h`; diuji pada 1 imej K3H selepas 5b (SVG + 18×24). 27 Nov: parameter `--palet` ditambah (warna tepat SK07 / SK08, topeng setiap warna dilembutkan sebelum surih). Ruang tepi dan tekstur masih tetap S1–S6, belum dibaca daripada kad. **v1.1 (27 Nov 2026, Belajar SK, ubahan `tekstur_kad`, MENANG):** `--kad Kx` = jenis dan kekuatan tekstur daripada kad (kapur, lusuh / grunge, butir; "halus" = 0.6); bahagian tanpa jenis = amaran, diganti tekstur gaya daripada gambar upload yang sama (K8 → S4). **v1.2 (27 Nov 2026, ubahan `tepi_kad`, MENANG):** ruang tepi setiap saiz poster ikut kad (sama seperti SK02), diukur pada blok tulisan; amaran jika beza > 2 mata atau dakwat sentuh tepi. **v1.3 (27 Nov 2026, ubahan `tekstur_marker`, MENANG):** jenis tekstur `marker` (butir latar + butir dakwat) dengan parameter diukur pada gambar upload kad (`--ukur-tekstur`, disimpan di `rujukan.tekstur`); butir dijana pada skala rujukan dan hasil diukur semula (amaran jika beza > 30%) **v1.4 (27 Nov 2026, ubahan `titik_halus`, MENANG):** had komponen dakwat 30 → 4 px (skala imej asal); garis titik dan bintik latar K4 kekal. **v1.5 (ubahan `lusuh_saring_cop`, MENANG):** K32 'lusuh cetakan saring' dan K33 'lusuh cop kering' = jenis worn. **v1.6 (ubahan `nota_kurungan`, MENANG):** nota dalam kurungan pada teks tekstur kad diabaikan (K30 'tiada (vektor rata)' = tiada) |
| SK06 | Vektor + saiz cetak (`SK06_finish.py` + `styles.py`) | 6 | SVG induk, susun di tengah, PNG 300 DPI | ruang tepi, tekstur | Dibawa dari `claude/dazzling-cannon-5wzn6h`; diuji pada 1 imej K3H selepas 5b (SVG + 18×24). 27 Nov: parameter `--palet` ditambah (warna tepat SK07 / SK08, topeng setiap warna dilembutkan sebelum surih). Ruang tepi dan tekstur masih tetap S1–S6, belum dibaca daripada kad. **v1.1 (27 Nov 2026, Belajar SK, ubahan `tekstur_kad`, MENANG):** `--kad Kx` = jenis dan kekuatan tekstur daripada kad (kapur, lusuh / grunge, butir; "halus" = 0.6); bahagian tanpa jenis = amaran, diganti tekstur gaya daripada gambar upload yang sama (K8 → S4). **v1.2 (27 Nov 2026, ubahan `tepi_kad`, MENANG):** ruang tepi setiap saiz poster ikut kad (sama seperti SK02), diukur pada blok tulisan; amaran jika beza > 2 mata atau dakwat sentuh tepi. **v1.3 (27 Nov 2026, ubahan `tekstur_marker`, MENANG):** jenis tekstur `marker` (butir latar + butir dakwat) dengan parameter diukur pada gambar upload kad (`--ukur-tekstur`, disimpan di `rujukan.tekstur`); butir dijana pada skala rujukan dan hasil diukur semula (amaran jika beza > 30%). **v1.4 (27 Nov 2026, ubahan `tekstur_calar_semburan`, MENANG):** jenis `calar` (calar lurus nipis + bintik, K10) dan `semburan` (butir semburan kasar, K13); parameter = pecahan lubang dalam dakwat diukur pada gambar upload (`--ukur-tekstur --songsang` untuk dakwat gelap atas latar cerah), ditentukur sehingga 3 kali dan diukur semula |
| SK07 | Warna C ikut peranan (`SK07_warna.py`) | 6 | Peta peranan setiap piksel (utama, sokongan, penyambung, hiasan) ikut baris Spesifikasi Teks, kemudian warna kad atau warna C | `peta_warna`, `warna` (kad); `--warna Cxxx` (Daftar S/C) | Dibina 27 Nov 2026; diuji pada 14 imej K3K (12 lulus, 2 GAGAL dikesan betul) + K7M, K8G (satu dakwat, tidak rosak) + 1 varian C001. **v1.1 (27 Nov 2026, Belajar SK, ubahan `belah_leher`, MENANG):** huruf bertaut merentas baris dibelah pada leher paling sempit; 15 imej K3K: 15/15 tanpa cacat SK (v1: 13/15) |
| SK06 | Vektor + saiz cetak (`SK06_finish.py` + `styles.py`) | 6 | SVG induk, susun di tengah, PNG 300 DPI | ruang tepi, tekstur | Dibawa dari `claude/dazzling-cannon-5wzn6h`; diuji pada 1 imej K3H selepas 5b (SVG + 18×24). 27 Nov: parameter `--palet` ditambah (warna tepat SK07 / SK08, topeng setiap warna dilembutkan sebelum surih). Ruang tepi dan tekstur masih tetap S1–S6, belum dibaca daripada kad. **v1.1 (27 Nov 2026, Belajar SK, ubahan `tekstur_kad`, MENANG):** `--kad Kx` = jenis dan kekuatan tekstur daripada kad (kapur, lusuh / grunge, butir; "halus" = 0.6); bahagian tanpa jenis = amaran, diganti tekstur gaya daripada gambar upload yang sama (K8 → S4). **v1.2 (27 Nov 2026, ubahan `tepi_kad`, MENANG):** ruang tepi setiap saiz poster ikut kad (sama seperti SK02), diukur pada blok tulisan; amaran jika beza > 2 mata atau dakwat sentuh tepi. **v1.3 (27 Nov 2026, ubahan `tekstur_marker`, MENANG):** jenis tekstur `marker` (butir latar + butir dakwat) dengan parameter diukur pada gambar upload kad (`--ukur-tekstur`, disimpan di `rujukan.tekstur`); butir dijana pada skala rujukan dan hasil diukur semula (amaran jika beza > 30%) |
| SK07 | Warna C ikut peranan (`SK07_warna.py`) | 6 | Peta peranan setiap piksel (utama, sokongan, penyambung, hiasan) ikut baris Spesifikasi Teks, kemudian warna kad atau warna C | `peta_warna`, `warna` (kad); `--warna Cxxx` (Daftar S/C) | Dibina 27 Nov 2026; diuji pada 14 imej K3K (12 lulus, 2 GAGAL dikesan betul) + K7M, K8G (satu dakwat, tidak rosak) + 1 varian C001. **v1.1 (27 Nov 2026, Belajar SK, ubahan `belah_leher`, MENANG):** huruf bertaut merentas baris dibelah pada leher paling sempit; 15 imej K3K: 15/15 tanpa cacat SK (v1: 13/15). **v1.2 (27 Nov 2026, Belajar SK, parameter `hitam_putih`, MENANG):** `--warna HP` = latar kad + dakwat pertama kad untuk semua peranan (poster hitam putih sahaja; cth. K13 tanpa kuning); 17 imej K43i / K44j, 5 model: 17/17 lulus. **v1.3 (`hp_neutral`):** HP pada kad berwarna (K9–K11) = satu dakwat neutral paling kontras dengan latar, atau putih / hitam tulen (K10: putih); K12, K13 sama seperti v1.2 |
| SK08 | Bayang ikut kad (`SK08_bayang.py`) | 6 | Bayang 3D dalam huruf: bahagian bawah setiap strok peranan yang diminta jadi kelabu | `rujukan.bayang` (arah, nisbah, warna; diukur `--ukur` pada gambar upload) | Dibina 27 Nov 2026; diukur pada IMG_5775; diuji pada 12 imej K3K yang lulus SK07. Bayang lembut K1 belum (lihat bawah) |

Semua skrip di `designs/lettering-v1/skrip/`. Jalan 5b penuh: `python3 skrip/betulkan.py <kad> <folder keluar> <imej…> [--condong D] [--tepi P]` (satu folder keluar bagi setiap model). Ukur gambar upload: `python3 skrip/SK05_ukur.py <gambar>`.

Empat skrip pembetulan (SK01–SK04) ialah set asas. Skrip lain ditambah hanya ikut kaedah di bawah.

**Bila skrip baharu perlu:**
1. Semasa Kad Gaya dibuat daripada gambar upload: ada ciri yang AI tidak dibenarkan atau tidak boleh jana dalam hitam putih (warna, bayang, tekstur, kecerunan), atau ciri yang mesti tepat ukurannya (lengkung, condong, jarak), dan tiada skrip dalam daftar yang membuatnya.
2. Dalam kitaran QC: cacat yang sama berulang, dan ia bukan soal ejaan atau bentuk huruf (jadual kitaran QC, baris "Bukan prompt").

**Kaedah skrip baharu:**
1. **Nyatakan ciri itu pada kad:** ciri QC + ukuran daripada gambar upload, dan rujuk gambar itu (cth. IMG_5775). Skrip bergantung kepada gambar upload, bukan tekaan.
2. **Semak daftar dahulu:** jika skrip sedia ada boleh diberi parameter baharu, tambah parameter; jangan buat skrip baharu.
3. **Tulis skrip:** satu tugas satu skrip; parameter dibaca daripada kad, bukan tetap dalam skrip; input = imej yang lulus G1–G3; hasil disimpan berasingan (imej asal tidak ditimpa); log ukuran sebelum dan selepas.
4. **Simpan:** `designs/lettering-v1/skrip/<ID>_<nama>.py`. Kepala fail mencatat: ID, tugas, kad dan gambar upload yang memerlukannya, parameter kad, versi, tarikh.
5. **Uji pada imej yang sudah ada** (tiada jana baharu): sekurang-kurangnya 1 imej lulus daripada kad itu dan 1 imej kad lain (pastikan tidak merosakkan). Ejaan disemak semula selepas skrip.
6. **Daftar:** tambah baris dalam jadual di atas (ID seterusnya), dan catat ID itu pada kad yang memerlukannya. Nombor versi standard kekal v1.2.
7. **Dashboard:** kemas kini tab FC › Design (langkah 5 atau 6) dan tab Aliran dalam sesi yang sama.
8. **Beritahu pengguna dalam chat:** skrip apa, untuk gambar mana, hasil ujian.

**Turutan jalan:** skrip pembetulan baharu masuk SEBELUM SK04, kerana hitam putih bersih mesti akhir sekali. Skrip kemasan baharu ikut urutan langkah 6: warna (SK07), bayang (SK08), kemudian vektor + tekstur + saiz cetak (SK06).

**SK07 dan SK08 (dibina 27 Nov 2026, diluluskan pengguna: tanpa GIMP / Inkscape, Python sahaja):**
- **SK07 kaedah:** sudut condong (SK05) → komponen bersambung dikumpul ikut julat teras menegak → kumpulan = baris Spesifikasi Teks (lebih: gabung yang paling rapat; kurang: kumpulan paling tinggi dibelah pada garis paling nipis) → komponen kecil di luar julat perkataan = hiasan → dalam baris berlabel, ekor huruf baris jiran di luar segi empat label dipulangkan → warna. Huruf dalam label = lubang, jadi kekal hitam. Tepi anti-alias imej 5b disimpan (`_alfa.png`) supaya tepi cetak licin.
- **SK07 v1.1 (27 Nov 2026, Belajar SK):** komponen setinggi >= 1.6 x tinggi median huruf (huruf bertaut merentas baris) dikumpul ikut julat penuh; komponen yang melintas garis potong dibelah pada leher paling sempit (watershed atas jarak ke tepi dakwat) antara dua baris berjiran tanpa label; di sekitar label kekal cara v1 (label ialah bingkai berlubang, tiada leher yang jelas). Ujian pertama cuba leher di mana-mana: label AFTER terbelah dua warna pada 3 imej, jadi dihadkan.
- **SK07 ujian (14 imej K3K selepas 5b, 5 model):** 12 lulus; 2 GAGAL dengan sebab betul (ernie s123: baris salah dibelah; zturbo s7: tiada label segi empat). Cacat yang masih nampak: ernie s42, puncak huruf S "Stays" yang bersentuh KINDNESS ikut kuning (amaran "dibelah" dicatat); dibuang atas arahan pengguna 27 Nov 2026. Kad satu dakwat K7M, K8G: tukar warna sahaja, tidak rosak. Varian C001 pada MOSS s42: lulus.
- **SK07 ujian (14 imej K3K selepas 5b, 5 model):** 12 lulus; 2 GAGAL dengan sebab betul (ernie s123: baris salah dibelah; zturbo s7: tiada label segi empat). Cacat yang masih nampak: ernie s42, puncak huruf S "Stays" yang bersentuh KINDNESS ikut kuning (amaran "dibelah" dicatat; pengguna semak di langkah 7). Kad satu dakwat K7M, K8G: tukar warna sahaja, tidak rosak. Varian C001 pada MOSS s42: lulus.
- **SK08 ukuran IMG_5775 (salinan dashboard 236×354, satu gambar, anggaran):** bayang BUKAN di luar huruf. Bahagian bawah setiap strok skrip putih berwarna kelabu cerah (dua tona rata). Model: piksel dalam 40% larian strok yang paling hampir dengan arah 250° (relatif garis dasar, iaitu ke bawah dan sedikit ke kiri) = kelabu. Warna diukur #b2b3b5; putih #f1f1f3. Padanan model dengan gambar: IoU 0.389; kongsi kelabu dalam huruf 28.6% (model 35.3%). Kad K3 sebelum ini menulis "kelabu gelap #3a3a3a di bawah / kanan" tanpa ukuran; kad kini guna ukuran.
- **SK08 ujian:** 12 imej K3K yang lulus SK07: kongsi bayang 33.6–36.5% setiap imej (rujukan model 35.3%), tiada amaran.
- **SK08 had:** bayang lembut K1 (IMG_5818: bayang jatuh atas coretan lain di bawahnya) tidak boleh dibuat daripada imej hitam putih rata, kerana susunan coretan (mana di atas) tiada. Kad lain belum ada rujukan bayang.
- **Hasil:** `designs/lettering-v1/final/v12-cpu-sk07/` (SVG induk + pratonton 18×24; PNG 300 DPI dijana semula bila perlu), `final/v12-cpu-sk07/peranan/` (peta, imej berwarna, palet, `log_6.jsonl`), helaian `qc/sk07_sk08_kemasan.jpg`.
- **Simpanan (keputusan pengguna 27 Nov 2026: SNC):** 11 design K3K berwarna + 1 varian C001 didaftar sebagai warna C011–C022 (gambar = pratonton 18×24, medan `gaya` = kod S imej hitam putih asal). Tiga imej hitam putih FLUX 3 Klein K3K (lesen diterima) didaftar sebagai gaya S036–S038 supaya design berwarna itu ada kod S. C008 dikemas kini: kelabu bayang #3a3a3a → #b2b3b5 (ukuran SK08). Peta rekod: `designs/lettering-v1/qc/sk07_sk08_snc.json`.

### Belajar SK selepas setiap batch: skrip dibaiki atau dicipta sendiri (keputusan pengguna 27 Nov 2026)
**Tujuan:** sama seperti 3.15 untuk aturan prompt, tetapi untuk skrip SK. Setiap batch menambah bukti; kelemahan SK dibaiki, parameter kad yang belum dibaca ditambah, dan cacat tanpa SK mendapat SK baharu. Bukti, bukan tekaan.

**Bila:** selepas SETIAP batch, selepas 5b dan langkah 6, dan selepas `belajar.py` (3.15). Tiada jana tambahan.

**Langkah (Claude, dalam sesi yang sama, tanpa tanya):**
1. Salin stor dashboard (sama seperti 3.15 langkah 1).
2. Rekod keputusan pengguna pada imej siap dalam `belajar/sk_pengguna.jsonl`, satu baris setiap imej: `{"imej": "<batch>/<model>/<ID>_s<seed>[+Cxxx]", "keputusan": "lulus" atau "tolak", "sebab": "...", "sk": "SK08" (pilihan)}`. Tolak dalam `pengguna.jsonl` yang sebabnya milik SK, dan kod C yang dipadam daripada Daftar S/C, juga dikira.
3. Jalan `python3 belajar_sk.py` (dalam `designs/lettering-v1/`). Hasil: `belajar/sk_log.jsonl` (sejarah imej × SK × versi; versi lama kekal untuk banding), `belajar/sk_ringkasan.json`, `data/export/ai_tests/sk_belajar.json` (dashboard), dan TINDAKAN bagi setiap SK.
4. Laksana setiap TINDAKAN terus, kemudian lapor dalam jadual jawapan:
   - **SEMAK:** lihat imej yang GAGAL atau ada amaran; tulis `belajar/sk_semakan.jsonl`: `silap` (kelemahan SK; `kelas` pilihan) atau `betul` (imej input rosak, atau amaran tidak merosakkan). Input rosak = jana semula / 3.15, bukan kerja SK.
   - **BAIKI:** satu ubahan kod pada SK itu; naikkan `VERSI` (SK01–SK04: `VERSI` dalam `betulkan.py`); tambah baris `cuba` dalam `belajar/sk_ubahan.json` (`sk`, `ubahan`, `kelas`, `dari`, `ke`, `imej`, `tarikh`); jalan semula SK pada imej yang sama (tiada jana); jalan `belajar_sk.py` semula.
   - **MENANG:** tanda `menang`; kemas kini jadual Daftar skrip (versi, status) dan "Catatan pembaikan SK".
   - **KALAH:** pulangkan kod ke versi lama (git); tanda `kalah`; ia tidak dicuba lagi.
   - **UJI SEMULA:** jalan semula SK versi baharu pada imej yang sama.
   - **PARAMETER:** tambah parameter yang dibaca daripada kad (kaedah skrip baharu langkah 2), dijalankan sebagai ubahan (cuba, kemudian menang / kalah).
   - **UKUR:** ukur gambar upload kad (SK05; SK08 `--ukur`), tulis rujukan pada kad.
   - **SK BAHARU:** cipta terus ikut "Kaedah skrip baharu" 1–8; tambah kelas cacatnya ke `KELAS_SK` dalam `belajar_sk.py` dengan pemilik SK baharu; kepala fail ada `LANGKAH = "..."` dan `VERSI = "..."`.
   - **HABIS:** 3 ubahan kalah bagi kelas yang sama: lapor pengguna; imej itu jana semula.
   - **TANYA:** imej ditolak tanpa sebab: tanya pengguna sebabnya (dalam jadual).
5. Muat naik `sk_belajar.json` ke dashboard (dataset `sk_belajar`, tab AI Image Test) dan simpan semua fail dalam git.

**Peraturan belajar SK (kod: `belajar_sk.py`, versi s1):**
- **Isyarat:** GAGAL dan amaran dalam log SK (`log_5b.jsonl`, `log_6.jsonl`, `info.json`); semakan Claude; tolak pengguna; ♥.
- **Kelas cacat SK (`KELAS_SK`):** sentuh tepi, ruang tepi (SK02); condong (SK01); kedudukan (SK03); kelabu (SK04); label, baris salah dibelah, huruf bertaut dibelah, tiada huruf, warna (SK07); bayang (SK08); tekstur, vektor (SK06). "Ekor huruf dipulangkan" = maklumat, bukan cacat. Kelas yang sama dikeluarkan daripada belajar prompt (3.15, b1.1).
- **GAGAL kerana input rosak** (semakan `betul`) tidak dikira cacat SK. **Amaran** dikira cacat hanya selepas semakan `silap` atau tolak pengguna.
- **Cacat berulang** = kelas yang sama pada sekurang-kurangnya 2 imej, pada versi semasa SK.
- **Satu ubahan setiap kali** bagi setiap SK; banding pada imej yang sama. **Menang** = lebih banyak imej tanpa cacat SK (atau sama, tetapi kelas sasaran berkurang), tanpa kelas cacat baharu.
- **Tiada ulangan:** ubahan yang kalah disenarai dalam TINDAKAN supaya tidak dicuba lagi.
- **Liputan kad:** setiap kad yang pernah dijana disemak: condong tanpa rujukan sudut, tiada rujukan ruang tepi, lebih satu dakwat tanpa `peta_warna`, bayang tanpa rujukan atau jenis yang SK08 tidak boleh buat (SK baharu), tekstur dan ruang tepi kad yang SK06 belum baca (parameter).
- **SK baharu:** cacat tanpa SK pemilik pada sekurang-kurangnya 2 imej, atau ciri kad tanpa SK: dicipta terus (keputusan pengguna 27 Nov 2026) dan dilaporkan. 1 imej: dipantau.
- **Ubahan jenis parameter** (`jenis: parameter`, `medan`): menang = tiada cacat baharu, lulus tidak turun, semua imej versi baharu disemak, dan jurang kad bagi medan itu tertutup.
- **Versi:** setiap SK ada `VERSI` dalam kod dan log mencatatnya. SK06: `VERSI` ditambah 27 Nov 2026 (kod lain tidak berubah; `info.json` lama = SK06 v1).

**Had:** ini bukan AI yang belajar sendiri. Ia peraturan tetap yang dijalankan Claude selepas setiap batch. Bukti kecil (satu batch, satu kad berwarna) mudah tersilap.

**Keputusan pertama (27 Nov 2026; 34 imej, 177 baris imej × SK; ♥ 0; tolak 0; bukti lemah):**
- SK01–SK04 (5b v1.1): 0 cacat. UKUR: kad K6 tiada rujukan sudut dan ruang tepi (IMG_5734).
- SK06 v1: tekstur kad belum dibaca (K6, K7, K8): PARAMETER seterusnya; ruang tepi kad menyusul.
- SK07 v1: semakan Claude 10 imej: 2 `silap` (ernie K3K s42 dan s123: huruf bertaut merentas baris diwarna salah); zturbo K3K s7 = input rosak (tiada label); 7 amaran tidak merosakkan. TINDAKAN: BAIKI SK07 (kelas huruf bertaut dibelah).
- **BAIKI SK07 dilaksana (diluluskan pengguna 27 Nov 2026): MENANG.** v1.1 `belah_leher`: 15 imej yang sama, tanpa cacat SK 13/15 → 15/15, kelas huruf bertaut 2 → 0, tiada kelas baharu; 12 imej lain sama piksel demi piksel. Kemasan ernie K3K s42 dijana semula; ernie K3K s123 kini siap. Log uji: `belajar/uji_sk/SK07_v1.1/log_6.jsonl`.
- **PARAMETER SK06 dilaksana (diluluskan pengguna 27 Nov 2026): MENANG.** v1.1 `tekstur_kad`: 3 imej (K3K, K7M, K8G) 3/3 → 3/3 tanpa cacat; jurang "SK06 belum baca tekstur kad" tertutup; K3K dan K8G sama piksel dengan v1; K7M kini butir halus ikut kad K7 (sebelum ini butir penuh gaya S2). Kemasan K7M dan K8G dijana semula. Seterusnya: PARAMETER ruang tepi kad, kemudian jenis tekstur K8.
- **PARAMETER ruang tepi SK06 dilaksana (diluluskan pengguna 27 Nov 2026): MENANG.** v1.2 `tepi_kad`: 3 imej 3/3 → 3/3; ruang tepi yang diukur SK05 pada pratonton = kad dalam 0.1 mata (K3K 13.6 / 15.5, K7M 6.2, K8G 12.2); v1.1 lari sehingga 5.8 mata (K7M 12.0 lawan 6.2). Ujian pertama memuat kotak semua dakwat: titik hiasan K8 membuat blok terlalu kecil, jadi diukur pada blok tulisan seperti SK05. 16 kemasan dan helaian `qc/sk07_sk08_kemasan.jpg` dijana semula. Seterusnya: jenis tekstur K8; ukur kad K6.
- **Jenis tekstur K8 dan UKUR K6 dilaksana (diluluskan pengguna 27 Nov 2026).** Gambar upload diambil daripada Daftar S/C (medan `asal`: S011 = IMG_5734, S032 = IMG_5735). K6 (SK05): condong 11.8°, ruang tepi sisi 9.8%, atas / bawah 4.3% (swash atas hampir mencecah tepi). K8: SK06 v1.3 `tekstur_marker` MENANG: butir latar sederhana 5.93, awan 5.22, butir dakwat 4.68 = IMG_5735 (kapur S4 sebelum ini 1.67 / 1.13); K3K dan K7M sama piksel. Cubaan pertama turut meniru butir bawah 1 px dan kekasaran tepi: tepi huruf jadi bertakuk hitam, kerana pada JPEG 600×449 itu kesan mampatan, bukan tepi marker. Jadi dibuang; tepi kekal ikut imej AI. **Had:** tepi marker kering K8 perlu gambar upload yang lebih besar.
- SK08 v1: 0 cacat.

### Catatan pembaikan SK
Setiap ubahan SK direkod di sini dan dalam `designs/lettering-v1/belajar/sk_ubahan.json`.

| Tarikh | SK | Ubahan | Kelas cacat | Versi | Keputusan | Bukti |
|---|---|---|---|---|---|---|
| 27 Nov 2026 | SK06 | `tekstur_calar`: jenis tekstur calar + bintik lusuh dalam dakwat (kad K23, dahulu K12), parameter diukur pada panel koral IMG_5793 (`ukur_calar`) | tekstur (jenis kad K23) | v1.3 → v1.4 | MENANG | K23f: 0/2 → 1/2 tanpa cacat SK; moss 1.61 / 24.5 lawan rujukan 2.08 / 24.9; klein3 masih terlalu ringan (0.92 / 12.3, `silap`); imej kad lain sama piksel (K2e beza 0). Juga UKUR: K23 diukur semula di dalam panel (tepi sisi 8.5, atas / bawah 6.1; ukuran pertama silap), K2 (IMG_5792: sisi 13.4, bawah 10.6) dan K4 (IMG_5764, foto: atas / bawah 10.2, sisi 10.9). Bukti lemah |
| 28 Nov 2026 | SK01 + SK02 (5b) | `gabung_cawangan`: SK01 `ukur_semula` (sleepy-edison) + SK02 `ukur_semula_selepas_SK04` (focused-allen) dalam `betulkan.py` | condong, ruang tepi | 5b v1.2 → v1.3 | MENANG | Uji semula: v12c-cpu 55/55 (54/55), v12b-cpu 47/48 (baki = imej input rosak, sama seperti v1.1); tiada kelas baharu |
| 27 Nov 2026 | SK06 | `nota_kurungan`: nota dalam kurungan pada teks tekstur kad diabaikan | tekstur (amaran palsu K30) | v1.5 → v1.6 | MENANG | 2 imej K30R sama piksel; amaran 2 → 0. Bukti sederhana |
| 27 Nov 2026 | SK06 | `lusuh_saring_cop`: K32 'lusuh cetakan saring', K33 'lusuh cop kering' = jenis worn | tekstur (parameter kad) | v1.4 → v1.5 | MENANG | 5 imej: amaran 5 → 0; dakwat_sd 0.0 → 2.2–2.3 (IMG_5743 4.44); dilihat mata. Bukti lemah |
| 27 Nov 2026 | SK06 | `titik_halus`: had komponen dakwat `clean()` 30 → 4 px | vektor (garis titik K4 hilang) | v1.3 → v1.4 | MENANG | 2/2 imej K4F: garis titik + bintik latar kembali; 6 imej lain tiada hingar baharu (mata). Bukti lemah |
| 27 Nov 2026 | SK02 | `ukur_semula_selepas_SK04`: ruang tepi diukur semula selepas SK04, SK02 sekali lagi jika di luar had | ruang tepi (doodle halus dibersihkan, kotak mengecil) | 5b v1.1 → v1.2 | MENANG | 55 imej: 52/55 → 54/55; K31T 6/6 (v1.1 4/6); tiada kelas baharu |
| 28 Nov 2026 | SK01 (5b) | `ukur_semula`: selepas SK01 memutar, blok diukur semula dan baki sudut dibetulkan, paling banyak 2 kali lagi (`betulkan.py`) | condong (ukuran pertama tersasar) | 5b v1.1 → v1.2 | MENANG | 2 imej: 0/2 → 2/2 (klein3 K9B s123 13.4 → 15.2; ERNIE K7M s123 0.0 → 13.6, ukuran pertama 15.5 di had julat); semakan mata. Bukti lemah |
| 27 Nov 2026 | SK02 (betulkan.py) | `had_ikut_skala`: had bintik ukur SK05 didarab luas matriks selepas setiap pembetulan | ruang tepi (sinar kecil K14 masuk / keluar kotak selepas skala) | 5b v1.1 → v1.2 | MENANG | 56 imej K14–K18: lulus 5b 53/56 → 56/56; 51 sama piksel; ejaan tidak berubah. Cubaan pertama (hiasan rapat dalam SK05) dibatalkan: 35/158 kotak berubah termasuk 3 rujukan. Bukti lemah |
| 27 Nov 2026 | SK06 | `kata_tekstur`: kata kad 'bintik' / 'berbintik' = lusuh; 'tiada (rata)' = tiada | tekstur (parameter kad K9–K13) | v1.3 → v1.4 | MENANG | K40Q, K41g, K44j kini bertekstur lusuh berbintik (pratonton 18x24); K12 rata. K11 'retak kasar' belum ada jenis (tertangguh). Bukti lemah: mata, tidak diukur |
| 27 Nov 2026 | SK02 (SK05) | `bintik_relatif`: penapis bintik SK05 juga simpan komponen >= 1% komponen terbesar, jadi sengkang sisi K12 kekal dalam kotak selepas skala | ruang tepi | 5b v1.1 → v1.2 (SK05 v1.1 → v1.2) | MENANG | GAGAL ruang tepi 3 → 1 (ernie, FLUX 3 Klein K43i s7 kini 17.6 / 17.2 lawan 17.9); baki moss K44j s42 = SK04 kelabu; 53 imej dijalankan semula, tiada gagal baharu, 2 imej berubah. Bukti lemah: satu batch |
| 27 Nov 2026 | SK07 | `hp_neutral`: `--warna HP` = satu dakwat neutral paling kontras dengan latar (atau putih / hitam tulen); peta peranan dilangkau | warna (parameter) | v1.2 → v1.3 | MENANG | 53 imej K40Q–K44j: 53/53 lulus SK07 + SK06; v1.2 gagal pada K9 (tiada peta_warna) dan K10 (dakwat pertama merah) |
| 27 Nov 2026 | SK07 | `hitam_putih`: `--warna HP` = latar kad + dakwat pertama kad | warna (parameter) | v1.1 → v1.2 | MENANG | 17 imej K43i / K44j: 17/17 lulus |
| 27 Nov 2026 | SK06 | `tekstur_calar_semburan`: jenis tekstur calar (K10) dan semburan (K13), pecahan lubang dakwat diukur pada gambar upload, dijana pada skala rujukan, ditentukur | tekstur (jenis kad K10, K13) | v1.3 → v1.4 | MENANG | 19 imej: 19/19 → 19/19, jurang tertutup; lubang diukur semula K10 0.025–0.028 (rujukan 0.027), K13 0.104–0.115 (rujukan 0.106). Cubaan pertama: bintik petak piksel, calar bertangga; dibaiki sebelum keputusan. Had: arah / panjang calar prosedur; bintik < 1 px tidak diukur. Bukti lemah |
| 27 Nov 2026 | SK06 | `tekstur_marker`: jenis tekstur marker, parameter diukur pada gambar upload kad, dijana pada skala rujukan | tekstur (jenis kad K8) | v1.2 → v1.3 | MENANG | K8G diukur = IMG_5735 (5.93 / 5.22 / 4.68; v1.2: 1.67 / 1.13); K3K, K7M sama piksel. Had: tepi marker kering tidak diukur (JPEG kecil). Bukti lemah |
| 27 Nov 2026 | SK06 | `tepi_kad`: ruang tepi setiap saiz poster ikut kad (asas.rujukan, seperti SK02), diukur pada blok tulisan | ruang tepi (parameter kad) | v1.1 → v1.2 | MENANG | 3 imej: diukur = kad dalam 0.1 mata (v1.1 lari sehingga 5.8); tiada terpotong; 16 kemasan dijana semula. Bukti lemah |
| 27 Nov 2026 | SK06 | `tekstur_kad`: tekstur dibaca daripada kad (`--kad`); bahagian tanpa jenis = amaran + ganti gaya daripada gambar yang sama | tekstur (parameter kad) | v1 → v1.1 | MENANG | 3 imej: 3/3 → 3/3, jurang tertutup; K3K, K8G sama piksel; K7M butir halus (dilihat pada 300 DPI). Bukti lemah |
| 27 Nov 2026 | SK07 | `belah_leher`: komponen berbilang baris dikumpul ikut julat penuh; belah pada leher paling sempit antara baris tanpa label | huruf bertaut dibelah (sambungan) | v1 → v1.1 | MENANG | 15 imej K3K: 13/15 → 15/15; ernie s42 (puncak S kuning) dan s123 (baris salah dibelah) betul; 12 imej lain tidak berubah. Bukti lemah: satu batch, satu kad |

## Langkah 7: Pengguna lulus atau tolak
- **Mata pengguna ialah pintu terakhir (v1.2).** Imej yang lulus semua QC tetapi nampak buruk di mata pengguna = gagal. Skor QC tidak mengatasi keputusan pengguna.
- Pengguna memilih daripada SATU helaian; imej sudah ditapis oleh QC dahulu.
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
Model baharu juga memerlukan aturan prompt sendiri sebelum dipakai untuk design sebenar: ikut "Kaedah model baharu" (3.12). Model yang terlalu lama atau bermasalah semasa jana: ikut "Peraturan langkau model" (langkah 4).

## Larian v1.2 pertama (26–27 Nov 2026, semalaman, arahan pengguna)
- **Tugas:** tiga gambar upload, ayat diganti, ayat sama untuk semua model, 3 seed (42, 7, 123), CPU, hitam putih.
- **Design dan kad:**

| Id | Gambar upload | Kad | Ayat (cadangan Claude, diluluskan pengguna) | Rujukan diukur SK05 |
|---|---|---|---|---|
| K3K | IMG_5775 | K3 (sedia ada) | Kindness Stays After Words Fade | condong 7.5–7.6°, ruang tepi 13.6% |
| K7M | IMG_5765 (helaian 6 poster) | K7 (baharu) | Make Room for Wonder | condong 12.4° (median 6 panel, julat 10.1–14.5), ruang tepi 6.2% (julat 5.4–10.3) |
| K8G | IMG_5735 | K8 (baharu) | Keep Going You Are Almost There | condong 7.4°, ruang tepi 12.2% (gambar melintang, latar bertekstur) |

- **K7 dan K8** dibuat Claude daripada gambar; pengguna membenarkan jana tanpa menunggu kelulusan kad. **Kedua-dua kad diluluskan pengguna pada 27 Nov 2026** (v1.0).
- **Model (soalan pengguna: boleh semua 7 di CPU? jika tidak, yang boleh sahaja):**

| Model | Keputusan | Sebab |
|---|---|---|
| MOSS, ERNIE Turbo, Z-Image Turbo, klein 4B | Dijalankan di CPU | Profil dikunci, sudah diukur |
| FLUX 3 Image Klein | Dijalankan di CPU (berjaya pada cubaan ketiga) | Transformer 5.6B (11.1 GB bf16) + pengekod teks 8.3 GB, dimuat berasingan. Cubaan 1 gagal: pustaka torchvision tiada (dipasang). Cubaan 2 dihentikan: muat turun dalam pipeline hanya kira-kira 1.7 MB sesaat (muat turun terus dengan 8 sambungan menyelesaikannya). Cubaan 3: 357 s setiap imej |
| Qwen-Image-2512 | DILANGKAU, tidak dijalankan | Tidak muat: repo 57.7 GB (transformer kira-kira 41 GB) lawan RAM 15 GB; 50 langkah dengan CFG. Tidak diukur; keputusan daripada saiz fail (rasmi) |
| GLM-Image | DILANGKAU, tidak dijalankan | Tidak muat: repo 35.8 GB (pengekod 20 GB + transformer 15 GB) lawan RAM 15 GB; tiada GGUF. Tidak diukur; keputusan daripada saiz fail (rasmi) |

- **Simpanan imej (keputusan pengguna 27 Nov 2026: SNC, semua imej lulus):** 24 imej yang lulus ejaan didaftar sebagai gaya S012–S035 (gambar = imej selepas 5b), dan dua warna C009 (krim + butir, K7) dan C010 (putih pudar + kapur, K8). Imej FLUX 3 Klein tidak didaftar (lesen belum diterima); imej salah ejaan tidak didaftar. Pengguna memadam sendiri yang tidak mahu. Peta rekod: `designs/lettering-v1/qc/v12_cpu_snc.json`. Semua imej kekal dalam repo (`designs/lettering-v1/raw/v12-cpu/`).
- **Hasil pusingan 0** (45 imej; semakan mata Claude, bukti lemah; lulus = pintu G1 ejaan + G2 tiada teks atau tanda rawak). Rekod setiap imej: `designs/lettering-v1/qc/v12_cpu.json`. Helaian: `qc/v12_cpu_K3K.jpg`, `qc/v12_cpu_K7M.jpg`, `qc/v12_cpu_K8G.jpg`.

| Model | K3K | K7M | K8G | Jumlah | Masa model (termasuk muat turun) |
|---|---|---|---|---|---|
| MOSS + LoRA | 3/3 | 3/3 | 0/3 | 6/9 | 55 minit |
| ERNIE Turbo | 2/3 | 3/3 | 3/3 | 8/9 | 73 minit |
| Z-Image Turbo | 3/3 | 1/3 | 0/3 | 4/9 | 52 minit |
| klein 4B | 3/3 | 2/3 | 1/3 | 6/9 | 17 minit |
| FLUX 3 Image Klein (aturan r0) | 3/3 | 3/3 | 3/3 | 9/9 | 57 minit (muat turun berasingan, kira-kira 10 minit) |
| Jumlah | 14/15 | 12/15 | 7/15 | 33/45 | Qwen-Image-2512 dan GLM-Image dilangkau (tidak muat) |

- **Pembina kod (3.13):** K3 dengan ayat baharu memberi 11/12, sama dengan contoh tulisan tangan pada ayat H (11/12). Ayat berbeza, jadi ini bukti lemah bahawa pembina tidak lebih buruk.
- **PE ERNIE (3.6):** K3K seed PE 42 ditolak semakan (PE memetik huruf 'S' sebagai rujukan), seed 7 lulus; K7M dan K8G lulus pada seed 42.
- **Cacat yang sama pada 2 atau 3 seed (calon kitaran QC):**

| Model × kad | Cacat | Bilangan |
|---|---|---|
| MOSS × K8 | 'ALMOST' jadi 'ALMIST' / 'ALMiOST' | 3/3 |
| Z-Image × K8 | Baris 'KEEP GOING' dipisah jadi dua baris; bintik latar di hujung baris dibaca sebagai noktah | 3/3; 2/3 |
| Z-Image × K7 | Titik tambahan selepas perkataan | 2/3 |
| klein 4B × K3 | Percikan dilukis di dalam label (cacat r1 yang sudah diketahui) | 3/3 |
| Z-Image × K3 | Bintang menggantikan percikan; label kecil | 3/3 |
| ERNIE × K8 | Huruf berus nipis, bukan marker bulat tebal (gaya, bukan ejaan) | 3/3 |

- **Kitaran QC pusingan 1** (dua kes tanpa imej lulus; satu ubahan, seed sama; helaian `qc/v12_cpu_pusingan1.jpg`):

| Model × kad | Ubahan tunggal | Hasil | Keputusan |
|---|---|---|---|
| MOSS × K8 | Tukar peranan 'Almost' (utama → sokongan) dan 'There' (sokongan → utama), id K8J | 0/3 → 0/3 ('ALMiST' 3/3) | Tidak berjaya; dibuang. Tiada ubahan lain dalam jadual kitaran QC, jadi terus ke "tukar model" |
| Z-Image × K8 | Baris berbilang perkataan ditulis "as two words side by side on one line" | 0/3 → 0/3 (masih 5 baris; 'ALWOST' pada seed 7) | Tidak berjaya; dibuang |

- **Model × kad selepas larian ini** (bukti lemah, satu ayat setiap kad): K8 = ERNIE, FLUX 3 Klein (lulus 3/3), klein 4B (1/3); MOSS dan Z-Image tidak sesuai untuk K8. K7 = MOSS, ERNIE, FLUX 3 Klein (3/3), klein 4B (2/3), Z-Image (1/3). K3 = semua lima model (ERNIE 2/3, lain 3/3).
- **FLUX 3 Image Klein:** ujian pertama aturan 3.8 (kapsyen + jadual kotak, penambah prompt dibuang). 9/9 lulus G1–G2; kedudukan baris mengikut kotak. Pembanding rangka am dijalankan 27 Nov 2026 (`raw/v12-cpu-am/klein3`, QC `qc/v12_cpu_am.json`): rangka am 6/9, jadi aturan lulus ujian kelayakan dan rev naik r0 → r1. Lesen FLUX Kommunity: hasil komersial bersyarat; pengguna menerima lesen 27 Nov 2026 (lihat 3.8).
- **5b:** 33 imej yang lulus dibetulkan (24 + 9 FLUX 3 Klein); angka di bawah untuk 24 yang pertama: imej dibetulkan (`designs/lettering-v1/betul/v12-cpu/`, `log_5b.jsonl`); 0 gagal semakan akhir. Dua pembaikan skrip semasa larian: SK05 v1.1 (bintik latar di tepi tidak lagi menggagalkan imej) dan SK02 v1.1 (ruang tepi sisi dan atas / bawah berasingan; K3: 13.6 / 15.5, K7: 6.2 / 11.3).
- **Kemasan (SK06):** imej terbaik setiap design, pilihan Claude; pengguna memilih melalui Daftar S/C: K3K MOSS seed 42 (gaya S3, putih; warna kuning + bayang dibuat 27 Nov oleh SK07 + SK08, lihat daftar skrip), K7M MOSS seed 42 (gaya S2, krim + butir), K8G klein 4B seed 42 (gaya S4, kapur). Fail: `designs/lettering-v1/final/v12-cpu/` (SVG induk + pratonton 18×24); gambar ringkas `qc/v12_cpu_akhir.jpg`.

## Larian v1.2 kedua, batch v12c (27–28 Nov 2026, cawangan focused-allen)
- **Tugas:** lima gambar upload, ayat baharu (pilihan Claude), semua model CPU, 3 seed (42, 7, 123), hitam putih, QC + gaya. Qwen-Image-2512 dan GLM-Image dilangkau (tidak muat 4 CPU / 15 GB).
- **Design dan kad** (K30–K33 diluluskan pengguna 28 Nov 2026; asalnya K9–K12, ayat R / T / O asalnya B / N / Y: dinamakan semula 28 Nov 2026 kerana cawangan sleepy-edison memakai K9–K13 dan ayat B, V, N, Y untuk design lain):

| Id | Gambar upload | Kad | Ayat | Rujukan SK05 (condong; tepi sisi / atas-bawah) |
|---|---|---|---|---|
| K30R | IMG_5852 | K30 (baharu, skrip bersambung + swash) | Rise Anyway | 12.5°; 12.3 / 9.4% |
| K31T | IMG_5751 | K31 (baharu, berus + doodle, 2 dakwat) | Little Wins Build Brave Days | –; 17.6 / 9.4% |
| K32S | IMG_5739 | K32 (baharu, quirky, 2 dakwat) | Still Waiting For My Brilliant Idea | –; 15.0 / 7.9% |
| K4F | IMG_5727 | K4 (sedia ada, diukur SK05) | Hard Days Forge Steady Hearts | 1.0°; 9.6 / 11.8% (anggaran, foto atas kayu) |
| K33O | IMG_5743 | K33 (baharu, cop dalam kurungan) | Joy Is Loud! | –; 23.1 / 14.8% |

- Saringan cap dagangan ayat: `qc/v12c_ayat.json` ("Bold Moves" ditolak, diganti "Rise Anyway").
- **Masa CPU** (`raw/v12c-cpu/enjin_masa.jsonl`): MOSS 5990 s, ERNIE 8541 s, FLUX 3 Klein 7285 s, klein 4B 4006 s.
- **QC (`qc/v12c_cpu.json`, semakan mata huruf demi huruf; bukti lemah):** 55/75 lulus. MOSS 12/15, ERNIE 12/15, FLUX 3 Klein 14/15, Z-Image 9/15, klein 4B 8/15. K4F dan K33O lulus pada semua model (K33O klein 4B 2/3). K32S: MOSS dan ERNIE 0/3 (teks rawak di sisi: kapsyen penyambung "tucked tightly beside" + kotak penuh lebar), FLUX 3 Klein 2/3, Z-Image 1/3, klein 4B 0/3 (BRILLIANT hilang I). K30R: Z-Image dan klein 4B 0/3 ('Anyway' salah eja), model lain 3/3. Kitaran QC tamat tanpa larian semula (setiap design ada imej lulus).
- **5b:** 55 imej; v1.1 52/55, v1.2 54/55 (baki: ERNIE K30R s7 condong 15.5° lawan 12.5°, swash dikira dalam sudut; 1 imej, dipantau).
- **Kemasan:** 12 imej, gaya S3; kad 1 dakwat dengan warna C003 (SK07 → SK08 → SK06); K31 dan K32 (2 dakwat) terus SK06 `--kad` kerana tiada palet hitam putih 2 dakwat. `final/v12c-cpu/`, SK06 v1.4–v1.6.
- **Dashboard (pengguna 28 Nov 2026: A):** 75 imej + 12 poster siap + 5 gambar rujukan di tab AI Image Test sebagai ujian U17 (`data/ai_tests/rows/U17.json`, `qc/v12c_blobs.json`); U13–U16 sudah dipakai sesi lain. Calon prompt diluluskan untuk larian seterusnya.
- **Belajar (3.15):** calon `klein4b_hiasan_kedudukan`, `klein4b_cara_baris` (`zturbo_had_positif` dibuang: kalah di batch v12b; lihat Catatan pembaikan aturan model). "Cacat lain (tiada kelas)" ERNIE dan FLUX 3 Klein = nota imej lulus (ciri 7/8, SK04), bukan cacat.

## Larian v1.2 kedua, batch v12b (27–28 Nov 2026, cawangan sleepy-edison)
- **Tugas:** empat gambar upload, ayat baharu dipilih Claude, 3 seed (42, 7, 123), CPU, hitam putih, semua model yang muat.
- **Design dan kad (dibuat Claude; jana terus, kelulusan kad menyusul):**

| Id | Gambar upload | Kad | Ayat |
|---|---|---|---|
| K9B | IMG_5810 | K9 (baharu) | Build It Daily (tanda dagang hampir: BUILD DAILY, pakaian; pengguna kekalkan) |
| K10V | IMG_5804 | K10 (baharu) | Be Brave Do Good |
| K11N | IMG_5796 | K11 (baharu) | Begin Shaky. Grow Steady. Small steps add up. |
| K12Y | IMG_5797 | K12 (baharu) | Stay Humble. Let Your Growth Show. |

- **Model:** Qwen-Image-2512 dan GLM-Image DILANGKAU (tidak muat RAM 15 GB, sama seperti larian pertama).
- **Lulus G1–G2 (ejaan, tiada teks rawak), QC `qc/v12b_cpu.json`, semakan mata, bukti lemah:**

| Model | K9B | K10V | K11N | K12Y |
|---|---|---|---|---|
| MOSS | 3/3 | 3/3 | 3/3 | 3/3 |
| ERNIE (jana semula selepas pepijat dibaiki) | 3/3 | 1/3 bersih (2 panel putih) | 2/3 tanpa kotak betul (s42, s2024 kotak tambahan pada 'STEADY.'; s7 tanda petikan; s123 tiada kotak); 4 seed habis → tukar model | 3/3 |
| FLUX 3 Klein | 3/3 | 3/3 | 3/3 | 3/3 |
| Z-Image | 1/3 (koma tambahan) | 3/3 | 2/3 | 2/3 |
| klein 4B | 0/3 ('Daly') | 3/3 | 1/3 | 0/3 ('HUMBLE' tanpa noktah) |

- **Dua pepijat dibaiki semasa larian:** (1) `kad.hitam_putih` menukar latar cerah (krim / putih) kepada putih, jadi rangka am hp menulis huruf putih atas putih (ERNIE K9B berongga selepas SK04); kini kad latar cerah = latar hitam, dakwat putih, kotak putih dengan huruf hitam (`terang`, `kotak_hp`). (2) `semak_pe` menolak PE ERNIE apabila petikan hanya hilang tanda baca hujung ('SHAKY' bagi 'SHAKY.'), lalu rangka am berpepijat dipakai; kini diterima. K9B tetap ditolak dengan betul (PE memetik huruf 'B').
- **Belajar (3.15):** Z-Image `had_positif` pada K9B KALAH (1/3 → 1/3), dibuang. klein 4B: `huruf_besar` dan `tukar_peranan` tidak berkenaan (K9 skrip bersambung; 'HUMBLE.' sudah huruf besar; tukar peranan mengubah design), jadi pilihan habis → tukar model: FLUX 3 Klein dan MOSS lulus 3/3 pada K9B dan K12Y. ERNIE `had_positif` (tanda petikan tambahan, K3K + K11N) diuji pada K11N: KALAH ikut G1–G2 (2/3 → 2/3; tanda petikan 'BEGIN' kekal pada s7), dibuang. Catatan bukti lemah: kotak di tempat betul ('SHAKY.' sahaja) 3/3, sebelum 0/3; PE berubah setiap kali, jadi sebab belum pasti. Cacat akibat pepijat kod yang sudah dibaiki kini tidak dikira oleh `belajar.py` ("pepijat kod" dalam nota QC).
- **Simpanan (28 Nov 2026, keputusan pengguna A):** 12 imej uji ERNIE (U26) dan 46 imej model lain yang belum ada di dashboard (U25: larian v1.2 pertama selain FLUX 3 Klein, kitaran QC p1, K3W). Kad K8: tiada gambar upload lebih besar (pengguna), jadi had tekstur K8 kekal.
- **Selepas larian (28 Nov 2026, keputusan pengguna):** kad K9–K12 diluluskan (v1.0); kad K10 tambah ciri QC wajib "Tiada panel atau kotak putih di sekeliling blok"; 76 imej disimpan di AI Image Test (ujian U16). Uji ulang ERNIE kotak: kalah. Uji ERNIE frasa bentuk (K7M, K8G): menang, ERNIE r1 → r2. SK01: 5b v1.2.
- **Kemasan (SK06, hitam putih):** FLUX 3 Klein seed 42 bagi setiap design: K9B S3, K10V S5 (lusuh), K11N S3, K12Y S3 (`final/v12b-cpu/`, helaian `qc/v12b_cpu_akhir.jpg`).
- **Model × kad selepas larian ini (bukti lemah):** K9 = MOSS, ERNIE, FLUX 3 Klein; K10 = semua lima (ERNIE 1/3); K11 = MOSS, FLUX 3 Klein, Z-Image (2/3); K12 = MOSS, ERNIE, FLUX 3 Klein, Z-Image (2/3).
## Larian K14–K18 (asal K9–K13) (27 Nov 2026, CPU, hitam putih sahaja, arahan pengguna)
Lima gambar upload baharu, lima kad baharu (K14–K18, `kad.py`, v1.0, diluluskan pengguna 28 Nov 2026; asalnya bernombor K9–K13, ditukar 28 Nov kerana sesi lain `exciting-sagan-qk5lce` memakai K9–K13; ayat R, S ditukar ke X, Z atas sebab sama), ayat baharu pilihan Claude. Semua model yang muat di CPU (15 GB RAM): MOSS, ERNIE, FLUX 3 Klein, Z-Image, klein 4B. Qwen-Image-2512 dan GLM-Image dilangkau (tidak muat RAM). Seed 42, 7, 123 (K14–K16) dan 42, 7 (K17–K18). Kemasan warna (langkah 6) tidak dibuat: arahan pengguna hitam putih sahaja. QC: semakan mata Claude, `qc/v12_cpu_k14.json`, helaian `qc/v12k14_<model>_<ID>.jpg` (bukti lemah).

| ID | Gambar | Kad | Ayat | Ciri utama |
|---|---|---|---|---|
| K14X | IMG_5838 | K14 | Rest Well and Dream Big | caps inline + skrip, reben bertakuk, sinar atas |
| K15E | IMG_5817 | K15 | Learn Explore Create Share Be Curious Be Kind | sans tebal bertindan, sama lebar |
| K16C | IMG_5819 | K16 | Some Days Need Extra Coffee | huruf tangan pelik tebal, kapur, bintik latar |
| K17Z | IMG_5745 | K17 | Small Wins Still Count | huruf gelembung kartun, titik + percikan |
| K18U | IMG_5743 | K18 | Sundays Feel Good! | cop getah lusuh, bingkai, anak panah |

Lulus G1–G2 (imej lulus / dijana):

| Model | K14X | K15E | K16C | K17Z | K18U | Jumlah | Masa jana CPU |
|---|---|---|---|---|---|---|---|
| MOSS | 3/3 | 3/3 | 3/3 | 2/2 | 2/2 | 13/13 | 4465 s |
| ERNIE | 2/3 | 3/3 | 3/3 | 1/2 | 2/2 | 11/13 | 6728 s |
| FLUX 3 Klein | 3/3 | 3/3 | 3/3 | 2/2 | 2/2 | 13/13 | 5295 s |
| Z-Image | 3/3 | 3/3 | 0/3 | 1/2 | 2/2 | 9/13 | 4192 s |
| klein 4B | 2/3 | 3/3 | 3/3 | 1/2 | 1/2 | 10/13 | 2605 s |

- **Paling hampir rujukan (semakan mata):** K14 = ERNIE s42, klein 4B s42; K15 = FLUX 3 Klein; K16 = ERNIE (berus kasar + bintik); K17 = ERNIE s7, FLUX 3 Klein; K18 = ERNIE (bingkai penuh, cop, anak panah).
- **Cacat utama:** Z-Image × K16 (NEED hilang / terlalu kecil, 3/3); huruf kecil i dalam STILL / WINS (Z-Image, klein 4B); MOSS × K16 terlalu kemas, MOSS × K18 bingkai atas / bawah sahaja; FLUX 3 Klein × K16, K18 blok kecil.
- **5b:** 56 imej lulus dibetulkan (`betul/v12-cpu-k14/`), 56/56 lulus semakan akhir selepas SK 5b v1.2 (lihat Catatan pembaikan SK). Ejaan tidak berubah.
- **Belajar (3.15, `belajar.py` b1.2):** nota QC kini ditulis dengan kata kelas cacat; kelas `bentuk` dan `hiasan_tempat` diluaskan (bentuk huruf, lebar baris, bingkai hanya, reben kecil); rekod SNC tanpa folder model (kemasan SK07 / SK08) dilangkau. TINDAKAN CUBA ditulis dalam `pembina.py` (`UJI`), dipakai pada jana seterusnya model itu: `zturbo_had_positif`, `ernie_hiasan_tepat`, `klein3_hiasan_kedudukan`, `klein4b_frasa_bentuk`. MOSS: HABIS bagi ejaan K8 (sedia ada).
- **Uji calon (28 Nov 2026, `run_uji_k14.sh`, `raw/v12-cpu-k14-uji/`, QC `qc/v12_cpu_k14_uji.json`, 17 imej, seed sama):** MENANG `zturbo_had_positif` 1/5 → 2/5, `ernie_hiasan_tepat` 2/3 → 3/3, `klein3_hiasan_kedudukan` 3/3 → 3/3 (bersih 0 → 3); KALAH `klein4b_frasa_bentuk` 6/6 → 6/6 (bersih 1 → 1). Tiga yang menang ditulis ke aturan (rev r2). 5b: 14 imej lulus QC, 14/14 lulus (`betul/v12-cpu-k14-uji/`). `belajar.py` b1.3: lulus sama → imej tanpa kelas cacat lebih banyak menang. Z-Image ejaan K16 masih HABIS pilihan ubahan: tukar model (ERNIE / FLUX 3 Klein lulus 3/3).
- **Dashboard (28 Nov 2026, pilihan pengguna A):** 65 imej disimpan di tab AI Image Test sebagai ujian **U15** (`data/ai_tests/rows/U15.json`, kad K14–K18). U13 / U14 milik sesi lain (cawangan `exciting-sagan-qk5lce`) dipulihkan ke dalam build ini selepas hampir tertimpa. Sesi itu juga mencipta kad K9–K13 daripada gambar upload yang sama (definisi lain); jadi kad sesi ini ditukar ke K14–K18 (keputusan pengguna 28 Nov 2026).
- **Belajar SK:** SK02 BAIKI (5b v1.2, MENANG). PARAMETER tertangguh: jenis tekstur K14–K18 (SK06) dan peta warna K15 (SK07) milik langkah 6, tidak dijalankan kerana hitam putih sahaja.
## Larian v1.2 kedua (27 Nov 2026, arahan pengguna)
- **Tugas:** lima gambar upload, ayat baharu dipilih Claude, kad gaya baharu, semua model yang muat di CPU, hitam putih sahaja, QC dan gaya.
- **Design dan kad (K9–K13 dibuat Claude, diluluskan pengguna 27 Nov 2026; jalur kuning K13 tidak dijana, keputusan pengguna):**

| Id | Gambar upload | Kad | Ayat | Laluan |
|---|---|---|---|---|
| K40Q | IMG_5776 | K9 | Quiet Effort Builds Loud Results | 2 (seed 42, 7, 123) |
| K41g | IMG_5777 | K10 | Fewer Excuses Bigger Moves | 1 (seed 42, 7; 123 untuk kitaran QC) |
| K42h | IMG_5761 | K11 | The Real Power Is Steady Progress | 2 |
| K43i | IMG_5762 | K12 | Hold Loosely Love Deeply | 1 |
| K44j | IMG_5755 | K13 | Make the Move or Miss Your Moment | 2 |

- **Model:** MOSS, ERNIE Turbo, FLUX 3 Image Klein, Z-Image Turbo, klein 4B di CPU, 768 × 1024. Qwen-Image-2512 dan GLM-Image dilangkau (tidak muat RAM 15 GB, seperti larian pertama). Purata masa setiap imej (`raw/v12e-cpu/*/log.jsonl`): MOSS 328 s, ERNIE 394 s, FLUX 3 Klein 401 s, Z-Image 306 s, klein 4B 95 s.
- **QC pintu G1–G3 (mata Claude, bukti lemah; `qc/v12e_cpu.json`, helaian `qc/v12e_cpu_<id>.jpg`):**

| Model | K40Q | K41g | K42h | K43i | K44j | Jumlah |
|---|---|---|---|---|---|---|
| MOSS | 3/3 | 2/2 | 3/3 | 2/2 | 2/3 | 12/13 |
| ERNIE Turbo | 3/3 | 2/2 | 3/3 | 2/2 | 3/3 | 13/13 |
| FLUX 3 Image Klein | 3/3 | 2/2 | 3/3 | 2/2 | 2/3 | 12/13 |
| Z-Image Turbo | 3/3 | 0/3 | 3/3 | 0/3 | 2/3 | 8/15 |
| klein 4B | 1/3 | 0/3 | 3/3 | 0/3 → 2/3 (r2) | 2/3 | 6/15 → 8/15 |

- **Kitaran QC (pusingan 1, `raw/v12e-cpu-p1`, helaian `qc/v12e_cpu_p1_<id>.jpg`):** empat model × design tanpa imej lulus; seed 123 dijana dahulu (laluan 1), cacat sama 3/3 = sistematik. Z-Image K41g (FEWER salah eja) tukar peranan 0/3 → 0/3; Z-Image K43i (titik selepas perkataan) had positif 0/3 → 0/3; klein 4B K41g tukar peranan 0/3 → 0/3; klein 4B K43i tukar peranan 0/3 → 2/3 (aturan 3.4 r2). Pilihan ubahan habis bagi Z-Image (K41g, K43i) dan klein 4B K41g; design itu sudah ada imej lulus daripada MOSS, ERNIE dan FLUX 3 Klein, jadi tiada tukar model.
- **Ciri kad yang lemah (lulus pintu, dicatat untuk 3.15):** K41g tidak condong pada sesetengah imej (SK01 betulkan ke 5.8°); K42h Z-Image tegak, bukan italik; K43i baris tidak bertaut (semua model); K44j tanda petik hilang (Z-Image) atau anak panah lebih (ERNIE).
- **K43i dan ciri teras (keputusan pengguna 28 Nov 2026):** "huruf antara baris bersentuh / bertaut" dan "huruf tangan gemuk" memang ciri teras (wajib) kad K12. Semua 8 kemasan K43i (MOSS, ERNIE, FLUX 3 Klein, klein 4B) gagal ciri bertaut, jadi K43i belum lulus langkah 5 penuh; kiraan "lulus" di atas ialah pintu G1–G3 sahaja (seperti larian pertama). Ujian ERNIE `ernie_frasa_bentuk` (K43i + K7M, seed 42, 7, 123) dijana dengan izin pengguna. Ujian itu KALAH (ciri bertaut masih gagal). **Keputusan pengguna 28 Nov 2026: ciri "bertaut" dilonggarkan jadi ciri biasa (bukan teras); kad K12 v1.1.** Dengan itu 8 kemasan K43i lulus ciri teras (huruf gemuk melantun, kilat dalam huruf).
- **5b:** semua imej lulus pintu. GAGAL: MOSS K44j s42 (SK04 padam tanda petik kelabu); ERNIE dan FLUX 3 Klein K43i s7 (SK02: satu skala tidak padan ruang tepi dua paksi). Ketiga-tiganya dicatat `silap` dalam `belajar/sk_semakan.jsonl`.
- **Belajar SK (batch ini):** SK07 v1.2 → v1.3 (HP), 5b v1.1 → v1.2 (SK05 penapis bintik relatif; BAIKI ruang tepi), SK06 v1.3 → v1.4 (kata tekstur); `peta_warna` K9 ditambah (varian berwarna sahaja). Tertangguh: ukuran K11 (SK05 gagal pada latar batu bertekstur IMG_5761, ambang 60–160), jenis tekstur 'retak kasar' K11, SK04 memadam tanda petik kelabu (1 imej, belum berulang). QC akhir 53 kemasan: semua hitam putih, ejaan betul; moss K44j s42 hilang tanda petik (ciri teras K13 gagal).
- **Langkah 6 (hitam putih sahaja):** `kemasan.py <kad> <ayat> S3 final/v12e-cpu <imej…> --warna HP` (SK07 v1.3): latar kad + satu dakwat neutral (K9–K11 putih atas hitam; K12, K13 hitam atas putih, ikut gambar upload).
## Larian v1.2 kedua: K50–K54 (27 Nov 2026, arahan pengguna)
- **Tugas:** lima gambar upload, ayat baharu pilihan Claude, semua model di CPU, hitam putih sahaja, ikut standard; QC dan Kad Gaya.
- **Design dan kad** (kad K50–K54 dibuat Claude daripada gambar, v1.0, **diluluskan pengguna 28 Nov 2026**; rujukan diukur SK05; saringan tanda dagang carian web sahaja, `qc/v12_k50k54.json`):

| Id | Gambar upload | Kad | Ayat (Claude) | Laluan | Rujukan diukur SK05 |
|---|---|---|---|---|---|
| K50k | IMG_5840 | K9 skrip berus + garis swash | Hold your ground | 1 | condong 1.9°, tepi 11.0 / 13.2% |
| K51m | IMG_5793 (dipotong ke poster karang) | K10 huruf condensed rata, satu perkataan gergasi, calar | Do The Work Quietly | 1 | tepi 8.0 / 5.7% |
| K52A | IMG_5789 (bingkai putih dibuang) | K11 condensed condong, baris tengah kecil, jalur hazard, bar ucapan | Doubt Loses To Action | 1 | condong 4.5°, tepi 7.7 / 3.0% |
| K53n | IMG_5786 | K12 poster vintaj bertingkat, banner, garis, bintang | Effort Today Freedom Tomorrow | 1 | tepi 4.6 / 1.6% |
| K54p | IMG_5791 | K13 blok rata penuh tinggi, butir semburan | Steady Hands Build Strong Lives | 2 | tepi 11.7 / 2.0% |

- **Hitam putih:** semua kad satu dakwat putih atas hitam; warna asal disimpan dalam `warna_asal` kad. K12 dan K13: warna kad ditukar ke neutral (#f4f4f2 / #0b0b0b; sebelum ini krim dan hitam keperangan) supaya benar-benar hitam putih.
- **Model:** MOSS, ERNIE Turbo, FLUX 3 Image Klein, Z-Image Turbo, klein 4B di CPU; tiada yang dilangkau. Qwen-Image-2512 dan GLM-Image tidak dijalankan (tidak muat RAM 15 GB, sama seperti larian pertama).
- **Hasil pusingan 0** (55 imej; semakan mata Claude, bukti lemah; lulus = G1 ejaan + G2 tiada teks / tanda rawak + G3 tiada cacat). Rekod: `qc/v12_k50k54.json`; helaian `qc/v12_k50k54_<ID>.jpg`.

| Model | K50k | K51m | K52A | K53n | K54p | Jumlah | Masa CPU |
|---|---|---|---|---|---|---|---|
| MOSS + LoRA | 2/2 | 2/2 | 2/2 | 2/2 | 3/3 | 11/11 | 81 minit |
| ERNIE Turbo | 2/2 | 2/2 | 0/2 | 2/2 | 2/3 | 8/11 | 125 minit |
| FLUX 3 Image Klein | 2/2 | 0/2 | 2/2 | 2/2 | 0/3 | 6/11 | 110 minit |
| Z-Image Turbo | 2/2 | 2/2 | 1/2 | 2/2 | 3/3 | 10/11 | 77 minit |
| klein 4B | 2/2 | 2/2 | 2/2 | 1/2 | 2/3 | 9/11 | 31 minit |
| Jumlah | 10/10 | 8/10 | 7/10 | 9/10 | 10/15 | 44/55 | |

- **Gagal:** ERNIE K52A s42, s7 dan K54p s7 (bingkai putih separa; 5b membaca latar sebagai putih); Z-Image K52A s42 (serpihan jalur seperti tanda petikan); klein 4B K53n s42 (garis tegak separa di tepi), K54p s42 ('BUIILD'); FLUX 3 Klein K51m 2/2 dan K54p 3/3: ciri teras gagal, huruf lebar bukan condensed (syarat QC, keputusan pengguna 28 Nov 2026; sebelum itu nota gaya, jadi angka awal 49/55).
- **Nota gaya pada imej lulus** (bukan pintu): ERNIE K51m 'WORK' tidak cukup besar; MOSS K54p lebar baris tidak sama; Z-Image dan FLUX 3 Klein K53n bintang menyentuh huruf O; jalur hazard menyentuh 'ACTION' (Z-Image, klein 4B); klein 4B K53n s7 bingkai garis nipis.
- **Kitaran QC pusingan 1** (ERNIE × K52A tanpa imej lulus; cacat sama 2/2 seed = sistematik): calon 3.15 `ernie_hiasan_tepat` ("These are the only decorations, on a clean empty background."), K52A + K54p, seed 42, 7, 123 (`raw/v12-cpu-k50k54-p1`, 63 minit). Bingkai hilang 6/6; K52A 3/3 lulus (kitaran tamat, imej dipakai); K54p s123 tanda petikan tambahan. `belajar.py`: KALAH (2/5 → 4/5 tetapi kelas cacat baharu 'rawak'); dibuang.
- **Kitaran QC pusingan 1, FLUX 3 Klein × K51m / K54p** (28 Nov 2026): calon `klein3_frasa_bentuk` ("Every letter is a tall, narrow condensed letterform, much taller than it is wide."), seed 42, 7, 123 (56 minit): huruf masih lebar 6/6. KALAH, dibuang; pilihan bentuk habis → FLUX 3 Klein tidak dipakai untuk K10 / K13. 6 imej ini disimpan di U23 (keputusan pengguna 28 Nov 2026: A), jadi U23 = 67 imej.
- **5b:** 50 imej lulus (45 + 5 pusingan 1; 5 imej FLUX 3 Klein K51m / K54p kemudian dibuang kerana syarat condensed) dibetulkan, 0 gagal semakan akhir (`betul/v12-cpu-k50k54*/`).
- **Kemasan langkah 6 (hitam putih, SK07 satu dakwat → SK06 `--kad`):** 49 imej (54 − 5 FLUX 3 Klein) (`final/v12-cpu-k50k54/`, `final/v12-cpu-k50k54-p1/`; SVG induk + pratonton 18×24; PNG 300 DPI dijana semula bila perlu, tidak disimpan dalam git). Tekstur: K9 tiada, K10 calar, K11 lusuh, K12 lusuh halus, K13 semburan. Helaian `qc/v12_k50k54_akhir.jpg`.
- **Belajar SK:** SK06 v1.4 `tekstur_calar_semburan` MENANG (19/19, jurang tekstur K10 / K13 tertutup). SK01–SK04, SK07, SK08: tiada cacat.
- **Satu sesi sahaja (keputusan pengguna 28 Nov 2026):** sesi ini (cawangan `claude/focused-faraday-f7q7vc`) berhenti menulis dashboard selepas simpanan U23; kerja K50–K54 diteruskan dalam satu sesi.
- **Simpanan (keputusan pengguna 28 Nov 2026: A):** 61 imej (55 + 6 pusingan 1 ERNIE) di AI Image Test sebagai **U23** (`data/ai_tests/rows/U23.json`, `ai_rows_k50k54.py`; peta blob `qc/v12_k50k54_blobs.txt`; `img_siap` = pratonton kemasan). Nombor U13 diambil oleh sesi Claude lain yang menjalankan K50–K54 dengan ayat berbeza; `ai_all` digabung di atas versi dashboard terkini (955 baris), bukan dijana semula, supaya U13–U22 sesi itu kekal. `aturan_belajar` dan `sk_belajar` di dashboard kini milik sesi itu; tidak ditimpa (fail cawangan ini dalam `data/export/ai_tests/`).
- **Belajar 3.15** (`belajar.py` b1.2: kelas bentuk juga "bentuk huruf lebar"): ERNIE `hiasan_tepat` KALAH → pilihan habis bagi 'hiasan yang tidak diminta' (tukar model); Z-Image `had_positif` tidak berkenaan (aturan r1 sudah positif) → pilihan habis bagi 'teks rawak'; klein 4B calon `klein4b_hiasan_tepat` ditulis (dipakai pada jana klein 4B seterusnya); FLUX 3 Klein `frasa_bentuk` KALAH → pilihan habis bagi bentuk (tukar model).
- **Model × kad selepas larian ini** (bukti lemah, satu ayat setiap kad): K9, K10 = MOSS, ERNIE, Z-Image, klein 4B (FLUX 3 Klein tidak: huruf lebar); K11 = MOSS, FLUX 3 Klein, klein 4B (2/2), Z-Image (1/2), ERNIE hanya dengan baris hiasan tepat; K12 = MOSS, ERNIE, FLUX 3 Klein, Z-Image (2/2), klein 4B (1/2); K13 = MOSS, Z-Image (3/3), ERNIE, klein 4B (2/3); FLUX 3 Klein tidak (huruf lebar). Paling hampir gaya rujukan (mata Claude): K9 ERNIE, K10 Z-Image / klein 4B, K11 MOSS / FLUX 3 Klein, K12 ERNIE / klein 4B, K13 Z-Image / ERNIE.

## Catatan pembaikan aturan model
Setiap ubahan aturan (3.4–3.10) direkod di sini, dan juga dalam `designs/lettering-v1/belajar/ubahan.json` (dibaca oleh `belajar.py`, 3.15). Ujian pertama (26 Nov 2026, K3 × ayat H, seed 42, 7, 123, semakan mata, bukti lemah) mengubah beberapa perkara serentak, kerana dibuat sebelum peraturan "satu ubahan setiap pusingan".

| Tarikh | Model | Rev | Cacat dengan rangka am | Ubahan | Ejaan betul sebelum → selepas |
|---|---|---|---|---|---|
| 28 Nov 2026 | Z-Image Turbo | r2 → r1 | Titik / tanda rawak | `had_positif` dinilai semula atas rekod gabungan nifty-lovelace (K7M, K8G) + sleepy-edison (K9B): 1/10 → 3/10 tetapi kelas cacat baharu (hiasan tambahan) → KALAH, teks dipulangkan ke r1 | 1/10 → 3/10 |
| 28 Nov 2026 | Z-Image Turbo | r1 → r2 | Titik / tanda rawak | Selepas gabung lucid-galileo: `had_positif` ada tiga ayat berlainan dengan nama sama. Dinilai ikut ayat: versi lucid-galileo menang (K16C, K17Z 1/5 → 2/5, tiada kelas baharu) dan kini aturan 3.5 r2; versi nifty-lovelace juga tiada kelas baharu (K7M, K8G 0 → 2); versi sleepy-edison kalah (K9B). Pengajaran: nama calon mesti unik bagi setiap ayat | 2/15 → 5/15 (gabungan) |
| 27 Nov 2026 | Z-Image Turbo | r1 → r2 | Titik / tanda rawak (K7M, K8G) | `had_positif` MENANG: ayat had akhir kini "Every letter in the image belongs to these N words, and each word appears once; the rest of the canvas is plain empty background" (ganti "The only text in the image is…") | G1+G2 0/4 → 2/4 (K7M 2/2 bersih; K8G masih 5 baris + bintik). Had: prompt K3L kini 254 perkataan (> 250), K3L tidak boleh dijana dengan Z-Image |
| 27 Nov 2026 | klein 4B | r1 → r2 | Percikan di dalam label (K3K) | `hiasan_kedudukan`: hiasan sisi ditulis "placed outside the label, one group on its left and one group on its right". Mula-mula KALAH (lulus seri 3/3, tiada ♥); 28 Nov dinilai semula dengan belajar.py b1.2 (seri dipecah oleh cacat sasaran, keputusan pengguna): MENANG | 3/3 → 3/3; percikan di dalam label 3 → 0 |
| 27 Nov 2026 | ERNIE Turbo | r1 | Tanda petikan rawak (K22c, K3K) | `had_positif` KALAH: tanda petikan hilang 2/2, tetapi K3K s7 dapat 'AFTER' berulang + hiasan tambahan | 0/2 → 1/2 (kelas baharu) |
| 28 Nov 2026 | klein 4B | r2 → r3 | Baris berbilang perkataan dipisah (K4q 'QUIET WORK', K8G 'KEEP GOING') | `dua_kata_sebaris` MENANG: setiap baris berbilang perkataan mendapat ", as N words side by side on one line" | G1+G2 2/6 → 3/6; cacat baris 3 → 2; K4q s123 dapat salah eja baru ('WOK'). Pembanding r1 sah kerana prompt sama tepat (belajar b1.2) |
| 26 Nov 2026 | klein 4B | r1 | Label tambahan di bawah; "WHAT" tiada kotak (3/3) | Prosa mengalir; gaya di dalam ayat baris; had satu ayat | 0/3 → 3/3 |
| 26 Nov 2026 | Z-Image Turbo | r1 | Bintang dan garis lengkung yang tidak diminta | Huraian panjang, baris bernombor, had positif | 3/3 → 3/3 |
| 26 Nov 2026 | ERNIE Turbo | r1 | "WHAT WHAT" (3/3) | Prompt mentah pendek + PE rasmi | 0/3 → 2/3 |
| 26 Nov 2026 | MOSS + LoRA | r1 | Garis lengkung tambahan atas dan bawah | Susun atur JSON dengan kotak setiap baris | 3/3 → 3/3 |
| 26 Nov 2026 | MOSS + LoRA | r1 (tiada perubahan) | K8 × ayat G: 'ALMOST' jadi 'ALMIST' (3/3) | Tukar peranan perkataan (kitaran QC pusingan 1). TIDAK berjaya, dibuang | 0/3 → 0/3 |
| 26 Nov 2026 | Z-Image Turbo | r1 (tiada perubahan) | K8 × ayat G: baris dua perkataan dipisah jadi dua baris (3/3) | Tambah "as two words side by side on one line". TIDAK berjaya, dibuang | 0/3 → 0/3 |
| 26 Nov 2026 | FLUX 3 Image Klein | r0 (ujian pertama) | Tiada pembanding rangka am | Aturan 3.8 seperti ditulis; CPU | 9/9 pada K3, K7, K8 |
| 27 Nov 2026 | FLUX 3 Image Klein | r0 → r1 (ujian kelayakan, `belajar.py`) | K8 × ayat G: 'KEEP GOING' tanpa jarak antara perkataan (3/3) | Tiada ubahan teks; rangka am lawan aturan 3.8 pada kad, ayat dan seed yang sama | rangka am 6/9 → aturan 9/9 |
| 27 Nov 2026 | klein 4B | calon (CUBA, belum dijana; diluluskan pengguna 28 Nov 2026 untuk larian seterusnya) | BRILLIANT hilang huruf I, anak panah rosak (klein 4B) | `klein4b_hiasan_kedudukan`; `klein4b_cara_baris` (kata ≥ 7 huruf: "a word spelled out in full with all N of its letters"). Semak 3.11 lulus K3K, K7M, K8G, K30R, K31T, K32S | – (dijana pada larian seterusnya, seed sama) |
| 27 Nov 2026 | Z-Image Turbo | r1 (tiada perubahan) | K9 × ayat B: koma tambahan selepas 'Build' / 'Daily' (2/3) | Ayat had: "written exactly as quoted, character for character, with nothing added after any word". TIDAK berjaya, dibuang | 1/3 → 1/3 |
| 27 Nov 2026 | ERNIE Turbo | r1 (tiada perubahan) | K11 × ayat N: tanda petikan pada 'BEGIN' (s7); kotak di tempat salah | Ayat had positif: "The only text in the image is these N words, each drawn once exactly as written between the quotes, without the quote marks". TIDAK berjaya (G1–G2), dibuang; kotak betul 3/3 (sebelum 0/3) | 2/3 → 2/3 |
| 28 Nov 2026 | ERNIE Turbo | r1 (tiada perubahan) | K11 × ayat N: kotak di tempat salah (ujian pembaikan kotak, arahan pengguna) | Ayat had positif yang sama, diuji pada K11N + K12Y. TIDAK berjaya: kotak K11N 0/3 → 3/3 tetapi K12Y 3/3 → 0/3 (kotak 'GROWTH' jadi garis luar). Dibuang | 5/6 → 5/6 |
| 28 Nov 2026 | ERNIE Turbo | r1 → r2 | K7 × ayat M, K8 × ayat G: huruf berus nipis / kering (6/6, imej lulus) | Blok I: "Every letter is drawn with a thick, heavy, fully filled stroke, never thin, scratchy or dry-brushed." MENANG: huruf tebal penuh 6/6; K8G latar bersih | lulus 6/6 → 6/6, bersih 0 → 6 |

## Gabung sesi (28 Nov 2026, keputusan pengguna: satu sesi gabung)
- Cawangan hab: `claude/nifty-lovelace-i32bdx`. Cawangan `sleepy-edison` digabung dengan git (kod + kad K9–K12 + ayat B V N Y; kad sesi ini K20–K23 + ayat a b c e f q; tiada kunci bertembung). `belajar.py` b1.3 = b1.1 sleepy-edison (pemecah seri bersih, rekod cawangan) + b1.2 sesi ini (cacat sasaran, pembanding prompt sama).
- Cawangan lain (exciting-sagan, focused-allen, focused-faraday, lucid-galileo dan 5 lagi) digabung pada aras rekod sahaja (`gabung_cawangan.py`, `cawangan/<sesi>/`), kerana ID kad K9–K13 dan huruf ayat mereka bertembung. Kod mereka (pembina, SK) belum digabung.
- Jadual dashboard `aturan_belajar` dan `sk_belajar` kini daripada rekod semua sesi (muat naik 28 Nov 2026, 08:55 UTC).

## Larian v1.2: enam gambar upload, ayat baharu (27 Nov 2026, arahan pengguna)
- **28 Nov 2026:** kad K9–K12 sesi ini ditukar nama ke K20–K23, dan ayat A, B, C, E, F, Q ke huruf kecil a, b, c, e, f, q, kerana empat sesi lain memakai K9–K13 dan huruf ayat yang sama untuk gambar lain. Ujian AI Image Test sesi ini: U20 (dahulu U13).
- Kad baharu v1.0 (diluluskan pengguna 27 Nov 2026, langkah 1d): K20 (IMG_5845, skrip melantun + sans bulat + hati), K21 (IMG_5846, lencana bulat), K22 (IMG_5840, skrip berus bertangga), K23 (IMG_5793, blok sans sempit calar, hitam atas koral). IMG_5792 = K2 dan IMG_5764 = K4 (kad sedia ada, 1b). Ukuran rujukan SK05 dalam `kad.BLOK[...]["rujukan"]`. Gambar upload: `designs/lettering-v1/rujukan/`.
- Ayat (Claude pilih): a "Strong Moms Raise Brave Kids" (K20), b "Every Single Day Spreading Kindness Teacher Life" (K21), c "Trust Your Timing" (K22), e "Comfort Zones Kill Dreams" (K2), f "Build Your Habits Not Your Excuses" (K23), q "Quiet Work Builds Loud Results" (K4).
- Jana: `run_v12.sh`, CPU container 4 teras, 5 enjin, seed 42 sahaja (bukan 2–4 seed; ujian pantas), pembina v1.2-p1, tiada enjin dilangkau. Imej: `raw/v12-cpu-ref6/`; QC: `qc/v12_cpu_ref6.json`, helaian `qc/v12_cpu_ref6_grid.jpg`.
- G1 + G2 lulus (semakan mata Claude, bukti lemah): MOSS 6/6, FLUX 3 Klein 6/6, ERNIE 5/6 (K22c tanda petikan), Z-Image 5/6 (K4q baris dipisah), klein 4B 5/6 (K21b ejaan). Jumlah 27/30. Masa jana: MOSS ~6 min, ERNIE ~7 min, FLUX 3 Klein ~7 min, Z-Image ~6 min, klein 4B ~2 min setiap imej.
- **Seed 7 dan 123 (27 Nov 2026, izin pengguna):** G1 + G2 lulus: MOSS 12/12, FLUX 3 Klein 12/12, ERNIE 10/12 (K22c tanda petikan 2/2), Z-Image 10/12 (K4q 'LOOD' 2/2), klein 4B 8/12 (K20a s123 'Kids' berulang, K21b s123 'TEACHIER', K4q baris dipisah 2/2). Jumlah 3 seed: 79/90. K23 'HABITS' tidak gergasi pada semua model (ciri teras kad belum tercapai). Kemasan 36 imej MOSS + FLUX 3 Klein: `final/v12-cpu-ref6/`, helaian `qc/v12_cpu_ref6_kemasan.jpg`.
- Disimpan sebagai A (pilihan pengguna): AI Image Test ujian U13 (`data/ai_tests/rows/U13.json`), 30 baris.
- Belajar 3.15: calon CUBA ditulis dalam `pembina.py` (`klein4b_hiasan_kedudukan`, `zturbo_had_positif`, `ernie_had_positif`); belum diuji (perlu izin jana).
| 28 Nov 2026 | Z-Image Turbo | r1 → r2 (`had_positif`, MENANG) | K16C: NEED hilang / rosak (3/3); K17Z s7: huruf kecil i | Had positif "exactly these N words … spelled exactly as quoted … every other area is plain empty black" | 1/5 → 2/5 (K16C 0/3 → 1/3; K17Z 1/2 → 1/2). Masih rosak: NEEZ, EED. Bukti lemah |
| 28 Nov 2026 | ERNIE Turbo | r1 → r2 (`hiasan_tepat`, MENANG) | K14X s7: jalur putih tepi kanan / bawah | Tambah "Clean empty background …, no other shapes, lines or borders than those described." | 2/3 → 3/3. Bukti lemah |
| 28 Nov 2026 | FLUX 3 Image Klein | r1 → r2 (`hiasan_kedudukan`, MENANG ikut seri b1.3) | K14X: reben kecil sahaja pada AND / BIG (3/3) | Bekas "spanning the full width of the block" (kecuali bekas `small`) | 3/3 → 3/3; bersih 0/3 → 3/3. Bukti lemah |
| 28 Nov 2026 | klein 4B | r1 (tiada perubahan) | K15E: lebar baris tidak sama; K16C: huruf kurang kasar | `frasa_bentuk`: "Every line uses the same … letterforms, and each line is stretched to exactly the same width". TIDAK berjaya, dibuang | 6/6 → 6/6; bersih 1 → 1 |
| 27 Nov 2026 | Z-Image Turbo | r1 (tiada perubahan) | K41g: 'FEWER' jadi 'FERER' / 'FENER' / 'FEHER' (3/3) | Tukar peranan (FEWER utama → sokongan). TIDAK berjaya, dibuang | 0/3 → 0/3 |
| 27 Nov 2026 | Z-Image Turbo | r1 (tiada perubahan) | K43i: titik selepas setiap perkataan (3/3) | Had positif: "Each word ends cleanly with its last letter, followed only by empty black space." TIDAK berjaya, dibuang | 0/3 → 0/3 |
| 27 Nov 2026 | FLUX.2 klein 4B | r1 → r2 | K43i: 'LOOSELY' jadi 'LOSELY' (3/3); K41g: 'FEWER' jadi 'FEVER' (3/3) | Tukar peranan perkataan itu (`belajar.py`: MENANG 0/6 → 2/6). Ditulis bagi K43i sahaja | K43i 0/3 → 2/3; K41g 0/3 → 0/3 |
| 28 Nov 2026 | ERNIE Turbo | r1 (tiada perubahan) | Bentuk huruf lain daripada kad (K7M, K8G; K43i tidak gemuk / bertaut) | `frasa_bentuk`: bentuk huruf setiap peranan disebut semula sekali (izin jana pengguna). TIDAK berjaya, dibuang: K43i tetap tidak bertaut + garis lengkung tambahan 2/3; K7M swash hilang 3/3 | ejaan 5/5 → 5/5 (+1 seed baharu) |
| 27 Nov 2026 | ERNIE Turbo | r1 (tiada perubahan) | K11 / K13: bingkai putih separa di tepi (3 imej) | Calon `hiasan_tepat`: "These are the only decorations, on a clean empty background." KALAH (bingkai hilang 6/6, tetapi tanda petikan baharu K54p s123), dibuang | 2/5 → 4/5 |
| 27 Nov 2026 | Z-Image Turbo | r1 (tiada perubahan) | Teks / tanda rawak (5 imej, K7, K8, K11) | Calon `had_positif`: tidak berkenaan (aturan 3.5 r1 sudah positif, tiada perkataan berisiko); tidak dijana | - |
| 28 Nov 2026 | FLUX 3 Image Klein | r1 (tiada perubahan) | K10 / K13: huruf lebar, bukan condensed (5 imej; syarat QC pengguna) | Calon `frasa_bentuk`: "Every letter is a tall, narrow condensed letterform, much taller than it is wide." KALAH (6/6 masih lebar), dibuang | 0/5 → 0/5 |
| 27 Nov 2026 | klein 4B | r1 (calon) | K12: bingkai / garis tepi tidak diminta (2 imej) | Calon `klein4b_hiasan_tepat` ditulis dalam `pembina.py` (UJI); belum dijana | - |

## Belum selesai
- v1.2, sudah dibina (26 Nov): pembina kod bagi tujuh model + semakan 3.11 (`pembina.py`, 3.13).
- v1.2, sudah ditulis (26 Nov): kaedah model baharu (3.12), daftar skrip + kaedah skrip baharu, peraturan langkau model (`run_v12.sh`).
- v1.2, sudah dibina (26 Nov): SK01–SK05 dan `betulkan.py`; SK06 (`finish.py`) dibawa ke cawangan ini.
- v1.2, sudah dibina (27 Nov): belajar selepas setiap jana (`belajar.py`, 3.15). `gen_hf_space.py` (ujian K6 lama) belum mencatat `rev` dan `uji`.
- v1.2, sudah dibina (27 Nov): SK07 (warna ikut peranan), SK08 (bayang dalam huruf K3), `kemasan.py`; SK06 `--palet`.
- v1.2, tidak akan dibina: tepi marker kering K8 (pengguna 28 Nov 2026: tiada gambar asal lebih besar; had kekal, `rujukan.tekstur.had_kekal`). Belum dibina: butir latar sudah, SK06 v1.3); semakan ejaan automatik (kini mata sahaja); bayang lembut K1. (Selesai 27 Nov 2026 melalui Belajar SK: tekstur dibaca daripada kad, SK06 v1.1; ruang tepi ikut kad, SK06 v1.2; tekstur K8 marker, SK06 v1.3; rujukan K6 diukur; garis potong SK07 tidak lagi lurus di sambungan, SK07 v1.1.)
- v1.2, had diterima: gambar upload lebih besar untuk tekstur K8, K10, K13 tiada (pengguna 28 Nov 2026); bintik < 1 px tidak diukur.
- v1.2, belum dibina: tepi marker kering K8 (perlu gambar upload lebih besar; butir latar sudah, SK06 v1.3); semakan ejaan automatik (kini mata sahaja); bayang lembut K1. (Selesai 27 Nov 2026 melalui Belajar SK: tekstur dibaca daripada kad, SK06 v1.1; ruang tepi ikut kad, SK06 v1.2; tekstur K8 marker, SK06 v1.3; rujukan K6 diukur; garis potong SK07 tidak lagi lurus di sambungan, SK07 v1.1.)
- v1.2, belum selesai: sudut rujukan K1 dan K6 belum diukur; Qwen-Image-2512 dan GLM-Image belum diuji (tidak muat di CPU).
- v1.2, bukti masih lemah: aturan 3.4–3.7 diuji pada satu kad (K3) dan satu ayat sahaja. Perlu diulang pada kad lain dan ayat pendek sebelum dianggap kukuh.
- v1.2, belum diuji langsung: aturan 3.9–3.10 (Qwen-Image-2512, GLM-Image). Aturan 3.8 (FLUX 3 Image Klein) lulus ujian kelayakan di CPU, 27 Nov 2026. Perlu ujian kelayakan melalui Space (GPU, kuota harian); pengguna sebelum ini meminta CPU sahaja, jadi ujian ini menunggu kebenaran. `gen_hf_space.py` belum ada profil untuk tiga Space ini.
- Calon v1.3, belum diuji: gambar rujukan sebagai input model (klein 4B dan Z-Image ada saluran input gambar dalam diffusers; ERNIE tiada).
- Belum dibina: struktur Kad Gaya, pembina prompt, rekod QC, kemasan ikut kad, daftar design.
- Prompt hitam putih K2, K3 dan K4 (pembina v1.1) belum diuji pada model utama. K3 hitam putih: 2 imej GLM-Image sahaja (26 Nov), kedua-dua gagal QC (perkataan berulang).
- Ujian banding gaya yang sama: hitam putih lawan berwarna.
- Ujian laluan 3 pada satu ayat ~12 perkataan.
- PyTorch, diffusers dan OCR dalam skrip setup environment.
- Kerja lettering masih di 7 cawangan (tidak digabung, keputusan pengguna 25 Nov); peta: handover bahagian 6.
