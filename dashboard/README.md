# Dashboard riset

Dashboard: https://claude.ai/artifact/EeAC4MqQijSGYGTWfZW3Sg (jenis "Data").

- `index.html`: salinan halaman dashboard (disimpan dalam stor artifact sebagai `files/index.html`).
- Data: `data/export/*.json`, dijana oleh `scripts/export_dashboard.py` dari `data/*.json`, dimuat naik sebagai fail tetap.
- Kemas kini: jalankan `scripts/profit_model.py`, `scripts/build_registry.py`, `scripts/export_dashboard.py`, kemudian muat naik semula fail yang berubah ke artifact.

## Tab

- **Poster** (dibuka dahulu): riset khas poster P1–P8, kalkulator harga dan slider pelawat (data `data/export/posters/*.json`, dijana oleh `scripts/poster_p1.py` … `scripts/poster_p7.py`; dataset `poster_*` dalam artifact).
- **Setup**: checklist 30 langkah (stor dashboard `data/setup/checklist`, dijana oleh `scripts/build_setup.py`); Claude menyemak dan mengemas kini status. Bahagian "Alat AI di komputer awan" (dataset `setup_ai_tools`, dijana oleh `scripts/build_ai_tools.py` → `data/export/setup/ai_tools.json`).
- **Workflow**: tugas harian/mingguan/bulanan anda dan Claude (`data/export/setup/workflow.json`).
- **Prestasi**: rangka 5 analisa, corong sasaran 10 jualan/hari × $30, milestone dan alat data (data `data/export/prestasi/*.json`, dijana oleh `scripts/build_prestasi.py`). Angka sebenar diisi bila GA4, Pinterest dan WooCommerce disambung.
- **Model AI**: banding model jana gambar untuk typography poster, cadangan ikut jenis poster, hasil chat lepas, workflow pilih model dan sumber (data `data/export/models/*.json`, dijana oleh `scripts/build_model_ai.py`; dataset `model_*`). Bahagian "Ujian sebenar": 30 imej 3 model dengan gambar (dataset `model_test`, `model_test_models`, `model_test_refs` = gambar rujukan pengguna di kiri, dijana oleh `scripts/build_model_test.py`; gambar kecil di-upload sebagai aset artifact, peta di `designs/model-test/assets.json`). Bahagian "Ujian lettering": 16 imej ayat panjang, 4 cara jana (dataset `lettering_test`, `lettering_test_models`, `lettering_test_refs`, `lettering_gaps`; calc `lettering_summary`; dijana oleh `scripts/build_lettering_test.py` daripada `designs/lettering-test/` review.json, notes.json, gaps.json, assets.json). Bahagian "Ujian ERNIE v2": 10 imej ayat baharu, prompt ikut ciri rujukan, 2 seed (dataset `lettering_v2`, `lettering_v2_models`, `lettering_v2_refs`, `lettering_standard`; calc `lettering_v2_summary`; `build_lettering_test.py thumbs2` / `v2`, fail di `designs/lettering-test/v2/`).
- **Semua produk**: riset semua produk (data `data/export/*.json`).
