"""Standard Lettering v1.2, langkah 3.4-3.11: pembina prompt ikut model (kod, menggantikan contoh tulisan tangan khas.py).

Isi datang daripada dua sumber sahaja: blok isi kad (kad.BLOK) dan Spesifikasi Teks (kad.AYAT). Setiap aturan model
di bawah hanya menentukan CARA MENULIS isi itu. Kad + ayat + model yang sama memberi prompt yang sama.
Model: klein4b, zturbo, ernie (prompt mentah untuk PE), moss, klein3, qwen, glm. Mod hitam putih sahaja.

Guna: python3 pembina.py                 -> semak semua kad x ayat x model (3.11)
      python3 pembina.py K3H klein4b     -> cetak satu prompt
      python3 pembina.py --banding       -> banding K3H dengan contoh tulisan tangan khas.py
      python3 pembina.py --daftar        -> daftar aturan setiap model (bahagian standard, rev, status, sumber)
"""
import difflib
import json
import os
import re
import sys

import kad

VERSI = "v1.2-p1"
# Daftar aturan model (standard 3.12). Setiap model ada SATU baris di sini, SATU fungsi aturan di bawah dan SATU
# bahagian 3.x dalam docs/lettering-standard.md. Model baharu: ikut "Kaedah model baharu" (3.12), kemudian tambah
# baris + fungsi + bahagian. Model yang belum ada baris memakai rangka am (kad.bina) dan ditanda "am".
# rev r0 = ditulis daripada sumber sahaja, belum diuji; r1+ = sudah diuji pada imej.
DAFTAR = {
    "klein4b": dict(nama="FLUX.2 klein 4B", bahagian="3.4", rev="r1", tarikh="2026-11-26",
                    status="diuji: K3H, CPU, 3 seed", sumber="kad model BFL (rasmi); panduan BFL (lemah)"),
    "zturbo": dict(nama="Z-Image Turbo", bahagian="3.5", rev="r1", tarikh="2026-11-26",
                   status="diuji: K3H, CPU, 3 seed", sumber="pasukan Z-Image di Hugging Face + pe.py (rasmi)"),
    "ernie": dict(nama="ERNIE-Image-Turbo", bahagian="3.6", rev="r1", tarikh="2026-11-26",
                  status="diuji: K3H, CPU, 3 seed", sumber="dokumen diffusers + kad model (rasmi)"),
    "moss": dict(nama="MOSS-Image SFT + LoRA 8 langkah", bahagian="3.7", rev="r1", tarikh="2026-11-26",
                 status="diuji: K3H, CPU, 3 seed", sumber="kad model + panduan MOSS (rasmi); kad LoRA (pihak ketiga)"),
    "klein3": dict(nama="FLUX 3 Image Klein", bahagian="3.8", rev="r0", tarikh="2026-11-26",
                   status="diuji: 3 kad, CPU, 9/9; LESEN BELUM DITERIMA", sumber="kad model + system_prompts.json (rasmi)"),
    "qwen": dict(nama="Qwen-Image-2512", bahagian="3.9", rev="r0", tarikh="2026-11-26",
                 status="belum diuji", sumber="kad model + prompt_utils.py (rasmi)"),
    "glm": dict(nama="GLM-Image", bahagian="3.10", rev="r0", tarikh="2026-11-26",
                status="belum diuji", sumber="kad model + prompt_utils.py (rasmi)"),
}
REV = {k: v["rev"] for k, v in DAFTAR.items()}
MODEL = list(REV)
W, H = 768, 1024
# Ubahan CALON kitaran QC (langkah 5): hanya hidup bila dinamakan dalam PEMBINA_UJI (dipisah koma). Ubahan yang
# berjaya ditulis balik ke aturan (rev naik) dan dibuang dari sini; yang gagal dicatat dalam standard dan dibuang.
# Tiada calon semasa. (26 Nov 2026: 'zturbo_satu_baris' diuji pada K8G, tidak berjaya, dibuang.)
UJI = {u for u in os.environ.get("PEMBINA_UJI", "").split(",") if u}
SATU = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
KE = ["first", "second", "third", "fourth", "fifth", "sixth"]
FUNGSI = {"utama": "title", "sokongan": "supporting line", "penyambung": "connecting word"}
KATA_KUALITI = re.compile(r"\b(masterpiece|best quality|8k|4k|ultra hd|award[- ]winning)\b", re.I)
NAMA_FONT = re.compile(r"\b(helvetica|arial|futura|bebas|impact|garamond|times new roman|comic sans|gotham|"
                       r"montserrat|lobster|pacifico|canva|adobe|pinterest)\b", re.I)


