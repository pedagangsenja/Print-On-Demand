"""Belajar SK selepas setiap batch: skrip pembetulan (5b) dan kemasan (langkah 6) dibaiki, diberi parameter atau dicipta sendiri.

Keputusan pengguna 27 Nov 2026 (Standard Lettering v1.2, bahagian "Belajar SK"): sama seperti 3.15 (aturan prompt), tetapi
untuk skrip SK. Jalan selepas SETIAP batch, selepas 5b dan langkah 6. Claude laksana TINDAKAN terus (SK baharu dicipta
tanpa tanya; tiada jana imej baharu) dan lapor dalam jadual jawapan.

Baca:
  betul/<batch>/<model>/log_5b.jsonl     SK01-SK04 (betulkan.py): ukuran sebelum / selepas lawan rujukan kad, gagal
  final/<larian>/peranan/log_6.jsonl     SK07, SK08: lulus, gagal, amaran
  belajar/uji_sk/<SK>_<versi>/log_6.jsonl  log uji semula SK versi baharu pada imej sedia ada (imej tidak disimpan)
  final/<larian>/<imej>/info.json        SK06: vektor + saiz cetak siap
  belajar/pengguna.jsonl                 tolak pengguna langkah 7; bahagian sebab yang milik SK (condong, warna, bayang, ...)
  belajar/sk_pengguna.jsonl              keputusan pengguna pada imej siap: {"imej": "<batch>/<model>/<ID>_s<seed>[+Cxxx]",
                                         "keputusan": "lulus"|"tolak", "sebab": "...", "sk": "SK08" (pilihan)}
  belajar/sk_semakan.jsonl               semakan Claude bagi GAGAL / amaran SK: {"imej": ..., "sk": "SK07", "semakan": "silap"|"betul",
                                         "kelas": "..." (pilihan), "versi": "..." (pilihan), "nota": "..."}
                                         silap = kelemahan SK (dibaiki); betul = SK betul (imej input rosak, atau amaran tidak merosakkan)
  belajar/sk_ubahan.json                 semua ubahan SK yang pernah dicuba: cuba / menang / kalah
  belajar/stor/data/...                  salinan stor dashboard: likes (♥), warna/items (kod C dipadam = tolak warna)
  qc/*_snc.json, kad.py, skrip/SK*.py    kod S/C, ciri kad yang perlu SK, versi setiap SK
Tulis:
  belajar/sk_log.jsonl                   sejarah: satu baris = satu imej x SK x versi (versi lama kekal untuk banding)
  belajar/sk_ringkasan.json              setiap SK: prestasi ikut versi, cacat berulang, TINDAKAN
  ../../data/export/ai_tests/sk_belajar.json   dataset dashboard `sk_belajar` (satu baris = satu SK atau calon SK baharu)
Jalan: python3 belajar_sk.py   (tiada jana; tiada ubah skrip: TINDAKAN dilaksana oleh Claude ikut standard)
"""
import datetime
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

VERSI = "s1 (27 Nov 2026)"
B = os.path.join(HERE, "belajar")
SKRIP = os.path.join(HERE, "skrip")
STOR = os.path.join(B, "stor", "data")
EXPORT = os.path.normpath(os.path.join(HERE, "..", "..", "data", "export", "ai_tests", "sk_belajar.json"))

