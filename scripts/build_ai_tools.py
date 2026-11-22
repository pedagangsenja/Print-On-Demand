"""Alat AI untuk komputer awan (container sesi Claude Code) -> data/export/setup/ai_tools.json.

Lesen disemak 22 Nov 2026: Hugging Face API (tag `license:`) untuk model, PyPI JSON untuk pakej.
Container: 4 teras CPU, 15 GB RAM, tiada GPU (diukur dalam sesi: nproc, free -g, nvidia-smi tiada).
"""
import json
from pathlib import Path

HF = "https://huggingface.co/"
PYPI = "https://pypi.org/project/"

# kerja, alat, lesen, bukti, sumber, percuma, muat, status, nota
ROWS = [
    ("Jana gambar", "FLUX.2 klein 4B", "Apache 2.0", "rasmi (Hugging Face)", HF + "black-forest-labs/FLUX.2-klein-4B",
     "Ya", "Ya (diuji 22 Nov)", "Perlu pasang semula",
     "~3.5 min/gambar 1024² di 4 teras (diukur). Kadang salah eja: jana 3-4 seed. Muat turun ~15 GB setiap sesi baharu."),
    ("Jana gambar", "Z-Image-Turbo (GGUF)", "Apache 2.0", "rasmi (Hugging Face)", HF + "Tongyi-MAI/Z-Image-Turbo",
     "Ya", "Ya, melalui stable-diffusion.cpp", "Belum dipasang",
     "6.2B parameter. Lebih pandai tulis huruf. Program stable-diffusion.cpp perlu dibina; perlu kebenaran anda. Kelajuan belum diukur."),
    ("Semak ejaan", "Tesseract OCR (pytesseract)", "Apache 2.0", "rasmi (PyPI)", PYPI + "pytesseract/",
     "Ya", "Ya, ringan", "Belum dipasang",
     "Baca tulisan dalam gambar, pilih seed yang ejaannya betul secara automatik."),
    ("Upscale", "vtracer", "MIT", "rasmi (PyPI)", PYPI + "vtracer/",
     "Ya", "Ya, ringan", "Belum dipasang",
     "Tukar ke vektor (SVG): cetak sebesar mana pun tanpa kabur. Terbaik untuk poster huruf."),
    ("Upscale", "Real-ESRGAN x4", "BSD-3 (PyPI juga tulis Apache)", "rasmi (PyPI)", PYPI + "realesrgan/",
     "Ya", "Ya, perlahan tanpa GPU", "Belum dipasang",
     "Untuk poster bertekstur. Kedua-dua lesen benarkan guna komersial. Kelajuan belum diukur."),
    ("Buang latar", "rembg + BiRefNet", "MIT", "rasmi (PyPI, Hugging Face)", HF + "ZhengPeng7/BiRefNet",
     "Ya", "Ya, ringan", "Belum dipasang", "Buang latar belakang gambar."),
    ("Mockup", "Skrip Python (Pillow/OpenCV)", "Bebas (sumber terbuka)", "rasmi", PYPI + "pillow/",
     "Ya", "Ya", "Belum dibuat",
     "Tak perlu AI. Foto bilik mesti milik sendiri atau berlesen komersial."),
    ("Teks / SEO", "Claude (sesi ini)", "–", "–", "",
     "Termasuk pelan Claude", "Tak perlu pasang", "Sedia",
     "Tajuk, deskripsi dan tag Pinterest. Lebih cepat dan baik daripada model kecil yang dipasang sendiri."),
    ("Tak muat", "Qwen-Image-2512", "Apache 2.0", "rasmi (Hugging Face)", HF + "Qwen/Qwen-Image-2512",
     "Ya", "Tidak", "Tidak sesuai",
     "20.4B parameter: perlu lebih 15 GB RAM."),
    ("Ditolak", "FLUX.2 klein 9B", "FLUX Non-Commercial", "rasmi (Hugging Face)", HF + "black-forest-labs/FLUX.2-klein-9B",
     "Percuma tapi tak boleh jual", "–", "Ditolak", "Hasil tak boleh dijual."),
]

KEYS = ["job", "tool", "license", "evidence", "source", "free", "fits", "status", "note"]


def main():
    out = Path(__file__).resolve().parent.parent / "data/export/setup/ai_tools.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = [dict(zip(KEYS, r)) for r in ROWS]
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n")
    print(out, len(rows))


if __name__ == "__main__":
    main()
