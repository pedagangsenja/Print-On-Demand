# Standard Lettering: draf kerja (belum muktamad)

Nota kerja semasa menyemak cadangan standard langkah demi langkah (25 Nov 2026). Akan disusun semula selepas semua langkah disemak.
Asas: aliran S1–S6 (Lettering P9, `scripts/lettering/styles.py` dan `finish.py` di cawangan `claude/affectionate-wright-7y95k3`) dan SOP v3 (cawangan `claude/sharp-franklin-29eamk`).
Tahap bukti semua angka di bawah: lemah (ujian kecil, dinilai oleh Claude).

## Rangka cadangan

4 lapisan (Kad Gaya, pembina prompt, QC ikut kad, kemasan ikut kelas), 4 laluan ikut panjang ayat, 5 kunci gaya.

Laluan ikut panjang ayat baharu (bukan ayat rujukan):
1. Pendek, 1–4 perkataan: AI penuh, satu blok.
2. Sederhana, 5–8: AI penuh, hierarki wajib.
3. Panjang, 9–16: hibrid. AI lukis perkataan utama, font berlesen untuk baris lain.
4. Terlalu panjang, 17+: font dahulu. AI buat tajuk dan hiasan sahaja.

Lima kunci gaya: (1) Kad Gaya satu-satunya sumber; (2) QC sama untuk semua model; (3) model hanya untuk gaya yang ia lulus (jadual model × gaya); (4) skrip paksa warna, margin, tekstur; (5) peraturan ulang (ayat penegas + seed baharu, maks 4, kemudian model sandaran).

## Langkah 1: Kad Gaya (disemak 25 Nov; disimpan atas arahan pengguna)

Dapatan: prompt S1–S6 membawa 16 jenis maklumat; kad cadangan asal hanya ada tempat untuk 7.

Medan kad (16):
1. Medium
2. Warna latar (dalam C)
3. Bentuk susunan
4. Bentuk huruf ikut peranan (utama / sokongan / penyambung)
5. Hierarki saiz
6. Hiasan (jenis, warna, letak)
7. Tekstur dan kelas kemasan (F1 vektor rata, F2 rata + tekstur, F3 raster)
8. Huruf besar / kecil ikut peranan
9. Peta warna ikut peranan (perkataan mana dapat dakwat mana)
10. Jarak dan hubungan baris (rapat, bertindih, bertaut, sama lebar)
11. Garis dasar dan condong (melantun, condong, melengkung)
12. Butiran garisan (inline, kontras tebal-nipis, tepi kasar)
13. Ruang tepi
14. Larangan khusus gaya (cth. tiada outline, bayang, gradien)
15. Tanda baca
16. Peraturan pecahan baris (sebagai peraturan, bukan baris tetap)

Tambahan yang disyorkan:
- Ciri teras: 2–3 daripada 8 ciri QC wajib lulus (S001 lulus walaupun "kurang melantun", iaitu ciri utama rujukannya).
- Unsur berisiko (cth. reben berteks menghasilkan huruf rawak).
- Senarai "jangan salin": ayat, susun atur tepat, tandatangan atau logo rujukan.
- Julat panjang ayat yang sesuai untuk gaya itu.

Langkah kecil:
- 1a. Simpan imej rujukan di tempat kekal (sekarang hanya dalam container).
- 1b. Semak gaya sedia ada dalam S&C (elak pendua).
- 1c. Isi kad: medan tetap dengan pilihan tetap.
- 1d. Pengguna luluskan kad dan sahkan ciri teras (~2 minit).
- 1e. Imej bukti: satu ayat pendek, 2 seed, dibanding dengan upload. Kad aktif dan masuk S&C hanya selepas lulus.

## Langkah 2: Ayat, peranan dan laluan (cadangan 25 Nov; menunggu semakan pengguna)

Dapatan: S1–S6 hanya menyimpan senarai 4 perkataan; baris, peranan dan huruf besar/kecil terkunci dalam templat. "Semak trademark" tiada kaedah bertulis.

Data ralat ejaan (51 imej lettering BM v1–v3; 535 perkataan, 33 salah dipadankan):
- Ikut panjang perkataan: 1–3 huruf 0/51; 4–6 huruf 20/387 (5.2%); 7+ huruf 13/97 (13.4%).
- Ikut jenis huruf: Huruf Awal 21/203 (10.3%); HURUF BESAR 10/277 (3.6%); kecil 2/55 (3.6%). Huruf Awal biasanya ditulis dalam skrip, jadi kesan huruf dan kesan skrip bercampur.

Yang perlu ditambah:
1. Sumber dan keaslian ayat: ayat asal, bukan ayat rujukan, lirik atau petikan terkenal; bahasa direkod.
2. Saringan trademark dengan kaedah bertulis dan hasil direkod (saringan, bukan pengesahan undang-undang).
3. Ukuran kesukaran: bilangan perkataan + perkataan berisiko (7+ huruf) + perkataan berulang.
4. Padanan dengan kad: ayat mesti dalam julat panjang gaya; jika tidak, pendekkan atau tukar laluan.
5. Peraturan memilih perkataan utama: kata isi = utama; kata fungsi = penyambung; bilangan utama ikut laluan.
6. Peraturan huruf: sokongan dan penyambung dalam HURUF BESAR kecuali kad mewajibkan skrip; perkataan 7+ huruf dijadikan perkataan utama jika boleh.
7. Peraturan baris dan blok: perkataan utama dapat baris sendiri; maksimum 5–6 blok teks; susunan bacaan ditulis jelas.
8. Tanda baca ditulis jelas; elak jika kad tidak memerlukan.
9. Laluan 3–4: tetapkan di sini bahagian AI dan bahagian font.
10. Hasil langkah: Spesifikasi Teks berstruktur (baris, perkataan, peranan, huruf, tanda baca, laluan, perkataan berisiko). Ini rujukan ejaan untuk QC.

Langkah kecil: 2a ayat dan saringan; 2b ukur dan pilih laluan; 2c padan dengan kad; 2d peranan, baris, huruf, tanda baca; 2e Spesifikasi Teks.
