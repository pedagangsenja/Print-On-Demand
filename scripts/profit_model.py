"""Model untung setahun (Peringkat 6). Jalankan: python3 scripts/profit_model.py"""
import json, os

MONTHS = ["Jan","Feb","Mac","Apr","Mei","Jun","Jul","Ogos","Sep","Okt","Nov","Dis"]
STEADY_VISITORS = 3000
# Ramp tahun 1 (Jan 2027 = bulan 1): pecahan trafik matang
RAMP = [0.05,0.10,0.20,0.33,0.50,0.67,0.83,1,1,1,1,1]

NICHES = {
  # share trafik, conversion, untung/pesanan, hasil/pesanan, indeks musim (jumlah 1200), jenis
  "bridal":     dict(name="Bridal", share=0.15, conv=0.010, profit=70, revenue=160, type="bermusim",
                     idx=[110,110,115,125,125,95,100,120,115,70,50,65],
                     pin="Nov-Feb (proposal), Jan-Ogos (set bridal party)"),
  "teacher":    dict(name="Cikgu", share=0.12, conv=0.015, profit=20, revenue=35, type="bermusim",
                     idx=[70,60,70,120,150,80,140,160,90,60,80,120],
                     pin="Mac-Apr (appreciation), Mei-Jul (back-to-school), Okt-Nov (hadiah Krismas)"),
  "nursery":    dict(name="Nursery", share=0.15, conv=0.015, profit=25, revenue=45, type="sepanjang tahun",
                     idx=[95,95,105,120,105,95,95,95,95,95,100,105],
                     pin="Sepanjang tahun; tambah Feb-Mac"),
  "funny_home": dict(name="Tanda lucu rumah", share=0.20, conv=0.015, profit=22, revenue=40, type="sepanjang tahun",
                     idx=[90,80,95,105,100,90,85,95,100,110,125,125],
                     pin="Sepanjang tahun; tambah Dis-Feb dan Ogos-Okt"),
  "mama":       dict(name="Mama", share=0.12, conv=0.015, profit=20, revenue=35, type="sepanjang tahun + puncak",
                     idx=[70,70,90,140,190,70,60,60,70,90,130,150],
                     pin="Feb-Apr (Mother's Day), Sep-Okt (Krismas)"),
  "christmas":  dict(name="Krismas", share=0.08, conv=0.015, profit=26, revenue=45, type="bermusim",
                     idx=[10,0,0,0,0,0,10,30,80,200,420,450],
                     pin="Jul-Okt"),
  "friendship": dict(name="Kawan / Galentine", share=0.06, conv=0.015, profit=22, revenue=40, type="bermusim",
                     idx=[300,420,40,40,40,40,40,40,40,40,60,100],
                     pin="Nov-Jan"),
  "bookish":    dict(name="Bookish", share=0.12, conv=0.015, profit=18, revenue=32, type="sepanjang tahun",
                     idx=[90,85,90,90,95,95,100,100,100,105,125,125],
                     pin="Sepanjang tahun; tambah Ogos-Okt"),
}
SCENARIOS = {
  "pesimis": dict(traffic=0.5, conv_mult={"bridal":0.5}, conv_default=0.667),
  "asas":    dict(traffic=1.0, conv_mult={}, conv_default=1.0),
  "optimis": dict(traffic=2.0, conv_mult={}, conv_default=1.0),
}

def run(scn, ramp):
    s = SCENARIOS[scn]
    rows = []
    for m in range(12):
        row = {"month": MONTHS[m], "by_niche": {}, "profit": 0, "orders": 0, "revenue": 0}
        for k, n in NICHES.items():
            conv = n["conv"] * s["conv_mult"].get(k, s["conv_default"])
            visitors = STEADY_VISITORS * s["traffic"] * n["share"] * n["idx"][m] / 100 * (ramp[m] if ramp else 1)
            orders = visitors * conv
            row["by_niche"][k] = round(orders * n["profit"], 1)
            row["profit"] += orders * n["profit"]
            row["orders"] += orders
            row["revenue"] += orders * n["revenue"]
        row["profit"] = round(row["profit"], 1); row["orders"] = round(row["orders"], 1); row["revenue"] = round(row["revenue"], 1)
        rows.append(row)
    total = {k: round(sum(r[k] for r in rows), 1) for k in ("profit","orders","revenue")}
    return rows, total

out = {"stage": 6, "title": "Kalendar musim + model untung setahun", "updated": "2026-11-21",
       "assumptions": {
         "steady_visitors_per_month": STEADY_VISITORS,
         "ramp_year1": dict(zip(MONTHS, RAMP)),
         "conversion": "1.5% satu-satu; 1.0% bridal (anggaran berdasarkan purata kedai POD ~1.7%)",
         "profit_per_order": "Dari Peringkat 4 (kos Printify disahkan), campuran produk setiap niche",
         "seasonality": "Indeks anggaran Claude berdasarkan bukti Peringkat 1-5 (jumlah 1200 = purata 100/bulan); belum disahkan dengan Pinterest/Google Trends",
         "pessimistic": "trafik x0.5, conversion x0.67 (bridal x0.5)",
         "optimistic": "trafik x2 (6,000 pelawat/bulan)"},
       "niches": {k: {kk: v for kk, v in n.items()} for k, n in NICHES.items()},
       "results": {}}
for scn in SCENARIOS:
    steady_rows, steady_total = run(scn, None)
    y1_rows, y1_total = run(scn, RAMP)
    out["results"][scn] = {"steady": {"months": steady_rows, "total": steady_total},
                           "year1": {"months": y1_rows, "total": y1_total}}
path = os.path.join(os.path.dirname(__file__), "..", "data", "model.json")
json.dump(out, open(path, "w"), indent=2, ensure_ascii=False)
for scn in SCENARIOS:
    r = out["results"][scn]
    print(scn, "matang:", r["steady"]["total"], "| tahun1:", r["year1"]["total"])
base = out["results"]["asas"]["steady"]["months"]
print("\nAsas matang bulanan:")
for r in base:
    print(r["month"], r["profit"], r["orders"], {k: v for k, v in r["by_niche"].items()})
print("\nAsas tahun 1:")
for r in out["results"]["asas"]["year1"]["months"]:
    print(r["month"], r["profit"], r["orders"])
