"""Poster P6: kalendar musim + model untung setahun (poster sahaja). Tulis data/posters/model.json"""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")
MONTHS = ["Jan","Feb","Mac","Apr","Mei","Jun","Jul","Ogos","Sep","Okt","Nov","Dis"]
STEADY = 3000
RAMP = [0.05,0.10,0.20,0.33,0.50,0.67,0.83,1,1,1,1,1]
WALL = [95,85,100,105,100,90,85,95,100,105,120,120]
HOME = [95,90,100,105,100,95,90,95,100,105,115,110]
N = {  # bahagian trafik, conversion, untung/pesanan, hasil/pesanan, indeks, campuran produk, tetingkap pin
 "living_room":  dict(name="Ruang tamu", share=0.14, conv=0.012, profit=42, revenue=85, idx=WALL, mix="Canvas 24×36/16×20, set 3 matte 18×24", pin="Sepanjang tahun; tambah Dis-Feb, Sep-Okt"),
 "bathroom":     dict(name="Bilik air (lucu)", share=0.14, conv=0.015, profit=27, revenue=50, idx=HOME, mix="Berbingkai 11×14, set 3, metal sign", pin="Sepanjang tahun"),
 "kitchen":      dict(name="Dapur & coffee bar", share=0.12, conv=0.015, profit=24, revenue=42, idx=HOME, mix="Matte 16×20, set 2-3, berbingkai", pin="Sepanjang tahun; tambah Sep-Nov"),
 "bedroom":      dict(name="Bilik tidur", share=0.10, conv=0.013, profit=35, revenue=70, idx=WALL, mix="Set 2 berbingkai atas katil, canvas, matte 18×24", pin="Sepanjang tahun; tambah Dis-Jan (Valentine)"),
 "nursery":      dict(name="Nursery", share=0.10, conv=0.014, profit=34, revenue=62, idx=[95,95,105,120,105,95,95,95,95,95,100,105], mix="Berbingkai, canvas 16×20, set 3", pin="Sepanjang tahun; tambah Jan-Mac"),
 "home_office":  dict(name="Home office & cubicle", share=0.10, conv=0.015, profit=22, revenue=40, idx=[130,135,100,90,85,80,85,95,120,100,90,90], mix="Berbingkai kecil, matte 8×10/11×14", pin="Nov-Jan, Jul-Ogos"),
 "classroom":    dict(name="Kelas", share=0.08, conv=0.015, profit=22, revenue=26, idx=[110,70,60,60,70,90,190,220,110,70,70,80], mix="Bundle digital 12 (utama), set fizikal kecil", pin="Mei-Ogos, Nov-Dis"),
 "reading_nook": dict(name="Reading nook & bookish", share=0.06, conv=0.015, profit=17, revenue=26, idx=[90,85,90,90,95,95,100,100,100,105,125,125], mix="Matte 16×20, printable", pin="Sepanjang tahun; tambah Ogos-Okt"),
 "seasonal_xmas":dict(name="Krismas & musim cuti", share=0.06, conv=0.015, profit=14, revenue=20, idx=[5,0,0,0,0,0,5,15,60,150,450,515], mix="Printable, matte 18×24", pin="Jul-Okt"),
 "counselor":    dict(name="Kaunselor / calm corner", share=0.05, conv=0.015, profit=18, revenue=20, idx=[100,90,90,90,80,60,100,170,150,100,90,80], mix="Bundle printable, set poster", pin="Mei-Ogos"),
 "laundry":      dict(name="Bilik dobi", share=0.05, conv=0.015, profit=17, revenue=30, idx=HOME, mix="Matte, metal sign, set 2", pin="Sepanjang tahun"),
}
for k, n in N.items(): assert abs(sum(n["idx"]) - 1200) < 1, k
assert abs(sum(n["share"] for n in N.values()) - 1) < 1e-9
SC = {"pesimis": dict(traffic=0.5, conv=0.667), "asas": dict(traffic=1.0, conv=1.0), "optimis": dict(traffic=2.0, conv=1.0)}
def run(s, ramp):
    rows = []
    for m in range(12):
        r = {"month": MONTHS[m], "month_no": m + 1, "profit": 0.0, "orders": 0.0, "revenue": 0.0}
        for k, n in N.items():
            v = STEADY * SC[s]["traffic"] * n["share"] * n["idx"][m] / 100 * (ramp[m] if ramp else 1)
            o = v * n["conv"] * SC[s]["conv"]
            r[k] = round(o * n["profit"]); r["profit"] += o * n["profit"]; r["orders"] += o; r["revenue"] += o * n["revenue"]
        r["profit"] = round(r["profit"]); r["orders"] = round(r["orders"], 1); r["revenue"] = round(r["revenue"])
        rows.append(r)
    tot = {k: round(sum(r[k] for r in rows)) for k in ("profit", "orders", "revenue")}
    return rows, tot
res = {}
for s in SC:
    st, stt = run(s, None); y1, y1t = run(s, RAMP)
    res[s] = {"steady": {"months": st, "total": stt}, "year1": {"months": y1, "total": y1t}}
base = res["asas"]["steady"]["months"]
by_niche = {k: sum(r[k] for r in base) for k in N}
out = {"stage": "P6", "title": "Kalendar musim + model untung poster setahun", "updated": "2026-11-21",
       "assumptions": {"steady_visitors": STEADY, "ramp_year1_from": "Jan 2027", "ramp": dict(zip(MONTHS, RAMP)),
                       "conversion": "1.5% (ruang tamu 1.2%, bilik tidur 1.3%, nursery 1.4% kerana harga lebih tinggi)",
                       "profit_per_order": "Campuran format dari P4 setiap niche",
                       "seasonality": "Indeks anggaran Claude dari bukti P1-P5 (christmas art Sep 8,100 -> Dis 135,000; office decor puncak Feb; back-to-school Jul-Ogos); belum disahkan dengan Pinterest/Google Trends",
                       "pessimistic": "trafik x0.5, conversion x0.67", "optimistic": "trafik x2"},
       "niches": {k: {kk: v for kk, v in n.items()} for k, n in N.items()},
       "by_niche_steady": by_niche, "results": res,
       "comparison": {"mixed_model_steady_profit": 13765, "note": "Model campuran (apparel + poster) dari Peringkat 6 asal"}}
json.dump(out, open(os.path.join(ROOT, "data", "posters", "model.json"), "w"), indent=2, ensure_ascii=False)
for s in SC: print(s, "matang", res[s]["steady"]["total"], "| tahun1", res[s]["year1"]["total"])
print({k: v for k, v in sorted(by_niche.items(), key=lambda x: -x[1])})
for r in base: print(r["month"], r["profit"], r["orders"])
print("tahun1:", [r["profit"] for r in res["asas"]["year1"]["months"]])
