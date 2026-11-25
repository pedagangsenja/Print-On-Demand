"""Tab FC > Design dalam dashboard: carta aliran lettering v1 (9 langkah x 3 lajur) + lajur Alat bagi setiap lajur.

Sumber isi: scripts/lettering_flowchart.py dan docs/lettering-standard.md (cawangan great-sagan / funny-goldberg, 25 Nov 2026).
Status alat = keadaan 25 Nov 2026 (bukti: designs/lettering-v1/*, scripts/lettering/*, data/export/setup/*.json).

Guna: python3 scripts/build_fc_design.py <dashboard.html>
  Kali pertama: tambah butang tab FC, seksyen, CSS dan JS. Seterusnya: ganti jadual antara penanda FC:DESIGN sahaja.
"""
import html
import re
import sys

E = html.escape
OK, PART, NO = ("ada", "ok"), ("sebahagian", "warn"), ("belum dibina", "bad")
TESTED = ("diuji 24 Nov", "warn")
GPU = ("belum diuji", "warn")

COLS = [("Sedia ada: S1–S6 (Lettering P9)", "fc-c1"), ("Cadangan pertama: 4 lapisan, 5 kunci", "fc-c2"),
        ("Standard v1: aliran terkini", "fc-c3")]

# Setiap baris: (sedia ada, alat), (cadangan pertama, alat), (standard v1, alat)
ROWS = [
    ((dict(title="1. Rujukan", body=["Upload rujukan", "Ambil ciri umum sahaja"],
           warn=["Ciri gaya hanya ada dalam ayat templat"]),
      [("Anda", "upload imej rujukan", OK), ("Claude", "baca imej, ambil ciri umum", OK)]),
     (dict(tag="LAPISAN 1", status="BAHARU", title="1. Kad Gaya",
           body=["Gaya lama: guna kad dalam S&C", "Gaya baharu: Claude isi kad daripada upload",
                 "Isi kad: medium, bentuk huruf ikut peranan, susunan, hierarki, hiasan, kelas kemasan, 8 ciri QC, julat panjang sesuai",
                 "Warna C berasingan: latar + dakwat 1–3"],
           keys=["Kunci 1: Kad Gaya satu-satunya sumber gaya"]),
      [("Claude", "isi kad daripada upload", OK), ("Tab Daftar S/C", "semak gaya lama", OK)]),
     (dict(tag="LAPISAN 1", status="DIKEMAS KINI", title="1. Kad Gaya",
           body=["1a simpan rujukan di tempat kekal; 1b semak pendua dalam S&C",
                 "1c isi kad 16 medan; setiap medan = semakan QC (ya / tidak) + frasa prompt",
                 "2–3 ciri teras wajib lulus; unsur berisiko; senarai jangan salin; julat panjang ayat",
                 "Warna C berasingan: peranan + nama warna untuk prompt",
                 "1d anda luluskan kad (~2 minit); 1e imej bukti (ayat pendek, 2 seed) jadi imej sauh"],
           keys=["Kunci 1: Kad Gaya satu-satunya sumber gaya"]),
      [("Tab Daftar S/C", "1a simpan rujukan, 1b semak pendua", OK),
       ("kad.py (Python)", "Kad Gaya K1–K6, ciri QC + frasa prompt", PART),
       ("Anda", "1d luluskan kad", OK), ("gen_moss.py / gen.py", "1e imej bukti, 2 seed", OK)])),

    ((dict(title="2. Ayat", body=["3–7 perkataan, semak trademark", "Tetapkan baris dan perkataan utama"],
           warn=["Diuji pada 4 perkataan sahaja", "Hanya 2 kelas: pendek ≤ 6, panjang ≥ 7"]),
      [("Claude", "pilih ayat, baris, perkataan utama", OK), ("Semak trademark", "tiada kaedah bertulis", NO)]),
     (dict(status="DIUBAH", title="2. Ayat + peranan + laluan",
           body=["Semak trademark", "Setiap perkataan: utama / sokongan / penyambung",
                 "Laluan ikut panjang ayat baharu, bukan ayat rujukan"],
           minis=[("Laluan 1", "Pendek (1–4 perkataan). AI penuh, satu blok"),
                  ("Laluan 2", "Sederhana (5–8). AI penuh, hierarki wajib"),
                  ("Laluan 3", "Panjang (9–16). Hibrid: AI lukis perkataan utama, font berlesen untuk baris lain"),
                  ("Laluan 4", "Terlalu panjang (17+). Font dahulu: AI buat tajuk dan hiasan sahaja")]),
      [("Claude", "peranan setiap perkataan, pilih laluan", OK), ("USPTO", "semak trademark (Setup s26: Belum)", NO),
       ("Font berlesen", "laluan 3–4", NO)]),
     (dict(status="DIKEMAS KINI", title="2. Ayat + peranan + laluan",
           body=["Ayat asal; saringan trademark bertulis, hasil direkod",
                 "Ukur kesukaran: bilangan perkataan, perkataan 7+ huruf, perkataan berulang",
                 "Kata isi = utama; kata fungsi = penyambung; perkataan 7+ huruf jadi utama",
                 "Sokongan dan penyambung HURUF BESAR kecuali kad wajibkan skrip",
                 "Hasil: Spesifikasi Teks (rujukan ejaan untuk QC)"],
           minis=[("Laluan 1: standard v1", "1–4 perkataan. AI penuh, satu blok"),
                  ("Laluan 2: standard v1", "5–8 perkataan. AI penuh, hierarki wajib"),
                  ("Laluan 3: percubaan", "9–16 perkataan. Hibrid. Belum diuji; perlu kelulusan anda"),
                  ("Laluan 4: percubaan", "17+ perkataan. Font dahulu. Belum diuji; perlu kelulusan anda")]),
      [("kad.py (Python)", "Spesifikasi Teks + ukur kesukaran", PART), ("Claude", "peranan, pilih laluan", OK),
       ("USPTO", "saringan bertulis, hasil direkod", NO), ("Font berlesen", "laluan 3–4 (percubaan)", NO)])),

    ((dict(title="3. Prompt: templat tetap", body=["styles.py: 6 ayat siap (S1–S6)", "Arahan setiap perkataan + ekor larangan"],
           warn=["Dikunci pada 4 perkataan", "Gaya, warna dan latar bercampur"]),
      [("styles.py (Python)", "6 prompt siap S1–S6", OK)]),
     (dict(tag="LAPISAN 2", status="BAHARU", title="3. Pembina prompt",
           body=["Kad Gaya + ayat + warna C + keluarga model",
                 "Peraturan: petikan sekali sahaja, tiada hex atau nombor, ayat hierarki wajib"],
           minis=[("Keluarga LLM", "MOSS, klein, Z-Image, ERNIE: prompt penuh"),
                  ("Keluarga T5", "schnell, Chroma: ringkas, teks di depan")]),
      [("Pembina prompt (Python)", "dibina sebagai kad.py dalam v1", PART)]),
     (dict(tag="LAPISAN 2", status="DIKEMAS KINI", title="3. Pembina prompt (kod)",
           body=["Kad + Spesifikasi Teks yang sama → prompt yang sama",
                 "Rangka tetap 9 bahagian; had token setiap model + turutan potong",
                 "Semak automatik: petikan sekali, sama dengan Spesifikasi Teks, tiada hex / nombor / nama font",
                 "Profil model: format, pembalut, penambah prompt; format T5 diuji A/B dahulu",
                 "Syarat pakai: hasilkan semula S1–S6 tidak lebih buruk"]),
      [("kad.py: bina() + semak() (Python)", "prompt + semakan automatik", PART),
       ("gen.py: PROFIL", "profil setiap model dikunci", PART)])),

    ((dict(title="4. Jana", body=["MOSS SFT + LoRA 8 langkah", "Text-to-image penuh, 768×1024", "2 seed (CPU)"],
           warn=["Tiada peraturan tukar model"]),
      [("MOSS-Image SFT + LoRA", "model, 8 langkah", OK), ("gen_moss.py (Python, diffusers)", "CPU, 2 seed", OK)]),
     (dict(status="DIUBAH", title="4. Jana",
           body=["Text-to-image penuh, 768×1024",
                 "Laluan 1–2: seluruh ayat. Laluan 3: perkataan utama sahaja. Laluan 4: tajuk + hiasan",
                 "Seed: 2 (laluan 1), 3–4 (laluan 2)", "Log: model, seed, prompt, masa"],
           keys=["Kunci 3: model hanya untuk gaya yang ia lulus"]),
      [("MOSS-Image, ERNIE-Image-Turbo", "keluarga LLM", OK), ("FLUX.2 klein 4B, Z-Image-Turbo", "keluarga LLM", OK),
       ("FLUX.1 schnell, Chroma", "keluarga T5", OK), ("diffusers (Python)", "enjin", OK)]),
     (dict(status="DIKEMAS KINI", title="4. Jana",
           body=["Tetapan dikunci dalam profil model; enjin diffusers",
                 "Model utama: MOSS dan ERNIE (12/12 pada S1–S6); klein 4B 6/12",
                 "Seed tetap 42, 7, 123, 2024: laluan 1 = 2 seed, laluan 2 = 3–4",
                 "Satu model besar pada satu masa; semak RAM dan disk dahulu",
                 "Log lengkap setiap imej; imej mentah disimpan sebelum sesi tamat"],
           keys=["Kunci 3: model hanya untuk gaya yang ia lulus"]),
      [("gen_moss.py", "MOSS SFT + LoRA", OK),
       ("gen.py", "ERNIE, klein 4B, Z-Image, schnell, Chroma, Kandinsky", OK),
       ("run_k6.py", "ujian 6 enjin, satu demi satu", OK), ("Kaggle GPU (GEN_DEVICE)", "banding CPU vs GPU", GPU)])),

    ((dict(title="5. QC", body=["Ejaan 100%, tiada teks rawak, tiada cacat", "9 ciri gaya (semak mata)",
                                "Gagal: seed baharu (maks 4)"]),
      [("Claude", "semak mata: ejaan + 9 ciri gaya", OK)]),
     (dict(tag="LAPISAN 3", status="DIUBAH", title="5. QC ikut kad",
           body=["OCR saring dahulu, kemudian semak mata",
                 "3 pintu wajib: ejaan 100%, tiada teks rawak, tiada cacat", "Gaya: sekurang-kurangnya 7/8 ciri kad",
                 "Gagal: tambah ayat penegas + seed baharu (maks 4), kemudian model sandaran"],
           keys=["Kunci 2: QC sama untuk semua model", "Kunci 5: peraturan ulang"]),
      [("RapidOCR", "saring ejaan", TESTED), ("Claude", "semak mata + ayat penegas", OK)]),
     (dict(tag="LAPISAN 3", status="DIKEMAS KINI", title="5. QC ikut kad",
           body=["3 pintu wajib; ejaan huruf demi huruf ikut Spesifikasi Teks; OCR hanya menanda",
                 "Ciri kad ≥ 7/8 + ciri teras wajib; banding dengan upload dan imej sauh",
                 "Ciri sejagat: boleh dibaca kecil, tiada teks terpotong, margin cukup",
                 "QC dua kali: imej mentah dan selepas kemasan",
                 "Ulang ikut jenis gagal (maks 4) → model sandaran → pendekkan ayat → lapor"],
           keys=["Kunci 2: QC sama untuk semua model", "Kunci 5: peraturan ulang"]),
      [("Claude + helaian semakan", "3 pintu, ciri kad ≥ 7/8", OK),
       ("RapidOCR", "hanya menanda (skor 0.33–0.88 pada ejaan betul)", TESTED),
       ("qc/<model>.json", "rekod QC setiap imej", PART)])),

    ((dict(title="6. Kemasan: finish.py", body=["Vektor → palet gaya → margin seragam", "300 DPI, 8×10 hingga 24×36",
                                                "Tekstur: grain / worn / chalk"],
           warn=["Dakwat rata atas latar satu warna sahaja"]),
      [("finish.py (Python)", "k-means, potrace, cairosvg, tekstur", OK)]),
     (dict(tag="LAPISAN 4", status="DIUBAH", title="6. Kemasan ikut kelas",
           body=["Palet C dipaksa di sini", "F1 dan F2: 1 imej → beberapa warna",
                 "Laluan 3–4: skrip gabung baris font ikut kad, kemudian semak 8 ciri sekali lagi"],
           minis=[("F1", "Vektor rata (finish.py)"), ("F2", "Rata + tekstur"), ("F3", "Raster: gaya bergambar, gradien")],
           keys=["Kunci 4: skrip paksa warna, margin, tekstur"]),
      [("finish.py", "F1 vektor rata, F2 tekstur", OK), ("Alat F3 raster", "belum dipilih", NO),
       ("Skrip gabung baris font", "laluan 3–4", NO)]),
     (dict(tag="LAPISAN 4", status="DIKEMAS KINI", title="6. Kemasan ikut kad",
           body=["Parameter daripada kad: margin, tekstur, bilangan dakwat, butiran halus",
                 "Semak automatik: bilangan lapisan dan dakwat yang hilang",
                 "Warna ikut peranan: 1 imej → beberapa warna C", "Seed tekstur berbeza setiap design",
                 "Simpan SVG induk; PNG besar dijana semula bila perlu"],
           minis=[("F1: v1", "Vektor rata"), ("F2: v1", "Rata + tekstur"), ("F3: ditangguh", "Raster; belum wujud")],
           keys=["Kunci 4: skrip paksa warna, margin, tekstur"]),
      [("finish.py", "F1 / F2; parameter masih tetap dalam skrip", PART),
       ("Kemasan ikut kad (Python)", "baca kad + semakan automatik", NO)])),

    ((dict(title="7. Anda lulus atau tolak", body=["~5 minit"]),
      [("Anda", "~5 minit", OK)]),
     (dict(title="7. Anda lulus atau tolak", body=["~5 minit"]),
      [("Anda", "~5 minit", OK)]),
     (dict(status="DIKEMAS KINI", title="7. Anda lulus atau tolak",
           body=["Papar upload, imej sauh dan hasil sebelah-menyebelah + skor QC",
                 "Sebab tolak daripada senarai tetap; disalur balik ke kad, jadual model × gaya atau ulangan",
                 "3 titik kelulusan: kad, contoh pertama laluan 3–4, hasil akhir", "Had bilangan imej setiap helaian"]),
      [("Anda", "3 titik kelulusan", OK), ("Paparan sebelah-menyebelah", "upload, imej sauh, hasil + skor QC", NO),
       ("Tab AI Image Test / Daftar S/C", "pilih A atau SNC selepas setiap jana", OK)])),

    ((dict(title="8. Simpan dalam S&C", body=["Nama, nota, imej contoh, imej asal, prompt terisi"],
           warn=["Prompt terisi sahaja; tiada ciri gaya berstruktur"]),
      [("Tab Daftar S/C", "stor data/gaya + data/warna", OK)]),
     (dict(status="DIUBAH", title="8. Simpan dalam S&C", body=["Kad Gaya + prompt + model + seed + imej",
                                                               "Gaya boleh dijana semula"]),
      [("Tab Daftar S/C", "rekod S dan C", OK), ("Kad Gaya berstruktur dalam stor", "", NO)]),
     (dict(status="DIKEMAS KINI", title="8. Simpan dalam S&C",
           body=["Rekod S: Kad Gaya + templat prompt tanpa perkataan + model lulus + versi kad",
                 "Rekod C: peranan + nama warna; satu sumber kod hex",
                 "Daftar design lulus: ayat, S, C, model, seed, fail induk", "Semua fail disimpan sebelum sesi tamat"]),
      [("Tab Daftar S/C", "rekod S dan C", OK), ("Kad Gaya berstruktur dalam stor", "templat, model lulus, versi", NO),
       ("Daftar design", "ayat, S, C, model, seed, fail induk", NO)])),

    ((dict(title="9. Mockup → pin → upload", body=[]),
      [("Skrip mockup", "Workflow w03", NO), ("Printify API", "w04; akaun Printify: Sedang (Setup s09)", PART),
       ("Pinterest API", "w05; Setup s15–s18: Belum", NO)]),
     (dict(title="9. Mockup → pin → upload", body=[]),
      [("Skrip mockup", "Workflow w03", NO), ("Printify API", "w04; Setup s09: Sedang", PART),
       ("Pinterest API", "w05; Setup s15–s18: Belum", NO)]),
     (dict(status="DIKEMAS KINI", title="9. Serahan → mockup → pin → upload",
           body=["Standard berhenti di serahan kepada Workflow",
                 "Serahan: fail cetak setiap saiz, pratonton, ayat, kod S dan C, hasil trademark",
                 "Produk dan pin ditanda kod S / C → tab Prestasi",
                 "Jualan kembali ke S&C: gaya menang dapat lebih ayat dan warna"]),
      [("USPTO", "w02 hasil saringan dalam serahan", NO), ("Skrip mockup", "w03", NO),
       ("Printify API", "w04; Setup s09: Sedang", PART), ("Pinterest API", "w05; Setup s15–s18: Belum", NO),
       ("Prestasi (kod S / C)", "tiada dalam dashboard semasa", NO)])),

    ((dict(title="Tukar model", body=["Tiada peraturan bertulis.",
                                      "Ujian P9b (24 Nov) pada S1–S6: MOSS 12/12, ERNIE 12/12, klein 4B 6/12 imej ejaan betul."]),
      [("Ujian P9b", "MOSS, ERNIE, klein 4B pada S1–S6", OK)]),
     (dict(title="Tukar model", body=["Ujian kelayakan sekali bagi setiap model baharu, direkod dalam jadual model × gaya.",
                                      "Setiap gaya × ayat pendek dan sederhana × 2 seed.",
                                      "Lulus: ≥ 90% imej ejaan betul, gaya ≥ 7/8, tiada teks liar."]),
      [("Jadual model × gaya", "", NO)]),
     (dict(title="Tukar model", body=["Standard v1 (25 Nov, dipersetujui pengguna): laluan 1–2, kemasan F1–F2. Belum dibina.",
                                      "Ujian kelayakan seperti cadangan, sah untuk gabungan tetapan yang dikunci sahaja.",
                                      "Tahap bukti angka: lemah."]),
      [("gen.py + run_k6.py", "ujian kelayakan setiap enjin", OK),
       ("qc/<model>.json", "hasil → jadual model × gaya", PART)])),
]


