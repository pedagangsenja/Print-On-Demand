// Butang like (♥) untuk setiap gambar. Like disimpan di stor data/likes/items/<id blob>.
// Hanya editor dashboard boleh simpan. Claude baca stor ini sebelum jana imej AI.
(() => {
  const PATH = 'data/likes/items';
  const KEY = /^\/_blob\/([0-9a-f]+)$/;
  let seen = null; let liked = new Set();
  const likedSet = () => {
    const d = dash.data('likes');
    if (d.status !== 'ok') return null;
    if (d.data !== seen) { seen = d.data; liked = new Set(d.data.map((r) => r.id)); }
    return liked;
  };
  const pending = new Map();
  let msgT = 0;
  const showMsg = (on) => document.querySelectorAll('.pod-heart-msg').forEach((p) => { p.hidden = !on; });
  const tabOf = (btn) => {
    const s = btn.closest('.pod-tab'); if (!s) return { tab_id: '', tab: '' };
    const b = document.getElementById(s.getAttribute('aria-labelledby') || '');
    return { tab_id: s.id, tab: b ? b.textContent.trim() : s.id };
  };
  const clean = (o) => {
    const out = {};
    Object.entries(o || {}).forEach(([k, v]) => {
      if (v === undefined || v === null || v === '') return;
      out[k] = typeof v === 'number' || typeof v === 'boolean' ? v : String(v).slice(0, 500);
    });
    return out;
  };
  const press = (key, on) => document.querySelectorAll('.pod-heart').forEach((x) => {
    if (x.dataset.like === key) x.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
  // POD.heart(src, info): butang ♥ untuk satu gambar /_blob/<id>; null jika bukan blob.
  POD.heart = (src, info = {}) => {
    const m = KEY.exec(String(src || '')); if (!m) return null;
    const key = m[1];
    const b = document.createElement('button'); b.type = 'button'; b.className = 'pod-heart'; b.textContent = '♥';
    b.dataset.like = key;
    const set = likedSet();
    const on = pending.has(key) ? pending.get(key) : !!(set && set.has(key));
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    b.setAttribute('aria-label', `Suka gambar: ${info.cap || 'gambar'}`);
    b.addEventListener('click', async (ev) => {
      ev.preventDefault(); ev.stopPropagation();
      const now = b.getAttribute('aria-pressed') !== 'true';
      press(key, now); pending.set(key, now);
      let ok = true;
      try {
        const db = await claude.use('db');
        const doc = db.doc(`${PATH}/${key}`);
        if (now) await doc.set({ ...clean(info), src: m[0], ...tabOf(b), liked_at: new Date().toISOString() });
        else await doc.delete();
      } catch (e) { ok = false; }
      pending.delete(key);
      if (!ok) { press(key, !now); clearTimeout(msgT); showMsg(true); msgT = setTimeout(() => showMsg(false), 5000); }
    });
    return b;
  };
  // POD.likeOn(host, src, info): letak ♥ di penjuru kanan atas host, dan nama model (info.model) di kiri atas.
  POD.likeOn = (host, src, info) => {
    const b = POD.heart(src, info); if (!b || !host) return null;
    host.classList.add('pod-likable');
    host.querySelectorAll(':scope > .pod-model-tag').forEach((x) => x.remove());
    host.appendChild(b);
    const m = info && info.model ? String(info.model).trim() : '';
    if (m) { const t = document.createElement('span'); t.className = 'pod-model-tag'; t.textContent = m; t.title = m; host.appendChild(t); }
    return b;
  };
})();

dash.calc('likes_n', {
  inputs: ['likes'],
  title: 'Bilangan gambar disukai',
  description: 'Jumlah gambar yang ditanda ♥.',
  fn: (likes) => likes.length,
});

dash.draw('suka-n', (el) => {
  const d = dash.data('likes_n');
  el.textContent = d.status === 'ok' ? String(d.data) : '—';
});

dash.draw('suka-grid', (el) => {
  el.replaceChildren();
  const d = dash.data('likes');
  const say = (t) => { const p = document.createElement('p'); p.className = 'pod-muted'; p.textContent = t; el.appendChild(p); };
  if (d.status !== 'ok') { say(POD.statusMsg('likes')); return; }
  const rows = [...d.data].filter((r) => POD.blob(r.src)).sort((a, b) => String(b.liked_at || '').localeCompare(String(a.liked_at || '')));
  if (!rows.length) { say('Belum ada gambar disukai. Tekan ♥ pada mana-mana gambar di tab lain.'); return; }
  const tarikh = (s) => { const t = new Date(s); return isNaN(t) ? '' : t.toLocaleDateString('ms-MY', { day: 'numeric', month: 'short', year: 'numeric' }); };
  rows.forEach((r) => {
    const fig = document.createElement('figure'); fig.className = 'suka-card'; fig.dataset.key = r.id;
    const box = document.createElement('div');
    const img = document.createElement('img'); img.src = r.src; img.loading = 'lazy'; img.alt = String(r.cap || 'Gambar disukai');
    box.appendChild(img); fig.appendChild(box);
    POD.likeOn(box, r.src, { cap: r.cap, model: r.model });
    const cap = document.createElement('figcaption');
    const t = document.createElement('b'); t.textContent = String(r.cap || 'Gambar'); cap.appendChild(t);
    const meta = [r.model && `Model ${r.model}`, r.gaya && `Gaya ${r.gaya}`, r.warna && `Warna ${r.warna}`, r.teks && `"${r.teks}"`, r.seed !== undefined && `seed ${r.seed}`].filter(Boolean);
    if (meta.length) { const s = document.createElement('span'); s.textContent = meta.join(' · '); cap.appendChild(s); }
    const w = document.createElement('span'); w.className = 'pod-muted'; w.textContent = [r.tab, tarikh(r.liked_at)].filter(Boolean).join(' · '); cap.appendChild(w);
    if (r.tab_id && document.getElementById(r.tab_id)) {
      const go = document.createElement('button'); go.type = 'button'; go.className = 'suka-go'; go.textContent = `Buka tab ${r.tab || ''}`.trim();
      go.addEventListener('click', () => POD.openTab(r.tab_id, true));
      cap.appendChild(go);
    }
    fig.appendChild(cap); el.appendChild(fig);
  });
});
