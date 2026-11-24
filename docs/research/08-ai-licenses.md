# Lesen komersial, kuota GPU dan VRAM: model jana imej di Hugging Face

Semakan 2026-11-24. Dijana oleh `scripts/build_ai_licenses.py` (jangan ubah manual).
Sumber: fail LICENSE / model card di HF (rasmi), `app.py` setiap Space (rasmi), dokumen ZeroGPU https://huggingface.co/docs/hub/spaces-zerogpu (rasmi).

## Kuota ZeroGPU sehari

- Tanpa log masuk: 2 minit. Keutamaan barisan rendah
- Free: 5 minit. Akaun anda. Diset semula 24 jam selepas kali pertama guna
- PRO: 40 minit. $9/bulan. Boleh lebih guna kredit: $1 setiap 10 minit
- Team: 40 minit. Ahli organisasi Team
- Enterprise: 60 minit. Ahli organisasi Enterprise
- Saiz `large` (48 GB) kira 1×, `xlarge` (96 GB) kira 2×. Tanpa `duration`, Space minta 60 s.
- Gambar/hari = paling kurang gambar 1024² untuk akaun Free (300 s) = kuota ÷ (masa GPU maksimum Space × saiz). Kuota ditolak ikut masa sebenar, jadi biasanya lebih.
- VRAM "agg." = anggaran 2 GB setiap 1B parameter (BF16); lain-lain daripada model card.

## Jadual

