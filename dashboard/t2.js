POD.t2 = { ujian: '', model: '', hasil: '', open: null, zoom: null };
POD.t2Bulan = ['Jan', 'Feb', 'Mac', 'Apr', 'Mei', 'Jun', 'Jul', 'Ogo', 'Sep', 'Okt', 'Nov', 'Dis'];
POD.t2Tarikh = (s) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s || ''); return m ? `${Number(m[3])} ${POD.t2Bulan[Number(m[2]) - 1]} ${m[1]}` : '—'; };
POD.t2Hasil = (r) => (r.lulus === true ? '1' : r.lulus === false ? '0' : 'na');
dash.calc('ai_banding', {
  title: 'AI Image Test: banding model (semua ujian)',
  description: 'Bagi setiap model AI, daripada semua ujian dan generation: imej, imej diuji (ada keputusan Lulus/Gagal), lulus, % lulus, % ejaan betul (imej yang ejaannya disemak), purata saat jana di CPU dan di GPU, bilangan ujian dan tarikh ujian terakhir. Versi warna bukan AI tidak dikira.',
  inputs: ['ai_all'],
  fn: (images) => {
    const by = new Map();
    images.filter((r) => r.ai !== false).forEach((r) => { if (!by.has(r.model)) by.set(r.model, []); by.get(r.model).push(r); });
    const avg = (xs) => (xs.length ? Math.round(xs.reduce((s, v) => s + v, 0) / xs.length) : null);
    const pct = (a, b) => (b ? Math.round((100 * a) / b) : null);
    const rows = [...by.entries()].map(([model, r]) => {
      const diuji = r.filter((x) => x.lulus === true || x.lulus === false);
      const lulus = diuji.filter((x) => x.lulus === true).length;
      const ej = r.filter((x) => x.ejaan === true || x.ejaan === false);
      const saat = (f) => avg(r.filter((x) => f(String(x.tempat || '')) && Number(x.saat) > 0).map((x) => Number(x.saat)));
      return {
        model, model_name: r[0].model_name, imej: r.length, diuji: diuji.length, lulus,
        pct_lulus: pct(lulus, diuji.length), pct_ejaan: pct(ej.filter((x) => x.ejaan === true).length, ej.length),
        saat_cpu: saat((t) => t === 'CPU'), saat_gpu: saat((t) => t.includes('GPU') || t.includes('HF')),
        ujian: new Set(r.map((x) => x.ujian)).size, tarikh_akhir: r.map((x) => x.tarikh).sort().pop(),
      };
    });
    return rows.sort((a, b) => ((b.pct_lulus ?? -1) - (a.pct_lulus ?? -1)) || (b.imej - a.imej));
  },
});
dash.calc('ai_ringkas', {
  title: 'AI Image Test: jumlah',
  description: 'Jumlah imej AI, bilangan ujian dan generation, tarikh pertama dan terakhir, dan model dengan % lulus tertinggi antara model yang sekurang-kurangnya 20 imej diuji.',
  inputs: ['ai_all', 'ai_banding'],
  fn: (images, banding) => {
    const ai = images.filter((r) => r.ai !== false);
    const d = images.map((r) => r.tarikh).filter(Boolean).sort();
    const best = banding.filter((m) => m.diuji >= 20).sort((a, b) => b.pct_lulus - a.pct_lulus)[0];
    return [{ imej: ai.length, ujian: new Set(images.map((r) => r.ujian)).size, dari: d[0] || null, hingga: d[d.length - 1] || null, terbaik: best ? best.model_name : null, terbaik_p: best ? best.pct_lulus : null }];
  },
});
POD.t2Text = (field, fmt) => (el) => { const r = POD.ok('ai_ringkas'); const v = r && r[0] ? r[0][field] : null; el.textContent = v == null ? '—' : fmt ? fmt(v) : String(v); };
dash.draw('t2-n', POD.t2Text('imej'));
dash.draw('t2-u', POD.t2Text('ujian'));
dash.draw('t2-dari', POD.t2Text('dari', POD.t2Tarikh));
dash.draw('t2-hingga', POD.t2Text('hingga', POD.t2Tarikh));
dash.draw('t2-best', POD.t2Text('terbaik'));
dash.draw('t2-best-p', POD.t2Text('terbaik_p'));
POD.mRows('t2-sum-body', 'ai_banding', 10, (tr, r) => {
  tr.dataset.key = POD.enc(r.model);
  POD.cell(tr, r.model_name).style.fontWeight = '600';
  POD.cell(tr, r.imej, 'pod-num'); POD.cell(tr, r.diuji, 'pod-num'); POD.cell(tr, r.lulus, 'pod-num');
  const p = POD.cell(tr, r.pct_lulus, 'pod-num'); p.style.fontWeight = '600';
  if (r.pct_lulus != null) p.classList.add(r.pct_lulus >= 50 ? 'mt-ok' : 'mt-bad');
  POD.cell(tr, r.pct_ejaan, 'pod-num'); POD.cell(tr, r.saat_cpu, 'pod-num'); POD.cell(tr, r.saat_gpu, 'pod-num');
  POD.cell(tr, r.ujian, 'pod-num'); POD.cell(tr, POD.t2Tarikh(r.tarikh_akhir));
});
POD.mRows('t2-aturan-body', 'aturan_belajar', 10, (tr, r) => {
  tr.dataset.key = POD.enc(r.model);
  POD.cell(tr, r.nama).style.fontWeight = '600';
  POD.cell(tr, r.rev); POD.cell(tr, r.imej_semasa, 'pod-num'); POD.cell(tr, r.lulus_semasa, 'pod-num');
  const p = POD.cell(tr, r.pct_semasa, 'pod-num'); p.style.fontWeight = '600';
  if (r.pct_semasa != null) p.classList.add(r.pct_semasa >= 50 ? 'mt-ok' : 'mt-bad');
  POD.cell(tr, r.suka, 'pod-num'); POD.cell(tr, r.tolak, 'pod-num'); POD.cell(tr, r.ubahan_dicuba, 'pod-num');
  POD.cell(tr, r.cacat_berulang, 'pod-wide'); POD.cell(tr, r.tindakan, 'pod-wide');
});
POD.mRows('t2-sk-body', 'sk_belajar', 14, (tr, r) => {
  tr.dataset.key = POD.enc(r.sk);
  POD.cell(tr, r.sk).style.fontWeight = '600';
  POD.cell(tr, r.nama); POD.cell(tr, r.langkah); POD.cell(tr, r.versi);
  POD.cell(tr, r.imej, 'pod-num'); POD.cell(tr, r.lulus, 'pod-num');
  const c = POD.cell(tr, r.cacat_sk, 'pod-num'); c.style.fontWeight = '600';
  if (r.cacat_sk != null) c.classList.add(r.cacat_sk ? 'mt-bad' : 'mt-ok');
  POD.cell(tr, r.input_rosak, 'pod-num'); POD.cell(tr, r.belum_semak, 'pod-num'); POD.cell(tr, r.tolak, 'pod-num');
  POD.cell(tr, r.suka, 'pod-num'); POD.cell(tr, r.ubahan_dicuba, 'pod-num');
  POD.cell(tr, r.cacat_berulang, 'pod-wide'); POD.cell(tr, r.tindakan, 'pod-wide');
});
POD.t2Pilih = (sel, opts, key) => {
  sel.replaceChildren(new Option('Semua', ''), ...opts.map(([v, t]) => new Option(t, v)));
  sel.value = POD.t2[key];
  sel.onchange = () => { POD.t2[key] = sel.value; if (key === 'ujian' && sel.value) POD.t2.open = new Set([sel.value]); dash.draw('t2-galeri'); dash.draw('t2-detail-body'); };
};
POD.t2Ujian = (rows) => {
  const by = new Map();
  rows.forEach((r) => {
    if (!by.has(r.ujian)) by.set(r.ujian, { id: r.ujian, nama: r.ujian_nama, nota: r.ujian_nota, standard: r.standard, jenis: r.jenis, rows: [] });
    by.get(r.ujian).rows.push(r);
  });
  const list = [...by.values()];
  list.forEach((u) => { const d = u.rows.map((r) => r.tarikh).sort(); u.dari = d[0]; u.hingga = d[d.length - 1]; });
  return list.sort((a, b) => String(b.hingga).localeCompare(String(a.hingga)) || b.id.localeCompare(a.id));
};
dash.draw('t2-f-ujian', (sel) => {
  const rows = POD.ok('ai_all') || [];
  POD.t2Pilih(sel, POD.t2Ujian(rows).map((u) => [u.id, `${POD.t2Tarikh(u.hingga)} · ${u.nama}`]), 'ujian');
});
dash.draw('t2-f-model', (sel) => {
  const m = new Map(); (POD.ok('ai_all') || []).forEach((r) => m.set(r.model, r.model_name));
  POD.t2Pilih(sel, [...m.entries()].sort((a, b) => a[1].localeCompare(b[1])), 'model');
});
POD.t2Match = (r) => (!POD.t2.model || r.model === POD.t2.model) && (!POD.t2.hasil || POD.t2Hasil(r) === POD.t2.hasil);
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
  if (POD.modelTag) POD.modelTag(wrap, z.label);
  const cap = document.createElement('figcaption'); cap.textContent = z.cap;
  fig.append(wrap, cap);
});
POD.t2El = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
POD.t2Cap = (r) => `${r.label} · ${POD.t2Tarikh(r.tarikh)} · ${r.baris || r.kad} · ${r.lulus === true ? 'Lulus' : r.lulus === false ? 'Gagal' : 'Design siap'}${r.gaya ? ' · gaya ' + r.gaya : ''}${r.sebab ? ' · ' + r.sebab : ''}${r.saat ? ' · ' + Math.round(r.saat) + ' s' : ''}`;
POD.t2Cell = (r) => {
  const td = document.createElement('td');
  const fig = POD.t2El('figure', 'mt-cell'); fig.dataset.ok = POD.t2Hasil(r);
  const src = POD.blob(r.img);
  if (src) {
    const b = POD.t2El('button'); b.type = 'button'; b.setAttribute('aria-label', `Besarkan: ${r.label}, ${r.baris || r.kad}`);
    const im = document.createElement('img'); im.src = src; im.loading = 'lazy'; im.alt = `${r.label}: ${r.teks}`;
    if (r.w && r.h) { im.width = r.w; im.height = r.h; }
    b.append(im);
    b.addEventListener('click', () => POD.t2Open(src, POD.t2Cap(r), r.label));
    fig.appendChild(b);
    if (POD.likeOn) POD.likeOn(fig, src, { cap: POD.t2Cap(r), model: r.label, gaya: r.gaya, teks: r.teks, kad: r.kad, tarikh_jana: r.tarikh, lulus: r.lulus });
  } else {
    const ph = POD.t2El('div', 't2-noimg'); ph.append(POD.t2El('span', 't2-tag', r.label), POD.t2El('span', null, 'Gambar tidak disimpan'));
    fig.appendChild(ph);
  }
  const cap = POD.t2El('figcaption', 'mt-cap');
  const v = POD.t2El('b', r.lulus === true ? 'mt-ok' : r.lulus === false ? 'mt-bad' : 'pod-muted',
    `${r.lulus === true ? '✓ Lulus' : r.lulus === false ? '✗ Gagal' : 'Siap'}${r.gaya ? ' · ' + r.gaya : ''}${r.saat ? ' · ' + Math.round(r.saat) + ' s' : ''}`);
  cap.appendChild(v);
  if (r.tanda) cap.appendChild(POD.t2El('span', null, r.tanda));
  if (r.sebab) cap.appendChild(POD.t2El('span', 'pod-muted', r.sebab));
  else if (r.nota) cap.appendChild(POD.t2El('span', 'pod-muted', r.nota));
  const siap = POD.blob(r.img_siap);
  if (siap) {
    const l = POD.t2El('button', 't2-link', 'Lihat siap cetak'); l.type = 'button';
    l.addEventListener('click', () => POD.t2Open(siap, `Siap cetak · ${POD.t2Cap(r)}`, r.label));
    cap.appendChild(l);
  }
  fig.appendChild(cap); td.appendChild(fig);
  return td;
};
POD.t2Left = (br) => {
  const first = br[0];
  const c0 = POD.t2El('td', 't2-c0');
  const src = POD.blob(first.ref_img);
  if (src) {
    const b = POD.t2El('button', 't2-refbtn'); b.type = 'button'; b.setAttribute('aria-label', `Lihat rujukan ${first.kad}`);
    const im = document.createElement('img'); im.src = src; im.alt = `Rujukan ${first.kad}`; im.loading = 'lazy';
    b.appendChild(im);
    b.addEventListener('click', () => POD.t2Open(src, `Rujukan anda · ${first.kad} · ${first.kad_name} (design orang lain, rujukan gaya sahaja)`, 'Rujukan anda'));
    const box = POD.t2El('div'); box.appendChild(b); c0.appendChild(box);
    if (POD.likeOn) POD.likeOn(box, src, { cap: `Rujukan ${first.kad} · ${first.kad_name}`, kad: first.kad, jenis: 'rujukan' });
  } else if (first.ref_nota) c0.appendChild(POD.t2El('div', 'pod-muted', `${first.ref_nota} (tiada gambar)`));
  c0.appendChild(POD.t2El('div', 't2-date', [...new Set(br.map((r) => r.tarikh))].sort().map(POD.t2Tarikh).join(' / ')));
  if (first.baris) c0.appendChild(POD.t2El('b', null, first.baris));
  if (first.teks) c0.appendChild(POD.t2El('div', 'pod-muted t2-teks', `“${first.teks}”`));
  return c0;
};
POD.t2Table = (u, rows) => {
  const cols = [...new Set(rows.map((r) => r.lajur))];
  const wrap = POD.t2El('div', 'pod-table-wrap');
  const t = POD.t2El('table', 't2-grid'); t.style.width = `${150 + cols.length * 160}px`;
  const hr = document.createElement('tr'); hr.appendChild(POD.t2El('th', 't2-c0', 'Rujukan · tarikh · ayat'));
  cols.forEach((c) => hr.appendChild(POD.t2El('th', null, c)));
  const th = document.createElement('thead'); th.appendChild(hr);
  const tb = document.createElement('tbody');
  const kads = [...new Set(rows.map((r) => r.kad))];
  kads.forEach((k) => {
    const kr = rows.filter((r) => r.kad === k);
    const f0 = kr[0];
    if (kads.length > 1 || f0.kad_name) {
      const gr = POD.t2El('tr', 't2-kadrow'); const td = POD.t2El('td'); td.colSpan = cols.length + 1;
      td.appendChild(POD.t2El('b', null, f0.kad_name && f0.kad_name !== k ? `${k} · ${f0.kad_name}` : k));
      if (f0.kad_nota) td.appendChild(POD.t2El('div', 'pod-muted', f0.kad_nota));
      gr.appendChild(td); tb.appendChild(gr);
    }
    [...new Set(kr.map((r) => r.baris))].forEach((b) => {
      const br = kr.filter((r) => r.baris === b);
      const tr = document.createElement('tr'); tr.appendChild(POD.t2Left(br));
      cols.forEach((c) => {
        const r = br.find((x) => x.lajur === c);
        if (r) tr.appendChild(POD.t2Cell(r)); else tr.appendChild(POD.t2El('td', 't2-empty', '·'));
      });
      tb.appendChild(tr);
    });
  });
  t.append(th, tb); wrap.appendChild(t);
  return wrap;
};
dash.draw('t2-galeri', (host) => {
  host.replaceChildren();
  const all = POD.ok('ai_all');
  if (!all) { host.appendChild(POD.t2El('p', 'pod-msg', POD.statusMsg('ai_all'))); return; }
  const tests = POD.t2Ujian(all);
  if (!POD.t2.open) POD.t2.open = new Set(tests.length ? [tests[0].id] : []);
  let shown = 0;
  tests.forEach((u) => {
    if (POD.t2.ujian && u.id !== POD.t2.ujian) return;
    const rows = u.rows.filter(POD.t2Match).sort((a, b) => a.urut - b.urut);
    if (!rows.length) return;
    shown += 1;
    const tested = u.rows.filter((r) => r.lulus === true || r.lulus === false);
    const ok = tested.filter((r) => r.lulus === true).length;
    const d = POD.t2El('details', 't2-test'); d.dataset.ujian = u.id;
    d.open = POD.t2.open.has(u.id);
    const s = document.createElement('summary');
    s.append(POD.t2El('span', 't2-date', u.dari === u.hingga ? POD.t2Tarikh(u.hingga) : `${POD.t2Tarikh(u.dari)} – ${POD.t2Tarikh(u.hingga)}`),
      POD.t2El('b', null, ` ${u.nama}`),
      POD.t2El('span', 'pod-muted', ` · ${u.rows.length} imej${tested.length ? ` · ${ok}/${tested.length} lulus` : ' · design siap'}`),
      POD.t2El('span', 'pod-pill', u.jenis));
    d.appendChild(s);
    const body = POD.t2El('div');
    body.appendChild(POD.t2El('p', 'pod-muted', `${u.nota} Standard: ${u.standard}.`));
    d.addEventListener('toggle', () => {
      if (d.open) { POD.t2.open.add(u.id); if (body.childElementCount < 2) body.appendChild(POD.t2Table(u, rows)); } else POD.t2.open.delete(u.id);
    });
    if (d.open) body.appendChild(POD.t2Table(u, rows));
    d.appendChild(body); host.appendChild(d);
  });
  if (!shown) host.appendChild(POD.t2El('p', 'pod-msg', 'Tiada imej untuk pilihan ini.'));
});
dash.draw('t2-detail-body', (tb) => {
  const rows = POD.ok('ai_all'); tb.replaceChildren();
  if (!rows) { POD.emptyRow(tb, 11, POD.statusMsg('ai_all')); return; }
  const list = rows.filter((r) => (!POD.t2.ujian || r.ujian === POD.t2.ujian) && POD.t2Match(r))
    .sort((a, b) => String(b.tarikh).localeCompare(String(a.tarikh)) || b.ujian.localeCompare(a.ujian) || (a.urut - b.urut));
  if (!list.length) { POD.emptyRow(tb, 11, 'Tiada imej untuk pilihan ini.'); return; }
  list.forEach((r) => {
    const tr = document.createElement('tr'); tr.dataset.key = POD.enc(r.key);
    POD.cell(tr, POD.t2Tarikh(r.tarikh)); POD.cell(tr, r.ujian_nama); POD.cell(tr, r.label); POD.cell(tr, r.tempat);
    POD.cell(tr, r.baris || r.kad);
    const e = POD.cell(tr, r.ejaan === true ? '✓' : r.ejaan === false ? '✗' : '—'); if (r.ejaan != null) e.className = r.ejaan ? 'mt-ok' : 'mt-bad';
    POD.cell(tr, r.gaya, 'pod-num');
    const l = POD.cell(tr, r.lulus === true ? 'Lulus' : r.lulus === false ? 'Gagal' : 'Siap');
    l.className = r.lulus === true ? 'mt-ok' : r.lulus === false ? 'mt-bad' : 'pod-muted'; l.style.fontWeight = '600';
    POD.cell(tr, [r.tanda, r.sebab || r.nota].filter(Boolean).join(' · '), 'pod-wide');
    POD.cell(tr, r.saat, 'pod-num');
    POD.cell(tr, r.standard);
    tb.appendChild(tr);
  });
});
(() => {
  const h = document.getElementById('t2-f-hasil');
  if (h) h.addEventListener('change', () => { POD.t2.hasil = h.value; dash.draw('t2-galeri'); dash.draw('t2-detail-body'); });
  const z = document.getElementById('t2-zoom');
  if (z) z.addEventListener('click', (e) => { if (e.target === z || e.target.id === 't2-zoom-close') POD.t2Close(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') POD.t2Close(); });
})();
