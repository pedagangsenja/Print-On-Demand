"""Contoh tulisan tangan bagi aturan prompt ikut model (Standard Lettering v1.2, langkah 3.4-3.7, rev r1):
satu prompt khas bagi setiap model, kad K3 x ayat H, hitam putih. Pembina kod belum dibina.

Tujuan: uji sama ada prompt yang ditulis ikut panduan setiap model memberi hasil lebih baik daripada
satu prompt sama (kad.bina). Ditulis tangan oleh Claude 26 Nov 2026 daripada kajian online:
- klein4b: BFL (kad model + petikan panduan): ayat mengalir, gaya ditulis terus di sisi setiap teks, tiada penambah.
- zturbo: pasukan Z-Image (perbincangan HF + templat pe.py): panjang, terperinci, objektif; semua teks dalam
  petikan; huraikan font dan susun atur; tiada negative prompt, jadi had ditulis sebagai ayat positif di hujung.
- ernie: dokumen diffusers: penambah prompt (PE) hidup secara lalai; prompt mentah ringkas, PE yang kembangkan.
- moss: panduan pengguna MOSS-Image + kad LoRA 8 langkah (dilatih dengan kapsyen JSON): susun atur JSON,
  kotak setiap baris dalam piksel berpusat (yxyx), kanvas 768x1024.
Guna: python3 khas.py  -> cetak semakan setiap prompt
"""
import json
import re

VERSI = "khas-v0 (percubaan)"
ID = "K3H"
SPEC = ["PATIENCE", "Builds", "WHAT", "Hurry", "BREAKS"]

KLEIN = (
    'A black-and-white hand-lettering quote poster in portrait format, flat vector artwork on a solid black '
    'background. Five lines of white lettering are stacked in one tight block in the center of the poster, with '
    'wide empty black margins around it, and the whole block tilts gently so that each line rises toward the '
    'right. At the top, the word "PATIENCE" is written in huge heavy condensed bold sans-serif capitals. Directly '
    'beneath it, the word "Builds" flows in large bold brush script with a big looping initial capital. In the '
    'middle of the block sits a small solid white rectangular label, and inside that label the word "WHAT" is '
    'printed in small bold black sans-serif capitals, with three short white sparkle strokes on each side of the '
    'label. Below the label, the word "Hurry" is written in the same bold brush script with a looping initial '
    'capital. At the bottom, the word "BREAKS" is the largest of all, in the same heavy condensed sans-serif '
    'capitals as the top line. The lines touch and slightly overlap. The poster shows only these five words, each '
    'of them once, in pure white and black with no gray, no shadow, no texture, and nothing below the last line.'
)

ZTURBO = (
    'A typography poster design in portrait orientation. The entire background is a flat solid black surface '
    'with no texture. All lettering is pure white with crisp clean vector edges. The poster contains exactly five '
    'words arranged as five stacked lines that form one compact block centered on the canvas; the block occupies '
    'the middle two thirds of the width and leaves wide empty black margins on all four sides. The block is '
    'rotated slightly counterclockwise, so every line rises a little toward the right, and neighbouring lines '
    'touch or overlap slightly. Line one, at the top, reads "PATIENCE" in very large, heavy, condensed bold '
    'sans-serif capital letters. Line two reads "Builds" in large, thick, connected brush-script lettering with a '
    'big looping initial capital. Line three is a small solid white rectangular label placed at the center of the '
    'block; inside the label the word "WHAT" is set in small bold sans-serif capital letters colored black; three '
    'short white dash strokes radiate from the left side of the label and three from the right side. Line four '
    'reads "Hurry" in the same thick connected brush script with a big looping initial capital. Line five, at the '
    'bottom, reads "BREAKS" in the same heavy condensed bold sans-serif capitals as line one, and it is the '
    'tallest line of the poster. The only text in the image is these five words, each appearing once. The image '
    'uses only pure white and pure black, flat fills, sharp edges, and a clean empty background.'
)

ERNIE_MENTAH = (
    'A black and white hand-lettering quote poster, portrait. Solid black background, white lettering. Five '
    'stacked lines in one tight centered block that tilts up to the right: "PATIENCE" in huge heavy condensed '
    'bold sans-serif capitals; "Builds" in large bold brush script; "WHAT" in small black bold capitals inside a '
    'small white rectangular label with short sparkle strokes on both sides; "Hurry" in large bold brush script; '
    '"BREAKS" in huge heavy condensed bold sans-serif capitals, the tallest line. Only these five words, no '
    'other text, pure black and white, flat vector style, wide black margins.'
)

SANS = "Huge heavy condensed bold sans-serif capitals, white, flat vector."
SKRIP = "Large bold flowing brush script with a big looping initial capital, white, flat vector."
MOSS_LAYOUT = {
    "summary": {
        "meta": ["poster"],
        "canvas": "single",
        "caption": ("A black-and-white mixed-font hand-lettering quote poster, flat vector, on a solid black "
                    "background with wide empty margins. Five stacked lines of white lettering form one tight "
                    "centered block that tilts slightly so each line rises to the right. The top and bottom lines "
                    "are heavy condensed sans-serif capitals, the second and fourth lines are bold brush script, "
                    "and the middle word is black inside a small white rectangular label. Only black and white, "
                    "no gray, no shadow, no texture, no other text."),
    },
    "items": [
        {"label": "text", "caption": SANS + " Top line of the block.", "text": "PATIENCE",
         "bbox": [-400, -304, -232, 304]},
        {"label": "text", "caption": SKRIP + " Second line.", "text": "Builds", "bbox": [-240, -256, -72, 256]},
        {"label": "text", "caption": ("Small bold sans-serif capitals in black inside a small solid white "
                                      "rectangular label, centered."), "text": "WHAT", "bbox": [-64, -112, 16, 112]},
        {"label": "object", "caption": "Three short white sparkle strokes left of the label.",
         "bbox": [-56, -208, 8, -136]},
        {"label": "object", "caption": "Three short white sparkle strokes right of the label.",
         "bbox": [-56, 136, 8, 208]},
        {"label": "text", "caption": SKRIP + " Fourth line.", "text": "Hurry", "bbox": [24, -256, 192, 256]},
        {"label": "text", "caption": SANS + " Bottom line, the tallest line of the poster.", "text": "BREAKS",
         "bbox": [192, -312, 408, 312]},
    ],
    "bbox_coord_space": "abs_centralized",
    "bbox_format": "yxyx",
}
MOSS = json.dumps(MOSS_LAYOUT, ensure_ascii=False)

PROMPT = {"klein4b": KLEIN, "zturbo": ZTURBO, "ernie": ERNIE_MENTAH, "moss": MOSS}


def petikan(model, prompt=None):
    """Teks yang diminta dilukis, ikut turutan dalam prompt."""
    if model == "moss" and prompt is None:
        return [i["text"] for i in MOSS_LAYOUT["items"] if "text" in i]
    return re.findall(r'"([^"]+)"', prompt or PROMPT[model])


def semak(model, prompt=None):
    """Semakan ringkas: lima perkataan, sekali setiap satu, ejaan dan huruf besar / kecil sama dengan SPEC."""
    q = petikan(model, prompt)
    err = []
    if q != SPEC:
        err.append(f"petikan {q} tidak sama dengan Spesifikasi Teks")
    return err


if __name__ == "__main__":
    for m, p in PROMPT.items():
        print(m, len(p.split()), "kata;", semak(m) or "semak: lulus")
