"""Fon F3: gambar specimen 12 fon pilihan setiap mood -> docs/research/fonts/specimens/<mood>.png
Input: data/export/fonts/fonts_picks.json, fonts_moods.json (dari scripts/build_fonts.py)
Fail fon dimuat turun ke FONT_CACHE (tidak disimpan dalam repo; lesen FFL melarang edar semula).
Perlu: Playwright + Chromium. Jalankan: FONT_CACHE=/tmp/fontcache python3 scripts/fonts_specimens.py [mood ...]"""
import json, os, re, subprocess, sys, zipfile, html

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EXP = os.path.join(ROOT, "data", "export", "fonts")
OUT = os.path.join(ROOT, "docs", "research", "fonts", "specimens")
CACHE = os.environ.get("FONT_CACHE", "/tmp/pod-font-cache")
FDIR = os.path.join(CACHE, "files"); os.makedirs(FDIR, exist_ok=True); os.makedirs(OUT, exist_ok=True)

SAMPLE = {"berus": "Dream Big", "romantik": "Forever Yours", "tangan": "Home Sweet Home", "lucu": "Wash Your Hands",
          "kanak": "Little Explorer", "tenang": "Breathe Slowly", "motivasi": "NO EXCUSES", "retro": "Stay Groovy",
          "klasik": "Read More Books", "mewah": "The Good Life", "rustik": "Fresh Laundry", "gotik": "Merry Christmas",
          "seram": "Trick or Treat", "grunge": "Stay Wild", "moden": "Less Is More", "tekno": "Game On"}
BG = {"berus": ("#f3ece4", "#5b3a4a"), "romantik": ("#f6eeee", "#6d3b4c"), "tangan": ("#f7f3ea", "#3d4a3a"), "lucu": ("#fff4d6", "#d0482c"),
      "kanak": ("#eef5f1", "#3f7a68"), "tenang": ("#eef1ec", "#5d6f5a"), "motivasi": ("#1d1d1f", "#f5f5f5"), "retro": ("#f6e3c3", "#b4532a"),
      "klasik": ("#f4efe3", "#2f3a4a"), "mewah": ("#13332f", "#e3c78a"), "rustik": ("#efe6d6", "#3b2f25"), "gotik": ("#2a1416", "#e9dcc7"),
      "seram": ("#151515", "#ff7a1a"), "grunge": ("#d9d6d0", "#1f1f1f"), "moden": ("#ffffff", "#111111"), "tekno": ("#0e1726", "#6ee7f9")}

def curl(url, path):
    r = subprocess.run(["curl", "-sfL", "-m", "90", "-o", path, url])
    return r.returncode == 0 and os.path.exists(path) and os.path.getsize(path) > 0

def pick_member(names, prefer_bold):
    c = [n for n in names if n.lower().endswith((".ttf", ".otf")) and "variable" not in n.lower() and ".." not in n and not n.startswith("/") and "__MACOSX" not in n]
    want = ("-Bold.", "-Black.", "-ExtraBold.") if prefer_bold else ("-Regular.", "-Medium.", "Regular")
    c.sort(key=lambda n: (not any(w in n for w in want), "/WEB/" in n, n))
    return c[0] if c else None

