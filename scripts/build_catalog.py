"""Katalog produk Printify + digital dan padanan produk untuk setiap niche.
Jalankan: python3 scripts/build_catalog.py  (tulis data/catalog.json)"""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")
FEE = lambda price, ship: 0.06 * (price + (ship or 0)) + 0.22
def P(price, base, ship): return round(price - base - FEE(price, ship), 1)

PF = "https://printify.com/app/products/"
C = []  # katalog
def add(id, product, cat, base, prem, ship, price, src, level, cost_note="", ship_note="", profit=None, profit_note="", status="Disyorkan"):
    if profit is None and base is not None and price is not None: profit = P(price, base, ship)
    C.append(dict(id=id, product=product, category=cat, base_usd=base, premium_usd=prem, cost_note=cost_note,
                  shipping_usd=ship, shipping_note=ship_note, price_usd=price, profit_usd=profit,
                  profit_note=profit_note, status=status, level=level, source=src))

add("poster_matte", "Poster matte 18×24", "Wall art", 8.50, 3.61, 7.39, 29.99, PF+"282/generic-brand/matte-vertical-posters", "rasmi", "Termurah $4.96 (Premium $3.61); saiz 18×24 dianggar ~$8.50", "Today's Graphics ke US (+$1.99 item tambahan)")
add("poster_set3", "Set 3 poster 18×24", "Set / bulk", 25.50, None, 11.37, 69.99, PF+"282/generic-brand/matte-vertical-posters", "rasmi", "3 × ~$8.50", "$7.39 + 2 × $1.99")
add("poster_framed", "Poster berbingkai", "Wall art", 35.89, 26.01, 12.80, 74.99, PF+"540/roma-imaging/framed-vertical-poster", "rasmi", "", "~$12.49–13.19")
add("canvas", "Canvas 16×20", "Wall art", 18.50, None, 10.0, 69.99, PF+"home-and-living/canvas", "pihak_ketiga", "Termurah $10.63 (Premium $7.94); 16×20 dianggar $15–22", "Anggaran", profit_note="julat $43–50")
add("printable", "Printable digital (bundle)", "Digital", 0, None, 0, 12.99, "https://www.etsy.com/listing/4315142864", "rasmi", "Tiada kos; dijual sebagai produk 'downloadable' WooCommerce", "Tiada")
add("svg", "Fail SVG/PNG (Cricut, sublimation)", "Digital", 0, None, 0, 9.99, "https://mydesigns.io/blog/svg-files-for-cricut/", "pihak_ketiga", "Tiada kos", "Tiada")
add("mug", "Mug seramik 11oz", "Dapur & minum", 4.93, 3.68, 5.49, 19.99, PF+"478/generic-brand/ceramic-mug-11oz-15oz", "rasmi", "", "Printify Choice (+$2.99 item tambahan)")
add("tumbler", "Tumbler stainless 20oz", "Dapur & minum", None, None, None, 32.99, PF+"1927/generic-brand/stainless-steel-tumbler-20oz", "pihak_ketiga", "EUR 18.59 (Premium EUR 16.48); USD pihak ketiga $12–16", "EUR 5.56", profit=13.0, profit_note="julat $10–16")
add("tea_towel", "Tuala dapur (microfiber)", "Dapur & minum", 10.10, None, 5.0, 22.99, PF+"1169/generic-brand/microfiber-tea-towel", "rasmi", "Tea towel kapas $17.47 (Premium $12.67)", "Anggaran")
add("apron", "Apron (AOP)", "Dapur & minum", 18.72, 13.99, 6.0, 34.99, PF+"418/generic-brand/apron-aop", "rasmi", "", "Anggaran")
add("tote", "Tote bag kanvas", "Aksesori & stationery", 9.67, None, 5.0, 24.99, "https://printify.com/app/brand/94/liberty-bags", "rasmi", "Liberty Bags", "Anggaran")
add("stickers", "Kiss-cut stickers", "Aksesori & stationery", 1.21, None, 4.0, 4.99, "https://printify.com/make-your-own-stickers", "rasmi", "Premium hingga 20% diskaun", "Anggaran")
add("journal", "Jurnal / buku nota", "Aksesori & stationery", None, None, None, 19.99, PF+"home-and-living/journals-and-notebooks", "rasmi", "Hardcover EUR 9.21 (Premium EUR 6.68); spiral EUR 7.19; USD belum dijumpai", "")
add("hat_emb", "Topi bersulam", "Aksesori & stationery", 13.20, None, 5.0, 32.99, "https://podvector.ai/articles/printify/products/the-complete-guide-to-printifys-most-profitable-products", "lemah", "Blog: $11.95–14.50 (belum disahkan di Printify)", "Anggaran")
add("gildan18000", "Sweatshirt Gildan 18000", "Pakaian", 17.87, None, 8.0, 44.99, PF+"49/gildan/unisex-heavy-blendtm-crewneck-sweatshirt", "rasmi", "", "Anggaran $5.99–8.79")
add("emb_sweatshirt", "Sweatshirt Gildan 18000 bersulam", "Pakaian", 19.61, None, 8.0, 54.99, "https://printify.com/custom-embroidered-hoodies/", "rasmi", "", "Anggaran")
add("cc1566", "Sweatshirt Comfort Colors 1566", "Pakaian", 31.29, 23.85, 8.0, 59.99, PF+"bestsellers", "rasmi", "", "Anggaran")
add("cc1717", "T-shirt Comfort Colors 1717", "Pakaian", 12.41, None, 4.75, 32.99, "https://printify.com/custom-t-shirts-ab/", "rasmi", "", "Printify Choice (+$2.40 item tambahan)")
add("hoodie_emb", "Hoodie Gildan 18500 bersulam", "Pakaian", 23.20, None, 8.0, 59.99, "https://printify.com/custom-embroidered-hoodies/", "rasmi", "", "Anggaran")
add("cc1567", "Hoodie Comfort Colors 1567", "Pakaian", 38.01, 27.14, 7.99, 64.99, PF+"1298/comfort-colors/unisex-garment-dyed-hoodie", "rasmi")
add("sweatpants", "Sweatpants / jogger", "Pakaian", 25.54, 23.37, 8.0, 49.99, "https://printify.com/custom-sweatpants/", "rasmi", "", "Anggaran")
add("velveteen", "Velveteen plush blanket", "Rumah & tekstil", 13.64, 9.88, 5.69, 44.99, PF+"522/generic-brand/velveteen-plush-blanket", "rasmi", "Saiz termurah")
add("sherpa", "Sherpa fleece blanket", "Rumah & tekstil", 29.31, 21.24, 13.79, 64.99, PF+"918/generic-brand/tan-sherpa-blanket", "rasmi")
add("pillow", "Bantal hiasan (spun polyester)", "Rumah & tekstil", None, None, None, 29.99, PF+"220/generic-brand/spun-polyester-square-pillow", "rasmi", "EUR 14.22 (Premium EUR 10.30); USD belum dijumpai", "")
add("doormat", "Doormat poliester", "Rumah & tekstil", 13.04, None, 7.0, 34.99, PF+"1601/generic-brand/polyester-doormat/", "rasmi", "18×30 inci", "Anggaran")
add("bathmat", "Bath mat", "Rumah & tekstil", None, None, None, 29.99, PF+"254/generic-brand/bath-mat", "rasmi", "EUR 14.97 (Premium EUR 10.85); USD belum dijumpai", "")
add("shower_curtain", "Langsir bilik mandi", "Rumah & tekstil", 40.80, 31.06, 9.0, 69.99, PF+"235/generic-brand/shower-curtains", "rasmi", "71×74 inci", "Anggaran")
add("ornament", "Perhiasan seramik (2 sisi)", "Musim", 9.79, None, 5.0, 19.99, PF+"1676/generic-brand/ceramic-ornament-2-side-print", "rasmi", "", "Anggaran")
add("baby_bodysuit", "Bodysuit bayi", "Bayi & kanak-kanak", None, None, None, 22.99, PF+"33/rabbit-skins/infant-fine-jersey-bodysuit", "rasmi", "EUR 9.16 (Premium EUR 7.27); USD belum dijumpai", "")
add("toddler_tee", "T-shirt toddler", "Bayi & kanak-kanak", 11.63, 8.85, 4.75, 24.99, PF+"580/bella-canvas/toddler-short-sleeve-tee", "rasmi", "", "Anggaran")
add("pet_bandana", "Bandana haiwan (clip-on)", "Haiwan", 8.92, 6.46, 4.0, 19.99, PF+"1672/generic-brand/clip-on-pet-bandana", "rasmi", "", "Anggaran")
add("bridal_set_sweat", "Set bridal 5 × Gildan 18000", "Set / bulk", 89.35, None, 18.0, 190.0, PF+"49/gildan/unisex-heavy-blendtm-crewneck-sweatshirt", "rasmi", "5 × $17.87; $38 sehelai", "$8 + 4 × ~$2.50")
add("bridal_set_tee", "Set bridal 5 × Comfort Colors 1717", "Set / bulk", 62.05, None, 14.35, 149.95, "https://printify.com/custom-t-shirts-ab/", "rasmi", "5 × $12.41; $29.99 sehelai", "$4.75 + 4 × $2.40")
add("comforter", "Comforter", "Elak", 78.59, 56.97, 12.0, 149.99, PF+"home-and-living/bedding", "rasmi", "Permintaan typography tidak terbukti; kos tinggi", "Anggaran", status="Elak")
add("duvet", "Sarung duvet", "Elak", 67.67, 49.06, 11.59, 109.99, PF+"home-and-living/bedding", "rasmi", "Permintaan typography tidak terbukti; kos tinggi", status="Elak")
add("rug", "Area rug", "Elak", 24.50, 17.76, 10.69, 49.99, PF+"../print-provider/10/mww-on-demand", "rasmi", "Permintaan typography tidak terbukti", status="Elak")
for c in C:
    if c["id"] == "rug": c["source"] = "https://printify.com/app/print-provider/10/mww-on-demand"

