"""SK07 Warna C ikut peranan (Standard Lettering v1.2, langkah 6). Versi 1.3, 27 Nov 2026.
v1.3 (Belajar SK, ubahan hp_neutral, parameter): --warna HP pada kad berbilang dakwat / tanpa peta_warna / berwarna
(K9-K11): satu dakwat = dakwat kad yang neutral (tanpa warna) dan paling kontras dengan latar; jika tiada, putih atau
hitam tulen. Semua peranan satu dakwat, jadi peta_warna tidak diperlukan. K12, K13: sama seperti v1.2.
v1.2 (Belajar SK, ubahan hitam_putih, parameter): --warna HP = latar kad + dakwat pertama kad untuk semua peranan.
v1.1 (Belajar SK, ubahan belah_leher): huruf bertaut merentas baris dibelah pada leher paling sempit, bukan garis
lurus; komponen berbilang baris dikumpul ikut julat penuhnya. Bukti: ernie K3K s42 (puncak S 'Stays' ikut kuning),
ernie K3K s123 (baris salah dibelah).

Tugas: imej hitam putih yang lulus QC + 5b -> peta peranan (setiap piksel dakwat = utama / sokongan / penyambung /
hiasan) -> warna ikut peta warna kad, atau ikut warna C dalam Daftar S/C (varian warna tanpa jana semula).
Diperlukan oleh: kad berbilang dakwat K3 (IMG_5775: sans kuning, skrip putih, label kuning, percikan kuning) dan K2
(IMG_5792: kotak kuning, huruf putih). Kad satu dakwat (K1, K4-K8): tukar warna dakwat dan latar sahaja.
Parameter kad: KAD[kad]["warna"] (latar + senarai dakwat), KAD[kad]["peta_warna"] (peranan -> nombor dakwat).

Kaedah:
  1. Topeng dakwat dan sudut condong (SK05). Baris dikira selepas koordinat diluruskan ikut sudut itu.
  2. Komponen bersambung. Komponen besar (tinggi >= 45% tinggi median huruf, luas >= 0.3% dakwat) dikumpul ikut
     julat teras menegak (persentil 20-80 piksel): julat teras bertindih = satu kumpulan. Lebih kumpulan daripada
     baris Spesifikasi Teks: gabung dua kumpulan berjiran yang paling rapat. Kurang (baris bertaut, cth. K3 yang
     memang minta baris bersentuh): kumpulan paling tinggi dibelah pada garis mendatar yang paling sedikit dakwat.
     v1.1: komponen setinggi >= 1.6 x tinggi median huruf (huruf bertaut merentas baris) dikumpul ikut julat penuh
     y0-y1. Setiap komponen yang melintas garis potong: penanda = pikselnya dalam zon dalam setiap jalur (jauh 30%
     tinggi jalur daripada garis potong). Penanda satu jalur sahaja = seluruh komponen ikut jalur itu (ekor huruf);
     dua jalur atau lebih = dibelah pada leher paling sempit (watershed atas jarak ke tepi dakwat). Komponen yang
     menyentuh baris berbekas (label: huruf ialah lubang, jadi tiada leher yang jelas): cara v1 di sekitar label
     (75% di satu jalur ikut jalur itu, selebihnya garis lurus; ekor di luar label dipulangkan), leher hanya antara
     dua baris berjiran tanpa bekas. Jalur kosong: cara v1 sepenuhnya.
  3. Baris ke-i = peranan baris ke-i dalam Spesifikasi Teks (kad.AYAT).
  4. Komponen kecil masuk baris terdekat; di luar julat mendatar perkataan baris itu = hiasan.
  5. Setiap komponen diwarna penuh. Huruf dalam bekas (label / kotak) ialah lubang pada bekas putih, jadi kekal
     warna latar (hitam atas kuning) tanpa langkah tambahan.
Semakan (GAGAL = tiada fail imej, imej itu kekal satu dakwat atau jana semula): bilangan baris = Spesifikasi
Teks; baris berbekas mesti ada komponen segi empat (isi >= 75%); komponen utuh yang masuk teras baris lain yang
berlainan warna > 30% piksel = GAGAL, 10-30% = amaran (standard langkah 6: huruf bertaut merentas baris tidak boleh
diasingkan warnanya). Komponen yang dibelah dicatat sebagai amaran. Kad satu dakwat tidak perlu peta baris.

Guna: python3 SK07_warna.py <imej> <kad> <ayat> <folder keluar> [--warna Cxxx | --warna HP (hitam putih: latar kad, satu dakwat neutral paling kontras; v1.3)]
Hasil (imej asal tidak ditimpa): <nama>_peranan.png (0 latar, 1 utama, 2 sokongan, 3 penyambung, 4 hiasan,
5 bayang), <nama>_alfa.png (kelegapan tepi anti-alias), <nama>_warna.png, <nama>_palet.json (untuk SK06 --palet),
log_6.jsonl. GAGAL = tiada fail imej.
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import kad  # noqa: E402
from SK05_ukur import condong, latar, muat, topeng  # noqa: E402

ID, VERSI = "SK07", "SK07 v1.3 (27 Nov 2026)"
KOD = dict(latar=0, utama=1, sokongan=2, penyambung=3, hiasan=4, bayang=5)
NAMA = {v: k for k, v in KOD.items()}
STOR = Path(__file__).resolve().parent.parent / "belajar" / "stor" / "data" / "warna" / "items"
HAD = dict(besar_tinggi=0.45, besar_luas=0.003, segi_empat=0.75, bertaut=0.10, bertaut_gagal=0.30, multi=1.6, zon=0.30)


def hexa(c):
    return "#%02x%02x%02x" % tuple(int(round(float(v))) for v in c)


def rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def palet(kid, warna=None):
    """Warna setiap peranan. Lalai = warna kad; --warna Cxxx = latar + huruf daripada Daftar S/C (nombor dakwat
    sama dengan kad: dakwat ke-i kad diganti huruf ke-i warna C)."""
    k = kad.KAD[kid]
    if warna == "HP":
        # v1.2 (Belajar SK, ubahan hitam_putih): poster hitam putih sahaja (keputusan pengguna 27 Nov 2026).
        # v1.3 (hp_neutral): satu dakwat = dakwat kad neutral paling kontras dengan latar (K13: hitam, bukan kuning
        # mustard; K10: tiada dakwat neutral -> putih tulen); semua peranan dakwat itu.
        latar = k["warna"]["latar"][1]
        terang = lambda h: sum(int(h[i:i + 2], 16) for i in (1, 3, 5)) / 3
        neutral = lambda h: max(int(h[i:i + 2], 16) for i in (1, 3, 5)) - min(int(h[i:i + 2], 16) for i in (1, 3, 5)) <= 24
        calon = [d[1] for d in k["warna"]["dakwat"] if neutral(d[1]) and abs(terang(d[1]) - terang(latar)) >= 128]
        dakwat = max(calon, key=lambda h: abs(terang(h) - terang(latar))) if calon else (
            "#ffffff" if terang(latar) < 128 else "#000000")
        return dict(sumber=f"kad {kid} HP", latar=latar, peranan={r: dakwat for r in KOD if r != "latar"})
    peta = k.get("peta_warna")
    if peta is None:
        if k["dakwat"] != 1:
            raise SystemExit(f"{kid}: kad {k['dakwat']} dakwat tetapi tiada peta_warna pada kad")
        peta = {r: 0 for r in KOD if r != "latar"}
    if warna:
        f = STOR / f"{warna}.json"
        if not f.exists():
            raise SystemExit(f"{f} tiada: salin stor Daftar S/C dahulu (ArtifactData list data/warna/items, "
                             "out_dir=designs/lettering-v1/belajar/stor)")
        c = json.loads(f.read_text())
        latar, dakwat = c["latar"], c["huruf"]
    else:
        latar, dakwat = k["warna"]["latar"][1], [d[1] for d in k["warna"]["dakwat"]]
    perlu = max(peta.values()) + 1
    if len(dakwat) < perlu:
        raise SystemExit(f"warna {warna or kid} ada {len(dakwat)} dakwat; kad {kid} perlukan {perlu}")
    return dict(sumber=warna or f"kad {kid}", latar=latar, peranan={r: dakwat[i] for r, i in peta.items()})


def alfa(rgb_, semua=None):
    """Kelegapan dakwat 0-255 daripada imej hitam putih (tepi anti-alias SK04 dikekalkan, supaya tepi tidak jadi
    anak tangga bila dibesarkan untuk cetak)."""
    g = cv2.cvtColor(rgb_, cv2.COLOR_RGB2GRAY).astype(np.float32)
    if semua is None:
        semua = topeng(rgb_)[1]
    b, d = float(np.mean(latar(rgb_))), float(np.percentile(g[semua > 0], 90)) if semua.any() else 255.0
    a = np.clip((g - b) / max(1.0, d - b), 0, 1)
    a[a < 0.03] = 0
    return (a * 255).round().astype(np.uint8)


def penuh(peta, a):
    """Piksel tepi (alfa > 0 tetapi di luar topeng) ikut peranan piksel dakwat yang paling hampir."""
    if a is None or not (peta > 0).any():
        return peta
    kosong = (peta == 0).astype(np.uint8)
    _, lab = cv2.distanceTransformWithLabels(kosong, cv2.DIST_L2, 3, labelType=cv2.DIST_LABEL_PIXEL)
    jadual = np.zeros(lab.max() + 1, np.uint8)
    jadual[lab[peta > 0]] = peta[peta > 0]
    out = peta.copy()
    isi = (peta == 0) & (a > 0)
    out[isi] = jadual[lab[isi]]
    return out


def warnakan(peta, pal, a=None):
    bg = np.array(rgb(pal["latar"]), np.float32)
    out = np.empty(peta.shape + (3,), np.float32)
    out[:] = bg
    p = penuh(peta, a)
    for r, h in pal["peranan"].items():
        out[p == KOD[r]] = rgb(h)
    if a is not None:
        k = a.astype(np.float32)[..., None] / 255
        out = bg + (out - bg) * k
    return out.round().astype(np.uint8)


def _komponen(semua, sudut):
    h, w = semua.shape
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -sudut, 1)
    nk, lab = cv2.connectedComponents(semua, connectivity=8)
    ys, xs = np.nonzero(lab)
    ids = lab[ys, xs]
    o = np.argsort(ids, kind="stable")
    ids, ys, xs = ids[o], ys[o], xs[o]
    yr, xr = M[1, 0] * xs + M[1, 1] * ys + M[1, 2], M[0, 0] * xs + M[0, 1] * ys + M[0, 2]
    pot = np.searchsorted(ids, np.arange(2, nk))
    kom = []
    for i, (y, x, py, px) in enumerate(zip(np.split(yr, pot), np.split(xr, pot), np.split(ys, pot),
                                           np.split(xs, pot)), 1):
        kom.append(dict(id=i, luas=len(y), y=y, x=x, py=py, px=px, t20=np.percentile(y, 20),
                        t80=np.percentile(y, 80), y0=y.min(), y1=y.max(), x0=x.min(), x1=x.max(), yc=y.mean()))
    return lab, kom


def _potong(y, c):
    """c-1 garis potong mendatar (selepas diluruskan) pada baris piksel yang paling sedikit dakwat, setiap jalur
    sekurang-kurangnya 35% tinggi purata jalur. Pulang senarai kedudukan potong."""
    y0 = int(np.floor(y.min()))
    prof = np.bincount((y - y0).astype(int)).astype(np.float32)
    prof = cv2.GaussianBlur(prof.reshape(-1, 1), (1, 0), 2).ravel() if len(prof) > 5 else prof
    L = len(prof)
    hmin = max(3, int(L / c * 0.35))
    INF = np.float32(1e18)
    f = [np.where(np.arange(L) >= hmin, prof, INF)]
    asal = []
    for _ in range(c - 2):
        pm = np.minimum.accumulate(f[-1])
        arg = np.array([int(np.argmin(f[-1][:i + 1])) for i in range(L)])
        g = np.full(L, INF)
        g[hmin:] = prof[hmin:] + pm[:-hmin]
        asal.append(arg)
        f.append(g)
    akhir = f[-1].copy()
    akhir[L - hmin:] = INF
    p = int(np.argmin(akhir))
    cuts = [p]
    for arg in reversed(asal):
        p = int(arg[p - hmin])
        cuts.append(p)
    return sorted(y0 + q + 0.5 for q in cuts)


def _belah_leher(k, had_jalur, bentuk):
    """v1.1: indeks jalur bagi setiap piksel komponen k. had_jalur = [y atas, potong..., y bawah] (koordinat lurus).
    Penanda = piksel dalam zon dalam jalur (HAD['zon'] x tinggi jalur dari garis potong; jalur pertama / akhir terbuka
    ke atas / bawah). Satu jalur bertanda: semua piksel ke jalur itu. Dua atau lebih: watershed atas -jarak ke tepi
    dakwat, jadi sempadan jatuh pada leher paling sempit (titik sentuh), bukan garis lurus. Tiada penanda: None."""
    from skimage.segmentation import watershed
    c = len(had_jalur) - 1
    pen = np.zeros(k["luas"], np.int32)
    for j in range(c):
        m = HAD["zon"] * (had_jalur[j + 1] - had_jalur[j])
        lo = -np.inf if j == 0 else had_jalur[j] + m
        hi = np.inf if j == c - 1 else had_jalur[j + 1] - m
        pen[(k["y"] > lo) & (k["y"] < hi)] = j + 1
    ada = np.unique(pen[pen > 0])
    if not len(ada):
        return None
    if len(ada) == 1:
        return np.full(k["luas"], ada[0] - 1)
    oy, ox = k["py"].min(), k["px"].min()
    h, w = k["py"].max() - oy + 3, k["px"].max() - ox + 3
    topi = np.zeros((h, w), np.uint8)
    topi[k["py"] - oy + 1, k["px"] - ox + 1] = 1
    dt = cv2.distanceTransform(topi, cv2.DIST_L2, 3)
    mk = np.zeros((h, w), np.int32)
    mk[k["py"] - oy + 1, k["px"] - ox + 1] = pen
    lab = watershed(-dt, mk, mask=topi.astype(bool), connectivity=2)   # 8 jiran, sama seperti komponen
    jal = lab[k["py"] - oy + 1, k["px"] - ox + 1] - 1
    sisa = jal < 0
    if sisa.any():
        jal[sisa] = np.clip(np.searchsorted(had_jalur[1:-1], k["y"][sisa]), 0, c - 1)
    return jal


def _baris(bahagian):
    y = np.concatenate([k["y"][m] for k, m in bahagian])
    x = np.concatenate([k["x"][m] for k, m in bahagian])
    return dict(bahagian=bahagian, t20=np.percentile(y, 20), t80=np.percentile(y, 80), y0=y.min(), y1=y.max(),
                x0=x.min(), x1=x.max())


def _bekas_sahaja(garis, huruf, bentuk):
    """Baris berbekas (label / kotak): bahagian komponen yang DIBELAH dan terletak di luar segi empat bekas (ekor huruf
    baris jiran yang bersentuh label) dipulangkan ke jalur lain komponen itu. Segi empat = segi empat condong terkecil
    yang meliputi hasil bukaan morfologi (kernel 40% tinggi teras baris: ekor nipis hilang, kotak kekal), dikembang
    2 piksel. Pulang bilangan piksel yang dipindah."""
    pindah = 0
    for g in garis:
        if not (isinstance(huruf.get(g["peranan"]), dict) and "bekas" in huruf[g["peranan"]]):
            continue
        t = np.zeros(bentuk, np.uint8)
        for k, m in g["bahagian"]:
            t[k["py"][m], k["px"][m]] = 1
        n = max(3, int(0.4 * (g["t80"] - g["t20"])))
        cs, _ = cv2.findContours(t, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(t, cs, -1, 1, cv2.FILLED)   # isi lubang huruf dalam label dahulu
        buka = cv2.morphologyEx(t, cv2.MORPH_OPEN, np.ones((n, n), np.uint8))
        cs, _ = cv2.findContours(buka, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cs:
            continue
        kotak = np.zeros(bentuk, np.uint8)   # segi empat condong penuh (bucu tidak terpotong oleh kernel tegak)
        cv2.fillPoly(kotak, [np.intp(cv2.boxPoints(cv2.minAreaRect(max(cs, key=cv2.contourArea))))], 1)
        kotak = cv2.dilate(kotak, np.ones((5, 5), np.uint8))
        for j, (k, m) in enumerate(g["bahagian"]):
            if m.all():
                continue
            luar = m & (kotak[k["py"], k["px"]] == 0)
            lain = [(g2, i2) for g2 in garis if g2 is not g for i2, (k2, _) in enumerate(g2["bahagian"]) if k2 is k]
            if not luar.any() or not lain:
                continue
            yl = k["y"][luar].mean()   # ke jalur lain komponen itu yang terasnya paling hampir
            g2, i2 = min(lain, key=lambda gi: abs((gi[0]["t20"] + gi[0]["t80"]) / 2 - yl))
            g2["bahagian"][i2] = (k, g2["bahagian"][i2][1] | luar)
            g["bahagian"][j] = (k, m & ~luar)
            pindah += int(luar.sum())
    return pindah


def baris_peranan(rgb_, kid, aid):
    """Pulang (peta peranan uint8, catatan). peta = None jika gagal."""
    baris = kad.AYAT[aid]["baris"]
    n = len(baris)
    blok, semua = topeng(rgb_)
    sudut = condong(blok)
    cat = dict(skrip=ID, versi=VERSI, condong_darjah=sudut, baris_dijangka=n, amaran=[], gagal=[])
    lab, kom = _komponen(semua, sudut)
    jumlah = semua.sum()
    tinggi = [k["y1"] - k["y0"] for k in kom if k["luas"] >= 0.01 * jumlah]
    t_med = float(np.median(tinggi)) if tinggi else 0
    for k in kom:
        k["besar"] = k["luas"] >= HAD["besar_luas"] * jumlah and k["y1"] - k["y0"] >= HAD["besar_tinggi"] * t_med
    for k in kom:   # v1.1: komponen berbilang baris (huruf bertaut merentas baris) dikumpul ikut julat penuh y0-y1
        k["j0"], k["j1"] = ((k["y0"], k["y1"]) if k["y1"] - k["y0"] >= HAD["multi"] * t_med else (k["t20"], k["t80"]))
    besar = sorted([k for k in kom if k["besar"]], key=lambda k: k["j0"])
    kump = []
    for k in besar:   # julat bertindih (teras, atau penuh bagi komponen berbilang baris) = satu kumpulan
        if kump and k["j0"] <= kump[-1]["j1"]:
            kump[-1]["ahli"].append(k)
            kump[-1]["t80"] = max(kump[-1]["t80"], k["t80"])
            kump[-1]["j1"] = max(kump[-1]["j1"], k["j1"])
        else:
            kump.append(dict(ahli=[k], t20=k["t20"], t80=k["t80"], j1=k["j1"]))
    while len(kump) > n:   # gabung dua kumpulan berjiran yang paling rapat
        i = min(range(len(kump) - 1), key=lambda j: kump[j + 1]["t20"] - kump[j]["t80"])
        b = kump.pop(i + 1)
        kump[i]["ahli"] += b["ahli"]
        kump[i]["t80"] = max(kump[i]["t80"], b["t80"])
        cat["amaran"].append("dua kumpulan digabung menjadi satu baris (lebih kumpulan daripada baris ayat)")
    cat["kumpulan"] = len(kump)
    if not kump:
        cat["gagal"].append("tiada huruf dikesan")
        return None, cat
    huruf = kad.BLOK.get(kid, {}).get("huruf", {})
    # Baris bertaut (kad K3: baris bersentuh): kumpulan paling tinggi dibelah dahulu pada garis paling nipis.
    bil = [1] * len(kump)
    tg = [max(k["y1"] for k in g["ahli"]) - min(k["y0"] for k in g["ahli"]) for g in kump]
    while sum(bil) < n:
        i = max(range(len(kump)), key=lambda j: tg[j] / bil[j])
        bil[i] += 1
    garis, dibelah = [], 0
    for g, c in zip(kump, bil):
        if c == 1:
            garis.append(_baris([(k, np.ones(k["luas"], bool)) for k in g["ahli"]]))
            continue
        semua_y = np.concatenate([k["y"] for k in g["ahli"]])
        cuts = _potong(semua_y, c)
        had_jalur = [semua_y.min() - 1] + list(cuts) + [semua_y.max() + 1]
        bekas = [isinstance(huruf.get(baris[len(garis) + j][1]), dict) and "bekas" in huruf[baris[len(garis) + j][1]]
                 for j in range(c)]
        bah, belah = [[] for _ in range(c)], 0   # v1.1: belah pada leher paling sempit
        for k in g["ahli"]:
            lurus = np.searchsorted(cuts, k["y"])
            kira = np.bincount(lurus, minlength=c)
            ws = _belah_leher(k, had_jalur, semua.shape)
            if any(bekas[j] for j in np.nonzero(kira)[0]):   # sentuh baris berbekas (label): cara v1 di sekitar label
                if kira.max() >= 0.75 * k["luas"]:
                    jal = np.full(k["luas"], int(kira.argmax()))
                elif ws is None:
                    jal = lurus
                else:   # leher dipakai hanya antara dua baris berjiran tanpa bekas; selebihnya garis lurus v1
                    bk = np.array(bekas)
                    jal = np.where(~bk[lurus] & ~bk[ws] & (np.abs(ws - lurus) <= 1), ws, lurus)
            else:
                jal = ws if ws is not None else np.full(k["luas"], int(kira.argmax()))
            kira = np.bincount(jal, minlength=c)
            if (kira > 0).sum() == 1:
                bah[int(kira.argmax())].append((k, np.ones(k["luas"], bool)))
            else:
                belah += 1
                for j in np.nonzero(kira)[0]:
                    bah[j].append((k, jal == j))
        for ekor in (() if all(bah) else (0.75, 1.01)):   # jalur kosong: cara v1 (ekor ikut jalur terbesar, kemudian belah semua)
            bah, belah = [[] for _ in range(c)], 0
            for k in g["ahli"]:
                jal = np.searchsorted(cuts, k["y"])
                kira = np.bincount(jal, minlength=c)
                if kira.max() >= ekor * k["luas"]:   # ekor kecil (cth. ekor y) ikut jalur terbesar
                    bah[int(kira.argmax())].append((k, np.ones(k["luas"], bool)))
                else:
                    belah += 1
                    for j in np.nonzero(kira)[0]:
                        bah[j].append((k, jal == j))
            if all(bah):
                break
        dibelah += belah
        if any(not b for b in bah):
            cat["gagal"].append(f"baris bertaut tidak dapat dibelah kepada {c} baris")
            return None, cat
        garis += [_baris(b) for b in bah]
    if dibelah:
        cat["amaran"].append(f"{dibelah} komponen bertaut dibelah pada leher paling sempit: semak warna di sambungan")
    cat["baris_dikesan"] = len(garis)
    for g, (teks, r) in zip(garis, baris):
        g.update(teks=teks, peranan=r)
    pulang = _bekas_sahaja(garis, huruf, semua.shape)
    if pulang:
        cat["amaran"].append(f"{pulang} piksel ekor huruf di luar segi empat label dipulangkan ke baris asal")
    peta = np.zeros(semua.shape, np.uint8)
    for g in garis:
        for k, m in g["bahagian"]:
            peta[k["py"][m], k["px"][m]] = KOD[g["peranan"]]
    hiasan = 0
    for k in (k for k in kom if not k["besar"]):
        dalam = [g for g in garis if g["y0"] <= k["yc"] <= g["y1"]]
        g = min(dalam or garis, key=lambda g: abs((g["t20"] + g["t80"]) / 2 - k["yc"]))
        luar = not dalam or k["x1"] < g["x0"] or k["x0"] > g["x1"]
        peta[k["py"], k["px"]] = KOD["hiasan"] if luar else KOD[g["peranan"]]
        hiasan += luar
    pal = palet(kid)["peranan"]
    for g in garis:   # komponen utuh yang masuk teras baris lain yang berlainan warna
        for k, m in g["bahagian"]:
            if not m.all():
                continue
            for g2 in garis:
                if g2 is g or pal[g2["peranan"]] == pal[g["peranan"]]:
                    continue
                masuk = ((k["y"] >= g2["t20"]) & (k["y"] <= g2["t80"])).mean()
                if masuk > HAD["bertaut_gagal"]:
                    cat["gagal"].append(f"'{g['teks']}' masuk teras baris '{g2['teks']}' {masuk:.0%}: baris salah dibelah")
                elif masuk > HAD["bertaut"]:
                    cat["amaran"].append(f"'{g['teks']}' masuk teras baris '{g2['teks']}' {masuk:.0%}: semak warna")
    for g in garis:
        if isinstance(huruf.get(g["peranan"]), dict) and "bekas" in huruf[g["peranan"]]:
            k, m = max(g["bahagian"], key=lambda km: km[1].sum())
            t = np.zeros(semua.shape, np.uint8)
            t[k["py"][m], k["px"][m]] = 1
            cs, _ = cv2.findContours(t, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            c = max(cs, key=cv2.contourArea)
            (_, _), (rw, rh), _ = cv2.minAreaRect(c)
            isi = cv2.contourArea(c) / max(1.0, rw * rh)
            cat["bekas_isi"] = round(float(isi), 3)
            if isi < HAD["segi_empat"]:
                cat["gagal"].append(f"bekas '{g['teks']}' bukan segi empat (isi {isi:.0%}): tiada label atau baris salah dibelah")
    cat["baris"] = [dict(teks=g["teks"], peranan=g["peranan"], komponen=len(g["bahagian"]),
                         teras=[round(float(g["t20"])), round(float(g["t80"]))]) for g in garis]
    cat["hiasan"] = int(hiasan)
    return (None if cat["gagal"] else peta), cat


def peranan(rgb_, kid, aid, warna=None):
    # v1.3 (hp_neutral): --warna HP = satu dakwat untuk semua peranan, jadi peta peranan tidak diperlukan
    if warna == "HP" or (kad.KAD[kid]["dakwat"] == 1 and len(set(palet(kid)["peranan"].values())) == 1):
        blok, semua = topeng(rgb_)
        return semua.astype(np.uint8) * KOD["utama"], dict(skrip=ID, versi=VERSI, condong_darjah=condong(blok),
                                                           amaran=[], gagal=[],
                                                           nota="hitam putih (HP)" if warna == "HP" else "kad satu dakwat")
    return baris_peranan(rgb_, kid, aid)


def baca_log(peta_path):
    f = Path(peta_path).parent / "log_6.jsonl"
    stem = Path(peta_path).name.replace("_peranan.png", "")
    if not f.exists():
        return None
    rows = [json.loads(x) for x in f.read_text().splitlines() if x.strip()]
    rows = [r for r in rows if r.get("nama") == stem and r.get("skrip") == ID]
    return rows[-1] if rows else None


def tulis(keluar, stem, peta, pal, log, a=None):
    keluar.mkdir(parents=True, exist_ok=True)
    lulus = not log.get("gagal")
    if lulus:
        Image.fromarray(peta).save(keluar / f"{stem}_peranan.png")
        if a is not None:
            Image.fromarray(a).save(keluar / f"{stem}_alfa.png")
        Image.fromarray(warnakan(peta, pal, a)).save(keluar / f"{stem}_warna.png")
        ada = sorted({int(v) for v in np.unique(peta)} - {0})
        dakwat = list(dict.fromkeys(pal["peranan"][NAMA[v]] for v in ada))
        (keluar / f"{stem}_palet.json").write_text(json.dumps(dict(latar=pal["latar"], dakwat=dakwat,
                                                                   sumber=pal["sumber"]), indent=1))
        log["piksel"] = {NAMA[v]: int((peta == v).sum()) for v in ada}
    with open(keluar / "log_6.jsonl", "a") as fh:
        fh.write(json.dumps(dict(nama=stem, warna=pal["sumber"], lulus=lulus, **log), ensure_ascii=False) + "\n")
    return lulus


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 4:
        sys.exit(__doc__)
    pil = {a[i][2:]: a[i + 1] for i in range(4, len(a) - 1, 2)}
    f, kid, aid, keluar = Path(a[0]), a[1], a[2], Path(a[3])
    pal = palet(kid, pil.get("warna"))
    im = muat(f)
    peta, cat = peranan(im, kid, aid, pil.get("warna"))
    lulus = tulis(keluar, f.stem, peta, pal, dict(imej=str(f), kad=kid, ayat=aid, **cat), alfa(im))
    print(f.stem, "|", [b["teks"] + ":" + b["peranan"] for b in cat.get("baris", [])] or cat.get("nota", ""),
          "| hiasan", cat.get("hiasan", 0), "|", "lulus" if lulus else "GAGAL: " + "; ".join(cat["gagal"]),
          ("| amaran: " + "; ".join(cat["amaran"])) if cat["amaran"] else "")
