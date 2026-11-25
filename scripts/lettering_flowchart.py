"""Dua carta aliran sebelah-menyebelah: sedia ada (S1-S6, Lettering P9) vs cadangan (Standard 4 lapisan)."""
import sys
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
def F(w, s): return ImageFont.truetype(FD % w, s)
F_MAIN, F_SUB, F_HEAD = F("Bold", 62), F("Regular", 34), F("Bold", 46)
F_T, F_B, F_BS, F_CH, F_TAG, F_MH = F("Bold", 42), F("Regular", 35), F("Regular", 32), F("SemiBold", 29), F("Bold", 27), F("Bold", 33)

BG, INK, MUTED, LINE = (250, 249, 246), (31, 35, 40), (91, 100, 112), (100, 116, 139)
OLD_HEAD, OLD_BORDER = (71, 85, 105), (203, 213, 225)
NEW, NEW_TINT, NEW_BORDER = (15, 118, 110), (230, 244, 241), (15, 118, 110)
WARN_BG, WARN_INK = (255, 240, 205), (133, 84, 0)
WHITE = (255, 255, 255)
KEY = (30, 58, 95)

W, M, LOOP, GAPC, GAPR, P = 2400, 60, 110, 60, 58, 34
CW = (W - 2 * M - 2 * LOOP - GAPC) // 2
XL = M + LOOP
XR = XL + CW + GAPC

