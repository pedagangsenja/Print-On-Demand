# Standard Lettering v1.2 (v1: 25 Nov 2026; v1.2: 26 Nov 2026)

Status: v1 dipersetujui pengguna 25 Nov 2026; v1.2 diluluskan pengguna sebagai standard 26 Nov 2026 (menggantikan v1); **sebahagian dibina**: pembina prompt ikut model siap (3.13); selebihnya lihat "Belum selesai". Liputan: laluan 1–2 (ayat 1–8 perkataan), kemasan F1–F2. Laluan 3–4 = percubaan (belum diuji); F3 ditangguh.

## Apa berubah dalam v1.2
1. **Prompt ikut model** (langkah 3): isi gaya tetap daripada Kad; cara menulis berbeza bagi setiap model. Tujuh model: 3.4 klein 4B, 3.5 Z-Image Turbo, 3.6 ERNIE Turbo, 3.7 MOSS (diuji), dan 3.8 FLUX 3 Image Klein, 3.9 Qwen-Image-2512, 3.10 GLM-Image (belum diuji).
2. **Kitaran QC** (langkah 5): tukar seed dahulu; reka semula prompt model itu hanya untuk cacat sistematik; had 2 pusingan; pembaikan ditulis balik ke aturan model.
3. **Ukuran rujukan dalam Kad** (langkah 1): angka diukur daripada gambar upload, bukan diteka.
4. **Pembetulan selepas jana oleh skrip** (langkah 5b): ruang tepi, kedudukan, condong, hitam putih bersih; hanya bila ukuran tersasar.
5. **Mata pengguna pintu terakhir** (langkah 7): imej yang lulus QC tetapi nampak buruk = gagal; sebabnya masuk Kad.
6. **Kaedah model baharu** (3.12, arahan pengguna 26 Nov 2026): model yang belum ada aturan dikaji dahulu ikut borang 10 soalan; aturannya ditulis dan disimpan untuk model itu sahaja, supaya setiap model ada standard prompt sendiri.
7. **Daftar skrip dan kaedah skrip baharu** (selepas langkah 6, arahan pengguna 26 Nov 2026): empat skrip pembetulan + skrip kemasan didaftar; skrip baharu dibina bila gambar upload memerlukannya, kemudian disimpan, didaftar dan dimasukkan ke dashboard.
8. **Peraturan langkau model** (langkah 4, arahan pengguna 26 Nov 2026): model yang terlalu lama atau bermasalah dilangkau, model seterusnya dijalankan, dan hal itu dilaporkan dalam chat.

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
- Tujuh model ada aturan: empat sudah diuji (3.4–3.7, rev r1) dan tiga ditulis daripada sumber rasmi sahaja, belum diuji (3.8–3.10, rev r0). Aturan r0 mesti lulus ujian kelayakan (3.12) sebelum dipakai untuk design sebenar.
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

### 3.8 Aturan FLUX 3 Image Klein (rev r0: sumber rasmi sahaja, BELUM diuji)
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
- **Dalam kapsyen DILARANG:** perkataan Spesifikasi Teks, petikan, koordinat, pertimbangan mutu atau emosi. Semua itu duduk dalam jadual.
- **Jadual unsur:** satu baris bagi setiap baris teks, satu bagi latar, satu bagi setiap hiasan. Kunci ikut turutan: `id`, `bbox`, `desc`.
  - `id` baris teks: `En_Text_1`, `En_Text_2`… dari atas ke bawah. Unsur lain: kata nama + indeks dari kiri ke kanan (`background_1`, `sparkle_1`, `sparkle_2`). Setiap id unik, dan setiap id disebut sekali dalam kapsyen.
  - `desc`: bermula dengan identiti unsur, tanpa kedudukan; baris teks membawa perkataan tepat dalam petikan berganda serta tipografinya: `Huge heavy condensed bold sans-serif capitals in pure white reading "PATIENCE", flat vector.`
  - Label: `Small solid white rectangular label carrying small bold black sans-serif capitals reading "WHAT".`
