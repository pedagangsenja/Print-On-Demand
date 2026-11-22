"""Bina senarai font Google Fonts untuk Font Generator.
Sahkan: (1) family wujud + weight sebenar via fonts.googleapis.com/css (v1),
(2) lesen via direktori google/fonts di GitHub (ofl/apache/ufl).
Output: data/export/fonts/font_list.json
"""
import json, re, sys, urllib.request, urllib.parse, concurrent.futures as cf
from datetime import date
from pathlib import Path

FONTS = {
 "sans": ["Inter","Inter Tight","Manrope","DM Sans","Work Sans","Public Sans","IBM Plex Sans","Archivo","Archivo Narrow","Barlow","Barlow Semi Condensed","Space Grotesk","Schibsted Grotesk","Hanken Grotesk","Familjen Grotesk","Bricolage Grotesque","Instrument Sans","Onest","Geist","Figtree","Plus Jakarta Sans","Outfit","Sora","Urbanist","Lexend","Albert Sans","Red Hat Display","Rubik","Karla","Mulish","Nunito Sans","Poppins","Montserrat","Raleway","Josefin Sans","Jost","Kumbh Sans","Epilogue","Syne","Unbounded","Darker Grotesque","Chivo","Overpass","Be Vietnam Pro","Libre Franklin","Roboto","Roboto Flex","Sofia Sans","Encode Sans","Tenor Sans","Michroma","Questrial","Didact Gothic","Mona Sans","Hubot Sans","Funnel Display","Host Grotesk","Golos Text","Wix Madefor Display","Afacad"],
 "condensed": ["Barlow Condensed","Roboto Condensed","Oswald","Anton","Bebas Neue","League Gothic","Fjalla One","Antonio","Big Shoulders Display","Six Caps","Teko","Saira Condensed","Sofia Sans Condensed","Sofia Sans Extra Condensed","Encode Sans Condensed","Pathway Gothic One","Archivo Black","Staatliches","Kanit","League Spartan","Tusker Grotesk"],
 "mono": ["Space Mono","JetBrains Mono","IBM Plex Mono","DM Mono","Courier Prime","Fragment Mono","Martian Mono","Azeret Mono","Geist Mono","Major Mono Display","Syne Mono"],
 "serif": ["Playfair Display","Playfair","DM Serif Display","DM Serif Text","Fraunces","Instrument Serif","Cormorant","Cormorant Garamond","EB Garamond","Libre Baskerville","Libre Caslon Display","Libre Caslon Text","Lora","Merriweather","Newsreader","Noto Serif Display","Bodoni Moda","Abril Fatface","Prata","Gloock","Young Serif","Spectral","Crimson Pro","Source Serif 4","IBM Plex Serif","Literata","Zilla Slab","Roboto Slab","Arvo","Rozha One","Yeseva One","Italiana","Marcellus","Cinzel","Gilda Display","Bellefair","Libre Bodoni","Old Standard TT","Domine","Alfa Slab One","Ultra","Gravitas One","Bagnard","Besley","Petrona","Hedvig Letters Serif","Imbue"],
 "script": ["Caveat","Dancing Script","Great Vibes","Pinyon Script","Allura","Sacramento","Parisienne","Homemade Apple","Reenie Beanie","Nothing You Could Do","La Belle Aurore","Mrs Saint Delafield","Monsieur La Doulaise","Birthstone","Ephesis","WindSong","Mea Culpa","Corinthia","Kalam","Shadows Into Light","Permanent Marker","Rock Salt","Gochi Hand","Patrick Hand","Pacifico","Lobster","Yellowtail","Satisfy","Kaushan Script","Mrs Sheppards","Herr Von Muellerhoff","Licorice"],
 "display": ["Righteous","Bungee","Rubik Mono One","Monoton","Shrikhand","Fredoka","Baloo 2","Chango","Climate Crisis","Dela Gothic One","Bowlby One","Titan One","Paytone One","Passion One","Rammetto One","Syncopate","Krona One","Zen Dots","Orbitron","Audiowide","Bungee Shade","Rubik Glitch","Bagel Fat One","Gasoek One","Rubik Dirt","Londrina Solid","Lilita One","Black Ops One","Bungee Outline","Tilt Warp","Silkscreen","Press Start 2P","VT323"],
}
WEIGHTS = "100,200,300,400,500,600,700,800,900"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "replace")

def check(fam):
    try:
        st, css = get("https://fonts.googleapis.com/css?family=" + urllib.parse.quote(fam) + ":" + WEIGHTS + "," + WEIGHTS.replace(",", "i,") + "i")
    except Exception as e:
        return fam, None, None, None, f"css: {e}"
    w = sorted({int(m.group(2)) for m in re.finditer(r"font-style: (normal);\s*font-weight: (\d+)", css)})
    it = sorted({int(m.group(1)) for m in re.finditer(r"font-style: italic;\s*font-weight: (\d+)", css)})
    if not w:
        return fam, None, None, None, "no weights"
    slug = re.sub(r"[^a-z0-9]", "", fam.lower())
    lic = None
    for d in ("ofl", "apache", "ufl"):
        try:
            st, meta = get(f"https://raw.githubusercontent.com/google/fonts/main/{d}/{slug}/METADATA.pb")
            if st == 200 and f'name: "{fam}"' in meta:
                m = re.search(r'license: "([A-Z0-9]+)"', meta)
                lic = m.group(1) if m else d.upper()
                break
        except Exception:
            pass
    return fam, w, it, lic, None

out, bad = [], []
fams = [(c, f) for c, l in FONTS.items() for f in l]
with cf.ThreadPoolExecutor(12) as ex:
    res = dict(((r[0]), r) for r in ex.map(lambda cf_: check(cf_[1]), fams))
for cat, fam in fams:
    _, w, it, lic, err = res[fam]
    if err or not lic:
        bad.append((fam, err or "lesen tidak disahkan"))
        continue
    out.append({"family": fam, "category": cat, "weights": w, "italics": it, "license": lic})
dest = Path(__file__).resolve().parent.parent / "data/export/fonts/font_list.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps({
  "generated": str(date.today()),
  "evidence": "rasmi",
  "sources": ["https://fonts.googleapis.com/css (weight)", "https://github.com/google/fonts (lesen METADATA.pb)", "https://developers.google.com/fonts/faq (guna komersial dibenarkan)"],
  "fonts": out}, ensure_ascii=False, indent=1))
print(len(out), "ok;", len(bad), "ditolak:", bad, file=sys.stderr)
