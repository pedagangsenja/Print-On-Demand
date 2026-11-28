"""Gabung rekod QC dan log belajar daripada cawangan sesi lain (keputusan pengguna 28 Nov 2026).

Sebab: beberapa sesi Claude bekerja serentak pada cawangan berlainan; setiap sesi memuat naik jadual belajar dashboard
(aturan_belajar, sk_belajar) daripada rekod cawangannya sahaja, jadi muat naik terakhir menimpa yang lain.
Skrip ini menyalin rekod (bukan imej) setiap cawangan ke cawangan/<tag>/ dengan laluan yang sama, supaya belajar.py dan
belajar_sk.py membaca SEMUA rekod. Tag ditambah pada nama batch dan kad (cth. 'lucid-galileo:K9') kerana ID kad yang
sama dipakai untuk gaya yang berlainan dalam sesi berlainan.

Disalin (hanya fail yang berbeza daripada HEAD): qc/*.json, raw/*/*/log.jsonl, betul/*/*/log_5b.jsonl,
final/*/*/info.json, final/*/peranan/log_6.jsonl, belajar/{ubahan.json, sk_ubahan.json, sk_semakan.jsonl,
pengguna.jsonl, sk_pengguna.jsonl}.

Guna: python3 gabung_cawangan.py origin/claude/<cawangan> [...]   (git fetch dahulu; jalan semula = kemas kini)
"""
import fnmatch
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AKAR = "designs/lettering-v1/"
CORAK = ["qc/*.json", "raw/*/*/log.jsonl", "betul/*/*/log_5b.jsonl", "final/*/*/info.json", "final/*/peranan/log_6.jsonl",
         "belajar/ubahan.json", "belajar/sk_ubahan.json", "belajar/sk_semakan.jsonl", "belajar/pengguna.jsonl",
         "belajar/sk_pengguna.jsonl"]


def git(*a):
    return subprocess.run(["git", *a], cwd=HERE, check=True, capture_output=True).stdout


def tag(cawangan):
    nama = cawangan.rsplit("/", 1)[-1]
    return nama.rsplit("-", 1)[0] if "-" in nama else nama


def salin(cawangan):
    t = tag(cawangan)
    keluar = os.path.join(HERE, "cawangan", t)
    shutil.rmtree(keluar, ignore_errors=True)
    fail = git("diff", "--name-only", "--diff-filter=AM", f"HEAD...{cawangan}", "--", ":/" + AKAR).decode().split()
    n = 0
    for f in fail:
        rel = f[len(AKAR):]
        if not any(fnmatch.fnmatch(rel, c) and rel.count("/") == c.count("/") for c in CORAK):
            continue
        p = os.path.join(keluar, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        isi = git("show", f"{cawangan}:{f}")
        lokal = os.path.join(HERE, rel)
        if rel.endswith(".jsonl") and os.path.exists(lokal):  # buang baris yang sudah ada dalam fail cawangan ini
            ada = set(open(lokal, "rb").read().splitlines())
            isi = b"".join(x + b"\n" for x in isi.splitlines() if x.strip() and x not in ada)
            if not isi:
                continue
        open(p, "wb").write(isi)
        n += 1
    if n:
        sumber = dict(cawangan=cawangan, commit=git("rev-parse", cawangan).decode().strip(), fail=n)
        json.dump(sumber, open(os.path.join(keluar, "SUMBER.json"), "w"), ensure_ascii=False, indent=1)
    print(f"{t}: {n} fail")


if __name__ == "__main__":
    for c in sys.argv[1:]:
        salin(c)