- **`bbox` daripada ukuran kad:** y = piksel_y ÷ tinggi kanvas × 1000; x = piksel_x ÷ lebar kanvas × 1000; integer; tinggalkan sedikit ruang di sekeliling teks. Daripada kotak MOSS (asalan tengah): y = (y + 512) ÷ 1024 × 1000, x = (x + 384) ÷ 768 × 1000.
- **Panjang kapsyen:** 100–350 perkataan (rasmi). Contoh K3H: kapsyen + jadual 303 perkataan.
- **Tetapan:** checkpoint suling, 16 langkah, tanpa guidance (Space: mod "Distilled (16 steps)", `guidance_scale` 1.0), `prompt_upsampling` False, 768×1024, seed tetap.
- **Tempat jalan:** Space rasmi `black-forest-labs/flux-3-image-klein` (GPU, kuota harian). CPU belum diukur.
- **Lesen (rasmi):** FLUX Kommunity v1.0: hasil komersial dibenarkan untuk pengguna dengan hasil kasar di bawah US$5 juta setahun, tertakluk kepada syarat lesen. Berbeza daripada enam model lain (Apache 2.0 / MIT).
- **Cacat diketahui:** belum diuji. Kad model: teks boleh tidak tepat; unsur kecil yang diminta mungkin tidak muncul; unsur boleh melepasi kotaknya.

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
- **Syarat pakai:** hasil pembina pada K3 × ayat H tidak lebih buruk daripada contoh tulisan tangan (11/12 ejaan betul). **Belum dibuktikan pada imej:** ujian 26 Nov dihentikan atas arahan pengguna selepas 6 imej klein 4B, dan 6 imej itu dipadam atas arahan pengguna; tiada hasil disimpan.

### 3.14 Aturan model tambahan
Tempat menyimpan aturan model baharu yang ditulis ikut 3.12 (3.14.1, 3.14.2, …). Belum ada.

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

- Tiga model tambahan (26 Nov 2026), dijalankan melalui Space Hugging Face (GPU, kuota harian) kerana tidak muat atau belum diukur di CPU. Belum diuji dengan aturan sendiri; perlu ujian kelayakan dahulu:

| Model | Tempat jalan | Langkah | Guidance | Penambah prompt | Aturan | Lesen | Kuota percuma |
|---|---|---|---|---|---|---|---|
| FLUX 3 Image Klein | Space `black-forest-labs/flux-3-image-klein` | 16 | tiada | dimatikan | 3.8 | FLUX Kommunity v1.0 (bersyarat) | kira-kira 9 imej sehari |
| Qwen-Image-2512 | Space `Qwen/Qwen-Image-2512` | 50 | 4.0 | dimatikan | 3.9 | Apache 2.0 | kira-kira 1 imej sehari |
| GLM-Image | Space `multimodalart/GLM-Image` | 50 | 1.5 | tidak dipakai | 3.10 | MIT | kira-kira 2 imej sehari |

Kuota: daripada jadual induk model dalam dashboard (2512 diukur 22–23 Nov; yang lain dikira daripada saat GPU setiap imej; bukti lemah).

### Peraturan langkau model (v1.2, arahan pengguna 26 Nov 2026)
- **Turutan model (CPU):** MOSS → ERNIE Turbo → Z-Image Turbo → klein 4B. Asas: lulus QC dalam AI Image Test 2 (23/30, 21/30, 13/30, 7/30; bukti lemah). Tiga model Space GPU tidak dijalankan (keputusan pengguna 26 Nov 2026: tiada Space GPU).
- **Langkau bila terlalu lama:** masa satu model melebihi 20 minit (muat turun) + 13 minit bagi setiap imej. 13 minit ialah kira-kira dua kali masa paling perlahan yang direkod (392 s, MOSS). Angka ini cadangan Claude; menunggu pengesahan pengguna.
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

5. **Ubahan berjaya** (lebih banyak seed lulus daripada sebelumnya, tiada cacat baharu): ditulis balik ke aturan model itu (3.4–3.10), rev naik, dicatat dalam "Catatan pembaikan aturan model". Design seterusnya terus memakai aturan yang sudah dibaiki.
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

## Daftar skrip dan kaedah skrip baharu (v1.2, arahan pengguna 26 Nov 2026)
Skrip di sini ialah kerja SELEPAS jana (pembetulan 5b dan kemasan langkah 6). Alat prompt dan jana ada dalam 3.13 dan langkah 4.

| ID | Skrip | Langkah | Tugas | Parameter daripada kad | Status (26 Nov 2026) |
|---|---|---|---|---|---|
| SK01 | Condong | 5b | Putar blok ke sudut rujukan kad | sudut condong | Belum dibina |
| SK02 | Ruang tepi | 5b | Skala blok supaya ruang tepi sama dengan kad | ruang tepi (%) | Belum dibina |
| SK03 | Kedudukan | 5b | Pusatkan blok pada kanvas | – | Belum dibina |
| SK04 | Hitam putih bersih | 5b | Tukar kelabu dan tepi kabur kepada hitam dan putih tulen | – | Belum dibina |
| SK05 | Ukuran rujukan | 1 | Ukur ruang tepi, sudut dan nisbah baris daripada gambar upload | – | Belum dibina |
| SK06 | Vektor + saiz cetak (`finish.py`) | 6 | SVG induk, susun di tengah, PNG 300 DPI | ruang tepi, tekstur | Ada di cawangan `claude/dazzling-cannon-5wzn6h`; dicuba pada 1 imej K3H (SVG + 18×24 terhasil); palet masih tetap S1–S6 |
| SK07 | Warna C ikut peranan | 6 | Warnakan lapisan ikut peta peranan kad | peta warna | Belum dibina |
| SK08 | Bayang ikut kad | 6 | Bayang 3D / lembut yang AI tidak jana (cth. K3) | arah dan tebal bayang | Belum dibina |

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

