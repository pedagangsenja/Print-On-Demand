"""Fon F1: ambil snapshot data fon dari sumber rasmi -> data/fonts/*.json
Sumber:
  - Google Fonts: repo github.com/google/fonts (METADATA.pb setiap keluarga + tags/all/families.csv)
  - Fontshare:    api.fontshare.com/v2/fonts (lesen, kategori, tag)
  - Font Squirrel: www.fontsquirrel.com/api/fontlist/all + fail lesen dalam zip setiap fon (bukan sans/serif biasa)
Jalankan: FONT_CACHE=/tmp/fontcache python3 scripts/fonts_fetch.py [google|fontshare|fontsquirrel ...]
Cache (zip, klon repo) disimpan di FONT_CACHE, bukan dalam repo."""
import csv, json, os, re, subprocess, sys, time, zipfile
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "data", "fonts")
CACHE = os.environ.get("FONT_CACHE", "/tmp/pod-font-cache")
os.makedirs(OUT, exist_ok=True); os.makedirs(CACHE, exist_ok=True)
TODAY = time.strftime("%Y-%m-%d")

def get(url, binary=False, tries=3):
    # guna curl: sesetengah laman (Font Squirrel) pulangkan 202 kosong kepada urllib
    for i in range(tries):
        r = subprocess.run(["curl", "-sfL", "-m", "60", url], capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout if binary else r.stdout.decode("utf-8", "replace")
        if i == tries - 1: raise RuntimeError(f"gagal: {url}")
        time.sleep(2 * (i + 1))

def save(name, meta, rows):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump({"meta": meta, "fonts": rows}, f, ensure_ascii=False, indent=0)
        f.write("\n")
    print(f"  {name}: {len(rows)} fon")

# ---------------- Google Fonts ----------------
def google():
    repo = os.path.join(CACHE, "google-fonts")
    if not os.path.isdir(os.path.join(repo, ".git")):
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--no-checkout",
                        "https://github.com/google/fonts.git", repo], check=True)
        subprocess.run(["git", "-C", repo, "sparse-checkout", "set", "--no-cone", "/*/*/METADATA.pb", "/tags/all/families.csv"], check=True)
        subprocess.run(["git", "-C", repo, "checkout", "-q", "main"], check=True)
    commit = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    # tag rasmi Google (skor 0-100 bagi /Expressive/*; ambil nilai maks setiap keluarga)
    tags = defaultdict(dict)
    for r in csv.reader(open(os.path.join(repo, "tags", "all", "families.csv"))):
        if len(r) >= 4 and r[2].startswith("/"):
            try: v = float(r[3])
            except ValueError: continue
            t = r[2][1:]
            tags[r[0]][t] = max(tags[r[0]].get(t, 0), v)
    rows = []
    for lic in ("ofl", "apache", "ufl"):
        for d in sorted(os.listdir(os.path.join(repo, lic))):
            p = os.path.join(repo, lic, d, "METADATA.pb")
            if not os.path.exists(p): continue
            t = open(p).read()
            top = t  # medan peringkat atas tiada inden; medan bersarang berinden
            one = lambda k: (re.search(rf'^{k}: "?([^"\n]*)"?', top, re.M) or [None, None])[1]
            many = lambda k: re.findall(rf'^{k}: "?([^"\n]*)"?', top, re.M)
            if one("is_noto") == "true": continue
            ps = one("primary_script")
            subs = many("subsets")
            if "latin" not in subs: continue
            styles = sorted({(int(w), s) for s, w in re.findall(r'fonts \{[^}]*?style: "(\w+)"[^}]*?weight: (\d+)', t, re.S)})
            axes = [{"tag": a, "min": float(lo), "max": float(hi)} for a, lo, hi in
                    re.findall(r'axes \{\s*tag: "(\w+)"\s*min_value: ([\d.]+)\s*max_value: ([\d.]+)', t)]
            name = one("name")
            rows.append({
                "name": name, "source": "google", "dir": f"{lic}/{d}",
                "license": {"ofl": "OFL-1.1", "apache": "Apache-2.0", "ufl": "UFL-1.0"}[lic],
                "license_url": f"https://github.com/google/fonts/tree/main/{lic}/{d}",
                "url": "https://fonts.google.com/specimen/" + name.replace(" ", "+"),
                "designer": one("designer"), "category": many("category"),
                "classifications": many("classifications"), "stroke": one("stroke"),
                "date_added": one("date_added"), "primary_script": ps,
                "weights": sorted({w for w, s in styles}), "italic": any(s == "italic" for w, s in styles),
                "axes": axes, "tags": tags.get(name, {}),
            })
    save("google.json", {"source": "https://github.com/google/fonts", "commit": commit, "fetched": TODAY,
                         "evidence": "rasmi", "note": "Hanya keluarga yang ada subset latin; Noto dikecualikan. Tag = google/fonts tags/all/families.csv (skor 0-100; Quality/* = skor kualiti lukisan dan jarak huruf)."}, rows)