# Kelas cacat SK, ikut turutan (padanan pertama menang bagi setiap bahagian sebab). Pemilik = SK yang bertanggungjawab.
# maklumat=True: catatan kerja biasa, bukan cacat (tidak dikira, tidak perlu disemak).
# SK baharu: tambah kelasnya di sini dengan pemilik SK itu (kaedah skrip baharu, langkah 6).
KELAS_SK = [
    ("sentuh_tepi", "Dakwat menyentuh tepi kanvas", r"menyentuh tepi|sentuh tepi|terpotong", "SK02", False),
    ("ruang_tepi", "Ruang tepi lain daripada kad", r"ruang tepi", "SK02", False),
    ("condong", "Sudut condong lain daripada kad", r"condong", "SK01", False),
    ("kedudukan", "Blok tidak di tengah", r"atas tengah|bawah tengah|tidak di tengah|lari dari tengah", "SK03", False),
    ("kelabu", "Kelabu, lorekan atau latar tidak hitam", r"kelabu(?! bayang)|lorekan|latar tidak hitam|tepi kabur", "SK04", False),
    ("label", "Label tidak dikesan sebagai segi empat", r"bukan segi empat|tiada label", "SK07", False),
    ("belah_baris", "Baris salah dibelah (warna ikut baris salah)", r"salah dibelah|tidak dapat dibelah|masuk teras baris", "SK07", False),
    ("sambungan", "Huruf bertaut dibelah (warna di sambungan)", r"bertaut dibelah", "SK07", False),
    ("ekor_label", "Ekor huruf di luar label dipulangkan", r"ekor huruf", "SK07", True),
    ("tiada_huruf", "Tiada huruf dikesan", r"tiada huruf dikesan", "SK07", False),
    ("warna", "Warna salah atau di tempat salah", r"warna (salah|lain|tidak|di tempat)|salah warna|ikut kuning", "SK07", False),
    ("bayang", "Bayang lain daripada kad", r"bayang", "SK08", False),
    ("tekstur", "Tekstur lain daripada kad", r"tekstur|grain|lusuh|kapur", "SK06", False),
    ("vektor", "Tepi vektor kasar atau saiz cetak salah", r"vektor|surih|bergerigi|\bDPI\b|pecah", "SK06", False),
]
KELAS = {k: dict(nama=n, pola=re.compile(p, re.I), sk=s, info=i) for k, n, p, s, i in KELAS_SK}
POLA_SK = re.compile("|".join(p for _, _, p, _, _ in KELAS_SK), re.I)  # dipakai belajar.py: bahagian ini bukan kerja prompt
LANGKAH = {"SK01": "5b", "SK02": "5b", "SK03": "5b", "SK04": "5b", "SK05": "1, 5b", "SK06": "6", "SK07": "6", "SK08": "6"}
SK_5B = ["SK01", "SK02", "SK03", "SK04"]  # dijalankan betulkan.py; versi log = VERSI betulkan.py (naikkan bila mana-mana berubah)
JENIS_BAYANG = {"dalam"}  # jenis bayang yang SK08 boleh buat; bayang lembut K1 belum (kemas kini bila SK menyokongnya)
TANPA_VERSI = {"SK06": "SK06 v1 (27 Nov 2026)"}  # info.json lama tanpa versi = kod yang sama (VERSI ditambah tanpa ubah kod)
HABIS_N = 3  # ubahan KALAH bagi kelas yang sama sebelum lapor pengguna


def baca_json(p, lalai):
    return json.load(open(p)) if os.path.exists(p) else lalai


def baca_jsonl(p):
    return [json.loads(x) for x in open(p) if x.strip()] if os.path.exists(p) else []


def kelas_sk(teks, semua=False):
    """Kelas SK bagi setiap bahagian teks (pisah ';'). semua=True: bahagian tanpa kelas dipulangkan sebagai 'lain'."""
    out = []
    for bah in re.split(r";", teks or ""):
        bah = bah.strip()
        if not bah:
            continue
        k = next((k for k, v in KELAS.items() if v["pola"].search(bah)), None)
        if k:
            out.append(k)
        elif semua:
            out.append("lain")
    return out


def daftar_sk():
    """Daftar SK daripada skrip/SK??_*.py: id, nama, langkah, versi semasa (daripada kod)."""
    v5b = re.search(r'VERSI\s*=\s*"([^"]+)"', open(os.path.join(SKRIP, "betulkan.py")).read())
    out = {}
    for f in sorted(glob.glob(os.path.join(SKRIP, "SK[0-9][0-9]_*.py"))):
        sid, nama = os.path.basename(f)[:4], os.path.basename(f)[5:-3].replace("_", " ")
        src = open(f).read()
        m = re.search(r'VERSI\s*=\s*(?:"SK\d+",\s*)?"([^"]+)"', src)
        lk = re.search(r'^LANGKAH\s*=\s*"([^"]+)"', src, re.M)
        versi = v5b[1] if sid in SK_5B else (m[1] if m else "?")
        out[sid] = dict(sk=sid, nama=nama, fail=os.path.basename(f), langkah=lk[1] if lk else LANGKAH.get(sid, "?"),
                        versi=versi, src=src)
    return out