**Turutan jalan:** skrip pembetulan baharu masuk SEBELUM SK04, kerana hitam putih bersih mesti akhir sekali. Skrip kemasan baharu ikut urutan langkah 6: vektor, warna, bayang / tekstur, saiz cetak.

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

## Catatan pembaikan aturan model
Setiap ubahan aturan (3.4–3.10) direkod di sini. Ujian pertama (26 Nov 2026, K3 × ayat H, seed 42, 7, 123, semakan mata, bukti lemah) mengubah beberapa perkara serentak, kerana dibuat sebelum peraturan "satu ubahan setiap pusingan".

| Tarikh | Model | Rev | Cacat dengan rangka am | Ubahan | Ejaan betul sebelum → selepas |
|---|---|---|---|---|---|
| 26 Nov 2026 | klein 4B | r1 | Label tambahan di bawah; "WHAT" tiada kotak (3/3) | Prosa mengalir; gaya di dalam ayat baris; had satu ayat | 0/3 → 3/3 |
| 26 Nov 2026 | Z-Image Turbo | r1 | Bintang dan garis lengkung yang tidak diminta | Huraian panjang, baris bernombor, had positif | 3/3 → 3/3 |
| 26 Nov 2026 | ERNIE Turbo | r1 | "WHAT WHAT" (3/3) | Prompt mentah pendek + PE rasmi | 0/3 → 2/3 |
| 26 Nov 2026 | MOSS + LoRA | r1 | Garis lengkung tambahan atas dan bawah | Susun atur JSON dengan kotak setiap baris | 3/3 → 3/3 |

## Belum selesai
- v1.2, sudah dibina (26 Nov): pembina kod bagi tujuh model + semakan 3.11 (`pembina.py`, 3.13).
- v1.2, sudah ditulis (26 Nov): kaedah model baharu (3.12), daftar skrip + kaedah skrip baharu, peraturan langkau model (`run_v12.sh`).
- v1.2, belum dibina: skrip SK01–SK05, SK07, SK08 (lihat Daftar skrip) dan had toleransi 5b; `finish.py` (SK06) belum dibawa ke cawangan ini; semakan ejaan automatik (kini mata sahaja).
- v1.2, belum dibuktikan pada imej: hasil pembina kod (3.13). Had masa langkau menunggu pengesahan pengguna.
- v1.2, bukti masih lemah: aturan 3.4–3.7 diuji pada satu kad (K3) dan satu ayat sahaja. Perlu diulang pada kad lain dan ayat pendek sebelum dianggap kukuh.
- v1.2, belum diuji langsung: aturan 3.8–3.10 (FLUX 3 Image Klein, Qwen-Image-2512, GLM-Image). Perlu ujian kelayakan melalui Space (GPU, kuota harian); pengguna sebelum ini meminta CPU sahaja, jadi ujian ini menunggu kebenaran. `gen_hf_space.py` belum ada profil untuk tiga Space ini.
- Calon v1.3, belum diuji: gambar rujukan sebagai input model (klein 4B dan Z-Image ada saluran input gambar dalam diffusers; ERNIE tiada).
- Belum dibina: struktur Kad Gaya, pembina prompt, rekod QC, kemasan ikut kad, daftar design.
- Skrip warna ikut peranan belum dibina; `finish.py` masih memaksa palet tetap.
- Prompt hitam putih K2, K3 dan K4 (pembina v1.1) belum diuji pada model utama. K3 hitam putih: 2 imej GLM-Image sahaja (26 Nov), kedua-dua gagal QC (perkataan berulang).
- Ujian banding gaya yang sama: hitam putih lawan berwarna.
- Ujian laluan 3 pada satu ayat ~12 perkataan.
- PyTorch, diffusers dan OCR dalam skrip setup environment.
- Kerja lettering masih di 7 cawangan (tidak digabung, keputusan pengguna 25 Nov); peta: handover bahagian 6.
