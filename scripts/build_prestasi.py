"""Tab Prestasi: sasaran KPI 5 analisa, milestone 10 jualan/hari, dan alat data.
Jalankan: python3 scripts/build_prestasi.py  ->  data/export/prestasi/*.json"""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "data", "export", "prestasi")
os.makedirs(OUT, exist_ok=True)

SALES_DAY, PROFIT_ORDER, CONV, CTR, DAYS = 10, 30, 2.5, 0.5, 30.4
ORDERS = SALES_DAY * DAYS
VISITORS = ORDERS / (CONV / 100)
IMPRESSIONS = VISITORS / (CTR / 100)
PROFIT_MONTH = ORDERS * PROFIT_ORDER

A = {1: "Laman web", 2: "Pelawat", 3: "Produk", 4: "Pinterest", 5: "Jualan & untung"}
Q = {1: "Adakah laman web menukar pelawat jadi pembeli?", 2: "Siapa datang, dari mana, buat apa?",
     3: "Produk dan niche mana yang menjual?", 4: "Pin mana yang membawa pelawat?",
     5: "Adakah kita menuju 10 jualan sehari?"}
MODEL = "Sasaran model Claude (10 jualan/hari × $30)"
kpi = [
 (1, "web_lcp", "Kelajuan halaman (LCP)", "< 2.5 saat", 2.5, "saat", "PageSpeed Insights", "Bulanan", "Kecilkan imej, aktifkan cache Cloudflare, kurangkan plugin", "Google Core Web Vitals"),
 (1, "web_conv", "Pelawat yang membeli", f"≥ {CONV}%", CONV, "%", "WooCommerce + GA4", "Mingguan", "Tonjolkan set 3, mockup bilik, panduan saiz, ulasan pelanggan", MODEL),
 (1, "web_atc", "Tambah ke troli", "Tetapkan selepas 1 bulan data", None, "%", "GA4", "Bulanan", "Baiki gambar produk, harga dan panduan saiz; lihat heatmap Clarity", "Belum ada data asas"),
 (1, "web_checkout", "Checkout selesai", "Tetapkan selepas 1 bulan data", None, "%", "WooCommerce", "Bulanan", "Semak kos shipping, kelajuan dan langkah checkout; pastikan Cloudflare tidak menyekat checkout", "Belum ada data asas"),
 (2, "vis_month", "Pelawat sebulan", f"≥ {VISITORS:,.0f} (bulan 24)", round(VISITORS), "pelawat", "GA4", "Mingguan", "Tambah pin berkualiti; gandakan pin yang menang", MODEL),
 (2, "vis_pinterest", "Bahagian dari Pinterest", "≥ 80%", 80, "%", "GA4 (tag UTM)", "Bulanan", "Semak tag UTM pada setiap pin", "Fokus pembeli Pinterest"),
 (2, "vis_us", "Bahagian dari US", "≥ 80%", 80, "%", "GA4", "Bulanan", "Semak kata kunci dan board berbahasa Inggeris US", "Pasaran sasaran US"),
 (2, "vis_device", "Telefon vs komputer", "Pantau", None, "%", "GA4 / Clarity", "Bulanan", "Uji halaman produk dan checkout di telefon dahulu", "Pantau sahaja"),
 (2, "vis_return", "Pelawat ulangan", "Pantau", None, "%", "GA4", "Bulanan", "Kumpul emel dengan MailPoet; hantar koleksi baru", "Pantau sahaja"),
 (3, "prod_profit_order", "Untung setiap pesanan", f"≥ ${PROFIT_ORDER}", PROFIT_ORDER, "USD", "WooCommerce + Printify", "Mingguan", "Tonjolkan set, berbingkai dan canvas; potongan beli 2 atau lebih", MODEL),
 (3, "prod_mix", "Pesanan set, canvas atau berbingkai", "≥ 60% pesanan", 60, "%", "WooCommerce", "Bulanan", "Jadikan set sebagai pilihan utama di halaman produk", "Campuran untuk capai $30/pesanan"),
 (3, "prod_top", "10 produk terlaris", "Senarai bulanan", None, "", "WooCommerce", "Bulanan", "Jana variasi font dan warna untuk design yang menang", "Pantau sahaja"),
 (3, "prod_reprint", "Cetak semula / refund", "Pantau", None, "%", "Printify", "Bulanan", "Tukar provider cetak kalau kerosakan berulang", "Pantau sahaja"),
 (4, "pin_impr", "Tayangan sebulan", f"≥ {IMPRESSIONS / 1e6:.2f} juta (bulan 24)", round(IMPRESSIONS), "tayangan", "Pinterest Analytics", "Mingguan", "Tambah pin baru; pin 45–90 hari sebelum musim", MODEL),
 (4, "pin_ctr", "Kadar klik keluar", f"≥ {CTR}%", CTR, "%", "Pinterest Analytics", "Mingguan", "Pin imej statik bilik penuh, overlay nama bilik, tajuk berkata kunci", "Penanda aras pin statik ~0.48% (GenSumo)"),
 (4, "pin_pace", "Pin baru sehari", "10 (15 selepas bulan 3)", 10, "pin", "Penjadual pin", "Mingguan", "Kekalkan 1 pin setiap URL setiap 7 hari", "Panduan Tailwind 2026"),
 (4, "pin_top", "1% pin teratas", "Senarai bulanan", None, "", "Pinterest Analytics", "Bulanan", "Gandakan design dan gaya pin yang menang", "1% pin = >50% klik"),
 (5, "sales_day", "Jualan sehari", f"≥ {SALES_DAY} (bulan 24)", SALES_DAY, "jualan", "WooCommerce", "Mingguan", "Betulkan peringkat corong paling lemah dahulu", MODEL),
 (5, "profit_month", "Untung sebulan", f"≥ ${PROFIT_MONTH:,.0f} (bulan 24)", round(PROFIT_MONTH), "USD", "WooCommerce + Printify", "Bulanan", "Bandingkan dengan milestone bulanan", MODEL),
 (5, "fees", "Fee bayaran", "≈ 6% + $0.22 setiap pesanan", None, "", "Stripe / PayPal", "Bulanan", "Semak fee kad antarabangsa dan tukaran mata wang", "Anggaran fee Stripe Malaysia"),
]
kpi_rows = [{"id": i, "analysis_no": a, "analysis": A[a], "question": Q[a], "metric": m, "target": t, "target_value": v,
             "unit": u, "tool": tool, "frequency": f, "if_low": low, "basis": b, "actual_status": "Belum disambung"}
            for a, i, m, t, v, u, tool, f, low, b in kpi]

