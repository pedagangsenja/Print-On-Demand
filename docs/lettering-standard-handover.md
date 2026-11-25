# Standard Lettering: dokumen serahan (25 Nov 2026)

Dokumen ini menyerahkan kerja daripada sesi 24–25 Nov (cawangan `claude/admiring-cerf-b3bdfi`) kepada chat baharu. Belum ada apa-apa yang dibina daripada cadangan; semuanya kajian dan cadangan.
Tahap bukti semua angka ujian: lemah (ujian kecil, satu hingga empat seed, dinilai oleh Claude), kecuali lesen (rasmi, API Hugging Face 24 Nov).

Kandungan:
1. Model yang dimuktamadkan
2. Workflow asal S1–S6
3. Cadangan pertama: 4 lapisan, 4 laluan, 5 kunci
4. Kajian cadangan langkah demi langkah (1–9)
5. Keputusan tertangguh
6. Peta cawangan dan fail

Carta aliran sebelah-menyebelah (bahagian 2 dan 3): `docs/lettering-aliran.png`, dijana oleh `scripts/lettering_flowchart.py`.

## 1. Model yang dimuktamadkan

Syarat pengguna: percuma, jalan di CPU sahaja (container 4 teras, 15 GB RAM, tiada GPU), tiada kuota, lesen komersial tanpa syarat. Disemak satu per satu pada 24 Nov: fail LICENSE, kad model, gate, dan lesen setiap komponen (pengekod teks dipadankan melalui config; VAE melalui hash fail).

Lulus: 12 model (11 penuh + 1 dengan titik kelabu). Enjin jana: diffusers 0.43 + PyTorch 2.15, bf16 dengan AMX. stable-diffusion.cpp tidak dipakai (676 s berbanding 68 s untuk imej klein yang sama).