def kunci(path):
    """'raw/v12-cpu/moss/K3K_s42.png' atau '../betul/v12-cpu/moss/K3K_s42.png' -> 'v12-cpu/moss/K3K_s42'."""
    p = path.replace("\\", "/").split("/")
    return "/".join(p[-3:])[:-4] if len(p) >= 3 else path


def baris_log():
    """Baris sejarah daripada log SK semasa: satu baris = satu imej x SK x versi."""
    rows = []
    for f in sorted(glob.glob(os.path.join(HERE, "betul", "*", "*", "log_5b.jsonl"))):
        for r in baca_jsonl(f):
            g = r.get("gagal") or []
            kel = [(x, kelas_sk(x)) for x in g]
            for sid in SK_5B:
                t = r.get("tindakan", {}).get(sid, {})
                mine = [x for x, k in kel if KELAS.get((k or ["lain"])[0], {}).get("sk") == sid]
                rows.append(dict(sk=sid, versi=r.get("versi", "?"), imej=kunci(r["imej"]), larian=f.split(os.sep)[-3],
                                 kad=r.get("kad", ""), jalan=bool(t.get("jalan", sid == "SK04")), gagal=mine, amaran=[]))
    semua_asas = {}
    for f in sorted(glob.glob(os.path.join(HERE, "final", "*", "peranan", "log_6.jsonl"))
                    + glob.glob(os.path.join(B, "uji_sk", "*", "log_6.jsonl"))):   # uji semula SK (log sahaja, tiada imej)
        larian, L = f.split(os.sep)[-3] if f.split(os.sep)[-2] == "peranan" else "uji_sk/" + f.split(os.sep)[-2], baca_jsonl(f)
        asas = {r["nama"]: kunci(r["imej"]) for r in L if r.get("skrip") == "SK07"}
        for r in L:
            nama = r["nama"][:-7] if r["nama"].endswith("_bayang") else r["nama"]
            m = re.match(r"(.+?)_(C\d+)$", nama)
            pokok = m[1] if m else nama
            key = asas.get(pokok) or asas.get(nama) or f"{larian}/{nama}"
            if m:
                key += "+" + m[2]
            rows.append(dict(sk=r.get("skrip", "?"), versi=r.get("versi", "?"), imej=key, larian=larian, kad=r.get("kad", ""),
                             jalan=True, gagal=list(r.get("gagal") or []), amaran=list(r.get("amaran") or [])))
        semua_asas.update(asas)
    for g in sorted(glob.glob(os.path.join(HERE, "final", "*", "*", "info.json"))
                    + glob.glob(os.path.join(B, "uji_sk", "*", "*", "info.json"))):   # SK06 (final, atau uji semula)
        p = g.split(os.sep)
        larian = p[-3] if "uji_sk" not in p else "uji_sk/" + p[-3]
        nama = p[-2]
        m = re.match(r"(.+?)_(C\d+)$", nama)
        key = semua_asas.get(m[1] if m else nama, f"{larian}/{nama}") + ("+" + m[2] if m else "")
        info = baca_json(g, {})
        v = info.get("versi") or TANPA_VERSI["SK06"]
        rows.append(dict(sk="SK06", versi=v, imej=key, larian=larian, kad=(info.get("tekstur") or {}).get("kad", ""),
                         jalan=True, gagal=list(info.get("gagal") or []), amaran=list(info.get("amaran") or [])))
    return rows


