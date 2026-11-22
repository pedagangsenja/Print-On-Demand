"""Fon F2: kelaskan fon ikut mood poster + pilih fon terbaik -> data/export/fonts/*.json
Input: data/fonts/google.json, fontshare.json, fontsquirrel.json (dari scripts/fonts_fetch.py),
       data/fonts/sites.json, data/fonts/licenses.json, data/fonts/research.json (kajian manual bersumber).
Jalankan: python3 scripts/build_fonts.py"""
import json, os
from collections import Counter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = lambda f: os.path.join(ROOT, "data", "fonts", f)
OUT = os.path.join(ROOT, "data", "export", "fonts")
os.makedirs(OUT, exist_ok=True)
L = lambda f: json.load(open(D(f)))
def W(name, rows):
    with open(os.path.join(OUT, name), "w") as f:
        f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n")
    print(f"  {name}: {len(rows)} baris")

# ---------- Mood poster ----------
# niche = id niche dari data/posters/niches.json; pair = fon teks kecil yang serasi
MOODS = [
    {"id": "berus", "label": "Berus / cat air", "desc": "Strok berus, tulisan dicat; hidup dan artistik", "niches": ["bedroom", "nursery", "affirmation", "faith"], "pair": "Montserrat, Quicksand", "elak": "Ayat panjang, huruf besar semua, saiz kecil"},
    {"id": "romantik", "label": "Romantik / elegan", "desc": "Script formal bersambung; anggun, majlis", "niches": ["bedroom", "wedding_signs", "seasonal_xmas"], "pair": "Cormorant Garamond, Montserrat", "elak": "Poster lucu atau gym; teks kecil"},
    {"id": "tangan", "label": "Tulisan tangan santai", "desc": "Macam ditulis pen/marker; mesra dan peribadi", "niches": ["nursery", "kitchen", "classroom", "affirmation"], "pair": "Nunito, Lato", "elak": "Poster mewah / pejabat formal"},
    {"id": "lucu", "label": "Lucu / pelik", "desc": "Bentuk melantun, tidak sekata; humor", "niches": ["bathroom", "kitchen", "laundry", "playroom"], "pair": "Poppins, Nunito", "elak": "Mesej serius, duka, keagamaan"},
    {"id": "kanak", "label": "Kanak-kanak / comel", "desc": "Bulat, tebal lembut; ceria", "niches": ["nursery", "classroom", "playroom"], "pair": "Quicksand, Nunito", "elak": "Pejabat, gym, mewah"},
    {"id": "tenang", "label": "Lembut / tenang", "desc": "Ringan, terbuka, jarak lapang; boho, kaunselor", "niches": ["counselor", "affirmation", "bedroom", "faith"], "pair": "Quicksand, Cormorant Garamond", "elak": "Humor kuat, motivasi agresif"},
    {"id": "motivasi", "label": "Kuat / motivasi", "desc": "Tebal, sempit (condensed), lantang", "niches": ["home_gym", "home_office", "dorm", "teen"], "pair": "Inter, Roboto Condensed", "elak": "Script halus; poster tidur/nursery"},
    {"id": "retro", "label": "Retro / groovy 60–70an", "desc": "Gemuk, melengkung, berbayang/inline", "niches": ["classroom", "kitchen", "dorm", "bathroom"], "pair": "DM Sans, Work Sans", "elak": "Minimalis moden, mewah"},
    {"id": "klasik", "label": "Klasik / akademik", "desc": "Serif buku tradisional; ilmu, sastera", "niches": ["reading_nook", "home_office", "faith"], "pair": "Lato, Source Sans 3", "elak": "Kanak-kanak, humor"},
    {"id": "mewah", "label": "Mewah / Art Deco", "desc": "Kontras tinggi (Didone), geometri Deco", "niches": ["bathroom", "home_office", "living_room"], "pair": "Montserrat, Josefin Sans", "elak": "Kanak-kanak, grunge"},
    {"id": "rustik", "label": "Rustik / farmhouse / western", "desc": "Slab kayu, tanda kedai lama", "niches": ["laundry", "kitchen", "entryway", "dining"], "pair": "Lato, Josefin Sans", "elak": "Mewah moden, futuristik"},
    {"id": "gotik", "label": "Gotik / medieval", "desc": "Blackletter, gaya manuskrip", "niches": ["seasonal_xmas", "seasonal_other", "reading_nook"], "pair": "EB Garamond, Cormorant", "elak": "Ayat panjang; kanak-kanak"},
    {"id": "seram", "label": "Seram / Halloween", "desc": "Menitis, retak, menakutkan", "niches": ["seasonal_other"], "pair": "Oswald, Bebas Neue", "elak": "Semua niche lain"},
    {"id": "grunge", "label": "Kasar / grunge", "desc": "Tekstur rosak, stensil, kasar", "niches": ["teen", "dorm", "man_cave", "home_gym"], "pair": "Oswald, Inter", "elak": "Nursery, perkahwinan"},
    {"id": "moden", "label": "Moden / minimalis", "desc": "Sans bersih geometri/grotesk", "niches": ["living_room", "home_office", "entryway"], "pair": "(gabung dengan serif atau script)", "elak": "—"},
    {"id": "tekno", "label": "Futuristik / tekno", "desc": "Piksel, segmen, sci-fi", "niches": ["teen", "dorm"], "pair": "Inter, Space Grotesk", "elak": "Hampir semua niche Gelombang 1"},
]
MID = [m["id"] for m in MOODS]

