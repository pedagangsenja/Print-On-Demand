# SOP: poster lettering + quality check (QC)

Disediakan 23 Nov 2026. Salinan dalam dashboard: tab Workflow → "SOP lettering + QC". Data: `designs/lettering-test/v3/` (sop.json, rubric.json, refs_deepdive.json); dataset dashboard dijana oleh `scripts/build_lettering_test.py v3`.

## Tujuan
Jana poster lettering yang ikut kualiti 5 poster rujukan pengguna (B1-B5, upload 23 Nov; design orang lain, rujukan gaya sahaja). Final = hanya imej yang **100% ejaan betul** dan lulus QC gaya.

## Alat
- Model: ERNIE-Image-Turbo + penambah prompt (Apache 2.0, percuma, tiada kuota), CPU, 768x1024, 8 langkah, ~10 min setiap imej.
- Penjana: `designs/lettering-test/gen.py ernie_pe --set v3 --seeds <seed> <id...>`.
- Prompt: `designs/lettering-test/v3/build_prompts.py` (templat = unsur rujukan + gaya huruf + teks baris demi baris + peraturan).

## Langkah
1. **Pilih gaya rujukan** (B1-B5) dan baca unsurnya (jadual "Kajian 5 rujukan").
2. **Tulis frasa baharu**: frasa Melayu asli, jangan salin ayat rujukan. Panjang: lencana 3-5 perkataan, poster 9-16. Letak tanda baca.
3. **Bahagi baris**: 2-5 perkataan utama sangat besar, lain kecil. Tentukan bekas: reben, label koyak, bulatan, atau ditulis atas objek.
4. **Pilih gaya huruf**: 3 atau lebih. Varian a = macam rujukan; varian b = font lain, unsur lain kekal.
5. **Bina prompt** dengan `build_prompts.py`.
6. **Jana** cubaan 1 (seed 42).
7. **QC pintu wajib** (semua mesti lulus):
   - G1 ejaan 100% (semak huruf demi huruf);
   - G2 tiada huruf/perkataan rawak, tiada tanda baca yang mengubah maksud;
   - G3 tiada kecacatan (huruf bertindih tak terbaca, teks terpotong, tangan/objek cacat).
8. **QC gaya**: banding sebelah-menyebelah dengan rujukan; semak 8 unsur gaya itu (`rubric.json`). Lulus jika 7/8 atau lebih.
9. **Redo (auto edit)**: ejaan salah → seed baharu (7, 123, 2024), prompt sama. Unsur gaya gagal → tambah ayat penegasan untuk unsur itu dalam `revisions.json` + seed baharu. Maksimum 4 cubaan. Setiap cubaan direkod dalam `qc.json`.
10. **Final**: hanya imej lulus. Gagal 4 kali → laporkan sebab dan cadang tukar perkataan/frasa.
11. **Pengguna luluskan**, kemudian besarkan imej (upscale) ke saiz cetak sebelum dijual.

## Unsur gaya setiap rujukan (ringkas)
- **B4 hiasan krim + emas**: krim + emas atas hitam; satu tiang di tengah; hierarki besar/kecil; baris bertaut + skrol emas di belakang huruf; 3+ gaya huruf; baris pertama melengkung; perkataan kecil dalam tag emas/bulatan; swash jadi hiasan.
- **B5 papan kapur**: kapur atas batu tulis; tiang di tengah; 2-3 perkataan utama besar; inline/3D; 3+ gaya huruf; reben kapur berlipat; pembahagi fleuron/bintang; butir kapur + tanda baca.
- **B3 berus berwarna**: latar grunge gelap + percikan; 4 warna, setiap baris lain; penuh kanvas, baris condong; berus kering + bayang; 3+ gaya huruf; label kertas koyak; anak panah/bintang/coretan; hierarki besar/kecil.
- **B2 lencana**: hitam-putih, latar luar putih; bentuk lencana + sinar matahari; 3-5 perkataan sangat besar; inline + bayang 3D; 3+ gaya huruf; garis dasar melantun + swash; daun/titik mengisi; tepi berus kasar + percikan.
- **B1 ilustrasi**: krim atas hitam gaya scratchboard; tangan memegang objek; satu perkataan atas objek; reben di belakang tangan; hierarki; 3+ gaya huruf; skrol/titik/sinar; cetakan lusuh.

## Had dan nota
- QC dibuat dengan mata oleh Claude (tahap bukti lemah). OCR biasa tidak boleh baca huruf hiasan dengan tepat (ujian 23 Nov).
- Perkataan yang kerap salah dalam ujian: "kerana", perkataan berakhiran "-nnya", perkataan panjang dalam skrip. Jika gagal 4 kali, tukar perkataan.
- Jangan tiru tandatangan atau watermark dalam rujukan.
