"""Penjana latar poster + semakan kontras warna fon.
Tulis data/export/typography/poster_typo.json (dibaca oleh demo/tipografi/index.html).

Untuk setiap niche (rujuk docs/research/posters/03-styles.md):
- pasangan fon (paparan + sokongan), semua Google Fonts SIL OFL
- palet 5 warna (hex = pilihan sendiri berdasarkan nama palet P3, bukan data)
- warna teks dilaras automatik sehingga kontras >= 4.5:1 dengan SETIAP warna latar (WCAG 2.x SC 1.4.3)
- N varian latar SVG (gaya ikut niche, rawak bertitik semaian -> boleh dijana semula sama)

Guna: python3 scripts/poster_bg.py [--variants 4] [--svg-dir DIR]
--svg-dir: juga tulis fail SVG latar penuh (600x900, nisbah 2:3) untuk dibuka di Canva/Inkscape.
"""
import argparse, colorsys, json, math, os, random

ROOT = os.path.join(os.path.dirname(__file__), "..")
W, H = 600, 900  # nisbah 2:3 (12x18, 16x24, 24x36 in)

SOURCES = {
    "wcag": ("https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html", "rasmi"),
    "lum": ("https://www.w3.org/WAI/WCAG22/Techniques/general/G18.html", "rasmi"),
    "kern_gf": ("https://fonts.google.com/knowledge/glossary/kerning_kerning_pairs", "rasmi"),
    "pair_gf": ("https://fonts.google.com/knowledge/choosing_type/pairing_typefaces", "rasmi"),
    "matrix_gf": ("https://fonts.google.com/knowledge/choosing_type/pairing_typefaces_based_on_their_construction_using_the_font_matrix", "rasmi"),
    "kern_adobe": ("https://helpx.adobe.com/indesign/using/kerning-tracking.html", "rasmi"),
    "p3": ("docs/research/posters/03-styles.md", "dalaman"),
}

# niche: (nama, fon paparan, berat, fon sokongan, berat, prinsip pasangan, gaya latar, palet, teks contoh, baris kecil)
# palet: bg, bg2, shape, ink, accent
N = [
    ("classroom", "Kelas", "Shrikhand", 400, "Fredoka", 500, "Retro tebal + sans bulat: kontras bentuk, mood sama (mesra)", "arches",
     ["#F7E8CF", "#F3C9A0", "#E9A07A", "#2E3A59", "#C8553D"], "Mistakes help\nus grow", "ROOM 12 · BE KIND · TRY AGAIN"),
    ("counselor", "Kaunselor", "Quicksand", 700, "Nunito", 400, "Dua sans bulat: beza berat (700 lawan 400) jadi hierarki", "blobs",
     ["#EEF1E8", "#DCE5D3", "#B9CBB0", "#33463A", "#5D7A8C"], "Breathe in.\nBreathe out.", "CALM CORNER"),
    ("bathroom", "Bilik air", "Limelight", 400, "Poiret One", 400, "Dua fon Art Deco satu era; Limelight tebal, Poiret halus", "deco",
     ["#0F3D36", "#13493F", "#C9A646", "#F4EBD6", "#C9A646"], "Wash your\nhands, darling", "EST. 1925 · POWDER ROOM"),
    ("kitchen", "Dapur", "Alfa Slab One", 400, "Montserrat", 600, "Slab berat + sans geometri: satu kuat, satu senyap", "stripes",
     ["#F6EBDA", "#B23A2E", "#6B7A3A", "#2A1E17", "#B23A2E"], "Coffee\nfirst", "BREWED DAILY · OPEN 7AM"),
    ("home_office", "Home office", "Poiret One", 400, "Cormorant Garamond", 600, "Deco sans halus + serif klasik: beza klasifikasi, era dekat", "deco",
     ["#173B33", "#1E4A40", "#B08D57", "#F1E6D0", "#B08D57"], "Do the\nwork", "OFFICE HOURS · 9 TO 5"),
    ("reading_nook", "Reading nook", "Cormorant Garamond", 600, "EB Garamond", 400, "Satu genre (Garamond): beza saiz, italik dan huruf besar kecil", "frame",
     ["#EFE4CF", "#E6D7BA", "#5B3A29", "#2F2A1F", "#4A5D3A"], "Just one more\nchapter", "THE READING ROOM"),
    ("bedroom", "Bilik tidur", "Great Vibes", 400, "Playfair Display", 500, "Script + serif kontras tinggi: script untuk 1-3 perkataan sahaja", "gradient",
     ["#F3E6E1", "#E3CFCB", "#C9A9A6", "#3E2338", "#6E3D5E"], "Sweet\ndreams", "GOODNIGHT, LOVE"),
    ("living_room", "Ruang tamu", "Fraunces", 700, "Montserrat", 500, "Serif lembut + sans geometri: pasangan selamat untuk teks besar", "sunburst",
     ["#E8EEF2", "#D3DFE6", "#9FB7C4", "#1D3340", "#2F6F73"], "Home is\nwhere we are", "EST. 2026 · THE PARKERS"),
    ("nursery", "Nursery", "Caveat", 700, "Fredoka", 400, "Tulisan tangan + sans bulat: lembut, mudah dibaca", "arches",
     ["#F4EEE4", "#E8DCC8", "#C8D3BE", "#3B3A33", "#A26B4E"], "Dream big,\nlittle one", "OLIVER · 4.11.2026"),
    ("laundry", "Dobi", "Rye", 400, "Montserrat", 600, "Display western + sans neutral: satu fon hiasan sahaja", "frame",
     ["#E9EEF0", "#D8E2E6", "#7E9CAB", "#1F2A30", "#3E6A80"], "Laundry\nco.", "WASH · DRY · FOLD"),
    ("christmas", "Krismas", "Playfair Display", 700, "Great Vibes", 400, "Serif tebal sebagai utama, script sebagai aksen kecil", "grain",
     ["#6E1E23", "#5A181C", "#2F4A3A", "#F6ECDD", "#D8B26E"], "Merry &\nbright", "Season's greetings"),
    ("home_gym", "Home gym", "Bebas Neue", 400, "Oswald", 300, "Dua condensed: Bebas besar, Oswald 300 kecil; beza berat dan saiz", "stripes",
     ["#1B1C1E", "#26282B", "#3A3D42", "#F2F2F0", "#F2C230"], "No days\noff", "REP · SET · REPEAT"),
]

