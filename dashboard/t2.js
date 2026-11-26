POD.t2 = { kad: '', ayat: '', model: '', hasil: '', zoom: null };
POD.t2Models = ['klein4b', 'schnell', 'zturbo', 'ernie', 'moss'];
dash.calc('ai2_summary', {
  title: 'AI Image Test 2: ringkasan setiap model',
  description: 'Bagi setiap model: imej lulus daripada 30, ejaan betul bagi setiap panjang ayat (daripada 10), imej yang ada teks rawak, gaya yang layak (4 imej ayat pendek dan sederhana semua lulus) dan purata minit setiap imej. Model yang tidak diuji di hujung.',
  inputs: ['ai2_images', 'ai2_models'],
  fn: (images, models) => {
    const kads = [...new Set(images.map((x) => x.kad))].sort();
    const rows = models.map((m) => {
      const r = images.filter((x) => x.model === m.model);
      if (!r.length) return { model: m.model, model_name: m.model_name, lulus: null, ejaan_p: null, ejaan_d: null, ejaan_l: null, rawak: null, layak: `${m.status} (${m.note})`, purata_min: null, versi: m.versi, diuji: 0, order: m.model_order };
      const ej = (a) => r.filter((x) => x.ayat === a && x.g1).length;
      const layak = kads.filter((k) => { const pd = r.filter((x) => x.kad === k && x.ayat !== 'L'); return pd.length > 0 && pd.every((x) => x.lulus); });
      const avg = r.reduce((s, x) => s + Number(x.saat), 0) / r.length;
      return { model: m.model, model_name: m.model_name, lulus: r.filter((x) => x.lulus).length, ejaan_p: ej('P'), ejaan_d: ej('D'), ejaan_l: ej('L'), rawak: r.filter((x) => !x.g2).length, layak: layak.length ? layak.join(', ') : 'Tiada', purata_min: Math.round(avg / 6) / 10, versi: m.versi, diuji: 1, order: m.model_order };
    });
    return rows.sort((a, b) => (b.diuji - a.diuji) || ((b.lulus || 0) - (a.lulus || 0)) || (a.order - b.order));
  },
});
dash.calc('ai2_bykad', {
  title: 'AI Image Test 2: lulus ikut gaya',
  description: 'Bagi setiap gaya (K1–K5): imej lulus daripada 6 bagi setiap model, dan model yang layak (4 imej ayat pendek dan sederhana semua lulus).',
  inputs: ['ai2_images', 'ai2_refs'],
  fn: (images, refs) => {
    const models = ['klein4b', 'schnell', 'zturbo', 'ernie', 'moss'];
    const names = new Map(images.map((x) => [x.model, x.model_name]));
    return refs.map((ref) => {
      const row = { kad: ref.kad, kad_name: ref.kad_name };
      const layak = [];
      models.forEach((m) => {
        const r = images.filter((x) => x.model === m && x.kad === ref.kad);
        const pd = r.filter((x) => x.ayat !== 'L');
        row[m] = r.filter((x) => x.lulus).length;
        row[`${m}_layak`] = pd.length > 0 && pd.every((x) => x.lulus);
        if (row[`${m}_layak`]) layak.push(names.get(m));
      });
      row.layak = layak.length ? layak.join(', ') : 'Tiada';
      return row;
    });
  },
});
dash.calc('ai2_totals', {
  title: 'AI Image Test 2: jumlah',
  description: 'Jumlah imej, jumlah lulus, dan model dengan imej lulus terbanyak.',
  inputs: ['ai2_images'],
  fn: (images) => {
    const by = new Map();
    images.forEach((x) => by.set(x.model_name, (by.get(x.model_name) || 0) + (x.lulus ? 1 : 0)));
    const best = [...by.entries()].sort((a, b) => b[1] - a[1])[0] || [null, null];
    return [{ imej: images.length, lulus: images.filter((x) => x.lulus).length, terbaik: best[0], terbaik_lulus: best[1] }];
  },
});
POD.t2Text = (field) => (el) => { const r = POD.ok('ai2_totals'); el.textContent = r && r[0] && r[0][field] != null ? String(r[0][field]) : '—'; };
dash.draw('t2-n', POD.t2Text('imej'));
dash.draw('t2-ok', POD.t2Text('lulus'));
dash.draw('t2-best', POD.t2Text('terbaik'));
dash.draw('t2-best-n', POD.t2Text('terbaik_lulus'));
POD.mRows('t2-sum-body', 'ai2_summary', 9, (tr, r) => {
  tr.dataset.key = POD.enc(r.model);
  POD.cell(tr, r.model_name).style.fontWeight = '600';
  POD.cell(tr, r.lulus, 'pod-num').style.fontWeight = '600';
  POD.cell(tr, r.ejaan_p, 'pod-num'); POD.cell(tr, r.ejaan_d, 'pod-num'); POD.cell(tr, r.ejaan_l, 'pod-num');
  POD.cell(tr, r.rawak, 'pod-num');
  const l = POD.cell(tr, r.layak); l.className = !r.diuji ? 'pod-muted' : r.layak === 'Tiada' ? 'mt-bad' : 'mt-ok';
  POD.cell(tr, r.purata_min, 'pod-num');
  POD.cell(tr, r.versi);
});
POD.mRows('t2-kad-body', 'ai2_bykad', 7, (tr, r) => {
  tr.dataset.key = POD.enc(r.kad);
  POD.cell(tr, `${r.kad} · ${r.kad_name}`).style.fontWeight = '600';
  POD.t2Models.forEach((m) => {
    const td = POD.cell(tr, r[m], 'pod-num');
    if (r[`${m}_layak`]) { td.classList.add('mt-ok'); td.style.fontWeight = '600'; } else if (r[m] === 0) td.classList.add('pod-muted');
  });
  const l = POD.cell(tr, r.layak); if (r.layak === 'Tiada') l.className = 'mt-bad';
});
POD.t2Names = { klein4b: 'FLUX.2 klein 4B', schnell: 'FLUX.1-schnell', zturbo: 'Z-Image-Turbo', ernie: 'ERNIE-Image-Turbo', moss: 'MOSS + LoRA' };
POD.t2Label = (r) => POD.t2Names[r.model] || r.model_name;
POD.t2Open = (src, cap, label) => {
  const z = document.getElementById('t2-zoom'); if (!z) return;
  POD.t2.zoom = { src, cap, label }; z.hidden = false; dash.draw('t2-zoom');
  const c = document.getElementById('t2-zoom-close'); if (c) c.focus();
};
POD.t2Close = () => { const z = document.getElementById('t2-zoom'); if (z && !z.hidden) { z.hidden = true; POD.t2.zoom = null; } };
dash.draw('t2-zoom', (fig) => {
  fig.replaceChildren();
  const z = POD.t2.zoom; if (!z) return;
  const wrap = document.createElement('div'); wrap.className = 't2-zoomwrap';
  const im = document.createElement('img'); im.src = z.src; im.alt = z.cap; wrap.appendChild(im);
  if (z.label) { const tag = document.createElement('span'); tag.className = 't2-tag t2-tag-big'; tag.textContent = z.label; wrap.appendChild(tag); }
  const cap = document.createElement('figcaption'); cap.textContent = z.cap;
  fig.append(wrap, cap);
});
dash.draw('t2-grid', (tb) => {
  const rows = POD.ok('ai2_images'); tb.replaceChildren();
  if (!rows) { POD.emptyRow(tb, 6, POD.statusMsg('ai2_images')); return; }
  const refs = new Map((POD.ok('ai2_refs') || []).map((x) => [x.kad, x]));
  const by = new Map(rows.map((r) => [`${r.model}|${r.id}`, r]));
  const f = POD.t2;
  let shown = 0;
  [...new Set(rows.map((r) => r.kad))].sort().forEach((k) => {
    if (f.kad && k !== f.kad) return;
    const ref = refs.get(k);
    const hr = document.createElement('tr'); hr.className = 't2-kadrow';
    const td = document.createElement('td'); td.colSpan = 6;
    const wrap = document.createElement('div'); wrap.className = 't2-kadhead';
    if (ref && POD.blob(ref.ref_img)) {
      const b = document.createElement('button'); b.type = 'button'; b.className = 't2-refbtn';
      b.setAttribute('aria-label', `Lihat rujukan ${k}`);
      const im = document.createElement('img'); im.src = ref.ref_img; im.alt = `Rujukan ${k}`; im.loading = 'lazy';
      b.appendChild(im);
      b.addEventListener('click', () => POD.t2Open(ref.ref_img, `Rujukan anda · ${k} · ${ref.kad_name} (design orang lain, rujukan gaya sahaja)`, 'Rujukan anda'));
      wrap.appendChild(b);
    }
    const txt = document.createElement('div');
    const t = document.createElement('b'); t.textContent = `${k} · ${ref ? ref.kad_name : ''}`;
    const s = document.createElement('div'); s.className = 'pod-muted'; s.textContent = ref ? `Ciri teras: ${ref.teras}` : '';
    txt.append(t, s); wrap.appendChild(txt); td.appendChild(wrap); hr.appendChild(td); tb.appendChild(hr);
    ['P', 'D', 'L'].forEach((a) => {
      if (f.ayat && a !== f.ayat) return;
      [42, 7].forEach((seed) => {
        const id = `${k}${a}_s${seed}`;
        const first = rows.find((r) => r.id === id);
        if (!first) return;
        const tr = document.createElement('tr');
        const c0 = document.createElement('td'); c0.className = 't2-c0';
        const b0 = document.createElement('b'); b0.textContent = `${first.ayat_name} · seed ${seed}`;
        const p0 = document.createElement('div'); p0.className = 'pod-muted'; p0.textContent = `“${first.text}”`;
        c0.append(b0, p0); tr.appendChild(c0);
        POD.t2Models.forEach((m) => {
          const r = by.get(`${m}|${id}`); const cell = document.createElement('td');
          if (!r) { cell.textContent = '—'; tr.appendChild(cell); return; }
          const fig = document.createElement('figure'); fig.className = 'mt-cell'; fig.dataset.ok = r.lulus ? '1' : '0';
          const src = POD.blob(r.img);
          if (src) {
            const b = document.createElement('button'); b.type = 'button';
            b.setAttribute('aria-label', `Besarkan: ${r.model_name}, ${id}`);
            const im = document.createElement('img'); im.src = src; im.loading = 'lazy'; im.alt = `${r.model_name}: ${r.text}`; im.width = r.w; im.height = r.h;
            const tag = document.createElement('span'); tag.className = 't2-tag'; tag.textContent = POD.t2Label(r);
            b.append(im, tag);
            b.addEventListener('click', () => POD.t2Open(src, `${r.model_name} · ${r.kad} ${r.ayat_name} · seed ${r.seed} · ${r.lulus ? 'Lulus' : 'Gagal'} · gaya ${r.gaya}${r.sebab ? ' · ' + r.sebab : ''} · ${r.saat} s`, POD.t2Label(r)));
            fig.appendChild(b);
          }
          const cap = document.createElement('figcaption'); cap.className = 'mt-cap';
          const v = document.createElement('b'); v.className = r.lulus ? 'mt-ok' : 'mt-bad';
          v.textContent = `${r.lulus ? '✓ Lulus' : '✗ Gagal'} · ${r.gaya}`;
          cap.appendChild(v);
          if (r.sebab) { const sb = document.createElement('span'); sb.className = 'pod-muted'; sb.textContent = r.sebab; cap.appendChild(sb); }
          fig.appendChild(cap); cell.appendChild(fig); tr.appendChild(cell);
        });
        tb.appendChild(tr); shown += 1;
      });
    });
  });
  if (!shown) POD.emptyRow(tb, 6, 'Tiada imej untuk pilihan ini.');
});
dash.draw('t2-detail-body', (tb) => {
  const rows = POD.ok('ai2_images'); tb.replaceChildren();
  if (!rows) { POD.emptyRow(tb, 11, POD.statusMsg('ai2_images')); return; }
  const f = POD.t2;
  const list = rows.filter((r) => (!f.model || r.model === f.model) && (f.hasil === '' || (r.lulus ? '1' : '0') === f.hasil))
    .sort((a, b) => (a.model_order - b.model_order) || a.kad.localeCompare(b.kad) || ('PDL'.indexOf(a.ayat) - 'PDL'.indexOf(b.ayat)) || (b.seed - a.seed));
  if (!list.length) { POD.emptyRow(tb, 11, 'Tiada imej untuk pilihan ini.'); return; }
  const yes = (tr, v) => { const td = POD.cell(tr, v ? '✓' : '✗'); td.className = v ? 'mt-ok' : 'mt-bad'; };
  list.forEach((r) => {
    const tr = document.createElement('tr'); tr.dataset.key = POD.enc(r.key);
    POD.cell(tr, r.model_name); POD.cell(tr, r.id); POD.cell(tr, r.ayat_name);
    yes(tr, r.g1); yes(tr, r.g2); yes(tr, r.g3); yes(tr, r.teras);
    POD.cell(tr, r.gaya, 'pod-num');
    const l = POD.cell(tr, r.lulus ? 'Lulus' : 'Gagal'); l.className = r.lulus ? 'mt-ok' : 'mt-bad'; l.style.fontWeight = '600';
    POD.cell(tr, r.sebab, 'pod-wide'); POD.cell(tr, r.saat, 'pod-num');
    tb.appendChild(tr);
  });
});
(() => {
  const on = (id, fn) => { const el = document.getElementById(id); if (el) el.addEventListener('change', () => fn(el.value)); };
  on('t2-f-kad', (v) => { POD.t2.kad = v; dash.draw('t2-grid'); });
  on('t2-f-ayat', (v) => { POD.t2.ayat = v; dash.draw('t2-grid'); });
  on('t2-f-model', (v) => { POD.t2.model = v; dash.draw('t2-detail-body'); });
  on('t2-f-hasil', (v) => { POD.t2.hasil = v; dash.draw('t2-detail-body'); });
  const z = document.getElementById('t2-zoom');
  if (z) z.addEventListener('click', (e) => { if (e.target === z || e.target.id === 't2-zoom-close') POD.t2Close(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') POD.t2Close(); });
})();
