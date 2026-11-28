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
