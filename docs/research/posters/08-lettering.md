# Poster P9: Lettering tangan — alat, install dan workflow (23 Nov 2026)

Keputusan pengguna 23 Nov: **percuma sahaja**; fokus **quote Inggeris pendek (3–7 perkataan)**. Rujukan gaya = 6 imej upload 23 Nov (design orang lain: rujukan gaya sahaja; ayat, susun atur dan tandatangan tidak disalin). Kod: `scripts/lettering/`. Ujian: `designs/lettering/test-6gaya/`.

## 1. Kenapa cubaan lepas belum capai standard

| Punca | Bukti | Tahap |
|---|---|---|
| Model kecil di CPU (klein 4B, ERNIE-Turbo, MOSS), 768×1024, 6–10 min/imej: huruf kurang kemas, salah eja | dataset `model_history`, `lettering_test` (22–23 Nov) | diukur |
| Model percuma terbaik (Qwen-Image-2512) disekat kuota: Space minta 240 s GPU setiap imej, kuota percuma 300 s/hari = 1 imej/hari | ralat Space 23 Nov: "240s requested vs. 80s left" | diukur |
| GPU Kaggle tidak aktif: kernel `pod-typo-gen` (22 & 23 Nov) tiada GPU dan tiada internet | log kernel: `cuda False`, `name resolution` gagal | diukur |
| Ayat Melayu 9–16 perkataan: 92–96% perkataan betul, jarang 100% | dataset `lettering_standard` | lemah (semakan mata) |
| Tiada langkah siap cetak: imej mentah 768×1024 (18×24 in pada 300 DPI perlu 5400×7200) | `lettering_gaps` + kiraan | rasmi (kiraan) |
| Susun font dengan kod sahaja nampak "ditaip"; ditolak pengguna 22 Nov | `model_history` | keputusan pengguna |

## 2. Standard rujukan: 9 ciri QC gaya

QC pintu kekal (SOP 23 Nov, cawangan `sharp-franklin`): G1 ejaan 100%, G2 tiada huruf/perkataan rawak, G3 tiada kecacatan. Kemudian 9 ciri gaya, lulus jika ≥ 8/9:

1. Quote pendek 3–7 perkataan, 3–5 baris.
2. Hierarki: 1–2 perkataan utama sangat besar, perkataan penghubung kecil.
3. Lockup padat satu bentuk (segi empat / bujur), baris bertaut, margin gelap 10–15%.
4. Maksimum 2 jenis huruf: skrip + huruf besar.
5. Swash/ekor huruf mengikat baris (garis bawah, gelung).
6. Latar gelap rata (hitam / biru tua) + dakwat cerah + maksimum 1–2 warna aksen.
7. Hiasan kecil seimbang: titik, bintang, percikan, titisan.
8. Tekstur ikut gaya: rata bersih (S1, S3, S6) atau grain / kapur / lusuh (S2, S4, S5).
9. Masih boleh dibaca pada lakaran kecil Pinterest (~236 px lebar).

| Gaya | Rujukan | Ciri | Palet (dipaksa oleh finish.py) | Tekstur |
|---|---|---|---|---|
| S1 | IMG_5781 | Huruf besar melantun, bertaut, 3 warna, titik konfeti | biru tua + putih, oren, kelabu | tiada |
| S2 | IMG_5778 | Skrip vintaj berswash + huruf besar kecil berselang | hitam + krim | grain |
| S3 | IMG_5732 | Kaligrafi berus condong, swash panjang, percikan | hitam + putih | tiada |
| S4 | IMG_5735 | Berus santai campur besar/kecil | arang + putih kapur | kapur |
| S5 | IMG_5730 | Blok huruf tangan rata kiri-kanan, noktah | hitam + putih | lusuh |
| S6 | IMG_5738 | Skrip monoline + inline + percikan kuning bujur | biru tua + putih, kuning | tiada |

## 3. Alat yang betul (semua percuma, hasil boleh dijual)

