// Tab Etsy: rujukan gaya penjual ArtfulCraftsCreators, satu baris setiap design.
// Data: etsy_designs, etsy_listing, etsy_fonts (fail JSON dijana oleh scripts/build_etsy.py).
dash.calc('etsy_ringkas', {
  inputs: ['etsy_designs'],
  title: 'Ringkasan design rujukan Etsy',
  description: 'Satu baris: bilangan design dan gambar asal; purata blok teks, jenis font, jenis hiasan dan liputan dakwat; peratus design berikon, bersenget, berteks lengkung dan yang kata utamanya dalam skrip; bilangan design dengan ayat bermasalah.',
  fn: (designs) => {
    const n = designs.length;
    if (!n) return [];
    const avg = (k) => Math.round((designs.reduce((s, r) => s + Number(r[k] || 0), 0) / n) * 10) / 10;
    const pct = (test) => Math.round((designs.filter(test).length / n) * 1000) / 10;
    return [{
      design: n,
      gambar: new Set(designs.map((r) => String(r.id).split('-')[0])).size,
      purata_blok: avg('bil_blok'),
      purata_font: avg('bil_font'),
      purata_hiasan: avg('bil_jenis_hiasan'),
      purata_dakwat: avg('dakwat_pct'),
      pct_ikon: pct((r) => Number(r.bil_ikon) > 0),
      pct_skrip_utama: pct((r) => String(r.font_kata_utama).includes('Skrip')),
      pct_senget: pct((r) => r.senget === 'Ya'),
      pct_lengkung: pct((r) => r.lengkung === 'Ya'),
      isu: designs.filter((r) => r.isu_ayat).length,
    }];
  },
});

// Jadual kekerapan: [id, lajur dalam etsy_designs, pemisah jika satu design boleh ada beberapa nilai]
window.ETSY_FREQ = [
  ['susunan', 'susunan', null], ['font', 'jenis_font', ', '], ['gandingan', 'gandingan_font', null],
  ['font_utama', 'font_kata_utama', ', '], ['font_mula', 'font_baris_pertama', null], ['font_akhir', 'font_baris_akhir', null],
  ['rawat_mula', 'rawatan_baris_pertama', null], ['peranan', 'corak_peranan', null], ['tangga', 'tangga_saiz', null],
  ['bekas', 'bekas', ', '], ['kesan', 'kesan_khas', ', '], ['hiasan', 'jenis_hiasan', ', '],
  ['ikon', 'peranan_ikon', ', '], ['gaya_ikon', 'gaya_ikon', ', '], ['kat_ikon', 'kategori_ikon', ', '],
  ['nada', 'nada', null], ['pandang', 'sudut_pandang', null], ['formula', 'formula', null],
];
window.ETSY_FREQ.forEach(([id, field, sep]) => dash.calc(`etsy_f_${id}`, {
  inputs: ['etsy_designs'],
  title: `Kekerapan lajur ${field}`,
  description: `Bilangan dan peratus design bagi setiap nilai lajur ${field}${sep ? ' (satu design boleh ada beberapa nilai, jadi peratus tidak berjumlah 100)' : ''}. Nilai kosong dikira sebagai Tiada.`,
  fn: (designs) => {
    const m = new Map();
    designs.forEach((r) => {
      const v = String(r[field] == null ? '' : r[field]);
      (sep ? v.split(sep) : [v]).map((k) => (k === '' || k === '–' ? 'Tiada' : k))
        .forEach((k) => m.set(k, (m.get(k) || 0) + 1));
    });
    return [...m].map(([nama, bil]) => ({ nama, bil, pct: Math.round((bil / designs.length) * 1000) / 10 }))
      .sort((a, b) => b.bil - a.bil || a.nama.localeCompare(b.nama));
  },
}));

