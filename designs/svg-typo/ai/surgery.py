"""Text-line surgery for generated posters.
bands(path)            -> print ink row bands (y0,y1,x0,x1)
show(path, out, bands) -> save stacked crops of bands for viewing
glyphs(arr, y0,y1,x0,x1) -> glyph list (connected comps grouped by x-overlap)
rebuild(src, dst, y0,y1, order, ...) -> recompose one line from glyph indices
"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd

def load(p): return np.array(Image.open(p).convert("L")).astype(np.float32)

def bands(p, thr=128, mingap=3):
    a = load(p); ink = a < thr
    rows = ink.sum(1) > 0
    out = []; y = 0; H = len(rows)
    while y < H:
        if rows[y]:
            y0 = y
            while y < H and rows[y]: y += 1
            xs = np.where(ink[y0:y].any(0))[0]
            out.append((y0, y, int(xs.min()), int(xs.max())))
        y += 1
    return out

def glyphs(a, y0, y1, x0=0, x1=None, thr=128):
    x1 = a.shape[1] if x1 is None else x1
    ink = a < thr
    lab, n = nd.label(ink)
    objs = nd.find_objects(lab)
    comps = []
    for i, sl in enumerate(objs):
        cy = (sl[0].start + sl[0].stop) / 2; cx = (sl[1].start + sl[1].stop) / 2
        if y0 <= cy <= y1 and x0 <= cx <= x1 and (sl[0].stop - sl[0].start) <= (y1 - y0) * 1.25:
            comps.append((sl[1].start, sl[1].stop, sl[0].start, sl[0].stop, i + 1))
    comps.sort()
    gl = []
    for c in comps:
        if gl and c[0] < gl[-1]["x1"] - 2:
            g = gl[-1]; g["x1"] = max(g["x1"], c[1]); g["y0"] = min(g["y0"], c[2]); g["y1"] = max(g["y1"], c[3]); g["ids"].append(c[4])
        else:
            gl.append({"x0": c[0], "x1": c[1], "y0": c[2], "y1": c[3], "ids": [c[4]]})
    for g in gl:
        m = np.isin(lab, g["ids"])
        g["mask"] = nd.binary_dilation(m, iterations=2)
    return gl, lab

def bgval(a): return float(np.median(a[a > 200])) if (a > 200).any() else 255.0

def rebuild(src, dst, y0, y1, order, x0=0, x1=None, gap=None, wordgap=None, extra=None, center=None, maxw=None, split=None):
    """order: list of glyph indices (int), ' ' for word space, or ('x', k) for extra glyph k.
    extra: list of (path, y0, y1, x0, x1, glyph_index) taken from any image, scaled to this line's cap height.
    split: list of x positions where touching glyphs should be cut (applied before grouping)."""
    a = load(src); bg = bgval(a)
    if split:
        for sx in split: a[y0:y1, sx] = 255
    gl, lab = glyphs(a, y0, y1, x0, x1)
    print("glyphs:", [(i, g["x0"], g["x1"]) for i, g in enumerate(gl)])
    if not order: return gl
    capt = int(np.median([g["y0"] for g in gl])); capb = int(np.median([g["y1"] for g in gl]))
    gaps = [gl[i + 1]["x0"] - gl[i]["x1"] for i in range(len(gl) - 1)]
    g0 = gap if gap is not None else int(np.median([g for g in gaps if g < (capb - capt) * 0.3] or [6]))
    wg = wordgap if wordgap is not None else int((capb - capt) * 0.28)
    pieces = []  # (img crop with white bg, ytop)
    for o in order:
        if o == " ": pieces.append(None); continue
        if isinstance(o, tuple):
            p, ey0, ey1, ex0, ex1, k = extra[o[1]]
            ea = load(p); egl, _ = glyphs(ea, ey0, ey1, ex0, ex1); g = egl[k]
            crop = np.where(g["mask"], ea, 255)[g["y0"]-2:g["y1"]+2, g["x0"]-2:g["x1"]+2]
            h = capb - capt; s = h / (g["y1"] - g["y0"])
            im = Image.fromarray(crop.clip(0,255).astype(np.uint8)).resize((max(1,int(crop.shape[1]*s)), max(1,int(crop.shape[0]*s))), Image.LANCZOS)
            pieces.append((np.array(im).astype(np.float32), capt - 2)); continue
        g = gl[o]
        crop = np.where(g["mask"], a, 255)[g["y0"]-2:g["y1"]+2, g["x0"]-2:g["x1"]+2]
        pieces.append((crop, g["y0"] - 2))
    W = 0; xs = []
    for i, pc in enumerate(pieces):
        if pc is None: W += wg - g0; continue
        xs.append(W); W += pc[0].shape[1] - 4 + g0
    W -= g0
    top = min(pc[1] for pc in pieces if pc); bot = max(pc[1] + pc[0].shape[0] for pc in pieces if pc)
    strip = np.full((bot - top, W + 4), 255.0, np.float32)
    j = 0; cur = 0
    for pc in pieces:
        if pc is None: cur += wg - g0; continue
        h, w = pc[0].shape; yy = pc[1] - top
        strip[yy:yy + h, cur:cur + w] = np.minimum(strip[yy:yy + h, cur:cur + w], pc[0]); cur += w - 4 + g0
    # erase old glyphs
    old = np.zeros(a.shape, bool)
    for g in gl: old |= g["mask"]
    old = nd.binary_dilation(old, iterations=2)
    a2 = load(src); a2[old] = bg
    ox0 = min(g["x0"] for g in gl); ox1 = max(g["x1"] for g in gl)
    lim = maxw or max(ox1 - ox0, 1) * 1.06
    if strip.shape[1] > lim:
        s = lim / strip.shape[1]
        im = Image.fromarray(strip.clip(0,255).astype(np.uint8)).resize((int(strip.shape[1]*s), int(strip.shape[0]*s)), Image.LANCZOS)
        nt = top + int((strip.shape[0] - im.height) / 2); strip = np.array(im).astype(np.float32); top = nt
    cx = center if center is not None else (ox0 + ox1) / 2
    px = int(cx - strip.shape[1] / 2)
    h, w = strip.shape
    reg = a2[top:top + h, px:px + w]
    a2[top:top + h, px:px + w] = np.minimum(reg, np.where(strip > 250, 255, strip + (bg - 255)).clip(0, 255))
    Image.fromarray(a2.clip(0, 255).astype(np.uint8)).convert("RGB").save(dst)
    return gl

def show(p, out, bl, pad=4):
    a = Image.open(p).convert("RGB")
    cr = [a.crop((0, max(0, y0 - pad), a.width, min(a.height, y1 + pad))) for (y0, y1, *_ ) in bl]
    H = sum(c.height + 4 for c in cr); S = Image.new("RGB", (a.width, H), "red"); y = 0
    for c in cr: S.paste(c, (0, y)); y += c.height + 4
    S.save(out)

if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(p, bands(p))

def thin_clean(src, dst, y0, y1, w=6, x0=0, x1=None):
    """remove thin vertical hairlines (< w px wide) inside a caps band"""
    a = load(src); bg = bgval(a); x1 = a.shape[1] if x1 is None else x1
    sub = a[y0:y1, x0:x1]; m = sub < 215
    op = nd.binary_opening(m, structure=np.ones((1, w)))
    keep = nd.binary_dilation(op, iterations=2)
    rem = m & ~keep
    sub[rem] = bg; a[y0:y1, x0:x1] = sub
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGB").save(dst)
    return int(rem.sum())

def gap_close(src, dst, y0, y1, w=5, x0=0, x1=None):
    """fill thin white hairline gaps (< w px) between touching caps glyphs"""
    a = load(src); x1 = a.shape[1] if x1 is None else x1
    sub = a[y0:y1, x0:x1]; ink = sub < 128
    cl = nd.binary_closing(ink, structure=np.ones((1, w)))
    add = cl & ~ink; sub[add] = np.minimum(sub[add], 20); a[y0:y1, x0:x1] = sub
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGB").save(dst)
    return int(add.sum())