# ---------- Google: skor dari tag rasmi (0-100) ----------
def gmood(f):
    T = lambda k: f["tags"].get(k, 0)
    cat = set(f["category"]) | set(f.get("classifications") or [])
    hand, disp = "HANDWRITING" in cat, "DISPLAY" in cat
    nm = f["name"].lower()
    cond = any(w in nm for w in ("condensed", "compressed", "narrow", "bebas", "oswald", "anton", "gothic")) or (disp and any(a["tag"] == "wdth" and a["min"] < 100 for a in f["axes"]))
    heavy = max(f["weights"] or [400]) >= 700 or any(a["tag"] == "wght" and a["max"] >= 700 for a in f["axes"])
    avg = lambda *k: sum(T(x) for x in k) / len(k)
    s = {
        "berus": max(T("Theme/Brush"), 85 if "brush" in nm else 0),
        "romantik": max(T("Script/Formal"), avg("Expressive/Fancy", "Expressive/Sophisticated") if hand else 0, 0.8 * T("Seasonal/Valentine's Day") if hand else 0),
        "tangan": max(T("Script/Handwritten"), T("Script/Informal")) if T("Script/Formal") < 60 else 0,
        "lucu": max(T("Theme/Wacky"), T("Theme/Blobby"), avg("Expressive/Playful", "Expressive/Awkward", "Expressive/Happy") * 1.3 if (disp or hand) else 0) if not (T("Theme/Pixel") or "MONOSPACE" in cat) else 0,
        "kanak": max(T("Expressive/Childlike"), 0.9 * T("Expressive/Cute"), 0.8 * T("Sans/Rounded")),
        "tenang": (0.5 * T("Expressive/Calm") + 0.3 * T("Expressive/Sincere") + 0.4 * max(T("Sans/Rounded"), T("Script/Upright Script"))) if T("Expressive/Loud") < 40 and T("Expressive/Awkward") < 40 and T("Script/Formal") < 50 else 0,
        "motivasi": (avg("Expressive/Loud", "Expressive/Active", "Expressive/Competent") + (25 if cond else 0)) if not hand and T("Expressive/Loud") >= 60 and T("Sans/Rounded") < 50 and (cond or disp) and heavy else 0,
        "retro": max(0.8 * T("Theme/Blobby"), T("Theme/Shaded"), T("Theme/Inline"), T("Serif/Fat Face"), 0.9 * T("Expressive/Vintage") if disp and not hand else 0),
        "klasik": max(T("Serif/Old Style Garalde"), T("Serif/Humanist Venetian"), T("Serif/Transitional"), T("Serif/Scotch"), 0.8 * T("Serif/Modern")),
        "mewah": max(T("Theme/Art Deco"), T("Theme/Art Nouveau"), T("Serif/Didone"), 0.7 * T("Serif/Fat Face"), T("Expressive/Sophisticated")),
        "rustik": max(T("Theme/Woodtype"), T("Theme/Tuscan"), T("Slab/Clarendon"), avg("Expressive/Rugged", "Expressive/Vintage") if ("SERIF" in cat or "Slab/Humanist" in f["tags"] or "Slab/Geometric" in f["tags"]) else 0),
        "gotik": max(T("Theme/Blackletter"), T("Theme/Medieval")),
        "seram": T("Seasonal/Halloween"),
        "grunge": max(T("Theme/Distressed"), 0.8 * T("Theme/Stencil"), T("Expressive/Rugged") if T("Expressive/Loud") > 60 and disp else 0),
        "moden": max(T("Sans/Geometric"), T("Sans/Neo Grotesque"), T("Sans/Grotesque"), T("Sans/Superellipse"), 0.9 * T("Sans/Humanist")) if T("Sans/Rounded") < 50 else 0,
        "tekno": max(T("Expressive/Futuristic"), T("Theme/Techno"), T("Theme/Pixel")),
    }
    return {k: round(min(v, 100)) for k, v in s.items()}

