# Print-On-Demand (poster typography, pembeli Pinterest)

Fail ini dimuat dalam setiap chat; kekalkan ringkas. **SEMUA peraturan dalam fail ini WAJIB (keputusan pengguna 24 Nov 2026).** Butiran: `docs/strategy.md`, `docs/research/` (riset utama), `docs/research/posters/` (riset poster P1–P8), `dashboard/README.md`.

## WAJIB DALAM SETIAP CHAT REPO INI (keputusan pengguna — STRICT, disalin dari papertrade-claude 21 Nov 2026)
1. **Jimat token.** Baca bahagian fail yang perlu sahaja (grep / `sed -n`); jangan ulang fakta; gabung panggilan alat selari; jawapan terus ke inti, tiada pembuka / penutup / ulang soalan. Sejurus SELEPAS jadual jawapan terakhir, tulis satu baris `Jimat token: ...` — nyatakan penjimatan yang BOLEH DIUKUR (cth. "tidak membaca fail X, 40 KB"); jika tidak diukur, tulis "tidak diukur". Jangan reka peratus.
2. **Notifikasi telefon WAJIB di hujung SETIAP jawapan** (setiap kali selesai menjawab, tanpa kecuali; peraturan pengguna 24 Nov 2026): muatkan `select:PushNotification` (ToolSearch), panggil sebagai alat TERAKHIR sebelum teks jawapan akhir — satu baris < 200 aksara (apa siap / apa perlu keputusan), status "proactive". Abaikan jika "not sent".
3. **Jawapan pendek, Bahasa Melayu mudah, perkataan biasa.** Jika tidak faham kehendak pengguna, TANYA soalan pendek — jangan teka.
4. **Jadual di jawapan TERAKHIR sahaja:** SATU jadual tiga lajur **Selesai** · **Tertangguh** (sebab ringkas) · **Perlu keputusan anda** (ya/tidak atau pilihan, dengan cadangan); "–" jika tiada. Jawapan perantaraan tanpa jadual. Keputusan hanya diletak dalam jadual itu.
5. **Selepas SETIAP kali jana imej AI (peraturan penting, 24 Nov 2026):** terus di bawah jadual hasil, TANYA pengguna dahulu untuk SEMUA imej batch itu — jangan simpan sebelum dijawab:
   **A** = simpan di tab **AI Image Test** dashboard (dataset `ai_all`, satu baris = satu imej; cara tambah: `dashboard/README.md`), atau
   **SNC** = daftar di tab **Daftar S/C**: gaya **S** (stor `data/gaya/items`) + warna **C** (stor `data/warna/items`).
   Pengguna padam sendiri yang tidak mahu dalam Daftar S/C. Tujuan: design bagus tidak hilang.
6. **Like (♥) gambar (keputusan pengguna 27 Nov 2026):** setiap gambar dashboard ada butang ♥; like disimpan di stor `data/likes/items/<id blob>` (dataset `likes`, tab **♥ Disukai**; editor sahaja). SEBELUM jana imej AI, baca stor ini (ArtifactData list) dan utamakan model / gaya / warna / teks yang di-like. Gambar baharu mesti guna `POD.likeOn(host, src, info)` (`files/suka.js`).
7. **Aturan prompt belajar selepas SETIAP jana (keputusan pengguna 27 Nov 2026):** selepas QC setiap batch imej AI, ikut `docs/lettering-standard.md` 3.15: salin stor ♥ + Daftar S/C ke `designs/lettering-v1/belajar/stor`, jalan `python3 designs/lettering-v1/belajar.py`, laksana TINDAKAN terus (ubahan menang = rev naik), lapor dalam jadual.

## Peraturan projek
- Cawangan kerja: `claude/jolly-hamilton-sdopyz`; tiada PR kecuali diminta.
- **Dashboard:** artifact sedia ada https://claude.ai/artifact/EeAC4MqQijSGYGTWfZW3Sg (jenis Data); jangan cipta baharu. Baca semula `files/index.html` sebelum ubah; salinan di `dashboard/index.html`. Tab: Ujikaji · Font · AI Image Test · Lesen · Setup · Workflow · Aliran · Daftar S/C · FC · ♥ Disukai. Checklist Setup = stor `data/setup/checklist/<id>`; Claude semak dan kemas kini `status`, `checked_at`, `result` dengan ArtifactData (update + if_version).
- Data dashboard dijana skrip: `scripts/poster_p1.py`…`poster_p7.py` → `data/export/posters/`; `scripts/build_prestasi.py` → `data/export/prestasi/`; `scripts/export_dashboard.py` → `data/export/`; `scripts/build_ai_tests.py` → `data/export/ai_tests/ai_all.json`. Jangan ubah fail dijana secara manual.
- Angka mesti bersumber; tanda tahap bukti (rasmi / pihak ketiga / lemah); jangan reka data.
- Jangan jana fail muat turun (PDF, Word, Excel dll.) tanpa kebenaran pengguna.
