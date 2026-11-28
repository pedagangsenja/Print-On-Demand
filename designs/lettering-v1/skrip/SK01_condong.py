"""SK01 Condong (Standard Lettering v1.2, langkah 5b, pembetulan 1 daripada 4). Versi 1.1, 28 Nov 2026.
v1.1 (keputusan pengguna 28 Nov 2026): kad "tiada condong" yang ADA sudut rujukan terukur (bukti rujukan memang
     mendatar, cth. K24: 1.8 darjah) kini DILURUSKAN ke 0 darjah bila imej condong lebih 3 darjah. Dahulu kad sebegini
     tidak pernah diputar, jadi imej yang condong 6-8 darjah terlepas. Had 3 darjah (bukan 1.5) kerana ukuran sudut
     pada tulisan skrip tidak stabil: percubaan pertama (kejar 1.8 darjah, had 1.5) memutar imej yang sudah mendatar
     dan menggagalkan 4 daripada 10 imej. Kad tiada condong TANPA sudut rujukan: masih tidak disentuh.

Tugas: putar seluruh blok tulisan ke sudut rujukan kad; bucu diisi warna latar.
Diperlukan oleh: kad yang bloknya condong (K3, rujukan IMG_5775; K1, K6 bila sudutnya sudah diukur).
Parameter kad: rujukan.condong_darjah (diukur SK05 / SK09 daripada gambar upload).
Jalan hanya bila beza sudut melebihi HAD["condong"].
Guna: python3 SK01_condong.py <imej> <kad> <keluar.png> [--condong D]
"""
import cv2

import asas

ID = "SK01"
HAD_LURUS = 3.0   # kad tiada condong: luruskan ke 0 hanya bila imej condong lebih daripada ini (darjah)


def matriks(u, ruj, had=asas.HAD):
    """Pulang (matriks 3x3 atau None, catatan). Positif = baris naik ke kanan."""
    if not ruj["kad_condong"] and ruj["condong_darjah"] is None:
        return None, dict(jalan=False, sebab="kad tiada condong dan tiada sudut rujukan")
    if ruj["condong_darjah"] is None:
        return None, dict(jalan=False, sebab="tiada sudut rujukan (belum diukur daripada upload)")
    sasaran, h = (ruj["condong_darjah"], had["condong"]) if ruj["kad_condong"] else (0.0, HAD_LURUS)
    beza = round(sasaran - u["condong_darjah"], 1)
    if abs(beza) <= h:
        return None, dict(jalan=False, sebab=f"dalam had: beza {beza} darjah")
    x0, y0, x1, y1 = u["kotak"]
    return asas.tiga(cv2.getRotationMatrix2D(((x0 + x1) / 2, (y0 + y1) / 2), beza, 1.0)), dict(jalan=True, putar_darjah=beza)


def betul(rgb, ruj, had=asas.HAD):
    M, cat = matriks(asas.ukur(rgb), ruj, had)
    return (rgb if M is None else asas.lukis(rgb, M)), cat


if __name__ == "__main__":
    import SK01_condong
    asas.cli(SK01_condong)