BAD_PAIRS = [  # contoh pasangan lemah untuk dibandingkan dalam demo
    ("Great Vibes", "Dancing Script", "Dua script bersaing; tiada hierarki, sukar dibaca dalam thumbnail Pinterest"),
    ("Bebas Neue", "Alfa Slab One", "Dua fon paparan berat; kedua-duanya menjerit"),
    ("Montserrat", "Poppins", "Terlalu serupa (dua sans geometri); nampak seperti silap, bukan pilihan"),
]


# ---------- warna & kontras (WCAG 2.x) ----------
def hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb2hex(c):
    return "#" + "".join(f"{round(max(0, min(1, v)) * 255):02X}" for v in c)


def lum(h):
    def lin(v): return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(v) for v in hex2rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def fix_ink(ink, backs, target=4.5):
    """Gelapkan/cerahkan ink (ikut arah latar) sehingga >= target dengan semua latar."""
    if min(ratio(ink, b) for b in backs) >= target:
        return ink, False
    dark_bg = sum(lum(b) for b in backs) / len(backs) < 0.18
    h, l, s = colorsys.rgb_to_hls(*hex2rgb(ink))
    for _ in range(100):
        l = min(1, l + 0.01) if dark_bg else max(0, l - 0.01)
        c = rgb2hex(colorsys.hls_to_rgb(h, l, s))
        if min(ratio(c, b) for b in backs) >= target:
            return c, True
    return ("#FFFFFF" if dark_bg else "#000000"), True


# ---------- penjana latar ----------
GRAIN = ('<filter id="g{n}"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="{s}"/>'
         '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0"/></filter>')


def f(v): return f"{v:.1f}".rstrip("0").rstrip(".")


def bg_grain(p, r, n):
    return f'<rect width="{W}" height="{H}" fill="{p[0]}"/>', [p[0]]


def bg_gradient(p, r, n):
    a = r.choice([(0, 0, 0, 1), (0, 0, 1, 1), (1, 0, 0, 1)])
    d = f'<linearGradient id="lg{n}" x1="{a[0]}" y1="{a[1]}" x2="{a[2]}" y2="{a[3]}"><stop offset="0" stop-color="{p[0]}"/><stop offset="1" stop-color="{p[1]}"/></linearGradient>'
    return d + f'<rect width="{W}" height="{H}" fill="url(#lg{n})"/>', [p[0], p[1]]


