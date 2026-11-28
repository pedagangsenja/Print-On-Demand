# Dashboard riset

Dashboard: https://claude.ai/artifact/EeAC4MqQijSGYGTWfZW3Sg (jenis "Data").

- `index.html`: salinan halaman dashboard (disimpan dalam stor artifact sebagai `files/index.html`).
- Data: `data/export/*.json`, dijana oleh `scripts/export_dashboard.py` dari `data/*.json`, dimuat naik sebagai fail tetap.
- Kemas kini: jalankan `scripts/profit_model.py`, `scripts/build_registry.py`, `scripts/export_dashboard.py`, kemudian muat naik semula fail yang berubah ke artifact.

## Tab

- **Poster** (dibuka dahulu): riset khas poster P1–P8, kalkulator harga dan slider pelawat (data `data/export/posters/*.json`, dijana oleh `scripts/poster_p1.py` … `scripts/poster_p7.py`; dataset `poster_*` dalam artifact).
- **Setup**: checklist 30 langkah (stor dashboard `data/setup/checklist`, dijana oleh `scripts/build_setup.py`); Claude menyemak dan mengemas kini status.
- **Workflow**: tugas harian/mingguan/bulanan anda dan Claude (`data/export/setup/workflow.json`).
- **Prestasi**: rangka 5 analisa, corong sasaran 10 jualan/hari × $30, milestone dan alat data (data `data/export/prestasi/*.json`, dijana oleh `scripts/build_prestasi.py`). Angka sebenar diisi bila GA4, Pinterest dan WooCommerce disambung.
- **Semua produk**: riset semua produk (data `data/export/*.json`).
- **Etsy**: rujukan gaya penjual Etsy, satu baris setiap design dengan gambar potongan dan 77 lajur dalam 8 paparan (kod `etsy.js`, `etsy.css`; dataset `etsy_designs`, `etsy_listing`, `etsy_fonts`). Analisis tangan di `data/etsy/designs.txt` (lapisan pertama) dan `data/etsy/designs_extra.txt` (saiz baris, gaya ikon, kesan huruf, formula ayat, kunci gaya); `scripts/etsy_crop.py` memotong gambar grid dan mengukur piksel; `scripts/build_etsy.py` membina `data/export/etsy/*.json`; `scripts/etsy_section.py` menjana HTML tab daripada senarai `COLS` dalam `etsy.js`. Gambar potongan tidak dikomit (karya penjual lain); ia disimpan sebagai aset dashboard, id dalam `data/etsy/blobs.txt`. Nota: `files/index.html` kini kira-kira 236 KB daripada had 256 KB setiap dokumen.
- **FC** › sub tab **Design**: carta aliran lettering v1, 9 langkah + baris Tukar model × 6 lajur (Sedia ada · Alat · Cadangan pertama · Alat · Standard v1 · Alat), status alat 25 Nov 2026, butang Penuh / Ringkas; susunan (oren) dan warna (merah jambu) ditonjolkan, dengan butang Tonjol. Dijana oleh `scripts/build_fc_design.py dashboard/index.html dashboard`: isi dan gaya dalam `fc.js` + `fc.css` (stor dashboard menghadkan setiap dokumen kepada 256 KB).
- **AI Image Test**: satu tempat untuk SEMUA imej AI (ujian dan generation). Dataset `ai_all` = `data/export/ai_tests/ai_all.json`, dijana oleh `scripts/build_ai_tests.py` (kod `t2.js`, `t2.css`). Atas: jadual banding model (kiraan `ai_banding`, berubah sendiri). Tengah: grid gambar satu kotak setiap ujian. Jadual belajar: `aturan_belajar` (aturan prompt, `belajar.py`, 3.15) dan `sk_belajar` (skrip SK, `belajar_sk.py`, Belajar SK; upload `data/export/ai_tests/sk_belajar.json` → kemas kini `datasets/sk_belajar`). Bawah: butiran setiap imej + "Info model" (boleh lipat).

## AI Image Test: cara tambah ujian atau generation baharu

1. Tulis `data/ai_tests/rows/Uxx.json` (nombor ujian seterusnya, cth. `U11`): senarai baris, satu baris = satu imej. Lajur wajib:
   `key` (`Uxx|...`, unik), `ujian`, `ujian_nama`, `ujian_nota`, `jenis` (`Ujian` / `Generation`), `standard` (syarat lulus), `tarikh` (YYYY-MM-DD), `model` (kunci asas: `klein4b`, `schnell`, `zturbo`, `ernie`, `moss`, `qwen2512`, `chroma`; model baharu: tambah dalam `MODELS` skrip), `label` (teks atas gambar), `lajur` (tajuk lajur grid, biasanya nama model), `tempat` (`CPU` / `GPU …` / `—`), `kad` + `kad_name` (kumpulan gaya), `ref_img` (`/_blob/…` rujukan atau null), `baris` (cth. `Pendek · seed 42`), `teks`, `seed`, `saat`, `img` (`/_blob/…`), `lulus` (true / false / null untuk design siap), `ejaan` (true / false / null), `gaya` (cth. `7/8` atau ""), `sebab`, `ai` (false untuk imej bukan AI), `bukti` (`lemah` …).
   Pilihan: `rawak`, `cacat`, `teras`, `varian`, `nota`, `tanda` (cth. `★ Final`), `img_siap`, `w`, `h`, `kad_nota`, `ref_nota`.
2. Upload gambar ke artifact dahulu (`asset: true`) untuk dapat url `/_blob/…`.
3. `python3 scripts/build_ai_tests.py` → upload `data/export/ai_tests/ai_all.json` (`asset: true`) → kemas kini `datasets/ai_all` (`source.url` baharu + `updated`) dengan ArtifactData `update` + `if_version`.
4. Jadual banding, ringkasan, grid dan butiran berubah sendiri.

Data lama (sebelum 27 Nov 2026) disalin di `data/ai_tests/raw/` (baris) dan `data/ai_tests/raw/_datasets/` (tajuk dan sumber dataset yang dibuang dari dashboard). Gambar kekal dalam artifact.
