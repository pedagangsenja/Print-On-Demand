"""Poster P7: semakan konsistensi P1-P6, daftar sumber, percanggahan, dan eksport data tab Poster.
Jalankan: python3 scripts/poster_p7.py"""
import json, os
from urllib.parse import urlparse
from collections import Counter

ROOT = os.path.join(os.path.dirname(__file__), "..")
P = lambda f: os.path.join(ROOT, "data", "posters", f)
L = lambda f: json.load(open(P(f + ".json")))
OUT = os.path.join(ROOT, "data", "export", "posters")
os.makedirs(OUT, exist_ok=True)
def W(name, rows):
    with open(os.path.join(OUT, name), "w") as f:
        f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n")
    print(f"  {name}: {len(rows)} baris")

N, K, S, F, PE, M = (L(x) for x in ("niches", "keywords", "styles", "formats", "personas", "model"))
MONTHS = ["Jan","Feb","Mac","Apr","Mei","Jun","Jul","Ogos","Sep","Okt","Nov","Dis"]
ids = {n["id"] for n in N["niches"]}

# ---------- 1. Semakan konsistensi ----------
checks = []
def chk(name, ok, detail=""):
    checks.append({"check": name, "status": "LULUS" if ok else "GAGAL", "detail": detail})
miss = sorted({k["niche_id"] for k in K["keywords"]} - ids - {"sets"})
chk("ID niche kata kunci wujud di P1", not miss, ", ".join(miss) or "55 kata kunci; 'sets' = kategori set")
miss = sorted({s["niche_id"] for s in S["styles"]} - ids)
chk("ID niche gaya wujud di P1", not miss, ", ".join(miss) or f"{len(S['styles'])} panduan gaya")
miss = sorted(set(M["niches"]) - ids)
chk("ID niche model wujud di P1", not miss, ", ".join(miss) or f"{len(M['niches'])} niche dalam model")
sh = sum(n["share"] for n in M["niches"].values())
chk("Bahagian trafik model = 100%", abs(sh - 1) < 1e-9, f"{sh:.2f}")
bad = [k for k, n in M["niches"].items() if abs(sum(n["idx"]) - 1200) > 1]
chk("Indeks musim purata 100 setiap niche", not bad, ", ".join(bad) or "11 niche × 12 bulan")
worst = 0
for r in F["profit_by_size"]:
    p, b, s = r["price_usd"], r["base_usd"], r["shipping_usd"] or 0
    worst = max(worst, abs(p - b - (0.06 * (p + s) + 0.22) - r["profit_usd"]))
chk("Untung P4 = harga − kos − (6% × (harga + shipping) + $0.22)", worst <= 0.06, f"23 produk; beza maks ${worst:.2f}")
for sc, v in M["results"].items():
    for per in ("steady", "year1"):
        tot = sum(m["profit"] for m in v[per]["months"])
        chk(f"Jumlah bulanan = jumlah tahunan ({sc}, {per})", abs(tot - v[per]["total"]["profit"]) <= 6, f"${tot:,} vs ${v[per]['total']['profit']:,}")
wave = {n["id"]: n["decision"] for n in N["niches"]}
for u in K["decision_updates"]:
    if "to" in u: wave[u["niche_id"]] = u["to"]
not_w1 = [k for k in M["niches"] if wave.get(k) != "Gelombang 1"]
chk("Model hanya guna niche Gelombang 1 (selepas kemas kini P2)", not not_w1, ", ".join(not_w1) or "11/11 Gelombang 1")
w1 = [k for k, v in wave.items() if v == "Gelombang 1"]
chk("Semua niche Gelombang 1 ada dalam model", set(w1) <= set(M["niches"]), f"{len(w1)} niche Gelombang 1")
nostyle = sorted(set(w1) - {s["niche_id"] for s in S["styles"]})
chk("Semua niche Gelombang 1 ada panduan gaya", not nostyle, ", ".join(nostyle) or "lengkap")

