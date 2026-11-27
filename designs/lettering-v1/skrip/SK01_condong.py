"""SK01 Condong (Standard Lettering v1.2, langkah 5b, pembetulan 1 daripada 4). Versi 1, 26 Nov 2026.

Tugas: putar seluruh blok tulisan ke sudut rujukan kad; bucu diisi warna latar.
Diperlukan oleh: kad yang bloknya condong (K3, rujukan IMG_5775; K1, K6 bila sudutnya sudah diukur).
Parameter kad: rujukan.condong_darjah (diukur SK05 daripada gambar upload). Kad tanpa condong tidak pernah diputar.
Jalan hanya bila beza sudut melebihi HAD["condong"].
Guna: python3 SK01_condong.py <imej> <kad> <keluar.png> [--condong D]
"""
import cv2

import asas

ID = "SK01"


def matriks(u, ruj, had=asas.HAD):
    """Pulang (matriks 3x3 atau None, catatan). Positif = baris naik ke kanan."""
    if not ruj["kad_condong"]:
        return None, dict(jalan=False, sebab="kad tiada condong")
    if ruj["condong_darjah"] is None:
        return None, dict(jalan=False, sebab="tiada sudut rujukan (belum diukur daripada upload)")
    beza = round(ruj["condong_darjah"] - u["condong_darjah"], 1)
    if abs(beza) <= had["condong"]:
        return None, dict(jalan=False, sebab=f"dalam had: beza {beza} darjah")
    x0, y0, x1, y1 = u["kotak"]
    return asas.tiga(cv2.getRotationMatrix2D(((x0 + x1) / 2, (y0 + y1) / 2), beza, 1.0)), dict(jalan=True, putar_darjah=beza)


def betul(rgb, ruj, had=asas.HAD):
    M, cat = matriks(asas.ukur(rgb), ruj, had)
    return (rgb if M is None else asas.lukis(rgb, M)), cat


if __name__ == "__main__":
    import SK01_condong
    asas.cli(SK01_condong)