def pill(text, tone, cls=""):
    return f'<span class="pod-pill {cls}" data-tone="{tone}">{E(text)}</span>' if tone else f'<span class="pod-pill {cls}">{E(text)}</span>'


def cell(s):
    o = ['<div class="fc-head">']
    if s.get("tag"):
        o.append(f'<span class="fc-tag">{E(s["tag"])}</span>')
    if s.get("status"):
        o.append(f'<span class="pod-pill fc-st">{E(s["status"])}</span>')
    o.append(f'</div><b class="fc-title">{E(s["title"])}</b>')
    if s["body"]:
        o.append("<ul>" + "".join(f"<li>{E(b)}</li>" for b in s["body"]) + "</ul>")
    if s.get("minis"):
        o.append('<div class="fc-minis">' + "".join(
            f'<div class="fc-mini"><b>{E(h)}</b><span>{E(t)}</span></div>' for h, t in s["minis"]) + "</div>")
    chips = [f'<span class="pod-pill fc-key">{E(k)}</span>' for k in s.get("keys", [])]
    chips += [pill("! " + w, "warn", "fc-warn") for w in s.get("warn", [])]
    if chips:
        o.append('<div class="fc-chips">' + "".join(chips) + "</div>")
    return "".join(o)


def tools(ts):
    return '<ul class="fc-tools">' + "".join(
        f'<li><b>{E(n)}</b>{f"<span>{E(d)}</span>" if d else ""}{pill(st[0], st[1])}</li>' for n, d, st in ts) + "</ul>"