| Kerja | Alat | Lesen | Di mana | Status 23 Nov |
|---|---|---|---|---|
| Jana utama | Qwen-Image-2512 + LoRA Lightning 8 langkah (skor LongText-Bench 0.956 dalam jadual kertas LLaDA-Image) | Apache 2.0 (kedua-dua) | GPU T4 Kaggle, percuma | Tunggu anda sahkan telefon Kaggle |
| Jana sandaran | MOSS-Image-SFT 5B + LoRA 8 langkah lodestones | Apache 2.0 (kedua-dua) | CPU container, ~6 min/imej | Dipasang |
| Imej "hero" | Space rasmi Qwen-Image-2512 | Apache 2.0 | ZeroGPU percuma, 1 imej/hari | Ada |
| Betulkan 1 perkataan salah | Qwen-Image-Edit-2511 ("ubah teks X jadi Y, kekal font") | Apache 2.0 | GPU Kaggle | Tunggu telefon Kaggle |
| QC ejaan + gaya | `sheet.py` (helaian semakan) + semakan mata Claude | – | container | Siap |
| Vektor (ganti upscale) | potrace 1.16 melalui `finish.py` | GPL-2.0 (alat sahaja; fail hasil bebas) | container | Siap |
| Palet tepat, susun semula, tekstur, eksport 300 DPI | `finish.py` (OpenCV, scikit-image/scipy, cairosvg) | Apache 2.0 / BSD / LGPL-3.0 | container | Siap |
| Mockup + pin | skrip Pillow/OpenCV (pelan sedia ada) | – | container | Belum |

Tidak dipilih: Ideogram / GPT Image / Recraft (terbaik untuk tulisan tetapi berbayar; pengguna pilih percuma); Ideogram 4 open weights (lesen bukan komersial di Hugging Face); FLUX.2 klein 9B (bukan komersial); Real-ESRGAN (vektor lebih tajam untuk huruf rata); OCR biasa (gagal baca huruf hiasan, ujian 23 Nov).

## 4. Install dalam container (dibuat dan diuji 23 Nov)

```bash
apt-get update && apt-get install -y potrace                     # vektor
pip install vtracer opencv-python-headless scikit-image cairosvg svgelements rapidfuzz \
            huggingface_hub gradio_client kaggle six               # siap cetak + klien Space/Kaggle (~1 min)
pip install diffusers transformers accelerate safetensors sentencepiece  # jana CPU sandaran
# torch datang dari PyPI (~3 GB, binaan CUDA, jalan di CPU); indeks CPU pytorch.org disekat rangkaian.
# Model CPU sandaran (26 GB, muat turun ~10 min): OpenMOSS-Team/MOSS-Image-SFT + lodestones/MOSS-Image-SFT-8-steps-dmd
```

GPU (Kaggle) tidak perlu dipasang dalam container: Claude hantar job melalui `kaggle kernels push`, tunggu, kemudian ambil hasil dengan `kaggle kernels output`. Kredential Kaggle/HF disuntik oleh proxy sesi.

## 5. Workflow

**Sekali sahaja**
1. Anda: sahkan nombor telefon di Kaggle (Settings → Phone verification), ~2 min. Ini buka GPU T4 percuma (anggaran ~30 jam/minggu, angka tidak rasmi) dan internet dalam notebook.
2. Claude: bina dan uji job GPU: Qwen-Image-2512 4-bit + Lightning 8 langkah di T4 (ukur masa dan ingatan). Jika tidak muat atau rosak (T4 tiada bf16), guna MOSS-Image di T4.
3. Claude: simpan skrip setup container (potrace + pip ringan) dalam environment.

**Setiap batch (10 quote)**
1. Claude: tulis 10 quote Inggeris 3–7 perkataan (asli atau domain awam), semak trademark, tetapkan baris + perkataan utama.
2. Claude: bina prompt ikut gaya S1–S6 (`styles.py`).
3. Claude: jana 4 seed setiap quote (GPU Kaggle; sandaran CPU 2 seed).
4. Claude: QC pada helaian semakan (`sheet.py`): G1–G3 + 9 ciri. Gagal → seed baharu (maks 4) → edit perkataan (Qwen-Image-Edit) → tukar perkataan.
5. Claude: `finish.py` → SVG induk + PNG 300 DPI (8×10, 11×14, 16×20, 18×24, 24×36) + pratonton.
6. Anda: lulus / tolak (~5 min).
7. Claude: mockup, pin, upload (langkah Workflow sedia ada).

## 6. Hasil ujian 6 gaya (23 Nov, MOSS-Image di CPU)

