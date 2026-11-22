"""Jana senarai sumber inspirasi design untuk tab Inspirasi dashboard.

Output: data/export/inspirasi/inspirasi_sumber.json
Tahap bukti: rasmi (laman itu sendiri / Pinterest rasmi), pihak_ketiga (artikel bebas),
lemah (pautan carian; kedudukan hasil bukan bukti popular).
"""
import json
import os
from urllib.parse import quote_plus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "export", "inspirasi", "inspirasi_sumber.json")

WDD = "https://www.webdesignerdepot.com/2014/02/typographicposters-com-presents-a-beautiful-overview-of-poster-design/"
DS = "https://designshack.net/articles/inspiration/font-inspiration-websites"
CB = "https://www.creativebloq.com/inspiration/top-7-typography-galleries-to-inspire-your-designs"
PT_HELP = "https://help.pinterest.com/en/business/article/pinterest-trends"
AIGA = "https://eyeondesign.aiga.org/hand-drawn-type-masters-jessica-hische-and-gemma-obrien-on-when-to-say-no/"
SKS = "https://www.skillshare.com/en/blog/hand-lettering-artists-to-follow-on-instagram/"
SLANTED = "https://slanted.de/?p=631411"

ROWS = [
    # Alat trend (ganti "high pins": Pinterest tidak papar jumlah carian mentah)
    dict(id="pin-trends", jenis="Alat trend", nama="Pinterest Trends", url="https://trends.pinterest.com/",
         kenapa="Carian teratas Pinterest ikut negara, dengan perubahan mingguan, bulanan dan tahunan serta corak musim. Graf ialah nisbah, bukan jumlah carian.",
         guna="Pilih kata kunci dan tema yang sedang naik sebelum design", bukti="rasmi", bukti_url=PT_HELP),
    dict(id="pin-predicts", jenis="Alat trend", nama="Pinterest Predicts", url="https://business.pinterest.com/pinterest-predicts/",
         kenapa="Laporan tahunan Pinterest tentang trend yang dijangka naik tahun depan (warna, gaya, tema).",
         guna="Rancang koleksi musim dan warna", bukti="rasmi", bukti_url="https://business.pinterest.com/pinterest-predicts/"),
    # Laman kurasi poster / typography
    dict(id="typo-posters", jenis="Laman kurasi", nama="Typographic Posters", url="https://www.typographicposters.com/",
         kenapa="Platform kolektif pereka yang membuat poster berfokus typography; ribuan poster ikut pereka.",
         guna="Layout poster, hierarki huruf, poster eksperimental", bukti="pihak_ketiga", bukti_url=WDD),
    dict(id="slanted-posters", jenis="Laman kurasi", nama="typo/graphic posters (Slanted)", url="https://www.typo-graphicposters.com/",
         kenapa="Arkib 6,500+ poster dari 42 negara oleh 287 pereka; boleh cari ikut warna, tag dan kata kunci.",
         guna="Cari ikut warna untuk padan dekor bilik", bukti="pihak_ketiga", bukti_url=SLANTED),
    dict(id="fontsinuse", jenis="Laman kurasi", nama="Fonts In Use", url="https://fontsinuse.com/",
         kenapa="Arkib typography dalam projek sebenar (poster, kulit buku, album) dengan nama fon setiap satu; disusun ikut industri, format, zaman dan fon.",
         guna="Tahu fon apa dipakai dalam poster yang anda suka", bukti="pihak_ketiga", bukti_url=DS),
    dict(id="typewolf", jenis="Laman kurasi", nama="Typewolf", url="https://www.typewolf.com/",
         kenapa="Contoh pasangan fon dengan nama fon disenaraikan; dilancarkan 2013 oleh Jeremiah Shoaf. Lebih kuat untuk web, berguna untuk pasangan tajuk + teks.",
         guna="Pasangan fon tajuk dan teks kecil", bukti="pihak_ketiga", bukti_url=DS),
    dict(id="behance", jenis="Laman kurasi", nama="Behance: typography poster", url="https://www.behance.net/search/projects/typography%20poster",
         kenapa="Portfolio pereka (milik Adobe). Susun ikut 'Most Appreciated' untuk lihat projek yang paling ramai suka.",
         guna="Siri poster lengkap dan mockup", bukti="lemah", bukti_url="https://www.behance.net/"),
    dict(id="dribbble", jenis="Laman kurasi", nama="Dribbble: typography poster", url="https://dribbble.com/tags/typography_poster",
         kenapa="Shot pendek dari pereka; tag typography poster. Kiraan 'likes' setiap shot boleh jadi petanda minat (bukti lemah).",
         guna="Idea pantas gaya huruf dan warna", bukti="lemah", bukti_url="https://dribbble.com/"),
    dict(id="typespiration", jenis="Laman kurasi", nama="Typespiration", url="https://typespiration.com/",
         kenapa="Contoh pasangan fon dan warna; ada surat berita inspirasi fon.",
         guna="Pasangan fon + palet warna", bukti="pihak_ketiga", bukti_url=DS),
    dict(id="tdc", jenis="Laman kurasi", nama="Type Directors Club (TDC)", url="https://www.tdc.org/",
         kenapa="Anugerah typography antarabangsa tahunan; pemenang = rujukan kualiti tinggi.",
         guna="Tanda aras kualiti, bukan untuk ditiru terus", bukti="lemah", bukti_url="https://www.tdc.org/"),
    dict(id="letterform", jenis="Laman kurasi", nama="Letterform Archive", url="https://letterformarchive.org/",
         kenapa="Arkib sejarah lettering dan typography (koleksi dalam talian).",
         guna="Gaya vintage dan retro yang asli", bukti="lemah", bukti_url="https://letterformarchive.org/"),
    # Pereka lettering / typography
    dict(id="hische", jenis="Pereka", nama="Jessica Hische", url="https://www.jessicahische.is/",
         kenapa="Lettering artist dan type designer; projek Daily Drop Cap mencetuskan ramai pereka buat projek lettering harian.",
         guna="Huruf hiasan, drop cap, script elegan", bukti="pihak_ketiga", bukti_url="https://www.wikipedia.org/wiki/Jessica_Hische"),
    dict(id="obrien", jenis="Pereka", nama="Gemma O'Brien", url="https://www.gemmaobrien.com/",
         kenapa="Disebut AIGA Eye on Design sebagai antara pereka yang memimpin ledakan hand-lettering.",
         guna="Lettering ekspresif, mural, brush", bukti="pihak_ketiga", bukti_url=AIGA),
    dict(id="marinovich", jenis="Pereka", nama="Erik Marinovich", url="https://www.erikmarinovich.com/",
         kenapa="Letterer, pengasas bersama Title Case; gaya dari ringkas hingga grunge.",
         guna="Logo-style lettering, retro, badge", bukti="pihak_ketiga", bukti_url=SKS),
    dict(id="hom", jenis="Pereka", nama="Lauren Hom", url="https://www.homsweethom.com/",
         kenapa="Pereka dan letterer (studio Hom Sweet Hom); terkenal dengan projek Daily Dishonesty.",
         guna="Quote lucu, warna ceria, gaya playful", bukti="pihak_ketiga", bukti_url=SKS),
    dict(id="tanamachi", jenis="Pereka", nama="Dana Tanamachi", url="https://www.tanamachistudio.com/",
         kenapa="Perintis chalk lettering moden; klien termasuk Google, TIME dan Target.",
         guna="Gaya papan kapur untuk dapur, kelas, majlis", bukti="pihak_ketiga", bukti_url=SKS),
]