def bg_arches(p, r, n):
    """Pelangi boho di bucu bawah; zon teks (tengah) bebas bentuk."""
    out = [f'<rect width="{W}" height="{H}" fill="{p[0]}"/>']
    cx = r.choice([0, W, W / 2]); cy = H + r.randint(-20, 40)
    rad = r.randint(300, 380) if cx != W / 2 else r.randint(220, 270)
    cols = [p[2], p[1], p[0], p[1]]
    for i, c in enumerate(cols):
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(rad - i * rad / 4.6)}" fill="{c}"/>')
    if r.random() < .6:  # matahari kecil di atas
        out.append(f'<circle cx="{r.randint(90, 510)}" cy="{r.randint(70, 130)}" r="{r.randint(22, 38)}" fill="{p[2]}"/>')
    return "".join(out), [p[0]]


def bg_blobs(p, r, n):
    out = [f'<filter id="b{n}"><feGaussianBlur stdDeviation="40"/></filter><rect width="{W}" height="{H}" fill="{p[0]}"/><g filter="url(#b{n})" opacity=".85">']
    for _ in range(r.randint(3, 5)):
        x, y = r.choice([(r.randint(-60, 180), r.randint(-60, H + 60)), (r.randint(420, 660), r.randint(-60, H + 60))])
        out.append(f'<ellipse cx="{x}" cy="{y}" rx="{r.randint(110, 200)}" ry="{r.randint(90, 180)}" fill="{r.choice([p[1], p[2]])}"/>')
    return "".join(out) + "</g>", [p[0], p[1], p[2]]


def bg_sunburst(p, r, n):
    cx, cy = W / 2, r.choice([H + 40, H * .62])
    k = r.choice([24, 32, 40]); out = [f'<rect width="{W}" height="{H}" fill="{p[0]}"/>']
    R = 1400
    for i in range(0, k, 2):
        a0, a1 = 2 * math.pi * i / k, 2 * math.pi * (i + 1) / k
        out.append(f'<path d="M{f(cx)} {f(cy)}L{f(cx + R * math.cos(a0))} {f(cy + R * math.sin(a0))}L{f(cx + R * math.cos(a1))} {f(cy + R * math.sin(a1))}Z" fill="{p[1]}"/>')
    return "".join(out), [p[0], p[1]]


def bg_stripes(p, r, n):
    """Kanopi bistro di atas / jalur sisi gym."""
    out = [f'<rect width="{W}" height="{H}" fill="{p[0]}"/>']
    if r.random() < .5:  # kanopi beralun
        sw = r.choice([50, 60, 75]); hh = r.randint(90, 130)
        for i in range(0, W, sw * 2):
            out.append(f'<path d="M{i} 0h{sw}v{hh}a{sw / 2} {sw / 2} 0 0 1 -{sw} 0z" fill="{p[1]}"/>')
        out.append(f'<rect y="{H - 18}" width="{W}" height="18" fill="{p[2]}"/>')
    else:  # jalur sisi menegak
        n2 = r.choice([3, 4]); w2 = r.choice([10, 14, 18])
        for i in range(n2):
            x = 30 + i * (w2 + 10)
            out.append(f'<rect x="{x}" width="{w2}" height="{H}" fill="{p[2] if i % 2 else p[1]}"/>')
            out.append(f'<rect x="{W - x - w2}" width="{w2}" height="{H}" fill="{p[2] if i % 2 else p[1]}"/>')
    return "".join(out), [p[0]]


def bg_deco(p, r, n):
    """Kipas Art Deco: garisan emas nipis + bingkai berganda."""
    out = [f'<rect width="{W}" height="{H}" fill="{p[0]}"/>']
    sw = 1.6
    top = r.random() < .5
    cy = 0 if top else H
    for i in range(1, r.choice([6, 8, 10])):
        out.append(f'<circle cx="{W / 2}" cy="{cy}" r="{i * 28}" fill="none" stroke="{p[2]}" stroke-width="{sw}"/>')
    rays = r.choice([9, 13])
    for i in range(rays):
        a = math.pi * i / (rays - 1)
        y2 = cy + (1 if top else -1) * 260 * math.sin(a)
        out.append(f'<line x1="{W / 2}" y1="{cy}" x2="{f(W / 2 + 260 * math.cos(a))}" y2="{f(y2)}" stroke="{p[2]}" stroke-width="{sw}"/>')
    out.append(f'<rect x="24" y="24" width="{W - 48}" height="{H - 48}" fill="none" stroke="{p[2]}" stroke-width="2"/>')
    out.append(f'<rect x="34" y="34" width="{W - 68}" height="{H - 68}" fill="none" stroke="{p[2]}" stroke-width=".8"/>')
    return "".join(out), [p[0]]