# Kurasi visual Claude (bukti lemah: pemerhatian rupa, bukan tag rasmi)
CURATED = {
    "Kaushan Script": ["berus"], "Yesteryear": ["berus", "retro"], "Water Brush": ["berus"], "Sedgwick Ave": ["berus", "grunge"],
    "Comforter Brush": ["berus"], "Caveat Brush": ["berus", "tangan"], "Marck Script": ["berus", "romantik"], "Nanum Brush Script": ["berus", "tangan"],
    "Bebas Neue": ["motivasi"], "Oswald": ["motivasi"], "Anton": ["motivasi"], "League Gothic": ["motivasi"],
    "Shrikhand": ["retro", "lucu"], "Kalam": ["tangan"], "Rozha One": ["mewah"], "Modak": ["lucu", "kanak"], "Yatra One": ["retro"], "Fredoka": ["kanak"], "Baloo 2": ["kanak"], "Poiret One": ["mewah"], "Limelight": ["mewah"],
    "Rye": ["rustik"], "Alfa Slab One": ["rustik", "retro"], "Great Vibes": ["romantik"], "Dancing Script": ["romantik", "tangan"],
    "Quicksand": ["tenang"], "Nunito": ["tenang", "kanak"], "Comfortaa": ["tenang"], "Varela Round": ["tenang"], "Josefin Sans": ["tenang", "moden"],
    "Cormorant Garamond": ["klasik", "mewah"], "Montserrat": ["moden"], "Fraunces": ["klasik", "retro"],
    "Creepster": ["seram"], "Nosifer": ["seram"], "Butcherman": ["seram"], "Eater": ["seram"], "Frijole": ["seram", "lucu"],
}
NOT_MOOD = {"Kalam": ["berus"], "Yatra One": ["berus"]}  # tag rasmi tidak sepadan dengan rupa (kurasi visual)
FS_CUR = {
    "Array": ["tekno"], "Segment": ["tekno"], "Kola": ["tekno", "grunge"], "Bevellier": ["motivasi"], "Styro": ["motivasi"], "New Title": ["motivasi"],
    "Nippo": ["motivasi"], "Kihim": ["grunge", "motivasi"], "Boxing": ["retro", "motivasi"], "Chubbo": ["lucu", "kanak"], "Striper": ["retro", "lucu"],
    "Sharpie": ["berus", "motivasi"], "Stardom": ["mewah"], "Melodrama": ["mewah"], "Zina": ["mewah"], "Kohinoor Zerone": ["moden"],
    "Britney": ["retro", "romantik"], "Telma": ["berus", "romantik"], "Pencerio": ["romantik"], "Rosaline": ["romantik"], "Dancing Script": ["romantik", "tangan"],
    "Comico": ["lucu"], "Kalam": ["tangan", "kanak"], "Paquito": ["lucu", "kanak"], "Aktura": ["gotik"], "Anton": ["motivasi"], "Oswald": ["motivasi"],
    "Boska": ["mewah"], "Gambarino": ["mewah"], "Bonny": ["mewah", "retro"], "Bespoke Slab": ["rustik"], "Hoover": ["rustik"], "Trench Slab": ["rustik"],
}
FS_CAT = {"Serif": "klasik", "Sans": "moden", "Slab": "rustik", "Script": "romantik", "Handwritten": "tangan", "Blackletter": "gotik"}
FQ_CAT = {"Script": ["romantik", "tangan"], "Calligraphic": ["romantik"], "Handdrawn": ["tangan"], "Retro": ["retro"], "Novelty": ["lucu"],
          "Comic": ["lucu", "kanak"], "Blackletter": ["gotik"], "Stencil": ["grunge", "motivasi"], "Slab Serif": ["rustik"],
          "Typewriter": ["klasik", "grunge"], "Display": []}
