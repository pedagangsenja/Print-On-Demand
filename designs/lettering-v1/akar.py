"""Akar rekod untuk belajar.py dan belajar_sk.py: cawangan ini + salinan rekod cawangan sesi lain (gabung_cawangan.py).
Tag cawangan ditambah pada nama batch / kad / imej: '<tag>:<nama>' (ID kad yang sama = gaya berlainan dalam sesi lain)."""
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def akar():
    return [("", HERE)] + [(os.path.basename(d), d) for d in sorted(glob.glob(os.path.join(HERE, "cawangan", "*")))
                           if os.path.isdir(d)]


def tanda(t, s):
    return f"{t}:{s}" if t and s else s