| # | Model (repo Hugging Face) | Lesen | Pengekod teks (keluarga) | Fail yang dipakai | Tetapan | Masa CPU / imej 768×1024 | Hasil ujian |
|---|---|---|---|---|---|---|---|
| 1 | MOSS-Image SFT (`OpenMOSS-Team/MOSS-Image-SFT`) + LoRA `lodestones/MOSS-Image-SFT-8-steps-dmd` | Apache 2.0 (kedua-dua) | Qwen3.5-9B (LLM) | bf16 asal, 27–28 GB; pengekod sebahagian di cakera | 8 langkah, tanpa CFG, LoRA 0.7 | 439 s | S1–S6: 12/12 ejaan betul (P9, P9b). Lettering BM 9–16 perkataan: 0/5 |
| 2 | ERNIE-Image-Turbo (`baidu/ERNIE-Image-Turbo`) | Apache 2.0 | Ministral-3-3B (LLM) + penambah prompt | GGUF Q8 `unsloth/ERNIE-Image-Turbo-GGUF`, 8.7 GB | 8 langkah, guidance 1.0 | 438 s (P9b); 409 s (23 Nov) | S1–S6: 12/12 (P9b). 23 Nov: 10/10. v3 BM 9–16 perkataan dengan penambah: 14/20 |
| 3 | FLUX.2 klein 4B (`black-forest-labs/FLUX.2-klein-4B`) | Apache 2.0 | Qwen3-4B (LLM) | GGUF Q8 `leejet/FLUX.2-klein-4B-GGUF`, 4.3 GB | 4 langkah, guidance 1.0 | 68–93 s | S1–S6: 6/12 (P9b; S3 dan S6 0/2). 23 Nov: 3/10. Chat ini, teks sahaja: 5/9 |
| 4 | Z-Image-Turbo (`Tongyi-MAI/Z-Image-Turbo`) | Apache 2.0 | Qwen3-4B (LLM) | GGUF Q8 `leejet/Z-Image-Turbo-GGUF`, 6.6 GB | 9 langkah, guidance 0 | 280 s (23 Nov) | 23 Nov: 6/10. Belum diuji pada S1–S6 |
| 5 | FLUX.1-schnell (`black-forest-labs/FLUX.1-schnell`; komponen dari `unsloth/FLUX.1-schnell`) | Apache 2.0; titik kelabu: CLIP-L OpenAI tiada tag lesen | T5-XXL + CLIP-L (T5) | GGUF Q6_K `city96/FLUX.1-schnell-gguf`, 9.8 GB (Q8 12.7 GB kehabisan RAM) | 4–6 langkah, guidance 0, had 256 token | 260 s (img2img) | Text-to-image belum diuji |
| 6 | Chroma1-Flash / Chroma1-HD (`lodestones/Chroma1-Flash`) | Apache 2.0 | T5-XXL (T5), tiada CLIP | GGUF Q8 `silveroxides/Chroma1-Flash-GGUF`, 9.7 GB; T5 dikongsi dengan schnell (hash sama) | Flash: 10 langkah, guidance 1.0 | 266 s (img2img) | Text-to-image belum diuji |
| 7 | Z-Image asas (`Tongyi-MAI/Z-Image`) | Apache 2.0 | Qwen3-4B (LLM) | belum dimuat turun | 28–50 langkah | belum diukur | Belum diuji (lambat) |
| 8 | FLUX.2 klein base 4B (`black-forest-labs/FLUX.2-klein-base-4B`) | Apache 2.0 | Qwen3-4B (LLM) | belum dimuat turun | 50 langkah | belum diukur | Belum diuji (lambat) |
| 9 | AuraFlow v0.3 (`fal/AuraFlow-v0.3`) | Apache 2.0 | Pile-T5-XL (T5) | belum dimuat turun | 50 langkah | belum diukur | Belum diuji |
| 10 | LongCat-Image (`meituan-longcat/LongCat-Image`) | Apache 2.0 | Qwen2.5-VL-7B (LLM) | belum dimuat turun | 50 langkah | belum diukur | Belum diuji |
| 11 | OmniGen v1 (`Shitao/OmniGen-v1`) | MIT | Phi-3-mini | belum dimuat turun | – | belum diukur | Belum diuji |
| 12 | Kandinsky 2.2 (`kandinsky-community/kandinsky-2-2-decoder`) | Apache 2.0 | CLIP-bigG (had 77 token) | fail asal | 50 langkah | 391 s (img2img) | 0/9: huruf rosak. Tidak sesuai untuk lettering |

Kedudukan untuk lettering: MOSS dan ERNIE (kedua-duanya 12/12 pada S1–S6) ialah model utama; klein 4B paling laju tetapi 6/12; Z-Image-Turbo, schnell dan Chroma perlu ujian text-to-image pada S1–S6 sebelum dipakai; model 7–11 belum diuji; Kandinsky digugurkan.

Tidak lulus syarat (jangan dipakai): Emuru (bukan penjana gambar); FLUX.3 Image Klein (had pendapatan US$5 juta); SDXL, SSD-1B, Segmind-Vega (OpenRAIL++); OmniSVG 1.1 (dibina atas Qwen2.5-VL-3B, lesen research); Lumina-Image-2.0 (Gemma); HiDream-I1 (Llama, 17B); FLUX.2 klein 9B / dev (bukan komersial). Tak muat RAM: Qwen-Image / 2512, GLM-Image, NextStep-1.1, LLaDA-Image, Ming-Image. Belum pasti: Nitro-E, Lens, MiniT2I.

Ujian 24 Nov dalam chat ini (cara "panduan susun atur", img2img kekuatan 0.6, 63 imej): ejaan 9/9 untuk ERNIE, MOSS, Z-Image, Chroma dan schnell; klein 8/9; Kandinsky 0/9. Hasil nampak seperti template kerana model hanya menokok tekstur atas font. Cara ini DITOLAK; standard memakai text-to-image penuh. Data: `designs/model-test-12/results.json`.

