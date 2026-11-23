"""Build dashboard data for the Design tab.
Input : designs/svg-typo/out/motiv/picks.json, FINAL_30.txt, data/export/designs/motiv_assets.json (blob urls after upload)
Output: data/export/designs/motiv_posters.json  {rows, meta}
"""
import json, re, pathlib
R = pathlib.Path(__file__).resolve().parents[1]
M = R / "designs/svg-typo/out/motiv"
picks = json.load(open(M / "picks.json"))
assets = json.load(open(R / "data/export/designs/motiv_assets.json"))
quotes = {}
for line in open(M / "FINAL_30.txt"):
    m = re.match(r"(\d+) (\w+) - (.+?)(\s{2,}\(.*)?$", line.rstrip())
    if m: quotes[m.group(2)] = (int(m.group(1)), m.group(3).strip())
rows = []
for k, src in picks.items():
    no, q = quotes[k]
    rows.append({"no": no, "id": k, "quote": q, "img": assets[k],
                 "repaired": "fix/" in src, "model": "FLUX.2 klein 4B",
                 "format": "864x1152 (3:4), hitam atas putih", "file": f"designs/svg-typo/out/motiv/final/{k}.png"})
rows.sort(key=lambda r: r["no"])
code = pathlib.Path(__file__).read_text()
out = {"rows": rows, "meta": [{"label": "build_designs.py", "value": code, "type": "code", "lang": "python"},
                              {"label": "Input", "value": "designs/svg-typo/out/motiv/picks.json, FINAL_30.txt"}]}
p = R / "data/export/designs/motiv_posters.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(rows), "rows ->", p.relative_to(R))
