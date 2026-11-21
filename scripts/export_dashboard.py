"""Eksport data peringkat 1-7 kepada fail JSON (satu array) untuk dashboard.
Jalankan: python3 scripts/export_dashboard.py"""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")
L = lambda f: json.load(open(os.path.join(ROOT, "data", f)))
OUT = os.path.join(ROOT, "data", "export")
def W(name, rows):
    with open(os.path.join(OUT, name), "w") as f:
        f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n")
    print(name, len(rows))

niches = L("niches.json"); model = L("model.json"); kw = L("keywords.json")
prod = L("products.json"); per = L("personas.json"); pins = L("pins.json"); src = L("sources.json")
NAMES = {k: v["name"] for k, v in model["niches"].items()}
wave = {i: "Gelombang 1" for i in niches["decision"]["wave_1"]}
wave.update({i: "Gelombang 2" for i in niches["decision"]["wave_2"]})
wave.update({i: "Fasa 2" for i in niches["decision"]["phase_2_personalization"]})

rows = []
for rank, n in enumerate(sorted(niches["niches"], key=lambda x: -x["total"]), 1):
    ev = n["evidence"][0]
    m = model["niches"].get(n["id"], {})
    rows.append({"rank": rank, "niche": n["name"], "id": n["id"], **n["scores"], "total": n["total"],
                 "season": n["season"], "peak_months": n["peak_months"], "pin_window": m.get("pin", ""),
                 "wave": wave.get(n["id"], ""), "key_evidence": ev["claim"], "evidence_level": ev["level"],
                 "source": ev["source"] or ""})
W("niches.json", rows)

rows = []
for nid, items in kw["niches"].items():
    for k in items:
        vol = k.get("google_monthly") or k.get("google_monthly_peak")
        if vol is None: continue
        rows.append({"niche": NAMES.get(nid, "Nenek (rujukan)"), "keyword": k["keyword"], "google_monthly": vol,
                     "volume_type": "purata" if k.get("google_monthly") else "puncak",
                     "etsy_listings": k.get("etsy_listings"), "opportunity": k.get("opportunity"),
                     "note": k.get("note", ""), "source": k["source"]})
W("keywords.json", rows)

rows = []
for p in prod["products"]:
    pr = p.get("profit_usd")
    if pr is None:
        lo, hi = map(float, p["profit_usd_range"].split("-")); pr = round((lo + hi) / 2, 1)
    rows.append({"product": p["name"], "base_usd": p.get("base_usd"), "premium_usd": p.get("base_premium_usd"),
                 "shipping_usd": p.get("shipping_usd"), "price_usd": p.get("price_usd"), "profit_usd": pr,
                 "profit_note": p.get("profit_usd_range", "") and f"julat ${p['profit_usd_range']}",
                 "level": p["level"], "source": p["sources"][0]})
for b in prod["bundles"]:
    rows.append({"product": b["name"], "base_usd": None, "premium_usd": None, "shipping_usd": None,
                 "price_usd": b["revenue_usd"], "profit_usd": b["profit_usd"], "profit_note": "set / bulk",
                 "level": "dikira dari kos rasmi", "source": "https://printify.com/app/products/49/gildan/unisex-heavy-blendtm-crewneck-sweatshirt"})
W("products.json", rows)

rows = []
for p in per["personas"]:
    ms = p["market_size"][0] if p["market_size"] else {}
    sp = p["spend"][0] if p["spend"] else {}
    rows.append({"persona": p["name"], "niche": NAMES.get(p["niche"], p["niche"]), "who": p["who"],
                 "market_size": ms.get("claim", "Tiada data"), "spend": sp.get("claim", "Tiada data"),
                 "frequency": p["frequency"], "when": p["when"], "how": p["how"],
                 "products": ", ".join(p["products"]), "emotion": p["emotion"],
                 "source": ms.get("source") or sp.get("source") or ""})
W("personas.json", rows)

base = model["results"]["asas"]; y1 = base["year1"]["months"]
rows = []
for i, m in enumerate(base["steady"]["months"]):
    r = {"month": m["month"], "month_no": i + 1}
    r.update({k: round(v) for k, v in m["by_niche"].items()})
    r.update({"total": round(m["profit"]), "orders": round(m["orders"], 1), "revenue": round(m["revenue"]), "year1_profit": round(y1[i]["profit"])})
    rows.append(r)
W("model_monthly.json", rows)

rows = []
for k, n in model["niches"].items():
    for i, mon in enumerate(["Jan","Feb","Mac","Apr","Mei","Jun","Jul","Ogos","Sep","Okt","Nov","Dis"]):
        rows.append({"niche": n["name"], "niche_id": k, "month": mon, "month_no": i + 1, "index": n["idx"][i]})
W("seasonality.json", rows)

A = model["assumptions"]
rows = []
for s, desc in [("pesimis", A["pessimistic"]), ("asas", "3,000 pelawat/bulan; conversion 1.5% (bridal 1.0%)"), ("optimis", A["optimistic"])]:
    r = model["results"][s]
    rows.append({"scenario": s.capitalize(), "assumption": desc, "year1_profit": round(r["year1"]["total"]["profit"]),
                 "steady_profit": round(r["steady"]["total"]["profit"]), "steady_orders": round(r["steady"]["total"]["orders"]),
                 "steady_revenue": round(r["steady"]["total"]["revenue"])})
W("scenarios.json", rows)

rows = []
for t in pins["pin_templates"]:
    rows.append({"kind": "Templat pin", "item": f"{t['id']} {t['name']}", "detail": t["use"], "share_pct": int(t["share"].rstrip("%")), "level": "cadangan", "source": ""})
for r in pins["format_rules"]:
    rows.append({"kind": "Peraturan format", "item": r["rule"], "detail": "", "share_pct": None, "level": r["level"], "source": r["source"]})
for r in pins["pinterest_2026_trends"]:
    rows.append({"kind": "Trend Pinterest 2026", "item": r["trend"], "detail": "", "share_pct": None, "level": r["level"], "source": r["source"]})
for r in pins["typography_trends"]:
    rows.append({"kind": "Trend typography", "item": r["trend"], "detail": "", "share_pct": None, "level": r["level"], "source": r["source"]})
W("pin_playbook.json", rows)

rows = [{"id": s["id"], "domain": s["domain"], "level": s["level"], "stages": ", ".join(map(str, s["stages"])),
         "claim": (s["claims"][0] if s["claims"] else ""), "url": s["url"]} for s in src["sources"]]
W("sources.json", rows)

rows = [{"topic": c["topic"], "values": " | ".join(c["values"]), "resolution": c["resolution"]} for c in src["conflicts"]]
W("conflicts.json", rows)

# Katalog produk Printify + padanan niche (dari scripts/build_catalog.py)
cat = L("catalog.json")
W("catalog.json", cat["catalog"])
byid = {c["id"]: c for c in cat["catalog"]}
rows = []
for n in cat["niche_products"]:
    for role, ids in (("Utama", n["main"]), ("Tambahan", n["addon"])):
        for pid in ids:
            c = byid[pid]
            rows.append({"key": f"{n['niche_id']}:{pid}", "niche_id": n["niche_id"], "niche": n["niche"], "role": role,
                         "product_id": pid, "product": c["product"], "category": c["category"],
                         "price_usd": c["price_usd"], "profit_usd": c["profit_usd"],
                         "cost_note": c["cost_note"], "source": c["source"]})
W("niche_products.json", rows)
