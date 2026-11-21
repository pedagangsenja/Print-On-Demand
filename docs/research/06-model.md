# Peringkat 6: Kalendar Musim + Model Untung Setahun

Tarikh: 2026-11-21. Model: `scripts/profit_model.py` → `data/model.json` (boleh dijalankan semula bila data sebenar masuk).

## Andaian

- Trafik matang: 3,000 pelawat/bulan dari Pinterest (perlu ~0.6–1.5 juta impressions/bulan).
- Conversion: 1.5% (satu-satu), 1.0% (bridal). Purata kedai POD ~1.7% (pihak ketiga).
- Untung/pesanan: campuran produk setiap niche dari Peringkat 4 (kos Printify disahkan).
- Indeks musim: anggaran Claude dari bukti Peringkat 1–5; **belum disahkan dengan Pinterest/Google Trends**.
- Tahun 1 bermula Januari 2027 dengan ramp trafik 5% → 100% (Ogos).

## Kalendar musim & pin

| Niche | Jenis | Bulan jualan puncak | Tetingkap pin | Bahagian trafik |
|---|---|---|---|---|
| Bridal | Bermusim | Jan–Mei, Ogos–Sep | Nov–Feb (proposal), Jan–Ogos (set) | 15% |
| Cikgu | Bermusim | Apr–Mei, Jul–Ogos, Dis | Mac–Apr, Mei–Jul, Okt–Nov | 12% |
| Nursery | Sepanjang tahun | Apr | Sepanjang tahun (+Feb–Mac) | 15% |
| Tanda lucu rumah | Sepanjang tahun | Okt–Dis | Sepanjang tahun (+Dis–Feb, Ogos–Okt) | 20% |
| Mama | Sepanjang tahun + puncak | Apr–Mei, Nov–Dis | Feb–Apr, Sep–Okt | 12% |
| Krismas | Bermusim | Okt–Dis | Jul–Okt | 8% |
| Kawan / Galentine | Bermusim | Jan–Feb | Nov–Jan | 6% |
| Bookish | Sepanjang tahun | Nov–Dis | Sepanjang tahun (+Ogos–Okt) | 12% |

## Senario asas, fasa matang (USD)

| Bulan | Bridal | Cikgu | Nursery | Tanda lucu | Mama | Krismas | Kawan | Bookish | **Jumlah** | Pesanan |
|---|---|---|---|---|---|---|---|---|---|---|
| Jan | 347 | 76 | 160 | 178 | 76 | 9 | 178 | 88 | **1,111** | 40 |
| Feb | 347 | 65 | 160 | 158 | 76 | 0 | 250 | 83 | **1,138** | 42 |
| Mac | 362 | 76 | 177 | 188 | 97 | 0 | 24 | 88 | **1,012** | 35 |
| Apr | 394 | 130 | 203 | 208 | 151 | 0 | 24 | 88 | **1,196** | 43 |
| Mei | 394 | 162 | 177 | 198 | 205 | 0 | 24 | 92 | **1,252** | 46 |
| Jun | 299 | 86 | 160 | 178 | 76 | 0 | 24 | 92 | **916** | 33 |
| Jul | 315 | 151 | 160 | 168 | 65 | 9 | 24 | 97 | **990** | 36 |
| Ogos | 378 | 173 | 160 | 188 | 65 | 28 | 24 | 97 | **1,113** | 40 |
| Sep | 362 | 97 | 160 | 198 | 76 | 75 | 24 | 97 | **1,089** | 39 |
| Okt | 221 | 65 | 160 | 218 | 97 | 187 | 24 | 102 | **1,074** | 42 |
| Nov | 158 | 86 | 169 | 248 | 140 | 393 | 36 | 122 | **1,351** | 55 |
| Dis | 205 | 130 | 177 | 248 | 162 | 421 | 59 | 122 | **1,523** | 62 |
| **Setahun** | **3,780** | **1,296** | **2,025** | **2,376** | **1,285** | **1,123** | **713** | **1,166** | **~13,765** | **~513** |

Purata ~$1,147/bulan; terendah Jun ($916, −20%), tertinggi Dis ($1,523, +33%). Jualan kasar ~$26,400/tahun.

## Tahun 1 (Jan–Dis 2027, ramp trafik)

| Jan | Feb | Mac | Apr | Mei | Jun | Jul | Ogos | Sep | Okt | Nov | Dis | **Jumlah** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 56 | 114 | 202 | 395 | 626 | 614 | 822 | 1,113 | 1,089 | 1,074 | 1,351 | 1,523 | **~$8,980** (~339 pesanan) |

## Tiga senario

| Senario | Andaian | Tahun 1 | Matang (setahun) | Pesanan/tahun (matang) |
|---|---|---|---|---|
| Pesimis | Trafik ×0.5, conversion ×0.67 (bridal ×0.5) | ~$2,810 | ~$4,275 | ~166 |
| **Asas** | 3,000 pelawat/bulan | **~$8,980** | **~$13,765** | **~513** |
| Optimis | 6,000 pelawat/bulan | ~$17,955 | ~$27,530 | ~1,025 |

## Kesimpulan

- Bridal ialah penyumbang terbesar (~27% untung) walaupun 15% trafik, tetapi paling bermusim dan berisiko operasi.
- Wall art (tanda lucu + nursery) memberi asas stabil ~$4,400/tahun.
- Krismas dan Mama mengangkat Q4 dan Mei; Kawan mengisi Jan–Feb.
- Pemacu terbesar untung ialah **trafik**: setiap 1,000 pelawat matang tambahan ≈ +$4,600/tahun (senario asas).