def font_file(p, bold):
    key = re.sub(r"\W+", "_", f"{p['src']}_{p['name']}_{int(bold)}")
    for ext in (".ttf", ".otf"):
        if os.path.exists(os.path.join(FDIR, key + ext)): return os.path.join(FDIR, key + ext)
    if p["src"] == "google":
        fam = p["name"].replace(" ", "+")
        css = subprocess.run(["curl", "-sfL", "-m", "60", f"https://fonts.googleapis.com/css2?family={fam}" + (":wght@700" if bold else "")], capture_output=True, text=True).stdout
        for alt in ("", ":wght@" + re.split(r"\D", str(p.get("w", "400")))[0]):
            if css: break
            css = subprocess.run(["curl", "-sfL", "-m", "60", f"https://fonts.googleapis.com/css2?family={fam}{alt}"], capture_output=True, text=True).stdout
        m = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css)
        dst = os.path.join(FDIR, key + ".ttf")
        return dst if m and curl(m.group(1), dst) else None
    slug = p["url"].rstrip("/").split("/")[-1]
    zp = os.path.join(CACHE, p["src"], slug + ".zip"); os.makedirs(os.path.dirname(zp), exist_ok=True)
    url = f"https://api.fontshare.com/v2/fonts/download/{slug}" if p["src"] == "fontshare" else f"https://www.fontsquirrel.com/fonts/download/{slug}"
    if not os.path.exists(zp) and not curl(url, zp): return None
    if not zipfile.is_zipfile(zp): return None
    z = zipfile.ZipFile(zp); m = pick_member(z.namelist(), bold)
    if not m: return None
    dst = os.path.join(FDIR, key + os.path.splitext(m)[1].lower())
    open(dst, "wb").write(z.read(m)); return dst

def render(mood, picks, meta):
    bg, fg = BG[mood]; bold = mood in ("motivasi",)
    faces, cards = [], []
    for i, p in enumerate(picks):
        f = font_file(p, bold)
        if not f: print("   tiada fail:", p["name"]); continue
        faces.append(f"@font-face{{font-family:'f{i}';src:url('file://{f}')}}")
        lic = html.escape(p["lic"]); w = html.escape(p["w"])
        cards.append(f"""<div class=c><div class=s style="font-family:'f{i}'">{html.escape(SAMPLE[mood])}</div>
<div class=a style="font-family:'f{i}'">Aa Bb Cc Gg 123 &amp;</div><div class=n><b>{p['rank']}. {html.escape(p['name'])}</b> · {p['src']} · {lic} · berat {w}</div></div>""")
    doc = f"""<!doctype html><html><head><meta charset=utf-8><style>{''.join(faces)}
body{{margin:0;padding:36px;width:1200px;background:#e9e6e1;font-family:Arial,sans-serif}}
h1{{margin:0 0 4px;font-size:26px;color:#222}} .d{{color:#555;font-size:15px;margin-bottom:22px}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
.c{{background:{bg};color:{fg};border-radius:6px;padding:22px 18px 14px;height:196px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.12)}}
.s{{font-size:58px;line-height:1.15;white-space:nowrap;text-align:center}} .a{{font-size:24px;opacity:.8;text-align:center;white-space:nowrap}}
.n{{font-size:12.5px;opacity:.85;border-top:1px solid currentColor;padding-top:7px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
</style></head><body><h1>Mood: {html.escape(meta['label'])}</h1><div class=d>{html.escape(meta['desc'])} · Niche: {html.escape(', '.join(meta.get('niche_names') or meta['niches']))} · Pasangan teks: {html.escape(meta['pair'])} · Elak: {html.escape(meta['elak'])}</div>
<div class=g>{''.join(cards)}</div>
<script>document.fonts.ready.then(()=>{{document.querySelectorAll('.s,.a').forEach(e=>{{let s=parseFloat(getComputedStyle(e).fontSize);while(e.scrollWidth>e.clientWidth&&s>14){{s-=2;e.style.fontSize=s+'px'}}}});document.body.dataset.ok=1}})</script></body></html>"""
    hp = os.path.join(CACHE, f"spec_{mood}.html"); open(hp, "w").write(doc)
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1272,height:900}}}});
await p.goto('file://{hp}');await p.waitForSelector('body[data-ok]',{{timeout:60000}});await p.waitForTimeout(300);
await p.screenshot({{path:'{os.path.join(OUT, mood + '.png')}',fullPage:true}});await b.close()}})()"""
    subprocess.run(["node", "-e", js], check=True)
    print(f"  {mood}.png: {len(cards)} fon")

if __name__ == "__main__":
    picks = json.load(open(os.path.join(EXP, "fonts_picks.json")))
    moods = {m["id"]: m for m in json.load(open(os.path.join(EXP, "fonts_moods.json")))}
    for mood in (sys.argv[1:] or list(moods)):
        render(mood, [p for p in picks if p["mood"] == mood], moods[mood])
