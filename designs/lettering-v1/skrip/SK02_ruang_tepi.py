"""SK02 Ruang tepi (Standard Lettering v1.2, langkah 5b, pembetulan 2 daripada 4). Versi 1, 26 Nov 2026.

Tugas: skala blok tulisan (sekata, dari pusat blok) supaya ruang tepi sama dengan nilai kad.
Diperlukan oleh: semua kad (set asas).
Parameter kad: rujukan.tepi_pct jika diukur daripada upload; jika tidak, ruang_tepi kad. Ruang tepi = sisi paling
sempit bila blok dipusatkan: min((1 - lebar blok / lebar) / 2, (1 - tinggi blok / tinggi) / 2).
Jalan hanya bila beza melebihi HAD["tepi"] (mata peratus).
Guna: python3 SK02_ruang_tepi.py <imej> <kad> <keluar.png> [--tepi P]
"""
import cv2

import asas

ID = "SK02"


def matriks(u, ruj, had=asas.HAD):
    beza = round(u["tepi_pct"] - ruj["tepi_pct"], 1)
    if abs(beza) <= had["tepi"]:
        return None, dict(jalan=False, sebab=f"dalam had: beza {beza} mata")
    x0, y0, x1, y1 = u["kotak"]
    muat_ = 1 - 2 * ruj["tepi_pct"] / 100
    f = min(u["w"] * muat_ / (x1 - x0), u["h"] * muat_ / (y1 - y0))
    return asas.tiga(cv2.getRotationMatrix2D(((x0 + x1) / 2, (y0 + y1) / 2), 0, f)), dict(jalan=True, skala=round(f, 3))


def betul(rgb, ruj, had=asas.HAD):
    M, cat = matriks(asas.ukur(rgb), ruj, had)
    return (rgb if M is None else asas.lukis(rgb, M)), cat


if __name__ == "__main__":
    import SK02_ruang_tepi
    asas.cli(SK02_ruang_tepi)