def table():
    head = "".join(f'<th class="{c}">{E(t)}</th><th class="{c} fc-alat">Alat</th>' for t, c in COLS)
    body = []
    for row in ROWS:
        tds = "".join(f'<td class="{COLS[i][1]}">{cell(s)}</td><td class="{COLS[i][1]} fc-alat">{tools(t)}</td>'
                      for i, (s, t) in enumerate(row))
        body.append(f"<tr>{tds}</tr>")
    return (f'<div class="fc-wrap"><table class="fc-table"><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')


START, END = "<!-- FC:DESIGN START -->", "<!-- FC:DESIGN END -->"

SECTION = f"""<section id="tab-fc" class="pod-tab" role="tabpanel" aria-labelledby="btn-fc" hidden>
<div class="fc-subbar" role="tablist" aria-label="Sub tab FC">
  <button type="button" class="fc-sub-btn" role="tab" id="btn-fc-design" data-sub="fc-design" aria-controls="fc-design" aria-selected="true">Design</button>
</div>
<section id="fc-design" class="pod-section pod-first fc-sub" role="tabpanel" aria-labelledby="btn-fc-design">
  <h2>Aliran kerja lettering: sedia ada, cadangan pertama, standard v1</h2>
  <p class="pod-muted">Sumber: carta v1 (scripts/lettering_flowchart.py) dan docs/lettering-standard.md, 25 Nov 2026. Standard v1 dipersetujui pengguna 25 Nov; belum dibina sepenuhnya. Laluan 3–4 percubaan, F3 ditangguh. Status alat = keadaan 25 Nov 2026.</p>
  <p class="fc-legend"><span>{pill("ada", "ok")} alat wujud dan dipakai</span><span>{pill("sebahagian", "warn")} separuh siap / sedang diuji</span><span>{pill("belum dibina", "bad")} belum wujud</span><span><span class="pod-pill fc-key">Kunci</span> 5 kunci gaya</span><span>{pill("! kelemahan", "warn", "fc-warn")} kelemahan aliran sedia ada</span></p>
{START}
{END}
</section>
</section>
"""

