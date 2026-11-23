"""Ujian v3 (SOP lettering + QC): bina prompts.json dan rubric.json daripada kajian 5 poster rujukan.

Guna: python3 build_prompts.py
Setiap gaya rujukan (B1-B5) ada 'unsur' (dari kajian rujukan) -> dipakai untuk prompt DAN senarai semak QC.
Setiap design: frasa Melayu baharu + baris (teks, saiz, gaya huruf, bekas). Varian 'a' = gaya huruf macam
rujukan; varian 'b' = gaya huruf lain (font lain), unsur lain kekal. 'rev' naik bila prompt dibaiki selepas QC.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
W, H = 768, 1024

# Pintu wajib (semua mesti lulus)
GATES = [
    ("G1", "Ejaan semua perkataan betul (100%)"),
    ("G2", "Tiada huruf/perkataan rawak; tiada tanda baca yang mengubah maksud"),
    ("G3", "Tiada kecacatan: huruf bertindih tak terbaca, teks terpotong di tepi, tangan/objek cacat"),
]
RULES = (" Every word is spelled exactly as written, letter by letter, and appears once. No other words, letters or"
         " numbers anywhere: no signature, no watermark, no faint background writing; ribbons, labels and badges hold"
         " only the listed words. Flat poster artwork, no mockup.")

# Unsur setiap rujukan: (kod, semakan QC dalam BM, ayat prompt Inggeris). Unsur 'L' = gaya huruf (ikut varian).
STYLES = {
 "B4": {"name": "Hiasan krim + emas atas hitam",
  "head": "Vintage hand-lettering typography poster.",
  "el": [
   ("P", "Palet krim + emas antik atas hitam pekat", "Cream lettering with antique-gold as the only second colour, on a solid black background."),
   ("K", "Satu tiang teks tinggi di tengah, ruang hitam di tepi", "The lettering forms one tall centered column about 75% of the canvas width, with black margins on all sides."),
   ("H", "Hierarki: 3-4 perkataan utama sangat besar, baris lain kecil", "Hero words are huge and span the column width; connector words are small."),
   ("R", "Baris bertaut rapat; ruang kosong diisi skrol emas di belakang huruf", "Lines interlock tightly with almost no gaps; every gap is filled with antique-gold acanthus scrolls and filigree swirls layered behind the letters."),
   ("L", "Campuran 3+ gaya huruf seperti dalam prompt", None),
   ("A", "Baris pertama melengkung (arch)", "The first line is arched like a rainbow over the next word."),
   ("T", "Perkataan kecil dalam tag reben emas atau bulatan", None),
   ("S", "Ekor huruf/swash memanjang jadi hiasan", "Letter terminals end in long swashes and curls that flow into the ornaments."),
  ]},
 "B5": {"name": "Papan kapur + reben",
  "head": "Chalkboard hand-lettering poster drawn with white chalk.",
  "el": [
   ("P", "Kapur putih atas papan batu tulis gelap dengan kesan sapuan", "White and light-grey chalk on a dark slate blackboard with soft smudges."),
   ("K", "Satu tiang teks di tengah, ruang tepi", "The lettering forms one centered column with dark margins on all sides."),
   ("H", "Hierarki: 2-3 perkataan utama sangat besar", "Hero words are huge; connector words are small."),
   ("D", "Huruf ada kedalaman: garis inline/3D dan bayang", "Letters have chalk inline highlights and a 3D drop shading."),
   ("L", "Campuran 3+ gaya huruf seperti dalam prompt", None),
   ("T", "Perkataan kecil dalam reben kapur berlipat", None),
   ("O", "Pembahagi hiasan (fleuron, daun, bintang kecil, titik) antara baris", "Small chalk flourish dividers with a leaf in the middle, tiny stars and dots between the lines."),
   ("X", "Tekstur butir kapur dalam garisan huruf; ada tanda baca", "Visible chalk grain inside every stroke; keep the punctuation marks shown."),
  ]},
 "B3": {"name": "Berus berwarna, grunge",
  "head": "Bold street-style brush lettering poster.",
  "el": [
   ("P", "Latar arang/coklat gelap dengan grunge dan percikan cat", "Dark charcoal-brown grunge background with paint splatter and scratches."),
   ("C", "4 warna (oren, teal, krim, kuning); setiap baris warna lain", "Use exactly four colours: orange, teal, cream and yellow; each line has a different colour."),
   ("K", "Tiang tinggi penuh kanvas; baris condong sedikit", "The text block fills the canvas from top to bottom; lines are slightly tilted."),
   ("D", "Huruf besar berus kering, tepi kasar, bayang gelap", "Hero words in dry-brush capitals with rough bristle edges and a dark drop shadow."),
   ("L", "Campuran 3+ gaya huruf seperti dalam prompt", None),
   ("T", "Perkataan kecil dalam reben/label kertas koyak berwarna", None),
   ("O", "Anak panah, bintang, pusaran dan coretan", "Hand-drawn arrows, small stars, swirls and scribble marks around the words."),
   ("H", "Hierarki: perkataan utama sangat besar", "Hero words are huge; connector words are small."),
  ]},
 "B2": {"name": "Lencana hitam-putih",
  "head": "Black-and-white sticker badge design.",
  "el": [
   ("P", "Hitam-putih sahaja; latar luar putih", "Pure black and white only; the area outside the badge is plain white."),
   ("B", "Bentuk lencana: atas melengkung, sisi berukir, sinar matahari di bawah", "One tall black badge with an arched top, notched decorative sides, short spikes radiating from the top and a small sunburst at the bottom centre."),
   ("H", "3-5 perkataan sahaja, setiap satu sangat besar", "Each word is very large and fills the badge width."),
   ("D", "Huruf putih dengan garis inline dan bayang 3D", "White letters with a black inline stripe and a 3D extruded shadow."),
   ("L", "Campuran 3+ gaya huruf seperti dalam prompt", None),
   ("S", "Garis dasar melantun; ekor swash", "Bouncing baselines; letters end in swash tails."),
   ("O", "Daun, titik dan pusaran mengisi ruang dalam lencana", "Small leaves, dots and swirls fill the empty space inside the badge."),
   ("X", "Tepi berus kasar dan percikan dakwat kecil di sekeliling", "Rough hand-inked brush edges and tiny ink splatter dots around the badge."),
  ]},
 "B1": {"name": "Ilustrasi + lettering",
  "head": "Vintage scratchboard lettering poster.",
  "el": [
   ("P", "Krim atas hitam, gaya ukiran scratchboard (garis silang)", "Cream ink on black in an engraved scratchboard style with cross-hatching."),
   ("I", "Ilustrasi tangan memegang objek di tengah, berukir", None),
   ("W", "Satu perkataan ditulis atas objek", None),
   ("T", "Reben berpusing di belakang tangan berisi perkataan", None),
   ("H", "Hierarki: 3-4 perkataan utama besar, perkataan kecil", "Hero words are large; connector words are small and tucked around the object."),
   ("L", "Campuran 3+ gaya huruf seperti dalam prompt", None),
   ("O", "Hiasan skrol, titik dan sinar di belakang objek", "Scroll flourishes, dots and light rays behind the object."),
   ("X", "Tekstur cetakan lusuh", "Slightly distressed print texture."),
  ]},
}

# Design: id, rujukan, varian, gaya huruf (L), baris [(teks, peranan, gaya, bekas)], tambahan prompt (objek dll)
DESIGNS = [
 ("R4a", "B4", "a", "tall spurred Victorian Tuscan capitals, looping brush script with big swash capitals, and small spaced capitals separated by dots", [
   ("Jangan Risau Kalau", "small", "small spaced capitals", "arched first line"),
   ("LANGKAHMU", "hero", "huge spurred Tuscan capitals", ""),
   ("MASIH KECIL,", "small", "small capitals with a dot on each side", ""),
   ("Pokok Besar", "hero", "large looping brush script", ""),
   ("PUN", "small", "small capitals inside a gold circle", "gold circle"),
   ("BERMULA", "hero", "huge condensed Tuscan capitals", ""),
   ("DARI SEBIJI", "small", "small cream capitals inside a gold ribbon tag", "gold ribbon tag"),
   ("BENIH.", "hero", "huge spurred Tuscan capitals", "")], ""),
 ("R4b", "B4", "b", "elegant Spencerian copperplate script, high-contrast Didone capitals and small italic capitals", [
   ("Orang Cuma", "small", "small italic capitals", "arched first line"),
   ("NAMPAK", "hero", "huge high-contrast Didone capitals", ""),
   ("Senyuman,", "hero", "large Spencerian copperplate script", ""),
   ("bukan", "small", "small italic capitals inside a gold circle", "gold circle"),
   ("PENAT LELAH", "hero", "huge Didone capitals", ""),
   ("yang kita", "small", "small cream capitals inside a gold ribbon tag", "gold ribbon tag"),
   ("Simpan", "hero", "large Spencerian copperplate script", ""),
   ("SETIAP MALAM.", "small", "medium Didone capitals", "")], ""),
 ("R5a", "B5", "a", "copperplate script with 3D chalk shading, Victorian serif capitals with drop shadow, and small spaced serif capitals", [
   ("Dah Makan,", "hero", "large copperplate script", ""),
   ("BELUM?", "small", "small spaced serif capitals inside a folded chalk ribbon banner", "folded chalk ribbon"),
   ("Jangan Lupa", "hero", "huge copperplate script with 3D shading", ""),
   ("JAGA", "small", "tiny spaced serif capitals", ""),
   ("Diri Sendiri", "hero", "medium copperplate script", ""),
   ("BAIK-BAIK", "hero", "huge Victorian serif capitals with a drop shadow", ""),
   ("Ya.", "small", "swashed script", "")], ""),
 ("R5b", "B5", "b", "rounded bold sans-serif capitals with chalk outline, casual brush script and small condensed capitals", [
   ("Kalau Ada", "small", "casual brush script", ""),
   ("ORANG", "hero", "huge rounded bold sans-serif capitals with a chalk outline", ""),
   ("yang doakan kita", "small", "small condensed capitals inside a folded chalk ribbon banner", "folded chalk ribbon"),
   ("Diam-Diam,", "hero", "large casual brush script", ""),
   ("ITULAH", "small", "small condensed capitals", ""),
   ("KAYA", "hero", "huge rounded bold capitals with 3D chalk shading", ""),
   ("yang sebenar.", "small", "casual brush script", "")], ""),
 ("R3a", "B3", "a", "dry-brush capitals, fast brush script and bold italic capitals with an outline", [
   ("Kalau Orang", "small", "fast cream brush script", ""),
   ("PANDANG", "hero", "huge orange dry-brush capitals", ""),
   ("RENDAH,", "hero", "huge teal dry-brush capitals", ""),
   ("senyum saja,", "small", "small capitals in a torn yellow paper label", "torn label"),
   ("BIAR", "small", "bold italic cream capitals", ""),
   ("KEJAYAAN", "hero", "huge yellow dry-brush capitals", ""),
   ("yang bercakap", "small", "small capitals in a torn teal paper label", "torn label"),
   ("NANTI.", "hero", "huge orange dry-brush capitals", "")], ""),
 ("R3b", "B3", "b", "chunky retro 70s italic capitals, marker handwriting and stencil capitals", [
   ("Tak Perlu", "small", "cream marker handwriting", ""),
   ("JADI", "small", "small stencil capitals in a torn orange paper label", "torn label"),
   ("YANG TERBAIK,", "hero", "huge chunky retro yellow italic capitals", ""),
   ("cukup", "small", "teal marker handwriting", ""),
   ("JADI", "small", "small stencil capitals in a torn cream paper label", "torn label"),
   ("LEBIH BAIK", "hero", "huge chunky retro orange italic capitals", ""),
   ("dari", "small", "cream marker handwriting", ""),
   ("SEMALAM.", "hero", "huge chunky retro teal italic capitals", "")], ""),
 ("R2a", "B2", "a", "bold slanted brush capitals, a tall brush script and small capitals", [
   ("RESTU", "hero", "bold slanted brush capitals", ""),
   ("IBU", "hero", "tall brush script", ""),
   ("PEMBUKA", "hero", "bold slanted brush capitals", ""),
   ("REZEKI", "hero", "huge bold slanted brush capitals", "")], ""),
 ("R2b", "B2", "b", "rounded retro script, wide block capitals and small slab-serif capitals", [
   ("HATI", "hero", "rounded retro script", ""),
   ("TENANG", "hero", "huge wide block capitals", ""),
   ("HIDUP", "hero", "small slab-serif capitals", ""),
   ("SENANG", "hero", "huge rounded retro script", "")], ""),
 ("R1a", "B1", "a", "condensed Victorian serif capitals with engraved lines and drop shadow, swash script and small capitals", [
   ("HUJAN", "hero", "huge condensed Victorian serif capitals", ""),
   ("tak", "small", "small capitals inside the curling ribbon behind the hand", "ribbon"),
   ("Selamanya,", "hero", "large swash script", ""),
   ("tapi", "small", "small capitals", ""),
   ("PAYUNG", "hero", "bold capitals written on the canopy of the umbrella", "object"),
   ("yang kau kongsi", "small", "small capitals inside a second ribbon", "ribbon"),
   ("Tetap", "small", "medium swash script", ""),
   ("DIINGAT.", "hero", "huge condensed Victorian serif capitals", "")],
  "In the middle an engraved hand holds an open umbrella; the ribbon curls behind the hand; the word PAYUNG is written on the umbrella canopy."),
 ("R1b", "B1", "b", "rounded engraved serif capitals, upright brush script and small spaced capitals", [
   ("Jadilah", "hero", "large upright brush script", ""),
   ("PELITA,", "hero", "bold capitals written on the glass of the oil lamp", "object"),
   ("walau kecil", "small", "small spaced capitals inside the curling ribbon behind the hand", "ribbon"),
   ("IA TETAP", "small", "small spaced capitals", ""),
   ("MENERANGI", "hero", "huge rounded engraved serif capitals", ""),
   ("Jalan Orang.", "hero", "large upright brush script", "")],
  "In the middle an engraved hand holds an old oil lamp (pelita) with a small flame; the ribbon curls behind the hand; the word PELITA is written on the lamp glass."),
]
REVS = json.loads((HERE / "revisions.json").read_text()) if (HERE / "revisions.json").exists() else {}


def build():
    out, rubric = [], {"gates": [{"code": c, "check": t} for c, t in GATES], "styles": {}}
    for ref, st in STYLES.items():
        rubric["styles"][ref] = {"name": st["name"], "elements": [{"code": c, "check": t} for c, t, _ in st["el"]]}
    for pid, ref, var, fonts, lines, extra in DESIGNS:
        st = STYLES[ref]
        parts = [st["head"]] + [e for _, _, e in st["el"] if e]
        parts.append(f"Lettering styles: {fonts}.")
        if extra:
            parts.append(extra)
        order = "; ".join(f'{style}: "{t}"' for t, _, style, _ in lines)
        parts.append(f"Text, top to bottom: {order}.")
        for extra_rev in REVS.get(pid, []):  # pembaikan selepas QC (unsur yang gagal ditekankan)
            parts.append(extra_rev)
        prompt = " ".join(parts) + RULES
        text = " / ".join(t for t, *_ in lines)
        out.append({"id": pid, "ref": ref, "variant": var, "type": f"{st['name']} ({'gaya huruf rujukan' if var == 'a' else 'font lain'})",
                    "w": W, "h": H, "text": text, "words": len(text.replace("/", " ").split()), "fonts": fonts,
                    "rev": 1 + len(REVS.get(pid, [])), "sha": hashlib.sha1(prompt.encode()).hexdigest()[:8], "prompt": prompt})
    (HERE / "prompts.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    (HERE / "rubric.json").write_text(json.dumps(rubric, ensure_ascii=False, indent=1) + "\n")
    for o in out:
        print(o["id"], o["words"], len(o["prompt"].split()), o["sha"], "|", o["text"])


if __name__ == "__main__":
    build()