TH = 60

def wrange(weights, axes):
    a = next((x for x in axes if x["tag"] == "wght"), None)
    if a: return f"{int(a['min'])}–{int(a['max'])} (variable)", int((a["max"] - a["min"]) / 100) + 1
    if not weights: return "–", 0
    return (f"{min(weights)}–{max(weights)}" if len(weights) > 1 else str(weights[0])), len(weights)

rows = []
G = L("google.json")
for f in G["fonts"]:
    sc = gmood(f)
    for m in CURATED.get(f["name"], []): sc[m] = max(sc[m], 90)
    for m in NOT_MOOD.get(f["name"], []): sc[m] = 0
    moods = sorted([m for m in MID if sc[m] >= TH], key=lambda m: -sc[m])
    q = [v for k, v in f["tags"].items() if k.startswith("Quality/")]
    wr, nw = wrange(f["weights"], f["axes"])
    rows.append({"name": f["name"], "src": "google", "lic": f["license"], "risk": "selamat", "cat": "/".join(c.title().replace("_", " ") for c in f["category"]),
                 "moods": moods, "score": {m: sc[m] for m in moods}, "basis": "tag rasmi Google" + (" + kurasi" if f["name"] in CURATED else ""),
                 "w": wr, "nw": nw, "it": f["italic"], "var": any(a["tag"] == "wght" for a in f["axes"]),
                 "q": round(sum(q) / len(q)) if q else None,
                 "season": [k.split("/")[1] for k, v in f["tags"].items() if k.startswith("Seasonal/") and v >= TH],
                 "by": f["designer"], "added": f["date_added"], "url": f["url"], "lic_url": f["license_url"],
                 **({"script": f["primary_script"]} if f.get("primary_script") not in (None, "Latn") else {}),
                 **({"learn": True} if f["tags"].get("Purpose/Learn To Write", 0) >= 50 or f["name"].startswith("Edu ") else {})})

for f in L("fontshare.json")["fonts"]:
    moods = list(FS_CUR.get(f["name"], []))
    for c in f["category"]:
        m = FS_CAT.get(c)
        if m and m not in moods and not (f["name"] in FS_CUR and c in ("Sans", "Serif", "Display")): moods.append(m)
    tg = {t.lower() for t in f["font_tags"]}
    if tg & {"funny", "fun", "comic", "comics"} and "lucu" not in moods: moods.append("lucu")
    if tg & {"kids", "children"} and "kanak" not in moods: moods.append("kanak")
    if tg & {"wedding", "luxury", "beauty", "fashion", "cosmetic"} and not moods: moods.append("mewah")
    wr, nw = wrange(f["weights"], [])
    rows.append({"name": f["name"], "src": "fontshare", "lic": f["license"], "risk": "selamat", "cat": "/".join(f["category"]),
                 "moods": moods, "score": {}, "basis": "kategori Fontshare" + (" + kurasi visual" if f["name"] in FS_CUR else ""),
                 "w": wr, "nw": nw, "it": f["italic"], "var": f.get("variable", False), "q": None, "season": [],
                 "by": f["designer"], "added": f["date_added"], "url": f["url"], "lic_url": f["license_url"]})

