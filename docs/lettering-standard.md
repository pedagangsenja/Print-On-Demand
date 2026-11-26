# Standard Lettering v1.2 (v1: 25 Nov 2026; v1.2: 26 Nov 2026)

Status: v1 dipersetujui pengguna 25 Nov 2026; rombakan v1.2 diarahkan pengguna 26 Nov 2026; **belum dibina** (lihat "Belum selesai"). Liputan: laluan 1–2 (ayat 1–8 perkataan), kemasan F1–F2. Laluan 3–4 = percubaan (belum diuji); F3 ditangguh.

## Apa berubah dalam v1.2
1. **Prompt ikut model** (langkah 3): isi gaya tetap daripada Kad; cara menulis berbeza bagi setiap model (3.4 klein 4B, 3.5 Z-Image Turbo, 3.6 ERNIE Turbo, 3.7 MOSS).
2. **Kitaran QC** (langkah 5): tukar seed dahulu; reka semula prompt model itu hanya untuk cacat sistematik; had 2 pusingan; pembaikan ditulis balik ke aturan model.
3. **Ukuran rujukan dalam Kad** (langkah 1): angka diukur daripada gambar upload, bukan diteka.
4. **Pembetulan selepas jana oleh skrip** (langkah 5b): ruang tepi, kedudukan, condong, hitam putih bersih; hanya bila ukuran tersasar.
5. **Mata pengguna pintu terakhir** (langkah 7): imej yang lulus QC tetapi nampak buruk = gagal; sebabnya masuk Kad.

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
- Model yang ada aturan sendiri (3.4–3.7) WAJIB memakai aturan itu. Model tanpa aturan memakai rangka am (3.3) sehingga aturannya ditulis (3.9).
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
4. Tiada negative prompt untuk mana-mana model. Tetapan yang dikunci semuanya tanpa CFG (guidance 0 atau 1), jadi negative prompt tidak dibaca. Larangan ditulis di dalam prompt ikut aturan model.
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

### 3.4 Aturan FLUX.2 klein 4B (rev r1)
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

### 3.5 Aturan Z-Image Turbo (rev r1)
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
- **Had ditulis sebagai ayat POSITIF, bukan "no …":** `The only text in the image is these five words, each appearing once. The image uses only pure white and pure black, flat fills, sharp edges, and a clean empty background.`
- **Panjang:** 80–250 perkataan. Contoh yang lulus: 249 perkataan.
- **Tetapan:** GGUF Q8_0, 9 langkah, guidance 0.0, tiada penambah prompt.
- **Cacat diketahui (r1):** percikan hanya di kanan label; ruang tepi sempit (dibetulkan skrip, 5b). Rangka am juga lulus ejaan 3/3, jadi aturan ini mengemaskan hiasan, bukan ejaan.

### 3.6 Aturan ERNIE-Image-Turbo (rev r1)
- **Sumber:** dokumen diffusers: penambah prompt (PE) hidup secara lalai dan "may reduce instruction-following accuracy" (rasmi). Kad model: skor teks OneIG-EN 0.9488 tanpa PE lawan 0.9666 dengan PE; GENEval keseluruhan 0.8667 tanpa PE lawan 0.8510 dengan PE (rasmi).
- **Dua peringkat:** (a) pembina menulis prompt mentah yang pendek; (b) PE rasmi mengembangkannya; imej dijana daripada prompt yang dikembangkan.
- **Prompt mentah, satu perenggan pendek (contoh yang lulus: 94 perkataan):**
  1. Blok A: `A black and white hand-lettering quote poster, portrait.`
  2. Blok B: `Solid black background, white lettering.`
  3. Blok C, kemudian titik bertindih, kemudian blok D + E + F sebagai senarai dipisah koma bernoktah, satu butir setiap baris, bentuk `"PERKATAAN" in <frasa bentuk huruf>`: `Five stacked lines in one tight centered block that tilts up to the right: "PATIENCE" in huge heavy condensed bold sans-serif capitals; "Builds" in large bold brush script; …`
  4. Blok H + G: `Only these five words, no other text, pure black and white, flat vector style, wide black margins.`
- **PE dijalankan SEKALI bagi setiap prompt, seed 42.** Hasil yang sama dipakai untuk semua seed imej, supaya seed hanya mengubah imej, bukan prompt. PE boleh menulis dalam bahasa Cina; itu dibenarkan.
- **Semakan WAJIB pada hasil PE sebelum jana:** setiap perkataan Spesifikasi Teks ada, ejaan dan huruf besar / kecil tepat; turutan baris sama; tiada perkataan Latin lain dalam petikan. PE boleh menyebut semula sesuatu perkataan sebagai rujukan (contoh K3H: 'PATIENCE' dua kali); itu dibenarkan.
- **Jika semakan gagal:** jalankan PE semula dengan seed 7, kemudian 123. Masih gagal: PE dimatikan, rangka am (3.3) dipakai, dan hal ini direkod.
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

### 3.8 Semakan automatik sebelum jana (semua model)
Prompt yang gagal mana-mana semakan TIDAK dijana.
- Semua model: perkataan dalam petikan (MOSS: senarai `text`) sama tepat dengan Spesifikasi Teks, ikut turutan, sekali setiap satu; tiada angka, hex, nama font, jenama, atau nama warna selain black dan white; dalam had token model.
- klein 4B: satu perenggan; tiada senarai gaya terpisah; tiada senarai larangan selepas ayat had (no signature, no watermark, no logo, no frame…).
- Z-Image Turbo: bilangan ayat "Line …" sama dengan bilangan baris; tiada frasa "no …" dalam ayat penutup.
- ERNIE Turbo: semakan pada prompt mentah DAN pada hasil PE (3.6).
- MOSS: JSON sah; kunci wajib ada; setiap `bbox` di dalam kanvas dan y_atas < y_bawah, x_kiri < x_kanan; bilangan butir teks sama dengan bilangan baris.

