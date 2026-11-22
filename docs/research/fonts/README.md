# Kajian fon: senarai induk fon bebas untuk jualan

Tarikh: 22 Nov 2026. Tujuan: satu senarai fon yang **boleh dipakai untuk poster dan fail digital yang dijual**, dikumpul ikut **mood poster**, supaya pilihan fon sepadan dengan mesej dan tiada isu hak cipta.

## Fail dalam folder ini
- `README.md`: rangka kajian, peraturan lesen dan cara memilih (fail ini).
- `fonts-by-mood.md`: 12 fon terbaik setiap mood. Dijana oleh skrip, jangan ubah dengan tangan.
- `specimens/<mood>.png`: gambar contoh 12 fon setiap mood.
- `web-research-raw.md`: nota penuh kajian web (laman sumber, lesen, kajian mood, fon berus luar Google), dengan URL bukti.

Data (dijana skrip, jangan ubah dengan tangan):
- `data/fonts/google.json`, `fontshare.json`, `fontsquirrel.json`: snapshot dari sumber rasmi (`scripts/fonts_fetch.py`).
- `data/fonts/sites.json`, `licenses.json`, `research.json`: kajian web yang disusun dengan tangan, setiap baris ada URL bukti.
- `data/export/fonts/`: senarai induk, mood, pilihan teratas dan fon yang ditolak (`scripts/build_fonts.py`).

Jalankan semula:
```
FONT_CACHE=/tmp/fontcache python3 scripts/fonts_fetch.py      # ambil data terkini (perlukan akses rangkaian)
python3 scripts/build_fonts.py                                 # kelaskan mood + pilih fon
FONT_CACHE=/tmp/fontcache python3 scripts/fonts_specimens.py   # gambar contoh (Playwright)
```

## 1. Rangka kajian
1. **Sumber fon yang selamat.** Hanya sumber yang lesennya boleh dibaca dan membenarkan jualan: Google Fonts (OFL / Apache / UFL), Fontshare (ITF FFL v2) dan Font Squirrel (lesen dibaca dari fail dalam setiap zip).
2. **Semak lesen setiap fon.**
   - Google: folder lesen dalam repo `google/fonts`.
   - Fontshare: `License/FFL.txt` dalam zip.
   - Font Squirrel: fail lesen dalam zip, dikelaskan automatik kepada *selamat* (OFL / Apache / domain awam), *semak* (lesen sendiri yang sebut komersial dibenarkan) atau *berisiko* (tiada lesen, tidak jelas, atau ada had komersial).
3. **Label mood.**
   - Google: tag rasmi `tags/all/families.csv` (dinilai manusia, skor 0–100) dipetakan kepada 16 mood poster.
   - Fontshare dan Font Squirrel: kategori laman itu, ditambah semakan rupa oleh Claude (bukti lemah).
4. **Kedudukan.** Skor mood (55%), kualiti lukisan dan jarak huruf dari tag `Quality/*` Google (35%) dan bilangan ketebalan. Fon yang mood lain lebih kuat diturunkan. Satu fon setiap keluarga sahaja dalam senarai teratas.
5. **Bukti visual.** Gambar contoh setiap mood dijana dari fail fon sebenar, supaya pilihan dibuat dengan mata, bukan dengan nama sahaja.