rejected, unchecked = [], 0
REV = {f["name"].lower(): f for f in L("fontsquirrel_reviewed.json")["fonts"]} if os.path.exists(D("fontsquirrel_reviewed.json")) else {}
if os.path.exists(D("fontsquirrel.json")):
    for f in L("fontsquirrel.json")["fonts"]:
        r = {"name": f["name"], "src": "fontsquirrel", "lic": f["license"], "risk": f["risk"], "cat": f["category"][0],
             "moods": FQ_CAT.get(f["category"][0], []), "score": {}, "basis": "kelas Font Squirrel",
             "w": "–", "nw": f["styles_count"], "it": False, "var": False, "q": None, "season": [],
             "by": f["designer"], "added": None, "url": f["url"], "lic_url": f["license_url"], "lic_note": f["license_snippet"]}
        rv = REV.pop(f["name"].lower(), None)
        if rv:  # lesen dibaca manual oleh ejen kajian (halaman lesen Font Squirrel)
            r.update({"lic": rv["license"], "risk": rv["risk"], "basis": "lesen disemak manual", "moods": rv["moods"] or r["moods"]})
        elif f["risk"] == "tidak_disemak":
            unchecked += 1; continue  # lesen tidak dapat dibaca: tidak masuk senarai
        (rows if r["risk"] in ("selamat", "semak") else rejected).append(r)
    for rv in REV.values():  # fon disemak ejen yang tiada dalam kelas yang diambil
        r = {"name": rv["name"], "src": "fontsquirrel", "lic": rv["license"], "risk": rv["risk"], "cat": "–", "moods": rv["moods"], "score": {},
             "basis": "lesen disemak manual", "w": "–", "nw": 1, "it": False, "var": False, "q": None, "season": [], "by": None, "added": None,
             "url": "https://www.fontsquirrel.com/fonts/" + rv["slug"], "lic_url": "https://www.fontsquirrel.com/license/" + rv["slug"], "lic_note": rv["license"]}
        (rows if rv["risk"] in ("selamat", "semak") else rejected).append(r)

# buang pendua nama (utamakan Google > Fontshare > Font Squirrel)
seen, master = set(), []
for r in rows:
    k = r["name"].lower()
    if k in seen: continue
    seen.add(k); master.append(r)
master.sort(key=lambda r: r["name"].lower())

# ---------- Pilihan teratas setiap mood ----------
NICHE = {n["id"]: n["niche"] for n in json.load(open(os.path.join(ROOT, "data", "posters", "niches.json")))["niches"]}
R = L("research.json") if os.path.exists(D("research.json")) else {}
picks_out, moods_out = [], []
for m in MOODS:
    c = [r for r in master if m["id"] in r["moods"] and r["risk"] == "selamat"]
    def rank(r):
        s = r["score"].get(m["id"], 75)
        other = max([v for k, v in r["score"].items() if k != m["id"]] or [0])
        s -= 0.3 * max(0, other - s)  # utamakan fon yang mood ini paling kuat
        q = r["q"] if r["q"] is not None else 70
        cur = 8 if "kurasi" in r["basis"] else 0
        return -(0.55 * s + 0.35 * q + min(r["nw"], 9) + cur)
    c.sort(key=rank)
    top, fam = [], set()
    for r in c:
        nm = r["name"]; first = nm.split()[0].lower()
        if (r["q"] is not None and r["q"] < 60) or first in fam or r.get("learn"): continue
        if r.get("script") and nm not in CURATED: continue  # skrip utama bukan Latin: huruf Latin selalunya sekunder
        if nm.endswith(" SC") or (" Mono" in nm and m["id"] != "tekno"): continue
        if m["id"] in ("lucu", "kanak", "retro") and "seram" in r["moods"]: continue
        top.append(r); fam.add(first)
        if len(top) == 12: break
    for i, r in enumerate(top):
        picks_out.append({"mood": m["id"], "rank": i + 1, "name": r["name"], "src": r["src"], "lic": r["lic"], "w": r["w"], "nw": r["nw"], "q": r["q"], "url": r["url"]})
    other = [r["name"] + (" (semak lesen)" if r["risk"] == "semak" else "") for r in master
             if m["id"] in r["moods"] and r["src"] != "google" and r["risk"] in ("selamat", "semak") and r["name"] not in [t["name"] for t in top]][:8]
    moods_out.append({**m, "niche_names": [NICHE.get(x, x) for x in m["niches"]], "count": len(c), "top": [r["name"] for r in top], "other": other, "evidence": R.get("moods", {}).get(m["id"], [])})