## 2. Workflow asal S1–S6 (Lettering P9, 23–24 Nov)

Sumber: `scripts/lettering/styles.py`, `gen_moss.py`, `sheet.py`, `finish.py` dan `docs/research/posters/08-lettering.md` di cawangan `claude/affectionate-wright-7y95k3`; perbandingan 3 enjin di `claude/dazzling-cannon-5wzn6h`.

1. Rujukan: pengguna upload poster rujukan; Claude ambil ciri umum sahaja (ayat, susun atur dan tandatangan tidak disalin).
2. Ayat: 3–7 perkataan Inggeris (diuji pada 4 perkataan sahaja), semak trademark, tetapkan baris dan perkataan utama. Definisi dashboard: pendek ≤ 6 perkataan, panjang ≥ 7.
3. Prompt: 6 templat tetap dalam `styles.py` (S1–S6), slot 4 perkataan dengan huruf besar / kecil ditetapkan, + ekor larangan tetap (`COMMON_TAIL`). Panjang 87–124 kata.
4. Jana: text-to-image penuh, 768×1024, seed 42 dan 7 (CPU). Enjin asal MOSS SFT + LoRA 8 langkah.
5. QC pada helaian semakan: 3 pintu wajib (G1 ejaan 100%, G2 tiada teks rawak, G3 tiada cacat) + 9 ciri gaya umum yang sama untuk semua gaya (lulus ≥ 8/9). Gagal: seed baharu (maksimum 4).
6. Kemasan `finish.py`: besarkan 4×, asing dakwat, bersih, vektor (potrace), paksa palet gaya, susun satu blok di tengah (76% × 78%), 300 DPI untuk 8×10, 11×14, 16×20, 18×24, 24×36, tekstur prosedur (grain / worn / chalk).
7. Pengguna lulus atau tolak (~5 minit).
8. Simpan dalam Daftar S/C: gaya S (`data/gaya/items`) dan warna C (`data/warna/items`). Sejak 25 Nov rekod menyimpan prompt terisi dan imej asal.
9. Mockup, pin, upload: diserah kepada Workflow (belum dibuat).

Struktur prompt S1–S6 (urutan tetap): medium + "portrait"; latar satu warna bernama; bentuk susunan; "The text reads exactly, N lines:" + arahan setiap perkataan (jenis huruf, saiz, warna); hiasan; ruang tepi; had warna atau larangan khusus; ekor larangan. Peraturan tersirat: setiap perkataan dalam petikan muncul sekali; tiada kod hex atau nombor; huruf diterangkan ikut kelakuan, bukan nama font.

Hasil: MOSS 12/12 dan ERNIE 12/12 ejaan betul pada "Small steps every day"; klein 4B 6/12. 60 imej MOSS lagi (10 quote × 6 gaya) dijana di `claude/happy-davinci-hv0xb3`, QC tidak direkod. Kelemahan yang dicatat: S1 kurang melantun berbanding rujukan; S3 semua baris hampir sama besar; S4 tekstur kapur dibina semula; S6 seed 42 garis inline tercantum semasa vektor.

## 3. Cadangan pertama (25 Nov): 4 lapisan, 4 laluan, 5 kunci

Sebab cadangan: templat S1–S6 terkunci pada 4 perkataan; gaya, warna dan latar bercampur dalam satu ayat; QC tidak diambil daripada upload; tiada peraturan tukar model; `finish.py` hanya untuk dakwat rata atas latar satu warna.

Empat lapisan:
1. Kad Gaya: data berstruktur yang dinyahkod daripada upload; warna C berasingan.
2. Pembina prompt: kad + ayat + warna C + keluarga model menghasilkan prompt.
3. QC ikut kad: 3 pintu wajib + ciri kad (≥ 7/8).
4. Kemasan ikut kelas: F1 vektor rata, F2 rata + tekstur, F3 raster (belum wujud).