def gabung_sejarah(baru):
    """Sejarah sk_log.jsonl + baris baharu; kunci (sk, versi, imej); baris terbaharu menang."""
    p = os.path.join(B, "sk_log.jsonl")
    d = {(r["sk"], r["versi"], r["imej"]): r for r in baca_jsonl(p)}
    for r in baru:
        d[(r["sk"], r["versi"], r["imej"])] = {k: r[k] for k in ("sk", "versi", "imej", "larian", "kad", "jalan", "gagal", "amaran")}
    rows = sorted(d.values(), key=lambda r: (r["sk"], r["versi"], r["imej"]))
    with open(p, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return rows


def isyarat_pengguna():
    """Tolak / lulus pengguna pada imej siap, dan kod C yang dipadam daripada Daftar S/C. Pulang {imej: [(keputusan, sebab, sk)]}."""
    out = defaultdict(list)
    for r in baca_jsonl(os.path.join(B, "pengguna.jsonl")):  # langkah 7 (3.15): hanya bahagian sebab yang milik SK
        if r.get("keputusan") == "tolak" and kelas_sk(r.get("sebab", "")):
            out[r["imej"]].append(("tolak", r.get("sebab", ""), None, "pengguna.jsonl"))
    for r in baca_jsonl(os.path.join(B, "sk_pengguna.jsonl")):
        out[r["imej"]].append((r.get("keputusan", "tolak"), r.get("sebab", ""), r.get("sk"), "sk_pengguna.jsonl"))
    warna = os.path.join(STOR, "warna", "items")
    ada = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(warna, "*.json"))} if os.path.isdir(warna) else None
    suka_blob = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(STOR, "likes", "items", "*.json"))}
    suka = set()
    for f in glob.glob(os.path.join(HERE, "qc", "*_snc.json")):
        batch = os.path.basename(f)[:-9].replace("_", "-")
        rek = baca_json(f, {}).get("rekod", {})
        s_imej = {k: f"{batch}/{v['imej']}" for k, v in rek.items() if "imej" in v}
        for kod, v in rek.items():
            key = s_imej.get(kod) or (s_imej.get(v.get("gaya", "")) and f"{s_imej[v['gaya']]}+{kod}")
            if not key:
                continue
            if v.get("blob") in suka_blob:
                suka.add(key)
            if kod.startswith("C") and ada is not None and kod not in ada:
                out[key].append(("tolak", "", "SK07", f"Daftar S/C: {kod} dipadam"))
    return out, suka


def semakan():
    d = defaultdict(list)
    for r in baca_jsonl(os.path.join(B, "sk_semakan.jsonl")):
        d[(r["imej"], r["sk"])].append(r)
    return d


def nilai(rows, sem, user):
    """Setiap baris: cacat SK (dikira), cacat input (SK betul), amaran belum disemak, tolak pengguna."""
    out = []
    for r in rows:
        s = [x for x in sem.get((r["imej"], r["sk"]), []) if x.get("versi") in (None, r["versi"])]
        betul = any(x["semakan"] == "betul" for x in s)
        silap = [x for x in s if x["semakan"] == "silap"]
        cacat, input_rosak, belum = [], [], []
        for t in r["gagal"]:
            k = (kelas_sk(t) or ["lain"])[0]
            (input_rosak if betul and not silap else cacat).append(k)
            if not s:
                belum.append(t)
        for t in r["amaran"]:
            k = (kelas_sk(t) or ["lain"])[0]
            if KELAS.get(k, {}).get("info"):
                continue
            if silap:
                cacat.append(k)
            elif not s:
                belum.append(t)
        cacat += [x["kelas"] for x in silap if x.get("kelas")]
        tolak = []
        for kep, sebab, sk, asal in user.get(r["imej"], []):
            if kep != "tolak":
                continue
            ks = kelas_sk(sebab, semua=True) if sebab else ["ditolak"]
            for k in ks:
                pemilik = KELAS.get(k, {}).get("sk") or sk
                if pemilik == r["sk"] or (k in ("lain", "ditolak") and sk == r["sk"]):
                    tolak.append(dict(kelas=k, sebab=sebab or asal))
        cacat += [t["kelas"] for t in tolak]
        out.append(dict(r, cacat=sorted(set(cacat)), input_rosak=sorted(set(input_rosak)), belum=belum, tolak=tolak,
                        ok=not cacat))
    return out


def stat(rows):
    return dict(imej=len({r["imej"] for r in rows}), lulus=sum(r["ok"] for r in rows),
                cacat=sum(bool(r["cacat"]) for r in rows), input_rosak=sum(bool(r["input_rosak"]) for r in rows),
                belum=sum(bool(r["belum"]) for r in rows), tolak=sum(bool(r["tolak"]) for r in rows))


