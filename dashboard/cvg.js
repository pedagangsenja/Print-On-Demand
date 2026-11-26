(() => {
  const na = (v) => (v == null || v === '' ? 'belum' : String(v));
  const dash0 = (v) => (v == null || v === '' ? '—' : String(v));
  const one = (name, field, dev) => dash.draw(name, (el) => {
    const rows = POD.ok('cvg_peranti'); const r = rows && rows.find((x) => x.peranti === dev);
    el.textContent = r ? String(r[field]) : '—';
  });
  one('cvg-cpu-n', 'imej', 'CPU'); one('cvg-gpu-n', 'imej', 'GPU'); one('cvg-gpu-status', 'status', 'GPU'); one('cvg-hf-n', 'imej', 'GPU HF');
  POD.mRows('cvg-peranti-body', 'cvg_peranti', 5, (tr, r) => {
    tr.dataset.key = POD.enc(r.peranti);
    const m = POD.cell(tr, r.peranti); m.style.fontWeight = '600';
    POD.cell(tr, r.tempat); POD.cell(tr, r.butiran, 'pod-wide'); POD.cell(tr, String(r.imej), 'pod-num'); POD.cell(tr, r.status);
  });
  POD.mRows('cvg-enjin-body', 'cvg_enjin', 10, (tr, r) => {
    tr.dataset.key = POD.enc(r.enjin);
    const m = POD.cell(tr, r.enjin); m.style.fontWeight = '600';
    POD.cell(tr, dash0(r.cpu_ejaan), 'pod-num'); POD.cell(tr, na(r.gpu_ejaan), 'pod-num'); POD.cell(tr, na(r.hf_ejaan), 'pod-num');
    POD.cell(tr, dash0(r.cpu_saat), 'pod-num'); POD.cell(tr, na(r.gpu_saat), 'pod-num');
    POD.cell(tr, na(r.hf_saat), 'pod-num'); POD.cell(tr, na(r.gpu_laju_x), 'pod-num'); POD.cell(tr, na(r.hf_laju_x), 'pod-num'); POD.cell(tr, r.gaya_cpu, 'pod-wide');
  });
  POD.mRows('cvg-ayat-body', 'cvg_ayat', 10, (tr, r) => {
    tr.dataset.key = POD.enc(r.enjin);
    const m = POD.cell(tr, r.enjin); m.style.fontWeight = '600';
    ['P', 'D', 'L'].forEach((a) => { POD.cell(tr, dash0(r['cpu_' + a]), 'pod-num'); POD.cell(tr, na(r['gpu_' + a]), 'pod-num'); POD.cell(tr, na(r['hf_' + a]), 'pod-num'); });
  });
  POD.mRows('cvg-imej-body', 'cvg_imej', 12, (tr, r) => {
    tr.dataset.key = POD.enc(r.kunci);
    POD.cell(tr, r.enjin); POD.cell(tr, r.ayat); POD.cell(tr, String(r.seed), 'pod-num');
    POD.cell(tr, dash0(r.cpu_saat), 'pod-num'); POD.cell(tr, dash0(r.cpu_ejaan)); POD.cell(tr, dash0(r.cpu_sebab), 'pod-wide');
    POD.cell(tr, na(r.gpu_saat), 'pod-num'); POD.cell(tr, na(r.gpu_ejaan)); POD.cell(tr, na(r.gpu_sebab), 'pod-wide');
    POD.cell(tr, na(r.hf_saat), 'pod-num'); POD.cell(tr, na(r.hf_ejaan)); POD.cell(tr, na(r.hf_sebab), 'pod-wide');
  });
})();
(() => {
  const na = (v) => (v == null || v === '' ? 'belum' : String(v));
  const box = (text) => {
    const d = document.createElement('div'); d.textContent = text;
    Object.assign(d.style, { aspectRatio: '3 / 4', display: 'grid', placeItems: 'center', border: '1px dashed var(--color-border-line)', borderRadius: 'var(--cds-radius)', color: 'var(--color-fg-muted)', fontSize: 'var(--cds-font-size-caption)' });
    return d;
  };
  dash.draw('cvg-galeri', (el) => {
    const rows = POD.ok('cvg_imej'); const dev = POD.ok('cvg_peranti') || [];
    el.replaceChildren();
    if (!rows) { el.textContent = POD.statusMsg('cvg_imej'); return; }
    const z = document.createElement('div'); z.className = 'mt-zoom'; z.hidden = true;
    z.setAttribute('role', 'dialog'); z.setAttribute('aria-modal', 'true'); z.setAttribute('aria-label', 'Gambar besar');
    const zf = document.createElement('figure'); const zi = document.createElement('img'); zi.alt = ''; const zc = document.createElement('figcaption');
    const zb = document.createElement('button'); zb.type = 'button'; zb.className = 'mt-zoom-close'; zb.textContent = 'Tutup ✕';
    zf.append(zi, zc); z.append(zf, zb);
    const close = () => { z.hidden = true; zi.removeAttribute('src'); };
    z.addEventListener('click', (e) => { if (e.target === z || e.target === zb) close(); });
    z.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
    const zoom = (src, cap) => { zi.src = src; zc.textContent = cap; z.hidden = false; zb.focus(); };
    const pic = (src, alt, cap) => {
      const img = document.createElement('img'); img.src = src; img.loading = 'lazy'; img.alt = alt;
      img.addEventListener('click', () => zoom(src, cap)); return img;
    };
    const ref = POD.blob((dev.find((r) => r.peranti === 'CPU') || {}).ref_img);
    if (ref) {
      const fig = document.createElement('figure'); fig.className = 'p9-card';
      fig.style.gridTemplateColumns = '1fr 1fr 1fr';
      fig.append(pic(ref, 'Rujukan gaya K6', 'Rujukan gaya K6 (IMG_5734), rujukan sahaja'), box('Ayat rujukan tidak disalin'), box('3 ayat baharu, gaya sama'));
      const cap = document.createElement('figcaption'); cap.className = 'pod-muted'; cap.textContent = 'Rujukan gaya K6 (IMG_5734)';
      fig.appendChild(cap); el.appendChild(fig);
    }
    let last = null;
    rows.forEach((r) => {
      if (r.enjin !== last) { last = r.enjin; const h = document.createElement('h4'); h.textContent = r.enjin; h.style.gridColumn = '1 / -1'; h.style.margin = 'var(--cds-gap-md) 0 0'; el.appendChild(h); }
      const fig = document.createElement('figure'); fig.className = 'p9-card'; fig.style.gridTemplateColumns = '1fr 1fr 1fr';
      [['cpu', 'CPU'], ['gpu', 'GPU'], ['hf', 'GPU HF']].forEach(([k, lab]) => {
        const src = POD.blob(r[k + '_img']);
        const cap = `${r.enjin} · ${r.ayat} · seed ${r.seed} · ${lab}: ${na(r[k + '_ejaan'])}${r[k + '_sebab'] ? ' (' + r[k + '_sebab'] + ')' : ''}`;
        fig.appendChild(src ? pic(src, cap, cap) : box(`${lab}: belum`));
      });
      const c = document.createElement('figcaption'); c.className = 'pod-muted';
      c.textContent = `${r.ayat}, seed ${r.seed} · CPU ${na(r.cpu_ejaan)}${r.cpu_saat != null ? ' ' + Math.round(r.cpu_saat) + ' s' : ''} · GPU ${na(r.gpu_ejaan)} · GPU HF ${na(r.hf_ejaan)}${r.hf_saat != null ? ' ' + Math.round(r.hf_saat) + ' s' : ''}${r.cpu_sebab ? ' · CPU: ' + r.cpu_sebab : ''}${r.hf_sebab ? ' · HF: ' + r.hf_sebab : ''}`;
      fig.appendChild(c); el.appendChild(fig);
    });
    el.appendChild(z);
  });
})();
