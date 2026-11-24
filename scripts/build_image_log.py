"""Daftar ujian imej AI: satu baris untuk setiap imej yang pernah dijana dalam repo ini.

Sumber (dataset per-imej yang sedia ada, tiada angka direka):
  data/export/models/model_test.json          ujian 3 model, 23 Nov
  data/export/models/lettering_test.json      ujian lettering ayat panjang, 23 Nov
  data/export/models/lettering_v2.json        ERNIE v2, 23 Nov
  data/export/models/lettering_v3.json        QC v3 (cubaan 1-4), 23 Nov
  data/export/models/lettering_v3_final.json  QC v3 imej final, 23 Nov
  data/export/lettering_p9/lettering_p9_test.json  Lettering P9 (6 gaya), 23 Nov
Output: data/export/models/image_log.json  (dataset dashboard `image_log`)
Jalankan: python3 scripts/build_image_log.py
Tambah imej baharu: tulis baris dalam data/export/models/image_log_extra.json (senarai objek
dengan medan yang sama), kemudian jalankan skrip ini semula.
"""
import json, pathlib, re

BASE = pathlib.Path(__file__).resolve().parent.parent
MODELS = BASE / 'data/export/models'
P9 = BASE / 'data/export/lettering_p9'

# enjin sebenar di sebalik label setiap set (daripada kad model / tools set itu)
ENGINE = {
    'FLUX.2 klein 4B': ('FLUX.2 klein 4B', ''),
    'Z-Image-Turbo': ('Z-Image-Turbo', ''),
    'ERNIE-Image-Turbo': ('ERNIE-Image-Turbo', ''),
    'ERNIE-Image-Turbo + penambah prompt': ('ERNIE-Image-Turbo', 'penambah prompt'),
    'MOSS-Image SFT (8 langkah)': ('MOSS-Image SFT', 'LoRA 8 langkah'),
    'Qwen-Image-2512': ('Qwen-Image-2512', ''),
    'ERNIE + penambah, seed 42': ('ERNIE-Image-Turbo', 'penambah prompt'),
    'ERNIE + penambah, seed 7': ('ERNIE-Image-Turbo', 'penambah prompt'),
}
V3 = ('ERNIE-Image-Turbo', 'penambah prompt')     # v3 = pusingan QC lanjutan ujian ERNIE v2


def load(path):
    d = json.loads(path.read_text())
    return d['rows'] if isinstance(d, dict) else d


def blob(v):
    v = str(v or '')
    m = re.search(r'([0-9a-f]{32})', v)
    return m.group(1) if m else ''


def row(**kw):
    kw.setdefault('steps', None)
    kw.setdefault('variant', '')
    kw['size'] = f"{kw['w']}×{kw['h']}" if kw.get('w') and kw.get('h') else '—'
    kw['result'] = 'Lulus' if kw.pop('ok', False) else 'Tolak'
    kw['tone'] = 'ok' if kw['result'] == 'Lulus' else 'bad'
    return kw


def main():
    out = []
    names = {r['model']: r['model_name'] for r in load(MODELS / 'model_test_models.json')}
    for r in load(MODELS / 'model_test.json'):
        label = names.get(r['model'], r.get('model_name', ''))
        eng, var = ENGINE.get(label, (label, ''))
        out.append(row(id='mt-' + r['id'] + '-' + r['model'], date='2026-11-23', engine=eng, variant=var,
                       where='Container CPU (4 teras)', purpose='Ujian 3 model: 10 design sama',
                       text=r.get('text'), style=r.get('type'), seed=r.get('seed'), w=r.get('w'), h=r.get('h'),
                       seconds=r.get('seconds'), ok=bool(r.get('ok')), wrong=r.get('wrong') or '',
                       img=blob(r.get('img')), source='model_test', level=r.get('level')))

    for file, purpose, mfile in [('lettering_test', 'Ujian lettering ayat panjang', 'lettering_test_models'),
                                 ('lettering_v2', 'ERNIE v2: ayat baharu', 'lettering_v2_models'),
                                 ('lettering_v3', 'QC v3: cubaan ulang', 'lettering_v3_models'),
                                 ('lettering_v3_final', 'QC v3: imej final', 'lettering_v3_final_models')]:
        labels = {r['model']: r['model_name'] for r in load(MODELS / (mfile + '.json'))}
        for r in load(MODELS / (file + '.json')):
            label = labels.get(r['model'], r.get('model_name', ''))
            eng, var = ENGINE.get(label, V3 if file.startswith('lettering_v3') else (label, ''))
            out.append(row(id=file.replace('lettering_', 'lt-') + '-' + str(r['id']) + '-' + str(r['model']),
                           date='2026-11-23', engine=eng, variant=var, where='—', purpose=purpose,
                           text=r.get('text'), style=r.get('type'), seed=r.get('seed'), w=r.get('w'), h=r.get('h'),
                           seconds=r.get('seconds'), ok=bool(r.get('ok')), wrong=r.get('wrong') or '',
                           img=blob(r.get('img')), source=file, level=r.get('level')))

    for r in load(P9 / 'lettering_p9_test.json'):
        out.append(row(id='p9-' + r['id'], date='2026-11-23', engine='MOSS-Image SFT', variant='LoRA 8 langkah',
                       steps=8, where='Container CPU', purpose='Lettering P9: 6 gaya (S001–S006)',
                       text=r.get('text'), style=r.get('style_name'), seed=r.get('seed'), w=None, h=None,
                       seconds=r.get('seconds'), ok=not r.get('wrong_n'), wrong=('dipilih' if r.get('pick') else ''),
                       img=blob(r.get('final_img') or r.get('raw_img')), source='lettering_p9_test',
                       level=r.get('level')))

    extra = MODELS / 'image_log_extra.json'
    if extra.exists():
        for r in load(extra):
            r.setdefault('source', 'manual')
            out.append(row(**{k: v for k, v in r.items() if k not in ('size', 'result', 'tone')}))

    out.sort(key=lambda r: (r['date'], r['engine'], r['id']))
    meta = [{'label': 'Sumber', 'value': 'model_test, lettering_test, lettering_v2, lettering_v3, '
                                         'lettering_v3_final, lettering_p9_test (+ image_log_extra.json)'},
            {'label': 'Skrip', 'value': 'scripts/build_image_log.py'}]
    (MODELS / 'image_log.json').write_text(json.dumps({'rows': out, 'meta': meta}, ensure_ascii=False, indent=2) + '\n')
    lulus = sum(1 for r in out if r['result'] == 'Lulus')
    print(f'image_log: {len(out)} imej, {lulus} lulus, {len(out) - lulus} tolak')


if __name__ == '__main__':
    main()