def banding(a, b, kelas=None):
    """Versi baharu a lawan versi lama b pada imej yang sama: (lulus a, lulus b, n, kelas cacat baharu, kelas sasaran a, b)."""
    kb = {r["imej"]: r for r in b}
    pa = [r for r in a if r["imej"] in kb]
    pb = [kb[r["imej"]] for r in pa]
    baru = sorted({k for r in pa for k in r["cacat"]} - {k for r in pb for k in r["cacat"]})
    sas = (lambda rs: sum(kelas in r["cacat"] for r in rs)) if kelas else (lambda rs: 0)   # cacat disahkan sahaja
    return sum(r["ok"] for r in pa), sum(r["ok"] for r in pb), len(pa), baru, sas(pa), sas(pb)


def liputan_kad(daf):
    """Ciri kad (kad yang pernah dipakai dalam jana) yang perlu SK: pulang senarai tindakan ikut SK, dan calon SK baharu."""
    import kad
    import belajar
    pakai = sorted({r.get("kad") for r in belajar.muat_log().values() if r.get("kad") in kad.KAD})
    tind, calon = defaultdict(list), []
    baca = lambda sid, medan: bool(re.search(r"""\[\s*["']%s["']\s*\]|get\(\s*["']%s["']""" % (medan, medan), daf.get(sid, {}).get("src", "")))
    tekstur = [k for k in pakai if kad.KAD[k].get("tekstur", "tiada") != "tiada"]
    if tekstur and "SK06" in daf and not baca("SK06", "tekstur"):
        tind["SK06"].append(dict(jenis="parameter", medan="tekstur", teks=f"SK06 belum membaca tekstur kad (tetap S1-S6); kad dipakai dengan tekstur: "
                                 + ", ".join(f"{k} ({kad.KAD[k]['tekstur']})" for k in tekstur)
                                 + ". Tambah parameter tekstur daripada kad, uji pada imej sedia ada"))
    if "SK06" in daf and not (baca("SK06", "ruang_tepi") or baca("SK06", "tepi_pct")):
        tind["SK06"].append(dict(jenis="parameter", medan="ruang_tepi", teks="SK06 belum membaca ruang tepi kad (tetap 76% x 78%). Tambah parameter "
                                 "ruang tepi daripada kad (rujukan.tepi_pct atau ruang_tepi), uji pada imej sedia ada"))
    if tekstur and "SK06" in daf and baca("SK06", "tekstur"):   # SK06 membaca kad: bahagian tekstur kad tanpa jenis
        try:
            sys.path.insert(0, SKRIP)
            import SK06_finish
            tak = [(k, b) for k in tekstur for b in SK06_finish.tekstur_kad(kad.KAD[k]["tekstur"])["tidak_dibuat"]]
        except Exception as e:  # noqa: BLE001
            tak = [("?", f"tidak dapat semak ({e})")]
        if tak:
            tind["SK06"].append(dict(jenis="parameter", medan="tekstur_jenis", teks="Tekstur kad belum ada jenisnya dalam SK06: "
                                     + "; ".join(f"{k} '{b}'" for k, b in tak)
                                     + ". Tambah jenis tekstur prosedur (ukur pada gambar upload kad), uji pada imej sedia ada"))
    for k in pakai:
        K, BL = kad.KAD[k], kad.BLOK.get(k, {})
        ruj, ref = BL.get("rujukan") or {}, K.get("ref", "?")
        if BL.get("condong") and "condong_darjah" not in ruj:
            tind["SK01"].append(dict(jenis="ukur", teks=f"Kad {k} condong tetapi tiada rujukan sudut: ukur SK05 pada {ref}, tulis kad.BLOK['{k}']['rujukan']"))
        if "tepi_pct" not in ruj:
            tind["SK02"].append(dict(jenis="ukur", teks=f"Kad {k} tiada rujukan ruang tepi: ukur SK05 pada {ref}"))
        if K.get("dakwat", 1) > 1 and not K.get("peta_warna"):
            tind["SK07"].append(dict(jenis="parameter", teks=f"Kad {k} ada {K['dakwat']} dakwat tetapi tiada peta_warna: tulis peta peranan -> dakwat ikut {ref}"))
        ada_bayang = any("bayang" in d[0] for d in K.get("warna", {}).get("dakwat", [])) or "bayang" in ruj
        if ada_bayang and "bayang" not in ruj:
            tind["SK08"].append(dict(jenis="ukur", teks=f"Kad {k} ada bayang tetapi tiada rujukan bayang: ukur SK08 --ukur pada {ref}"))
        elif ada_bayang and ruj["bayang"].get("jenis") not in JENIS_BAYANG:
            calon.append(dict(kelas="bayang", sebab=f"kad {k}: bayang jenis '{ruj['bayang'].get('jenis')}' ({ref})",
                              imej=[], sumber="kad"))
    return pakai, tind, calon