Empat laluan, ikut panjang ayat baharu (bukan ayat rujukan):

| Laluan | Panjang | Cara | Bukti: imej betul semua ejaan (102 imej, semua ujian digabung) |
|---|---|---|---|
| 1 Pendek | 1–4 perkataan | AI penuh, satu blok, 2 seed | 25/28 (89%) |
| 2 Sederhana | 5–8 | AI penuh, hierarki wajib, 3–4 seed | 17/27 (63%) |
| 3 Panjang | 9–16 | Hibrid: AI lukis 2–4 perkataan utama; baris lain font berlesen; skrip susun ikut kad | 20/44 (45%) bila AI penuh |
| 4 Terlalu panjang | 17+ | Font dahulu: AI buat tajuk 1–3 perkataan dan hiasan sahaja | 1/3 (33%) bila AI penuh |

Laluan 3 dan 4 belum dibina dan belum diuji. Perkara terbuka: nota P9 merekod pengguna menolak susunan font dengan kod pada 22 Nov kerana nampak "ditaip"; kedua-dua laluan mesti diuji dan diluluskan pengguna sebelum masuk standard.

Lima kunci gaya (supaya gaya diikut walaupun model ditukar):
1. Kad Gaya satu-satunya sumber gaya.
2. QC yang sama untuk semua model.
3. Model hanya dipakai untuk gaya yang ia lulus (jadual model × gaya).
4. Skrip memaksa warna, margin, tekstur.
5. Peraturan ulang: ayat penegas + seed baharu (maksimum 4), kemudian model sandaran. Bukti v3 (ERNIE + penambah, 10 design): gaya ≥ 7/8 pada cubaan pertama 6/10; menjelang cubaan ke-3 10/10.

Keluarga model: LLM (MOSS, klein, Z-Image, ERNIE) menerima prompt penuh; T5 (schnell, Chroma) dicadang menerima versi ringkas dengan teks di depan (hipotesis, belum diuji).

Aliran cadangan (9 langkah): 1 Kad Gaya; 2 Ayat + peranan + laluan; 3 Pembina prompt; 4 Jana; 5 QC ikut kad; 6 Kemasan ikut kelas; 7 Pengguna lulus atau tolak; 8 Simpan dalam S&C; 9 Mockup, pin, upload.

## 4. Kajian cadangan langkah demi langkah

Setiap langkah dibanding dengan S1–S6. Langkah 1–6 (termasuk semua tambahan langkah 1) disimpan atas arahan pengguna; langkah 7–9 masih menunggu semakan pengguna. Susunan akhir (satu standard + carta aliran baharu) belum dibuat.

### Pembetulan (25 Nov, selepas membaca cawangan sesi lain)

Beberapa kenyataan awal dalam semakan ini sudah lapuk. Kerja berkaitan ada di cawangan lain yang tidak dibaca pada mulanya:
- `claude/dazzling-cannon-5wzn6h` (P9b, 24 Nov): MOSS, ERNIE-Image-Turbo (GGUF Q8) dan FLUX.2 klein 4B diuji pada S1–S6 × 2 seed dengan prompt yang sama, text-to-image. Ejaan betul: MOSS 12/12, ERNIE 12/12, klein 6/12 (S3 dan S6 tiada seed betul). Purata masa: 438 s, 438 s, 93 s. Jadi jadual model × gaya sudah ada data pertama, dan "hanya MOSS diuji" tidak lagi benar.
- `claude/happy-davinci-hv0xb3` (24 Nov): 60 imej mentah MOSS (10 quote 4 perkataan × 6 gaya). Keputusan QC tidak direkod dalam cawangan itu. Jadi S1–S6 sudah dijana pada lebih daripada satu ayat, tetapi masih 4 perkataan sahaja.
- `claude/friendly-knuth-hkclbr` (25 Nov): rekod S dan C dalam Daftar S/C kini menyimpan `prompt` (terisi, dengan perkataan ujian) dan `asal` (imej rujukan). Jadi "prompt tidak disimpan" tidak lagi benar; yang masih tiada ialah ciri gaya berstruktur dan templat tanpa perkataan.
- Carta aliran yang dihantar pada 25 Nov masih membawa tiga tanda lapuk ini dan perlu dibetulkan semasa susunan akhir.