def bg_frame(p, r, n):
    """Tanda vintage: bingkai berganda + sudut potong + bintik grain."""
    out = [f'<rect width="{W}" height="{H}" fill="{p[0]}"/>']
    m = r.choice([28, 36, 44]); c = r.choice([0, 24])
    def octo(m2):
        return (f'M{m2 + c} {m2}H{W - m2 - c}L{W - m2} {m2 + c}V{H - m2 - c}L{W - m2 - c} {H - m2}'
                f'H{m2 + c}L{m2} {H - m2 - c}V{m2 + c}Z')
    out.append(f'<path d="{octo(m)}" fill="none" stroke="{p[2]}" stroke-width="5"/>')
    out.append(f'<path d="{octo(m + 12)}" fill="none" stroke="{p[2]}" stroke-width="1.5"/>')
    if r.random() < .5:
        out.append(f'<rect x="{m + 12}" y="{m + 12}" width="{W - 2 * m - 24}" height="{H - 2 * m - 24}" fill="{p[1]}" opacity=".6"/>')
        return "".join(out), [p[0], p[1]]
    return "".join(out), [p[0]]


STYLES = {"grain": bg_grain, "gradient": bg_gradient, "arches": bg_arches, "blobs": bg_blobs,
          "sunburst": bg_sunburst, "stripes": bg_stripes, "deco": bg_deco, "frame": bg_frame}


def make_bg(style, p, seed, n):
    r = random.Random(seed)
    body, backs = STYLES[style](p, r, n)
    grain = GRAIN.format(n=n, s=seed % 997) + f'<rect width="{W}" height="{H}" filter="url(#g{n})" opacity=".09"/>'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">{body}{grain}</svg>'
    return svg, backs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variants", type=int, default=4)
    ap.add_argument("--svg-dir")
    a = ap.parse_args()
    out = []
    for i, (nid, name, d, dw, b, bw, why, style, pal, text, small) in enumerate(N):
        bg, bg2, shape, ink, acc = pal
        variants, allbacks = [], set()
        for v in range(a.variants):
            seed = 1000 * (i + 1) + v
            svg, backs = make_bg(style, pal, seed, f"{nid}{v}")
            allbacks.update(backs)
            variants.append({"seed": seed, "svg": svg})
            if a.svg_dir:
                os.makedirs(a.svg_dir, exist_ok=True)
                open(os.path.join(a.svg_dir, f"{nid}_{seed}.svg"), "w").write(svg)
        backs = sorted(allbacks)
        ink2, ink_fixed = fix_ink(ink, backs)
        acc_ok = min(ratio(acc, x) for x in backs) >= 4.5
        out.append({
            "id": nid, "name": name, "style": style,
            "display": {"family": d, "weight": dw}, "body": {"family": b, "weight": bw}, "why": why,
            "palette": {"bg": bg, "bg2": bg2, "shape": shape, "ink": ink2, "accent": acc},
            "ink_original": ink, "ink_fixed": ink_fixed,
            "text_behind": backs,
            "ink_min_ratio": round(min(ratio(ink2, x) for x in backs), 2),
            "accent_min_ratio": round(min(ratio(acc, x) for x in backs), 2),
            "small_color": acc if acc_ok else ink2,
            "text": text, "small": small, "variants": variants,
        })
    data = {
        "generated_by": "scripts/poster_bg.py", "ratio": "2:3", "viewbox": [W, H],
        "rules": {"aa_normal": 4.5, "aa_large": 3.0, "large_def": "18pt+, atau 14pt+ tebal"},
        "sources": {k: {"url": u, "level": l} for k, (u, l) in SOURCES.items()},
        "bad_pairs": [{"a": x, "b": y, "why": w} for x, y, w in BAD_PAIRS],
        "niches": out,
    }
    path = os.path.join(ROOT, "data", "export", "typography", "poster_typo.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w"), ensure_ascii=False, separators=(",", ":"))
    print(path, os.path.getsize(path), "bait")
    for n in out:
        print(f'{n["id"]:13} ink {n["ink_min_ratio"]:5}:1{" (dilaras)" if n["ink_fixed"] else ""}  aksen {n["accent_min_ratio"]:5}:1')


if __name__ == "__main__":
    main()
