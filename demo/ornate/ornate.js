/* Enjin poster motivasi gaya vintage ornate (Victorian / Tuscan / sign-painter).
 * Semua grafik dijana kod (SVG) + Google Fonts SIL OFL. Tiada imej AI.
 * Dipakai oleh demo/ornate/index.html (pratonton) dan scripts/ornate_export.js (PNG cetak).
 * API: Ornate.ready(spec) -> Promise (muat fon); Ornate.render(spec, uid) -> rentetan SVG 1000x1500 (2:3). */
(function (root) {
  "use strict";
  const W = 1000, H = 1500;

  const STYLES = {
    saloon: { name: "Saloon (Tuscan barat)", arch: ["Rye", 400], l1: ["Sancreek", 400], l2: ["Rye", 400], amp: ["Berkshire Swash", 400], small: ["IM Fell English SC", 400], upper: true },
    royal: { name: "Royal (ukiran klasik)", arch: ["Cinzel Decorative", 700], l1: ["Playfair Display SC", 900], l2: ["Playfair Display SC", 900], amp: ["Pinyon Script", 400], small: ["Cinzel", 600], upper: true },
    circus: { name: "Circus (karnival Victorian)", arch: ["Diplomata SC", 400], l1: ["Holtwood One SC", 400], l2: ["Bevan", 400], amp: ["Berkshire Swash", 400], small: ["IM Fell English SC", 400], upper: true },
    gothic: { name: "Gothic (blackletter)", arch: ["Cinzel", 700], l1: ["UnifrakturMaguntia", 400], l2: ["UnifrakturMaguntia", 400], amp: ["Pirata One", 400], small: ["IM Fell English SC", 400], upper: false },
  };
  const GOLD = ["#FFF4C8", "#EDC765", "#B9852A", "#F6DC8E", "#8F611B"];
  const RED = ["#F7B29A", "#D9573F", "#A8301F", "#E8735A", "#7E2115"];
  const CREAM = ["#FFFBF0", "#F1E2C0", "#C9B184", "#F6EBD2", "#A08A62"];
  const COPPER = ["#FFE3CC", "#E7A06E", "#B0643A", "#F1BC92", "#7F4224"];
  const PALETTES = {
    noir_gold: { name: "Hitam & emas", bg: "#0E0C0A", bg2: "#221D15", m1: GOLD, m2: RED, orn: GOLD, outline: "#080604", extrude: "#4A2F0E", ink: "#EBD9A8", ribbon: ["#B53A28", "#7E2115"], ribbonInk: "#FBEFD0" },
    oxblood: { name: "Merah hati & emas", bg: "#3A0D12", bg2: "#521820", m1: GOLD, m2: CREAM, orn: GOLD, outline: "#170406", extrude: "#24070A", ink: "#F1E2C0", ribbon: ["#C9A04A", "#8F6A22"], ribbonInk: "#2A0A0D" },
    navy_brass: { name: "Biru malam & loyang", bg: "#0D1828", bg2: "#1A2B44", m1: GOLD, m2: RED, orn: GOLD, outline: "#050A12", extrude: "#3D2A10", ink: "#E9D7A6", ribbon: ["#A8392A", "#6E2016"], ribbonInk: "#FBEFD0" },
    forest: { name: "Hijau hutan & emas", bg: "#0E281D", bg2: "#1A3E2F", m1: GOLD, m2: CREAM, orn: GOLD, outline: "#04120C", extrude: "#3A2B0F", ink: "#EEDDB0", ribbon: ["#9E3326", "#6B1E15"], ribbonInk: "#FBEFD0" },
    teal_copper: { name: "Teal & tembaga", bg: "#0C2F31", bg2: "#174649", m1: COPPER, m2: CREAM, orn: COPPER, outline: "#041516", extrude: "#3B1E0E", ink: "#F3DCC4", ribbon: ["#B0643A", "#7F4224"], ribbonInk: "#FFF1E2" },
    cream_ink: { name: "Krim & dakwat (cerah)", light: true, bg: "#EFE2C2", bg2: "#E2CFA6", m1: ["#E06B5C", "#B33A2C", "#8E2A1F", "#C9473A", "#74201A"], m2: ["#5D7DA3", "#22395A", "#162842", "#2E4A70", "#0F1D33"], orn: ["#3A302A", "#2A2420", "#2A2420", "#3A302A", "#2A2420"], outline: "#1E1A16", extrude: "#1E1A16", ink: "#2A2420", ribbon: ["#22395A", "#162842"], ribbonInk: "#F4E8CC" },
  };
  const PATTERNS = { rays: "Sinar", lattice: "Kekisi berlian", grid: "Grid halus", none: "Tiada" };
  const MOTIFS = { mountains: "Gunung & matahari", laurel: "Daun laurel", stars: "Bintang", steps: "Tangga naik", none: "Tiada" };
  const PRESETS = [
    { name: "Grit & Grace", arch: "Rise with", l1: "Grit", amp: "&", l2: "Grace", ribbon: "Show up every single day", footer: "Est. 2026 · Daily Discipline", style: "saloon", palette: "noir_gold", pattern: "rays", motif: "mountains", seed: 11 },
    { name: "Make Today Count", arch: "Make", l1: "Today", amp: "", l2: "Count", ribbon: "One page at a time", footer: "The Morning Club", style: "royal", palette: "navy_brass", pattern: "lattice", motif: "stars", seed: 23 },
    { name: "Built Not Born", arch: "Strength is", l1: "Built", amp: "not", l2: "Born", ribbon: "Rep by rep · Day by day", footer: "Home Gym · Est. 2026", style: "circus", palette: "oxblood", pattern: "rays", motif: "steps", seed: 37 },
    { name: "Progress", arch: "Choose", l1: "Progress", amp: "over", l2: "Perfection", ribbon: "Small steps still count", footer: "Studio Rules No. 1", style: "royal", palette: "cream_ink", pattern: "grid", motif: "laurel", seed: 41 },
    { name: "Earn Your Crown", arch: "Earn", l1: "Your", amp: "", l2: "Crown", ribbon: "Quietly. Daily. Relentlessly.", footer: "Anno 2026", style: "gothic", palette: "forest", pattern: "lattice", motif: "laurel", seed: 53 },
    { name: "Do It Scared", arch: "Be brave and", l1: "Do It", amp: "", l2: "Scared", ribbon: "Courage is a habit", footer: "Brave Things Co.", style: "saloon", palette: "teal_copper", pattern: "rays", motif: "stars", seed: 67 },
    { name: "Discipline", arch: "Discipline", l1: "Beats", amp: "", l2: "Motivation", ribbon: "Do it on the hard days", footer: "Est. 2026 · No Excuses", style: "circus", palette: "noir_gold", pattern: "grid", motif: "steps", seed: 71 },
    { name: "Hustle & Heart", arch: "Lead with", l1: "Hustle", amp: "&", l2: "Heart", ribbon: "Work hard · Stay kind", footer: "The Office · Room 204", style: "saloon", palette: "oxblood", pattern: "rays", motif: "mountains", seed: 89 },
  ];
  const QUOTES = [
    { name: "Small Steps", arch: "", quote: "~Small steps every day\nadd up to\n#Big\n!Results", ribbon: "Keep showing up", footer: "Est. 2026 · Daily Progress", style: "royal", palette: "navy_brass", pattern: "lattice", motif: "steps", seed: 103 },
    { name: "Keep Climbing", arch: "", quote: "The view at the top\nbelongs to those who\n~kept\n#Climbing\nwhen it got hard", ribbon: "", footer: "Summit Club · No. 7", style: "saloon", palette: "noir_gold", pattern: "rays", motif: "mountains", seed: 117 },
    { name: "Strong & Brave", arch: "", quote: "Be the kind of\n!Strong\nthat makes\neveryone around you\n#Brave", ribbon: "", footer: "Home Gym · Est. 2026", style: "circus", palette: "oxblood", pattern: "rays", motif: "none", seed: 131 },
    { name: "Yesterday", arch: "", quote: "Your only\ncompetition is\nthe person you were\n#Yesterday", ribbon: "Beat your best", footer: "Anno 2026", style: "gothic", palette: "forest", pattern: "lattice", motif: "laurel", seed: 149 },
    { name: "Rise Eight", arch: "", quote: "Fall\n!Seven\ntimes\n~and\n#Rise Eight", ribbon: "Old Japanese proverb", footer: "Brave Things Co.", style: "saloon", palette: "teal_copper", pattern: "rays", motif: "stars", seed: 163 },
    { name: "Beginner", arch: "", quote: "Every expert\nyou admire today\nwas once a\n!Beginner\n~so keep going", ribbon: "", footer: "Studio Rules No. 2", style: "royal", palette: "cream_ink", pattern: "grid", motif: "laurel", seed: 179 },
    { name: "Something Good", arch: "", quote: "Not every day is good\nbut there is\n~something\n#Good\nin every day", ribbon: "", footer: "The Morning Club", style: "royal", palette: "oxblood", pattern: "lattice", motif: "stars", seed: 191 },
    { name: "Coffee & Chaos", arch: "", quote: "Fueled by\n#Coffee\n~courage\nand a little bit of\n!Chaos", ribbon: "", footer: "The Office · Room 204", style: "circus", palette: "noir_gold", pattern: "rays", motif: "none", seed: 211 },
  ];
  const FONT_URL = "https://fonts.googleapis.com/css2?family=Rye&family=Sancreek&family=Berkshire+Swash&family=IM+Fell+English+SC&family=Cinzel+Decorative:wght@700&family=Playfair+Display+SC:wght@900&family=Pinyon+Script&family=Cinzel:wght@600;700&family=Diplomata+SC&family=Holtwood+One+SC&family=Bevan&family=UnifrakturMaguntia&family=Pirata+One&display=swap";

  // ---------- utiliti ----------
  function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const f1 = v => Math.round(v * 10) / 10;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function lum(h) { const v = h.replace("#", ""); return [0, 2, 4].map(i => parseInt(v.substr(i, 2), 16) / 255).map(c => c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)).reduce((s, c, i) => s + c * [0.2126, 0.7152, 0.0722][i], 0); }
  function contrast(a, b) { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }

  let ctx = null;
  function measure(text, f, size, ls) {
    if (!ctx) ctx = document.createElement("canvas").getContext("2d");
    ctx.font = `${f[1]} ${size}px "${f[0]}"`;
    return ctx.measureText(text).width + ls * size * Math.max(0, [...text].length - 1);
  }
  const fit = (text, f, maxW, maxS, ls) => Math.min(maxS, maxW / (measure(text, f, 100, ls) / 100));
  const fa = (f, size, ls) => `font-family="'${f[0]}',serif" font-weight="${f[1]}" font-size="${f1(size)}" letter-spacing="${f1(ls * size)}"`;

  // teks berlapis: bayang, extrude 3D, garis luar gelap, (garis emas), isi logam, kilauan
  function layered(content, attrs, size, P, id, accent) {
    const ow = size * 0.09, dx = size * 0.006, dy = size * 0.009, o = [];
    const T = (x, tr) => `<text ${attrs} ${x}${tr ? ` transform="translate(${f1(tr[0])} ${f1(tr[1])})"` : ""}>${content}</text>`;
    o.push(T(`fill="#000" stroke="#000" stroke-width="${f1(ow)}" stroke-linejoin="round" opacity="${P.light ? 0.22 : 0.6}" filter="url(#${id}bl)"`, [size * 0.03, size * 0.05]));
    for (let i = 6; i >= 1; i--) o.push(T(`fill="${P.extrude}" stroke="${P.extrude}" stroke-width="${f1(ow)}" stroke-linejoin="round"`, [dx * i, dy * i]));
    o.push(T(`fill="none" stroke="${P.outline}" stroke-width="${f1(ow)}" stroke-linejoin="round"`));
    if (accent) o.push(T(`fill="none" stroke="url(#${id}orn)" stroke-width="${f1(ow * 0.42)}" stroke-linejoin="round"`));
    o.push(T(`fill="url(#${id}${accent ? "m2" : "m1"})"`));
    o.push(T(`fill="none" stroke="#FFFFFF" stroke-opacity="${P.light ? 0.3 : 0.45}" stroke-width="${f1(Math.max(1, size * 0.007))}"`, [-size * 0.004, -size * 0.006]));
    return o.join("");
  }

  // teks kecil: bayang + garis luar + isi logam (tanpa extrude)
  function lite(content, attrs, size, P, id) {
    const ow = Math.max(3, size * 0.14);
    return `<text ${attrs} fill="#000" stroke="#000" stroke-width="${f1(ow)}" stroke-linejoin="round" opacity="${P.light ? 0.2 : 0.55}" filter="url(#${id}bl)" transform="translate(2 4)">${content}</text>` +
      `<text ${attrs} fill="none" stroke="${P.outline}" stroke-width="${f1(ow)}" stroke-linejoin="round">${content}</text><text ${attrs} fill="url(#${id}m1)">${content}</text>`;
  }
  // ayat panjang: satu baris = satu ayat pendek. Penanda: # tajuk besar, ! tajuk aksen, ~ skrip, tiada = huruf kecil.
  // Tanpa penanda: baris satu perkataan jadi tajuk besar. Baris boleh dipisah dengan Enter atau " / ".
  function parseQuote(q) {
    const L = String(q || "").split(/\n|\s+\/\s+/).map(x => x.trim()).filter(Boolean);
    const marked = L.some(x => /^[#!~]/.test(x));
    return L.map(x => {
      const m = x[0], k = m === "#" ? "big" : m === "!" ? "acc" : m === "~" ? "script" : (!marked && !/\s/.test(x) ? "big" : "small");
      return { k, t: /^[#!~]/.test(x) ? x.slice(1).trim() : x };
    }).filter(q => q.t);
  }

  // ---------- ornamen ----------
  function spiral(cx, cy, r0, a0, turns, rot) {
    const p = [], n = Math.max(16, Math.round(turns * 40));
    for (let i = 0; i <= n; i++) { const t = i / n, a = a0 + rot * t * turns * 2 * Math.PI, r = r0 * (1 - 0.82 * t); p.push(f1(cx + r * Math.cos(a)) + " " + f1(cy + r * Math.sin(a))); }
    return p.join("L");
  }
  function bez(t, a, b, c, d) { const u = 1 - t; return u * u * u * a + 3 * u * u * t * b + 3 * u * t * t * c + t * t * t * d; }
  // batang mendatar bergelombang -> gulungan; vy=1 gulung ke bawah, -1 ke atas; spur = cabang kecil
  function scroll(x, y, len, dir, r, vy, spur) {
    const amp = r * 0.7, ex = x + dir * len;
    const c1x = x + dir * len * 0.3, c1y = y - vy * amp, c2x = ex - dir * len * 0.3, c2y = y + vy * amp * 0.3;
    let d = `M${f1(x)} ${f1(y)}C${f1(c1x)} ${f1(c1y)} ${f1(c2x)} ${f1(c2y)} ${f1(ex)} ${f1(y)}L` + spiral(ex, y + vy * r, r, vy > 0 ? -Math.PI / 2 : Math.PI / 2, 1.3, dir * vy);
    let leaf = "";
    if (spur && len > 60) {
      const t = 0.42, bx = bez(t, x, c1x, c2x, ex), by = bez(t, y, c1y, c2y, y);
      d += " " + scroll(bx, by, len * 0.28, dir, r * 0.5, -vy, false).d;
      const t2 = 0.72, lx = bez(t2, x, c1x, c2x, ex), ly = bez(t2, y, c1y, c2y, y);
      leaf = leafPath(lx, ly, dir > 0 ? (vy > 0 ? -50 : 50) : (vy > 0 ? -130 : 130), r * 1.5, r * 0.5);
    }
    return { d, leaf };
  }
  function leafPath(x, y, ang, L, w) {
    const a = ang * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
    const P = (u, v) => f1(x + u * c - v * s) + " " + f1(y + u * s + v * c);
    return `M${P(0, 0)}Q${P(L * 0.5, -w)} ${P(L, 0)}Q${P(L * 0.5, w)} ${P(0, 0)}Z`;
  }
  const star4 = (x, y, r, k = 0.16) => `M${f1(x)} ${f1(y - r)}L${f1(x + r * k)} ${f1(y - r * k)}L${f1(x + r)} ${f1(y)}L${f1(x + r * k)} ${f1(y + r * k)}L${f1(x)} ${f1(y + r)}L${f1(x - r * k)} ${f1(y + r * k)}L${f1(x - r)} ${f1(y)}L${f1(x - r * k)} ${f1(y - r * k)}Z`;
  const diamond = (x, y, r) => `M${f1(x)} ${f1(y - r)}L${f1(x + r * 0.7)} ${f1(y)}L${f1(x)} ${f1(y + r)}L${f1(x - r * 0.7)} ${f1(y)}Z`;

  function stroke(id, w) { return `fill="none" stroke="url(#${id}orn)" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"`; }
  function scrollSVG(s, id, w) { return `<path d="${s.d}" ${stroke(id, w)}/>` + (s.leaf ? `<path d="${s.leaf}" fill="url(#${id}orn)"/>` : ""); }

  function corner(id, R) {
    const a = scroll(34, 10, 140 + R() * 40, 1, 15, 1, true), b = scroll(34, 30, 70, 1, 9, -1, false);
    const g = scrollSVG(a, id, 3) + scrollSVG(b, id, 2);
    return g + `<g transform="matrix(0 1 1 0 0 0)">${g}</g>` +
      `<path d="${diamond(16, 16, 12)}" fill="url(#${id}orn)" transform="rotate(-45 16 16)"/>` +
      `<path d="${leafPath(30, 30, 45, 34, 9)}" fill="url(#${id}orn)"/>`;
  }
  function topOrnament(id, y, big) {
    const s = big ? 1 : 0.7;
    const L = scroll(470, y + 22 * s, 170 * s, -1, 17 * s, 1, true), Rr = scroll(530, y + 22 * s, 170 * s, 1, 17 * s, 1, true);
    const L2 = scroll(480, y + 4 * s, 90 * s, -1, 10 * s, -1, false), R2 = scroll(520, y + 4 * s, 90 * s, 1, 10 * s, -1, false);
    let o = scrollSVG(L, id, 3) + scrollSVG(Rr, id, 3) + scrollSVG(L2, id, 2) + scrollSVG(R2, id, 2);
    if (big) {
      o += `<circle cx="500" cy="${y + 10}" r="70" fill="url(#${id}glow2)"/>`;
      o += `<path d="${star4(500, y + 10, 58)}" fill="url(#${id}orn)"/><path d="${star4(500, y + 10, 26)}" fill="url(#${id}orn)" transform="rotate(45 500 ${y + 10})"/>`;
      o += `<path d="${leafPath(500, y + 50, 90, 46, 11)}" fill="url(#${id}orn)"/>`;
    } else {
      o += `<path d="${diamond(500, y + 10, 16)}" fill="url(#${id}orn)"/>`;
    }
    return o;
  }
  function frame(id, R) {
    const notch = R() < 0.5, i = 62, r = 34;
    let o = `<rect x="26" y="26" width="${W - 52}" height="${H - 52}" fill="none" stroke="url(#${id}orn)" stroke-width="6"/>` +
      `<rect x="40" y="40" width="${W - 80}" height="${H - 80}" fill="none" stroke="url(#${id}orn)" stroke-width="1.5"/>` +
      `<rect x="50" y="50" width="${W - 100}" height="${H - 100}" fill="none" stroke="url(#${id}orn)" stroke-width="2.4" stroke-dasharray="0.1 10" stroke-linecap="round"/>`;
    if (notch) o += `<path d="M${i + r} ${i}H${W - i - r}A${r} ${r} 0 0 0 ${W - i} ${i + r}V${H - i - r}A${r} ${r} 0 0 0 ${W - i - r} ${H - i}H${i + r}A${r} ${r} 0 0 0 ${i} ${H - i - r}V${i + r}A${r} ${r} 0 0 0 ${i + r} ${i}Z" ${stroke(id, 1.6)}/>`;
    else o += `<rect x="${i}" y="${i}" width="${W - 2 * i}" height="${H - 2 * i}" ${stroke(id, 1.6)}/>`;
    const c = corner(id, R);
    o += `<g transform="translate(${i} ${i})">${c}</g><g transform="translate(${W - i} ${i}) scale(-1 1)">${c}</g>` +
      `<g transform="translate(${i} ${H - i}) scale(1 -1)">${c}</g><g transform="translate(${W - i} ${H - i}) scale(-1 -1)">${c}</g>`;
    o += topOrnament(id, 78, true);
    o += `<g transform="translate(0 ${H}) scale(1 -1)">${topOrnament(id, 70, false)}</g>`;
    return o;
  }

  // ---------- latar & motif ----------
  function pattern(kind, P, id, R) {
    if (kind === "rays") {
      const k = 2 * (20 + Math.floor(R() * 8)), cx = 500, cy = 640, L = 1700; let d = "";
      for (let i = 0; i < k; i += 2) { const a0 = 2 * Math.PI * i / k, a1 = 2 * Math.PI * (i + 1) / k; d += `M${cx} ${cy}L${f1(cx + L * Math.cos(a0))} ${f1(cy + L * Math.sin(a0))}L${f1(cx + L * Math.cos(a1))} ${f1(cy + L * Math.sin(a1))}Z`; }
      return `<path d="${d}" fill="${P.bg2}" opacity="${P.light ? 0.55 : 0.7}"/>`;
    }
    if (kind === "lattice") return `<defs><pattern id="${id}lat" width="56" height="56" patternUnits="userSpaceOnUse"><path d="M28 2L54 28L28 54L2 28Z" fill="none" stroke="${P.bg2}" stroke-width="2"/><circle cx="28" cy="28" r="3" fill="${P.bg2}"/></pattern></defs><rect width="${W}" height="${H}" fill="url(#${id}lat)"/>`;
    if (kind === "grid") return `<defs><pattern id="${id}grd" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="${P.bg2}" stroke-width="1.4"/></pattern></defs><rect width="${W}" height="${H}" fill="url(#${id}grd)"/>`;
    return "";
  }
  function motif(kind, P, id, R) {
    if (kind === "mountains") {
      let s = `<circle cx="500" cy="1170" r="190" fill="url(#${id}m1)" opacity="${P.light ? 0.35 : 0.28}"/>`;
      for (let i = 0; i <= 16; i++) { const a = Math.PI + Math.PI * i / 16; s += `<line x1="${f1(500 + 215 * Math.cos(a))}" y1="${f1(1170 + 215 * Math.sin(a))}" x2="${f1(500 + 285 * Math.cos(a))}" y2="${f1(1170 + 285 * Math.sin(a))}" ${stroke(id, 4)} opacity=".45"/>`; }
      const range = (y0, amp, step) => { const pts = [[40, y0 + amp]]; let x = 40, up = true; while (x < 960) { x += step * (0.7 + R() * 0.6); pts.push([Math.min(960, x), up ? y0 - R() * amp : y0 + amp * (0.4 + R() * 0.5)]); up = !up; } return pts; };
      const back = range(1110, 90, 110), front = range(1200, 60, 90);
      const poly = (pts, fill) => `<path d="M${pts.map(p => f1(p[0]) + " " + f1(p[1])).join("L")}L960 1470L40 1470Z" fill="${fill}"/>`;
      s += poly(back, P.bg2);
      back.forEach((p, i) => { if (i % 2 && i < back.length - 1) s += `<path d="M${f1(p[0] - 34)} ${f1(p[1] + 30)}L${f1(p[0])} ${f1(p[1])}L${f1(p[0] + 30)} ${f1(p[1] + 26)}" ${stroke(id, 3)} opacity=".8"/>`; });
      s += poly(front, P.outline);
      return s;
    }
    if (kind === "laurel") {
      let g = "", cx = 500, cy = 700, Rr = 420;
      const pt = a => [cx + Rr * Math.cos(a), cy + Rr * Math.sin(a)];
      const a0 = 100 * Math.PI / 180, a1 = 238 * Math.PI / 180;
      const p0 = pt(a0), p1 = pt(a1);
      g += `<path d="M${f1(p0[0])} ${f1(p0[1])}A${Rr} ${Rr} 0 0 1 ${f1(p1[0])} ${f1(p1[1])}" ${stroke(id, 4)}/>`;
      for (let a = a0 + 0.07; a < a1; a += 0.12) {
        const p = pt(a), tang = a * 180 / Math.PI + 90, sz = 44 + 16 * Math.sin((a - a0) / (a1 - a0) * Math.PI);
        g += `<path d="${leafPath(p[0], p[1], tang + 35, sz, sz * 0.4)}" fill="url(#${id}orn)"/><path d="${leafPath(p[0], p[1], tang + 145, sz, sz * 0.4)}" fill="url(#${id}orn)"/>`;
      }
      return `<g opacity="${P.light ? 0.45 : 0.5}">${g}<g transform="translate(${W} 0) scale(-1 1)">${g}</g></g>`;
    }
    if (kind === "stars") {
      let s = "";
      for (let i = 0; i < 70; i++) { const x = 80 + R() * 840, y = 90 + R() * 1320, r = 2 + R() * R() * 12; s += `<path d="${star4(x, y, r, 0.22)}" fill="url(#${id}orn)" opacity="${f1(0.25 + R() * 0.6)}"/>`; }
      for (let i = 0; i < 5; i++) { const x = 110 + R() * 780, y = 160 + R() * 1150; s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="40" fill="url(#${id}glow2)"/><path d="${star4(x, y, 22 + R() * 14)}" fill="url(#${id}orn)"/>`; }
      return s;
    }
    if (kind === "steps") {
      let s = "", n = 11, top = [];
      for (let i = 0; i < n; i++) {
        const x = 100 + i * 74, h = 50 + i * 26 + R() * 40, y = 1300 - h;
        top.push([x + 24, y - 14]);
        s += `<rect x="${x}" y="${f1(y)}" width="48" height="${f1(h)}" fill="${P.bg2}" stroke="url(#${id}orn)" stroke-width="2" opacity=".85"/>`;
        s += `<line x1="${x + 24}" y1="${f1(y - 30)}" x2="${x + 24}" y2="${f1(y)}" ${stroke(id, 3)} opacity=".8"/>`;
      }
      const e = top[n - 1];
      s += `<path d="M${top.map(p => f1(p[0]) + " " + f1(p[1] - 20)).join("L")}" fill="none" stroke="url(#${id}m2)" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>`;
      s += `<path d="M${f1(e[0] - 30)} ${f1(e[1] - 30)}L${f1(e[0] + 22)} ${f1(e[1] - 52)}L${f1(e[0] - 2)} ${f1(e[1] + 2)}Z" fill="url(#${id}m2)"/>`;
      return `<g opacity="${P.light ? 0.6 : 0.75}">${s}</g>`;
    }
    return "";
  }

  // ---------- reben & plak ----------
  function ribbon(y, text, f, P, id) {
    const x0 = 165, x1 = 835, h = 92, c = 28, fs = fit(text, f, 560, 46, 0.08);
    const tail = (s) => `<g transform="${s}"><path d="M${x0 + 34} ${y + 26}H${x0 - 72}L${x0 - 38} ${y + 26 + h / 2}L${x0 - 72} ${y + 26 + h}H${x0 + 34}Z" fill="${P.ribbon[1]}" stroke="url(#${id}orn)" stroke-width="2.5" stroke-linejoin="round"/><path d="M${x0} ${y + h}L${x0 + 34} ${y + h + 26}V${y + h - 6}Z" fill="${P.outline}"/></g>`;
    let o = tail("") + tail(`translate(${W} 0) scale(-1 1)`);
    o += `<path d="M${x0} ${y}Q500 ${y - c} ${x1} ${y}V${y + h}Q500 ${y + h - c} ${x0} ${y + h}Z" fill="url(#${id}rb)" stroke="url(#${id}orn)" stroke-width="3"/>`;
    o += `<path d="M${x0 + 6} ${y + 9}Q500 ${y + 9 - c} ${x1 - 6} ${y + 9}M${x0 + 6} ${y + h - 9}Q500 ${y + h - 9 - c} ${x1 - 6} ${y + h - 9}" ${stroke(id, 1.2)} opacity=".8"/>`;
    const by = y + h / 2 + fs * 0.34;
    o += `<path id="${id}rbp" d="M${x0 + 10} ${f1(by)}Q500 ${f1(by - c)} ${x1 - 10} ${f1(by)}" fill="none"/>`;
    o += `<text ${fa(f, fs, 0.08)} text-anchor="middle" fill="${P.ribbonInk}"><textPath href="#${id}rbp" startOffset="50%">${esc(text)}</textPath></text>`;
    return o;
  }
  function plaque(cy, text, f, P, id) {
    const fs = fit(text, f, 480, 32, 0.12), tw = measure(text, f, fs, 0.12), pw = Math.min(620, tw + 110), hh = 33, x0 = 500 - pw / 2, x1 = 500 + pw / 2, k = 14;
    let o = `<line x1="120" y1="${cy}" x2="${f1(x0 - 22)}" y2="${cy}" ${stroke(id, 2)}/><line x1="${f1(x1 + 22)}" y1="${cy}" x2="880" y2="${cy}" ${stroke(id, 2)}/>`;
    o += `<path d="${diamond(x0 - 14, cy, 10)}" fill="url(#${id}orn)"/><path d="${diamond(x1 + 14, cy, 10)}" fill="url(#${id}orn)"/>`;
    const box = (m) => `M${f1(x0 + k + m)} ${cy - hh + m}H${f1(x1 - k - m)}L${f1(x1 - m)} ${cy}L${f1(x1 - k - m)} ${cy + hh - m}H${f1(x0 + k + m)}L${f1(x0 + m)} ${cy}Z`;
    o += `<path d="${box(0)}" fill="${P.outline}" stroke="url(#${id}orn)" stroke-width="3"/><path d="${box(6)}" ${stroke(id, 1)}/>`;
    o += `<text x="500" y="${f1(cy + fs * 0.34)}" ${fa(f, fs, 0.12)} text-anchor="middle" fill="url(#${id}m1)">${esc(text)}</text>`;
    return o;
  }

  // ---------- susun atur ----------
  function render(spec, uid) {
    const S = STYLES[spec.style] || STYLES.saloon, P = PALETTES[spec.palette] || PALETTES.noir_gold;
    const R = rng(spec.seed || 1), id = "o" + (uid || Math.random().toString(36).slice(2, 8));
    const up = t => (S.upper ? String(t || "").toUpperCase() : String(t || "")).trim();
    const arch = up(spec.arch), l1 = up(spec.l1), l2 = up(spec.l2), amp = String(spec.amp || "").trim(), rib = String(spec.ribbon || "").trim(), foot = String(spec.footer || "").trim();
    const CAP = 0.73, GAP = parseQuote(spec.quote).length ? 14 : 26;

    // ukur blok
    const blocks = [];
    if (arch) { const s = fit(arch, S.arch, 600, 104, 0.06); blocks.push({ k: "arch", s, h: s * CAP + 40 }); }
    const Q = parseQuote(spec.quote);
    for (const q of Q) {  // mod ayat panjang: setiap baris dimuatkan ke lebar penuh
      if (q.k === "small") { const s = fit(q.t, S.small, 700, 64, 0.08); blocks.push({ k: "q", m: "small", t: q.t, f: S.small, s, h: s * 0.78 }); continue; }
      if (q.k === "script") { const s = fit(q.t, S.amp, 640, 128, 0); blocks.push({ k: "q", m: "script", t: q.t, f: S.amp, s, h: s * 0.82 }); continue; }
      const t = up(q.t), f = q.k === "acc" ? S.l1 : S.l2, s = fit(t, f, 780, 230, 0.01), desc = !S.upper && /[gjpqy]/.test(t) ? 0.2 : 0;
      blocks.push({ k: "q", m: "head", acc: q.k === "acc", t, f, s, h: s * (CAP + desc) });
    }
    for (const [k, t] of (Q.length ? [] : [["l1", l1], ["amp", amp], ["l2", l2]])) {
      if (!t) continue;
      if (k === "amp") { const f = S.amp, s = t.length <= 2 ? 170 : fit(t, f, 420, 120, 0.02); blocks.push({ k, t, f, s, h: s * (t.length <= 2 ? 0.72 : 0.6) }); continue; }
      const f = S[k], s = fit(t, f, 780, 290, 0.01), desc = !S.upper && /[gjpqy]/.test(t) ? 0.2 : 0;
      blocks.push({ k, t, f, s, h: s * (CAP + desc) });
    }
    if (rib) blocks.push({ k: "rib", h: 92 });
    const top = 190, bottom = foot ? 1272 : 1330, avail = bottom - top;
    let total = blocks.reduce((a, b) => a + b.h, 0) + GAP * (blocks.length - 1);
    if (total > avail) { const sc = (avail - GAP * (blocks.length - 1)) / (total - GAP * (blocks.length - 1)); blocks.forEach(b => { if (b.k !== "rib") { b.s *= sc; b.h *= sc; } }); total = avail; }
    const gaps = Math.max(1, blocks.length - 1), extra = Math.max(0, avail - total), g2 = Math.min(extra / (gaps + 2), 64);
    let y = top + (avail - total - g2 * gaps) / 2;

    const defs = [];
    const grad = (gid, st, attrs) => `<linearGradient id="${id}${gid}" ${attrs}>${st.map(([o, c]) => `<stop offset="${o}" stop-color="${c}"/>`).join("")}</linearGradient>`;
    const band = m => [[0, m[0]], [0.38, m[1]], [0.5, m[2]], [0.56, m[3]], [1, m[4]]];
    defs.push(grad("m1", band(P.m1), 'x1="0" y1="0" x2="0" y2="1"'), grad("m2", band(P.m2), 'x1="0" y1="0" x2="0" y2="1"'));
    defs.push(grad("orn", [[0, P.orn[1]], [0.22, P.orn[0]], [0.45, P.orn[2]], [0.7, P.orn[3]], [1, P.orn[1]]], `gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="${W}" y2="${H}"`));
    defs.push(grad("rb", [[0, P.ribbon[0]], [1, P.ribbon[1]]], 'x1="0" y1="0" x2="0" y2="1"'));
    defs.push(`<radialGradient id="${id}glow" cx="500" cy="640" r="620" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="${P.m1[2]}" stop-opacity="${P.light ? 0.18 : 0.28}"/><stop offset="1" stop-color="${P.m1[2]}" stop-opacity="0"/></radialGradient>`);
    defs.push(`<radialGradient id="${id}glow2"><stop offset="0" stop-color="${P.m1[0]}" stop-opacity=".7"/><stop offset="1" stop-color="${P.m1[0]}" stop-opacity="0"/></radialGradient>`);
    defs.push(`<radialGradient id="${id}vig" cx=".5" cy=".45" r=".78"><stop offset=".55" stop-color="${P.light ? "#4A2E12" : "#000"}" stop-opacity="0"/><stop offset="1" stop-color="${P.light ? "#4A2E12" : "#000"}" stop-opacity="${P.light ? 0.45 : 0.75}"/></radialGradient>`);
    defs.push(`<filter id="${id}bl" x="-10%" y="-20%" width="120%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>`);
    defs.push(`<filter id="${id}gr"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="${(spec.seed || 1) % 97}"/><feColorMatrix type="saturate" values="0"/></filter>`);
    defs.push(`<clipPath id="${id}cl"><rect x="44" y="44" width="${W - 88}" height="${H - 88}"/></clipPath>`);

    const body = [];
    for (const b of blocks) {
      if (b.k === "arch") {
        const w = measure(arch, S.arch, b.s, 0.06), Rr = 760, th = (w * 1.18 / 2) / Rr, sag = Rr * (1 - Math.cos(th));
        const yMid = y + b.s * CAP + 8, x1 = 500 - Rr * Math.sin(th), x2 = 500 + Rr * Math.sin(th);
        defs.push(`<path id="${id}arc" d="M${f1(x1)} ${f1(yMid + sag)}A${Rr} ${Rr} 0 0 1 ${f1(x2)} ${f1(yMid + sag)}"/>`);
        body.push(layered(`<textPath href="#${id}arc" startOffset="50%">${esc(arch)}</textPath>`, `${fa(S.arch, b.s, 0.06)} text-anchor="middle"`, b.s, P, id, false));
        y += b.h + GAP + g2; continue;
      }
      if (b.k === "rib") { body.push(ribbon(y + 14, rib, S.small, P, id)); y += b.h + GAP + g2; continue; }
      const base = y + (b.k === "amp" ? b.h * 0.95 : b.m === "small" ? b.s * 0.72 : b.m === "script" ? b.s * 0.66 : b.s * CAP);
      if (b.m === "small") {
        body.push(lite(esc(b.t), `x="500" y="${f1(base)}" ${fa(b.f, b.s, 0.08)} text-anchor="middle"`, b.s, P, id));
      } else if (b.m === "script") {
        body.push(layered(esc(b.t), `x="500" y="${f1(base)}" ${fa(b.f, b.s, 0)} text-anchor="middle"`, b.s, P, id, false));
      } else if (b.k === "amp") {
        const aw = measure(b.t, b.f, b.s, 0.02), cy = base - b.s * 0.3;
        body.push(`<line x1="${f1(500 - aw / 2 - 30)}" y1="${f1(cy)}" x2="190" y2="${f1(cy)}" ${stroke(id, 2.5)}/><line x1="${f1(500 + aw / 2 + 30)}" y1="${f1(cy)}" x2="810" y2="${f1(cy)}" ${stroke(id, 2.5)}/>`);
        body.push(`<path d="${diamond(180, cy, 11)}" fill="url(#${id}orn)"/><path d="${diamond(820, cy, 11)}" fill="url(#${id}orn)"/>`);
        body.push(scrollSVG(scroll(170, cy, 60, -1, 10, 1, false), id, 2.5) + scrollSVG(scroll(830, cy, 60, 1, 10, 1, false), id, 2.5));
        body.push(layered(esc(b.t), `x="500" y="${f1(base)}" ${fa(b.f, b.s, 0.02)} text-anchor="middle"`, b.s, P, id, false));
      } else {
        const w = measure(b.t, b.f, b.s, 0.01), space = (W - 2 * 70 - w) / 2, cy = base - b.s * CAP * 0.5;
        if (space > 70) {
          const len = Math.min(space - 26, 150), xl = 500 - w / 2 - 18, xr = 500 + w / 2 + 18, rr = Math.min(18, len / 6);
          body.push(scrollSVG(scroll(xl, cy, len, -1, rr, -1, true), id, 3) + scrollSVG(scroll(xl, cy, len * 0.75, -1, rr * 0.8, 1, false), id, 2.5));
          body.push(scrollSVG(scroll(xr, cy, len, 1, rr, -1, true), id, 3) + scrollSVG(scroll(xr, cy, len * 0.75, 1, rr * 0.8, 1, false), id, 2.5));
        }
        const accent = b.k === "q" ? b.acc : b.k === "l1" && !!l2;
        body.push(layered(esc(b.t), `x="500" y="${f1(base)}" ${fa(b.f, b.s, 0.01)} text-anchor="middle"`, b.s, P, id, accent));
      }
      y += b.h + GAP + g2;
    }
    if (foot) body.push(plaque(1318, foot, S.small, P, id));

    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc([spec.arch, spec.quote ? parseQuote(spec.quote).map(q => q.t).join(" ") : [spec.l1, spec.amp, spec.l2].join(" ")].filter(Boolean).join(" "))}"><defs>${defs.join("")}</defs>` +
      `<rect width="${W}" height="${H}" fill="${P.bg}"/><g clip-path="url(#${id}cl)">${pattern(spec.pattern, P, id, R)}<rect width="${W}" height="${H}" fill="url(#${id}glow)"/>${motif(spec.motif, P, id, R)}</g>` +
      `<rect width="${W}" height="${H}" fill="url(#${id}vig)"/>${frame(id, R)}${body.join("")}` +
      `<rect width="${W}" height="${H}" filter="url(#${id}gr)" opacity="${P.light ? 0.16 : 0.12}" style="mix-blend-mode:overlay"/></svg>`;
  }

  function fontsFor(spec) { const S = STYLES[spec.style] || STYLES.saloon; return [S.arch, S.l1, S.l2, S.amp, S.small]; }
  async function ready(spec) {
    if (!document.fonts) return;
    await Promise.all(fontsFor(spec).map(f => document.fonts.load(`${f[1]} 100px "${f[0]}"`).catch(() => null)));
  }
  function checks(spec) {
    const P = PALETTES[spec.palette] || PALETTES.noir_gold;
    return { main: contrast(P.m1[1], P.bg), accent: contrast(P.m2[1], P.bg), ribbon: contrast(P.ribbonInk, P.ribbon[0]) };
  }

  root.Ornate = { W, H, STYLES, PALETTES, PATTERNS, MOTIFS, PRESETS, QUOTES, FONT_URL, render, ready, checks, contrast };
})(typeof window !== "undefined" ? window : globalThis);
