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

Tambahan daripada semakan langkah 4 (menunggu semakan pengguna):
- Nisbah kanvas rujukan dicatat (cth. upload ke-3 segi empat sama); kad menyatakan cara susunan disesuaikan ke potret 3:4.
- Imej bukti 1e merekod enjin penuh yang menghasilkannya (model, varian fail, langkah, seed).

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

## Langkah 4: Jana (cadangan 25 Nov; menunggu semakan pengguna)

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