LEFT = [
    dict(title="1. Rujukan", body=["Upload rujukan", "Ambil ciri umum sahaja"], warn=["Ciri gaya hanya ada dalam ayat templat"]),
    dict(title="2. Ayat", body=["3–7 perkataan, semak trademark", "Tetapkan baris dan perkataan utama"], warn=["Diuji pada 4 perkataan sahaja", "Hanya 2 kelas: pendek ≤ 6, panjang ≥ 7"]),
    dict(title="3. Prompt: templat tetap", body=["styles.py: 6 ayat siap (S1–S6)", "Arahan setiap perkataan + ekor larangan"],
         warn=["Dikunci pada 4 perkataan", "Gaya, warna dan latar bercampur"]),
    dict(title="4. Jana", body=["MOSS SFT + LoRA 8 langkah", "Text-to-image penuh, 768×1024", "2 seed (CPU)"], warn=["Tiada peraturan tukar model"]),
    dict(title="5. QC", body=["Ejaan 100%, tiada teks rawak, tiada cacat", "9 ciri gaya (semak mata)", "Gagal: seed baharu (maks 4)"]),
    dict(title="6. Kemasan: finish.py", body=["Vektor → palet gaya → margin seragam", "300 DPI, 8×10 hingga 24×36", "Tekstur: grain / worn / chalk"],
         warn=["Dakwat rata atas latar satu warna sahaja"]),
    dict(title="7. Anda lulus atau tolak", body=["~5 minit"]),
    dict(title="8. Simpan dalam S&C", body=["Nama, nota, imej contoh, imej asal, prompt terisi"], warn=["Prompt terisi sahaja; tiada ciri gaya berstruktur"]),
    dict(title="9. Mockup → pin → upload", body=[]),
]
RIGHT = [
    dict(tag="LAPISAN 1", status="BAHARU", title="1. Kad Gaya",
         body=["Gaya lama: guna kad dalam S&C", "Gaya baharu: Claude isi kad daripada upload",
               "Isi kad: medium, bentuk huruf ikut peranan, susunan, hierarki, hiasan, kelas kemasan, 8 ciri QC, julat panjang sesuai",
               "Warna C berasingan: latar + dakwat 1–3"],
         keys=["Kunci 1: Kad Gaya satu-satunya sumber gaya"]),
    dict(status="DIUBAH", title="2. Ayat + peranan + laluan",
         body=["Semak trademark", "Setiap perkataan: utama / sokongan / penyambung", "Laluan ikut panjang ayat baharu, bukan ayat rujukan"],
         mcols=2, minis=[("Laluan 1", "Pendek (1–4 perkataan). AI penuh, satu blok"),
                         ("Laluan 2", "Sederhana (5–8). AI penuh, hierarki wajib"),
                         ("Laluan 3", "Panjang (9–16). Hibrid: AI lukis perkataan utama, font berlesen untuk baris lain"),
                         ("Laluan 4", "Terlalu panjang (17+). Font dahulu: AI buat tajuk dan hiasan sahaja")]),
    dict(tag="LAPISAN 2", status="BAHARU", title="3. Pembina prompt",
         body=["Kad Gaya + ayat + warna C + keluarga model", "Peraturan: petikan sekali sahaja, tiada hex atau nombor, ayat hierarki wajib"],
         minis=[("Keluarga LLM", "MOSS, klein, Z-Image, ERNIE: prompt penuh"), ("Keluarga T5", "schnell, Chroma: ringkas, teks di depan")]),
    dict(status="DIUBAH", title="4. Jana",
         body=["Text-to-image penuh, 768×1024", "Laluan 1–2: seluruh ayat. Laluan 3: perkataan utama sahaja. Laluan 4: tajuk + hiasan",
               "Seed: 2 (laluan 1), 3–4 (laluan 2)", "Log: model, seed, prompt, masa"],
         keys=["Kunci 3: model hanya untuk gaya yang ia lulus"]),
    dict(tag="LAPISAN 3", status="DIUBAH", title="5. QC ikut kad",
         body=["OCR saring dahulu, kemudian semak mata", "3 pintu wajib: ejaan 100%, tiada teks rawak, tiada cacat", "Gaya: sekurang-kurangnya 7/8 ciri kad",
               "Gagal: tambah ayat penegas + seed baharu (maks 4), kemudian model sandaran"],
         keys=["Kunci 2: QC sama untuk semua model", "Kunci 5: peraturan ulang"]),
    dict(tag="LAPISAN 4", status="DIUBAH", title="6. Kemasan ikut kelas",
         body=["Palet C dipaksa di sini", "F1 dan F2: 1 imej → beberapa warna", "Laluan 3–4: skrip gabung baris font ikut kad, kemudian semak 8 ciri sekali lagi"],
         minis=[("F1", "Vektor rata (finish.py)"), ("F2", "Rata + tekstur"), ("F3", "Raster: gaya bergambar, gradien")],
         keys=["Kunci 4: skrip paksa warna, margin, tekstur"]),
    dict(title="7. Anda lulus atau tolak", body=["~5 minit"]),
    dict(status="DIUBAH", title="8. Simpan dalam S&C", body=["Kad Gaya + prompt + model + seed + imej", "Gaya boleh dijana semula"]),
    dict(title="9. Mockup → pin → upload", body=[]),
]
FOOT_L = "Tukar model: tiada peraturan bertulis. Ujian P9b (24 Nov) pada S1–S6: MOSS 12/12, ERNIE 12/12, klein 4B 6/12 imej ejaan betul."
FOOT_R = "Tukar model: ujian kelayakan sekali bagi setiap model baharu, direkod dalam jadual model × gaya. Setiap gaya × ayat pendek dan sederhana × 2 seed. Lulus: ≥ 90% imej ejaan betul, gaya ≥ 7/8, tiada teks liar."


