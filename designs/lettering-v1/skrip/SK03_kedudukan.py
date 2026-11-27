"""SK03 Kedudukan (Standard Lettering v1.2, langkah 5b, pembetulan 3 daripada 4). Versi 1, 26 Nov 2026.

Tugas: alih blok tulisan supaya pusatnya di tengah kanvas.
Diperlukan oleh: semua kad (set asas). Parameter kad: tiada.
Jalan hanya bila pusat blok lari melebihi HAD["pusat"] (% kanvas) pada mana-mana paksi.
Guna: python3 SK03_kedudukan.py <imej> <kad> <keluar.png>
"""
import numpy as np

import asas

ID = "SK03"


def matriks(u, ruj=None, had=asas.HAD):
    if max(abs(u["pusat_dx_pct"]), abs(u["pusat_dy_pct"])) <= had["pusat"]:
        return None, dict(jalan=False, sebab=f"dalam had: lari {u['pusat_dx_pct']}, {u['pusat_dy_pct']} %")
    x0, y0, x1, y1 = u["kotak"]
    dx, dy = u["w"] / 2 - (x0 + x1) / 2, u["h"] / 2 - (y0 + y1) / 2
    return np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1.0]]), dict(jalan=True, alih_px=[round(dx, 1), round(dy, 1)])


def betul(rgb, ruj=None, had=asas.HAD):
    M, cat = matriks(asas.ukur(rgb), ruj, had)
    return (rgb if M is None else asas.lukis(rgb, M)), cat


if __name__ == "__main__":
    import SK03_kedudukan
    asas.cli(SK03_kedudukan)
