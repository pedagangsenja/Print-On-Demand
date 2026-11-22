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
- **Font**: pautan ke Font Generator, dan senarai induk 1,802 fon bebas untuk jualan, kad 16 mood dengan gambar contoh, carian dan tapisan, laman sumber, jenis lesen dan fon ditolak (data `data/export/fonts/*.json`, dijana oleh `scripts/fonts_fetch.py` → `scripts/build_fonts.py`; gambar `scripts/fonts_specimens.py`; dataset `fonts_*` dalam artifact).
- **Semua produk**: riset semua produk (data `data/export/*.json`).