# ---------------- Fontshare ----------------
FS_LIC = {"itf_ffl": "ITF-FFL-2.0", "sil_ofl": "OFL-1.1"}
def fontshare():
    d = json.loads(get("https://api.fontshare.com/v2/fonts?limit=500"))
    rows = []
    for f in d["fonts"]:
        st = f.get("styles") or []
        rows.append({
            "name": f["name"], "source": "fontshare", "slug": f["slug"],
            "license": FS_LIC.get(f.get("license_type"), f.get("license_type")),
            "license_url": "https://www.fontshare.com/licenses/itf-ffl" if f.get("license_type") == "itf_ffl" else "https://openfontlicense.org",
            "url": f"https://www.fontshare.com/fonts/{f['slug']}",
            "designer": ", ".join(x.get("name", "") for x in (f.get("designers") or []) if isinstance(x, dict)) or (f.get("publisher") or {}).get("name"),
            "category": [c.strip() for c in (f.get("category") or "").split(",") if c.strip()],
            "font_tags": [t.get("name") if isinstance(t, dict) else t for t in (f.get("font_tags") or [])],
            "date_added": (f.get("inserted_at") or "")[:10],
            "weights": sorted({(s.get("weight") or {}).get("weight") for s in st if isinstance(s.get("weight"), dict) and (s.get("weight") or {}).get("weight")}),
            "italic": any(s.get("is_italic") for s in st),
            "variable": any(s.get("is_variable") for s in st),
        })
    save("fontshare.json", {"source": "https://api.fontshare.com/v2/fonts", "fetched": TODAY, "count_total": d.get("count_total"),
                            "evidence": "rasmi", "note": "Lesen ITF FFL v2 disahkan dari fail License/FFL.txt dalam zip (benarkan kegunaan komersial; fail fon tidak boleh diedar)."}, rows)

# ---------------- Font Squirrel ----------------
FQ_KEEP = {"Script", "Handdrawn", "Calligraphic", "Display", "Retro", "Novelty", "Comic", "Blackletter", "Stencil", "Slab Serif", "Typewriter"}
def classify_license(text):
    t = re.sub(r"\s+", " ", text)
    low = t.lower()
    if "sil open font license" in low or "open font license" in low: return "OFL-1.1", "selamat"
    if "apache license" in low: return "Apache-2.0", "selamat"
    if "ubuntu font licence" in low: return "UFL-1.0", "selamat"
    if "gnu general public license" in low or "gpl" in low.split(): return "GPL", "semak"
    if re.search(r"public domain|cc0", low): return "Public-domain", "selamat"
    neg = re.search(r"(personal use only|not for commercial|non-commercial|for commercial use (please )?(contact|purchase|buy)|commercial license (is )?required|may not be sold|shall .{0,40}be sold or purchased)", low)
    pos = re.search(r"(free for (both )?(personal and commercial|commercial)|commercial use (is )?(allowed|permitted|ok)|use (it|them|this font) (for|in) commercial|free to use .{0,40}commercial|100% free)", low)
    if neg and pos: return "Lesen sendiri (bercanggah)", "berisiko"
    if neg: return "Lesen sendiri (had komersial)", "berisiko"
    if pos: return "Lesen sendiri (komersial dibenarkan)", "semak"
    return "Lesen sendiri (tidak jelas)", "berisiko"