def ulasan(s, rows, ubahan, tind_kad):
    """TINDAKAN bagi satu SK: (1) ubahan terbuka, (2) kod berubah tanpa uji, (3) semak, (4) baiki, (5) kad."""
    versi_log = sorted({r["versi"] for r in rows})
    semasa = s["versi"]
    sem = [r for r in rows if r["versi"] == semasa and r["jalan"]]
    if not sem and rows:  # kod sudah naik versi tetapi belum dijalankan: statistik ikut versi terakhir dalam log
        akhir = max(versi_log, key=lambda v: max(i for i, r in enumerate(rows) if r["versi"] == v))
        sem = [r for r in rows if r["versi"] == akhir and r["jalan"]]
    dicuba = [u for u in ubahan if u["sk"] == s["sk"]]
    tind = []
    buka = [u for u in dicuba if u.get("keputusan") == "cuba"]
    for u in buka:
        a = [r for r in rows if r["versi"] == u["ke"]]
        b = [r for r in rows if r["versi"] == u["dari"]]
        la, lb, n, baru, ta, tb = banding(a, b, u.get("kelas"))
        if not n:
            senarai = ", ".join(u.get("imej") or sorted({r["imej"] for r in b})[:6])
            tind.append(dict(jenis="uji_semula", teks=f"Ubahan '{u['ubahan']}' ({u['dari']} -> {u['ke']}) belum diuji: jalan semula "
                                                       f"{s['sk']} versi baharu pada imej yang sama ({senarai}); tiada jana"))
        elif u.get("jenis") == "parameter" and la >= lb and not baru and not any(r["belum"] for r in a) \
                and not any(t.get("medan") == u.get("medan") for t in tind_kad.get(s["sk"], [])):
            tind.append(dict(jenis="menang", ubahan=u["ubahan"], teks=f"MENANG '{u['ubahan']}' {u['dari']} -> {u['ke']} (parameter "
                             f"'{u.get('medan')}'): lulus {lb}/{n} -> {la}/{n}, jurang kad '{u.get('medan')}' tertutup, tiada cacat baharu, "
                             f"semua imej disemak. Tanda menang dalam sk_ubahan.json, kemas kini jadual Daftar skrip + Catatan pembaikan SK"))
        elif u.get("jenis") == "parameter" and la >= lb and not baru and any(r["belum"] for r in a):
            tind.append(dict(jenis="semak", teks=f"Ubahan parameter '{u['ubahan']}': semak imej versi baharu dahulu (amaran belum disemak)"))
        elif (la > lb or (la == lb and ta < tb)) and not baru:
            tind.append(dict(jenis="menang", ubahan=u["ubahan"], teks=f"MENANG '{u['ubahan']}' {u['dari']} -> {u['ke']}: lulus {lb}/{n} -> {la}/{n}"
                             + (f", kelas '{u.get('kelas')}' {tb} -> {ta}" if u.get("kelas") else "")
                             + ". Tanda menang dalam sk_ubahan.json, kemas kini jadual Daftar skrip + Catatan pembaikan SK"))
        else:
            why = f"kelas cacat baharu: {', '.join(baru)}" if baru else "tidak lebih baik"
            tind.append(dict(jenis="kalah", ubahan=u["ubahan"], teks=f"KALAH '{u['ubahan']}' {u['dari']} -> {u['ke']}: lulus {lb}/{n} -> {la}/{n} ({why}). "
                             f"Pulangkan kod ke {u['dari']} (git), tanda kalah dalam sk_ubahan.json, catat dalam Catatan pembaikan SK"))
    if not buka and rows and semasa not in versi_log:
        tind.append(dict(jenis="uji_semula", teks=f"Kod {s['sk']} kini {semasa} tetapi log hanya {', '.join(versi_log)}: catat ubahan dalam "
                                                   f"sk_ubahan.json (cuba) dan jalan semula pada imej yang sama"))
    belum = [r for r in sem if r["belum"]]
    if belum:
        tind.append(dict(jenis="semak", teks=f"Semak {len(belum)} imej (GAGAL / amaran belum disemak): "
                         + ", ".join(r["imej"] for r in belum[:8]) + ("…" if len(belum) > 8 else "")
                         + ". Lihat imej; tulis sk_semakan.jsonl (silap = kelemahan SK, betul = imej input rosak / amaran tidak merosakkan)"))
    berulang = []
    for k in sorted({k for r in sem for k in r["cacat"]}):
        im = sorted({r["imej"] for r in sem if k in r["cacat"]})
        kalah = [u for u in dicuba if u.get("kelas") == k and u.get("keputusan") == "kalah"]
        berulang.append(dict(kelas=k, nama=KELAS.get(k, {}).get("nama", "Cacat lain (tiada kelas)" if k == "lain" else "Ditolak pengguna tanpa sebab"),
                             imej=im, n=len(im), kalah=[u["ubahan"] for u in kalah]))
    berulang.sort(key=lambda x: -x["n"])
    for x in berulang:
        if x["kelas"] == "ditolak":
            tind.append(dict(jenis="tanya", teks=f"{x['n']} imej ditolak tanpa sebab ({', '.join(x['imej'][:4])}): tanya pengguna sebabnya"))
    calon = [x for x in berulang if x["kelas"] == "lain" and x["n"] >= 2]
    ulang = [x for x in berulang if x["kelas"] not in ("lain", "ditolak") and x["n"] >= 2]
    if ulang and not buka:
        x = ulang[0]
        if len(x["kalah"]) >= HABIS_N:
            tind.append(dict(jenis="habis", teks=f"Cacat '{x['nama']}' ({x['n']} imej): {len(x['kalah'])} ubahan kalah ({', '.join(x['kalah'])}). "
                                                  f"Lapor pengguna; imej itu jana semula"))
        else:
            elak = f"; jangan ulang: {', '.join(x['kalah'])}" if x["kalah"] else ""
            tind.append(dict(jenis="baiki", kelas=x["kelas"], teks=f"BAIKI {s['sk']} bagi cacat '{x['nama']}' ({x['n']} imej: {', '.join(x['imej'][:4])}). "
                             f"Satu ubahan kod, versi naik, catat sk_ubahan.json (cuba), jalan semula pada imej yang sama{elak}"))
    ada_ubah = any(t["jenis"] in ("menang", "kalah", "uji_semula", "baiki") for t in tind)
    for t in tind_kad.get(s["sk"], []):
        if t["jenis"] == "ukur" or not ada_ubah:  # ukur = data kad (bukan ubah kod); parameter tunggu ubahan lain selesai
            tind.append(t)
            ada_ubah = ada_ubah or t["jenis"] == "parameter"
    ikut = {v: stat([r for r in rows if r["versi"] == v and r["jalan"]]) for v in versi_log}
    return dict(sk=s["sk"], nama=s["nama"], fail=s["fail"], langkah=s["langkah"], versi=semasa, ikut_versi=ikut,
                semasa=stat(sem), berulang=berulang, calon=calon, ubahan_dicuba=len(dicuba),
                tindakan=tind or [dict(jenis="tiada", teks="Tiada tindakan: tiada cacat berulang")])