# ---------- 2. Daftar sumber ----------
STAGE = {"niches": "P1", "keywords": "P2", "styles": "P3", "formats": "P4", "personas": "P5", "model": "P6"}
src = {}
def add(url, stage, claim, level):
    if not (isinstance(url, str) and url.startswith("http")): return
    s = src.setdefault(url, {"url": url, "domain": urlparse(url).netloc.replace("www.", ""), "stages": set(), "claims": [], "level": level or "pihak_ketiga"})
    s["stages"].add(stage)
    if claim and claim not in s["claims"]: s["claims"].append(claim)
    rank = {"rasmi": 0, "pihak_ketiga": 1, "lemah": 2}
    if level in rank and rank[level] < rank.get(s["level"], 1): s["level"] = level
def walk(o, stage, claim=None, level=None):
    if isinstance(o, dict):
        c = o.get("claim") or o.get("rule") or o.get("keyword") or o.get("key") or o.get("format") or claim
        lv = o.get("level") if o.get("level") in ("rasmi", "pihak_ketiga", "lemah") else level
        for k, v in o.items():
            if k == "source": add(v, stage, c, lv)
            elif k == "sources" and isinstance(v, list):
                for u in v: add(u, stage, c, lv)
            else: walk(v, stage, c, lv)
    elif isinstance(o, list):
        for v in o: walk(v, stage, claim, level)
for f, st in STAGE.items(): walk(L(f), st)
main = {s["url"] for s in json.load(open(os.path.join(ROOT, "data", "sources.json")))["sources"]}
DOWNGRADE = {"aol.com": "Media yang memetik laporan Pinterest, bukan laporan asal",
             "homesandgardens.com": "Media hiasan rumah", "minted.com": "Vendor (kedai)"}
for v in src.values():
    if v["domain"] in DOWNGRADE and v["level"] == "rasmi": v["level"] = "pihak_ketiga"; v["reclassified"] = DOWNGRADE[v["domain"]]
reg = sorted(src.values(), key=lambda s: ({"rasmi": 0, "pihak_ketiga": 1, "lemah": 2}[s["level"]], s["domain"]))
for i, s in enumerate(reg, 1):
    s["id"] = f"PS{i:03d}"; s["stages"] = sorted(s["stages"]); s["in_main_registry"] = s["url"] in main
counts = Counter(s["level"] for s in reg)
doms = Counter(s["domain"] for s in reg).most_common(8)

# ---------- 3. Percanggahan ----------
conflicts = [
 {"topic": "Punca pulangan baju kerana saiz/fit", "values": "~53% (Coresight, 2023) | ~56% (Loop, 2026)", "resolution": "Guna julat 53–56%; kedua-dua sokong poster lebih rendah risiko"},
 {"topic": "Bahagian isi rumah US menyewa", "values": "~1/3 (pemilikan 65.2%, USAFacts 2025) | ~35% / 44.6 juta (VerticalRent)", "resolution": "Konsisten; guna ~1/3"},
 {"topic": "Gelombang niche kaunselor", "values": "Gelombang 2 (skor P1 = 22) | Gelombang 1 (peluang kata kunci 276, P2)", "resolution": "Guna Gelombang 1 (data kata kunci lebih kukuh)"},
 {"topic": "Home office: permintaan vs saingan", "values": "Pinterest 'chic cubicle decor' +1,543% | 'office art' 4.86 juta listing Etsy", "resolution": "Kekal Gelombang 1; sasar long-tail sahaja"},
 {"topic": "Volum 'bookish print'", "values": "40,500/bulan (RankHero) | kata kunci sejenis jauh lebih rendah", "resolution": "Tidak digunakan dalam model sehingga disahkan"},
 {"topic": "Margin printable digital", "values": "~100% (tiada kos cetak) | ~92% (selepas fee bayaran 6% + $0.22)", "resolution": "Guna 92%"},
 {"topic": "Kos canvas 16×20 & 24×36", "values": "Min $10.63 (saiz terkecil, Printify) | anggaran $15–22 dan $25–35", "resolution": "Model guna anggaran ($18.50, $30); sahkan dalam editor Printify"},
 {"topic": "Shipping berbingkai/canvas/metal", "values": "Tiada angka rasmi ikut saiz | anggaran $8–12", "resolution": "Guna anggaran; sahkan dalam editor Printify"},
 {"topic": "Belanja cikgu dari duit sendiri", "values": "$600 (DonorsChoose/EdWeek 2025-26) | ~$895 (AdoptAClassroom)", "resolution": "Guna $600 (terkini)"},
]

