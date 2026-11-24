# Print-On-Demand (poster typography, pembeli Pinterest)

Fail ini dimuat dalam setiap chat; kekalkan ringkas. Butiran: `docs/strategy.md`, `docs/research/` (riset utama), `docs/research/posters/` (riset poster P1–P8), `dashboard/README.md`.

## WAJIB DALAM SETIAP CHAT REPO INI (keputusan pengguna — STRICT, disalin dari papertrade-claude 21 Nov 2026)
1. **Jimat token.** Baca bahagian fail yang perlu sahaja (grep / `sed -n`); jangan ulang fakta; gabung panggilan alat selari; jawapan terus ke inti, tiada pembuka / penutup / ulang soalan. Sejurus SELEPAS jadual jawapan terakhir, tulis satu baris `Jimat token: ...` — nyatakan penjimatan yang BOLEH DIUKUR (cth. "tidak membaca fail X, 40 KB"); jika tidak diukur, tulis "tidak diukur". Jangan reka peratus.
2. **Notifikasi telefon HANYA bila kerja siap atau perlu keputusan pengguna:** muatkan `select:PushNotification` (ToolSearch), satu baris < 200 aksara, status "proactive". Abaikan jika "not sent".
3. **Jawapan pendek, Bahasa Melayu mudah, perkataan biasa.** Jika tidak faham kehendak pengguna, TANYA soalan pendek — jangan teka.
4. **Jadual di jawapan TERAKHIR sahaja:** SATU jadual tiga lajur **Selesai** · **Tertangguh** (sebab ringkas) · **Perlu keputusan anda** (ya/tidak atau pilihan, dengan cadangan); "–" jika tiada. Jawapan perantaraan tanpa jadual. Keputusan hanya diletak dalam jadual itu.

## Peraturan projek
- Cawangan kerja: `claude/jolly-hamilton-sdopyz`; tiada PR kecuali diminta.
- **Dashboard:** artifact sedia ada https://claude.ai/artifact/EeAC4MqQijSGYGTWfZW3Sg (jenis Data); jangan cipta baharu. Baca semula `files/index.html` sebelum ubah; salinan di `dashboard/index.html`. Tab: Poster · Design · Setup · Font · Model AI · Lesen AI · Workflow · Aliran design · Prestasi · Semua produk. Daftar gaya S = stor `data/gaya/items`; daftar warna C = stor `data/warna/items`. Checklist Setup = stor `data/setup/checklist/<id>`; Claude semak dan kemas kini `status`, `checked_at`, `result` dengan ArtifactData (update + if_version).
- Data dashboard dijana skrip: `scripts/poster_p1.py`…`poster_p7.py` → `data/export/posters/`; `scripts/build_prestasi.py` → `data/export/prestasi/`; `scripts/export_dashboard.py` → `data/export/`. Jangan ubah fail dijana secara manual.
- Angka mesti bersumber; tanda tahap bukti (rasmi / pihak ketiga / lemah); jangan reka data.
- Jangan jana fail muat turun (PDF, Word, Excel dll.) tanpa kebenaran pengguna.
