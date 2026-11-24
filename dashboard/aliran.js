(() => {
  const POD = window.POD || {};
  const HEX = /^#[0-9a-fA-F]{6}$/;
  const BLOB = /^[0-9a-f]{32}$/;
  const txt = (v) => (v == null ? '' : String(v));
  const show = (form, state) => {
    form.querySelectorAll('[data-al-msg]').forEach((p) => { p.hidden = p.dataset.alMsg !== state; });
    form.querySelectorAll('button[type="submit"]').forEach((b) => { b.disabled = state === 'busy'; });
  };
  const nextCode = (id, prefix) => {
    const rows = (dash.data(id).data || []);
    let n = 0;
    rows.forEach((r) => { const m = new RegExp('^' + prefix + '(\\d{3,})$').exec(txt(r.id)); if (m) n = Math.max(n, Number(m[1])); });
    return prefix + String(n + 1).padStart(3, '0');
  };
  const upload = async (file) => {
    if (!file) return null;
    if (!/^image\/(png|jpeg|webp)$/.test(file.type)) throw new Error('type');
    const assets = await claude.use('assets');
    if (!assets) throw new Error('assets');
    const up = await assets.upload(file);
    return up.id;
  };
  const save = async (form, cfg) => {
    show(form, 'busy');
    try {
      if (dash.data(cfg.source).status !== 'ok') throw new Error('data');
      const f = new FormData(form);
      const row = cfg.read(f);
      if (!row) throw new Error('form');
      const file = f.get('gambar');
      const img = await upload(file && file.size ? file : null);
      if (cfg.needImg && !img) throw new Error('img');
      if (img) row.img = img;
      row.dibuat = new Date().toISOString().slice(0, 10);
      const db = await claude.use('db');
      if (!db) throw new Error('db');
      await db.doc(cfg.path + '/' + nextCode(cfg.source, cfg.prefix)).set(row);
      form.reset();
      show(form, 'ok');
    } catch (e) { show(form, 'fail'); }
  };
  let zoomed = null;
  const zoom = (src, cap) => {
    const z = document.getElementById('al-zoom'); if (!z) return;
    zoomed = { src, cap }; z.hidden = false; dash.draw('al-zoom-fig');
    const x = document.getElementById('al-zoom-close'); if (x) x.focus();
  };
  const unzoom = () => { const z = document.getElementById('al-zoom'); if (z && !z.hidden) { z.hidden = true; zoomed = null; } };
  document.querySelectorAll('#al-zoom').forEach((z) => {
    z.addEventListener('click', (e) => { if (e.target === z || e.target.id === 'al-zoom-close') unzoom(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') unzoom(); });
  });
  dash.draw('al-zoom-fig', (el) => {
    el.replaceChildren(); if (!zoomed) return;
    const im = document.createElement('img'); im.src = zoomed.src; im.alt = zoomed.cap;
    const c = document.createElement('figcaption'); c.textContent = zoomed.cap;
    el.append(im, c);
  });

  const line = (label, value) => {
    if (!txt(value)) return null;
    const p = document.createElement('div'); p.className = 'al-meta';
    const b = document.createElement('b'); b.textContent = label + ': ';
    p.append(b, document.createTextNode(txt(value)));
    return p;
  };
  const card = (r, source, path) => {
    const code = txt(r.id);
    const li = document.createElement('article'); li.className = 'al-item';
    const where = 'id=' + (POD.enc ? POD.enc(code) : code);
    const h = document.createElement('h3');
    const c = document.createElement('span'); c.className = 'al-code'; c.textContent = code;
    const n = document.createElement('span'); n.textContent = txt(r.nama) || '—';
    n.dataset.source = source; n.dataset.field = 'nama'; n.dataset.where = where;
    h.append(c, n); li.appendChild(h);
    return { li, code };
  };
  const thumb = (li, r, cap) => {
    if (!BLOB.test(txt(r.img))) return;
    const src = '/_blob/' + r.img;
    const b = document.createElement('button'); b.type = 'button'; b.className = 'al-thumb';
    b.setAttribute('aria-label', 'Besarkan gambar ' + cap);
    const im = document.createElement('img'); im.src = src; im.loading = 'lazy'; im.alt = cap;
    b.appendChild(im); b.addEventListener('click', () => zoom(src, cap)); li.appendChild(b);
  };
  const tail = (li, r, code, path) => {
    const u = POD.link ? POD.link(r.sumber, 'Sumber rujukan') : null;
    if (u) { const d = document.createElement('div'); d.appendChild(u); li.appendChild(d); }
    const nota = line('Nota', r.nota); if (nota) li.appendChild(nota);
    const del = document.createElement('button'); del.type = 'button'; del.className = 'al-del'; del.textContent = 'Padam';
    del.addEventListener('click', async () => {
      if (del.dataset.arm !== '1') { del.dataset.arm = '1'; del.textContent = 'Tekan sekali lagi untuk padam ' + code; return; }
      del.disabled = true;
      try { const db = await claude.use('db'); await db.doc(path + '/' + code).delete(); }
      catch (e) { del.disabled = false; del.dataset.arm = '0'; del.textContent = 'Tidak dipadam (hanya editor)'; }
    });
    li.appendChild(del);
  };
  const list = (source, path, body) => (el) => {
    const d = dash.data(source); el.replaceChildren();
    if (d.status !== 'ok') { const p = document.createElement('p'); p.className = 'pod-msg'; p.textContent = POD.statusMsg ? POD.statusMsg(source) : '—'; el.appendChild(p); return; }
    const rows = [...d.data].sort((a, b) => txt(a.id).localeCompare(txt(b.id), undefined, { numeric: true }));
    rows.forEach((r) => { const { li, code } = card(r, source, path); body(li, r, code); tail(li, r, code, path); el.appendChild(li); });
  };
  dash.onData(() => {
    ['gaya_daftar', 'warna_daftar'].forEach((s) => {
      const d = dash.data(s);
      document.querySelectorAll('[data-al-empty="' + s + '"]').forEach((p) => { p.hidden = !(d.status === 'ok' && d.data.length === 0); });
    });
  });

  const engine = (li, r) => {
    const b = document.createElement('span'); b.className = 'al-engine';
    const v = txt(r.enjin);
    b.textContent = v || 'Enjin tidak direkod';
    if (!v) b.dataset.none = '1';
    li.appendChild(b);
  };
  dash.draw('al-gaya-list', list('gaya_daftar', 'data/gaya/items', (li, r, code) => {
    engine(li, r);
    thumb(li, r, code + ' ' + txt(r.nama));
    [line('Jenis ayat', r.jenis), line('Panjang ayat', r.panjang), line('Ikon / hiasan', r.ikon)].forEach((x) => { if (x) li.appendChild(x); });
  }));
  dash.draw('al-warna-list', list('warna_daftar', 'data/warna/items', (li, r, code) => {
    engine(li, r);
    const cols = [r.latar].concat(Array.isArray(r.huruf) ? r.huruf : []).filter((c) => HEX.test(txt(c)));
    if (cols.length) {
      const sw = document.createElement('div'); sw.className = 'al-sw'; sw.setAttribute('role', 'img');
      sw.setAttribute('aria-label', 'Palet ' + code + ': latar ' + cols[0] + ', huruf ' + cols.slice(1).join(', '));
      cols.forEach((c) => { const s = document.createElement('span'); s.style.background = c; sw.appendChild(s); });
      li.appendChild(sw);
      const hx = document.createElement('div'); hx.className = 'al-hex';
      hx.textContent = 'Latar ' + cols[0].toUpperCase() + ' · Huruf ' + (cols.slice(1).map((c) => c.toUpperCase()).join(', ') || '—');
      li.appendChild(hx);
    }
    thumb(li, r, code + ' ' + txt(r.nama));
    [line('Jenis ayat', r.jenis), line('Gaya serasi', r.gaya)].forEach((x) => { if (x) li.appendChild(x); });
  }));

  const clean = (f, k, max) => txt(f.get(k)).trim().slice(0, max);
  const url = (f) => { const u = clean(f, 'sumber', 500); return /^https?:\/\//.test(u) ? u : ''; };
  document.querySelectorAll('#al-gaya-form').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      save(form, { source: 'gaya_daftar', path: 'data/gaya/items', prefix: 'S', needImg: true, read: (f) => {
        const nama = clean(f, 'nama', 80); if (!nama) return null;
        return { nama, jenis: clean(f, 'jenis', 40), panjang: clean(f, 'panjang', 40), ikon: clean(f, 'ikon', 200), enjin: clean(f, 'enjin', 60), sumber: url(f), nota: clean(f, 'nota', 400) };
      } });
    });
  });
  document.querySelectorAll('#al-warna-form').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      save(form, { source: 'warna_daftar', path: 'data/warna/items', prefix: 'C', needImg: false, read: (f) => {
        const nama = clean(f, 'nama', 80); const latar = clean(f, 'latar', 7);
        const huruf = clean(f, 'huruf', 60).split(/[\s,;]+/).filter(Boolean).map((c) => (c[0] === '#' ? c : '#' + c));
        if (!nama || !HEX.test(latar) || !huruf.length || huruf.length > 4 || !huruf.every((c) => HEX.test(c))) return null;
        return { nama, latar: latar.toLowerCase(), huruf: huruf.map((c) => c.toLowerCase()), jenis: clean(f, 'jenis', 40), gaya: clean(f, 'gaya', 120), enjin: clean(f, 'enjin', 60), sumber: url(f), nota: clean(f, 'nota', 400) };
      } });
    });
    // Baca warna utama daripada gambar yang dipilih, dan isi medan warna.
    const pick = form.querySelector('input[name="gambar"]');
    if (pick) pick.addEventListener('change', () => {
      const file = pick.files && pick.files[0];
      if (!file || !/^image\/(png|jpeg|webp)$/.test(file.type)) return;
      const im = new Image(); const src = URL.createObjectURL(file);
      im.onload = () => {
        try {
          const S = 80; const cv = document.createElement('canvas'); cv.width = S; cv.height = S;
          const cx = cv.getContext('2d'); cx.drawImage(im, 0, 0, S, S);
          const px = cx.getImageData(0, 0, S, S).data; const bins = new Map();
          for (let i = 0; i < px.length; i += 4) {
            if (px[i + 3] < 128) continue;
            const k = (px[i] >> 4) << 8 | (px[i + 1] >> 4) << 4 | (px[i + 2] >> 4);
            const b = bins.get(k) || [0, 0, 0, 0]; b[0] += 1; b[1] += px[i]; b[2] += px[i + 1]; b[3] += px[i + 2]; bins.set(k, b);
          }
          const top = [...bins.values()].sort((a, b) => b[0] - a[0]).map((b) => [b[1] / b[0], b[2] / b[0], b[3] / b[0], b[0]]);
          const far = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
          const keep = [];
          top.forEach((c) => { if (keep.length < 4 && c[3] >= S * S * 0.004 && keep.every((k) => far(k, c) > 60)) keep.push(c); });
          const hex = (c) => '#' + c.slice(0, 3).map((v) => Math.round(v).toString(16).padStart(2, '0')).join('');
          if (keep.length >= 2) {
            const a = form.querySelector('input[name="latar"]'); const h = form.querySelector('input[name="huruf"]');
            if (a) a.value = hex(keep[0]);
            if (h) h.value = keep.slice(1).map(hex).join(', ');
          }
        } catch (e) { /* medan kekal seperti ditaip */ }
        URL.revokeObjectURL(src);
      };
      im.onerror = () => URL.revokeObjectURL(src);
      im.src = src;
    });
  });
})();
