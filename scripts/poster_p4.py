"""Poster P4: format poster Printify + digital, kos & untung ikut saiz. Tulis data/posters/formats.json"""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")
fee = lambda price, ship: 0.06 * (price + ship) + 0.22
prof = lambda price, base, ship: round(price - base - fee(price, ship), 1)
PF = "https://printify.com/app/products/"
F = [  # id, format, kos min (Free), Premium, saiz, sumber, tahap, kegunaan, cadangan
 ("rolled", "Rolled poster", 2.98, 2.13, "102 saiz, 4 provider", PF+"home-and-living/canvas", "rasmi", "Poster kecil paling murah", "Pilihan untuk saiz kecil"),
 ("matte", "Poster matte", 4.96, 3.61, "47 saiz (8×10 hingga 28×28); hanya ke US (Today's Graphics)", PF+"282/generic-brand/matte-vertical-posters", "rasmi", "Format teras semua niche", "Teras"),
 ("satin_archival", "Satin & archival matte", None, 2.44, "Premium bermula $2.44", PF+"1309/generic-brand/satin-and-archival-matte-posters", "pihak_ketiga", "Alternatif kertas", "Pilihan"),
 ("uncoated", "Poster uncoated", 6.87, 4.97, "", PF+"1079/generic-brand/unframed-posters", "pihak_ketiga", "Alternatif kertas", "Pilihan"),
 ("fine_art", "Fine art (Giclée 220gsm)", 8.39, 6.08, "10×8 hingga 30×30 (Print Clever)", PF+"804/generic-brand/fine-art-posters", "rasmi", "Naik taraf kualiti", "Upsell"),
 ("satin300", "Poster satin 300gsm", 9.47, 6.86, "14-26 saiz (Sensaria)", PF+"829/generic-brand/satin-posters-300gsm", "rasmi", "Kurang silau", "Pilihan"),
 ("foam_board", "Foam board", 7.72, 5.59, "19 saiz, 2 provider", PF+"../products/promotional-collections/trending-wall-art-picks", "pihak_ketiga", "Papan tanda perkahwinan / majlis", "Fasa 2 (wedding)"),
 ("framed_budget", "Poster berbingkai (asas)", 13.19, None, "7 saiz, 11×14 hingga 16×16; produksi ~3 hari", PF+"540/generic-brand/framed-vertical-poster", "rasmi", "Hadiah, bilik air (tahan lembap lebih baik)", "Teras"),
 ("metal_sign", "Metal art sign (aluminium)", 13.80, 10.30, "18 saiz, 2 provider", PF+"1206/generic-brand/metal-art-sign", "rasmi", "Bilik air, gym, dobi, garaj (tahan lembap)", "Disyorkan untuk bilik lembap"),
 ("acrylic_panel", "Panel akrilik", 14.16, 10.56, "Dalaman sahaja", PF+"1098/generic-brand/acrylic-wall-art-panels", "rasmi", "Premium moden", "Pilihan"),
 ("framed_canvas", "Canvas berbingkai", 19.60, 15.21, "Pelbagai warna bingkai", PF+"944/generic-brand/matte-canvas-black-frame", "rasmi", "Premium", "Upsell"),
 ("canvas", "Canvas stretched 1.25\"", 10.63, 7.94, "Saiz termurah; 16×20 dianggar $15-22, 24×36 $25-35", PF+"home-and-living/canvas", "rasmi", "Ruang tamu, bilik tidur, nursery", "Teras (untung dolar tertinggi)"),
 ("framed_premium", "Poster berbingkai premium", 42.29, None, "8×11 hingga 24×36", PF+"492/generic-brand/premium-framed-vertical-poster", "rasmi", "Hadiah premium", "Upsell"),
 ("framed_roma", "Poster berbingkai (Roma)", 35.89, 26.01, "", PF+"540/roma-imaging/framed-vertical-poster", "rasmi", "Hadiah", "Pilihan"),
 ("acrylic_print", "Acrylic print (French cleat)", 54.75, 39.69, "", PF+"../products/promotional-collections/trending-wall-art-picks", "pihak_ketiga", "Premium tinggi", "Elak buat masa ini (modal tinggi)"),
 ("digital", "Printable digital", 0, None, "Fail muat turun", "https://sellertoolshq.com/guides/how-to-sell-wall-art-etsy/", "pihak_ketiga", "Semua niche; kelas & calm corner", "Teras (margin ~100%)"),
]
for f in F:
    if f[0] in ("foam_board", "acrylic_print"): pass
formats = [{"id": a, "format": b, "base_min_usd": c, "premium_min_usd": d, "sizes": e, "source": s.replace("app/products/../products/", "app/products/"), "level": l, "use": u, "recommendation": r} for a, b, c, d, e, s, l, u, r in F]

