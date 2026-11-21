"""Peringkat 7: bina daftar sumber + fail data gabungan untuk dashboard.
Jalankan: python3 scripts/build_registry.py"""
import json, os, re
from urllib.parse import urlparse
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(__file__), "..")
D = lambda f: os.path.join(ROOT, "data", f)
STAGE_FILES = {1: "niches.json", 2: "keywords.json", 3: "pins.json", 4: "products.json", 5: "personas.json", 6: "model.json"}
OFFICIAL = {"nrf.com", "cdc.gov", "printify.com", "help.printify.com", "newsroom.pinterest.com", "help.pinterest.com",
            "developers.pinterest.com", "theknot.com", "community.etsy.com", "help.erank.com", "etsy.com", "edweek.org",
            "ed.gov", "walmart.com", "axios.com", "teacherspayteachers.com"}

sources = {}
def level_for(url, given):
    host = urlparse(url).netloc.replace("www.", "")
    if given: return given
    return "rasmi" if host in OFFICIAL else "pihak_ketiga"

def add(url, stage, claim, level=None):
    if not url or not isinstance(url, str) or not url.startswith("http"): return
    s = sources.setdefault(url, {"url": url, "domain": urlparse(url).netloc.replace("www.", ""),
                                 "stages": set(), "claims": [], "level": level_for(url, level)})
    s["stages"].add(stage)
    if claim and claim not in s["claims"]: s["claims"].append(claim)
    if level == "rasmi": s["level"] = "rasmi"

def walk(obj, stage, ctx_claim=None, ctx_level=None):
    if isinstance(obj, dict):
        claim = obj.get("claim") or obj.get("rule") or obj.get("trend") or obj.get("keyword") or obj.get("name") or ctx_claim
        level = obj.get("level") if obj.get("level") in ("rasmi", "pihak_ketiga", "lemah") else ctx_level
        for k, v in obj.items():
            if k in ("source", "source_2") and isinstance(v, str): add(v, stage, claim, level)
            elif k == "sources" and isinstance(v, list):
                for u in v: add(u, stage, claim, level)
            else: walk(v, stage, claim, level)
    elif isinstance(obj, list):
        for v in obj: walk(v, stage, ctx_claim, ctx_level)

merged = {}
for stage, f in STAGE_FILES.items():
    data = json.load(open(D(f)))
    merged[f.replace(".json", "")] = data
    walk(data, stage)

reg = sorted(({**s, "stages": sorted(s["stages"])} for s in sources.values()), key=lambda x: (x["level"] != "rasmi", x["domain"]))
for i, s in enumerate(reg, 1): s["id"] = f"S{i:03d}"
counts = defaultdict(int)
for s in reg: counts[s["level"]] += 1

conflicts = [
  {"topic": "Kos Gildan 18000 (Printify)", "values": ["$15.24 (Podvector, pihak ketiga)", "$17.87 (halaman Printify)"], "resolution": "Guna $17.87 (rasmi)"},
  {"topic": "Kos mug 11oz (Printify)", "values": ["$6.45-8.25 (blog)", "$4.93 (halaman Printify, saiz/provider termurah)"], "resolution": "Guna $4.93; sahkan provider dalam editor"},
  {"topic": "Yuran Printify Premium", "values": ["$29/bulan (sumber lama)", "$39/bulan atau $299/tahun (ApparelHub 2026)"], "resolution": "BELUM SELESAI - semak printify.com/pricing"},
  {"topic": "Peratus wanita di Pinterest", "values": ["~70%", "71-72%"], "resolution": "Guna ~70%"},
  {"topic": "Belanja cikgu dari duit sendiri", "values": ["$600 (DonorsChoose 2025-26)", "~$895 (AdoptAClassroom, tahun tidak jelas)", "$655 (DonorsChoose 2024-25)"], "resolution": "Guna $600 (terkini, sampel 2,501)"},
  {"topic": "Bilangan majlis kahwin US", "values": ["2,011,044 (The Wedding Report 2025)", "2.5 juta 2026 (Zippia, tiada sumber)"], "resolution": "Guna 2.01 juta"},
  {"topic": "Volum 'teach shirt' & 'galentines' (RankHero)", "values": ["1,500,000", "1,000,000 (Feb)"], "resolution": "Dikecualikan sebagai anomali"}
]

verification = {
  "method": "Setiap angka dikumpul dari hasil carian web yang memetik halaman sumber. Halaman sumber TIDAK dapat dibuka terus dari persekitaran ini (rangkaian disekat; percubaan fetch 8 halaman utama gagal pada 2026-11-21).",
  "levels": {"rasmi": "Organisasi/platform asal (NRF, CDC, Printify, Pinterest, Etsy, The Knot, EdWeek, eRank)",
             "pihak_ketiga": "Tool kata kunci, blog vendor, media",
             "lemah": "Satu sumber, anekdot atau tiada metodologi"},
  "status": "Disemak melalui indeks carian; belum disemak secara langsung pada halaman asal",
  "next_step": "Benarkan akses rangkaian ke domain utama (nrf.com, cdc.gov, printify.com, theknot.com, rankhero.com) untuk semakan langsung, atau semak manual 10 angka kritikal."
}

out_sources = {"stage": 7, "updated": "2026-11-21", "verification": verification,
               "counts": {"total": len(reg), **counts}, "conflicts": conflicts, "sources": reg}
json.dump(out_sources, open(D("sources.json"), "w"), indent=2, ensure_ascii=False)
merged["registry"] = {"counts": out_sources["counts"], "conflicts": conflicts, "verification": verification}
json.dump(merged, open(D("dashboard.json"), "w"), indent=2, ensure_ascii=False)
print("sumber:", out_sources["counts"])
