// Eksport poster ornate ke PNG (dan SVG) guna Chromium (Playwright).
// Guna: node scripts/ornate_export.js [--size pin|print] [--spec fail.json] [--out folder]
//   pin   = 1000x1500 px (pin Pinterest 2:3)
//   print = 3600x5400 px (24x36 in pada 150 dpi; juga cukup untuk 16x24 dan 12x18 pada 225/300 dpi)
// --set short|quotes|all: set contoh (lalai all). --spec: fail JSON berisi senarai spesifikasi (medan sama seperti Ornate.PRESETS). Lalai: 8 contoh.
// Perlu internet ke fonts.googleapis.com untuk memuat fon.
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");

const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const size = arg("--size", "pin"), out = arg("--out", path.join(__dirname, "..", "build", "ornate"));
const engine = path.join(__dirname, "..", "demo", "ornate", "ornate.js");
const specFile = arg("--spec"), set = arg("--set", "all");
const slug = s => String(s).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 1500 }, deviceScaleFactor: size === "print" ? 3.6 : 1 });
  await p.setContent('<html><body style="margin:0"><div id="o"></div></body></html>');
  await p.addScriptTag({ path: engine });
  await p.evaluate(() => new Promise((ok, no) => { const l = document.createElement("link"); l.rel = "stylesheet"; l.href = Ornate.FONT_URL; l.onload = ok; l.onerror = () => no(new Error("Fon Google tidak dapat dimuat")); document.head.append(l); }));
  const specs = specFile ? JSON.parse(fs.readFileSync(specFile, "utf8")) : await p.evaluate(set => set === "short" ? Ornate.PRESETS : set === "quotes" ? Ornate.QUOTES : Ornate.PRESETS.concat(Ornate.QUOTES), set);
  for (const [i, s] of specs.entries()) {
    const svg = await p.evaluate(async s => { await Ornate.ready(s); await document.fonts.ready; const svg = Ornate.render(s, "x"); const o = document.getElementById("o"); o.innerHTML = svg; o.firstChild.setAttribute("width", "1000"); o.firstChild.setAttribute("height", "1500"); return svg; }, s);
    const name = `${String(i + 1).padStart(2, "0")}-${slug(s.name || [s.l1, s.l2].join(" "))}`;
    await p.locator("#o svg").screenshot({ path: path.join(out, `${name}-${size}.png`) });
    fs.writeFileSync(path.join(out, `${name}.svg`), svg);
    console.log("ditulis", name);
  }
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
