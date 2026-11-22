# Serah tugas: design SVG tipografi gaya Etsy (22 Nov 2026)

## Matlamat
Bundle design quote sarkastik hitam-putih (SVG + PNG) gaya bundle Etsy, ayat asli sendiri. Pengguna mahu **percuma** dan Claude sendiri yang jana.

## Keputusan setakat ini
- Susun font percuma dengan kod (`designs/svg-typo/tools/`) dicuba ~10 pusingan: pengguna nilai **tidak profesional**. Jangan ulang cara ini sebagai jalan utama.
- **Berjaya:** AI Qwen-Image-2512 (lesen Apache 2.0) melalui ruang Hugging Face percuma → PNG → SVG dengan potrace. Contoh: `designs/svg-typo/samples/qwen_antisocial.{png,svg}` (ejaan betul, gaya hampir rujukan).

## Cara jana (Hugging Face, sedia berfungsi)
- Token HF disimpan sebagai network secret persekitaran "Interior" untuk `huggingface.co` dan `qwen-qwen-image-2512.hf.space` (pengepala `Authorization` dan `x-hf-authorization`). Skrip guna token palsu; proksi gantikan.
- `pip install gradio_client potracer` → `python3 designs/svg-typo/ai/gen.py prompt.txt out.png` → `python3 -I designs/svg-typo/ai/vec.py out.png out.svg`.
- Templat prompt: `designs/svg-typo/ai/p1.txt`.
- **Had:** kuota ZeroGPU percuma ~5 min/hari dikongsi semua ruang. Qwen-Image-2512 tempah 240 s/design (≈1 sehari). Lebih murah: `multimodalart/Qwen-Image-Fast` (60 s), `Tongyi-MAI/Z-Image-Turbo` (60 s) — perlu secret untuk hos ruang masing-masing.

## Alternatif dikaji
- **Kaggle:** token disimpan (`api.kaggle.com`), notebook `abdulazim1411/pod-typo-gen` dihantar, tetapi GPU+internet tak dibuka (akaun belum sahkan telefon; pengguna sukar sahkan). Skrip: `ai/gen_kernel.py`, `ai/poll.py`.
- **Modal** (22 Nov, dalam proses): pengguna sudah daftar. Klien `modal` tidak boleh dijalankan dari sesi Claude: proksi sesi hanya HTTP/1.1 bila token disuntik, gRPC perlu HTTP/2 ("Connection lost"). Jalan: GitHub Actions `.github/workflows/modal-gen.yml` + `designs/svg-typo/ai/modal_gen.py` (Qwen-Image-2512, H100, cache volume `qwen-image-cache`). Cara guna: tambah `designs/svg-typo/ai/queue/<nama>.txt` (prompt) dan push ke cawangan `claude/**` → PNG+SVG di-commit ke `designs/svg-typo/out/`. Perlu repo secrets `MODAL_TOKEN_ID`, `MODAL_TOKEN_SECRET`. Kos sebenar per design belum diukur.
- **Cloudflare Workers AI:** 10k neuron/hari percuma, Leonardo Phoenix pandai huruf tetapi lesen output belum jelas; FLUX schnell selamat lesen tetapi huruf lemah.
- Recraft: percuma tak boleh dijual; API $0.08/SVG (pengguna tolak berbayar).
- Tak sesuai: Gemini API (tiada kuota gambar percuma 2026), NVIDIA build (ralat akaun percuma), Lightning AI (perlu telefon).

## Peraturan jualan
- Etsy: wajib nyatakan dibuat dengan AI.
- Semak setiap ayat di USPTO (cap dagangan) sebelum jual.
