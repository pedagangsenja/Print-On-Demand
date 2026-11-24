# Dashboard riset

Dashboard: https://claude.ai/artifact/EeAC4MqQijSGYGTWfZW3Sg (jenis "Data").

- `index.html`: salinan halaman dashboard (disimpan dalam stor artifact sebagai `files/index.html`).
- Data: `data/export/*.json`, dijana oleh `scripts/export_dashboard.py` dari `data/*.json`, dimuat naik sebagai fail tetap.
- Kemas kini: jalankan `scripts/profit_model.py`, `scripts/build_registry.py`, `scripts/export_dashboard.py`, kemudian muat naik semula fail yang berubah ke artifact.

## Tab

- **Poster** (dibuka dahulu): riset khas poster P1–P8, kalkulator harga dan slider pelawat (data `data/export/posters/*.json`, dijana oleh `scripts/poster_p1.py` … `scripts/poster_p7.py`; dataset `poster_*` dalam artifact).
- **Setup**: checklist 30 langkah (stor dashboard `data/setup/checklist`, dijana oleh `scripts/build_setup.py`); Claude menyemak dan mengemas kini status.
- **Workflow**: tugas harian/mingguan/bulanan anda dan Claude (`data/export/setup/workflow.json`).
- **Aliran design**: aliran 12 langkah (ayat → hitam putih → warna → fail), daftar gaya S (stor `data/gaya/items`, dataset `gaya_daftar`) dan daftar warna C (stor `data/warna/items`, dataset `warna_daftar`) dengan muat naik gambar contoh. Kod: `dashboard/aliran.js`, `dashboard/aliran.css` (fail `files/aliran.js`, `files/aliran.css` dalam artifact).
- **Prestasi**: rangka 5 analisa, corong sasaran 10 jualan/hari × $30, milestone dan alat data (data `data/export/prestasi/*.json`, dijana oleh `scripts/build_prestasi.py`). Angka sebenar diisi bila GA4, Pinterest dan WooCommerce disambung.
- **Semua produk**: riset semua produk (data `data/export/*.json`).
