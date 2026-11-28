# Baris AI Image Test U23 (U13 dipakai sesi lain) (K9-K13): python3 ai_rows_k50k54.py dalam designs/lettering-v1 -> data/ai_tests/rows/U23.json
import json, sys, os
sys.path.insert(0, '.')
import kad, pembina
SP = os.environ.get('SP', 'qc')  # peta blob: <SP>/blobmap.txt (salinan: qc/v12_k50k54_blobs.txt)
bm = dict(l.split() for l in open(f'{SP}/blobmap.txt' if SP != 'qc' else 'qc/v12_k50k54_blobs.txt'))
qc = json.load(open('qc/v12_k50k54.json'))
NAMA = {'moss': ('moss', 'MOSS-Image SFT'), 'ernie': ('ernie', 'ERNIE-Image-Turbo'), 'klein3': ('flux3klein', 'FLUX 3 Image Klein'),
        'zturbo': ('zturbo', 'Z-Image-Turbo'), 'klein4b': ('klein4b', 'FLUX.2 klein 4B')}
REF = {'K9': 'IMG_5840', 'K10': 'IMG_5793', 'K11': 'IMG_5789', 'K12': 'IMG_5786', 'K13': 'IMG_5791'}
NOTA_P = {'v12-cpu-k50k54-p1': {'ernie': "pusingan 1: calon 'ernie_hiasan_tepat' (KALAH)", 'klein3': "pusingan 1: calon 'klein3_frasa_bentuk'"}}
saat = {}
for b in ('v12-cpu-k50k54', 'v12-cpu-k50k54-p1'):
    for m in NAMA:
        f = f'raw/{b}/{m}/log.jsonl'
        if os.path.exists(f):
            for l in open(f):
                r = json.loads(l); saat[(b, m, r['id'], r['seed'])] = r['saat']
rows = []
for b in ('v12-cpu-k50k54', 'v12-cpu-k50k54-p1'):
    for m, d in qc.get(b, {}).items():
        for k, (ok, nota, _) in d.items():
            iid, s = k.split('_s'); s = int(s); kid, aid = iid[:-1], iid[-1]
            raw = f'raw/{b}/{m}/{k}.png'
            if raw not in bm: continue
            fin = f'final/{b}/{m}_{k}/18x24_preview.jpg'
            p1 = b.endswith('-p1')
            lines = pembina.bina(m, kid, aid)[1]
            mk, mn = NAMA[m]
            rows.append(dict(
                ujian='U23', ujian_nama='Standard v1.2: K50–K54 sesi B (5 gaya, 5 model CPU, hitam putih)', jenis='Ujian',
                standard='Lettering v1.2: G1 ejaan + G2 tiada teks / tanda rawak + G3 tiada cacat + ciri teras kad (huruf condensed, keputusan pengguna 28 Nov 2026)',
                ujian_nota='Lima gambar upload (IMG_5840, 5793, 5789, 5786, 5791), ayat baharu pilihan Claude, kad K50–K54 (diluluskan pengguna 28 Nov 2026). CPU container, laluan 1 seed 42, 7; laluan 2 (K54p) seed 42, 7, 123. Pusingan 1 kitaran QC: ERNIE (K52A, K54p) dan FLUX 3 Klein (K51m, K54p). img_siap = kemasan hitam putih (5b + SK07 + SK06 v1.4) pratonton 18×24. Semakan mata Claude.',
                ai=True, bukti='lemah', tempat='CPU', kad=kid, kad_name=kad.KAD[kid]['nama'], kad_nota=kad.KAD[kid]['versi'],
                ref_img='/_blob/' + bm[f'rujukan/{REF[kid]}.jpg'], ref_nota=REF[kid],
                baris=f'{iid} · seed {s}' + (' · pusingan 1' if p1 else ''), teks=' / '.join(lines), seed=s,
                img_siap=('/_blob/' + bm[fin]) if fin in bm else None,
                cacat=nota.startswith('G3'), teras=(False if 'ciri teras gagal' in nota else (True if ok else None)), gaya='', tanda='',
                tarikh='2026-11-28' if 'klein3' == m and p1 else '2026-11-27',
                key=f'U23|{m}-{k}' + ('-p1' if p1 else ''), model=mk, model_name=mn, label=mn,
                lajur=mn + (' · pusingan 1' if p1 else ''), varian=NOTA_P.get(b, {}).get(m, 'aturan semasa (pembina v1.2)'),
                saat=saat.get((b, m, iid, s)), img='/_blob/' + bm[raw], w=768, h=1024,
                lulus=bool(ok), ejaan=not nota.startswith('G1'), rawak=nota.startswith('G2'), sebab=nota))
json.dump(rows, open('../../data/ai_tests/rows/U23.json', 'w'), ensure_ascii=False, indent=1)
print(len(rows), sum(r['lulus'] for r in rows), sum(1 for r in rows if r['img_siap']), sum(1 for r in rows if r['saat'] is None))
