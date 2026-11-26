(() => {
  const na = (v) => (v == null || v === '' ? 'belum' : String(v));
  const dash0 = (v) => (v == null || v === '' ? '—' : String(v));
  const masa = (s) => { if (s == null || s === '') return '—'; const n = Math.round(Number(s)); return n >= 60 ? `${Math.floor(n / 60)} min ${n % 60} s` : `${n} saat`; };
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  const frac = (rows, f) => { let a = 0, b = 0; rows.forEach((r) => { const m = String(r[f] || '').match(/^(\d+)\/(\d+)$/); if (m) { a += +m[1]; b += +m[2]; } }); return b ? `${a}/${b}` : '—'; };
  const gpuRows = () => (POD.ok('cvg_enjin') || []).filter((r) => r.hf_n > 0);
  const zoomBox = (host) => {
    const z = el('div', 'mt-zoom'); z.hidden = true;
    z.setAttribute('role', 'dialog'); z.setAttribute('aria-modal', 'true'); z.setAttribute('aria-label', 'Gambar besar');
    const f = el('figure'); const i = el('img'); i.alt = ''; const c = el('figcaption'); const b = el('button', 'mt-zoom-close', 'Tutup ✕'); b.type = 'button';
    f.append(i, c); z.append(f, b); host.appendChild(z);
    const close = () => { z.hidden = true; i.removeAttribute('src'); };
    z.addEventListener('click', (e) => { if (e.target === z || e.target === b) close(); });
    z.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
    return (src, cap) => { i.src = src; c.textContent = cap; z.hidden = false; b.focus(); };
  };
  const pic = (src, cap, zoom) => { const i = el('img'); i.src = src; i.loading = 'lazy'; i.alt = cap; i.addEventListener('click', () => zoom(src, cap)); return i; };

  dash.draw('cvg-kali', (e) => { const r = gpuRows(); if (!r.length) { e.textContent = '—'; return; } const k = r.map((x) => x.hf_laju_x); const lo = Math.min(...k), hi = Math.max(...k); e.textContent = lo === hi ? `${lo} kali` : `${lo}–${hi} kali`; });
  dash.draw('cvg-ok-cpu', (e) => { e.textContent = frac(gpuRows(), 'hf_cpu_ejaan'); });
  dash.draw('cvg-ok-gpu', (e) => { e.textContent = frac(gpuRows(), 'hf_ejaan_sama'); });
  dash.draw('cvg-kaggle', (e) => { const r = (POD.ok('cvg_peranti') || []).find((x) => x.peranti === 'GPU'); e.textContent = r ? r.status : '—'; });

  dash.draw('cvg-cards', (host) => {
    host.replaceChildren();
    const rows = POD.ok('cvg_enjin'); if (!rows) { host.textContent = POD.statusMsg('cvg_enjin'); return; }
    gpuRows().forEach((r) => {
      const c = el('div', 'cvg-card'); c.appendChild(el('h3', null, r.enjin));
      const vs = el('div', 'cvg-vs');
      [['CPU', r.hf_cpu_saat, r.hf_cpu_ejaan], ['GPU', r.hf_saat_sama, r.hf_ejaan_sama]].forEach(([lab, s, ok]) => {
        const col = el('div', 'cvg-col'); col.append(el('span', 'cvg-lab', lab), el('span', 'cvg-big', masa(s)), el('span', 'pod-muted', 'setiap imej'), el('span', null, `Ejaan betul ${ok}`));
        vs.appendChild(col);
      });
      const bars = el('div', 'cvg-bars');
      [['CPU', 100, 0], ['GPU', Math.max(100 * r.hf_saat_sama / r.hf_cpu_saat, 0.5), 1]].forEach(([lab, w, ci]) => {
        const b = el('div', 'cvg-bar'); const s = el('span'); s.style.width = `${w}%`; s.style.background = dash.colors[ci]; b.appendChild(s);
        bars.append(el('span', null, lab), b);
      });
      c.append(vs, bars, el('p', 'cvg-verdict', `GPU ${r.hf_laju_x} kali lebih laju`));
      host.appendChild(c);
    });
    if (!host.children.length) host.textContent = 'Belum ada enjin yang diuji di GPU.';
  });

  dash.draw('cvg-pairs', (host) => {
    host.replaceChildren();
    const rows = POD.ok('cvg_banding'); if (!rows) { host.textContent = POD.statusMsg('cvg_banding'); return; }
    const zoom = zoomBox(host); let last = null;
    rows.forEach((r) => {
      if (r.enjin !== last) { last = r.enjin; host.appendChild(el('h3', null, r.enjin)); }
      const fig = el('figure', 'cvg-pair');
      fig.appendChild(el('figcaption', null, `${r.ayat}: "${r.teks}"`));
      [['CPU', r.cpu_saat, r.cpu_ejaan, r.cpu_sebab, r.cpu_img], [r.gpu === 'GPU HF' ? 'GPU' : r.gpu, r.gpu_saat, r.gpu_ejaan, r.gpu_sebab, r.gpu_img]].forEach(([lab, s, ok, why, img]) => {
        const shot = el('div', 'cvg-shot'); const src = POD.blob(img);
        const cap = `${r.enjin} · ${r.ayat} · ${lab} · ${masa(s)}`;
        if (src) shot.appendChild(pic(src, cap, zoom));
        shot.appendChild(el('b', null, `${lab} · ${masa(s)}`));
        shot.appendChild(ok === 'Lulus' ? el('span', 'cvg-ok', '✓ Ejaan betul') : el('span', 'cvg-bad', `✗ ${why || 'Ejaan salah'}`));
        fig.appendChild(shot);
      });
      host.appendChild(fig);
    });
  });

  POD.mRows('cvg-enjin-body', 'cvg_enjin', 4, (tr, r) => {
    tr.dataset.key = POD.enc(r.enjin);
    const m = POD.cell(tr, r.enjin); m.style.fontWeight = '600';
    POD.cell(tr, dash0(r.cpu_ejaan), 'pod-num'); POD.cell(tr, masa(r.cpu_saat), 'pod-num'); POD.cell(tr, r.gaya_cpu, 'pod-wide');
  });
  POD.mRows('cvg-imej-body', 'cvg_imej', 9, (tr, r) => {
    tr.dataset.key = POD.enc(r.kunci);
    POD.cell(tr, r.enjin); POD.cell(tr, r.ayat); POD.cell(tr, String(r.seed), 'pod-num');
    POD.cell(tr, masa(r.cpu_saat), 'pod-num'); POD.cell(tr, dash0(r.cpu_ejaan)); POD.cell(tr, dash0(r.cpu_sebab), 'pod-wide');
    POD.cell(tr, r.hf_saat == null ? '—' : masa(r.hf_saat), 'pod-num'); POD.cell(tr, dash0(r.hf_ejaan)); POD.cell(tr, dash0(r.hf_sebab), 'pod-wide');
  });
  dash.draw('cvg-galeri', (host) => {
    host.replaceChildren();
    const rows = POD.ok('cvg_imej'); if (!rows) { host.textContent = POD.statusMsg('cvg_imej'); return; }
    const zoom = zoomBox(host); let last = null;
    rows.forEach((r) => {
      const src = POD.blob(r.cpu_img); if (!src) return;
      if (r.enjin !== last) { last = r.enjin; const h = el('h4', null, r.enjin); h.style.gridColumn = '1 / -1'; h.style.margin = 'var(--cds-gap-md) 0 0'; host.appendChild(h); }
      const shot = el('div', 'cvg-shot'); const cap = `${r.enjin} · ${r.ayat} · seed ${r.seed} · ${masa(r.cpu_saat)}`;
      shot.append(pic(src, cap, zoom), el('span', null, `${r.ayat}, seed ${r.seed}`), r.cpu_ejaan === 'Lulus' ? el('span', 'cvg-ok', '✓ Ejaan betul') : el('span', 'cvg-bad', `✗ ${r.cpu_sebab || 'Ejaan salah'}`));
      host.appendChild(shot);
    });
  });
})();
