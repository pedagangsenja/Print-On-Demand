"""Tiga carta aliran sebelah-menyebelah: sedia ada (S1-S6, Lettering P9), cadangan pertama (4 lapisan), standard v1 (docs/lettering-standard.md)."""
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
STD, STD_TINT = (67, 56, 202), (236, 235, 250)

M, LOOP, GAPC, GAPR, P, CW = 60, 110, 150, 58, 34, 1000
XL = M + LOOP
XR = XL + CW + GAPC
XS = XR + CW + GAPC
W = XS + CW + M

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

THIRD = [
    dict(tag="LAPISAN 1", status="DIKEMAS KINI", title="1. Kad Gaya",
         body=["1a simpan rujukan di tempat kekal; 1b semak pendua dalam S&C",
               "1c isi kad 16 medan; setiap medan = semakan QC (ya / tidak) + frasa prompt",
               "2–3 ciri teras wajib lulus; unsur berisiko; senarai jangan salin; julat panjang ayat",
               "Warna C berasingan: peranan + nama warna untuk prompt",
               "1d anda luluskan kad (~2 minit); 1e imej bukti (ayat pendek, 2 seed) jadi imej sauh"],
         keys=["Kunci 1: Kad Gaya satu-satunya sumber gaya"]),
    dict(status="DIKEMAS KINI", title="2. Ayat + peranan + laluan",
         body=["Ayat asal; saringan trademark bertulis, hasil direkod",
               "Ukur kesukaran: bilangan perkataan, perkataan 7+ huruf, perkataan berulang",
               "Kata isi = utama; kata fungsi = penyambung; perkataan 7+ huruf jadi utama",
               "Sokongan dan penyambung HURUF BESAR kecuali kad wajibkan skrip",
               "Hasil: Spesifikasi Teks (rujukan ejaan untuk QC)"],
         mcols=2, minis=[("Laluan 1: standard v1", "1–4 perkataan. AI penuh, satu blok"),
                         ("Laluan 2: standard v1", "5–8 perkataan. AI penuh, hierarki wajib"),
                         ("Laluan 3: percubaan", "9–16 perkataan. Hibrid. Belum diuji; perlu kelulusan anda"),
                         ("Laluan 4: percubaan", "17+ perkataan. Font dahulu. Belum diuji; perlu kelulusan anda")]),
    dict(tag="LAPISAN 2", status="DIKEMAS KINI", title="3. Pembina prompt (kod)",
         body=["Kad + Spesifikasi Teks yang sama → prompt yang sama",
               "Rangka tetap 9 bahagian; had token setiap model + turutan potong",
               "Semak automatik: petikan sekali, sama dengan Spesifikasi Teks, tiada hex / nombor / nama font",
               "Profil model: format, pembalut, penambah prompt; format T5 diuji A/B dahulu",
               "Syarat pakai: hasilkan semula S1–S6 tidak lebih buruk"]),
    dict(status="DIKEMAS KINI", title="4. Jana",
         body=["Tetapan dikunci dalam profil model; enjin diffusers",
               "Model utama: MOSS dan ERNIE (12/12 pada S1–S6); klein 4B 6/12",
               "Seed tetap 42, 7, 123, 2024: laluan 1 = 2 seed, laluan 2 = 3–4",
               "Satu model besar pada satu masa; semak RAM dan disk dahulu",
               "Log lengkap setiap imej; imej mentah disimpan sebelum sesi tamat"],
         keys=["Kunci 3: model hanya untuk gaya yang ia lulus"]),
    dict(tag="LAPISAN 3", status="DIKEMAS KINI", title="5. QC ikut kad",
         body=["3 pintu wajib; ejaan huruf demi huruf ikut Spesifikasi Teks; OCR hanya menanda",
               "Ciri kad ≥ 7/8 + ciri teras wajib; banding dengan upload dan imej sauh",
               "Ciri sejagat: boleh dibaca kecil, tiada teks terpotong, margin cukup",
               "QC dua kali: imej mentah dan selepas kemasan",
               "Ulang ikut jenis gagal (maks 4) → model sandaran → pendekkan ayat → lapor"],
         keys=["Kunci 2: QC sama untuk semua model", "Kunci 5: peraturan ulang"]),
    dict(tag="LAPISAN 4", status="DIKEMAS KINI", title="6. Kemasan ikut kad",
         body=["Parameter daripada kad: margin, tekstur, bilangan dakwat, butiran halus",
               "Semak automatik: bilangan lapisan dan dakwat yang hilang",
               "Warna ikut peranan: 1 imej → beberapa warna C",
               "Seed tekstur berbeza setiap design",
               "Simpan SVG induk; PNG besar dijana semula bila perlu"],
         minis=[("F1: v1", "Vektor rata"), ("F2: v1", "Rata + tekstur"), ("F3: ditangguh", "Raster; belum wujud")],
         keys=["Kunci 4: skrip paksa warna, margin, tekstur"]),
    dict(status="DIKEMAS KINI", title="7. Anda lulus atau tolak",
         body=["Papar upload, imej sauh dan hasil sebelah-menyebelah + skor QC",
               "Sebab tolak daripada senarai tetap; disalur balik ke kad, jadual model × gaya atau ulangan",
               "3 titik kelulusan: kad, contoh pertama laluan 3–4, hasil akhir",
               "Had bilangan imej setiap helaian"]),
    dict(status="DIKEMAS KINI", title="8. Simpan dalam S&C",
         body=["Rekod S: Kad Gaya + templat prompt tanpa perkataan + model lulus + versi kad",
               "Rekod C: peranan + nama warna; satu sumber kod hex",
               "Daftar design lulus: ayat, S, C, model, seed, fail induk",
               "Semua fail disimpan sebelum sesi tamat"]),
    dict(status="DIKEMAS KINI", title="9. Serahan → mockup → pin → upload",
         body=["Standard berhenti di serahan kepada Workflow",
               "Serahan: fail cetak setiap saiz, pratonton, ayat, kod S dan C, hasil trademark",
               "Produk dan pin ditanda kod S / C → tab Prestasi",
               "Jualan kembali ke S&C: gaya menang dapat lebih ayat dan warna"]),
]
FOOT_S = "Standard v1 (25 Nov, dipersetujui pengguna): laluan 1–2, kemasan F1–F2. Belum dibina. Tukar model: ujian kelayakan seperti cadangan, sah untuk gabungan tetapan yang dikunci sahaja. Tahap bukti angka: lemah."


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


