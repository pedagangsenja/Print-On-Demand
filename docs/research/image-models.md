# Model Jana Imej: Harga & Ujian (Qwen-Image vs alternatif)

Tarikh: 2026-11-22. Tujuan: pilih model AI untuk poster tipografi (teks mesti tepat).

## Harga satu imej (~1 MP)

| Model | Harga | Teks dalam imej | Bukti |
|---|---|---|---|
| Qwen-Image-2512 (HF Space) | Percuma, ikut kuota ZeroGPU | Kuat | rasmi (ujian sendiri, lihat bawah) |
| Qwen-Image-2512 (fal.ai) | $0.02/MP; LoRA $0.035/MP | Kuat | rasmi (fal) |
| Qwen-Image 2.0 / 3.0 (Alibaba) | $0.025–0.035; Pro $0.075 | Kuat | rasmi (Alibaba) |
| FLUX.1 Schnell | $0.003/MP | Lemah | pihak ketiga |
| gpt-image-1 mini / gpt-image-1 | $0.005 / $0.02–0.19 | Sederhana–kuat | pihak ketiga |
| Ideogram 4.0 / 3.0 Turbo | $0.03; Quality $0.09–0.10 | Kuat (khusus teks) | pihak ketiga |
| Seedream 4.0 / 5.0 Lite | $0.03–0.035 | Sederhana | pihak ketiga |
| Recraft V4.1 / V4 Pro | $0.035 / $0.25 | Sederhana–kuat | pihak ketiga |
| Imagen 4 / Ultra | ~$0.05 / ~$0.054 | Sederhana | pihak ketiga |
| Qwen sendiri di Modal (H100) | ~$3.95/jam; kredit percuma $30/bulan | Kuat | pihak ketiga; kos/imej belum diukur |

Kos 100 poster: Qwen (fal) ~$2, Ideogram Turbo ~$3. Semua model keluar ~1–2 MP; poster cetak besar tetap perlu upscale.

## Ujian 22 Nov 2026 (Qwen vs Ideogram) — belum lengkap

- **HF Space Qwen percuma:** gagal. Mesej Space: "exceeded your free ZeroGPU quota (240s requested vs. 87s left)… PRO to get 25 min of ZeroGPU quota a day". Satu panggilan minta 240 s GPU; akaun percuma praktikal ≤1 imej/hari. PRO 25 min/hari ≈ 6 imej/hari (anggaran: 25×60/240). Dokumen HF pula sebut PRO 40 min, jadi angka bercanggah (rasmi, dua sumber HF).
- **Modal:** tidak boleh dari sesi awan ini (klien Modal guna gRPC; proksi tidak sokong).
- **HF Inference Providers (fal / wavespeed untuk Qwen-Image-2512):** host `router.huggingface.co` disekat rangkaian sesi.
- **Ideogram:** tiada kunci API (permintaan kunci ditolak).

## 5 prompt ujian (guna sama untuk kedua-dua model, nisbah 3:4)

1. **p1-kelas** — Retro colorful classroom typography poster, pastel and retro palette, rounded bubbly display font, the exact text "MISTAKES ARE PROOF THAT YOU ARE TRYING" in large letters, simple sun and rainbow shapes, flat vector style, clean cream background, print-ready wall art
2. **p2-bilikair** — Vintage Art Deco funny bathroom wall art, black and white with gold accents, elegant Art Deco display font, the exact text "PLEASE REMAIN SEATED FOR THE ENTIRE PERFORMANCE" centered, decorative geometric Art Deco border, flat print-ready typography poster
3. **p3-dapur** — Retro bistro coffee bar sign poster in menu style, cream background with tomato red and olive green, bold slab serif heading "COFFEE BAR", below it a small menu list "Espresso · Latte · Cappuccino · Mocha", footer text "FRESHLY BREWED DAILY", flat vintage typography print
4. **p4-pejabat** — Neo Deco luxe home office typography print, deep emerald green background with brass gold thin lines, elegant high-contrast serif font, the exact text "DO MORE OF WHAT MAKES YOU HAPPY", minimal geometric frame, sophisticated wall art
5. **p5-bacaan** — Dark academia poetcore reading nook typography poster, dark brown and forest green with cream, classic Garamond style serif, the exact quote "SO MANY BOOKS, SO LITTLE TIME" and below it in small italic "— Frank Zappa", small vintage book stack illustration, print-ready wall art

Skor setiap imej: ejaan betul (0–2), teks kecil boleh baca (0–2), gaya ikut niche (0–2), sedia cetak / tiada artifak (0–2). Maks 8.

## Sumber

Alibaba Model Studio pricing (alibabacloud.com/help/en/model-studio/model-pricing); qwen-image-3.0 (alibabacloud.com/help/en/model-studio/qwen-image-3-0); fal.ai/models/fal-ai/qwen-image-2512; huggingface.co/docs/hub/spaces-zerogpu; pricepertoken.com/image; modelslab.com/text-to-image-api-pricing-comparison; atlascloud.ai/blog/tips/cheapest-ai-image-generation-api-2026; ideogram.ai/api-pricing; usagepricing.com (Ideogram 4.0 launch 2026-06-15); dupple.com/learn/modal-pricing; modal.com/pricing.
