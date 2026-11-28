#!/usr/bin/env python3
"""Jana HTML tab Etsy (dashboard/etsy_section.html) dan sisip ke dashboard/index.html.

Kepala jadual utama dijana daripada senarai COLS dalam dashboard/etsy.js supaya
lajur dalam HTML dan kod sentiasa sepadan. Jalankan selepas mengubah COLS.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "dashboard")

FREQ = [
    ("susunan", "Jenis susunan"), ("font", "Jenis font"), ("gandingan", "Gandingan font (12 teratas)"),
    ("font_utama", "Font kata utama"), ("font_mula", "Font baris pertama"), ("font_akhir", "Font baris akhir"),
    ("rawat_mula", "Rawatan baris pertama"), ("peranan", "Corak peranan (12 teratas)"),
    ("tangga", "Tangga saiz (12 teratas)"), ("bekas", "Bekas teks"), ("kesan", "Kesan huruf"),
    ("hiasan", "Jenis hiasan"), ("ikon", "Peranan ikon"), ("gaya_ikon", "Gaya ikon"), ("kat_ikon", "Kategori ikon"),
    ("nada", "Nada ayat"), ("pandang", "Sudut pandang"), ("formula", "Formula ayat (15 teratas)"),
]
KPI = [
    ("design", "etsy-k-design", "Design unik", None),
    ("purata_blok", "etsy-k-blok", "Purata blok teks", "setiap design"),
    ("purata_font", "etsy-k-font", "Purata jenis font", "setiap design"),
    ("purata_hiasan", "etsy-k-hiasan", "Purata jenis hiasan", "setiap design"),
    ("purata_dakwat", "etsy-k-dakwat", "Purata liputan dakwat", "bahagian hitam dalam kotak design"),
    ("pct_ikon", "etsy-k-ikon", "Design berikon", "ada sekurang-kurangnya satu ikon"),
    ("pct_skrip_utama", "etsy-k-skrip", "Kata utama dalam skrip", "design yang kata utamanya skrip"),
    ("pct_senget", "etsy-k-senget", "Design senget", "teks condong 5 darjah atau lebih"),
    ("pct_lengkung", "etsy-k-lengkung", "Ada teks melengkung", "sekurang-kurangnya satu baris"),
    ("isu", "etsy-k-isu", "Ayat bermasalah", "design dengan ayat atau ejaan rosak"),
]
VIEWS = [("ringkas", "Ringkas"), ("teks", "Teks dan font"), ("ikon", "Ikon dan hiasan"), ("susun", "Susunan"),
         ("ukur", "Ukuran piksel"), ("ayat", "Ayat"), ("tiru", "Tiru"), ("semua", "Semua lajur")]


def mark(field):
    return f'data-source="etsy_ringkas" data-field="{field}" data-row="0"'


def main():
    js = open(os.path.join(D, "etsy.js"), encoding="utf-8").read()
    cols = json.loads(re.search(r"/\*COLS\*/\s*const COLS = (\[.*?\]);\s*/\*COLS\*/", js, re.S).group(1))
    h = []
    a = h.append
    a('<section id="tab-etsy" class="pod-tab" role="tabpanel" aria-labelledby="btn-etsy" hidden>\n')
    a('<div id="etsy-intro" class="pod-section pod-first">')
    a(f'  <p class="pod-lede">Rujukan gaya daripada kedai Etsy ArtfulCraftsCreators: <b data-draw="etsy-k-design" {mark("design")}>—</b> design unik dinyahkod satu demi satu (teks, font, saiz, kesan huruf, ikon, bekas teks, hiasan, susunan, ukuran piksel, formula ayat) supaya gaya ini boleh ditiru dengan ayat kita sendiri.</p>')
    a('  <div class="pod-kpis" id="etsy-kpis">')
    for field, draw, label, sub in KPI:
        if field == "design":
            sub_html = f'daripada <span data-draw="etsy-k-gambar" {mark("gambar")}>—</span> gambar grid'
        else:
            sub_html = sub
        a(f'    <div class="pod-kpi" id="etsy-kpi-{field}"><div class="pod-q">{label}</div><div class="pod-big" data-draw="{draw}" {mark(field)}>—</div><div class="pod-muted">{sub_html}</div></div>')
    a('  </div>')
    a('  <p class="pod-muted">Gambar di tab ini ialah design penjual lain. Guna sebagai rujukan gaya sahaja: ayat dan susunan kita mesti berbeza.</p>')
    a('</div>\n')
    a('<nav class="pod-nav" aria-label="Bahagian tab Etsy">\n  <a href="#etsy-semua">Semua design</a>\n  <a href="#etsy-corak">Corak gaya</a>\n  <a href="#etsy-font">Font boleh tiru</a>\n  <a href="#etsy-listing">Listing</a>\n</nav>\n')

    a('<section id="etsy-semua" class="pod-section">')
    a('  <h2>Semua design</h2>')
    a('  <p class="pod-muted">Satu baris setiap design. Tekan gambar atau Butiran untuk lihat semua yang dinyahkod bagi design itu; tekan ♥ untuk tanda kegemaran. Pilih kumpulan lajur di bawah, atau Semua lajur dan seret jadual ke kiri.</p>')
    a('  <div class="etsy-filters" id="etsy-filters">')
    a('    <input type="search" data-etsy-f="q" aria-label="Cari design" placeholder="Cari ayat, ikon, font, formula…">')
    a('    <select class="dash-select" data-etsy-f="tema" aria-label="Tema"><option value="">Semua tema</option><option>Sindiran</option><option>Football</option></select>')
    a('    <select class="dash-select" data-draw="etsy-f-susunan" data-source="etsy_f_susunan" aria-label="Jenis susunan"></select>')
    a('    <select class="dash-select" data-draw="etsy-f-nada" data-source="etsy_f_nada" aria-label="Nada ayat"></select>')
    a('    <select class="dash-select" data-etsy-f="sukar" aria-label="Kesukaran tiru"><option value="">Semua kesukaran</option><option>Mudah</option><option>Sederhana</option><option>Sukar</option></select>')
    a('    <label class="etsy-chk"><input type="checkbox" data-etsy-f="isu"> Ayat bermasalah sahaja</label>')
    a('    <button type="button" class="etsy-reset">Set semula</button>')
    a('  </div>')
    a('  <div class="etsy-views" id="etsy-views" role="group" aria-label="Kumpulan lajur">')
    for i, (key, label) in enumerate(VIEWS):
        a(f'    <button type="button" data-etsy-view="{key}" aria-pressed="{"true" if i == 0 else "false"}">{label}</button>')
    a('  </div>')
    a(f'  <p class="pod-muted">Menunjukkan <b data-draw="etsy-count">—</b> daripada <b data-draw="etsy-k-design" {mark("design")}>—</b> design.</p>')
    a('  <div class="etsy-wrap">')
    a('    <table class="etsy-table etsy-v-ringkas" data-source="etsy_designs" data-row-key="id">')
    a('      <thead><tr>')
    a('        <th class="etsy-c-img">Gambar</th>\n        <th data-field="id">ID</th>\n        <th data-field="ayat">Ayat</th>')
    for key, label, groups, typ in cols:
        cls = "ec " + " ".join(f"eg-{g}" for g in groups.split()) + (" pod-num" if typ == "n" else "")
        field = "" if typ == "lines" else f' data-field="{key}"'
        a(f'        <th class="{cls}"{field}>{label}</th>')
    a('      </tr></thead>')
    a('      <tbody data-draw="etsy-body"></tbody>')
    a('    </table>')
    a('  </div>')
    a('  <details id="etsy-cara">')
    a('    <summary>Cara lajur dikira</summary>')
    a('    <p class="pod-muted">Pemerhatian ditulis oleh penyemak bebas (Claude kedua) yang melihat setiap gambar tanpa bergantung pada rekod asal; penyemak yang sama membandingkan setiap rekod dengan gambarnya dan isu yang disahkan telah dibetulkan. Bacaan mata Claude (bukti lemah): font, saiz baris 1 hingga 5, rawatan, kesan huruf, ikon, hiasan, susunan, sudut senget, formula ayat, nada, rasa, khalayak dan kunci gaya. Font boleh tiru ialah padanan terdekat, bukan font asal penjual.</p>')
    a('    <p class="pod-muted">Diukur daripada piksel (piksel dengan kelabu di bawah 110 dikira dakwat, dalam kotak ketat design): Lebar ÷ tinggi; Dakwat (%) = dakwat ÷ luas kotak; Dakwat sepertiga atas, tengah, bawah = bahagian dakwat dalam setiap sepertiga tinggi; Pusat jisim X dan Y = purata kedudukan dakwat (50 = tengah); Simetri cermin = pertindihan dakwat dengan imej cerminnya (teks tidak pernah bercermin sempurna, jadi 50 ke atas sudah sangat simetri); Kepingan hitam = bilangan bentuk hitam terpisah; Lubang putih = bilangan ruang putih tertutup dalam bentuk hitam; Tebal garis purata = 2 × luas dakwat ÷ perimeter, sebagai peratus lebar; Isi siluet = luas bentuk keseluruhan selepas celah ditutup ÷ luas kotak.</p>')
    a('    <p class="pod-muted">Dikira daripada lajur lain: tangga saiz, corak peranan, urutan dan gandingan font, jenis hiasan, kategori ikon, sudut pandang, resipi tiru. Skor tiru = bilangan blok teks + bilangan jenis font + 2 jika ikon mengganti huruf, menjadi bingkai atau panel + 1 jika ada teks melengkung + 1 jika tekstur kasar + 1 jika ada tiga bekas teks atau lebih. Skor 6 ke bawah Mudah, 7 hingga 9 Sederhana, 10 ke atas Sukar.</p>')
    a('  </details>')
    a('  <div class="etsy-dlg" id="etsy-dlg" hidden role="dialog" aria-modal="true" aria-label="Butiran design">')
    a('    <div class="etsy-dlg-box">')
    a('      <div class="etsy-dlg-bar"><button type="button" class="etsy-dlg-prev">‹ Sebelum</button><button type="button" class="etsy-dlg-next">Seterusnya ›</button><button type="button" class="etsy-dlg-close">Tutup ✕</button></div>')
    a('      <div class="etsy-detail" data-draw="etsy-detail" data-source="etsy_designs"></div>')
    a('    </div>')
    a('  </div>')
    a('</section>\n')

    a('<section id="etsy-corak" class="pod-section">')
    a('  <h2>Corak gaya</h2>')
    a('  <p class="pod-muted">Berapa banyak design menggunakan setiap unsur. Bagi font, bekas teks, kesan huruf, hiasan dan ikon, satu design boleh ada beberapa nilai, jadi peratus tidak berjumlah 100. Dalam corak peranan, U = kata utama, S = sokongan, K = kata sambung, dari baris atas ke bawah.</p>')
    a('  <div class="etsy-freqs">')
    for fid, title in FREQ:
        a(f'    <div class="etsy-freq" id="etsy-fqbox-{fid}"><h3>{title}</h3><table data-source="etsy_f_{fid}" data-row-key="nama"><thead><tr><th data-field="nama">Nilai</th><th data-field="bil" class="pod-num">Design</th><th data-field="pct">Bahagian</th></tr></thead><tbody data-draw="etsy-fq-{fid}"></tbody></table></div>')
    a('  </div>')
    a('</section>\n')

    a('<section id="etsy-font" class="pod-section">')
    a('  <h2>Font boleh tiru</h2>')
    a('  <p class="pod-muted">Padanan terdekat mengikut mata, bukan font asal penjual. Lesen dan risiko disalin daripada senarai induk font di tab Font. Pilihan 1 ialah calon utama; pilihan 9 ialah calon khusus untuk beberapa design.</p>')
    a('  <div class="pod-table-wrap pod-scroll">')
    a('    <table data-source="etsy_fonts" data-row-key="kunci"><thead><tr><th data-field="jenis">Jenis font</th><th data-field="ciri">Ciri</th><th data-field="bil_design" class="pod-num">Design guna</th><th data-field="font">Font calon</th><th data-field="pilihan" class="pod-num">Pilihan</th><th data-field="sumber">Sumber</th><th data-field="lesen">Lesen</th><th data-field="risiko">Risiko</th></tr></thead><tbody data-draw="etsy-font-body"></tbody></table>')
    a('  </div>')
    a('</section>\n')

    a('<section id="etsy-listing" class="pod-section">')
    a('  <h2>Listing sumber</h2>')
    a('  <p class="pod-muted">Maklumat listing seperti dilihat pada tarikh dalam jadual. Harga dan rating boleh berubah.</p>')
    a('  <div class="pod-table-wrap">')
    a('    <table data-source="etsy_listing" data-row-key="listing"><thead><tr><th data-field="listing">Listing</th><th data-field="penjual">Penjual</th><th data-field="harga_rm" class="pod-num">Harga (RM)</th><th data-field="harga_asal_rm" class="pod-num">Harga asal (RM)</th><th data-field="diskaun_pct" class="pod-num">Diskaun (%)</th><th data-field="rating" class="pod-num">Rating</th><th data-field="bil_rating" class="pod-num">Bil. rating</th><th data-field="format">Format</th><th data-field="bil_design" class="pod-num">Design di sini</th><th data-field="gambar">Gambar anda</th><th data-field="dilihat">Dilihat</th><th data-field="bukti">Bukti</th><th data-field="nota_bukti">Nota bukti</th></tr></thead><tbody data-draw="etsy-listing-body"></tbody></table>')
    a('  </div>')
    a('</section>\n')
    a('</section>\n')
    sec = "\n".join(h)
    open(os.path.join(D, "etsy_section.html"), "w", encoding="utf-8").write(sec)

    p = os.path.join(D, "index.html")
    page = open(p, encoding="utf-8").read()
    i, j = page.index('<section id="tab-etsy"'), page.index('<section id="tab-suka"')
    open(p, "w", encoding="utf-8").write(page[:i] + sec + "\n" + page[j:])
    print(f"{len(cols) + 3} lajur, {len(FREQ)} jadual kekerapan; bahagian {len(sec)} aksara; index.html {len(page[:i] + sec) + len(page[j:])} aksara")


if __name__ == "__main__":
    main()