# Untung ikut saiz/produk (pembeli bayar shipping)
SIZES = [  # format, saiz, kos, shipping, harga, nota kos, nota shipping
 ("Poster matte", "8×10", 4.96, 7.39, 14.99, "Kos termurah", "Anggaran (tier Today's Graphics)"),
 ("Poster matte", "11×14", 5.50, 7.39, 19.99, "Anggaran", "Anggaran"),
 ("Poster matte", "12×18", 6.50, 7.39, 22.99, "Anggaran", "Anggaran"),
 ("Poster matte", "16×20", 7.50, 7.39, 27.99, "Anggaran", "Today's Graphics $7.39 (+$1.99)"),
 ("Poster matte", "18×24", 8.50, 7.39, 29.99, "Anggaran", "Today's Graphics $7.39 (+$1.99)"),
 ("Poster matte", "24×36", 10.39, 11.59, 39.99, "Dari kedai Printify", "Sensaria $11.59 (+$6.19)"),
 ("Rolled poster", "8×12", 2.98, 5.79, 12.99, "Kos termurah", "Jondo economy $5.79 (+$0.39)"),
 ("Satin 300gsm", "18×24", 11.00, 7.39, 32.99, "Anggaran (termurah $9.47)", "Anggaran"),
 ("Fine art Giclée", "16×20", 12.00, 8.09, 34.99, "Anggaran (termurah $8.39)", "Printify Choice fine art $8.09 (+$1.99)"),
 ("Berbingkai asas", "11×14", 13.19, 10.00, 49.99, "Kos termurah", "Anggaran"),
 ("Berbingkai (Roma)", "terkecil", 35.89, 12.80, 74.99, "Kos termurah", "~$12.49-13.19"),
 ("Metal art sign", "terkecil", 13.80, 8.00, 34.99, "Kos termurah", "Anggaran"),
 ("Panel akrilik", "terkecil", 14.16, 8.00, 39.99, "Kos termurah", "Anggaran"),
 ("Foam board", "terkecil", 7.72, 9.00, 34.99, "Kos termurah; saiz papan tanda lebih mahal", "Anggaran"),
 ("Canvas", "16×20", 18.50, 10.00, 69.99, "Anggaran $15-22", "Anggaran"),
 ("Canvas", "24×36", 30.00, 12.00, 99.99, "Anggaran $25-35", "Anggaran"),
 ("Digital", "1 fail", 0, 0, 6.99, "", "Tiada"),
 ("Digital", "Bundle 3", 0, 0, 12.99, "", "Tiada"),
 ("Digital", "Bundle kelas 12", 0, 0, 24.99, "", "Tiada"),
]
sizes = []
for fmt, sz, base, ship, price, cn, sn in SIZES:
    sizes.append({"key": f"{fmt} {sz}", "format": fmt, "size": sz, "base_usd": base, "shipping_usd": ship, "price_usd": price,
                  "profit_usd": prof(price, base, ship), "margin_pct": round(prof(price, base, ship) / price * 100), "cost_note": cn, "shipping_note": sn})
SETS = [  # nama, harga, kos, shipping
 ("Set 3 poster matte 11×14", 49.99, 16.50, 7.39 + 2 * 1.99),
 ("Set 3 poster matte 18×24", 69.99, 25.50, 7.39 + 2 * 1.99),
 ("Set 2 berbingkai asas 11×14 (atas katil)", 89.99, 26.38, 20.00),
 ("Set 12 poster matte 11×14 (kelas)", 99.99, 66.00, 7.39 + 11 * 1.99),
]
for name, price, base, ship in SETS:
    sizes.append({"key": name, "format": "Set gallery wall", "size": name.split(" ", 3)[-1], "base_usd": round(base, 2), "shipping_usd": round(ship, 2),
                  "price_usd": price, "profit_usd": prof(price, base, ship), "margin_pct": round(prof(price, base, ship) / price * 100),
                  "cost_note": "Dikira dari kos seunit", "shipping_note": "Item tambahan lebih murah" if "berbingkai" not in name else "Anggaran"})
out = {"stage": "P4", "title": "Format poster Printify + digital", "updated": "2026-11-21",
       "assumptions": "Pelan Printify Free; pembeli di US bayar shipping; fee bayaran 6% x (harga + shipping) + $0.22. Kos 'termurah' ialah saiz/provider paling murah; banyak kos saiz ialah anggaran.",
       "market_benchmarks": [
         {"claim": "Harga jualan poster POD saiz popular: $28-55, $32-65, $45-85", "source": "https://merchize.com/poster-sizes/", "level": "pihak_ketiga"},
         {"claim": "Printable digital $5-25 sekeping; kebanyakan penjual berjaya $12-18", "source": "https://sellertoolshq.com/guides/how-to-sell-wall-art-etsy/", "level": "pihak_ketiga"},
         {"claim": "18×24 = pilihan ramai; 24×36 = karya utama dengan harga premium (kos & shipping lebih tinggi)", "source": "https://printify.com/knowledge-hub/poster-sizes-that-sell/", "level": "rasmi"},
         {"claim": "Tawarkan beberapa saiz yang muat bingkai sedia ada; terlalu banyak saiz mengelirukan pembeli", "source": "https://printify.com/knowledge-hub/poster-sizes-that-sell/", "level": "rasmi"},
         {"claim": "Saiz biasa: 8×10, 11×14, 16×20, 18×24 (nisbah 4:5, 2:3, 3:4)", "source": "https://elistit-web.pages.dev/blog/etsy-wall-art-sizes-2026-complete-guide/", "level": "pihak_ketiga"},
         {"claim": "Kanvas dalam kumpulan saiz sama: item pertama + item tambahan; saiz berbeza: setiap satu kadar item pertama", "source": "https://help.printify.com/hc/en-us/articles/4483643971473", "level": "rasmi"}],
       "formats": formats, "profit_by_size": sizes}
json.dump(out, open(os.path.join(ROOT, "data", "posters", "formats.json"), "w"), indent=2, ensure_ascii=False)
for s in sizes: print(s["key"], s["price_usd"], s["profit_usd"], str(s["margin_pct"]) + "%")
