"""SK04 Hitam putih bersih (Standard Lettering v1.2, langkah 5b, pembetulan 4 daripada 4, AKHIR sekali). Versi 1, 26 Nov 2026.

Tugas: tukar kelabu rata, latar yang bukan hitam tulen dan tepi kabur kepada hitam dan putih tulen.
Cara: besarkan 3x, ambang (Otsu), kecilkan semula; tepi huruf kekal licin selebar kira-kira 1 piksel.
Diperlukan oleh: semua kad (set asas), KECUALI kad yang memang ada bayang lembut (K1): kad itu tidak disentuh.
Parameter kad: tiada. Untuk imej mentah hitam putih sahaja (dakwat putih atas latar hitam).
Jalan bila: SK01-SK03 baru dijalankan (putar / skala menghasilkan tepi kelabu), atau kelabu rata melebihi
HAD["kelabu_rata"] (% piksel), atau latar lebih cerah daripada HAD["latar"].
Guna: python3 SK04_hitam_putih.py <imej> <kad> <keluar.png>
"""
import cv2
import numpy as np

import asas

ID = "SK04"


def perlu(u, ruj, had=asas.HAD, selepas_ubah=False):
    if ruj["kad_bayang"]:
        return False, "kad ada bayang lembut: tidak disentuh"
    if selepas_ubah:
        return True, "selepas putar / skala / alih"
    if u["kelabu_rata_pct"] > had["kelabu_rata"]:
        return True, f"kelabu rata {u['kelabu_rata_pct']} %"
    if max(u["latar"]) > had["latar"]:
        return True, f"latar {u['latar']} bukan hitam tulen"
    return False, "dalam had"


def bersih(rgb):
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    besar = cv2.resize(g, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    _, bw = cv2.threshold(besar, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kecil = cv2.resize(bw, (g.shape[1], g.shape[0]), interpolation=cv2.INTER_AREA)
    return np.dstack([kecil] * 3)


def betul(rgb, ruj, had=asas.HAD, selepas_ubah=False):
    ya, sebab = perlu(asas.ukur(rgb), ruj, had, selepas_ubah)
    return (bersih(rgb) if ya else rgb), dict(jalan=ya, sebab=sebab)


if __name__ == "__main__":
    import SK04_hitam_putih
    asas.cli(SK04_hitam_putih)