# Carian Pinterest terus ikut niche poster P1–P8 (POD.NICHES) + gaya umum
PIN_QUERIES = [
    ("bridal", "Bridal", "bridal shower sign typography"),
    ("teacher", "Cikgu", "classroom poster typography"),
    ("nursery", "Nursery", "nursery quote print typography"),
    ("funny_home", "Tanda lucu rumah", "funny bathroom sign typography print"),
    ("mama", "Mama", "mama quote typography print"),
    ("christmas", "Krismas", "christmas typography print"),
    ("friendship", "Kawan / Galentine", "galentines typography print"),
    ("bookish", "Bookish", "bookish quote typography poster"),
    ("gaya-swiss", "Gaya: Swiss minimal", "swiss typography poster"),
    ("gaya-retro", "Gaya: retro / groovy", "retro groovy typography poster"),
    ("gaya-serif", "Gaya: serif besar", "big serif typography poster wall art"),
]
for key, label, q in PIN_QUERIES:
    ROWS.append(dict(
        id="pin-" + key, jenis="Carian Pinterest", nama=label + ": " + q,
        url="https://www.pinterest.com/search/pins/?q=" + quote_plus(q),
        kenapa="Carian terus di Pinterest. Pin yang berulang muncul di atas dan ada banyak versi tiruan = petanda gaya laku (bukti lemah; Pinterest tidak papar jumlah simpanan secara tetap).",
        guna="Kumpul gaya untuk niche ini, kemudian upload yang anda suka", bukti="lemah",
        bukti_url="https://www.pinterest.com/search/pins/?q=" + quote_plus(q)))


def main():
    ids = [r["id"] for r in ROWS]
    assert len(ids) == len(set(ids)), "id berulang"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(ROWS, f, ensure_ascii=False, indent=1)
    print(OUT, len(ROWS))


if __name__ == "__main__":
    main()
