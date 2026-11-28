// Tab Etsy: rujukan gaya penjual ArtfulCraftsCreators, satu baris setiap design.
// Data: etsy_designs, etsy_listing, etsy_fonts (fail JSON dijana oleh scripts/build_etsy.py).
dash.calc('etsy_ringkas', {
  inputs: ['etsy_designs'],
  title: 'Ringkasan design rujukan Etsy',
  description: 'Satu baris: bilangan design, bilangan gambar asal, purata baris teks, purata jenis font, purata liputan dakwat, peratus design berikon dan bilangan design dengan ayat bermasalah.',
  fn: (designs) => {
    const n = designs.length;
    if (!n) return [];
    const avg = (k) => Math.round((designs.reduce((s, r) => s + Number(r[k] || 0), 0) / n) * 10) / 10;
    return [{
      design: n,
      gambar: new Set(designs.map((r) => String(r.id).split('-')[0])).size,
      purata_baris: avg('bil_baris'),
      purata_font: avg('bil_font'),
      purata_dakwat: avg('dakwat_pct'),
      pct_ikon: Math.round((designs.filter((r) => Number(r.bil_ikon) > 0).length / n) * 1000) / 10,
      isu: designs.filter((r) => r.isu_ayat).length,
    }];
  },
});

dash.calc('etsy_f_susunan', {
  inputs: ['etsy_designs'],
  title: 'Kekerapan jenis susunan',
  description: 'Bilangan dan peratus design bagi setiap jenis susunan.',
  fn: (designs) => {
    const m = new Map();
    designs.forEach((r) => m.set(r.susunan, (m.get(r.susunan) || 0) + 1));
    return [...m].map(([nama, bil]) => ({ nama, bil, pct: Math.round((bil / designs.length) * 1000) / 10 }))
      .sort((a, b) => b.bil - a.bil || a.nama.localeCompare(b.nama));
  },
});

dash.calc('etsy_f_font', {
  inputs: ['etsy_designs'],
  title: 'Kekerapan jenis font',
  description: 'Bilangan dan peratus design yang menggunakan setiap jenis font (satu design boleh guna beberapa jenis).',
  fn: (designs) => {
    const m = new Map();
    designs.forEach((r) => String(r.jenis_font || '').split(', ').filter((k) => k && k !== '–')
      .forEach((k) => m.set(k, (m.get(k) || 0) + 1)));
    return [...m].map(([nama, bil]) => ({ nama, bil, pct: Math.round((bil / designs.length) * 1000) / 10 }))
      .sort((a, b) => b.bil - a.bil || a.nama.localeCompare(b.nama));
  },
});

dash.calc('etsy_f_bekas', {
  inputs: ['etsy_designs'],
  title: 'Kekerapan bekas teks',
  description: 'Bilangan dan peratus design yang ada setiap jenis bekas teks (reben, kotak, pil dan lain-lain); "Tiada" bermaksud semua teks tanpa bekas.',
  fn: (designs) => {
    const m = new Map();
    designs.forEach((r) => String(r.bekas || 'Tiada').split(', ').filter(Boolean)
      .forEach((k) => m.set(k, (m.get(k) || 0) + 1)));
    return [...m].map(([nama, bil]) => ({ nama, bil, pct: Math.round((bil / designs.length) * 1000) / 10 }))
      .sort((a, b) => b.bil - a.bil || a.nama.localeCompare(b.nama));
  },
});

dash.calc('etsy_f_ikon', {
  inputs: ['etsy_designs'],
  title: 'Kekerapan peranan ikon',
  description: 'Bilangan dan peratus design mengikut peranan ikon (atas, tengah, sisi, aksen, ganti huruf, bingkai, panel); "tiada ikon" bagi design tanpa ikon.',
  fn: (designs) => {
    const m = new Map();
    designs.forEach((r) => (Number(r.bil_ikon) > 0 ? String(r.peranan_ikon).split(', ') : ['tiada ikon'])
      .forEach((k) => m.set(k, (m.get(k) || 0) + 1)));
    return [...m].map(([nama, bil]) => ({ nama, bil, pct: Math.round((bil / designs.length) * 1000) / 10 }))
      .sort((a, b) => b.bil - a.bil || a.nama.localeCompare(b.nama));
  },
});