### 3.9 Menambah atau mengubah aturan model
- **Model baharu:** (1) baca kad model rasmi dan panduan prompt rasminya; (2) catat sumber dan tahap bukti; (3) tulis aturan dengan tujuh medan yang sama seperti 3.4–3.7: sumber, bentuk, turutan, cara tulis teks dan gaya, cara tulis had, tetapan, cacat diketahui; (4) uji banding rangka am lawan aturan baharu: kad sama, ayat sama, seed 42, 7, 123; (5) aturan diterima jika bilangan imej lulus tidak kurang daripada rangka am.
- **Mengubah aturan sedia ada:** hanya melalui kitaran QC (langkah 5), SATU ubahan setiap pusingan. Setiap ubahan, berjaya atau tidak, direkod dalam "Catatan pembaikan aturan model" di hujung dokumen ini; ubahan yang berjaya menaikkan rev aturan (r1 → r2).
- **Rekod bersama setiap imej:** prompt, model, rev aturan, versi kad, versi pembina.
- **Status:** aturan 3.4–3.7 kini wujud sebagai contoh tulisan tangan untuk K3 × ayat H (`designs/lettering-v1/khas.py`, versi khas-v0, lulus `khas.semak`). Pembina kod bagi setiap model belum dibina. Sehingga dibina, prompt ditulis tangan ikut aturan ini, ayat demi ayat, dan mesti lulus semakan 3.8.

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

- Qwen-Image dan GLM-Image: tidak muat dalam RAM 15 GB di CPU; di luar v1.2.
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
2. **Ada imej lulus:** terus ke langkah 7. Kitaran tamat.
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

5. **Ubahan berjaya** (lebih banyak seed lulus daripada sebelumnya, tiada cacat baharu): ditulis balik ke aturan model itu (3.4–3.7), rev naik, dicatat dalam "Catatan pembaikan aturan model". Design seterusnya terus memakai aturan yang sudah dibaiki.
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
- **Belum ditetapkan:** had toleransi setiap ukuran. Ia ditetapkan daripada ukuran upload dan ujian, bukan tekaan. Skrip belum dibina.
- Ruang tepi untuk cetak kekal urusan kemasan (langkah 6); pembetulan di sini hanya supaya imej mentah menepati kad.

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
Model baharu juga memerlukan aturan prompt sendiri sebelum dipakai untuk design sebenar (3.9).

## Catatan pembaikan aturan model
Setiap ubahan aturan (3.4–3.7) direkod di sini. Ujian pertama (26 Nov 2026, K3 × ayat H, seed 42, 7, 123, semakan mata, bukti lemah) mengubah beberapa perkara serentak, kerana dibuat sebelum peraturan "satu ubahan setiap pusingan".

| Tarikh | Model | Rev | Cacat dengan rangka am | Ubahan | Ejaan betul sebelum → selepas |
|---|---|---|---|---|---|
| 26 Nov 2026 | klein 4B | r1 | Label tambahan di bawah; "WHAT" tiada kotak (3/3) | Prosa mengalir; gaya di dalam ayat baris; had satu ayat | 0/3 → 3/3 |
| 26 Nov 2026 | Z-Image Turbo | r1 | Bintang dan garis lengkung yang tidak diminta | Huraian panjang, baris bernombor, had positif | 3/3 → 3/3 |
| 26 Nov 2026 | ERNIE Turbo | r1 | "WHAT WHAT" (3/3) | Prompt mentah pendek + PE rasmi | 0/3 → 2/3 |
| 26 Nov 2026 | MOSS + LoRA | r1 | Garis lengkung tambahan atas dan bawah | Susun atur JSON dengan kotak setiap baris | 3/3 → 3/3 |

## Belum selesai
- v1.2, belum dibina: pembina kod bagi setiap model (kini contoh tulisan tangan `khas.py`); skrip ukuran rujukan daripada upload; skrip pembetulan 5b dan had toleransinya; semakan ejaan automatik (kini mata sahaja).
- v1.2, bukti masih lemah: aturan 3.4–3.7 diuji pada satu kad (K3) dan satu ayat sahaja. Perlu diulang pada kad lain dan ayat pendek sebelum dianggap kukuh.
- Calon v1.3, belum diuji: gambar rujukan sebagai input model (klein 4B dan Z-Image ada saluran input gambar dalam diffusers; ERNIE tiada).
- Belum dibina: struktur Kad Gaya, pembina prompt, rekod QC, kemasan ikut kad, daftar design.
- Skrip warna ikut peranan belum dibina; `finish.py` masih memaksa palet tetap.
- Prompt hitam putih K2, K3 dan K4 (pembina v1.1) belum diuji pada model utama. K3 hitam putih: 2 imej GLM-Image sahaja (26 Nov), kedua-dua gagal QC (perkataan berulang).
- Ujian banding gaya yang sama: hitam putih lawan berwarna.
- Ujian laluan 3 pada satu ayat ~12 perkataan.
- PyTorch, diffusers dan OCR dalam skrip setup environment.
- Kerja lettering masih di 7 cawangan (tidak digabung, keputusan pengguna 25 Nov); peta: handover bahagian 6.
