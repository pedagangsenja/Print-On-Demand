# Gabung cawangan lettering: peta pertembungan (28 Nov 2026)

Lima sesi Claude bekerja serentak pada `designs/lettering-v1/` dari asas yang sama (`2309b2c`) dan TIDAK digabung. Semakan 28 Nov 2026, 03:50 UTC (sesi `exciting-sagan` masih aktif).

## Pertembungan nama
| Cawangan | Kad baharu (gambar upload) | Huruf ayat baharu | Folder batch | Ujian dashboard |
|---|---|---|---|---|
| nifty-lovelace (sesi ini) | K20–K23 (dahulu K9–K12; IMG_5845, 5846, 5840, 5793) + K2, K4 | a b c e f q (dahulu A B C E F Q) | v12-cpu-ref6, v12-cpu-uji | U20, U21 |
| focused-faraday | K9–K13 (IMG_5840, 5793, 5789, 5786, 5791) | R Q A T S | v12-cpu-k9k13(-p1) | tiada baris sendiri dalam ai_all semasa |
| lucid-galileo | K9–K13 (IMG_5838, 5817, 5819, 5745, 5743) | R E C S U | v12-cpu-k9 | U15 |
| sleepy-edison | K9–K12 (IMG_5810, 5804, 5796, 5797) | B V N Y | v12b-cpu(-p1, -p2, -uji) | U16 |
| exciting-sagan | K9–K13 (IMG_5776, 5777, 5761, 5762, 5755) | Q F R O V | v12b-cpu(-p1, -p2) | U13, U14 |
| focused-allen | tiada kad baharu (larian kedua K1–K8 + rujukan baharu) | – | v12b-cpu | U17 |

IMG_5840 dan IMG_5793 dipakai oleh dua sesi (sesi ini dan focused-faraday) dengan kad berlainan.

## Pertembungan kod (versi sama, isi berlainan)
- `skrip/SK06_finish.py`: v1.3 (galileo, sleepy), v1.4 (sesi ini: tekstur calar; sagan; faraday), v1.6 (allen).
- `skrip/betulkan.py`: 5b v1.1 (sesi ini, faraday, sleepy), 5b v1.2 (sagan, allen, galileo).
- `belajar.py`: b1.1 (sagan, allen, sleepy), b1.2 (sesi ini: seri dipecah oleh cacat sasaran; faraday; galileo).
- `pembina.py`: label v1.2-p1 di semua cawangan, tetapi aturan model berbeza (sesi ini: klein4b r2, zturbo r2).

## Syarat gabung yang selamat
1. Hentikan semua sesi lettering lain dahulu.
2. Satu nombor kad dan satu huruf ayat yang unik bagi setiap sesi (huruf ayat satu aksara: `pembina` membaca `id[:-1]`, `id[-1]`), dan satu nama folder batch bagi setiap sesi.
3. Gabung kod SK / belajar satu demi satu dengan nombor versi baharu; jalankan semula belajar.py dan belajar_sk.py selepas gabung.
4. Dashboard: `ai_all` sekarang last-writer-wins. Bina semula daripada semua `data/ai_tests/rows/*.json` selepas gabung.