def fontsquirrel():
    lp = os.path.join(CACHE, "fontsquirrel_fontlist.json")  # salinan senarai jika API disekat
    try:
        lst = json.loads(get("https://www.fontsquirrel.com/api/fontlist/all")); json.dump(lst, open(lp, "w"))
    except Exception:
        lst = json.load(open(lp)); print("  guna salinan senarai:", lp)
    gnames = set()
    gp = os.path.join(OUT, "google.json")
    if os.path.exists(gp): gnames = {f["name"].lower() for f in json.load(open(gp))["fonts"]}
    zdir = os.path.join(CACHE, "fontsquirrel"); os.makedirs(zdir, exist_ok=True)
    rows = []
    for x in lst:
        if x["classification"] not in FQ_KEEP: continue
        nm = x["family_name"].strip()
        if nm.lower() in gnames or nm.lower().replace(" ot", "") in gnames: continue
        zp = os.path.join(zdir, x["family_urlname"] + ".zip")
        if not os.path.exists(zp):
            try: b = get(f"https://www.fontsquirrel.com/fonts/download/{x['family_urlname']}", binary=True, tries=2)
            except Exception: b = None
            if b: open(zp, "wb").write(b)
            time.sleep(0.3)
        lic, risk, file_, snippet, nfont = "Tiada fail lesen", "berisiko", None, "", 0
        if os.path.exists(zp) and zipfile.is_zipfile(zp):
            z = zipfile.ZipFile(zp)
            names = [n for n in z.namelist() if not n.startswith("__MACOSX")]
            nfont = sum(n.lower().endswith((".ttf", ".otf")) for n in names)
            cands = [n for n in names if re.search(r"licen|ofl|eula|readme|read me|\.txt$", n, re.I) and not n.endswith("/")]
            texts = []
            for n in cands[:4]:
                try: texts.append(z.read(n)[:20000].decode("utf-8", "replace"))
                except Exception: pass
            if texts:
                file_ = cands[0]
                lic, risk = classify_license(" ".join(texts))
                m = re.search(r"[^.]{0,120}(commercial|personal use|open font license|freeware)[^.]{0,120}\.", re.sub(r"\s+", " ", " ".join(texts)), re.I)
                snippet = m.group(0).strip()[:240] if m else re.sub(r"\s+", " ", texts[0])[:200]
        else:
            lic, risk = "Muat turun gagal (fon dihos di laman pereka)", "tidak_disemak"
        rows.append({
            "name": nm, "source": "fontsquirrel", "slug": x["family_urlname"],
            "url": f"https://www.fontsquirrel.com/fonts/{x['family_urlname']}",
            "license_url": f"https://www.fontsquirrel.com/license/{x['family_urlname']}",
            "designer": x.get("foundry_name"), "category": [x["classification"]],
            "styles_count": int(x.get("family_count") or 0), "font_files": nfont,
            "license": lic, "risk": risk, "license_file": file_, "license_snippet": snippet,
        })
    save("fontsquirrel.json", {"source": "https://www.fontsquirrel.com/api/fontlist/all", "fetched": TODAY, "evidence": "rasmi (fail lesen dalam zip)",
                               "note": "Hanya kelas bukan sans/serif biasa dan bukan pendua Google Fonts. Lesen dikelaskan automatik dari teks fail lesen; 'semak' = baca sendiri sebelum guna."}, rows)

if __name__ == "__main__":
    for job in (sys.argv[1:] or ["google", "fontshare", "fontsquirrel"]):
        print(job); globals()[job]()
