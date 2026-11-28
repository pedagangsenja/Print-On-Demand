"""Belajar selepas setiap jana: aturan prompt setiap model dikemas kini daripada hasil sebenar (standard 3.15).

Keputusan pengguna 27 Nov 2026: jalan selepas SETIAP batch imej AI yang sudah di-QC; ♥ dan tolak pengguna dikira;
ubahan yang menang ditulis terus ke aturan (rev naik) dan dilaporkan dalam jadual jawapan.

Baca:
  qc/*.json                         rekod QC (format dict batch>model>imej, format senarai, *_snc.json, *_blobs.json)
  raw/<batch>/<model>/log.jsonl     log jana: rev aturan, versi pembina, ubahan uji (PEMBINA_UJI), prompt
  belajar/ubahan.json               semua ubahan aturan yang pernah dicuba (menang / kalah / tidak berkenaan)
  belajar/pengguna.jsonl            keputusan pengguna langkah 7: {"imej": "batch/model/ID_sSEED", "keputusan": "lulus"|"tolak", "sebab": ...}
  belajar/stor/data/...             salinan stor dashboard (ArtifactData list, out_dir=belajar/stor):
                                    data/likes/items (♥), data/gaya/items + data/warna/items (Daftar S/C: kod dipadam = tolak)
Tulis:
  belajar/log.jsonl                 satu baris = satu imej
  belajar/ringkasan.json            setiap model: prestasi ikut rev, cacat berulang, TINDAKAN
  ../../data/export/ai_tests/aturan_belajar.json   dataset dashboard `aturan_belajar` (satu baris = satu model)
Jalan: python3 belajar.py   (tiada jana; tiada ubah aturan: TINDAKAN dilaksana oleh Claude ikut standard 3.15)
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
import akar  # noqa: E402
import pembina  # noqa: E402
import belajar_sk  # noqa: E402

VERSI = "b1.5 (28 Nov 2026)"  # b1.5 = b1.4 (sleepy-edison + nifty-lovelace + lucid-galileo) + b1.2 focused-faraday (kelas bentuk "bentuk huruf lebar") (pemecah seri: lulus, ♥, bersih, cacat sasaran)
B = os.path.join(HERE, "belajar")
STOR = os.path.join(B, "stor", "data")
EXPORT = os.path.normpath(os.path.join(HERE, "..", "..", "data", "export", "ai_tests", "aturan_belajar.json"))
PERANTI = {"cpu": "-cpu", "hf": "-gpu-hf"}  # awalan kunci *_blobs.json -> akhiran folder batch

# Kelas cacat = baris jadual kitaran QC (langkah 5). Pilihan ubahan ikut turutan; id pilihan dipakai sebagai
# nama ubahan calon dalam pembina.py: PEMBINA_UJI=<model>_<id>.
KELAS = {
    "berulang": ("Perkataan berulang atau tertinggal", r"berulang|hilang|tertinggal|WHAT WHAT",
                 [("cara_baris", "Cara menulis baris teks ikut aturan model (klein: satu ayat prosa setiap baris; ERNIE: PE hidup)")]),
    "rawak": ("Teks rawak, label atau tanda baca tambahan",
              r"label tambahan|tandatangan|tanda rawak|tanda petikan|tambahan selepas|titik tambahan|koma tambahan|bintik|'on' tambahan|dan tambahan",
              [("had_positif", "Buang perkataan berisiko daripada ayat had (label, logo, signature, watermark); tulis had sebagai ayat positif")]),
    "luar_label": ("Perkataan tidak di dalam label", r"tiada kotak",
                   [("bekas_dahulu", "Tulis bekas dahulu, perkataan kemudian (\"a small white label, and inside that label the word ...\")")]),
    "hiasan_lebih": ("Hiasan yang tidak diminta", r"bintang|garis lengkung|garis tambahan",
                     [("hiasan_tepat", "Nyatakan hiasan yang dibenarkan dengan tepat, tambah \"clean empty background\"")]),
    "hiasan_tempat": ("Hiasan di tempat salah", r"percikan dilukis di dalam|percikan hanya|tiada percikan|anak panah|tempat salah|bukan di sudut|bingkai hanya|reben kecil",
                      [("hiasan_kedudukan", "Nyatakan kedudukan hiasan (kiri dan kanan, di luar label)")]),
    "baris": ("Bilangan baris salah (baris dipisah)", r"\b\d baris|dipisah",
              [("dua_kata_sebaris", "Nyatakan dua perkataan sebaris (\"as two words side by side on one line\")"),
               ("frasa_hierarki", "Frasa hierarki atau nisbah baris dalam aturan model")]),
    "ejaan": ("Perkataan salah eja, rosak, atau huruf besar / kecil salah",
              r"jadi|rosak|meragukan|huruf besar|huruf kecil|Morrrnings|omornings|Betters",
              [("huruf_besar", "Huruf besar untuk baris itu jika kad membenarkan"),
               ("tukar_peranan", "Tukar peranan perkataan itu")]),
    "bentuk": ("Bentuk huruf atau saiz label lain daripada kad", r"nipis|label (lebih )?besar|label kecil|huruf lebar|bukan sempit|tidak gergasi|tidak bertaut|bentuk huruf|lebar baris",
               [("frasa_bentuk", "Frasa bentuk huruf dalam aturan model")]),
    "ditolak": ("Ditolak pengguna tanpa sebab", r"^dipadam|^ditolak", []),
}
POLA = {k: re.compile(v[1], re.I) for k, v in KELAS.items()}
# Bukan kerja prompt: cacat milik skrip SK (5b / langkah 6), dan cacat akibat pepijat kod yang sudah dibaiki (27 Nov 2026); senarai kelas di belajar_sk.KELAS_SK (b1.1: diselaraskan)
BUKAN_PROMPT = re.compile(r"condong|ruang tepi|atas tengah|kelabu|lorekan|latar tidak hitam|pepijat kod|" + belajar_sk.POLA_SK.pattern, re.I)
HABIS = "Pilihan ubahan habis: tukar ke model seterusnya ikut jadual model × gaya, kemudian pendekkan ayat, kemudian lapor kepada pengguna"


def kelas(sebab):
    """Kelas cacat (berkaitan prompt) daripada teks sebab QC. Cacat 'bukan prompt' (skrip 5b) diabaikan."""
    out = set()
    for bah in re.split(r";", sebab or ""):
        bah = bah.strip()
        if not bah:
            continue
        hit = {k for k, p in POLA.items() if p.search(bah)}
        if hit:
            out |= hit
        elif not BUKAN_PROMPT.search(bah):
            out.add("lain")
    return sorted(out)


def baca_json(p, lalai):
    return json.load(open(p)) if os.path.exists(p) else lalai


def muat_log():
    L = {}
    for t, d in akar.akar():  # cawangan ini + cawangan sesi lain (gabung_cawangan.py, 28 Nov 2026)
      for f in glob.glob(os.path.join(d, "raw", "*", "*", "log.jsonl")):
        batch = akar.tanda(t, f.split(os.sep)[-3])
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                L[(batch, r["model"], r["id"], int(r["seed"]))] = r
    return L


def muat_qc(L):
    rows, blob, snc = [], {}, {}
    for t, f in [(t, f) for t, a in akar.akar() for f in sorted(glob.glob(os.path.join(a, "qc", "*.json")))]:
        d, stem = json.load(open(f)), os.path.basename(f)[:-5]
        if stem.endswith("_blobs"):
            base = stem.split("_")[0]
            for k, v in d.items():
                m = re.match(r"(cpu|hf)_(.+)_(K\w+?)_s(\d+)$", k)
                if m:
                    blob[(akar.tanda(t, base + PERANTI[m[1]]), m[2], m[3], int(m[4]))] = str(v).rsplit("/", 1)[-1]
            continue
        if stem.endswith("_snc"):
            batch = akar.tanda(t, stem[:-4].replace("_", "-"))
            for kod, r in d.get("rekod", {}).items():
                if "/" not in r.get("imej", "/"[:0]):  # kod warna C (skrip, bukan prompt) atau imej tanpa model/
                    continue
                m = re.match(r"([\w.-]+?)[/_](K\w+?)_s(\d+)", r["imej"])  # 'model/ID_sN' (atau format sesi lain)
                if m:
                    snc[(batch, m[1], m[2], int(m[3]))] = (kod, r.get("blob", ""))
            continue
        if isinstance(d, list):
            batch = akar.tanda(t, stem.replace("_", "-"))
            for r in d:
                if not isinstance(r, dict) or "_s" not in str(r.get("id", "")):  # bukan rekod QC imej (cth. laporan decode)
                    continue
                i, s = r["id"].rsplit("_s", 1)
                rows.append(dict(batch=batch, model=r["model"], id=i, seed=int(s), ok=bool(r.get("ejaan")),
                                 sebab=r.get("sebab", ""), blob=""))
            continue
        for batch, v in d.items():
            if not isinstance(v, dict):
                continue
            batch = akar.tanda(t, batch)
            for model, x in v.items():
                if not isinstance(x, dict):
                    continue
                for k, y in x.items():
                    if not isinstance(y, list):
                        continue
                    i, s = k.rsplit("_s", 1) if "_s" in k else (None, k)
                    if i is None:  # kunci seed sahaja (cth. k3h): id daripada log
                        i = next((key[2] for key in L if key[:2] == (batch, model) and key[3] == int(s)), "?")
                    rows.append(dict(batch=batch, model=model, id=i, seed=int(s), ok=bool(y[0]),
                                     sebab=y[1] if len(y) > 1 else "", blob=(y[2] if len(y) > 2 else "") or ""))
    return rows, blob, snc


def stor_ids(*bah):
    p = os.path.join(STOR, *bah)
    return {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(p, "*.json"))} if os.path.isdir(p) else None


UBAHAN = baca_json(os.path.join(B, "ubahan.json"), [])
for _t, _d in akar.akar()[1:]:  # keputusan cawangan sesi lain: hanya menang / kalah / tidak berkenaan; design ditanda
    for _u in baca_json(os.path.join(_d, "belajar", "ubahan.json"), []):
        _u = dict(_u, design=", ".join(akar.tanda(_t, x.strip()) for x in str(_u.get("design", "")).split(",") if x.strip()))
        if _u.get("keputusan") in ("menang", "kalah", "tidak berkenaan") and _u not in UBAHAN:
            UBAHAN.append(_u)
# Kenaikan rev tanpa ubahan teks (ujian kelayakan r0 -> r1): imej rev lama dikira pada rev baharu.
ALIAS = {(u["model"], u["rev_dari"]): u["rev_ke"] for u in UBAHAN
         if u.get("ubahan") == "kelayakan" and u.get("keputusan") == "menang"}


def bina_log():
    L = muat_log()
    rows, blob, snc = muat_qc(L)
    suka = stor_ids("likes", "items") or set()
    ada = {"S": stor_ids("gaya", "items"), "C": stor_ids("warna", "items")}
    pengguna = {}
    for t, d in akar.akar():
        pp = os.path.join(d, "belajar", "pengguna.jsonl")
        if os.path.exists(pp):
            for line in open(pp):
                if line.strip():
                    r = json.loads(line)
                    pengguna[akar.tanda(t, r["imej"])] = dict(r, imej=akar.tanda(t, r["imej"]))
    out = []
    for r in rows:
        key = (r["batch"], r["model"], r["id"], r["seed"])
        g = L.get(key, {})
        kod, b2 = snc.get(key, ("", ""))
        bl = r["blob"] or b2 or blob.get(key, "")
        rev = g.get("rev") or ("khas-v0" if str(g.get("pembina", "")).startswith("khas") else ("am" if g else "?"))
        rev = ALIAS.get((r["model"], rev), rev)
        uji = sorted(u[len(r["model"]) + 1:] if u.startswith(r["model"] + "_") else u for u in (g.get("uji") or []))
        if not uji and re.search(r"-p\d+$", r["batch"]):  # pusingan kitaran QC lama (log tanpa 'uji'): ubahan daripada ubahan.json
            uji = [u["ubahan"] for u in UBAHAN if u["model"] == r["model"]
                   and akar.tanda(r["batch"].split(":")[0] if ":" in r["batch"] else "", r["id"])
                   in [x.strip() for x in u.get("design", "").split(",")]
                   and u.get("keputusan") in ("menang", "kalah")][-1:]
        m = re.match(r"(K\d+)(\w+)", r["id"] or "")
        nama = f"{r['batch']}/{r['model']}/{r['id']}_s{r['seed']}"
        tolak, sebab_tolak = False, ""
        if kod and ada.get(kod[0]) is not None and kod not in ada[kod[0]]:
            tolak, sebab_tolak = True, f"dipadam dari Daftar S/C ({kod})"
        if nama in pengguna:
            u = pengguna[nama]
            tolak = u.get("keputusan") == "tolak"
            sebab_tolak = (u.get("sebab") or "ditolak pengguna") if tolak else ""
        if r["ok"] and re.match(r"G1-G3 lulus", r["sebab"] or ""):  # nota perihal (format sesi lain), bukan cacat
            r = dict(r, sebab="")
        k = kelas(r["sebab"])
        if tolak:
            k = sorted(set(k) | set(kelas(sebab_tolak) or ["ditolak"]))
        tg = r["batch"].split(":")[0] if ":" in r["batch"] else ""
        kad_, ayat_ = g.get("kad") or (m[1] if m else ""), g.get("ayat") or (m[2] if m else "")
        try:   # b1.2: prompt imej ini sama dengan prompt aturan semasa (rev naik yang tidak mengubah kad / ayat ini)
            kini = not tg and bool(g.get("prompt")) and not uji and r["model"] in pembina.DAFTAR and \
                g["prompt"] == pembina.bina(r["model"], kad_, ayat_)[0]
        except Exception:
            kini = False
        out.append(dict(imej=nama, batch=r["batch"], model=r["model"], kad=akar.tanda(tg, kad_), kini=kini,
                        ayat=g.get("ayat") or (m[2] if m else ""), seed=r["seed"], rev=rev, pembina=g.get("pembina"),
                        uji=uji, ok=r["ok"], suka=bool(bl) and bl in suka, tolak=tolak, lulus=r["ok"] and not tolak,
                        kelas=k, sebab="; ".join(x for x in (r["sebab"], sebab_tolak) if x), blob=bl, snc=kod))
    return out


def stat(rows):
    n = len(rows)
    lulus = sum(r["lulus"] for r in rows)
    return dict(imej=n, lulus=lulus, pct=round(100 * lulus / n) if n else None, suka=sum(r["suka"] for r in rows),
                tolak=sum(r["tolak"] for r in rows), design=len({(r["kad"], r["ayat"]) for r in rows}))


def skor(rows):
    # (lulus, ♥, bersih). Bersih = lulus tanpa kelas cacat prompt; pemecah seri supaya ubahan bagi cacat yang tidak
    # menggagalkan imej (cth. bentuk huruf, "imej lulus; ciri gaya kad") boleh menang (pembaikan 28 Nov 2026).
    return (sum(r["lulus"] for r in rows), sum(r["suka"] for r in rows),
            sum(r["lulus"] and not r["kelas"] for r in rows))


def sasaran(nama):
    """Kelas cacat yang disasar oleh ubahan calon (id pilihan dalam KELAS), atau None."""
    return next((k for k, v in KELAS.items() if any(i == nama for i, _ in v[2])), None)


def banding(a, b, kelas_sasaran=None):
    """Imej a lawan b pada (kad, ayat, seed) yang sama. Pulang (skor a, skor b, bilangan pasangan, kelas baharu dalam a).
    b1.2: skor = (lulus, ♥, -imej dengan kelas sasaran); jadi seri lulus dan ♥ dipecah oleh cacat gaya sasaran
    yang berkurang (cth. hiasan di tempat salah pada imej yang sudah lulus)."""
    kb = {(r["kad"], r["ayat"], r["seed"]): r for r in b}
    pa = [r for r in a if (r["kad"], r["ayat"], r["seed"]) in kb]
    pb = [kb[(r["kad"], r["ayat"], r["seed"])] for r in pa]
    baru = sorted({k for r in pa for k in r["kelas"]} - {k for r in pb for k in r["kelas"]})
    c = lambda rr: -sum(kelas_sasaran in r["kelas"] for r in rr) if kelas_sasaran else 0
    return skor(pa) + (c(pa),), skor(pb) + (c(pb),), len(pa), baru


def nisbah(s, n):
    return f"{s[0]}/{n}" + (f" (♥ {s[1]})" if s[1] else "") + f", bersih {s[2]}" + \
        (f" (cacat sasaran {-s[3]})" if len(s) > 3 and s[3] else "")


def ulasan(model, rows, ubahan):
    d = pembina.DAFTAR.get(model)
    semasa = d["rev"] if d else "am"
    tindakan = []
    dicuba = [u for u in ubahan if u["model"] == model]
    cuba_id = {u["ubahan"] for u in dicuba}
    # 1. Ubahan calon (PEMBINA_UJI) lawan aturan semasa pada kad, ayat, seed yang sama.
    kump = defaultdict(list)
    for r in rows:
        if r["uji"]:  # dikumpul ikut cawangan juga: ujian sesi lain dinilai berasingan (gabung_cawangan.py)
            kump[(r["batch"].split(":")[0] if ":" in r["batch"] else "", "+".join(r["uji"]))].append(r)
    for (tg, nama), a in sorted(kump.items()):
        asas = [r for r in rows if not r["uji"] and (r["rev"] == a[0]["rev"] or r.get("kini"))]   # b1.2: atau prompt sama
        sa, sb, n, baru = banding(a, asas, sasaran(nama))
        design = ", ".join(sorted({r["kad"] + r["ayat"] for r in a}))
        if any(u["ubahan"] == nama and set(design.split(", ")) <= {x.strip() for x in u.get("design", "").split(",")}
               for u in dicuba):
            continue
        if not n:
            tindakan.append(dict(jenis="uji", teks=f"Ubahan '{nama}' ({design}) tiada pembanding: jana aturan semasa pada kad, ayat dan seed yang sama"))
        elif sa > sb and not baru:
            tindakan.append(dict(jenis="menang", ubahan=nama, design=design, sebelum=nisbah(sb, n), selepas=nisbah(sa, n),
                                 teks=f"MENANG '{nama}' ({design}): {nisbah(sb, n)} -> {nisbah(sa, n)}. Tulis balik ke aturan "
                                      f"{d['bahagian'] if d else '?'}, rev naik, buang dari UJI, catat ubahan.json + Catatan pembaikan"))
        else:
            why = f"kelas cacat baharu: {', '.join(baru)}" if baru else "tidak lebih baik"
            tindakan.append(dict(jenis="kalah", ubahan=nama, design=design, sebelum=nisbah(sb, n), selepas=nisbah(sa, n),
                                 teks=f"KALAH '{nama}' ({design}): {nisbah(sb, n)} -> {nisbah(sa, n)} ({why}). Buang dari UJI, "
                                      f"catat ubahan.json + Catatan pembaikan"))
    # 2. Ujian kelayakan aturan r0 (r0 lawan rangka am pada kad, ayat, seed yang sama).
    if semasa == "r0":
        r0 = [r for r in rows if r["rev"] == "r0" and not r["uji"]]
        am = [r for r in rows if r["rev"] == "am" and not r["uji"]]
        sa, sb, n, _ = banding(r0, am)
        if not r0:
            tindakan.append(dict(jenis="kelayakan", teks="Belum diuji: ujian kelayakan (rangka am lawan aturan r0; kad sama; seed 42, 7, 123; perlu izin jana)"))
        elif not n:
            tindakan.append(dict(jenis="kelayakan", teks=f"Aturan r0 sudah dijana ({nisbah(skor(r0), len(r0))}) tetapi tiada pembanding rangka am: "
                                                       f"jana rangka am pada kad, ayat dan seed yang sama (perlu izin jana)"))
        elif sa >= sb:
            tindakan.append(dict(jenis="naik", teks=f"Ujian kelayakan LULUS ({nisbah(sa, n)} lawan rangka am {nisbah(sb, n)}): naikkan r0 -> r1"))
        else:
            tindakan.append(dict(jenis="tidak_layak", teks=f"Ujian kelayakan GAGAL ({nisbah(sa, n)} lawan rangka am {nisbah(sb, n)}): tanda model tidak layak, simpan aturan"))
    # 3. Cacat berulang pada aturan semasa: >= 2 imej, dan sama ada >= 2 design atau >= 2 seed dalam satu design.
    sem = [r for r in rows if r["rev"] == semasa and not r["uji"]]
    berulang = []
    for k in sorted({k for r in sem for k in r["kelas"]}):
        im = [r for r in sem if k in r["kelas"]]
        per = Counter((r["kad"], r["ayat"]) for r in im)
        if k == "ejaan":  # ejaan: berulang hanya jika PERKATAAN yang sama salah pada >= 2 imej
            kata = Counter(w.lower() for r in im for w in set(re.findall(r"'([^']+)' (?:jadi|rosak|meragukan)", r["sebab"])))
            sama = {w for w, n in kata.items() if n >= 2}
            im = [r for r in im if {w.lower() for w in re.findall(r"'([^']+)' (?:jadi|rosak|meragukan)", r["sebab"])} & sama]
            per = Counter((r["kad"], r["ayat"]) for r in im)
        if len(im) >= 2 and (len(per) >= 2 or max(per.values()) >= 2):
            gagal = sum(not r["lulus"] for r in im)
            tak = set()
            if k == "ejaan":  # huruf besar tidak berkenaan jika perkataan yang salah sudah huruf besar
                kata = [w for r in im for w in re.findall(r"'([^']+)' (?:jadi|rosak)", r["sebab"])]
                if kata and all(w.isupper() for w in kata):
                    tak.add("huruf_besar")
            pil = [p for p in KELAS.get(k, ("", "", []))[2] if p[0] not in cuba_id | tak]
            berulang.append(dict(kelas=k, nama=KELAS.get(k, ("Cacat lain (tiada kelas)",))[0], imej=len(im), gagal=gagal,
                                 design=sorted(a + b for a, b in per), cadangan=pil[0][0] if pil else None,
                                 cadangan_teks=pil[0][1] if pil else (HABIS if k in KELAS and KELAS[k][2] else
                                                                     "Tanya pengguna sebabnya; tambah ke kad sebagai ciri QC")))
    berulang.sort(key=lambda x: (-x["gagal"], -x["imej"]))
    if berulang and not d:
        tindakan.append(dict(jenis="tiada_aturan", teks="Model tanpa aturan sendiri (rangka am): tulis aturan ikut 3.12 sebelum dipakai untuk design"))
    elif berulang and not any(t["jenis"] in ("menang", "kalah", "uji") for t in tindakan):
        x = berulang[0]
        nota = " (imej lulus; ciri gaya kad)" if not x["gagal"] else ""
        if x["cadangan"]:
            tindakan.append(dict(jenis="cuba", ubahan=x["cadangan"],
                                 teks=f"Satu ubahan untuk jana seterusnya model ini: PEMBINA_UJI={model}_{x['cadangan']} "
                                      f"({x['cadangan_teks']}) bagi cacat '{x['nama']}'{nota} ({x['imej']} imej, {len(x['design'])} design); "
                                      f"jana bersama aturan semasa, seed sama"))
        else:
            tindakan.append(dict(jenis="habis", teks=f"Cacat '{x['nama']}': {x['cadangan_teks']}"))
    tolak = [r for r in rows if r["tolak"]]
    if tolak:
        tindakan.append(dict(jenis="tolak", teks=f"{len(tolak)} imej ditolak pengguna; sebab yang sama pada 2 design model ini masuk ke aturan (kitaran QC butir 9)"))
    revs = sorted({r["rev"] for r in rows})
    return dict(model=model, nama=d["nama"] if d else model, bahagian=d["bahagian"] if d else "-", rev=semasa,
                status=d["status"] if d else "tiada aturan sendiri (rangka am)", ikut_rev={v: stat([r for r in rows if r["rev"] == v and not r["uji"]]) for v in revs},
                semasa=stat(sem), semua=stat(rows), berulang=berulang, ubahan_dicuba=len(dicuba),
                suka_imej=[r["imej"] for r in rows if r["suka"]],
                tindakan=tindakan or [dict(jenis="tiada", teks="Tiada tindakan: tiada cacat berulang pada aturan semasa")])


def main():
    os.makedirs(B, exist_ok=True)
    log = bina_log()
    ubahan = UBAHAN
    with open(os.path.join(B, "log.jsonl"), "w") as f:
        for r in log:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    per = defaultdict(list)
    for r in log:
        per[r["model"]].append(r)
    model = list(pembina.DAFTAR) + sorted(m for m in per if m not in pembina.DAFTAR)
    hasil = {m: ulasan(m, per.get(m, []), ubahan) for m in model}
    hari = datetime.date.today().isoformat()
    json.dump(dict(versi=VERSI, tarikh=hari, imej=len(log), suka=sum(r["suka"] for r in log),
                   tolak=sum(r["tolak"] for r in log), model=hasil),
              open(os.path.join(B, "ringkasan.json"), "w"), ensure_ascii=False, indent=1)
    eks = []
    for m in pembina.DAFTAR:
        h = hasil[m]
        eks.append(dict(model=m, nama=h["nama"], bahagian=h["bahagian"], rev=h["rev"], status=h["status"],
                        imej=h["semua"]["imej"], imej_semasa=h["semasa"]["imej"], lulus_semasa=h["semasa"]["lulus"],
                        pct_semasa=h["semasa"]["pct"], suka=h["semua"]["suka"], tolak=h["semua"]["tolak"],
                        cacat_berulang="; ".join(f"{x['nama']} ({x['imej']} imej, {len(x['design'])} design)" for x in h["berulang"]) or "-",
                        tindakan=" | ".join(t["teks"] for t in h["tindakan"]), ubahan_dicuba=h["ubahan_dicuba"], tarikh=hari))
    os.makedirs(os.path.dirname(EXPORT), exist_ok=True)
    json.dump(eks, open(EXPORT, "w"), ensure_ascii=False, indent=1)
    print(f"belajar.py {VERSI}: {len(log)} imej, ♥ {sum(r['suka'] for r in log)}, tolak {sum(r['tolak'] for r in log)}")
    for m in model:
        h = hasil[m]
        s = h["semasa"]
        print(f"\n{m} ({h['nama']}) rev {h['rev']}: semasa {s['lulus']}/{s['imej']} lulus, ♥ {s['suka']}, tolak {s['tolak']}; "
              f"ikut rev " + ", ".join(f"{v} {x['lulus']}/{x['imej']}" for v, x in h["ikut_rev"].items()))
        for x in h["berulang"]:
            print(f"  cacat berulang: {x['nama']}: {x['imej']} imej ({x['gagal']} gagal), design {', '.join(x['design'])}")
        for t in h["tindakan"]:
            print(f"  TINDAKAN [{t['jenis']}]: {t['teks']}")
    # QC B (28 Nov 2026): ciri gaya yang gagal berulang lawan gambar upload -> calon ubahan frasa kad. Calon sahaja.
    try:
        sys.path.insert(0, os.path.join(HERE, "skrip"))
        import SK10_ringkas
        SK10_ringkas.cetak(SK10_ringkas.ringkas())
    except Exception as e:  # QC B tidak boleh menghentikan belajar.py
        print(f"\nQC B dilangkau: {e}")


if __name__ == "__main__":
    main()
