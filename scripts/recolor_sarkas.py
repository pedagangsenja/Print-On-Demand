"""Warna semula 30 design sarkastik (hitam atas putih) ikut 5 palet contoh Pinterest.

Guna: python scripts/recolor_sarkas.py <dir_png_hitam_putih> <dir_output>
Setiap baris ayat diwarna ikut urutan palet; hiasan kecil dan swash/bingkai guna warna aksen.
Palet diagih ikut susunan: design ke-i guna palet i % 5. Palet 'hijau' dan 'merah' diberi tekstur kasar.
"""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ORDER = ['lazy', 'disturbed', 'vacation', 'nobody', 'adult', 'funsize', 'sideeye', 'judging', 'bed', 'cats',
         'email', 'friday', 'hardly', 'patience', 'schedule', 'meeting', 'monday', 'coffeefirst', 'decaf',
         'bloodtype', 'stayin', 'peopling', 'books', 'wenthome', 'momvoice', 'askdad', 'saidso', 'tiredmom',
         'tinyhumans', 'momhair']

H = lambda s: np.array([int(s[i:i + 2], 16) for i in (1, 3, 5)], float)
PAL = {
    'oren':   dict(bg='#1F2A3C', seq=['#F4F6F8', '#A9B0BC', '#F2A12B'], accent='#F2A12B', deco='#F2A12B', grunge=False),
    'kuning': dict(bg='#0B0B0B', seq=['#F5C518', '#F2F2F2'], accent='#F5C518', deco='#F5C518', grunge=False),
    'hijau':  dict(bg='#0A0A0A', seq=['#F3F1EA', '#A4C93A'], accent='#A4C93A', deco='#A4C93A', grunge=True),
    'merah':  dict(bg='#0E0E0E', seq=['#E5554F', '#EDE3CC', '#4E8A8C'], accent='#EDE3CC', deco='#E5554F', grunge=True),
    'biru':   dict(bg='#0D1F45', seq=['#BFE6F7', '#29A9E1'], accent='#29A9E1', deco='#BFE6F7', grunge=False),
}
PNAMES = list(PAL)
# design yang huruf dua barisnya bersambung (cth. 'Going' + 'OUT'): warna dipecah ikut baris per piksel
SPLIT = {'stayin'}


def line_colors(n, seq):
    if len(seq) == 3 and n >= 3:  # palet 3 warna: baris pertama & akhir warna utama, tengah selang-seli
        mid = [seq[1 + i % 2] for i in range(n - 2)]
        return [seq[0]] + mid + [seq[0]]
    return [seq[i % len(seq)] for i in range(n)]


def recolor(img, pal, seed, split=False):
    g = np.asarray(img.convert('L'), float) / 255.0
    h, w = g.shape
    alpha = np.clip((0.92 - g) / 0.84, 0, 1)
    solid = g < 0.5
    lab, n = ndi.label(solid)
    if n == 0:
        raise ValueError('tiada piksel teks')
    objs = ndi.find_objects(lab)
    area = ndi.sum(solid, lab, range(1, n + 1))
    min_a = 0.0012 * h * w
    kind = {}  # id -> 'deco' | 'accent' | line index
    texts = []
    tall = []
    for i, sl in enumerate(objs, 1):
        hh = sl[0].stop - sl[0].start
        ww = sl[1].stop - sl[1].start
        if area[i - 1] < min_a:
            kind[i] = 'deco'
        elif (hh > 0.32 * h and (not split or area[i - 1] / (hh * ww) < 0.25)) or (ww > 0.55 * w and area[i - 1] / (hh * ww) < 0.18):
            kind[i] = 'accent'  # bingkai / swash panjang
        elif hh > 0.32 * h and split:
            tall.append(i)  # huruf dari dua baris yang bersambung; warna ikut baris terdekat per piksel
        else:
            texts.append((i, sl[0].start, sl[0].stop))
    # himpun komponen teks kepada baris ikut pertindihan menegak
    texts.sort(key=lambda t: (t[1] + t[2]) / 2)
    lines = []
    for i, a, b in texts:
        for L in lines:
            ov = min(b, L['b']) - max(a, L['a'])
            if ov > 0.5 * min(b - a, L['b'] - L['a']):
                L['ids'].append(i); L['a'] = min(a, L['a']); L['b'] = max(b, L['b'])
                break
        else:
            lines.append(dict(a=a, b=b, ids=[i]))
    lines.sort(key=lambda L: L['a'])
    # gabung baris yang hampir terkandung dalam baris lain (huruf skrip tidak bersambung, cth. "Going")
    merged = True
    while merged:
        merged = False
        for x in range(len(lines)):
            for y in range(x + 1, len(lines)):
                A, B = lines[x], lines[y]
                ov = min(A['b'], B['b']) - max(A['a'], B['a'])
                if ov > 0.8 * min(A['b'] - A['a'], B['b'] - B['a']):
                    A['ids'] += B['ids']; A['a'] = min(A['a'], B['a']); A['b'] = max(A['b'], B['b'])
                    del lines[y]; merged = True
                    break
            if merged:
                break
    lines.sort(key=lambda L: L['a'])
    cols = line_colors(len(lines), pal['seq'])
    cmap = np.zeros((n + 1, 3))
    for i, k in kind.items():
        cmap[i] = H(pal[k])
    for L, c in zip(lines, cols):
        for i in L['ids']:
            cmap[i] = H(c)
    # sebar label ke piksel tepi (anti-alias)
    _, (iy, ix) = ndi.distance_transform_edt(lab == 0, return_indices=True)
    near = lab[iy, ix]
    color = cmap[near]
    if tall and lines:
        cy = np.array([(L['a'] + L['b']) / 2 for L in lines])
        rowcol = np.array([H(cols[int(np.argmin(np.abs(cy - y)))]) for y in range(h)])
        m = np.isin(near, tall)
        color[m] = rowcol[np.nonzero(m)[0]]
    if pal['grunge']:
        rng = np.random.default_rng(seed)
        big = ndi.gaussian_filter(rng.random((h, w)), 3.0)
        fine = ndi.gaussian_filter(rng.random((h, w)), 0.8)
        holes = (big < np.quantile(big, 0.10)) | (fine < np.quantile(fine, 0.03))
        alpha = alpha * np.where(holes, 0.0, 1.0)
        alpha = ndi.gaussian_filter(alpha, 0.6)
    bg = H(pal['bg'])
    out = bg * (1 - alpha[..., None]) + color * alpha[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), len(lines)


def main(src, dst):
    os.makedirs(dst, exist_ok=True)
    for k, did in enumerate(ORDER):
        pn = PNAMES[k % 5]
        im, nl = recolor(Image.open(os.path.join(src, did + '.png')), PAL[pn], seed=k, split=did in SPLIT)
        im.save(os.path.join(dst, f'{did}.png'))
        print(f'{k + 1:2d} {did:12s} palet={pn:7s} baris={nl}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
