"""Tab dashboard "Model AI": banding model jana gambar untuk typography poster -> data/export/models/*.json.

Riset 23 Nov 2026. Lesen & saiz: Hugging Face API (rasmi). Skor OneIG/LongText: kad model baidu/ERNIE-Image
(rasmi, dilapor pembuat ERNIE). Forum: perbincangan Hugging Face. Blog: carian web (pihak ketiga / lemah).
Reddit, arxiv.org dan artificialanalysis.ai tidak boleh dibaca dari sesi ini (disekat).
Hasil sendiri: cawangan claude/eager-brahmagupta-slpql8 (designs/svg-typo/out/batch*/REVIEW.md).
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data/export/models"
HF = "https://huggingface.co/"

# ---------- 1. Banding model ----------
MK = ["model", "license", "commercial", "run", "ram", "steps", "text_short", "text_long",
      "bw", "color", "bg", "speed", "community", "verdict", "tone", "level", "source"]
MODELS = [
    ("FLUX.2 klein 4B (sekarang)", "Apache 2.0", "Ya", "Container CPU (diuji)", "15 GB fail; GGUF Q8 4.3 GB", "4",
     "Sederhana: 14/20 ayat lulus dalam 4 seed (batch 2), 3/10 (batch 3)",
     "Lemah: perkataan panjang & skrip salah (PATISINCE, LIMTED). Versi 9B: LongText-EN 0.864",
     "Baik: 33 design hitam-putih lulus", "Belum diuji", "Baik, paling laju",
     "~81 s/imej di CPU (diukur 23 Nov, 10 imej)",
     "Blog: paling laju; satu ujian 112 imej: teks Latin 0/4 (Z-Image 4/4)",
     "Simpan: sandaran & latar", "warn", "rasmi", HF + "black-forest-labs/FLUX.2-klein-4B"),
    ("Z-Image-Turbo", "Apache 2.0", "Ya", "Container CPU (diuji 23 Nov, GGUF Q8) + Space percuma", "~10 GB (anggaran)", "8",
     "Kuat: OneIG-EN Text 0.994 (tertinggi dalam jadual ERNIE)",
     "Sederhana: LongText-EN 0.917",
     "Sesuai (blog: ink line art, flat design)", "Kuat", "Kuat: fotorealistik",
     "~280 s/imej di CPU (diukur 23 Nov, 10 imej)",
     "Blog: tajuk 1–5 perkataan biasanya betul; poster padat kadang salah. AI Horde kita: 1 imej salah eja",
     "DIUJI: 6/10 ejaan betul (23 Nov)", "warn", "rasmi", HF + "Tongyi-MAI/Z-Image-Turbo"),
    ("ERNIE-Image-Turbo", "Apache 2.0", "Ya", "Container CPU (diuji 23 Nov, GGUF Q8) + Space percuma", "~8 GB (anggaran)", "8",
     "Kuat: OneIG-EN Text 0.949 (0.967 dengan prompt enhancer)",
     "Kuat: LongText-EN 0.960, tertinggi antara yang muat container",
     "Baik: 5/5 gaya SVG hitam-putih betul (ujian 23 Nov)", "Kuat: blog poster & speech bubble bersih", "Baik",
     "~409 s/imej di CPU (diukur 23 Nov, 10 imej)",
     "Blog ComfyUI: tajuk bersih; perkataan jarang kadang salah ('Barkkins')",
     "DIUJI: 10/10 ejaan betul, terbaik (23 Nov)", "ok", "rasmi", HF + "baidu/ERNIE-Image-Turbo"),
    ("MOSS-Image SFT", "Apache 2.0", "Ya", "Space percuma (CPU terlalu ketat)", "~12 GB (anggaran)", "50 (komuniti 8)",
     "Kuat bila guna kotak susun atur (forum HF: 5/5 kotak tepat)",
     "Kuat: LLTB 96.3 (laporan pembuat)",
     "Baik: poster OK walau prompt pendek (forum HF)", "Baik", "Baik",
     "~80 s/imej di GPU A40, 50 langkah (blog): sangat perlahan di CPU",
     "Ujian bebas 30 poster: 15 tepat. Forum HF 131 imej: prompt pendek rosak pada layout padat",
     "Uji di Space: poster padat", "warn", "pihak_ketiga", HF + "OpenMOSS-Team/MOSS-Image-SFT"),
    ("FLUX.3 Image Klein", "FLUX Kommunity", "Bersyarat: percuma jika jualan < US$5 juta/tahun",
     "Container (stable-diffusion.cpp) + Space percuma", "~9 GB (anggaran)", "16",
     "Ujian bebas 30 poster: 18 tepat (tertinggi dalam ujian itu)", "Tiada data",
     "Belum ada bukti", "Belum ada bukti", "Baik",
     "CPU belum diukur",
     "Kad model sendiri beri amaran teks mungkin salah (blog)",
     "Simpan: baca lesen penuh dahulu", "warn", "pihak_ketiga", HF + "black-forest-labs/flux-3-image-klein"),
    ("Qwen-Image-2512", "Apache 2.0", "Ya", "Space percuma sahaja (~1 imej/hari)", "41 GB: tak muat", "50",
     "Kuat: ujian kita 'antisocial' ejaan betul; blog: tajuk 1–3 perkataan ~70% lulus",
     "Sederhana: LongText-EN 0.956; blog: ayat penuh < 40% lulus",
     "Baik", "Kuat", "Kuat",
     "240 s kuota GPU setiap imej (diukur 22 Nov)",
     "Blog: rancang 2–4 cubaan setiap imej akhir",
     "Design penting sahaja", "warn", "rasmi", HF + "Qwen/Qwen-Image-2512"),
    ("HiDream-O1-Image-Dev", "MIT", "Ya", "Container? (8 GB fp8, jana terus piksel)", "~9 GB (anggaran)", "28",
     "Tiada data", "Kuat: LongText-EN 0.979 (laporan pembuat)",
     "Belum ada bukti", "Belum ada bukti", "Baik",
     "Tiada VAE: dijangka sangat perlahan di CPU (belum diukur)",
     "Sedikit perbincangan komuniti",
     "Simpan: kelajuan tak diketahui", "warn", "pihak_ketiga", HF + "HiDream-ai/HiDream-O1-Image-Dev"),
    ("GLM-Image", "MIT", "Ya", "Tak muat (36 GB, tiada GGUF)", "36 GB", "–",
     "Forum HF: huruf rawak salah", "LongText avg 0.966 (jadual ERNIE)",
     "–", "–", "–", "Forum HF: perlahan",
     "Forum HF: 'slow and ugly', teks lemah dengan diffusers",
     "Tolak", "bad", "pihak_ketiga", HF + "zai-org/GLM-Image"),
    ("SDXL", "OpenRAIL++", "Ya (dengan sekatan guna)", "Container", "~7 GB", "20–30",
     "Lemah", "Lemah", "Sederhana", "Baik", "Baik: banyak LoRA gaya",
     "Ringan, CPU belum diukur", "Model lama (2023); huruf lemah",
     "Latar sahaja (pilihan)", "warn", "rasmi", HF + "stabilityai/stable-diffusion-xl-base-1.0"),
    ("OmniSVG 1.1 4B", "Apache 2.0", "Ya", "Container", "~8 GB (anggaran)", "–",
     "Tiada bukti tipografi", "Tiada bukti", "Terus SVG", "Terus SVG", "–",
     "Belum diukur", "Tiada ujian tipografi ditemui",
     "Belum matang untuk tipografi", "bad", "lemah", HF + "OmniSVG/OmniSVG1.1_4B"),
    ("Ditolak: FLUX.2 klein 9B / FLUX.2 dev", "FLUX Non-Commercial", "Tidak", "–", "–", "–",
     "–", "–", "–", "–", "–", "–", "Hasil tak boleh dijual", "Tolak", "bad", "rasmi",
     HF + "black-forest-labs/FLUX.2-klein-9B"),
    ("Ditolak: Qwen-Image-2.1", "qwen-research", "Tidak", "–", "–", "–",
     "–", "–", "–", "–", "–", "–", "Lesen penyelidikan sahaja", "Tolak", "bad", "rasmi", HF + "Qwen/Qwen-Image-2.1"),
    ("Ditolak: Ideogram 4.0 (terbuka)", "Berat bukan komersial", "Tidak", "–", "–", "–",
     "Kuat (blog)", "–", "–", "–", "–", "–", "Sumber bercanggah tentang lesen; nota lama: bukan komersial",
     "Tolak", "bad", "pihak_ketiga", "https://www.3daistudio.com/blog/ideogram-4-open-image-model-explained"),
    ("Ditolak: MiniMax-H3 / Cosmos3 / P-Image / Krea-2", "Komuniti / lain-lain", "Bersyarat / tak jelas", "Tak muat", "33–200 GB", "–",
     "–", "–", "–", "–", "–", "–", "Terlalu besar untuk container (12.8B–64.6B)",
     "Tolak", "bad", "rasmi", HF + "MiniMaxAI/MiniMax-H3-Image"),
    ("Ditolak: tessera-small", "CC-BY-NC 4.0", "Tidak", "–", "–", "–",
     "–", "–", "–", "–", "–", "–", "Bukan komersial", "Tolak", "bad", "rasmi", HF + "thejagstudio/tessera-small"),
]

# ---------- 2. Cadangan ikut jenis poster ----------
UK = ["kind", "main", "backup", "process", "why"]
USECASES = [
    ("Quote hitam-putih pendek (1–6 perkataan)", "Z-Image-Turbo (selepas ujian)", "FLUX.2 klein 4B (terbukti 33 design)",
     "4 seed → Tesseract semak ejaan → potrace/vtracer SVG",
     "Skor huruf pendek Z-Image tertinggi (OneIG 0.994); klein sudah terbukti tetapi gagal pada perkataan panjang/skrip"),
    ("Quote hitam-putih panjang / banyak baris", "ERNIE-Image-Turbo", "MOSS-Image (Space, kotak susun atur)",
     "4 seed → Tesseract → SVG; ayat gagal 4× = pecah baris atau tukar ayat",
     "LongText-EN ERNIE-Turbo 0.960 vs klein 9B 0.864; batch 3 klein hanya 3/10 lulus terus"),
    ("Typography berwarna (retro, pastel, art deco)", "ERNIE-Image-Turbo", "Z-Image-Turbo; Qwen-Image-2512 (Space) untuk design penting",
     "Jana PNG → Real-ESRGAN 4× untuk cetak",
     "Blog: ERNIE tajuk & poster berwarna bersih; warna tak boleh jadi SVG bersih seperti hitam-putih"),
    ("Poster dengan latar gambar + tulisan", "Hibrid: AI jana latar TANPA teks + tulisan guna font berlesen",
     "Latar: FLUX.2 klein 4B atau Z-Image-Turbo",
     "AI latar → enjin poster ornate (cawangan intelligent-bell) letak teks, gelapkan zon teks → eksport",
     "Ejaan 100% tepat; font komersial disemak di tab Font; blog cetak (Overnight Prints, Recraft) syor cara ini"),
    ("Teks mesti tepat 100% (nama, wordmark, harga)", "Susun font sebenar (hibrid)", "–",
     "AI untuk hiasan sahaja",
     "Forum HF MOSS: 'menamakan typeface tidak memuatkan font' — huruf AI cuma tiru gaya"),
]

# ---------- 3. Hasil chat lepas (recall) ----------
HK = ["date", "what", "images", "designs", "result", "lesson"]
HISTORY = [
    ("22 Nov", "Susun font dengan kod (~10 pusingan)", 0, 0, "Anda nilai tidak profesional", "Jangan jadikan cara utama"),
    ("22 Nov", "Qwen-Image-2512 di Space HF percuma", 1, 1, "'antisocial' ejaan betul", "Bagus tetapi kuota ~1 imej/hari"),
    ("22 Nov", "Modal & Kaggle (GPU)", 0, 0, "Modal perlu kad; Kaggle perlu sahkan telefon", "Tidak digunakan"),
    ("22 Nov", "AI Horde: Z-Image-Turbo", 1, 0, "825 s; ejaan salah ('TALK ME')", "Barisan percuma terlalu lambat"),
    ("22 Nov", "FLUX.2 klein 4B di CPU: ujian awal", 2, 1, "coffee betul; antisocial salah", "Jana 3–4 seed setiap ayat"),
    ("22 Nov", "Batch 1: 5 quote × 3 seed", 15, 3, "5/15 imej lulus ejaan", "Perkataan panjang/skrip mudah salah"),
    ("22 Nov", "Mod edit klein untuk betulkan ejaan", 1, 0, "Gagal: ejaan tidak berubah", "Betulkan = seed baharu / tukar ayat"),
    ("22 Nov", "Batch 2: 20 quote × 4 seed + 2 pusingan baiki", 104, 20, "14/20 lulus terus; 6 tukar ayat → 20/20", "Tukar perkataan sukar (Tomorrow → Later)"),
    ("22 Nov", "Batch 3: 10 quote gaya skrip/bingkai/padat", 72, 10, "3/10 lulus terus; 10/10 selepas baiki (1 dibaiki tangan)", "Gaya skrip & padat paling sukar untuk klein"),
    ("22 Nov", "Enjin poster ornate hibrid (cawangan lain)", 0, 0, "Latar AI + tipografi font + emas timbul", "Asas untuk poster berlatar"),
    ("23 Nov", "Mod poster motivasi 864×1152 + 30 quote", 0, 0, "Disediakan, belum dijana", "Sedia untuk ujian model baharu"),
]

# ---------- 4. Workflow pilih model ----------
WK = ["no", "who", "step", "detail", "status"]
WORKFLOW = [
    (1, "Anda", "Luluskan bina stable-diffusion.cpp", "Perlu untuk Z-Image-Turbo & ERNIE-Image-Turbo di container", "Perlu keputusan"),
    (2, "Claude", "Pasang & muat turun model", "GGUF Z-Image-Turbo + ERNIE-Image-Turbo, simpan klein 4B", "Belum"),
    (3, "Anda", "Pilih 10 ayat ujian", "5 hitam-putih pendek, 3 panjang, 2 berwarna (boleh guna 30 quote motivasi)", "Belum"),
    (4, "Container", "Jana 4 seed × 10 ayat × 3 model", "120 imej, saiz & langkah sama; masa setiap imej diukur", "Belum"),
    (5, "Container", "Tesseract semak ejaan", "Imej salah eja dibuang automatik", "Belum"),
    (6, "Claude", "Skor & kemas kini tab ini", "Ejaan, boleh baca, gaya, sedia cetak (0–8) + masa", "Belum"),
    (7, "Anda", "Pilih gaya terbaik", "Lihat contact sheet setiap model", "Belum"),
    (8, "Claude", "Tetapkan model ikut jenis poster", "Kemas kini jadual cadangan + setup script", "Belum"),
    (9, "Claude", "(Pilihan) Uji MOSS & Qwen di Space percuma", "3 ayat paling sukar sahaja (kuota terhad)", "Belum"),
]

# ---------- 5. Sumber ----------
SK = ["source", "kind", "used_for", "level", "url"]
SOURCES = [
    ("Hugging Face API: lesen, saiz, tarikh", "Rasmi", "Semua model", "rasmi", HF + "models"),
    ("Kad model ERNIE-Image: jadual OneIG & LongText", "Rasmi (dilapor Baidu)", "Skor tulisan", "rasmi", HF + "baidu/ERNIE-Image"),
    ("stable-diffusion.cpp README & docs", "Rasmi", "Sokongan CPU, komponen", "rasmi", "https://github.com/leejet/stable-diffusion.cpp"),
    ("Forum HF MOSS #16: 131 imej, 8 adegan", "Forum", "MOSS tulisan & susun atur", "pihak_ketiga", HF + "OpenMOSS-Team/MOSS-Image-SFT/discussions/16"),
    ("Forum HF MOSS #20: 6 kotak", "Forum", "MOSS kotak susun atur", "pihak_ketiga", HF + "OpenMOSS-Team/MOSS-Image-SFT/discussions/20"),
    ("Forum HF GLM-Image #6, #14", "Forum", "GLM-Image ditolak", "pihak_ketiga", HF + "zai-org/GLM-Image/discussions/6"),
    ("Forum HF klein 4B #13: jalan di laptop CPU", "Forum", "klein CPU", "pihak_ketiga", HF + "black-forest-labs/FLUX.2-klein-4B/discussions/13"),
    ("minimalcorp: klein vs Z-Image Turbo, 112 imej", "Blog", "Teks Latin 0/4 vs 4/4", "lemah", "https://tech.minimalcorp.com/en/posts/flux2-klein-vs-z-image-turbo"),
    ("runaihome: Z-Image-Turbo vs klein", "Blog", "Kelajuan & teks", "lemah", "https://runaihome.com/blog/z-image-turbo-16gb-vram-home-lab-image-gen-2026/"),
    ("Cybernews: ulasan Z-Image", "Blog", "Poster padat kadang salah", "lemah", "https://cybernews.com/ai-tools/z-image-ai-image-generator-review/"),
    ("note.com JSCDISK: ERNIE-Image Turbo", "Blog", "Teks ERNIE", "lemah", "https://note.com/jscdisk/n/n2c1150cfd857?hl=en"),
    ("sonusahani: ERNIE Turbo vs FLUX", "Blog", "'Barkkins' salah", "lemah", "https://sonusahani.com/blogs/ernie-image"),
    ("Silicium Rose: MOSS vs Z-Image, FLUX", "Blog", "Ujian 30 poster", "lemah", "https://siliciumrose.com/articles/moss-image-vs-z-image-flux-sdxl-krea-2.html"),
    ("inferencekey: MOSS-Image 80 s", "Blog", "Kelajuan MOSS", "lemah", "https://inferencekey.com/news/moss-image-open-text-rendering"),
    ("VentureBeat: FLUX.3 Klein lesen < $5M", "Berita", "Lesen FLUX.3", "pihak_ketiga", "https://venturebeat.com/technology/black-forest-labs-opens-flux-3-image-klein-weights-with-free-commercial-use-limited-to-smaller-businesses"),
    ("WaveSpeed: Qwen-Image-2512 teks", "Blog", "Kadar lulus Qwen", "lemah", "https://wavespeed.ai/blog/posts/qwen-image-2512-text-rendering/"),
    ("Overnight Prints: AI untuk poster", "Blog", "Cara hibrid", "lemah", "https://blog.overnightprints.com/?p=17565"),
    ("Recraft: design poster dengan AI", "Blog", "Cara hibrid", "lemah", "https://www.recraft.ai/blog/how-to-design-a-poster-with-ai"),
    ("Ujian sendiri batch 1–3 (cawangan eager-brahmagupta)", "Diukur sendiri", "Hasil klein 4B", "rasmi", ""),
]


def dump(name, keys, rows):
    data = [dict(zip(keys, r)) for r in rows]
    (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    return len(data)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, keys, rows in [("model_compare", MK, MODELS), ("model_usecase", UK, USECASES),
                             ("model_history", HK, HISTORY), ("model_workflow", WK, WORKFLOW),
                             ("model_sources", SK, SOURCES)]:
        assert all(len(r) == len(keys) for r in rows), name
        print(name, dump(name, keys, rows))


if __name__ == "__main__":
    main()
