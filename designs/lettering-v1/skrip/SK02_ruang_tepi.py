"""SK02 Ruang tepi (Standard Lettering v1.2, langkah 5b, pembetulan 2 daripada 4). Versi 1.1, 26 Nov 2026.
v1.1: ruang tepi sisi dan atas / bawah boleh berbeza (diukur berasingan daripada gambar upload). Sebab: rujukan K7
      (poster 2:3) ada sisi 6% tetapi atas / bawah 11%; satu angka menjadikan blok terlalu rapat ke atas dan bawah
      pada kanvas 3:4 (ditemui pada larian pertama).

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


def beza_tepi(u, ruj):
    """Pulang (beza dalam mata peratus pada sisi yang mengehad, faktor skala). Rujukan boleh memberi ruang tepi sisi
    dan atas / bawah berasingan (tepi_sisi_pct, tepi_atas_bawah_pct); jika tiada, satu angka tepi_pct untuk semua."""
    x0, y0, x1, y1 = u["kotak"]
    ts, ta = ruj.get("tepi_sisi_pct", ruj["tepi_pct"]), ruj.get("tepi_atas_bawah_pct", ruj["tepi_pct"])
    fw, fh = u["w"] * (1 - 2 * ts / 100) / (x1 - x0), u["h"] * (1 - 2 * ta / 100) / (y1 - y0)
    if fw <= fh:  # lebar mengehad
        return round((1 - (x1 - x0) / u["w"]) / 2 * 100 - ts, 1), fw
    return round((1 - (y1 - y0) / u["h"]) / 2 * 100 - ta, 1), fh


def matriks(u, ruj, had=asas.HAD):
    beza, f = beza_tepi(u, ruj)
    if abs(beza) <= had["tepi"]:
        return None, dict(jalan=False, sebab=f"dalam had: beza {beza} mata")
    x0, y0, x1, y1 = u["kotak"]
    return asas.tiga(cv2.getRotationMatrix2D(((x0 + x1) / 2, (y0 + y1) / 2), 0, f)), dict(jalan=True, skala=round(f, 3))


def betul(rgb, ruj, had=asas.HAD):
    M, cat = matriks(asas.ukur(rgb), ruj, had)
    return (rgb if M is None else asas.lukis(rgb, M)), cat


if __name__ == "__main__":
    import SK02_ruang_tepi
    asas.cli(SK02_ruang_tepi)