def wrap(text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if font.getlength(t) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def chip_w(text, font, pad=18):
    return int(font.getlength(text)) + 2 * pad


def box(spec, w, d=None, x=0, y=0):
    """Ukur (d=None) atau lukis kandungan kotak; pulang tinggi kandungan."""
    y0, iw = y, w - 2 * P
    st = spec.get("status")
    stw = chip_w(st, F_TAG, 14) if st else 0
    y += P
    if st and d:
        d.rounded_rectangle((x + w - P - stw, y, x + w - P, y + 42), 21, fill=NEW)
        d.text((x + w - P - stw + 14, y + 21), st, font=F_TAG, fill=WHITE, anchor="lm")
    if spec.get("tag"):
        if d:
            d.text((x + P, y + 21), spec["tag"], font=F_TAG, fill=NEW, anchor="lm")
        y += 50
    tw = iw - (stw + 20 if st and not spec.get("tag") else 0)
    for ln in wrap(spec["title"], F_T, tw):
        if d:
            d.text((x + P, y), ln, font=F_T, fill=INK)
        y += 54
    y += 8 if spec["body"] or spec.get("minis") or spec.get("warn") else 0
    for item in spec["body"]:
        for i, ln in enumerate(wrap(item, F_B, iw - 34)):
            if d:
                if i == 0:
                    d.ellipse((x + P + 4, y + 17, x + P + 14, y + 27), fill=MUTED)
                d.text((x + P + 34, y), ln, font=F_B, fill=INK)
            y += 46
        y += 4
    minis = spec.get("minis")
    if minis:
        y += 14
        n = spec.get("mcols") or len(minis); g = 16; mw = (iw - (n - 1) * g) // n
        for r0 in range(0, len(minis), n):
            grp = minis[r0:r0 + n]
            hh = max(len(wrap(h_, F_MH, mw - 40)) for h_, _ in grp) * 42
            mh = 20 + hh + 6 + max(len(wrap(t_, F_BS, mw - 40)) for _, t_ in grp) * 42 + 18
            for i, (head, txt) in enumerate(grp):
                mx = x + P + i * (mw + g)
                if d:
                    d.rounded_rectangle((mx, y, mx + mw, y + mh), 14, fill=NEW_TINT)
                    for j, ln in enumerate(wrap(head, F_MH, mw - 40)):
                        d.text((mx + 20, y + 20 + j * 42), ln, font=F_MH, fill=NEW)
                    for j, ln in enumerate(wrap(txt, F_BS, mw - 40)):
                        d.text((mx + 20, y + 26 + hh + j * 42), ln, font=F_BS, fill=INK)
            y += mh + g
        y -= g - 6
    keys = spec.get("keys")
    if keys:
        y += 14
        cx = x + P
        for t in keys:
            cw = chip_w(t, F_CH, 22)
            if cx + cw > x + w - P and cx > x + P:
                cx = x + P; y += 58
            if d:
                d.rounded_rectangle((cx, y, cx + cw, y + 48), 24, fill=KEY)
                d.text((cx + 22, y + 24), t, font=F_CH, fill=WHITE, anchor="lm")
            cx += cw + 12
        y += 48
    warn = spec.get("warn")
    if warn:
        y += 12
        cx = x + P
        for t in warn:
            cw = chip_w(t, F_CH) + 36
            if cx + cw > x + w - P and cx > x + P:
                cx = x + P; y += 58
            if d:
                d.rounded_rectangle((cx, y, cx + cw, y + 48), 24, fill=WARN_BG)
                d.ellipse((cx + 10, y + 9, cx + 40, y + 39), fill=WARN_INK)
                d.text((cx + 25, y + 24), "!", font=F_CH, fill=WARN_BG, anchor="mm")
                d.text((cx + 50, y + 24), t, font=F_CH, fill=WARN_INK, anchor="lm")
            cx += cw + 12
        y += 48
    return y + P - y0


def arrow_down(d, cx, y1, y2):
    d.line((cx, y1, cx, y2 - 14), fill=LINE, width=5)
    d.polygon([(cx - 13, y2 - 20), (cx + 13, y2 - 20), (cx, y2)], fill=LINE)


def vtext(img, text, font, cx, cy, fill):
    w = int(font.getlength(text)) + 8
    t = Image.new("RGBA", (w, 44), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((4, 22), text, font=font, fill=fill, anchor="lm")
    t = t.rotate(90, expand=True)
    img.paste(t, (int(cx - t.width / 2), int(cy - t.height / 2)), t)


def main(out):
    rows = [(box(l, CW), box(r, CW)) for l, r in zip(LEFT, RIGHT)]
    rh = [max(a, b) for a, b in rows]
    fl, fr = wrap(FOOT_L, F_BS, CW - 2 * P), wrap(FOOT_R, F_BS, CW - 2 * P)
    fh = max(len(fl), len(fr)) * 42 + 2 * 26
    top = 60 + 78 + 52 + 70 + 40      # tajuk, subtajuk, legenda
    head_h = 92
    H = top + head_h + GAPR + sum(rh) + GAPR * (len(rh) - 1) + 50 + fh + 60
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((M, 60), "Aliran kerja lettering: sedia ada vs cadangan terkini", font=F_MAIN, fill=INK)
    d.text((M, 60 + 82), "Cadangan pertama (25 Nov): 4 lapisan, 4 laluan, 5 kunci. Belum dibina; laluan 3 dan 4 belum diuji. Butiran: docs/lettering-standard-handover.md", font=F_SUB, fill=MUTED)
    ly = 60 + 82 + 62
    d.rounded_rectangle((M, ly, M + 46, ly + 46), 10, fill=WHITE, outline=NEW_BORDER, width=5)
    d.text((M + 62, ly + 23), "Kotak hijau = baharu atau diubah", font=F_BS, fill=INK, anchor="lm")
    x2 = M + 62 + int(F_BS.getlength("Kotak hijau = baharu atau diubah")) + 50
    d.rounded_rectangle((x2, ly, x2 + 46, ly + 46), 23, fill=WARN_BG)
    d.text((x2 + 23, ly + 23), "!", font=F_CH, fill=WARN_INK, anchor="mm")
    d.text((x2 + 62, ly + 23), "Tanda kuning = kelemahan aliran sedia ada", font=F_BS, fill=INK, anchor="lm")
    x3 = x2 + 62 + int(F_BS.getlength("Tanda kuning = kelemahan aliran sedia ada")) + 50
    d.rounded_rectangle((x3, ly, x3 + 120, ly + 46), 23, fill=KEY)
    d.text((x3 + 60, ly + 23), "Kunci", font=F_CH, fill=WHITE, anchor="mm")
    d.text((x3 + 136, ly + 23), "Pil biru = 5 kunci gaya", font=F_BS, fill=INK, anchor="lm")
    y = top
    for x, col, t in ((XL, OLD_HEAD, "SEDIA ADA: S1–S6 (Lettering P9)"), (XR, NEW, "CADANGAN: 4 lapisan, 4 laluan, 5 kunci")):
        d.rounded_rectangle((x, y, x + CW, y + head_h), 18, fill=col)
        d.text((x + CW // 2, y + head_h // 2), t, font=F_HEAD, fill=WHITE, anchor="mm")
    y += head_h
    mids = []
    for i, (l, r) in enumerate(zip(LEFT, RIGHT)):
        for x in (XL, XR):
            arrow_down(d, x + CW // 2, y + 6, y + GAPR - 6)
        y += GAPR
        h = rh[i]
        changed = bool(r.get("status"))
        d.rounded_rectangle((XL, y, XL + CW, y + h), 20, fill=WHITE, outline=OLD_BORDER, width=3)
        d.rounded_rectangle((XR, y, XR + CW, y + h), 20, fill=WHITE, outline=NEW_BORDER if changed else OLD_BORDER, width=5 if changed else 3)
        box(l, CW, d, XL, y + (h - rows[i][0]) // 2)
        box(r, CW, d, XR, y + (h - rows[i][1]) // 2)
        mids.append(y + h // 2)
        y += h
    # gelung QC (baris 5) kembali ke Jana (baris 4)
    for side, x_edge, sgn in (("L", XL, -1), ("R", XR + CW, 1)):
        xo = x_edge + sgn * 62
        d.line((x_edge, mids[4], xo, mids[4]), fill=LINE, width=5)
        d.line((xo, mids[4], xo, mids[3]), fill=LINE, width=5)
        d.line((xo, mids[3], x_edge + sgn * 16, mids[3]), fill=LINE, width=5)
        d.polygon([(x_edge + sgn * 22, mids[3] - 13), (x_edge + sgn * 22, mids[3] + 13), (x_edge + sgn * 2, mids[3])], fill=LINE)
        vtext(img, "gagal", F_CH, xo + sgn * 26, (mids[3] + mids[4]) // 2, MUTED)
    y += 50
    d.rounded_rectangle((XL, y, XL + CW, y + fh), 18, fill=(241, 243, 246))
    d.rounded_rectangle((XR, y, XR + CW, y + fh), 18, fill=NEW_TINT)
    for x, lines in ((XL, fl), (XR, fr)):
        for j, ln in enumerate(lines):
            d.text((x + P, y + 26 + j * 42), ln, font=F_BS, fill=INK)
    img.save(out)
    print(img.size)


if __name__ == "__main__":
    main(sys.argv[1])