CSS = """/* FC tab */
.fc-subbar { display: flex; gap: var(--cds-gap-xs); border-bottom: 1px solid var(--color-border-line); }
.fc-sub-btn { appearance: none; background: none; border: 0; border-bottom: 2px solid transparent; margin-bottom: -1px; padding: 4px var(--cds-pad-md); font: inherit; font-size: var(--cds-font-size-caption); color: var(--color-fg-muted); cursor: pointer; }
.fc-sub-btn[aria-selected="true"] { color: var(--color-fg); border-bottom-color: var(--color-fg); font-weight: var(--cds-font-weight-medium); }
.fc-sub-btn:focus-visible { outline: 2px solid var(--color-fg); outline-offset: 2px; }
.fc-sub[hidden] { display: none !important; }
.fc-legend { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 8px; font-size: var(--cds-font-size-caption); color: var(--color-fg-muted); }
.fc-wrap { overflow-x: auto; border: 1px solid var(--color-border-line); border-radius: var(--cds-radius); }
.pod .fc-table { min-width: 1500px; table-layout: fixed; }
.pod .fc-table th { position: static; white-space: normal; border-top: 3px solid var(--fc-accent); color: var(--color-fg); }
.pod .fc-table th, .pod .fc-table td { width: 21%; }
.pod .fc-table th.fc-alat, .pod .fc-table td.fc-alat { width: 12.33%; background: var(--color-panel); }
.pod .fc-table td.fc-alat + td { border-left: 2px solid var(--color-border-line); }
.fc-c1 { --fc-accent: #64748b; } .fc-c2 { --fc-accent: #0f9488; } .fc-c3 { --fc-accent: #6366f1; }
.fc-head { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px; }
.fc-head:empty { display: none; }
.fc-tag { font-size: 11px; font-weight: var(--cds-font-weight-medium); letter-spacing: .04em; color: var(--fc-accent); }
.pod .fc-st { color: var(--fc-accent); border-color: currentColor; font-size: 11px; }
.fc-title { display: block; margin: 2px 0 4px; }
.fc-table ul { margin: 0; padding-left: 16px; display: grid; gap: 3px; }
.fc-minis { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 6px; }
.fc-mini { border: 1px solid var(--color-border-line); border-left: 3px solid var(--fc-accent); border-radius: var(--cds-radius); padding: 4px 6px; display: grid; gap: 2px; }
.fc-mini b { color: var(--fc-accent); }
.fc-chips { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }
.pod .fc-chips .pod-pill { white-space: normal; border-radius: 10px; }
.fc-legend > span { white-space: nowrap; }
.pod .fc-key { color: #3b82f6; border-color: currentColor; }
.pod .fc-table .fc-tools { list-style: none; padding: 0; gap: 6px; }
.fc-tools li { display: grid; gap: 1px; justify-items: start; }
.fc-tools span:not(.pod-pill) { color: var(--color-fg-muted); }
"""