# ---------- 4. Eksport untuk tab Poster ----------
print("Eksport ke data/export/posters/:")
by_profit = M["by_niche_steady"]
style = {s["niche_id"]: s for s in S["styles"]}
topkw = {}
for k in K["keywords"]:
    if k["intent"] != "khusus" or not k.get("google_monthly") or "perlu disemak" in k["note"]: continue
    cur = topkw.get(k["niche_id"])
    if not cur or k["google_monthly"] > cur["google_monthly"]: topkw[k["niche_id"]] = k
rows = []
for rank, n in enumerate(sorted(N["niches"], key=lambda x: (-x["total"], -by_profit.get(x["id"], 0))), 1):
    m, st, kw, ev = M["niches"].get(n["id"], {}), style.get(n["id"], {}), topkw.get(n["id"], {}), (n["evidence"] or [{"claim": "Tiada bukti khusus; skor rendah (permintaan Pinterest lemah)", "level": "lemah", "source": ""}])[0]
    rows.append({"rank": rank, "id": n["id"], "niche": n["niche"], "group": n["group"],
        "demand": n["demand"], "competition": n["competition"], "typography_fit": n["typography_fit"],
        "pinterest_fit": n["pinterest_fit"], "order_value": n["order_value"], "automation": n["automation"],
        "total": n["total"], "season": n["season"], "peak_months": n["peak_months"], "wave": wave[n["id"]],
        "pin_window": m.get("pin", ""), "annual_profit": by_profit.get(n["id"]), "profit_per_order": m.get("profit"),
        "traffic_share_pct": round(m["share"] * 100) if m else None, "product_mix": m.get("mix", st.get("format", "")),
        "style": st.get("style", ""), "palette": st.get("palette", ""), "fonts": st.get("fonts", ""),
        "pin_overlay": st.get("pin_overlay", ""), "top_keyword": kw.get("keyword", ""),
        "top_keyword_volume": kw.get("google_monthly"), "top_keyword_opportunity": kw.get("opportunity"),
        "key_evidence": ev["claim"], "evidence_level": ev["level"], "source": ev["source"]})
W("poster_niches.json", rows)
NN = {n["id"]: n["niche"] for n in N["niches"]} | {"sets": "Set (semua bilik)"}
W("poster_keywords.json", [{"niche": NN.get(k["niche_id"], k["niche"]), "keyword": k["keyword"],
    "google_monthly": k["google_monthly"], "etsy_listings": k["etsy_listings"], "opportunity": k["opportunity"],
    "intent": k["intent"], "note": k["note"], "source": k["source"]} for k in K["keywords"]])
W("poster_formats.json", [{"format": f["format"], "base_min_usd": f["base_min_usd"], "premium_min_usd": f.get("premium_min_usd"),
    "use": f["use"], "recommendation": f["recommendation"], "level": f["level"], "source": f["source"]} for f in F["formats"]])
W("poster_profit.json", [{"product": r["key"], "format": r["format"], "size": r["size"], "base_usd": r["base_usd"],
    "shipping_usd": r["shipping_usd"], "price_usd": r["price_usd"], "profit_usd": r["profit_usd"], "margin_pct": r["margin_pct"],
    "cost_note": r["cost_note"] or "Rasmi", "shipping_note": r["shipping_note"]} for r in F["profit_by_size"]])