(() => {
  const F = { q: '', tema: '', susunan: '', sukar: '', isu: false };
  const COLS = 32;
  const rowsOf = (id) => { const d = dash.data(id); return d.status === 'ok' && Array.isArray(d.data) ? d.data : null; };
  const start = (tb, id, cols) => {
    tb.replaceChildren();
    const rows = rowsOf(id);
    if (!rows) POD.emptyRow(tb, cols, POD.statusMsg(id));
    return rows;
  };

  // Angka ringkasan
  const one = (name, field, fmt) => dash.draw(name, (el) => {
    const rows = rowsOf('etsy_ringkas');
    el.textContent = rows && rows[0] ? fmt(rows[0][field]) : '—';
  });
  one('etsy-k-design', 'design', (v) => String(v));
  one('etsy-k-gambar', 'gambar', (v) => String(v));
  one('etsy-k-baris', 'purata_baris', (v) => String(v));
  one('etsy-k-font', 'purata_font', (v) => String(v));
  one('etsy-k-dakwat', 'purata_dakwat', (v) => `${v}%`);
  one('etsy-k-ikon', 'pct_ikon', (v) => `${v}%`);
  one('etsy-k-isu', 'isu', (v) => String(v));

  // Listing
  dash.draw('etsy-listing-body', (tb) => {
    const rows = start(tb, 'etsy_listing', 13); if (!rows) return;
    rows.forEach((r) => {
      const tr = document.createElement('tr'); tr.dataset.key = POD.enc(r.listing);
      POD.cell(tr, r.listing, 'pod-wide'); POD.cell(tr, r.penjual);
      POD.cell(tr, r.harga_rm, 'pod-num'); POD.cell(tr, r.harga_asal_rm, 'pod-num'); POD.cell(tr, r.diskaun_pct, 'pod-num');
      POD.cell(tr, r.rating, 'pod-num'); POD.cell(tr, r.bil_rating, 'pod-num'); POD.cell(tr, r.format);
      POD.cell(tr, r.bil_design, 'pod-num'); POD.cell(tr, r.gambar); POD.cell(tr, r.dilihat);
      POD.pillCell(tr, r.bukti); POD.cell(tr, r.nota_bukti, 'pod-wide');
      tb.appendChild(tr);
    });
  });

  // Jadual kekerapan
  const freq = (name, id) => dash.draw(name, (tb) => {
    const rows = start(tb, id, 3); if (!rows) return;
    const max = Math.max(1, ...rows.map((r) => Number(r.bil) || 0));
    rows.forEach((r) => {
      const tr = document.createElement('tr'); tr.dataset.key = POD.enc(r.nama);
      POD.cell(tr, r.nama); POD.cell(tr, r.bil, 'pod-num');
      const td = document.createElement('td'); td.className = 'pod-barcell';
      const bar = document.createElement('span'); bar.className = 'etsy-bar'; bar.style.width = `${Math.round((r.bil / max) * 80)}px`;
      const t = document.createElement('span'); t.textContent = `${r.pct}%`;
      td.append(bar, t); tr.appendChild(td); tb.appendChild(tr);
    });
  });
  freq('etsy-fq-susunan', 'etsy_f_susunan');
  freq('etsy-fq-font', 'etsy_f_font');
  freq('etsy-fq-bekas', 'etsy_f_bekas');
  freq('etsy-fq-ikon', 'etsy_f_ikon');

  // Font calon
  dash.draw('etsy-font-body', (tb) => {
    const rows = start(tb, 'etsy_fonts', 8); if (!rows) return;
    rows.forEach((r) => {
      const tr = document.createElement('tr'); tr.dataset.key = POD.enc(r.kunci);
      POD.cell(tr, r.jenis); POD.cell(tr, r.ciri, 'pod-wide'); POD.cell(tr, r.bil_design, 'pod-num');
      const td = document.createElement('td'); const a = POD.link(r.url, r.font);
      if (a) td.appendChild(a); else td.textContent = r.font || '—';
      tr.appendChild(td);
      POD.cell(tr, r.pilihan, 'pod-num'); POD.cell(tr, r.sumber); POD.cell(tr, r.lesen);
      const rk = document.createElement('td'); rk.appendChild(POD.pill(String(r.risiko || '—'), null, r.risiko === 'selamat' ? 'ok' : 'warn'));
      tr.appendChild(rk); tb.appendChild(tr);
    });
  });

  // Gambar besar
  let zoomed = null;
  const zoomBox = () => document.querySelectorAll('#etsy-zoom');
  const unzoom = () => { zoomed = null; zoomBox().forEach((z) => { z.hidden = true; }); };
  const zoom = (src, cap) => { zoomed = { src, cap }; zoomBox().forEach((z) => { z.hidden = false; }); dash.draw('etsy-zoom-fig'); };
  dash.draw('etsy-zoom-fig', (fig) => {
    fig.replaceChildren();
    if (!zoomed) return;
    const img = document.createElement('img'); img.src = zoomed.src; img.alt = zoomed.cap;
    const cap = document.createElement('figcaption'); cap.textContent = zoomed.cap;
    fig.append(img, cap);
  });
  zoomBox().forEach((z) => z.addEventListener('click', (e) => { if (e.target === z || e.target.closest('.mt-zoom-close')) unzoom(); }));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && zoomed) unzoom(); });

  // Tapisan
  const match = (r) => {
    if (F.tema && r.tema !== F.tema) return false;
    if (F.susunan && r.susunan !== F.susunan) return false;
    if (F.sukar && r.kesukaran !== F.sukar) return false;
    if (F.isu && !r.isu_ayat) return false;
    const words = F.q.toLowerCase().split(/\s+/).filter(Boolean);
    if (words.length) {
      const hay = [r.id, r.ayat, r.ikon, r.jenis_font, r.font_calon, r.hiasan, r.bekas, r.rasa, r.khalayak, r.susunan, r.nota].join(' ').toLowerCase();
      if (!words.every((w) => hay.includes(w))) return false;
    }
    return true;
  };
  const redraw = () => { dash.draw('etsy-body'); dash.draw('etsy-count'); };
  document.querySelectorAll('[data-etsy-f]').forEach((el) => {
    const k = el.dataset.etsyF;
    el.addEventListener(el.type === 'search' ? 'input' : 'change', () => { F[k] = el.type === 'checkbox' ? el.checked : el.value; redraw(); });
  });
  document.querySelectorAll('.etsy-reset').forEach((b) => b.addEventListener('click', () => {
    F.q = ''; F.tema = ''; F.susunan = ''; F.sukar = ''; F.isu = false;
    document.querySelectorAll('[data-etsy-f]').forEach((el) => { if (el.type === 'checkbox') el.checked = false; else el.value = ''; });
    dash.draw('etsy-f-susunan'); redraw();
  }));
  dash.draw('etsy-f-susunan', (sel) => {
    const rows = rowsOf('etsy_f_susunan') || [];
    sel.replaceChildren(new Option('Semua jenis susunan', ''), ...rows.map((r) => new Option(`${r.nama} (${r.bil})`, r.nama)));
    sel.value = F.susunan;
    sel.onchange = () => { F.susunan = sel.value; redraw(); };
  });
  dash.draw('etsy-count', (el) => {
    const rows = rowsOf('etsy_designs');
    el.textContent = rows ? String(rows.filter(match).length) : '—';
  });

  // Jadual utama: satu baris setiap design
  dash.draw('etsy-body', (tb) => {
    const rows = start(tb, 'etsy_designs', COLS); if (!rows) return;
    const shown = rows.filter(match);
    if (!shown.length) { POD.emptyRow(tb, COLS, 'Tiada design sepadan dengan tapisan.'); return; }
    shown.forEach((r) => {
      const tr = document.createElement('tr'); tr.dataset.key = POD.enc(r.id);
      const td = document.createElement('td'); td.className = 'etsy-c-img';
      const box = document.createElement('div'); box.className = 'etsy-thumb';
      const src = POD.blob(r.img);
      if (src) {
        const b = document.createElement('button'); b.type = 'button'; b.className = 'etsy-open';
        b.setAttribute('aria-label', `Besarkan design ${r.id}`);
        const img = document.createElement('img'); img.src = src; img.loading = 'lazy'; img.alt = `Design ${r.id}: ${r.ayat}`;
        b.appendChild(img);
        b.addEventListener('click', () => zoom(src, `${r.id} · ${r.ayat} · design penjual lain, rujukan gaya sahaja`));
        box.appendChild(b);
        if (POD.likeOn) POD.likeOn(box, src, { cap: `Etsy ${r.id}: ${r.ayat}`, gaya: r.susunan, teks: r.ayat });
      } else { box.textContent = '—'; }
      td.appendChild(box); tr.appendChild(td);
      POD.cell(tr, r.id); POD.cell(tr, r.ayat, 'pod-wide'); POD.cell(tr, r.tema);
      const ltd = document.createElement('td'); ltd.className = 'etsy-c-lines';
      const wrap = document.createElement('div'); wrap.className = 'etsy-lines';
      let lines = [];
      try { lines = JSON.parse(r.baris_json || '[]'); } catch (e) { lines = []; }
      lines.forEach((l, i) => {
        const d = document.createElement('div');
        const t = document.createElement('b'); t.textContent = `${i + 1}. ${l.teks}`;
        const s = document.createElement('span'); s.textContent = ` — ${l.font} (${l.calon}) · ${l.rawatan} · ${l.peranan}`;
        d.append(t, s); wrap.appendChild(d);
      });
      if (!lines.length) wrap.textContent = '—';
      ltd.appendChild(wrap); tr.appendChild(ltd);
      POD.cell(tr, r.kata_utama); POD.cell(tr, r.bil_baris, 'pod-num'); POD.cell(tr, r.bil_perkataan, 'pod-num');
      POD.cell(tr, r.jenis_font); POD.cell(tr, r.bil_font, 'pod-num'); POD.cell(tr, r.font_calon, 'pod-wide');
      POD.cell(tr, r.ikon, 'pod-wide'); POD.cell(tr, r.peranan_ikon); POD.cell(tr, r.bekas); POD.cell(tr, r.hiasan, 'pod-wide');
      POD.cell(tr, r.susunan); POD.cell(tr, r.siluet); POD.cell(tr, r.simetri); POD.cell(tr, r.senget); POD.cell(tr, r.lengkung);
      POD.cell(tr, r.tekstur); POD.cell(tr, r.nisbah, 'pod-num'); POD.cell(tr, r.dakwat_pct, 'pod-num');
      POD.cell(tr, r.rasa); POD.cell(tr, r.khalayak); POD.cell(tr, r.isu_ayat);
      POD.cell(tr, r.skor_tiru, 'pod-num');
      const k = document.createElement('td');
      k.appendChild(POD.pill(String(r.kesukaran || '—'), null, r.kesukaran === 'Mudah' ? 'ok' : r.kesukaran === 'Sederhana' ? 'warn' : 'bad'));
      tr.appendChild(k);
      POD.cell(tr, r.status); POD.cell(tr, r.nota); POD.cell(tr, r.fail_asal); POD.cell(tr, r.kedudukan);
      tb.appendChild(tr);
    });
  });
})();