| Model | Saiz | Komersial? | Lesen | Had / syarat | Kegunaan | Space | GPU / gambar | Gambar/hari (Free) | VRAM | Cadangan |
|---|---|---|---|---|---|---|---|---|---|---|
| **A. Bebas komersial** | | | | | | | | | | |
| [ERNIE-Image-Turbo](https://huggingface.co/baidu/ERNIE-Image-Turbo) | 8B | Ya | Apache 2.0 | Tiada | Poster, infografik, teks padat dan panjang. 8 langkah | baidu/ERNIE-Image-Turbo (CPU + API Baidu, maks 10 serentak). Alternatif: akhaliq/ERNIE-Image-Turbo 120 s | Tiada kuota GPU HF (Space rasmi) | – | 24 GB | Pilihan utama |
| [ERNIE-Image](https://huggingface.co/baidu/ERNIE-Image) | 8B | Ya | Apache 2.0 | Tiada | Versi penuh 50 langkah, ikut arahan lebih tepat | Tiada Space khusus | — | – | 24 GB | Boleh guna |
| [Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) | 6B | Ya | Apache 2.0 | Tiada | Laju (8 langkah), teks Inggeris dan Cina | Tongyi-MAI/Z-Image-Turbo, mrfakename/Z-Image-Turbo | 60 s · large | ≥5 | 16 GB | Sandaran terbaik |
| [Z-Image](https://huggingface.co/Tongyi-MAI/Z-Image) | 6B | Ya | Apache 2.0 | Tiada | Versi penuh Z-Image (bukan Turbo) | Tongyi-MAI/Z-Image | 60 s · large | ≥5 | ~16 GB (agg., saiz sama Turbo) | Boleh guna |
| [Qwen-Image-2512](https://huggingface.co/Qwen/Qwen-Image-2512) | 20B | Ya | Apache 2.0 | Tiada | Teks dalam gambar lebih tepat (Dis 2025), poster | Qwen/Qwen-Image-2512 | 120 s · xlarge (2×) | ≥1 | ~40 GB+ (agg.) | Kualiti tinggi, kuota mahal |
| [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) | 20B | Ya | Apache 2.0 | Tiada | Teks kompleks dalam gambar (Cina/Inggeris), edit | Qwen/Qwen-Image | 120 s · large | ≥2 | ~40 GB+ (agg.) | Boleh guna |
| [Qwen-Image-Fast (Qwen-Image + Lightning LoRA)](https://huggingface.co/lightx2v/Qwen-Image-Lightning) | 20B | Ya | Apache 2.0 (semua komponen) | Tiada | Versi laju Qwen-Image | mcp-tools/Qwen-Image-Fast | 40 s · xlarge (2×) | ≥3 | ~40 GB+ (agg.) | Qwen paling jimat kuota |
| [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) | 20B | Ya | Apache 2.0 | Tiada | Edit gambar | Qwen/Qwen-Image-Edit-2511 | 180 s · large | ≥1 | ~40 GB+ (agg.) | Boleh guna |
| [MOSS-Image (SFT)](https://huggingface.co/OpenMOSS-Team/MOSS-Image-SFT) | 5B | Ya | Apache 2.0 | Tiada | Kawal letak teks guna JSON | OpenMOSS-Team/MOSS-Image | 80 s · large | ≥3 | ~10 GB+ (agg.) | Boleh guna |
| [MOSS-Image 8 langkah (DMD)](https://huggingface.co/lodestones/MOSS-Image-SFT-8-steps-dmd) | 5B | Ya | Apache 2.0 | Model masih dalam ujian (work-in-progress) | Versi laju MOSS-Image | hugging-apps/moss-image-8-step-dmd | 16 s · large | ≥18 | ~20 GB+ (agg., transformer wajib FP32) | Paling banyak gambar/hari, masih ujian |
| [FLUX.2 [klein] 4B](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B) | 4B | Ya | Apache 2.0 | Tiada | Sangat laju (4 langkah), edit guna beberapa gambar rujukan | black-forest-labs/FLUX.2-klein-4B | 95 s · large | ≥3 | 13 GB | Laju, VRAM paling rendah |
| [FLUX.1 [schnell]](https://huggingface.co/black-forest-labs/FLUX.1-schnell) | 12B | Ya | Apache 2.0 | Tiada | Laju (4 langkah) | black-forest-labs/FLUX.1-schnell | 70 s · large | ≥4 | ~24 GB+ (agg.) | Boleh guna |
| [GLM-Image](https://huggingface.co/zai-org/GLM-Image) | 7B decoder | Ya | MIT | Tiada | Pengekod khas huruf (Glyph Encoder), teks tepat | multimodalart/GLM-Image | 120 s · large | ≥2 | ~23 GB (dengan offload CPU) | Alternatif untuk teks |
| [HiDream-I1-Full](https://huggingface.co/HiDream-ai/HiDream-I1-Full) | 17B | Ya | MIT | Perlu terima lesen Llama 3.1 juga (pengekod teks) | Jana imej umum | Tiada Space khusus | — | – | ~34 GB+ (agg.) | Boleh guna |
| [Chroma](https://huggingface.co/lodestones/Chroma) | 8.9B | Ya | Apache 2.0 | Tiada | Seni, anime, foto. Tiada penapis kandungan | gokaygokay/Chroma | 60 s · large | ≥5 | ~18 GB (agg.) | Boleh guna |
| [Flex.1-alpha](https://huggingface.co/ostris/Flex.1-alpha) | 8B | Ya | Apache 2.0 | Tiada | Model asas untuk latih LoRA | ostris/Flex.1-alpha | 75 s · large | ≥4 | ~16 GB+ (agg.) | Boleh guna |
| [AuraFlow](https://huggingface.co/fal/AuraFlow) | 6.8B | Ya | Apache 2.0 | Tiada | Jana imej umum (2024) | gokaygokay/AuraFlow-with-Captioner | 100 s · large | ≥3 | ~14 GB+ (agg.) | Boleh guna |
| [FireRed-Image-Edit-1.0](https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.0) | 20B | Ya | Apache 2.0 | Tiada | Edit gambar | Tiada Space rasmi | — | – | ~40 GB+ (agg.) | Boleh guna |
| [SDXL base 1.0 / SDXL-Lightning](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) | 2.6B | Ya | OpenRAIL++ | Dilarang guna untuk tujuan berbahaya | Jana imej umum. Teks lemah | ByteDance/SDXL-Lightning | 60 s · large | ≥5 | ~6 GB+ (agg.) | Boleh guna |
| **B. Komersial bersyarat** | | | | | | | | | | |
| [FLUX 3 Image Klein](https://huggingface.co/black-forest-labs/flux-3-image-klein) | 5.5B | Ya | FLUX Kommunity v1.0 | Hasil < US$5 juta setahun. Wajib penapis atau semak hasil. Label AI jika undang-undang mewajibkan. Jangan guna hasil untuk latih model lain. Lesen boleh ditarik | Edit dan jana, teks dalam gambar, susun atur kotak | black-forest-labs/flux-3-image-klein | 33 s · large | ≥9 | 31 GB BF16 / 26 GB FP8 / 25 GB NVFP4 (+28 GB alat prompt) | Boleh: semak hasil + label AI |
| [SD 3.5 Large / Large Turbo / Medium](https://huggingface.co/stabilityai/stable-diffusion-3.5-large) | 8.1B / 8.1B / 2.5B | Ya | Stability Community | Hasil < US$1 juta setahun. Wajib daftar dengan Stability. Jangan guna hasil untuk latih model asas lain | Jana imej umum | stabilityai/stable-diffusion-3.5-large (Turbo 60 s) | 65 s · large | ≥4 | Large ~16 GB+, Medium ~5 GB+ (agg.) | Boleh, ikut syarat |
| [SDXL-Turbo](https://huggingface.co/stabilityai/sdxl-turbo) | 2.6B | Ya | Stability Community (label HF: sai-nc-community) | Hasil < US$1 juta setahun. Wajib daftar dengan Stability | Sangat laju (1–4 langkah) | diffusers/unofficial-SDXL-Turbo-i2i-t2i | 60 s · large | ≥5 | ~6 GB+ (agg.) | Boleh, ikut syarat |
| [Krea 2 (Turbo / Raw)](https://huggingface.co/krea/Krea-2-Turbo) | 12B | Ya | Krea 2 Community | Hasil < US$1 juta (12 bulan lepas). Notis atribusi jika edar model. Raw tidak disyorkan untuk jana | Gaya estetik, ada koleksi LoRA | krea/Krea-2 (8 langkah) | 41 s · xlarge (2×) | ≥3 | ~24 GB+ (agg.) | Boleh, ikut syarat |
| [Kolors](https://huggingface.co/Kwai-Kolors/Kolors) | 2.6B | Ya | Apache 2.0 + Model License | Wajib isi borang dan emel Kuaishou sebelum guna komersial. > 100 juta pengguna sebulan perlu lesen | Foto realistik, teks Cina dan Inggeris | Kwai-Kolors/Kolors | 60 s · large | ≥5 | ~5 GB+ (agg.) | Boleh selepas daftar |
| [Playground v2.5](https://huggingface.co/playgroundai/playground-v2.5-1024px-aesthetic) | 2.6B | Ya | Playground Community | Perlu lesen jika jana imej bisnes teras DAN > 1 juta pengguna sebulan. Jangan guna hasil untuk latih model lain | Gambar estetik | playgroundai/playground-v2.5 | 60 s · large | ≥5 | ~6 GB+ (agg.) | Boleh, ikut syarat |
| [HunyuanImage 3.0](https://huggingface.co/tencent/HunyuanImage-3.0) | 80B MoE (13B aktif) | Ya | Tencent Hunyuan Community | Tidak sah di EU, UK dan Korea Selatan. > 100 juta pengguna sebulan perlu lesen | Jana imej kualiti tinggi | akhaliq/HunyuanImage-3.0 (CPU, perlu akaun PRO) | Perlu PRO | – | ~160 GB (agg., README guna 4 GPU) | Terlalu besar untuk anda |
| [HunyuanImage 2.1](https://huggingface.co/tencent/HunyuanImage-2.1) | — | Ya | Tencent Hunyuan Community | Tidak sah di EU, UK dan Korea Selatan. > 100 juta pengguna sebulan perlu lesen | Jana imej 2K | Tiada Space khusus | — | – | 24 GB (FP8, gambar 2K) | Boleh, ikut syarat |
| **C. Bukan komersial** | | | | | | | | | | |
| [FLUX.2 [dev]](https://huggingface.co/black-forest-labs/FLUX.2-dev) | 32B | Tidak | FLUX Non-Commercial v2.1 | Model hanya untuk bukan komersial (jual hasil = bayaran tidak langsung). Lesen komersial: bfl.ai/licensing | Jana dan edit | black-forest-labs/FLUX.2-dev | 75 s · xlarge (2×) | ≥2 | RTX 4090 dengan 4-bit + pengekod teks jauh | Elak untuk jualan |
| [FLUX.2 [klein] 9B](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B) | 9B | Tidak | FLUX Non-Commercial v2.1 | Model hanya untuk bukan komersial | Jana dan edit, laju | black-forest-labs/FLUX.2-klein-9B | 95 s · xlarge (2×) | ≥1 | 29 GB | Elak untuk jualan |
| [FLUX.1 [dev]](https://huggingface.co/black-forest-labs/FLUX.1-dev) | 12B | Tidak | FLUX.1 Non-Commercial | Model hanya untuk bukan komersial | Jana imej | black-forest-labs/FLUX.1-dev | 75 s · large | ≥4 | ~24 GB+ (agg.) | Elak untuk jualan |
| [FLUX.1 Kontext [dev]](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev) | 12B | Tidak | FLUX.1 Non-Commercial | Model hanya untuk bukan komersial | Edit gambar | black-forest-labs/FLUX.1-Kontext-Dev | 70 s · large | ≥4 | ~24 GB+ (agg.) | Elak untuk jualan |
| [Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) | 7B | Tidak | Qwen Research | Penyelidikan dan penilaian sahaja. Komersial perlu lesen berasingan | Gambar latar lutsinar (RGBA), jana dan edit | Qwen/Qwen-Image-2.1 | 25 s · large | ≥12 | ~14 GB+ (agg.) | Elak untuk jualan |
| [Ideogram 4](https://huggingface.co/ideogram-ai/ideogram-4-fp8) | 9.3B | Tidak | Ideogram Non-Commercial | Jelas melarang guna hasil untuk produk berbayar atau iklan | Teks terbaik antara model terbuka (dakwaan pembuat) | ideogram-ai/ideogram4 (minimum 60 s) | 60 s · xlarge (2×) | ≥2 | ~9 GB+ FP8 (agg.) | Elak untuk jualan |
| [Bria Fibo 2.0 dev](https://huggingface.co/briaai/Fibo-2.0-dev) | 8B | Tidak | CC BY-NC 4.0 | Bukan komersial | Edit dan jana dalam satu model | briaai/Fibo-2.0-T2I | 120 s · large | ≥2 | ~16 GB+ (agg.) | Elak untuk jualan |
