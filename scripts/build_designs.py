"""Build dashboard data for the Design tab.
Input : designs/svg-typo/out/<set>/picks.json + FINAL_30.txt, data/export/designs/<name>_assets.json (blob urls after upload)
Output: data/export/designs/motiv_posters.json, data/export/designs/sarkas_designs.json  ({rows, meta})
"""
import json, re, pathlib
R = pathlib.Path(__file__).resolve().parents[1]
CODE = pathlib.Path(__file__).read_text()
THEME = {"lazy": "Umum", "email": "Kerja", "coffeefirst": "Kopi / introvert", "momvoice": "Ibu / keluarga"}

def build(folder, assets_name, out_name, model_fmt, themes=None):
    M = R / "designs/svg-typo/out" / folder
    picks = json.load(open(M / "picks.json"))
    assets = json.load(open(R / "data/export/designs" / assets_name))
    quotes = {}
    for line in open(M / "FINAL_30.txt"):
        m = re.match(r"(\d+) (\w+) - (.+?)(\s{2,}\(.*)?$", line.rstrip())
        if m: quotes[m.group(2)] = (int(m.group(1)), m.group(3).strip())
    rows, theme = [], None
    for k, src in picks.items():
        no, q = quotes[k]
        if themes and k in themes: theme = themes[k]
        r = {"no": no, "id": k, "quote": q, "img": assets[k], "repaired": "fix/" in src,
             "model": "FLUX.2 klein 4B", "format": model_fmt,
             "file": f"designs/svg-typo/out/{folder}/final/{k}.png"}
        if themes: r["theme"] = theme
        rows.append(r)
    rows.sort(key=lambda r: r["no"])
    meta = [{"label": "build_designs.py", "value": CODE, "type": "code", "lang": "python"},
            {"label": "Input", "value": f"designs/svg-typo/out/{folder}/picks.json, FINAL_30.txt"}]
    p = R / "data/export/designs" / out_name
    p.write_text(json.dumps({"rows": rows, "meta": meta}, ensure_ascii=False, indent=1))
    print(len(rows), "rows ->", p.relative_to(R))

build("motiv", "motiv_assets.json", "motiv_posters.json", "864x1152 (3:4), hitam atas putih")
build("batch4", "sarkas_assets.json", "sarkas_designs.json", "1024x1024 SVG, hitam atas putih", THEME)