JS = """<script>
(() => {
  const btns = [...document.querySelectorAll('.fc-sub-btn')];
  const open = (id) => btns.forEach((b) => {
    const on = b.dataset.sub === id;
    b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1;
    const p = document.getElementById(b.dataset.sub); if (p) p.hidden = !on;
  });
  btns.forEach((b) => b.addEventListener('click', () => open(b.dataset.sub)));
})();
</script>
"""

BTN = ('    <button type="button" class="pod-tab-btn" role="tab" id="btn-fc" data-tab="tab-fc" aria-controls="tab-fc" '
       'aria-selected="false" tabindex="-1">FC</button>\n')


def main(path):
    s = open(path, encoding="utf-8").read()
    if START not in s:
        a = s.index('data-tab="tab-daftar"')
        a = s.index("\n", a) + 1
        s = s[:a] + BTN + s[a:]
        s = s.replace("#tab-aliran, #tab-daftar { break-before", "#tab-aliran, #tab-daftar, #tab-fc { break-before", 1)
        s = s.replace("</style>", CSS + "</style>", 1)
        a = s.index("</div>\n\n<script>\nwindow.POD = window.POD || {};")
        s = s[:a] + SECTION + "\n" + s[a:]
        a = s.rindex("</script>") + len("</script>")
        s = s[:a] + "\n" + JS + s[a:]
    s = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda m: START + "\n" + table() + "\n" + END, s, flags=re.S)
    open(path, "w", encoding="utf-8").write(s)
    print(f"ok: {path}, {len(ROWS)} baris x 6 lajur")


if __name__ == "__main__":
    main(sys.argv[1])