M = {  # niche_id: (nama, [utama], [tambahan])
 "bridal": ("Bridal party & bachelorette", ["bridal_set_sweat", "bridal_set_tee", "emb_sweatshirt"], ["tote", "tumbler", "stickers", "hat_emb"]),
 "teacher": ("Cikgu", ["poster_set3", "printable", "tote"], ["tumbler", "mug", "stickers", "journal", "cc1717"]),
 "nursery": ("Nursery & bilik anak", ["poster_matte", "poster_framed", "canvas", "printable"], ["velveteen", "baby_bodysuit", "pillow"]),
 "funny_home": ("Tanda lucu rumah", ["poster_set3", "printable", "poster_framed"], ["doormat", "bathmat", "shower_curtain", "tea_towel", "apron", "mug"]),
 "christmas": ("Krismas & hadiah cuti", ["gildan18000", "mug", "ornament", "velveteen"], ["sherpa", "poster_matte", "pillow", "tea_towel"]),
 "mama": ("Mama & motherhood", ["mug", "poster_framed", "velveteen", "cc1566"], ["tote", "emb_sweatshirt", "tumbler", "hat_emb"]),
 "friendship": ("Valentine / Galentine & kawan", ["mug", "tumbler", "cc1717"], ["stickers", "tote", "journal"]),
 "bookish": ("Bookish", ["tote", "gildan18000", "poster_matte"], ["stickers", "journal", "svg", "mug"]),
 "home_office": ("Home office / humor kerja", ["poster_matte", "poster_framed", "mug"], ["journal", "printable"]),
 "faith": ("Iman / Kristian", ["poster_matte", "poster_framed", "canvas", "printable"], ["mug", "tote", "cc1717", "journal"]),
 "sports_mom": ("Sports mom", ["cc1717", "gildan18000", "tumbler"], ["hat_emb", "tote", "stickers", "hoodie_emb"]),
 "halloween": ("Halloween", ["gildan18000", "cc1717", "doormat"], ["mug", "pet_bandana", "toddler_tee", "pillow"]),
 "affirmation": ("Afirmasi / kaunselor", ["poster_set3", "printable", "poster_framed"], ["journal", "stickers", "mug"]),
 "pet": ("Ibu bapa haiwan", ["pet_bandana", "mug", "gildan18000"], ["tote", "ornament", "pillow", "hat_emb"]),
 "grandma": ("Nenek (Nana, Gigi)", ["mug", "emb_sweatshirt", "velveteen"], ["poster_framed", "tote", "ornament"]),
 "family_est": ("Nama keluarga 'Est.'", ["poster_framed", "canvas", "doormat"], ["pillow", "ornament", "velveteen"]),
}
out = {"updated": "2026-11-21", "fee": "6% x (harga + shipping) + $0.22", "catalog": C,
       "niche_products": [{"niche_id": k, "niche": v[0], "main": v[1], "addon": v[2]} for k, v in M.items()]}
json.dump(out, open(os.path.join(ROOT, "data", "catalog.json"), "w"), indent=2, ensure_ascii=False)
ids = {c["id"] for c in C}
for v in M.values():
    for p in v[1] + v[2]: assert p in ids, p
print(len(C), "produk;", len(M), "niche")
for c in C: print(c["id"], c["profit_usd"])