## 2. Kenapa mood penting (bukti)
- Fon yang sepadan dengan isi mengubah nada emosi yang dirasai pembaca dalam 700 ms. Pembaca juga lebih cepat bila fon sepadan dengan perkataan (Hazlett dkk. 2013). **Rasmi**: [PDF](https://www.microsoft.com/en-us/research/uploads/prod/2021/06/Hazlett-Larson-Shaikh-Chaparo-2013-two-studies-on-how-a-typeface-congruent-with-content-can-enhance-onscreen-communication.pdf).
- 561 responden menilai 20 fon (Shaikh dkk. 2006). Personaliti terbahagi ikut keluarga fon:
  - Serif: stabil dan matang.
  - Script: feminin dan elegan.
  - Ada kumpulan tersendiri **Script/Funny**.

  **Rasmi** (dilaporkan dalam Hazlett 2013).
- Jenama dipilih kira-kira 2× lebih kerap bila fonnya sesuai (Doyle & Bottomley 2004). **Lemah** (ringkasan carian).
- Fon bulat dan seperti tulisan tangan dinilai mesra (Mackiewicz 2005), dan dipadankan dengan "manis" (Velasco dkk. 2015). **Lemah**.
- Tiada kajian langsung yang membuktikan "condensed tebal = motivasi". Label itu datang dari tag Google (skor Loud tinggi). **Lemah**.

## 3. 16 mood poster
| Mood | Rupa | Niche utama | Elak |
|---|---|---|---|
| Berus / cat air | Strok berus, dicat | Bilik tidur, nursery, afirmasi, iman | Ayat panjang, huruf besar semua |
| Romantik / elegan | Script formal bersambung | Bilik tidur, perkahwinan, Krismas | Lucu, gym, teks kecil |
| Tulisan tangan | Pen / marker santai | Nursery, dapur, kelas, afirmasi | Mewah, pejabat formal |
| Lucu / pelik | Melantun, tidak sekata | Bilik air, dapur, dobi, playroom | Mesej serius atau keagamaan |
| Kanak-kanak / comel | Bulat, tebal lembut | Nursery, kelas, playroom | Pejabat, gym |
| Lembut / tenang | Ringan, bulat, lapang | Kaunselor, afirmasi, bilik tidur | Humor kuat |
| Kuat / motivasi | Tebal dan sempit (condensed) | Home gym, home office, dorm | Script halus, nursery |
| Retro / groovy | Gemuk, berbayang, inline | Kelas, dapur, dorm | Minimalis, mewah |
| Klasik / akademik | Serif buku | Reading nook, home office | Kanak-kanak, humor |
| Mewah / Art Deco | Didone kontras tinggi, Deco | Bilik air vintage, home office | Kanak-kanak, grunge |
| Rustik / farmhouse | Slab kayu, tanda kedai lama | Dobi, dapur, pintu masuk | Mewah moden |
| Gotik / medieval | Blackletter | Krismas Victorian, Halloween | Ayat panjang |
| Seram / Halloween | Menitis, retak | Halloween sahaja | Semua niche lain |
| Kasar / grunge | Tekstur rosak, stensil | Remaja, dorm, man cave | Nursery, perkahwinan |
| Moden / minimalis | Sans bersih | Ruang tamu, home office | – |
| Futuristik / tekno | Piksel, segmen | Remaja, dorm | Kebanyakan niche Gelombang 1 |

Senarai fon setiap mood ada di `fonts-by-mood.md`. Rupa setiap fon ada di `specimens/`.

## 4. Ketebalan (weight): cara memilih
- **Hierarki perlukan ketebalan berbeza.** Tajuk tebal dan subtajuk ringan dari keluarga yang sama nampak kemas. Utamakan keluarga yang ada 5 ketebalan atau lebih, atau "variable". Dashboard ada tapisan untuk ini.
- **Fon display atau script satu ketebalan** (cth. Kaushan Script, Water Brush): pakai untuk 1–3 perkataan. Pasangkan dengan sans yang banyak ketebalan untuk teks lain (lajur "Teks pasangan").
- **Gambar kecil Pinterest:** strok nipis (cth. Pencerio Hairline) hilang bila dikecilkan. Uji poster pada saiz kecil sebelum diterbitkan.
- **Motivasi dan gym:** pakai berat 700–900 dari fon condensed. Fon condensed ringan nampak lemah.
- **Satu poster, dua fon.** Satu fon mood (tajuk) dan satu fon neutral (teks). Lebih dua fon nampak bersepah.

## 5. Peraturan lesen (wajib)
1. Guna hanya lesen dalam jadual "boleh jual" di dashboard: OFL, Apache, UFL, ITF FFL, Fontfabric FFF EULA, Fontspring Desktop (Typodermic), CC0, atau teks lesen yang jelas menyebut kegunaan komersial dan cetakan.
2. **Jangan sekali-kali** kongsi atau jual fail fon. Lesen FFL dan Fontfabric melarang, termasuk kepada kedai cetak. Hantar PNG/JPG/PDF yang teksnya sudah diratakan (flatten) atau ditukar ke outline.
3. **Jangan jual template boleh-edit** (Canva, PSD) yang mengandungi fon.
4. Simpan tangkapan skrin lesen setiap fon yang dipakai, bersama tarikh muat turun.
5. Laman "elak" (DaFont, Befonts, Behance, Lost Type pada $0, freebie Creative Fabrica atau Envato): jangan guna kecuali zipnya ada lesen komersial bertulis.
6. Font Squirrel tidak 100% selamat. Ada fon "found on the internet" tanpa lesen dan fon untuk kegunaan peribadi sahaja. Guna hanya yang berlabel *selamat* atau *semak*, dan baca lesen yang berlabel *semak*.

## 6. Cat air (watercolour)
Tiada fon cat air berwarna yang lesen komersialnya jelas ditemui (bukti: kajian web, `web-research-raw.md` bahagian D). Kebanyakan "fon cat air" ialah produk SVG atau warna berbayar. **Cara selamat:** taip teks dengan fon berus OFL, kemudian letak tekstur cat air sendiri sebagai lapisan gambar.

## 7. Had kajian
- Banyak laman sumber dan jurnal disekat dari sesi ini. Baris berlabel *lemah* dalam `sites.json` dan `licenses.json` hanya dari ringkasan carian. Sahkan sebelum bergantung padanya.
- 22 Nov 2026 (kemudian): OFL FAQ, CC0, CC-BY, CC-BY-ND, 1001 Fonts FFC dan Collletttivo dibaca terus dari laman rasmi dan dinaikkan ke *rasmi*.
- Label mood Fontshare dan Font Squirrel ialah semakan rupa oleh Claude, bukan tag rasmi.
- Pengelasan automatik lesen Font Squirrel boleh tersilap. Label *semak* bermaksud baca lesen itu sendiri.
