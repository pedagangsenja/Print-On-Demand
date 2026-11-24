"""Master table model AI: gabung dataset lesen (ai_licenses) dengan dataset ujian (model_compare).

Input  : data/export/models/ai_licenses.json   (34 model: lesen, kuota GPU, VRAM)
         data/export/models/model_compare.json (24 baris ujian: skor tulisan, kelajuan)
Output : data/export/models/master_models.json   (dataset dashboard `master_models`)
         data/export/models/model_notes.json     (dataset dashboard `model_notes`)
Jalankan: python3 scripts/build_master_models.py
"""
import json, pathlib, re

BASE = pathlib.Path(__file__).resolve().parent.parent
MODELS = BASE / 'data/export/models'

# nama dalam model_compare -> nama dalam ai_licenses
NAME_MAP = {
    'FLUX.2 klein 4B (sekarang)': 'FLUX.2 [klein] 4B',
    'MOSS-Image SFT': 'MOSS-Image (SFT)',
    'FLUX.3 Image Klein': 'FLUX 3 Image Klein',
    'ERNIE-Image (penuh, 50 langkah)': 'ERNIE-Image',
    'Z-Image (asas, tidak disuling)': 'Z-Image',
    'SDXL': 'SDXL base 1.0 / SDXL-Lightning',
}
GROUP_D = 'D. Lesen belum disemak'
GRADES = ('Kuat', 'Baik', 'Sederhana', 'Lemah', 'Tolak')


def grade(text):
    """Darjah ringkas untuk jadual: 'Kuat: OneIG 0.99' -> 'Kuat'. Ayat tanpa darjah -> 'Skor sahaja'."""
    v = str(text or '').strip()
    if not v or v in ('-', '\u2013', '\u2014'):
        return None
    head = re.split(r'[:.(]', v, maxsplit=1)[0].strip()
    for g in GRADES:
        if head.lower().startswith(g.lower()):
            return g
    if head.lower().startswith('tiada'):
        return 'Tiada data'
    return 'Skor sahaja' 


def tone_of(grade_word):
    return {'Kuat': 'ok', 'Baik': 'ok', 'Sederhana': 'warn', 'Lemah': 'bad', 'Tolak': 'bad'}.get(grade_word)


def main():
    lic_doc = json.loads((MODELS / 'ai_licenses.json').read_text())
    lic_rows = lic_doc['rows'] if isinstance(lic_doc, dict) else lic_doc
    cmp_doc = json.loads((MODELS / 'model_compare.json').read_text())
    cmp_rows = cmp_doc['rows'] if isinstance(cmp_doc, dict) else cmp_doc

    notes, tests = [], {}
    for r in cmp_rows:
        name = r['model']
        if name.startswith('Ditolak'):
            notes.append({'kind': 'Ditolak', 'item': re.sub(r'^Ditolak[^:]*:\s*', '', name),
                          'stage': 'Langkah 2' if 'Langkah 2' in name else 'Langkah 1',
                          'why': r.get('community') or r.get('run') or '—',
                          'level': r.get('level'), 'source': r.get('source')})
        elif name.startswith('Tambahan'):
            notes.append({'kind': 'Tambahan', 'item': re.sub(r'^Tambahan:\s*', '', name),
                          'stage': 'Langkah 2', 'why': r.get('verdict') or '—',
                          'level': r.get('level'), 'source': r.get('source')})
        else:
            tests[NAME_MAP.get(name, name)] = r

    rows = []
    for lr in lic_rows:
        t = tests.pop(lr['model'], None)
        rows.append(build(lr, t))
    for name, t in tests.items():                      # diuji tetapi tiada baris lesen
        rows.append(build({'model': name, 'group': GROUP_D, 'license': t.get('license'),
                           'commercial': t.get('commercial')}, t))

    order = {'A. Bebas komersial': 0, 'B. Komersial bersyarat': 1, 'C. Bukan komersial': 2, GROUP_D: 3}
    rows.sort(key=lambda r: (order.get(r['group'], 9), 0 if r['tested'] == 'Ya' else 1))

    meta = [{'label': 'Gabungan', 'value': 'ai_licenses.json (lesen, kuota GPU, VRAM) + model_compare.json (ujian tulisan, kelajuan)'},
            {'label': 'Padanan nama', 'value': '; '.join(f'{k} = {v}' for k, v in NAME_MAP.items())},
            {'label': 'Skrip', 'value': 'scripts/build_master_models.py'}]
    write('master_models.json', {'rows': rows, 'meta': meta})
    write('model_notes.json', {'rows': notes, 'meta': meta[:1]})
    print(f'master_models: {len(rows)} baris ({sum(1 for r in rows if r["tested"] == "Ya")} ada ujian); '
          f'model_notes: {len(notes)} baris')


def build(lr, t):
    t = t or {}
    gs, gl = grade(t.get('text_short')), grade(t.get('text_long'))
    return {
        'model': lr['model'], 'group': lr.get('group') or GROUP_D,
        'commercial': lr.get('commercial') or '—', 'commercial_tone': lr.get('commercial_tone'),
        'license': lr.get('license') or '—', 'size': lr.get('size') or t.get('ram') or '—',
        'vram': lr.get('vram') or '—', 'img_free': lr.get('img_free'),
        'short': gs or '—', 'short_tone': tone_of(gs), 'long': gl or '—', 'long_tone': tone_of(gl),
        'verdict': lr.get('verdict') or t.get('verdict') or '—', 'tone': lr.get('tone'),
        'level': lr.get('level') or t.get('level'), 'source': lr.get('source') or t.get('source'),
        'tested': 'Ya' if t else '—',
        # butiran (baris buka/tutup)
        'terms': lr.get('terms'), 'use': lr.get('use'), 'space': lr.get('space'), 'gpu': lr.get('gpu'),
        'checked': lr.get('checked'),
        't_run': t.get('run'), 't_ram': t.get('ram'), 't_steps': t.get('steps'),
        't_short': t.get('text_short'), 't_long': t.get('text_long'), 't_bw': t.get('bw'),
        't_color': t.get('color'), 't_bg': t.get('bg'), 't_speed': t.get('speed'),
        't_community': t.get('community'), 't_verdict': t.get('verdict'),
        't_level': t.get('level'), 't_source': t.get('source'),
    }


def write(name, doc):
    (MODELS / name).write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
