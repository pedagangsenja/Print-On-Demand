"""SK08 Bayang ikut kad (Standard Lettering v1.2, langkah 6). Versi 1, 27 Nov 2026.

Tugas: tambah bayang 3D yang AI tidak jana (prompt hitam putih melarang kelabu dan bayang) pada peranan yang kad
minta, selepas SK07 (peta peranan). Diperlukan oleh: K3, gambar upload IMG_5775 (skrip putih ada kelabu cerah).
Parameter kad: KAD[kad]["peta_warna"]["bayang"] (nombor dakwat) dan BLOK[kad]["rujukan"]["bayang"]:
  jenis="dalam", peranan, arah_relatif_darjah, nisbah, warna_ukur (diukur oleh mod --ukur pada gambar upload).

Ukuran pada IMG_5775 (salinan dashboard 236x354): bayang BUKAN di luar huruf. Bahagian bawah setiap strok skrip
berwarna kelabu cerah, bahagian atas putih (dua tona rata, histogram dua puncak). Model: bagi setiap piksel strok,
ukur larian strok pada arah bayang; piksel di `nisbah` larian yang paling hampir dengan hujung arah itu = kelabu.
Arah disimpan relatif kepada garis dasar baris (condong blok ditambah semasa dipakai). Model tidak bergantung
kepada saiz imej. Had: satu gambar, resolusi rendah; padanan model dengan gambar (IoU) dicatat pada kad.
Bayang lembut K1 (IMG_5818: bayang jatuh atas coretan lain di bawahnya) TIDAK dibuat: imej hitam putih rata tidak
menyimpan susunan coretan (mana di atas, mana di bawah).

Guna: python3 SK08_bayang.py --ukur <gambar upload> <kad>            -> JSON untuk BLOK[kad]["rujukan"]["bayang"]
      python3 SK08_bayang.py <nama>_peranan.png <kad> <folder keluar> [--warna Cxxx]
Hasil (fail asal tidak ditimpa): <nama>_bayang_peranan.png (kod 5 = bayang), <nama>_bayang_warna.png,
<nama>_bayang_palet.json,
log_6.jsonl (kongsi piksel berbayang sebelum / selepas, banding rujukan).
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import SK07_warna as sk07  # noqa: E402
from SK05_ukur import condong, muat, topeng  # noqa: E402

ID, VERSI = "SK08", "SK08 v1 (27 Nov 2026)"
HAD_KONGSI = 15   # mata %: beza kongsi piksel berbayang dengan rujukan sebelum amaran
LEMBUT = 0.0025   # sigma pelembut sempadan bayang, nisbah sisi panjang imej


def pecahan(m, arah):
    """Bagi setiap piksel topeng m: kedudukan sepanjang larian strok pada arah `arah` (darjah, 0 = kanan,
    90 = atas, ikut jam terbalik). 0 = hujung larian di sebelah arah itu, 1 = hujung bertentangan."""
    h, w = m.shape
    d = int(np.ceil(np.hypot(h, w))) + 2
    px, py = (d - w) // 2, (d - h) // 2
    besar = cv2.copyMakeBorder(m.astype(np.uint8), py, d - h - py, px, d - w - px, cv2.BORDER_CONSTANT, value=0)
    R = cv2.getRotationMatrix2D((d / 2, d / 2), 270 - arah, 1)   # putar supaya arah menghala ke bawah imej
    r = cv2.warpAffine(besar, R, (d, d), flags=cv2.INTER_NEAREST) > 0
    atas, bawah = np.zeros(r.shape, np.float32), np.zeros(r.shape, np.float32)
    for y in range(1, d):
        atas[y] = (atas[y - 1] + 1) * r[y]
    atas[0] = r[0]
    bawah[-1] = r[-1]
    for y in range(d - 2, -1, -1):
        bawah[y] = (bawah[y + 1] + 1) * r[y]
    fr = np.where(r, (bawah - 0.5) / np.maximum(atas + bawah - 1, 1), 1.0).astype(np.float32)
    balik = cv2.warpAffine(fr, cv2.invertAffineTransform(R), (d, d), flags=cv2.INTER_NEAREST, borderValue=1.0)
    return balik[py:py + h, px:px + w]


def bayang_topeng(m, arah, nisbah):
    """Kawasan bayang dalam topeng m. Sempadan dilembutkan (Gaussian, sigma 0.25% sisi panjang imej) supaya garis
    putih / kelabu licin, bukan anak tangga piksel."""
    g = (m & (pecahan(m, arah) < nisbah)).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), LEMBUT * max(m.shape)) > 0.5
    return m & g


def ukur_rujukan(path):
    """Ukur bayang dalam pada gambar upload berwarna: siluet strok neutral (putih + kelabu), kelabu = bawah ambang
    Otsu kecerahan dalam siluet. Cari arah (darjah imej) dan nisbah dengan IoU terbaik, dengan syarat kongsi piksel
    kelabu model tidak lari lebih 7 mata % daripada gambar."""
    rgb = muat(path)
    blok, _ = topeng(rgb)
    sudut = condong(blok)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    S, V = hsv[..., 1].astype(int), hsv[..., 2]
    neutral = ((S < 45) & (V > 90)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(neutral, 8)
    simpan = np.zeros(n, bool)
    simpan[1:] = st[1:, cv2.CC_STAT_AREA] >= 0.0007 * neutral.size
    sil = simpan[lab]
    dalam = cv2.erode(sil.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)   # buang cincin anti-alias
    t, _ = cv2.threshold(V[dalam].reshape(-1, 1), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kelabu = dalam & (V < t)
    kongsi_ruj = kelabu.sum() / dalam.sum() * 100

    def skor(a, k):
        gp = dalam & bayang_topeng(sil, a, k)
        kongsi = gp.sum() / dalam.sum() * 100
        return (gp & kelabu).sum() / max(1, (gp | kelabu).sum()), kongsi

    calon = {}
    for a in range(0, 360, 5):
        fr = pecahan(sil, a)
        for k in np.arange(0.2, 0.71, 0.05):
            gp = (m := (sil & (fr < k)).astype(np.float32))
            gp = dalam & sil & (cv2.GaussianBlur(m, (0, 0), LEMBUT * max(sil.shape)) > 0.5)
            kongsi = gp.sum() / dalam.sum() * 100
            if abs(kongsi - kongsi_ruj) <= 7:
                calon[(a, round(float(k), 2))] = (gp & kelabu).sum() / max(1, (gp | kelabu).sum())
    a0, k0 = max(calon, key=calon.get)
    halus = {(a, k0): skor(a, k0) for a in range(a0 - 4, a0 + 5)}
    halus = {p: v for p, v in halus.items() if abs(v[1] - kongsi_ruj) <= 7}
    (a1, k1), (iou, kongsi) = max(halus.items(), key=lambda kv: kv[1][0])
    teras = cv2.erode(kelabu.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    warna = np.median(rgb[teras if teras.sum() > 50 else kelabu], axis=0)
    putih = np.median(rgb[dalam & ~kelabu], axis=0)
    return dict(jenis="dalam", arah_relatif_darjah=int(a1 - round(sudut)), nisbah=k1,
                warna_ukur=sk07.hexa(warna), putih_ukur=sk07.hexa(putih), iou=round(float(iou), 3),
                kongsi_ruj_pct=round(float(kongsi_ruj), 1), kongsi_model_pct=round(float(kongsi), 1),
                condong_gambar=sudut, saiz=list(rgb.shape[1::-1]), versi=VERSI)


def bayang(peta, kid, sudut):
    """Tambah kod bayang (5) pada peranan yang kad minta. Pulang (peta baharu, catatan)."""
    b = kad_bayang(kid)
    arah = b["arah_relatif_darjah"] + sudut
    m = np.isin(peta, [sk07.KOD[r] for r in b["peranan"]])
    g = bayang_topeng(m, arah, b["nisbah"])
    out = peta.copy()
    out[g] = sk07.KOD["bayang"]
    kongsi = round(float(g.sum() / max(1, m.sum()) * 100), 1)
    amaran = []
    if not m.any():
        amaran.append(f"tiada piksel peranan {b['peranan']}: bayang tidak dibuat")
    elif abs(kongsi - b["kongsi_ruj_pct"]) > HAD_KONGSI:
        amaran.append(f"kongsi bayang {kongsi}% jauh daripada rujukan {b['kongsi_ruj_pct']}%")
    return out, dict(skrip=ID, versi=VERSI, arah_imej_darjah=round(arah, 1), nisbah=b["nisbah"],
                     peranan=b["peranan"], kongsi_bayang_pct=kongsi, kongsi_ruj_pct=b["kongsi_ruj_pct"],
                     amaran=amaran)


def kad_bayang(kid):
    b = sk07.kad.BLOK[kid].get("rujukan", {}).get("bayang")
    if not b:
        raise SystemExit(f"{kid}: tiada rujukan bayang pada kad (jalan --ukur pada gambar upload dahulu)")
    return b


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "--ukur":
        print(json.dumps(dict(gambar=Path(a[1]).name, kad=a[2], **ukur_rujukan(a[1])), ensure_ascii=False))
        sys.exit()
    pil = {a[i][2:]: a[i + 1] for i in range(3, len(a) - 1, 2)}
    if len(a) < 3:
        sys.exit(__doc__)
    sumber, kid, keluar = Path(a[0]), a[1], Path(a[2])
    peta = np.array(Image.open(sumber))
    log_sumber = sk07.baca_log(sumber)
    sudut = log_sumber.get("condong_darjah", 0.0) if log_sumber else 0.0
    baru, cat = bayang(peta, kid, sudut)
    stem = sumber.name.replace("_peranan.png", "") + "_bayang"
    pal = sk07.palet(kid, pil.get("warna"))
    fa = Path(str(sumber).replace("_peranan.png", "_alfa.png"))
    a_ = np.array(Image.open(fa)) if fa.exists() else None
    sk07.tulis(keluar, stem, baru, pal, dict(imej=str(sumber), kad=kid, **cat), a_)
    print(stem, "| bayang", cat["kongsi_bayang_pct"], "% (rujukan", cat["kongsi_ruj_pct"], "%) |",
          "amaran: " + "; ".join(cat["amaran"]) if cat["amaran"] else "lulus")