### Langkah 1: Kad Gaya (disemak 25 Nov; disimpan atas arahan pengguna)

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

### Langkah 2: Ayat, peranan dan laluan (disemak 25 Nov; disimpan atas arahan pengguna)

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

### Langkah 3: Pembina prompt (disemak 25 Nov; disimpan atas arahan pengguna)

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

### Langkah 4: Jana (disemak 25 Nov; disimpan atas arahan pengguna)

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

### Langkah 5: QC (disemak 25 Nov; disimpan atas arahan pengguna)

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

### Langkah 6: Kemasan (disemak 25 Nov; disimpan atas arahan pengguna)

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

### Langkah 7, 8 dan 9 (cadangan 25 Nov; menunggu semakan pengguna)

#### Langkah 7: Pengguna lulus atau tolak
Sedia ada: "lulus / tolak (~5 minit)"; Workflow w07 memperuntukkan 15 minit sehari untuk design, produk dan pin. Selepas setiap jana imej, pengguna memilih A atau SNC dan memadam sendiri yang tidak dimahukan. Sebab penolakan tidak direkod.
Yang perlu ditambah:
1. Paparan tetap: upload asal, imej sauh dan hasil sebelah-menyebelah, dengan skor QC dan ejaan.
2. Keputusan direkod dengan sebab daripada senarai tetap (ejaan, gaya kurang serupa, terlalu serupa rujukan, tidak cantik, lain-lain).
3. Sebab tolak disalurkan balik: ke kad (ciri baharu), ke jadual model × gaya, atau ke ulangan.
4. Tiga titik kelulusan: kad (1d), contoh pertama laluan 3–4, dan hasil akhir.
5. Had setiap sesi kelulusan (bilangan imej setiap helaian) supaya masa semakan realistik.

#### Langkah 8: Simpan
Sedia ada (25 Nov): rekod S = nama, jenis, panjang, enjin, imej contoh, imej asal, prompt terisi, nota. Rekod C = nama, latar, senarai hex huruf, gaya, imej, prompt terisi, nota. `image_log` = satu baris setiap imej ujian (skrip di cawangan `claude/vigilant-knuth-0bmbio`).
Yang perlu ditambah:
1. Kad Gaya berstruktur dan templat prompt tanpa perkataan disimpan dalam rekod S (sekarang hanya prompt terisi).
2. Rekod C: peranan setiap warna dan nama warna untuk prompt; satu sumber kod hex (C001 `#f4f1eb` berbanding `styles.py` `#f4f1ea`).
3. Daftar design yang diluluskan (ayat, S, C, model, seed, fail induk, status produk); S&C hanya mendaftar gaya dan warna.
4. Hasil kelayakan model disambung ke rekod S (enjin mana lulus untuk gaya itu).
5. Satu sumber kerja: skrip dan data lettering kini berselerak di sekurang-kurangnya 7 cawangan; perlu digabung ke satu cawangan supaya setiap sesi nampak kerja sesi lain.
6. Fail disimpan sebelum sesi tamat: imej mentah, SVG induk, log.
7. Versi kad dan tarikh kemas kini.