Quote baharu "Small steps every day", 6 gaya × 2 seed (42, 7) = 12 imej 768×1024. Masa: purata 438 s/imej (363–529 s), jumlah ~88 min, tanpa GPU. Space Qwen ditolak (kuota). Helaian: `designs/lettering/test-6gaya/sheet.jpg` (atas = AI mentah, bawah = siap cetak).

| Gaya | Ejaan betul | Pilihan | Catatan (semakan mata Claude, bukti lemah) |
|---|---|---|---|
| S1 | 2/2 | s42 | Huruf bulat macam font, kurang "melantun" berbanding rujukan; s7 "EVERY DAY" terlalu rapat (dibaca EVERYDAY jika satu warna) |
| S2 | 2/2 | s42 | Paling hampir rujukan: skrip berswash + huruf kecil berselang |
| S3 | 2/2 | s42 | Swash panjang + percikan baik; hierarki saiz kurang (semua baris hampir sama besar) |
| S4 | 2/2 | s42 | Tekstur kapur asal dibuang semasa vektor, dibina semula oleh finish.py |
| S5 | 2/2 | s42 | Blok rata kiri-kanan + noktah; tekstur lusuh prosedur |
| S6 | 2/2 | s7 | Inline kekal pada s7; pada s42 warna inline tercantum dengan putih |

Siap cetak (finish.py): 7–10 s setiap saiz untuk gaya rata; S2 (grain) 5 saiz dalam 82 s. Saiz fail PNG S2: 8×10 4.8 MB, 18×24 25 MB, 24×36 50 MB (diukur). Tepi huruf licin pada 300 DPI (semakan potongan 1:1).

Kesimpulan: ayat Inggeris pendek = 12/12 ejaan betul walaupun model CPU (ujian Melayu panjang: 92–96% perkataan betul). Langkah siap cetak menyelesaikan saiz cetak. Had sekarang = kelajuan CPU (~8 imej/jam); GPU Kaggle diperlukan untuk Qwen-Image, Qwen-Image-Edit dan batch besar.

## 7. Had dan risiko
- Semakan ejaan dan gaya dibuat dengan mata Claude: tahap bukti lemah.
- Kuota GPU Kaggle mingguan tidak dinyatakan dalam dokumen rasmi (sumber pihak ketiga ~30 jam).
- Hak cipta hasil AI mungkin tidak dilindungi (pesaing boleh tiru); semak trademark frasa sebelum jual.
- Vektor membuang tekstur asal AI; tekstur dibina semula secara prosedur pada saiz cetak.

## Sumber
- Qwen-Image-2512, Z-Image, LongText-Bench: arXiv 2609.03796 (LLaDA-Image), jadual — pihak ketiga. https://arxiv.org/pdf/2609.03796
- MOSS-Image Apache 2.0, LongLongTextBench 96.3 (dakwaan pembuat): https://huggingface.co/OpenMOSS-Team/MOSS-Image-SFT — rasmi (dakwaan sendiri).
- Qwen-Image-Edit sunting teks kekal font: https://qwenlm.github.io/blog/qwen-image-edit/ — rasmi.
- Ideogram 4 open weights, lesen bukan komersial di HF: https://huggingface.co/ideogram-ai/ideogram-4-nf4 — rasmi.
- Lesen model/LoRA disemak melalui API Hugging Face 23 Nov (tag `license:apache-2.0`): Qwen-Image-2512, Qwen-Image-Edit-2511, lightx2v/Qwen-Image-Lightning, MOSS-Image-SFT, lodestones/MOSS-Image-SFT-8-steps-dmd — rasmi.
- Ideogram ketua tipografi 2026: https://invideo.io/blog/best-ai-model-text-in-images/ — pihak ketiga.
- Kuota ZeroGPU (percuma 5 min, PRO 40 min; mesej Space tulis PRO 25 min — bercanggah): https://huggingface.co/docs/hub/spaces-zerogpu — rasmi.
- Kaggle perlu sahkan telefon untuk GPU/internet: https://course.fast.ai/Resources/kaggle.html — pihak ketiga.
- Kuota GPU Kaggle ~30 jam/minggu (tidak rasmi): https://gpuperhour.com/blog/free-cloud-gpus-and-credits — pihak ketiga.
- Printify 300 DPI pada saiz cetak: https://printify.com/knowledge-hub/vector-files-for-print-on-demand/ — rasmi.
