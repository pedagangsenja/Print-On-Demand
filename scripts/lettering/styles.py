"""Enam gaya lettering (S1-S6) dan pembina prompt.

Setiap gaya diterangkan daripada ciri UMUM poster rujukan pengguna (upload 23 Nov 2026,
design orang lain = rujukan gaya sahaja; ayat, susun atur dan tandatangan tidak disalin).
Warna dalam prompt guna nama (bukan kod hex) supaya model tidak menulis kod sebagai teks;
warna tepat dipaksa kemudian oleh finish.py melalui `bg` dan `inks`.

Guna: python3 scripts/lettering/styles.py <out_prompts.json> [quote_id[,quote_id...] | all10]
"""
import json
import sys

COMMON_TAIL = ("No other text, no letters except the quoted words, no signature, no watermark, "
               "no frame, no border, no mockup, flat 2D artwork.")

STYLES = {
    "S1": {
        "name": "Huruf besar melantun (3 warna, vektor rata)",
        "ref": "IMG_5781",
        "bg": "#1d2742", "inks": ["#f4f1ea", "#f2a03d", "#b9bfcc"], "texture": "none",
        "tpl": ("Flat vector hand-lettering quote poster, portrait. Solid dark navy blue background. "
                "In the center, a compact rectangular block of playful hand-drawn uppercase letters with a "
                "bouncy baseline: every letter has a slightly different size and tilt, letters touch and "
                "interlock tightly, thick rounded strokes, like a modern hand-lettering illustration. "
                "The text reads exactly, three lines: line 1 \"{w1u}\" in off-white, line 2 \"{w2u}\" in warm "
                "orange, line 3 \"{w3u}\" in light gray and \"{w4u}\" in off-white. Small round confetti dots in "
                "off-white and orange scattered around the block. Generous empty navy margins. "
                "No outline, no shadow, no gradient, no texture. "),
    },
    "S2": {
        "name": "Skrip vintaj + huruf kecil (krim atas hitam)",
        "ref": "IMG_5778",
        "bg": "#0d0d0d", "inks": ["#efe6d2"], "texture": "grain",
        "tpl": ("Vintage sign-painter hand lettering quote, portrait. Solid matte black background. "
                "Centered stacked lettering in warm cream ink. The text reads exactly, four lines: "
                "\"{w1u}\" in small widely spaced uppercase letters; \"{w2c}\" in a large bold flowing brush script "
                "with a curling entry swash; \"{w3u}\" in small widely spaced uppercase letters; \"{w4c}\" in a large "
                "bold flowing brush script whose last letter ends in a long swash tail that sweeps under the word. "
                "The script words are much larger than the small uppercase words. Tight vertical spacing, the "
                "swashes tie the lines into one lockup. Wide empty black margins. Cream on black only. "),
    },
    "S3": {
        "name": "Kaligrafi berus ekspresif + percikan",
        "ref": "IMG_5732",
        "bg": "#0b0b0b", "inks": ["#ffffff"], "texture": "none",
        "tpl": ("Expressive brush calligraphy quote, portrait. Pure black background, pure white ink. "
                "The text reads exactly, four lines: \"{w1c}\" / \"{w2l}\" / \"{w3l}\" / \"{w4l}\", written in tall, "
                "slanted, energetic dry-brush script with strong thick-and-thin contrast, lines slightly "
                "overlapping. Long sweeping hairline swash strokes loop around and between the words, and fine "
                "ink splatter dots surround the lettering. Centered with empty margins. White on black only. "),
    },
    "S4": {
        "name": "Berus santai bertekstur kapur",
        "ref": "IMG_5735",
        "bg": "#1c1c1c", "inks": ["#f1efe9"], "texture": "chalk",
        "tpl": ("Casual hand-lettered quote in chalk, portrait. Dark charcoal slate background. Off-white "
                "chalk-textured brush lettering with slightly rough dry edges, a playful mix of upright and "
                "slanted letters. The text reads exactly, three lines: \"{w1c} {w2l}\" in medium casual brush letters, "
                "\"{w3u}\" in large bold brush capitals, \"{w4l}\" in a large bouncy brush script. A few tiny chalk "
                "dots and small stars around. Centered and compact with generous margins. "),
    },
    "S5": {
        "name": "Blok huruf tangan lusuh",
        "ref": "IMG_5730",
        "bg": "#0a0a0a", "inks": ["#f5f5f2"], "texture": "worn",
        "tpl": ("Hand-drawn typographic quote, portrait. Solid black background. White lettering with a "
                "distressed worn letterpress texture, small speckles and scratches. The text reads exactly, three "
                "lines forming a tight justified block: \"{w1u} {w2u}\" in chunky hand-drawn condensed capitals with "
                "slightly uneven edges, \"{w3l}\" in a bouncy lowercase hand-drawn script, \"{w4u}.\" in very large "
                "chunky hand-drawn capitals followed by a period. All lines have the same width and are tightly "
                "stacked. Centered with wide black margins. White on black only. "),
    },
    "S6": {
        "name": "Skrip monoline + inline + percikan kuning",
        "ref": "IMG_5738",
        "bg": "#151b3d", "inks": ["#ffffff", "#f6c12a", "#c9cde6"], "texture": "none",
        "tpl": ("Decorative hand-lettering quote, portrait. Solid deep navy blue background. An oval-shaped "
                "lettering composition in the center. The text reads exactly, four lines: \"{w1c}\" in a bold white "
                "monoline script with loops; \"{w2u}\" in bold white hand-drawn capitals with curly swirl terminals; "
                "\"{w3u}\" in small bright yellow uppercase sans-serif letters; \"{w4c}\" in a large bold white loopy "
                "script with a big swirl. Each white letter has a thin inline highlight line inside the stroke. "
                "Bright yellow teardrop splashes radiate outward around the oval, plus tiny white dots and short "
                "dashes. Clean flat vector illustration. "),
    },
}

# Quote ujian: 4 perkataan. Templat guna {w1u} (UPPER), {w1c} (Capital), {w1l} (lower) ... {w4*}.
QUOTES = {
    "steps": ["Small", "steps", "every", "day"],
    # Ujian 10 quote (24 Nov 2026), pengguna lulus senarai.
    "dream": ["Dream", "big", "work", "hard"],
    "kind": ["Be", "kind", "to", "yourself"],
    "going": ["Keep", "going", "keep", "growing"],
    "love": ["Do", "it", "with", "love"],
    "moment": ["Make", "every", "moment", "count"],
    "joy": ["Choose", "joy", "every", "day"],
    "breathe": ["Breathe", "in", "breathe", "out"],
    "wild": ["Stay", "wild", "and", "free"],
    "sunshine": ["Create", "your", "own", "sunshine"],
    "great": ["You", "are", "doing", "great"],
}


def build(quote_id="steps", w=768, h=1024):
    words = QUOTES[quote_id]
    keys = {}
    for i, x in enumerate(words, 1):
        keys.update({f"w{i}u": x.upper(), f"w{i}c": x.capitalize(), f"w{i}l": x.lower()})
    out = []
    for sid, s in STYLES.items():
        out.append({"id": f"{quote_id}_{sid}", "style": sid, "text": " ".join(words),
                    "prompt": s["tpl"].format(**keys) + COMMON_TAIL, "w": w, "h": h})
    return out


if __name__ == "__main__":
    dst = sys.argv[1]
    q = sys.argv[2] if len(sys.argv) > 2 else "steps"
    ids = [k for k in QUOTES if k != "steps"] if q == "all10" else q.split(",")
    data = [p for qi in ids for p in build(qi)]
    with open(dst, "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    print(len(data), "prompts ->", dst)
