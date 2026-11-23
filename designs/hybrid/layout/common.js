// Alat susun atur bersama. Kanvas 1350x1800 (CSS px); render.py tangkap pada DPR 4 = 5400x7200 (18x24 in @300 DPI).
const NS = 'http://www.w3.org/2000/svg', W = 1350, H = 1800;
let SVG, DEFS;
function el(tag, a, p) {
  const e = document.createElementNS(NS, tag);
  for (const k in a) e.setAttribute(k, a[k]);
  (p || SVG).appendChild(e);
  return e;
}
function initSvg() {
  SVG = document.getElementById('svg');
  for (const [k, v] of Object.entries({ viewBox: `0 0 ${W} ${H}`, width: W, height: H })) SVG.setAttribute(k, v);
  DEFS = el('defs', {});
}
const _c = document.createElement('canvas').getContext('2d');
const fstr = (f, s) => `${f.wt || 400} ${s}px "${f.fam}"`;
// Ukuran dakwat (ink) sebenar teks, bukan kotak fon.
function meas(t, f, s) {
  _c.font = fstr(f, s); _c.letterSpacing = ((f.ls || 0) * s) + 'px';
  const m = _c.measureText(t);
  return { L: m.actualBoundingBoxLeft, R: m.actualBoundingBoxRight, A: m.actualBoundingBoxAscent,
           D: m.actualBoundingBoxDescent, w: m.actualBoundingBoxLeft + m.actualBoundingBoxRight };
}
// Blok teks: saiz ikut lebar sasaran (w) atau saiz tetap (size); sy = regang menegak.
function block(t, f, o) {
  const s = o.size || 100 * o.w / meas(t, f, 100).w, sy = o.sy || 1, m = meas(t, f, s);
  return Object.assign({ kind: 'text', t, f, s, m, sy, h: (m.A + m.D) * sy, gap: 20 }, o);
}
// Lukis blok teks, pusat dakwat di cx, atas dakwat di top. Pulangkan {x0,x1,base} dalam koordinat kanvas.
function textEl(b, cx, top, attrs, parent, dx = 0, dy = 0) {
  const x = cx - (b.m.R - b.m.L) / 2 + dx, base = top + b.m.A * b.sy + dy;
  const e = el('text', Object.assign({ x: 0, y: 0, 'font-family': b.f.fam, 'font-weight': b.f.wt || 400,
    'font-size': b.s, 'letter-spacing': (b.f.ls || 0) * b.s, transform: `translate(${x} ${base}) scale(1 ${b.sy})` }, attrs), parent);
  e.textContent = b.t;
  return { e, x0: x - b.m.L, x1: x + b.m.R, base };
}
// Susun blok menegak, pusat dalam [top, bottom].
function stack(items, top, bottom) {
  const total = items.reduce((a, b, i) => a + b.h + (i < items.length - 1 ? b.gap : 0), 0);
  let y = top + ((bottom - top) - total) / 2;
  for (const it of items) { it.top = y; y += it.h + it.gap; }
  return total;
}
// Teks atas lengkung (pelangi). baseTop = garis dasar di puncak lengkung.
function arcBlock(t, f, s, R) {
  const m = meas(t, f, s), phi = (m.w / 2) / R, sag = R * (1 - Math.cos(phi));
  return { kind: 'arc', t, f, s, m, R, sag, h: m.A + m.D + sag, gap: 20 };
}
function arcEl(b, cx, top, attrs, parent) {
  const base = top + b.m.A, cy = base + b.R, a = Math.PI * 0.45, id = 'arc' + Math.round(top);
  const P = (t) => [cx + b.R * Math.sin(t), cy - b.R * Math.cos(t)];
  const [x0, y0] = P(-a), [x1, y1] = P(a);
  if (!document.getElementById(id)) el('path', { id, d: `M${x0},${y0} A${b.R},${b.R} 0 0 1 ${x1},${y1}`, fill: 'none' }, DEFS);
  const e = el('text', Object.assign({ 'font-family': b.f.fam, 'font-weight': b.f.wt || 400, 'font-size': b.s,
    'letter-spacing': (b.f.ls || 0) * b.s }, attrs), parent);
  const tp = el('textPath', { href: '#' + id, startOffset: b.R * a + (b.f.ls || 0) * b.s / 2, 'text-anchor': 'middle' }, e);
  tp.textContent = b.t;
  return e;
}
// Bentuk sabit (garis tirus) dari p0 ke p1, tebal t di tengah.
function taperD(p0, c1, c2, p1, t) {
  let nx = -(p1[1] - p0[1]), ny = p1[0] - p0[0]; const L = Math.hypot(nx, ny); nx = nx / L * t * 1.33; ny = ny / L * t * 1.33;
  return `M${p0} C${c1} ${c2} ${p1} C${c2[0] + nx},${c2[1] + ny} ${c1[0] + nx},${c1[1] + ny} ${p0} Z`;
}
// Reben berlipat: jalur tengah melengkung + ekor bertakuk di belakang.
function ribbonD(cx, cy, w, h, o = {}) {
  const bend = o.bend ?? 10, tail = o.tail ?? 0.34 * h * 2.2, d = o.drop ?? 0.32 * h, f = o.fold ?? 0.3 * h, notch = o.notch ?? 0.35 * h;
  const L = cx - w / 2, R = cx + w / 2, y1 = cy - h / 2, y2 = cy + h / 2;
  const band = `M${L},${y1} Q${cx},${y1 + bend * 2} ${R},${y1} L${R},${y2} Q${cx},${y2 + bend * 2} ${L},${y2} Z`;
  const tl = `M${L},${y1 + d} L${L - tail},${y1 + d} L${L - tail + notch},${(y1 + y2) / 2 + d} L${L - tail},${y2 + d} L${L + f},${y2 + d} L${L},${y2} Z`;
  const tr = `M${R},${y1 + d} L${R + tail},${y1 + d} L${R + tail - notch},${(y1 + y2) / 2 + d} L${R + tail},${y2 + d} L${R - f},${y2 + d} L${R},${y2} Z`;
  const folds = [`M${L},${y2} L${L + f},${y2 + d} L${L + f},${y2} Z`, `M${R},${y2} L${R - f},${y2 + d} L${R - f},${y2} Z`];
  return { band, tails: [tl, tr], folds, h: h + d, L, R, tail };
}
function star(cx, cy, r, n = 5, inner = 0.45) {
  let d = '';
  for (let i = 0; i < n * 2; i++) {
    const a = Math.PI * i / n - Math.PI / 2, rr = i % 2 ? r * inner : r;
    d += (i ? 'L' : 'M') + (cx + rr * Math.cos(a)).toFixed(1) + ',' + (cy + rr * Math.sin(a)).toFixed(1);
  }
  return d + 'Z';
}
async function loadFonts(list) {
  await Promise.all(list.map(f => document.fonts.load(fstr(f, 100), 'AaBb')));
  await document.fonts.ready;
}