FQM = L("fontsquirrel.json")["meta"] if os.path.exists(D("fontsquirrel.json")) else {}
W("fonts_meta.json", [{"google_commit": G["meta"]["commit"][:10], "fetched": G["meta"]["fetched"], "fq_unchecked": unchecked,
                       "fq_fetched": FQM.get("fetched"), "total": len(master), "rejected": len(rejected)}])
W("fonts_master.json", master)
W("fonts_moods.json", moods_out)
W("fonts_picks.json", picks_out)
W("fonts_rejected.json", rejected)
for f in ("sites.json", "licenses.json"):  # specimen_urls.json = url gambar yang dimuat naik ke dashboard
    if os.path.exists(D(f)): W("fonts_" + f, L(f))
if os.path.exists(D("specimen_urls.json")): W("fonts_specimens.json", L("specimen_urls.json"))
for f in ():
    if os.path.exists(D(f)): W("fonts_" + f, L(f))
c = Counter(r["src"] for r in master)
print("  sumber:", dict(c), "| mood:", {m["id"]: m["count"] for m in moods_out})

# ---------- Dokumen ringkas (dijana) ----------
SPEC = os.path.join(ROOT, "docs", "research", "fonts", "specimens")
md = ["# Fon terbaik ikut mood (dijana)", "",
      "Dijana oleh `scripts/build_fonts.py` dari `data/export/fonts/`. Jangan ubah dengan tangan. Kaedah dan peraturan lesen: `README.md`.", "",
      f"Senarai induk: {len(master)} fon ({', '.join(f'{k} {v}' for k, v in c.items())}); ditolak kerana lesen berisiko: {len(rejected)}; fon Font Squirrel yang lesennya tidak dapat dibaca (muat turun disekat): {unchecked}.", ""]
for m in moods_out:
    md += [f"## {m['label']} ({m['count']} fon)", "", f"{m['desc']}. Niche: {', '.join(m['niche_names'])}. Teks pasangan: {m['pair']}. Elak: {m['elak']}.", ""]
    if os.path.exists(os.path.join(SPEC, m["id"] + ".png")): md += [f"![{m['label']}](specimens/{m['id']}.png)", ""]
    for p in [p for p in picks_out if p["mood"] == m["id"]]:
        md.append(f"{p['rank']}. [{p['name']}]({p['url']}) · {p['src']} · {p['lic']} · ketebalan {p['w']}" + (f" · kualiti {p['q']}" if p["q"] is not None else ""))
    if m["other"]: md.append("\nLebih unik (luar Google Fonts): " + ", ".join(m["other"]))
    for e in m["evidence"]: md.append(f"\nBukti: {e['claim']} ([sumber]({e['url']}), {e['level']})")
    md.append("")
open(os.path.join(ROOT, "docs", "research", "fonts", "fonts-by-mood.md"), "w").write("\n".join(md) + "\n")
print("  docs/research/fonts/fonts-by-mood.md")