def main():
    os.makedirs(B, exist_ok=True)
    daf = daftar_sk()
    user, suka = isyarat_pengguna()
    rows = nilai(gabung_sejarah(baris_log()), semakan(), user)
    ubahan = baca_json(os.path.join(B, "sk_ubahan.json"), [])
    pakai, tind_kad, calon_kad = liputan_kad(daf)
    per = defaultdict(list)
    for r in rows:
        per[r["sk"]].append(r)
    hasil = {sid: ulasan(s, per.get(sid, []), ubahan, tind_kad) for sid, s in daf.items()}
    # Cacat tanpa SK pemilik: tolak pengguna dengan sebab tanpa kelas, dan ciri kad yang tiada SK -> calon SK baharu.
    seterus = max(int(s[2:]) for s in daf) + 1
    calon = list(calon_kad)
    lain = defaultdict(set)
    for key, isy in user.items():
        for kep, sebab, sk, asal in isy:
            if kep == "tolak" and sebab and not sk:
                for bah in re.split(";", sebab):
                    if bah.strip() and not kelas_sk(bah) and asal == "sk_pengguna.jsonl":
                        lain[bah.strip().lower()].add(key)
    for sebab, im in lain.items():
        calon.append(dict(kelas="lain", sebab=sebab, imej=sorted(im), sumber="sk_pengguna.jsonl"))
    for h in hasil.values():
        calon += [dict(kelas="lain", sebab=f"{h['sk']}: cacat tanpa kelas", imej=x["imej"], sumber="semakan") for x in h["calon"]]
    baharu = []
    for c in calon:
        if c["sumber"] == "kad" or len(c["imej"]) >= 2:
            sid = f"SK{seterus:02d}"
            seterus += 1
            baharu.append(dict(c, sk=sid, teks=f"SK BAHARU {sid}: {c['sebab']}" + (f" ({len(c['imej'])} imej)" if c["imej"] else "")
                               + ". Ikut kaedah skrip baharu 1-8 (semak daftar dahulu: parameter pada SK sedia ada jika boleh); "
                                 "tambah kelas ke KELAS_SK; uji pada imej sedia ada; daftar; lapor"))
        else:
            baharu.append(dict(c, sk="-", teks=f"Pantau: '{c['sebab']}' pada 1 imej ({', '.join(c['imej'])}); SK baharu jika berulang"))
    hari = datetime.date.today().isoformat()
    json.dump(dict(versi=VERSI, tarikh=hari, baris=len(rows), imej=len({r["imej"] for r in rows}), kad_dipakai=pakai,
                   suka=len(suka), sk={k: v for k, v in hasil.items()}, sk_baharu=baharu),
              open(os.path.join(B, "sk_ringkasan.json"), "w"), ensure_ascii=False, indent=1)
    eks = []
    for sid, h in hasil.items():
        s = h["semasa"]
        eks.append(dict(sk=sid, nama=h["nama"], langkah=h["langkah"], versi=h["versi"], imej=s["imej"], lulus=s["lulus"],
                        cacat_sk=s["cacat"], input_rosak=s["input_rosak"], belum_semak=s["belum"], tolak=s["tolak"],
                        suka=len({r["imej"] for r in per.get(sid, [])} & suka),
                        cacat_berulang="; ".join(f"{x['nama']} ({x['n']} imej)" for x in h["berulang"] if x["n"] >= 2) or "-",
                        tindakan=" | ".join(t["teks"] for t in h["tindakan"]), ubahan_dicuba=h["ubahan_dicuba"], tarikh=hari))
    for c in baharu:
        eks.append(dict(sk=c["sk"] + (" (calon)" if c["sk"] != "-" else " (pantau)"), nama=c["sebab"], langkah="-", versi="-",
                        imej=len(c["imej"]), lulus=0, cacat_sk=len(c["imej"]), input_rosak=0, belum_semak=0, tolak=0, suka=0,
                        cacat_berulang=c["sebab"], tindakan=c["teks"], ubahan_dicuba=0, tarikh=hari))
    os.makedirs(os.path.dirname(EXPORT), exist_ok=True)
    json.dump(eks, open(EXPORT, "w"), ensure_ascii=False, indent=1)
    print(f"belajar_sk.py {VERSI}: {len(rows)} baris (imej x SK x versi), {len({r['imej'] for r in rows})} imej, ♥ {len(suka)}, "
          f"kad dipakai {', '.join(pakai)}")
    for sid, h in hasil.items():
        s = h["semasa"]
        print(f"\n{sid} {h['nama']} ({h['versi']}, langkah {h['langkah']}): {s['lulus']}/{s['imej']} tanpa cacat SK, "
              f"input rosak {s['input_rosak']}, belum semak {s['belum']}, tolak {s['tolak']}; ikut versi "
              + (", ".join(f"{v} {x['lulus']}/{x['imej']}" for v, x in h["ikut_versi"].items()) or "tiada log"))
        for x in h["berulang"]:
            print(f"  cacat: {x['nama']}: {x['n']} imej ({', '.join(x['imej'][:4])})")
        for t in h["tindakan"]:
            print(f"  TINDAKAN [{t['jenis']}]: {t['teks']}")
    for c in baharu:
        print(f"\nTINDAKAN [sk_baharu]: {c['teks']}")


if __name__ == "__main__":
    main()