def box(spec, w, d=None, x=0, y=0, acc=NEW, tint=NEW_TINT):
    """Ukur (d=None) atau lukis kandungan kotak; pulang tinggi kandungan."""
    y0, iw = y, w - 2 * P
    st = spec.get("status")
    stw = chip_w(st, F_TAG, 14) if st else 0
    y += P
    if st and d:
        d.rounded_rectangle((x + w - P - stw, y, x + w - P, y + 42), 21, fill=acc)
        d.text((x + w - P - stw + 14, y + 21), st, font=F_TAG, fill=WHITE, anchor="lm")
    if spec.get("tag"):
        if d:
            d.text((x + P, y + 21), spec["tag"], font=F_TAG, fill=acc, anchor="lm")
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
                    d.rounded_rectangle((mx, y, mx + mw, y + mh), 14, fill=tint)
                    for j, ln in enumerate(wrap(head, F_MH, mw - 40)):
                        d.text((mx + 20, y + 20 + j * 42), ln, font=F_MH, fill=acc)
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
    cols = [(XL, LEFT, OLD_HEAD, OLD_HEAD, NEW_TINT, "SEDIA ADA: S1–S6 (Lettering P9)", FOOT_L, (241, 243, 246)),
            (XR, RIGHT, NEW, NEW, NEW_TINT, "CADANGAN PERTAMA: 4 lapisan, 5 kunci", FOOT_R, NEW_TINT),
            (XS, THIRD, STD, STD, STD_TINT, "STANDARD v1: aliran terkini", FOOT_S, STD_TINT)]
    n = len(LEFT)
    hs = [[box(c[1][i], CW, acc=c[3], tint=c[4]) for c in cols] for i in range(n)]
    rh = [max(r) for r in hs]
    feet = [wrap(c[6], F_BS, CW - 2 * P) for c in cols]
    fh = max(len(f) for f in feet) * 42 + 2 * 26
    top = 60 + 78 + 52 + 70 + 40      # tajuk, subtajuk, legenda
    head_h = 92
    H = top + head_h + GAPR + sum(rh) + GAPR * (n - 1) + 50 + fh + 60
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((M, 60), "Aliran kerja lettering: sedia ada, cadangan pertama, standard v1", font=F_MAIN, fill=INK)
    d.text((M, 60 + 82), "Standard v1 dipersetujui pengguna 25 Nov; belum dibina. Laluan 3–4 percubaan, F3 ditangguh. Butiran: docs/lettering-standard.md", font=F_SUB, fill=MUTED)
    ly = 60 + 82 + 62
    lx = M
    for colr, lab in ((NEW, "Hijau = cadangan pertama"), (STD, "Ungu = standard v1 (terkini)")):
        d.rounded_rectangle((lx, ly, lx + 46, ly + 46), 10, fill=WHITE, outline=colr, width=5)
        d.text((lx + 62, ly + 23), lab, font=F_BS, fill=INK, anchor="lm")
        lx += 62 + int(F_BS.getlength(lab)) + 50
    d.rounded_rectangle((lx, ly, lx + 46, ly + 46), 23, fill=WARN_BG)
    d.text((lx + 23, ly + 23), "!", font=F_CH, fill=WARN_INK, anchor="mm")
    d.text((lx + 62, ly + 23), "Tanda kuning = kelemahan aliran sedia ada", font=F_BS, fill=INK, anchor="lm")
    lx += 62 + int(F_BS.getlength("Tanda kuning = kelemahan aliran sedia ada")) + 50
    d.rounded_rectangle((lx, ly, lx + 120, ly + 46), 23, fill=KEY)
    d.text((lx + 60, ly + 23), "Kunci", font=F_CH, fill=WHITE, anchor="mm")
    d.text((lx + 136, ly + 23), "Pil biru = 5 kunci gaya", font=F_BS, fill=INK, anchor="lm")
    y = top
    for c in cols:
        d.rounded_rectangle((c[0], y, c[0] + CW, y + head_h), 18, fill=c[2])
        d.text((c[0] + CW // 2, y + head_h // 2), c[5], font=F_HEAD, fill=WHITE, anchor="mm")
    y += head_h
    mids = []
    for i in range(n):
        for c in cols:
            arrow_down(d, c[0] + CW // 2, y + 6, y + GAPR - 6)
        y += GAPR
        h = rh[i]
        for k, c in enumerate(cols):
            sp = c[1][i]
            changed = bool(sp.get("status"))
            d.rounded_rectangle((c[0], y, c[0] + CW, y + h), 20, fill=WHITE,
                                outline=c[3] if changed else OLD_BORDER, width=5 if changed else 3)
            box(sp, CW, d, c[0], y + (h - hs[i][k]) // 2, acc=c[3], tint=c[4])
        mids.append(y + h // 2)
        y += h
    # gelung QC (baris 5) kembali ke Jana (baris 4), di sebelah kiri setiap lajur
    for c in cols:
        x_edge, sgn = c[0], -1
        xo = x_edge + sgn * 62
        d.line((x_edge, mids[4], xo, mids[4]), fill=LINE, width=5)
        d.line((xo, mids[4], xo, mids[3]), fill=LINE, width=5)
        d.line((xo, mids[3], x_edge + sgn * 16, mids[3]), fill=LINE, width=5)
        d.polygon([(x_edge + sgn * 22, mids[3] - 13), (x_edge + sgn * 22, mids[3] + 13), (x_edge + sgn * 2, mids[3])], fill=LINE)
        vtext(img, "gagal", F_CH, xo + sgn * 26, (mids[3] + mids[4]) // 2, MUTED)
    y += 50
    for c, lines in zip(cols, feet):
        d.rounded_rectangle((c[0], y, c[0] + CW, y + fh), 18, fill=c[7])
        for j, ln in enumerate(lines):
            d.text((c[0] + P, y + 26 + j * 42), ln, font=F_BS, fill=INK)
    img.save(out)
    print(img.size)


if __name__ == "__main__":
    main(sys.argv[1])