def cap(s):
    return s[:1].upper() + s[1:]


def bahan(kid, aid):
    """Lapan blok isi (3.2) bagi satu kad x satu ayat: frasa kad + baris teks dengan peranan."""
    b, a, k = kad.BLOK[kid], kad.AYAT[aid], kad.KAD[kid]
    n, nampak, baris = len(a["baris"]), {}, []
    utama = [i for i, (_, r) in enumerate(a["baris"]) if r == "utama"]
    for i, (t, r) in enumerate(a["baris"]):
        h = b["huruf"][r]
        kunci = h.get("penuh") or h["bekas"]
        l = dict(i=i, n=n, q=kad.kes(t, k["huruf"][r][0]), peranan=r, bekas=h.get("bekas"), nama=h.get("nama"),
                 dalam=h.get("dalam"), penuh=h.get("penuh"), ringkas=h.get("ringkas"), dulu=nampak.get(kunci),
                 ke=sum(1 for x in baris if x["peranan"] == r),
                 tertinggi=b.get("tertinggi") == "akhir" and bool(utama) and i == utama[-1] and len(utama) > 1,
                 tengah=bool(h.get("bekas")) and n % 2 == 1 and i == n // 2)
        l["kata"], l["ialah"] = ("words", "are") if " " in l["q"] else ("word", "is")
        nampak.setdefault(kunci, i)
        baris.append(l)
    sisi = next((l for l in baris if l["bekas"] and b.get("sisi")), None)
    return dict(kid=kid, aid=aid, b=b, baris=baris, n=n, nw=len(a["ayat"].split()), sisi=sisi,
                petikan=[l["q"] for l in baris], tepi_pct=k["ruang_tepi"])


def latar(b, kata="background"):
    return f"{b['latar_warna']} {kata}" + (f" with {b['latar_isi']}" if b.get("latar_isi") else "")


def latar_tepi(b, kata="background"):
    """Latar + ruang tepi dalam satu frasa (elak 'with ... with ...')."""
    return latar(b, kata) + (" and " if b.get("latar_isi") else " with ") + b["margin"]


def tempat(l, baris, atas, kedua, lain, bawah, lepas):
    """Kata tempat bagi satu baris, atas ke bawah."""
    i, n = l["i"], l["n"]
    if i == 0:
        return atas
    if i == n - 1:
        return bawah
    if baris[i - 1]["bekas"]:
        return lepas.format(nama=baris[i - 1]["nama"])
    return kedua if i == 1 else lain


def frasa(l, rujuk=None):
    """Bentuk huruf: penuh pada sebutan pertama, 'the same <ringkas>' pada ulangan."""
    if l["dulu"] is None:
        return l["penuh"]
    return f"the same {l['ringkas']}" + (rujuk(l["dulu"]) if rujuk else "")


def tambahan(b):
    return [b[x] for x in ("hierarki", "hiasan") if b.get(x)]


def bawah_ada_hiasan(b):
    return any(h["pada"] == "bawah" for h in b["hiasan_kotak"])


# ---------- 3.4 FLUX.2 klein 4B: satu perenggan prosa; gaya di dalam ayat baris itu ----------
def klein4b(m):
    b, L = m["b"], m["baris"]
    s = [f"A black-and-white {b['medium']} in portrait format, {b['gaya']} artwork on a {latar(b)}."]
    c = (f"{cap(SATU[m['n'] - 1])} lines of white lettering are stacked in {b['bentuk']} in the center of the "
         f"poster, with {b['margin']} around it")
    s.append(c + (f", and the whole block {b['condong']}." if b.get("condong") else "."))
    for l in L:
        a = tempat(l, L, "At the top", "Directly beneath it", "Below it", "At the bottom", "Below the {nama}")
        if l["bekas"]:
            a = "In the middle of the block" if l["tengah"] else a
            t = (f'{a} sits a {l["bekas"]}, and inside that {l["nama"]} the {l["kata"]} "{l["q"]}" {l["ialah"]} '
                 f'printed in {l["dalam"]}')
            if l is m["sisi"]:
                t += f', with {b["sisi"]["frasa"]} on each side of the {l["nama"]}'
        else:
            t = (f'{a}, the {l["kata"]} "{l["q"]}" {l["ialah"]} written in '
                 f'{frasa(l, lambda d: " as the top line" if d == 0 else "")}')
        s.append(t + (", and it is the largest line of all." if l["tertinggi"] else "."))
    if b.get("sentuh"):
        s.append(f"The lines {b['sentuh']}.")
    s += tambahan(b)
    ekor = "no other lettering below the last line" if bawah_ada_hiasan(b) else "nothing below the last line"
    s.append(f"The poster shows only these {SATU[m['nw'] - 1]} words, each of them once, in pure white and black "
             f"with {', '.join('no ' + x for x in b['tiada'])}, and {ekor}.")
    return " ".join(s)


# ---------- 3.5 Z-Image Turbo: huraian objektif panjang; baris bernombor; had sebagai ayat positif ----------
def zturbo(m):
    b, L = m["b"], m["baris"]
    lebar = ("the middle two thirds" if m["tepi_pct"] >= 14 else
             "the middle three quarters" if m["tepi_pct"] >= 10 else "most")
    s = [f"A {b['medium']} design in portrait orientation.",
         f"The entire background is a flat {latar(b, 'surface')}. All lettering is pure white with {b['tepi']}.",
         f"The poster contains exactly {SATU[m['nw'] - 1]} words arranged as {SATU[m['n'] - 1]} stacked lines that "
         f"form {b['bentuk']} centered on the canvas; the block occupies {lebar} of the width and leaves "
         f"{b['margin']} on all four sides."]
    if b.get("condong") and b.get("sentuh"):
        s.append(f"The block {b['condong']}, and neighbouring lines {b['sentuh']}.")
    elif b.get("condong") or b.get("sentuh"):
        s.append(f"The block {b['condong']}." if b.get("condong") else f"Neighbouring lines {b['sentuh']}.")
    for l in L:
        p = ", at the top," if l["i"] == 0 else ", at the bottom," if l["i"] == l["n"] - 1 else ""
        if l["bekas"]:
            t = (f'Line {SATU[l["i"]]}{p} is a {l["bekas"]}' + (" placed at the center of the block" if l["tengah"] else "") +
                 f'; inside the {l["nama"]} the {l["kata"]} "{l["q"]}" {l["ialah"]} set in {l["dalam"]}')
            if l is m["sisi"]:
                t += f'; {b["sisi"]["frasa"]} sit on each side of the {l["nama"]}'
        else:
            t = f'Line {SATU[l["i"]]}{p} reads "{l["q"]}" in {frasa(l, lambda d: f" as line {SATU[d]}")}'
        s.append(t + (", and it is the tallest line of the poster." if l["tertinggi"] else "."))
    s += tambahan(b)
    s.append(f"The only text in the image is these {SATU[m['nw'] - 1]} words, each appearing once. The image uses "
             f"only pure white and pure black, {b['ada']}.")
    return " ".join(s)


# ---------- 3.6 ERNIE-Image-Turbo: prompt mentah pendek; PE rasmi yang mengembangkan ----------
def ernie(m):
    b, L = m["b"], m["baris"]
    butir = []
    for l in L:
        if l["bekas"]:
            t = f'"{l["q"]}" in {l["dalam"]} inside a {l["bekas"]}'
            if l is m["sisi"]:
                t += f' with {b["sisi"]["frasa"]} on each side of the {l["nama"]}'
        else:
            t = f'"{l["q"]}" in {l["penuh"] if l["dulu"] is None else l["ringkas"]}'
        butir.append(t + (", the tallest line" if l["tertinggi"] else ""))
    s = [f"A black and white {b['medium']}, portrait.",
         f"{cap(latar(b))}, white lettering.",
         f"{cap(SATU[m['n'] - 1])} stacked lines in {b['bentuk']} in the center" +
         (f" that {b['condong']}" if b.get("condong") else "") + ": " + "; ".join(butir) + "."]
    s += tambahan(b)
    s.append(f"Only these {SATU[m['nw'] - 1]} words, no other text, pure black and white, "
             f"{', '.join('no ' + x for x in b['tiada'])}, {b['gaya']} style, {b['margin']}.")
    return " ".join(s)


# ---------- kotak (3.7): piksel, asalan tengah kanvas, [y_atas, x_kiri, y_bawah, x_kanan] ----------
def bulat(x, g=8):
    return int(round(x / g) * g)


def kotak(m):
    """Unsur dari atas ke bawah dengan kotak. Ukuran: kad.BLOK[..]['ukuran'] jika ada; jika tidak, lalai daripada ruang tepi."""
    b, L, u = m["b"], m["baris"], m["b"].get("ukuran") or {}
    bw = bulat(W * (1 - 2 * m["tepi_pct"] / 100), 16)
    lalai = dict(utama=(bw, 168), tertinggi=(bw, 216), sokongan=(bw if b["sama_lebar"] else bulat(bw * 0.84, 16), 136),
                 penyambung=(bw if b["sama_lebar"] else bulat(bw * 0.5, 16), 80), sisi=(72, 64))
    saiz = lambda nama: u.get(nama) or lalai[nama]
    un = []
    for h in b["hiasan_kotak"]:
        if h["pada"] == "atas":
            un.append(dict(jenis="hiasan", h=h, wh=(bulat(bw * 0.6, 16), 64), sela=0))
    for l in L:
        w, t = saiz("tertinggi" if l["tertinggi"] else l["peranan"])
        if l["bekas"] and l["peranan"] != "penyambung" and not u:
            w = bw
        un.append(dict(jenis="teks", l=l, wh=(w, t), sela=8 if l["bekas"] else 0))
    for h in b["hiasan_kotak"]:
        if h["pada"] == "bawah":
            un.append(dict(jenis="hiasan", h=h, wh=(bulat(bw * 0.6, 16), 64), sela=0))
    sela = [max(un[i]["sela"], un[i + 1]["sela"]) for i in range(len(un) - 1)]
    had = H * (1 - 2 * m["tepi_pct"] / 100)
    jumlah = sum(x["wh"][1] for x in un) + sum(sela)
    if jumlah > had and not u:  # terlalu tinggi: kecilkan semua baris sama rata
        f = (had - sum(sela)) / (jumlah - sum(sela))
        for x in un:
            x["wh"] = (x["wh"][0], max(32, bulat(x["wh"][1] * f)))
        jumlah = sum(x["wh"][1] for x in un) + sum(sela)
    y = -bulat(jumlah / 2)
    for i, x in enumerate(un):
        w, t = x["wh"]
        x["bbox"] = [y, -w // 2, y + t, w // 2]
        y += t + (sela[i] if i < len(sela) else 0)
        if x["jenis"] == "teks" and x["l"] is m["sisi"]:
            sw, st = saiz("sisi")
            yc = (x["bbox"][0] + x["bbox"][2]) // 2
            x["sisi"] = [[yc - st // 2, -w // 2 - 24 - sw, yc + st // 2, -w // 2 - 24],
                         [yc - st // 2, w // 2 + 24, yc + st // 2, w // 2 + 24 + sw]]
    return un


def kedudukan(l):
    if l["n"] == 1:
        return "The only line."
    asas = "Top line of the block" if l["i"] == 0 else "Bottom line" if l["i"] == l["n"] - 1 else f"{cap(KE[l['i']])} line"
    return asas + (", the tallest line of the poster." if l["tertinggi"] else ".")


# ---------- 3.7 MOSS-Image SFT + LoRA: satu objek JSON; perkataan hanya dalam medan text ----------
def moss_layout(m):
    b, L = m["b"], m["baris"]
    kump = {}
    for l in L:
        kump.setdefault(l["bekas"] or l["ringkas"], []).append(l)
    nama_baris = lambda l: "top" if l["i"] == 0 else "bottom" if l["i"] == l["n"] - 1 else KE[l["i"]]
    sen = lambda x: ", ".join(x[:-1]) + (" and " if len(x) > 1 else "") + x[-1]
    ayat = []
    for kunci, ls in kump.items():
        siapa = sen([nama_baris(l) for l in ls])
        ada = "lines are" if len(ls) > 1 else "line is"
        ayat.append(f"the {siapa} {ada} " + (f"black lettering inside a {kunci}" if ls[0]["bekas"] else kunci))
    cp = [f"A black-and-white {b['medium']}, {b['gaya']}, on a {latar_tepi(b)}.",
          f"{cap(SATU[m['n'] - 1])} stacked lines of white lettering form {b['bentuk']} in the center" +
          (f" that {b['condong']}." if b.get("condong") else "."),
          cap(sen(ayat)) + "."] + tambahan(b)
    cp.append(f"Only black and white, {', '.join('no ' + x for x in b['tiada'])}, no other text.")
    items = []
    for x in kotak(m):
        if x["jenis"] == "hiasan":
            items.append({"label": "object", "caption": cap(x["h"]["ayat"]) + ".", "bbox": x["bbox"]})
            continue
        l = x["l"]
        if l["bekas"]:
            c = f"{cap(l['dalam'])} inside a {l['bekas']}, centered."
        else:
            c = f"{cap(l['penuh'])}, white, {b['gaya']}. {kedudukan(l)}"
        items.append({"label": "text", "caption": c, "text": l["q"], "bbox": x["bbox"]})
        for sisi, bb in zip(("left", "right"), x.get("sisi", [])):
            items.append({"label": "object", "caption": f"{cap(b['sisi']['frasa'])} {sisi} of the {l['nama']}.",
                          "bbox": bb})
    return {"summary": {"meta": ["poster"], "canvas": "single", "caption": " ".join(cp)}, "items": items,
            "bbox_coord_space": "abs_centralized", "bbox_format": "yxyx"}


def moss(m):
    return json.dumps(moss_layout(m), ensure_ascii=False)


# ---------- 3.8 FLUX 3 Image Klein: kapsyen penuh + jadual kotak JSON (grid 0-1000) ----------
def grid(bb):
    y0, x0, y1, x1 = bb
    return [round((y0 + H / 2) / H * 1000), round((x0 + W / 2) / W * 1000),
            round((y1 + H / 2) / H * 1000), round((x1 + W / 2) / W * 1000)]


def klein3_bahagian(m):
    b, L = m["b"], m["baris"]
    jadual = [{"id": "background_1", "bbox": [0, 0, 1000, 1000], "desc": f"A flat {latar(b, 'field')}."}]
    s = [f"{cap(b['gaya'])} {b['medium']} in black and white, portrait format.",
         f"A {b['latar_warna']} background <background_1>" + (f" with {b['latar_isi']}" if b.get("latar_isi") else "") +
         f" fills the frame with {b['margin']}.",
         f"{cap(SATU[m['n'] - 1])} lines of white lettering are stacked in {b['bentuk']} in the center of the frame."]
    if b.get("condong") and b.get("sentuh"):
        s.append(f"The block {b['condong']}, and neighbouring lines {b['sentuh']}.")
    elif b.get("condong") or b.get("sentuh"):
        s.append(f"The block {b['condong']}." if b.get("condong") else f"Neighbouring lines {b['sentuh']}.")
    bil, baris_ayat, hias_ayat = {}, [], []

    def idbaru(nama):
        bil[nama] = bil.get(nama, 0) + 1
        return f"{nama}_{bil[nama]}"

    for x in kotak(m):
        if x["jenis"] == "hiasan":
            i = idbaru(x["h"]["nama"])
            hias_ayat.append(f"{x['h']['ayat']} <{i}>.")
            jadual.append({"id": i, "bbox": grid(x["bbox"]), "desc": cap(x["h"]["frasa"]) + "."})
            continue
        l = x["l"]
        a = tempat(l, L, "At the top", "Directly below it", "Below it", "At the bottom", "Below the {nama}")
        i = f"En_Text_{l['i'] + 1}"
        if l["bekas"]:
            a = "In the center" if l["tengah"] else a
            t = f"{a}, a {l['bekas']} <{i}>"
            if "sisi" in x:
                kiri, kanan = idbaru(b["sisi"]["nama"]), idbaru(b["sisi"]["nama"])
                t += f" with {b['sisi']['frasa']} on its left <{kiri}> and on its right <{kanan}>"
                jadual.append({"id": kiri, "bbox": grid(x["sisi"][0]), "desc": cap(b["sisi"]["frasa"]) + "."})
            jadual.append({"id": i, "bbox": grid(x["bbox"]),
                           "desc": f'{cap(l["bekas"])} carrying {l["dalam"]}, reading "{l["q"]}".'})
            if "sisi" in x:
                jadual.append({"id": kanan, "bbox": grid(x["sisi"][1]), "desc": cap(b["sisi"]["frasa"]) + "."})
        else:
            if l["tertinggi"]:
                t = f"{a}, the tallest line, in {l['ringkas']} <{i}>"
            else:
                t = f"{a}, {'another' if l['dulu'] is not None else 'a'} line of {l['ringkas']} <{i}>"
            jadual.append({"id": i, "bbox": grid(x["bbox"]),
                           "desc": f'{cap(l["penuh"])} in pure white, reading "{l["q"]}"' +
                                   (", the tallest line." if l["tertinggi"] else ".")})
        baris_ayat.append(t + ".")
    s += baris_ayat + hias_ayat
    s += [b[x] for x in ("hierarki", "hiasan_baki") if b.get(x)]
    if b.get("hiasan") and not b["hiasan_kotak"]:
        s.append(b["hiasan"])
    s.append(f"The poster holds only these {SATU[m['n'] - 1]} lines of lettering, in pure white and pure black, "
             f"with {b['ada']}.")
    return " ".join(s), jadual


def klein3(m):
    kapsyen, jadual = klein3_bahagian(m)
    return kapsyen + " " + json.dumps(jadual, ensure_ascii=False)


# ---------- 3.9 Qwen-Image-2512: kurang 200 perkataan; kedudukan, petikan, gaya ----------
def qwen(m):
    b, L = m["b"], m["baris"]
    s = [f"Typography poster design: {b['gaya']} {b['medium']}, black and white, portrait.",
         f"{cap(latar_tepi(b))}.",
         f"{cap(SATU[m['n'] - 1])} stacked lines of white lettering form {b['bentuk']} in the center" +
         (f", and the block {b['condong']}." if b.get("condong") else ".")]
    for l in L:
        a = tempat(l, L, "At the top", "Directly below it", "Below it", "At the bottom", "Below the {nama}")
        if l["bekas"]:
            a = "In the center" if l["tengah"] else a
            t = f'{a}, a {l["bekas"]} with the {l["kata"]} "{l["q"]}" in {l["dalam"]}'
            if l is m["sisi"]:
                t += f', {b["sisi"]["frasa"]} on its left and on its right'
        else:
            t = f'{a}, "{l["q"]}" in {frasa(l)}'
        s.append(t + (", the tallest line." if l["tertinggi"] else "."))
    if b.get("sentuh"):
        s.append(f"The lines {b['sentuh']}.")
    s += tambahan(b)
    s.append(f"Clean graphic design, {b['ada']}, pure black and white only. No other text, no people, no objects.")
    return " ".join(s)


# ---------- 3.10 GLM-Image: satu perenggan naratif; kedudukan, fungsi, petikan, gaya ----------
def glm(m):
    b, L = m["b"], m["baris"]
    s = [f"A graphic design poster in the style of a {b['gaya']} {b['medium']}, portrait format, printed in pure "
         f"black and white.",
         f"The whole poster is a {latar_tepi(b, 'surface')}, and all lettering is white print with "
         f"{b['tepi']}, arranged as {SATU[m['n'] - 1]} stacked lines in {b['bentuk']} at the center" +
         (f" that {b['condong']}." if b.get("condong") else ".")]
    for l in L:
        a = tempat(l, L, "At the top of the block", "Directly beneath it", "Below it", "At the bottom",
                   "Below the {nama}")
        f = "connecting phrase" if l["peranan"] == "penyambung" and l["kata"] == "words" else FUNGSI[l["peranan"]]
        if l["peranan"] == "utama":
            f = "closing title" if l["i"] == l["n"] - 1 and l["ke"] else "main title" if not l["ke"] else f"{KE[l['ke']]} title"
        elif l["ke"]:
            f = f"{KE[l['ke']]} {f}"
        if l["bekas"]:
            a = "At the center" if l["tengah"] else a
            t = f'{a} sits a {l["bekas"]}, and the {f} printed on it reads "{l["q"]}" in {l["dalam"]}'
            if l is m["sisi"]:
                t += f', with {b["sisi"]["frasa"]} as decoration on the left and on the right of the {l["nama"]}'
        else:
            t = f'{a}, the {f} reads "{l["q"]}" in {frasa(l)}'
        s.append(t + (" and is the tallest line of the poster." if l["tertinggi"] else "."))
    if b.get("sentuh"):
        s.append(f"The lines {b['sentuh']}.")
    s += tambahan(b)
    s.append(f"Only these {SATU[m['nw'] - 1]} words appear on the poster, which shows {b['ada']}.")
    return " ".join(s)


ATURAN = dict(klein4b=klein4b, zturbo=zturbo, ernie=ernie, moss=moss, klein3=klein3, qwen=qwen, glm=glm)


def bina(model, kid, aid):
    """Prompt bagi satu model x kad x ayat. Pulang (prompt, petikan Spesifikasi Teks).
    Model tanpa aturan sendiri (tiada dalam DAFTAR): rangka am 3.3 (kad.bina), sehingga aturannya ditulis (3.12)."""
    if model not in ATURAN:
        return kad.bina(kid, aid)
    m = bahan(kid, aid)
    return ATURAN[model](m), m["petikan"]


def rev(model):
    """Rev aturan yang dipakai; 'am' = model belum ada aturan sendiri."""
    return REV.get(model, "am")


# ---------- 3.11 Semakan automatik sebelum jana ----------
PETIK = re.compile(r'"([^"]+)"')


def _sejagat(teks, err):
    """Peraturan sejagat pada teks prosa (petikan dibuang dahulu)."""
    t = PETIK.sub("", teks)
    w = kad.WARNA_LAIN.search(re.sub(r"\bno gray\b", "", t))
    if w:
        err.append("nama warna selain black / white: " + w.group(0))
    if re.search(r"#[0-9a-fA-F]{3,6}\b|\d", t):
        err.append("ada angka / hex")
    if KATA_KUALITI.search(t):
        err.append("ada kata kualiti kosong")
    if NAMA_FONT.search(t):
        err.append("ada nama font / jenama")


def semak(model, kid, aid, prompt=None):
    """Senarai ralat; kosong = lulus. Prompt yang gagal TIDAK dijana."""
    if model not in ATURAN:  # rangka am: semakan pembina v1.1
        pr, q = kad.bina(kid, aid)
        return kad.semak(prompt if prompt is not None else pr, q, kad.AYAT[aid]["ayat"])
    m = bahan(kid, aid)
    spec, err = m["petikan"], []
    p = prompt if prompt is not None else ATURAN[model](m)
    if model == "moss":
        try:
            lay = json.loads(p)
        except ValueError:
            return ["JSON tidak sah"]
        for kunci in ("summary", "items", "bbox_coord_space", "bbox_format"):
            if kunci not in lay:
                err.append(f"kunci {kunci} tiada")
        if err:
            return err
        teks = [i["text"] for i in lay["items"] if i.get("label") == "text"]
        if teks != spec:
            err.append(f"medan text {teks} tidak sama dengan Spesifikasi Teks")
        prosa = " ".join([lay["summary"]["caption"]] + [i["caption"] for i in lay["items"]])
        if PETIK.search(prosa) or any(re.search(rf"\b{re.escape(q)}\b", prosa) for q in spec):
            err.append("perkataan Spesifikasi Teks muncul di luar medan text")
        _sejagat(prosa, err)
        for i in lay["items"]:
            y0, x0, y1, x1 = i["bbox"]
            if not (-H // 2 <= y0 < y1 <= H // 2 and -W // 2 <= x0 < x1 <= W // 2):
                err.append(f"kotak di luar kanvas: {i.get('text') or i['caption'][:30]} {i['bbox']}")
        return err
    if model == "klein3":
        kapsyen, _, ekor = p.partition(" [{")
        try:
            jadual = json.loads("[{" + ekor)
        except ValueError:
            return ["jadual JSON tidak sah"]
        if "\n" in p:
            err.append("bukan satu baris")
        if PETIK.search(kapsyen) or re.search(r"\d", re.sub(r"<[^>]+>", "", kapsyen)):
            err.append("kapsyen ada petikan atau koordinat")
        ids = [r["id"] for r in jadual]
        if sorted(re.findall(r"<([^>]+)>", kapsyen)) != sorted(ids) or len(set(ids)) != len(ids):
            err.append("id kapsyen dan id jadual tidak sepadan / tidak unik")
        if [q for r in jadual for q in PETIK.findall(r["desc"])] != spec:
            err.append("petikan jadual tidak sama dengan Spesifikasi Teks")
        if sum(1 for i in ids if i.startswith("En_Text_")) != m["n"]:
            err.append("bilangan En_Text tidak sama dengan bilangan baris")
        for r in jadual:
            y0, x0, y1, x1 = r["bbox"]
            if not (0 <= y0 < y1 <= 1000 and 0 <= x0 < x1 <= 1000):
                err.append(f"kotak {r['id']} di luar grid")
        _sejagat(re.sub(r"<[^>]+>", "", kapsyen) + " " + " ".join(r["desc"] for r in jadual), err)
        if not 100 <= len(p.split()) <= 350:
            err.append(f"panjang {len(p.split())} perkataan, luar 100-350")
        return err
    q = PETIK.findall(p)
    if q != spec:
        err.append(f"petikan {q} tidak sama dengan Spesifikasi Teks {spec}")
    _sejagat(p, err)
    if "\n" in p:
        err.append("lebih daripada satu perenggan")
    kata = len(p.split())
    if kata > 380:
        err.append(f"{kata} perkataan: mungkin melebihi had token")
    if model == "klein4b":
        if re.search(r"\b(Large|Medium|Small) words:", p) or re.search(r"no signature|no watermark|no logo|no frame", p):
            err.append("klein4b: ada senarai gaya terpisah atau senarai larangan")
    if model == "zturbo":
        if len(re.findall(r"(?:^|\. )Line \w+", p)) != m["n"]:
            err.append("zturbo: bilangan ayat 'Line ...' tidak sama dengan bilangan baris")
        if re.search(r"\bno\b", p.rsplit("The only text", 1)[-1], re.I):
            err.append("zturbo: 'no ...' dalam ayat penutup")
        if not 80 <= kata <= 250:
            err.append(f"zturbo: {kata} perkataan, luar 80-250")
    if model == "qwen":
        if kata >= 200:
            err.append(f"qwen: {kata} perkataan (mesti kurang 200)")
        for x in spec:
            ayat = next(a for a in re.split(r"(?<=\.) ", p) if f'"{x}"' in a)
            if not re.match(r"(At|Directly|Below|In) ", ayat) or f'"{x}" in ' not in ayat:
                err.append(f"qwen: \"{x}\" tanpa kedudukan di depan atau gaya di belakang")
    if model == "glm":
        if ":" in p or re.search(r"\bLine (one|two|three|four|five|six)\b|^\s*[-*\d]", p):
            err.append("glm: ada senarai, nombor baris atau tajuk")
        if W % 32 or H % 32:
            err.append("glm: saiz tidak boleh dibahagi 32")
    return err


PETIK_PE = re.compile(r'"([^"]{1,60})"|“([^”]{1,60})”|‘([^’]{1,60})’|「([^」]{1,60})」|『([^』]{1,60})』|'
                      r"(?<![A-Za-z])'([^']{1,60})'(?![A-Za-z])")
LATIN = re.compile(r"[A-Za-z][A-Za-z' ]*[A-Za-z]|[A-Za-z]")


def semak_pe(hasil, kid, aid):
    """3.6: semakan pada hasil PE ERNIE. Setiap perkataan ada dan tepat; turutan sama; tiada perkataan Latin lain dalam petikan."""
    spec, err, mula = bahan(kid, aid)["petikan"], [], -1
    for q in spec:
        i = hasil.find(q)
        if i < 0:
            err.append(f"PE: \"{q}\" tiada atau ejaan / huruf besar kecil berubah")
        elif i < mula:
            err.append(f"PE: turutan \"{q}\" berubah")
        mula = max(mula, i)
    for kump in PETIK_PE.findall(hasil):
        for kata in LATIN.findall("".join(kump)):
            if kata.strip() not in spec:
                err.append(f"PE: perkataan Latin lain dalam petikan: {kata.strip()!r}")
    return err


def semua():
    gagal, n, kira = [], 0, {}
    for kid in kad.BLOK:
        for aid in kad.AYAT:
            for model in MODEL:
                p = ATURAN[model](bahan(kid, aid))
                e = semak(model, kid, aid, p)
                n += 1
                kira.setdefault(model, []).append(len(p.split()))
                if e:
                    gagal.append((f"{kid}{aid}", model, e))
    for model, k in kira.items():
        print(f"{model:8} rev {REV[model]}  kata min/maks {min(k)}/{max(k)}")
    print(n, "prompt;", len(gagal), "gagal semakan 3.11")
    for g in gagal:
        print("  GAGAL", *g)
    return gagal


def banding():
    import khas
    for model in MODEL:
        p = bina(model, "K3", "H")[0]
        r = difflib.SequenceMatcher(None, khas.PROMPT[model].split(), p.split()).ratio()
        print(f"{model:8} sama perkataan {r:.0%}; kata khas/pembina {len(khas.PROMPT[model].split())}/{len(p.split())}; "
              f"semak: {semak(model, 'K3', 'H', p) or 'lulus'}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(1 if semua() else 0)
    if sys.argv[1] == "--daftar":
        for k, d in DAFTAR.items():
            print(f"{k:8} {d['bahagian']:5} {d['rev']:3} {d['nama']:32} {d['status']:26} {d['sumber']}")
    elif sys.argv[1] == "--banding":
        banding()
    else:
        kid, aid = sys.argv[1][:-1], sys.argv[1][-1]
        for model in sys.argv[2:] or MODEL:
            print(f"--- {model} ({rev(model)}) semak: {semak(model, kid, aid) or 'lulus'}\n{bina(model, kid, aid)[0]}\n")