W("poster_personas.json", [{"persona": p["persona"], "niches": p["niches"], "who": p["who"], "how": p["how"],
    "frequency": p["frequency"], "when": p["when"], "products": p["products"], "budget": p["budget"],
    "evidence": p["evidence"][0]["claim"] if p["evidence"] else "", "level": p["evidence"][0]["level"] if p["evidence"] else "",
    "source": p["evidence"][0]["source"] if p["evidence"] else ""} for p in PE["personas"]])
R = M["results"]
W("poster_monthly.json", [{"month": MONTHS[i], "month_no": i + 1,
    "profit_steady": R["asas"]["steady"]["months"][i]["profit"], "orders_steady": R["asas"]["steady"]["months"][i]["orders"],
    "revenue_steady": R["asas"]["steady"]["months"][i]["revenue"], "profit_year1": R["asas"]["year1"]["months"][i]["profit"],
    "profit_pessimistic": R["pesimis"]["steady"]["months"][i]["profit"], "profit_optimistic": R["optimis"]["steady"]["months"][i]["profit"]}
    for i in range(12)])
W("poster_seasonality.json", [{"niche": n["name"], "niche_id": k, "month": MONTHS[i], "month_no": i + 1, "index": n["idx"][i],
    "profit": R["asas"]["steady"]["months"][i][k]} for k, n in M["niches"].items() for i in range(12)])
LBL = {"pesimis": ("Pesimis", "Trafik ×0.5, conversion ×0.67"), "asas": ("Asas", "3,000 pelawat/bulan, conversion 1.2–1.5%"), "optimis": ("Optimis", "Trafik ×2")}
W("poster_scenarios.json", [{"scenario": LBL[s][0], "assumption": LBL[s][1], "profit_steady": v["steady"]["total"]["profit"],
    "orders_steady": v["steady"]["total"]["orders"], "revenue_steady": v["steady"]["total"]["revenue"],
    "profit_year1": v["year1"]["total"]["profit"], "orders_year1": v["year1"]["total"]["orders"]} for s, v in R.items()])
W("poster_pin_playbook.json", [{"type": "Templat", "item": t["id"] + " " + t["template"], "share_pct": t["share_pct"], "level": "", "source": ""}
    for t in S["pin_templates_wallart"]] + [{"type": "Peraturan", "item": r["rule"], "share_pct": None, "level": r["level"], "source": r["source"]} for r in S["pin_rules"]])
W("poster_sources.json", [{"id": s["id"], "domain": s["domain"], "level": s["level"], "stages": ", ".join(s["stages"]),
    "claim": s["claims"][0] if s["claims"] else "", "url": s["url"]} for s in reg])
W("poster_conflicts.json", conflicts)
W("poster_checks.json", checks)

reg_out = {"stage": "P7", "updated": "2026-11-21",
    "verification": {"status": "Disemak melalui indeks carian; belum disemak secara langsung pada halaman asal (rangkaian persekitaran ini menyekat domain sumber)",
                     "levels": {"rasmi": "Platform/organisasi asal (Printify, Pinterest, CDC, Census, EdWeek, NRF)", "pihak_ketiga": "Tool kata kunci, blog vendor, media", "lemah": "Satu sumber/anekdot"}},
    "reclassified": [{"domain": d, "from": "rasmi", "to": "pihak_ketiga", "reason": r} for d, r in DOWNGRADE.items()],
    "counts": {"total": len(reg), **counts, "also_in_main_registry": sum(s["in_main_registry"] for s in reg)},
    "top_domains": doms, "checks": checks, "conflicts": conflicts, "sources": reg}
json.dump(reg_out, open(P("sources.json"), "w"), indent=2, ensure_ascii=False)
print("Sumber:", reg_out["counts"]); print("Domain teratas:", doms)
print("Semakan:", Counter(c["status"] for c in checks))
for c in checks: print(" ", c["status"], c["check"], "|", c["detail"])