ms = [(6, "Jun 2027", 1.5), (12, "Dis 2027", 3), (18, "Jun 2028", 6), (24, "Dis 2028", 10)]
ms_rows = [{"month": m, "label": f"Bulan {m}", "date": d, "sales_per_day": s, "profit_month": round(s * DAYS * PROFIT_ORDER),
            "actual_status": "Belum disambung"} for m, d, s in ms]

tools = [
 ("Google Analytics 4", "Pelawat, Laman web", "Pelawat, sumber trafik, peranti, tambah ke troli", "Pasang GA4 (plugin Site Kit) di WordPress", "Percuma"),
 ("Microsoft Clarity", "Laman web", "Heatmap dan rakaman sesi pelawat", "Pasang plugin Clarity", "Percuma"),
 ("PageSpeed Insights", "Laman web", "Kelajuan halaman (LCP)", "Tiada pemasangan; uji URL", "Percuma"),
 ("WooCommerce Analytics", "Produk, Jualan & untung", "Pesanan, produk terlaris, nilai pesanan", "Terbina dalam WooCommerce", "Percuma"),
 ("Printify", "Produk, Jualan & untung", "Kos pengeluaran, cetak semula", "Laporan Printify / API", "Percuma"),
 ("Pinterest Analytics + Pinterest Tag", "Pinterest", "Tayangan, klik keluar, saves, penukaran", "Akaun Business, sahkan domain, pasang tag", "Percuma"),
 ("Google Search Console", "Pelawat", "Carian Google ke laman web", "Sahkan domain", "Percuma"),
 ("Cloudflare Web Analytics", "Laman web", "Trafik tanpa cookie, kelajuan", "Aktifkan dalam Cloudflare", "Percuma"),
]
tool_rows = [{"tool": t, "analysis": a, "gives": g, "how": h, "cost": c, "status": "Belum disambung"} for t, a, g, h, c in tools]

def W(name, rows):
    with open(os.path.join(OUT, name), "w") as f:
        f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n")
    print(name, len(rows))
W("prestasi_kpi.json", kpi_rows)
W("prestasi_milestones.json", ms_rows)
W("prestasi_tools.json", tool_rows)
print(f"corong: tayangan {IMPRESSIONS:,.0f} -> pelawat {VISITORS:,.0f} -> pesanan {ORDERS:,.0f} -> untung ${PROFIT_MONTH:,.0f}")
