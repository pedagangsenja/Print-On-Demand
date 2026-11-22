"""Jana bundle typography gaya lencana (teks -> path vektor).

Output: data/export/typography/bundle01/{svg,png}/NN-slug.{svg,png} + preview.png
PNG 4500x4500 latar lutsinar, 300 dpi. SVG: semua teks ditukar ke path (sedia Cricut).
Fon: assets/fonts/*.ttf (Google Fonts, SIL OFL 1.1 — boleh guna komersial).
"""
import io
from xml.sax.saxutils import escape
import math
import os

import cairosvg
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "assets", "fonts")
OUT = os.path.join(ROOT, "data", "export", "typography", "bundle01")
INK = "#111111"


def _f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Font:
    _cache = {}

    def __new__(cls, name):
        if name not in cls._cache:
            o = super().__new__(cls)
            path = os.path.join(FONT_DIR, name + ".ttf")
            o.tt = TTFont(path)
            o.gs = o.tt.getGlyphSet()
            o.order = o.tt.getGlyphOrder()
            o.upm = o.tt["head"].unitsPerEm
            with open(path, "rb") as fh:
                o.hbfont = hb.Font(hb.Face(hb.Blob(fh.read())))
            cls._cache[name] = o
        return cls._cache[name]

    def shape(self, text):
        """-> list of (glyphname, x_offset_units, y_offset_units, advance_units)."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": True, "calt": True})
        out = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((self.order[info.codepoint], pos.x_offset, pos.y_offset, pos.x_advance))
        return out


def bb_union(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


class Design:
    def __init__(self, slug, title):
        self.slug, self.title = slug, title
        self.parts = []  # (d, evenodd)
        self.bb = None

    def add(self, d, bb, evenodd=False):
        self.parts.append((d, evenodd))
        self.bb = bb_union(self.bb, bb)

    # ---------- teks ----------
    def _draw_run(self, font, glyphs, mats):
        sp = SVGPathPen(font.gs, ntos=_f)
        bp = BoundsPen(font.gs)
        for (g, *_), m in zip(glyphs, mats):
            font.gs[g].draw(TransformPen(sp, m))
            font.gs[g].draw(TransformPen(bp, m))
        return sp.getCommands(), bp.bounds

    def _line_mats(self, font, glyphs, size, x, y, track):
        s = size / font.upm
        mats, pen_x = [], x
        for g, xo, yo, adv in glyphs:
            mats.append((s, 0, 0, -s, pen_x + xo * s, y - yo * s))
            pen_x += adv * s + track * size
        return mats

    def measure(self, font, text, size=100, track=0):
        g = font.shape(text)
        _, bb = self._draw_run(font, g, self._line_mats(font, g, size, 0, 0, track))
        return bb

    def text(self, font, text, cx, top, width=None, size=None, track=0, x=None, fill=True):
        """Teks lurus, tengah pada cx (atau kiri pada x), bahagian atas dakwat = top. Pulang bbox."""
        font = Font(font)
        bb = self.measure(font, text, 100, track)
        k = (width / (bb[2] - bb[0])) if width else (size / 100)
        size = 100 * k
        ox = (x - bb[0] * k) if x is not None else (cx - (bb[0] + bb[2]) / 2 * k)
        oy = top - bb[1] * k
        g = font.shape(text)
        d, rb = self._draw_run(font, g, self._line_mats(font, g, size, ox, oy, track))
        if fill:
            self.add(d, rb)
        return rb if fill else (d, rb)

    def arc(self, font, text, cx, cy, r, size, track=0.04, bottom=False):
        """Teks melengkung di atas (top) atau bawah (bottom) bulatan berpusat (cx,cy). Garis dasar pada jejari r."""
        font = Font(font)
        g = font.shape(text)
        s = size / font.upm
        advs = [a * s + track * size for *_, a in g]
        total = sum(advs) - track * size
        a = -total / 2 / r
        mats = []
        for (gn, xo, yo, adv), w in zip(g, advs):
            gw = adv * s
            mid = a + gw / 2 / r
            if not bottom:
                th, px, py = mid, cx + r * math.sin(mid), cy - r * math.cos(mid)
            else:
                th, px, py = -mid, cx + r * math.sin(mid), cy + r * math.cos(mid)
            c, sn = math.cos(th), math.sin(th)
            ox = -gw / 2 + xo * s
            mats.append((c * s, sn * s, sn * s, -c * s, c * ox + px, sn * ox + py))
            a += w / r
        d, bb = self._draw_run(font, g, mats)
        self.add(d, bb)
        return bb

    def banner(self, font, text, cx, top, width, padx=0.08, pady=0.22, radius=0.12, track=0.02):
        """Bar hitam dengan teks tembus (knockout, evenodd)."""
        f = Font(font)
        bb = self.measure(f, text, 100, track)
        tw = width / (1 + 2 * padx)
        k = tw / (bb[2] - bb[0])
        th = (bb[3] - bb[1]) * k
        py = th * pady
        h = th + 2 * py
        d, _ = self.text(font, text, cx, top + py, width=tw, track=track, fill=False)
        rr = h * radius
        x0, x1 = cx - width / 2, cx + width / 2
        self.add(rrect(x0, top, x1, top + h, rr) + d, (x0, top, x1, top + h), evenodd=True)
        return (x0, top, x1, top + h)

    # ---------- hiasan ----------
    def sparkle(self, x, y, r):
        q = r * 0.12
        d = (f"M{_f(x)} {_f(y-r)}Q{_f(x+q)} {_f(y-q)} {_f(x+r)} {_f(y)}Q{_f(x+q)} {_f(y+q)} {_f(x)} {_f(y+r)}"
             f"Q{_f(x-q)} {_f(y+q)} {_f(x-r)} {_f(y)}Q{_f(x-q)} {_f(y-q)} {_f(x)} {_f(y-r)}Z")
        self.add(d, (x - r, y - r, x + r, y + r))

    def star(self, x, y, r, inner=0.45):
        pts = []
        for i in range(10):
            rad = r if i % 2 == 0 else r * inner
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((x + rad * math.cos(a), y + rad * math.sin(a)))
        self.add(poly(pts), (x - r, y - r, x + r, y + r))

    def dot(self, x, y, r):
        self.add(circle(x, y, r), (x - r, y - r, x + r, y + r))

    def heart(self, x, y, s):
        d = (f"M{_f(x)} {_f(y+s*0.9)}C{_f(x-s*1.2)} {_f(y+s*0.1)} {_f(x-s*0.9)} {_f(y-s*0.9)} {_f(x)} {_f(y-s*0.35)}"
             f"C{_f(x+s*0.9)} {_f(y-s*0.9)} {_f(x+s*1.2)} {_f(y+s*0.1)} {_f(x)} {_f(y+s*0.9)}Z")
        self.add(d, (x - s, y - s, x + s, y + s))

    def rule(self, x0, x1, y, t, dots=True):
        """Garisan mendatar (hujung bulat) + titik di hujung luar."""
        self.add(rrect(x0, y - t / 2, x1, y + t / 2, t / 2), (x0, y - t / 2, x1, y + t / 2))
        r = t * 1.1
        if dots in (True, "left"):
            self.dot(x0 - r * 2.6, y, r)
        if dots in (True, "right"):
            self.dot(x1 + r * 2.6, y, r)

    def side_rules(self, bb, gap, length, t, dots=True):
        y = (bb[1] + bb[3]) / 2
        self.rule(bb[0] - gap - length, bb[0] - gap, y, t, "left" if dots else False)
        self.rule(bb[2] + gap, bb[2] + gap + length, y, t, "right" if dots else False)

    def swash(self, x0, x1, y, amp, t):
        """Garis lengkung tirus (macam sapuan pen)."""
        n = 40
        top, bot = [], []
        for i in range(n + 1):
            u = i / n
            x = x0 + (x1 - x0) * u
            yy = y + amp * math.sin(u * math.pi * 2) * 0.5 - amp * math.sin(u * math.pi) * 0.3
            w = t * math.sin(u * math.pi) ** 0.8
            top.append((x, yy - w / 2))
            bot.append((x, yy + w / 2))
        self.add(poly(top + bot[::-1]), (x0, y - amp - t, x1, y + amp + t))

    def wave(self, x0, x1, y, amp, period, t):
        n = 120
        top, bot = [], []
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            yy = y + amp * math.sin((x - x0) / period * 2 * math.pi)
            top.append((x, yy - t / 2))
            bot.append((x, yy + t / 2))
        self.add(poly(top + bot[::-1]), (x0, y - amp - t, x1, y + amp + t))

    def ticks(self, x, y, side, size, t):
        """Tiga garis pancaran pendek (/ | \\) di sisi teks. side=-1 kiri, 1 kanan."""
        for ang in (-35, 0, 35):
            a = math.radians(ang)
            cxx = x + side * size * 0.55 * math.cos(a)
            cyy = y + size * 0.55 * math.sin(a)
            dx, dy = side * math.cos(a) * size * 0.25, math.sin(a) * size * 0.25
            self.add(capsule(cxx - dx, cyy - dy, cxx + dx, cyy + dy, t), (cxx - size * 0.3, cyy - size * 0.3, cxx + size * 0.3, cyy + size * 0.3))

    def frame(self, bb, pad, t, gap=None, radius=0):
        x0, y0, x1, y1 = bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad
        d = rrect(x0, y0, x1, y1, radius) + rrect(x0 + t, y0 + t, x1 - t, y1 - t, max(radius - t, 0))
        if gap:
            g = gap + t
            d += rrect(x0 + g, y0 + g, x1 - g, y1 - g, max(radius - g, 0))
            d += rrect(x0 + g + t * 0.5, y0 + g + t * 0.5, x1 - g - t * 0.5, y1 - g - t * 0.5, max(radius - g - t * 0.5, 0))
        self.add(d, (x0, y0, x1, y1), evenodd=True)

    def battery(self, cx, cy, w, level, t):
        h = w * 0.48
        x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2 - w * 0.08, cy + h / 2
        d = rrect(x0, y0, x1, y1, h * 0.18) + rrect(x0 + t, y0 + t, x1 - t, y1 - t, max(h * 0.18 - t, 0))
        g = t * 0.9
        d += rrect(x0 + t + g, y0 + t + g, x0 + t + g + (x1 - x0 - 2 * t - 2 * g) * level, y1 - t - g, t * 0.3)
        self.add(d, (x0, y0, x1, y1), evenodd=True)
        self.add(rrect(x1 + t * 0.3, cy - h * 0.2, cx + w / 2, cy + h * 0.2, t * 0.3), (x1, cy - h * 0.2, cx + w / 2, cy + h * 0.2))

    def mug(self, cx, cy, w, t):
        h = w * 1.0
        x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2 - w * 0.2, cy + h / 2
        d = rrect(x0, y0, x1, y1, w * 0.12)
        hcx, hcy, hr = x1, cy - h * 0.02, h * 0.24
        self.add(d, (x0, y0, x1, y1))
        self.add(circle(hcx, hcy, hr) + circle(hcx, hcy, hr - t * 1.4), (hcx - hr, hcy - hr, hcx + hr, hcy + hr), evenodd=True)
        for i, sx in enumerate((-0.22, 0.0, 0.22)):
            xx = (x0 + x1) / 2 + sx * w
            self.wave_v(xx, y0 - h * 0.62, y0 - h * 0.12, w * 0.05, h * 0.3, t * 0.8)

    def wave_v(self, x, y0, y1, amp, period, t):
        n = 40
        l, r = [], []
        for i in range(n + 1):
            y = y0 + (y1 - y0) * i / n
            xx = x + amp * math.sin((y - y0) / period * 2 * math.pi)
            w = t * min(1, math.sin(i / n * math.pi) * 2)
            l.append((xx - w / 2, y))
            r.append((xx + w / 2, y))
        self.add(poly(l + r[::-1]), (x - amp - t, y0, x + amp + t, y1))

    def bubble(self, cx, cy, w, t):
        h = w * 0.62
        x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
        tail = poly([(x0 + w * 0.18, y1 - 2), (x0 + w * 0.12, y1 + h * 0.32), (x0 + w * 0.42, y1 - 2)])
        d = rrect(x0, y0, x1, y1, h * 0.35)
        dots = "".join(circle(cx + dx * w * 0.24, cy, h * 0.11) for dx in (-1, 0, 1))
        self.add(d + dots, (x0, y0, x1, y1), evenodd=True)
        self.add(tail, (x0, y1, x0 + w * 0.42, y1 + h * 0.32))

    # ---------- output ----------
    def svg(self, size=1000, margin=0.04):
        x0, y0, x1, y1 = self.bb
        w, h = x1 - x0, y1 - y0
        k = size * (1 - 2 * margin) / max(w, h)
        tx = size / 2 - (x0 + w / 2) * k
        ty = size / 2 - (y0 + h / 2) * k
        paths = "".join(
            f'<path d="{d}"{" fill-rule=\"evenodd\"" if eo else ""}/>' for d, eo in self.parts
        )
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">'
                f'<title>{escape(self.title)}</title><g fill="{INK}" transform="translate({_f(tx)} {_f(ty)}) scale({k:.5f})">{paths}</g></svg>')


def rrect(x0, y0, x1, y1, r):
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
    if r <= 0:
        return f"M{_f(x0)} {_f(y0)}H{_f(x1)}V{_f(y1)}H{_f(x0)}Z"
    return (f"M{_f(x0+r)} {_f(y0)}H{_f(x1-r)}A{_f(r)} {_f(r)} 0 0 1 {_f(x1)} {_f(y0+r)}V{_f(y1-r)}"
            f"A{_f(r)} {_f(r)} 0 0 1 {_f(x1-r)} {_f(y1)}H{_f(x0+r)}A{_f(r)} {_f(r)} 0 0 1 {_f(x0)} {_f(y1-r)}"
            f"V{_f(y0+r)}A{_f(r)} {_f(r)} 0 0 1 {_f(x0+r)} {_f(y0)}Z")


def circle(x, y, r):
    return f"M{_f(x-r)} {_f(y)}A{_f(r)} {_f(r)} 0 1 0 {_f(x+r)} {_f(y)}A{_f(r)} {_f(r)} 0 1 0 {_f(x-r)} {_f(y)}Z"


def poly(pts):
    return "M" + "L".join(f"{_f(x)} {_f(y)}" for x, y in pts) + "Z"


def capsule(xa, ya, xb, yb, t):
    a = math.atan2(yb - ya, xb - xa)
    nx, ny = -math.sin(a) * t / 2, math.cos(a) * t / 2
    r = t / 2
    return (f"M{_f(xa+nx)} {_f(ya+ny)}L{_f(xb+nx)} {_f(yb+ny)}A{_f(r)} {_f(r)} 0 0 0 {_f(xb-nx)} {_f(yb-ny)}"
            f"L{_f(xa-nx)} {_f(ya-ny)}A{_f(r)} {_f(r)} 0 0 0 {_f(xa+nx)} {_f(ya+ny)}Z")


# ====================== REKA BENTUK ======================
def d01():
    D = Design("01-energy-saving-mode", "I'm Not Lazy, I'm in Energy Saving Mode")
    b = D.text("pacifico", "I'm in", 0, 0, width=190)
    D.side_rules(b, 25, 120, 9)
    b = D.text("anton", "ENERGY", 0, b[3] + 22, width=520, track=0.03)
    D.sparkle(b[0] - 55, b[1] + 40, 34); D.sparkle(b[2] + 55, b[3] - 40, 34)
    D.star(b[0] - 40, b[3] - 25, 13); D.star(b[2] + 42, b[1] + 22, 13)
    b = D.banner("anton", "SAVING", 0, b[3] + 22, 520, track=0.06)
    b = D.text("pacifico", "Mode", 0, b[3] + 14, width=360)
    D.battery(b[2] + 70, (b[1] + b[3]) / 2 + 10, 110, 0.15, 10)
    D.arc("anton", "I'M NOT LAZY", 0, -42 + 420, 420, 74, track=0.06)
    return D


def d02():
    D = Design("02-plans-with-my-couch", "Sorry I Can't, I Have Plans With My Couch")
    b = D.text("kaushan", "Sorry, I Can't", 0, 0, width=470)
    b = D.text("bebas", "I HAVE PLANS", 0, b[3] + 26, width=400, track=0.04)
    D.side_rules(b, 22, 70, 8)
    b = D.text("anton", "WITH MY", 0, b[3] + 22, width=200, track=0.08)
    D.sparkle(b[0] - 40, (b[1] + b[3]) / 2, 22); D.sparkle(b[2] + 40, (b[1] + b[3]) / 2, 22)
    b = D.text("pacifico", "Couch", 0, b[3] + 4, width=560)
    D.swash(b[0] + 40, b[2] - 10, b[3] + 22, 16, 13)
    D.star(b[0] - 20, b[1] + 30, 16); D.star(b[2] + 18, b[1] + 55, 12)
    return D


def d03():
    D = Design("03-patience-left-the-chat", "My Patience Has Officially Left the Chat")
    D.bubble(0, 0, 150, 10)
    b = D.text("lobster", "My Patience", 0, 80, width=470)
    b = D.text("bebas", "HAS OFFICIALLY", 0, b[3] + 22, width=330, track=0.06)
    D.side_rules(b, 20, 90, 7)
    b = D.text("luckiest", "LEFT", 0, b[3] + 22, width=420, track=0.04)
    D.ticks(b[0] - 20, (b[1] + b[3]) / 2, -1, 80, 10); D.ticks(b[2] + 20, (b[1] + b[3]) / 2, 1, 80, 10)
    b = D.text("yellowtail", "the chat", 0, b[3] + 8, width=360)
    D.sparkle(b[2] + 30, b[1] + 10, 18)
    return D


def d04():
    D = Design("04-mentally-on-vacation", "Mentally On Vacation, Physically Here")
    b = D.text("kaushan", "Mentally", 0, 0, width=420)
    D.sparkle(b[2] + 30, b[1] + 15, 26); D.star(b[2] + 5, b[1] + 70, 11)
    b = D.text("anton", "ON VACATION", 0, b[3] + 24, width=560, track=0.03)
    D.wave(b[0], b[2], b[3] + 30, 9, 70, 10)
    D.wave(b[0] + 60, b[2] - 60, b[3] + 58, 9, 70, 10)
    b = D.text("yellowtail", "physically", 0, b[3] + 82, width=300)
    b = D.text("luckiest", "HERE", 0, b[3] + 14, width=250, track=0.05)
    D.side_rules(b, 22, 90, 8)
    return D


def d05():
    D = Design("05-already-disturbed", "Do Not Disturb, I'm Already Disturbed")
    b = D.text("bebas", "I'M ALREADY", 0, 0, width=300, track=0.06)
    b2 = D.text("lobster", "Disturbed", 0, b[3] + 20, width=580)
    D.sparkle(b2[0] - 40, b2[1] + 20, 26); D.sparkle(b2[2] + 40, b2[3] - 30, 26)
    r = 430
    D.arc("anton", "DO NOT DISTURB", 0, -58 + r, r, 72, track=0.07)
    D.arc("bebas", "SERIOUSLY. GO AWAY.", 0, b2[3] + 48 + 52 - r, r, 52, track=0.1, bottom=True)
    return D


def d06():
    D = Design("06-allergic-to-mornings", "Allergic to Mornings & People")
    b = D.text("kaushan", "Allergic to", 0, 0, width=400)
    D.ticks(b[0] - 15, (b[1] + b[3]) / 2, -1, 70, 9); D.ticks(b[2] + 15, (b[1] + b[3]) / 2, 1, 70, 9)
    b = D.banner("anton", "MORNINGS", 0, b[3] + 26, 560, track=0.05)
    b = D.text("pacifico", "& People", 0, b[3] + 14, width=460)
    D.sparkle(b[0] - 30, b[1] + 20, 24); D.sparkle(b[2] + 30, b[3] - 25, 24)
    D.star(b[2] + 10, b[1] + 5, 11)
    return D


def d07():
    D = Design("07-nope-not-today", "Nope. Not Today. Maybe Never.")
    b = D.text("luckiest", "NOPE.", 0, 0, width=400, track=0.04)
    D.sparkle(b[2] + 40, b[1] + 15, 26)
    b = D.text("anton", "NOT TODAY", 0, b[3] + 26, width=440, track=0.05)
    D.side_rules(b, 22, 60, 8)
    b = D.text("yellowtail", "maybe", 0, b[3] + 12, width=250)
    b = D.text("alfa", "NEVER", 0, b[3] + 10, width=480, track=0.03)
    D.star(b[0] - 35, b[1] + 15, 15); D.star(b[2] + 35, b[3] - 15, 15)
    return D


def d08():
    D = Design("08-coffee-questionable-decisions", "Powered by Coffee & Questionable Decisions")
    b = D.text("pacifico", "Powered by", 0, 0, width=380)
    b = D.text("luckiest", "COFFEE", 0, b[3] + 20, width=540, track=0.04)
    D.mug(b[2] + 85, (b[1] + b[3]) / 2 + 20, 90, 9)
    D.sparkle(b[0] - 45, b[1] + 25, 22)
    b = D.text("kaushan", "& Questionable", 0, b[3] + 20, width=520)
    b = D.text("bebas", "DECISIONS", 0, b[3] + 22, width=420, track=0.08)
    D.side_rules(b, 20, 50, 7, dots=False)
    D.frame(D.bb, 45, 9, gap=10, radius=28)
    return D


def d09():
    D = Design("09-social-battery-low", "Social Battery 2%, Please Come Back Later")
    b = D.text("alfa", "2%", -70, 0, width=260)
    D.battery(b[2] + 30 + 75, (b[1] + b[3]) / 2, 150, 0.12, 12)
    top = b
    b = D.text("yellowtail", "please come back", 0, b[3] + 18, width=430)
    b = D.text("bebas", "LATER", 0, b[3] + 16, width=300, track=0.1)
    D.side_rules(b, 22, 70, 8)
    cy = (top[1] + b[3]) / 2
    D.arc("anton", "SOCIAL BATTERY", 0, cy + 30, 300, 64, track=0.07)
    D.sparkle(-300, cy - 120, 20); D.sparkle(300, cy - 120, 20)
    D.star(-285, cy + 140, 13); D.star(285, cy + 140, 13)
    return D


def d10():
    D = Design("10-told-there-would-be-snacks", "I Was Told There Would Be Snacks")
    b = D.text("lobster", "I Was Told", 0, 0, width=400)
    D.heart(b[2] + 30, b[1] + 25, 18)
    b = D.banner("anton", "THERE WOULD BE", 0, b[3] + 24, 540, track=0.05)
    b = D.text("pacifico", "Snacks", 0, b[3] + 10, width=540)
    D.swash(b[0] + 30, b[2] - 20, b[3] + 22, 16, 13)
    D.sparkle(b[0] - 35, b[1] + 35, 26); D.star(b[2] + 30, b[1] + 25, 15); D.star(b[2] + 5, b[1] + 80, 10)
    b = D.text("bebas", "AND THERE WERE NONE", 0, b[3] + 56, width=330, track=0.08)
    return D


DESIGNS = [d01, d02, d03, d04, d05, d06, d07, d08, d09, d10]


def main():
    os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "png"), exist_ok=True)
    thumbs = []
    for fn in DESIGNS:
        D = fn()
        svg = D.svg()
        with open(os.path.join(OUT, "svg", D.slug + ".svg"), "w") as fh:
            fh.write(svg)
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=4500, output_height=4500)
        im = Image.open(io.BytesIO(png))
        im.save(os.path.join(OUT, "png", D.slug + ".png"), dpi=(300, 300), optimize=True)
        thumbs.append(im.resize((600, 600), Image.LANCZOS))
        print("ok", D.slug)
    cols, cell, pad = 5, 600, 20
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGBA", (cols * cell + (cols + 1) * pad, rows * cell + (rows + 1) * pad), (243, 237, 228, 255))
    for i, t in enumerate(thumbs):
        x = pad + (i % cols) * (cell + pad)
        y = pad + (i // cols) * (cell + pad)
        sheet.alpha_composite(t, (x, y))
    sheet.convert("RGB").save(os.path.join(OUT, "preview.png"), optimize=True)


if __name__ == "__main__":
    main()