(() => {
  // Lajur jadual utama: [kunci, label, kumpulan paparan, jenis]. Kepala jadual dalam index.html dijana daripada senarai ini.
  /*COLS*/
  const COLS = [
    ["tema", "Tema", "ringkas ayat", ""],
    ["susunan", "Jenis susunan", "ringkas susun", ""],
    ["kunci_gaya", "Kunci gaya (idea utama)", "ringkas tiru", "w"],
    ["baris", "Baris demi baris: font (calon) · saiz · rawatan · kesan · peranan", "teks", "lines"],
    ["kata_utama", "Kata utama", "ringkas teks", ""],
    ["kedudukan_utama", "Kedudukan kata utama", "teks", ""],
    ["tangga_saiz", "Tangga saiz (1–5)", "ringkas teks", ""],
    ["baris_terbesar", "Baris terbesar", "teks", ""],
    ["kontras_saiz", "Beza saiz", "teks", "n"],
    ["bil_blok", "Blok teks", "teks", "n"],
    ["bil_baris", "Baris", "teks", "n"],
    ["corak_peranan", "Corak peranan (U utama, S sokongan, K sambung)", "teks", ""],
    ["corak_font", "Urutan font", "teks", "w"],
    ["jenis_font", "Jenis font", "ringkas teks", ""],
    ["bil_font", "Bil. font", "teks", "n"],
    ["gandingan_font", "Gandingan font", "teks", ""],
    ["font_kata_utama", "Font kata utama", "teks", ""],
    ["font_baris_pertama", "Font baris pertama", "teks", ""],
    ["font_baris_akhir", "Font baris akhir", "teks", ""],
    ["rawatan_baris_pertama", "Rawatan baris pertama", "teks susun", ""],
    ["font_calon", "Font boleh tiru", "teks", "w"],
    ["kesan_khas", "Kesan huruf", "teks", ""],
    ["kesan_butiran", "Kesan huruf: butiran", "teks", "w"],
    ["huruf_besar_pct", "Huruf besar (%)", "teks", "n"],
    ["ikon", "Ikon: apa (kedudukan; gaya; saiz; slot)", "ringkas ikon", "w"],
    ["bil_ikon", "Bil. ikon", "ikon", "n"],
    ["peranan_ikon", "Peranan ikon", "ikon", ""],
    ["gaya_ikon", "Gaya ikon", "ikon", ""],
    ["saiz_ikon", "Saiz ikon", "ikon", ""],
    ["kategori_ikon", "Kategori ikon", "ikon", ""],
    ["hiasan", "Hiasan", "ikon", "w"],
    ["jenis_hiasan", "Jenis hiasan", "ikon", ""],
    ["bil_jenis_hiasan", "Bil. jenis hiasan", "ikon", "n"],
    ["bekas", "Bekas teks", "ringkas susun", ""],
    ["bil_bekas", "Bil. bekas", "susun", "n"],
    ["siluet", "Siluet", "susun", ""],
    ["simetri", "Simetri (mata)", "susun", ""],
    ["senget", "Senget", "susun", ""],
    ["sudut_senget", "Sudut senget (°)", "susun", "n"],
    ["lengkung", "Teks melengkung", "susun", ""],
    ["arah_lengkung", "Arah lengkung", "susun", ""],
    ["tindih", "Baris bertindih", "susun", ""],
    ["tekstur", "Tekstur", "susun", ""],
    ["nisbah", "Lebar ÷ tinggi", "ukur", "n"],
    ["lebar_px", "Lebar (px)", "ukur", "n"],
    ["tinggi_px", "Tinggi (px)", "ukur", "n"],
    ["dakwat_pct", "Dakwat (%)", "ukur", "n"],
    ["dakwat_atas_pct", "Dakwat sepertiga atas (%)", "ukur", "n"],
    ["dakwat_tengah_pct", "Dakwat sepertiga tengah (%)", "ukur", "n"],
    ["dakwat_bawah_pct", "Dakwat sepertiga bawah (%)", "ukur", "n"],
    ["pusat_x_pct", "Pusat jisim X (%)", "ukur", "n"],
    ["pusat_y_pct", "Pusat jisim Y (%)", "ukur", "n"],
    ["simetri_pct", "Simetri cermin (%)", "ukur", "n"],
    ["kepingan", "Kepingan hitam", "ukur", "n"],
    ["lubang", "Lubang putih", "ukur", "n"],
    ["tebal_pct", "Tebal garis purata (% lebar)", "ukur", "n"],
    ["isi_siluet_pct", "Isi siluet (%)", "ukur", "n"],
    ["formula", "Formula ayat", "ayat", "w"],
    ["bil_sekeluarga", "Design sama formula", "ayat", "n"],
    ["sekeluarga", "ID sama formula", "ayat", ""],
    ["nada", "Nada", "ayat", ""],
    ["sudut_pandang", "Sudut pandang", "ayat", ""],
    ["bil_perkataan", "Perkataan", "ayat", "n"],
    ["bil_aksara", "Huruf", "ayat", "n"],
    ["rasa", "Rasa", "ayat", ""],
    ["khalayak", "Khalayak", "ayat", ""],
    ["isu_ayat", "Isu ayat", "ayat", ""],
    ["resipi", "Resipi tiru (dijana daripada lajur lain)", "tiru", "xw"],
    ["skor_tiru", "Skor", "tiru", "n"],
    ["kesukaran", "Kesukaran tiru", "ringkas tiru", "pill"],
    ["status", "Status tiru", "ringkas tiru", ""],
    ["nota", "Nota", "tiru", ""],
    ["fail_asal", "Gambar asal", "tiru", ""],
    ["kedudukan", "Kedudukan", "tiru", ""]
  ];
  /*COLS*/
  const NCOL = COLS.length + 3;
  const GROUPS = [
    ['Teks dan font', 'teks'], ['Ikon dan hiasan', 'ikon'], ['Susunan', 'susun'],
    ['Ukuran piksel', 'ukur'], ['Ayat', 'ayat'], ['Tiru', 'tiru'],
  ];
  const TOP = { gandingan: 12, peranan: 12, tangga: 12, formula: 15 };
  const F = { q: '', tema: '', susunan: '', sukar: '', nada: '', isu: false };
  let view = 'ringkas';
  let openId = null;

  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  const rowsOf = (id) => { const d = dash.data(id); return d.status === 'ok' && Array.isArray(d.data) ? d.data : null; };
  const start = (tb, id, cols) => {
    tb.replaceChildren();
    const rows = rowsOf(id);
    if (!rows) POD.emptyRow(tb, cols, POD.statusMsg(id));
    return rows;
  };
  const parse = (s) => { try { const v = JSON.parse(s || '[]'); return Array.isArray(v) ? v : []; } catch (e) { return []; } };
  const tone = (k) => (k === 'Mudah' ? 'ok' : k === 'Sederhana' ? 'warn' : 'bad');

  // Angka ringkasan
  const one = (name, field, fmt) => dash.draw(name, (e) => {
    const rows = rowsOf('etsy_ringkas');
    e.textContent = rows && rows[0] ? fmt(rows[0][field]) : '—';
  });
  const num = (v) => String(v); const pc = (v) => `${v}%`;
  one('etsy-k-design', 'design', num); one('etsy-k-gambar', 'gambar', num);
  one('etsy-k-blok', 'purata_blok', num); one('etsy-k-font', 'purata_font', num);
  one('etsy-k-hiasan', 'purata_hiasan', num); one('etsy-k-dakwat', 'purata_dakwat', pc);
  one('etsy-k-ikon', 'pct_ikon', pc); one('etsy-k-skrip', 'pct_skrip_utama', pc);
  one('etsy-k-senget', 'pct_senget', pc); one('etsy-k-lengkung', 'pct_lengkung', pc);
  one('etsy-k-isu', 'isu', num);

  // Listing
  dash.draw('etsy-listing-body', (tb) => {
    const rows = start(tb, 'etsy_listing', 13); if (!rows) return;
    rows.forEach((r) => {
      const tr = el('tr'); tr.dataset.key = POD.enc(r.listing);
      POD.cell(tr, r.listing, 'pod-wide'); POD.cell(tr, r.penjual);
      POD.cell(tr, r.harga_rm, 'pod-num'); POD.cell(tr, r.harga_asal_rm, 'pod-num'); POD.cell(tr, r.diskaun_pct, 'pod-num');
      POD.cell(tr, r.rating, 'pod-num'); POD.cell(tr, r.bil_rating, 'pod-num'); POD.cell(tr, r.format);
      POD.cell(tr, r.bil_design, 'pod-num'); POD.cell(tr, r.gambar); POD.cell(tr, r.dilihat);
      POD.pillCell(tr, r.bukti); POD.cell(tr, r.nota_bukti, 'pod-wide');
      tb.appendChild(tr);
    });
  });

  // Jadual kekerapan
  window.ETSY_FREQ.forEach(([id]) => dash.draw(`etsy-fq-${id}`, (tb) => {
    const all = start(tb, `etsy_f_${id}`, 3); if (!all) return;
    const rows = TOP[id] ? all.slice(0, TOP[id]) : all;
    const max = Math.max(1, ...rows.map((r) => Number(r.bil) || 0));
    rows.forEach((r) => {
      const tr = el('tr'); tr.dataset.key = POD.enc(r.nama);
      POD.cell(tr, r.nama); POD.cell(tr, r.bil, 'pod-num');
      const td = el('td', 'pod-barcell');
      const bar = el('span', 'etsy-bar'); bar.style.width = `${Math.round((r.bil / max) * 70)}px`;
      td.append(bar, el('span', '', `${r.pct}%`)); tr.appendChild(td); tb.appendChild(tr);
    });
  }));

  // Font calon
  dash.draw('etsy-font-body', (tb) => {
    const rows = start(tb, 'etsy_fonts', 8); if (!rows) return;
    rows.forEach((r) => {
      const tr = el('tr'); tr.dataset.key = POD.enc(r.kunci);
      POD.cell(tr, r.jenis); POD.cell(tr, r.ciri, 'pod-wide'); POD.cell(tr, r.bil_design, 'pod-num');
      const td = el('td'); const a = POD.link(r.url, r.font);
      if (a) td.appendChild(a); else td.textContent = r.font || '—';
      tr.appendChild(td);
      POD.cell(tr, r.pilihan, 'pod-num'); POD.cell(tr, r.sumber); POD.cell(tr, r.lesen);
      const rk = el('td'); rk.appendChild(POD.pill(String(r.risiko || '—'), null, r.risiko === 'selamat' ? 'ok' : 'warn'));
      tr.appendChild(rk); tb.appendChild(tr);
    });
  });

  // Tapisan dan paparan lajur
  const match = (r) => {
    if (F.tema && r.tema !== F.tema) return false;
    if (F.susunan && r.susunan !== F.susunan) return false;
    if (F.sukar && r.kesukaran !== F.sukar) return false;
    if (F.nada && r.nada !== F.nada) return false;
    if (F.isu && !r.isu_ayat) return false;
    const words = F.q.toLowerCase().split(/\s+/).filter(Boolean);
    if (words.length) {
      const hay = [r.id, r.ayat, r.ikon, r.jenis_font, r.font_calon, r.hiasan, r.bekas, r.rasa, r.khalayak, r.susunan,
        r.nota, r.formula, r.kunci_gaya, r.kesan_butiran, r.nada].join(' ').toLowerCase();
      if (!words.every((w) => hay.includes(w))) return false;
    }
    return true;
  };
  const shownRows = () => (rowsOf('etsy_designs') || []).filter(match);
  const redraw = () => { dash.draw('etsy-body'); dash.draw('etsy-count'); };
  document.querySelectorAll('[data-etsy-f]').forEach((e) => {
    const k = e.dataset.etsyF;
    e.addEventListener(e.type === 'search' ? 'input' : 'change', () => { F[k] = e.type === 'checkbox' ? e.checked : e.value; redraw(); });
  });
  document.querySelectorAll('.etsy-reset').forEach((b) => b.addEventListener('click', () => {
    F.q = ''; F.tema = ''; F.susunan = ''; F.sukar = ''; F.nada = ''; F.isu = false;
    document.querySelectorAll('[data-etsy-f]').forEach((e) => { if (e.type === 'checkbox') e.checked = false; else e.value = ''; });
    dash.draw('etsy-f-susunan'); dash.draw('etsy-f-nada'); redraw();
  }));
  const pick = (name, calc, key, label) => dash.draw(name, (sel) => {
    const rows = rowsOf(calc) || [];
    sel.replaceChildren(new Option(label, ''), ...rows.map((r) => new Option(`${r.nama} (${r.bil})`, r.nama)));
    sel.value = F[key];
    sel.onchange = () => { F[key] = sel.value; redraw(); };
  });
  pick('etsy-f-susunan', 'etsy_f_susunan', 'susunan', 'Semua jenis susunan');
  pick('etsy-f-nada', 'etsy_f_nada', 'nada', 'Semua nada');
  dash.draw('etsy-count', (e) => { e.textContent = rowsOf('etsy_designs') ? String(shownRows().length) : '—'; });

  const setView = (v) => {
    view = v;
    document.querySelectorAll('.etsy-table').forEach((t) => {
      [...t.classList].filter((c) => c.startsWith('etsy-v-')).forEach((c) => t.classList.remove(c));
      t.classList.add(`etsy-v-${v}`);
    });
    document.querySelectorAll('[data-etsy-view]').forEach((b) => b.setAttribute('aria-pressed', b.dataset.etsyView === v ? 'true' : 'false'));
  };
  document.querySelectorAll('[data-etsy-view]').forEach((b) => b.addEventListener('click', () => setView(b.dataset.etsyView)));
  setView(view);

  // Butiran penuh satu design
  const dlg = () => document.querySelectorAll('#etsy-dlg');
  const closeDlg = () => { openId = null; dlg().forEach((z) => { z.hidden = true; }); };
  const openDlg = (id) => { openId = id; dlg().forEach((z) => { z.hidden = false; z.scrollTop = 0; }); dash.draw('etsy-detail'); };
  const step = (d) => {
    const rows = shownRows(); if (!rows.length) return;
    const i = rows.findIndex((r) => r.id === openId);
    openDlg(rows[(i + d + rows.length) % rows.length].id);
  };
  dlg().forEach((z) => z.addEventListener('click', (e) => {
    if (e.target === z || e.target.closest('.etsy-dlg-close')) closeDlg();
    else if (e.target.closest('.etsy-dlg-prev')) step(-1);
    else if (e.target.closest('.etsy-dlg-next')) step(1);
  }));
  document.addEventListener('keydown', (e) => {
    if (!openId) return;
    if (e.key === 'Escape') closeDlg(); else if (e.key === 'ArrowLeft') step(-1); else if (e.key === 'ArrowRight') step(1);
  });
  const miniTable = (heads, rows) => {
    const wrap = el('div', 'pod-table-wrap'); const t = el('table'); const hr = el('tr');
    heads.forEach((h) => hr.appendChild(el('th', '', h)));
    const th = el('thead'); th.appendChild(hr); const tb = el('tbody');
    rows.forEach((cells) => { const tr = el('tr'); cells.forEach((c) => POD.cell(tr, c)); tb.appendChild(tr); });
    t.append(th, tb); wrap.appendChild(t); return wrap;
  };
  dash.draw('etsy-detail', (box) => {
    box.replaceChildren();
    const r = (rowsOf('etsy_designs') || []).find((x) => x.id === openId);
    if (!r) return;
    box.appendChild(el('h3', 'etsy-d-title', `${r.id} · ${r.ayat}`));
    const top = el('div', 'etsy-d-top');
    const fig = el('div', 'etsy-d-img'); const src = POD.blob(r.img);
    if (src) { const img = el('img'); img.src = src; img.alt = `Design ${r.id}: ${r.ayat}`; fig.appendChild(img); if (POD.likeOn) POD.likeOn(fig, src, { cap: `Etsy ${r.id}: ${r.ayat}`, gaya: r.susunan, teks: r.ayat }); }
    const sum = el('div', 'etsy-d-sum');
    [['Kunci gaya', r.kunci_gaya], ['Jenis susunan', r.susunan], ['Tangga saiz', r.tangga_saiz], ['Formula ayat', r.formula], ['Kesukaran tiru', `${r.kesukaran} (skor ${r.skor_tiru})`]]
      .forEach(([k, v]) => { const p = el('p'); p.append(el('b', '', `${k}: `), document.createTextNode(String(v == null || v === '' ? '—' : v))); sum.appendChild(p); });
    top.append(fig, sum); box.appendChild(top);
    box.appendChild(el('h4', '', 'Baris demi baris'));
    const lines = parse(r.baris_json);
    box.appendChild(lines.length
      ? miniTable(['#', 'Teks', 'Font', 'Font boleh tiru', 'Saiz (1–5)', 'Huruf', 'Rawatan', 'Kesan', 'Peranan'],
        lines.map((l, i) => [i + 1, l.teks, l.font, l.calon, l.saiz, l.kes, l.rawatan, l.kesan, l.peranan]))
      : el('p', 'pod-muted', 'Tiada teks.'));
    box.appendChild(el('h4', '', 'Ikon'));
    const ik = parse(r.ikon_json);
    box.appendChild(ik.length
      ? miniTable(['Ikon', 'Kedudukan', 'Peranan', 'Gaya', 'Saiz', 'Slot dalam susunan', 'Kategori'],
        ik.map((i) => [i.apa, i.kedudukan, i.peranan, i.gaya, i.saiz, i.slot, i.kategori]))
      : el('p', 'pod-muted', 'Tiada ikon.'));
    GROUPS.forEach(([title, g]) => {
      box.appendChild(el('h4', '', title));
      const dl = el('dl', 'etsy-d-dl');
      COLS.filter((c) => c[2].split(' ').includes(g) && c[3] !== 'lines').forEach(([key, label]) => {
        const v = r[key];
        const d = el('div'); d.append(el('dt', '', label), el('dd', '', v == null || v === '' ? '—' : String(v))); dl.appendChild(d);
      });
      box.appendChild(dl);
    });
  });

  // Jadual utama: satu baris setiap design
  dash.draw('etsy-body', (tb) => {
    const rows = start(tb, 'etsy_designs', NCOL); if (!rows) return;
    const shown = rows.filter(match);
    if (!shown.length) { POD.emptyRow(tb, NCOL, 'Tiada design sepadan dengan tapisan.'); return; }
    shown.forEach((r) => {
      const tr = el('tr'); tr.dataset.key = POD.enc(r.id);
      const td = el('td', 'etsy-c-img'); const box = el('div', 'etsy-thumb');
      const src = POD.blob(r.img);
      if (src) {
        const b = el('button', 'etsy-open'); b.type = 'button'; b.setAttribute('aria-label', `Buka butiran design ${r.id}`);
        const img = el('img'); img.src = src; img.loading = 'lazy'; img.alt = `Design ${r.id}: ${r.ayat}`;
        b.appendChild(img); b.addEventListener('click', () => openDlg(r.id)); box.appendChild(b);
        if (POD.likeOn) POD.likeOn(box, src, { cap: `Etsy ${r.id}: ${r.ayat}`, gaya: r.susunan, teks: r.ayat });
      } else { box.textContent = '—'; }
      td.appendChild(box);
      const more = el('button', 'etsy-more', 'Butiran'); more.type = 'button'; more.addEventListener('click', () => openDlg(r.id));
      td.appendChild(more); tr.appendChild(td);
      POD.cell(tr, r.id); POD.cell(tr, r.ayat, 'pod-wide');
      COLS.forEach(([key, , groups, type]) => {
        const cls = `ec ${groups.split(' ').map((g) => `eg-${g}`).join(' ')}`;
        if (type === 'lines') {
          const ltd = el('td', `${cls} etsy-c-lines`); const wrap = el('div', 'etsy-lines');
          const lines = parse(r.baris_json);
          lines.forEach((l, i) => {
            const d = el('div');
            d.append(el('b', '', `${i + 1}. ${l.teks}`), el('span', '', ` — ${l.font} (${l.calon}) · saiz ${l.saiz} · ${l.rawatan}${l.kesan ? ` · ${l.kesan}` : ''} · ${l.peranan}`));
            wrap.appendChild(d);
          });
          if (!lines.length) wrap.textContent = '—';
          ltd.appendChild(wrap); tr.appendChild(ltd);
        } else if (type === 'pill') {
          const k = el('td', cls); k.appendChild(POD.pill(String(r[key] || '—'), null, tone(r[key]))); tr.appendChild(k);
        } else {
          POD.cell(tr, r[key], `${cls}${type === 'n' ? ' pod-num' : type === 'w' ? ' pod-wide' : type === 'xw' ? ' etsy-c-xw' : ''}`);
        }
      });
      tb.appendChild(tr);
    });
  });
})();