#### Langkah 9: Mockup, pin, upload
Sedia ada: diserah kepada Workflow (w02 semak trademark, w03 mockup, w04 upload Printify / WooCommerce, w05 jadual pin). Dalam salinan repo senarai Setup, 26 daripada 30 langkah masih "Belum"; skrip mockup belum dibuat.
Yang perlu ditambah:
1. Spesifikasi serahan daripada lettering ke Workflow: fail cetak setiap saiz ikut senarai semak pembekal, pratonton, ayat, kod S dan C, hasil saringan trademark.
2. Setiap produk dan pin ditanda dengan kod S dan C, supaya tab Prestasi boleh menunjukkan gaya dan warna mana yang menang.
3. Maklum balas jualan kembali ke S&C (gaya menang dapat lebih banyak ayat dan varian warna).
4. Dasar platform tentang kandungan janaan AI dan design yang serupa rujukan: belum disemak.
5. Langkah 9 bergantung pada Setup kedai yang belum siap; standard lettering boleh berhenti di serahan.

## 5. Keputusan tertangguh (menunggu pengguna)

1. Setuju tambahan langkah 7, 8 dan 9?
2. Susun semua langkah jadi satu standard dan carta aliran baharu.
3. Gabung kerja lettering dari cawangan lain ke satu cawangan; cawangan mana jadi induk? (`CLAUDE.md` menamakan `claude/jolly-hamilton-sdopyz`.)
4. Tangguh F3; standard versi pertama meliputi F1 dan F2 sahaja?
5. Uji laluan 3 pada satu ayat ~12 perkataan sebelum masuk standard?
6. Tambah PyTorch, diffusers dan OCR ke skrip setup environment (sekarang hanya potrace dan alat vektor)?
7. Simpan 3 upload rujukan sesi ini sebagai imej asal dalam Daftar S/C? Fail hanya ada dalam container (`designs/model-test-12/refs/`, tidak di-commit); perlu dimuat naik semula dalam chat baharu.
8. 72 imej ujian 24 Nov (63 panduan + 9 klein teks sahaja): A (tab AI Image Test) atau SNC? Imej hanya ada dalam container sesi 24–25 Nov (tidak di-commit) dan hilang bila sesi itu tamat; data ringkas kekal di `designs/model-test-12/results.json`.

Tiga upload rujukan sesi ini: (1) blok grunge kuning-putih atas hitam, 5 perkataan; (2) skrip berus putih atas hitam, 4 perkataan, sama rujukan dengan S003 (IMG_5732); (3) lettering vintaj krim atas hitam, 7 perkataan, segi empat sama.

## 6. Peta cawangan dan fail

| Cawangan | Isi berkaitan |
|---|---|
| `claude/admiring-cerf-b3bdfi` (sesi ini) | Dokumen ini; `docs/lettering-aliran.png`; `scripts/lettering_flowchart.py`; `designs/model-test-12/` (skrip jana 7 model, panduan, `results.json`) |
| `claude/affectionate-wright-7y95k3` | Lettering P9: `scripts/lettering/styles.py`, `gen_moss.py`, `sheet.py`, `finish.py`; `docs/research/posters/08-lettering.md`; `data/export/lettering_p9/` |
| `claude/dazzling-cannon-5wzn6h` | P9b: MOSS vs ERNIE vs klein pada S1–S6 (`designs/lettering-p9b/`, `lettering_p9_engines.json`) |
| `claude/happy-davinci-hv0xb3` | Ujian 10 quote: 60 imej mentah MOSS (`designs/lettering/test-10quote/`) |
| `claude/sharp-franklin-29eamk` | SOP v3: `designs/lettering-test/v3/build_prompts.py`; `data/export/models/lettering_*.json` (ujian v1–v3, rubrik QC, jurang) |
| `claude/friendly-knuth-hkclbr` | Daftar S/C terkini (prompt dan imej asal dalam rekod) |
| `claude/vigilant-knuth-0bmbio` | `scripts/build_image_log.py` (dataset `image_log`) |

Dashboard: https://claude.ai/artifact/EeAC4MqQijSGYGTWfZW3Sg (stor `data/gaya/items`, `data/warna/items`; dataset `image_log`, `model_compare`, `model_test`).
