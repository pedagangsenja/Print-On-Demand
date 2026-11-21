"""Poster P1: niche poster ikut bilik/tempat/tema. Tulis data/posters/niches.json"""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")
E = {
 "etsy_wallart": ("Carian 'wall art decor' +110%, 'gallery prints' +80% (Etsy S/S 2026, Everyday Exhibits)", "https://community.etsy.com/forum/etsy-success-300/topic/etsy-insights-explore-the-trends-shaping-spring-and-summer-2026-165859/", "rasmi"),
 "erank_wallart": ("'wall art' kata kunci #4 Etsy US, Q3 2026", "https://help.erank.com/blog/top-etsy-searches-q3-2026/", "rasmi"),
 "gelato_living": ("Ruang tamu bilik paling penting untuk wall decor; dinding atas kepala katil = penempatan bilik tidur paling dicari", "https://www.gelato.com/ja/blog/wall-decor-by-room-guide", "pihak_ketiga"),
 "lowes_living": ("Tema popular ruang tamu: fotografi, landskap, abstrak (typography bukan dominan)", "https://www.lowes.com/n/buying-guide/wall-art-decor-buying-guide", "pihak_ketiga"),
 "nursery_vol": ("'nursery art' ~8,100 carian/bulan; minat memuncak April", "https://adtargeting.io/industry/wall-decoration-keywords", "pihak_ketiga"),
 "circus_nursery": ("Pinterest: 'circus nursery' +50%, 'vintage circus aesthetic' +70%", "https://www.aol.com/articles/pinterests-2026-interior-design-trends-171800656.html", "rasmi"),
 "kids_design": ("Bilik anak lebih 'design-forward', ibu bapa pilih karya yang padan dengan rumah", "https://urbanroad.com/blogs/trends/2026-interior-art-trends-for-living-rooms-bedrooms-and-beyond", "pihak_ketiga"),
 "teen_curated": ("Bilik remaja: koleksi tersusun menggantikan poster rawak", "https://www.fab-art.co/blogs/news/teen-bedroom-wall-art-ideas", "pihak_ketiga"),
 "kitchen_vol": ("'kitchen art' ~22,200 carian/bulan; 'kitchen sign' ~5,400", "https://www.rankhero.com/keywords/kitchen-art", "pihak_ketiga"),
 "pinterest_spring": ("Pinterest Spring 2026: dapur, ruang makan kreatif dan reading nook antara trend", "https://newsroom.pinterest.com/news/spring-trend-report-2026/", "rasmi"),
 "coffee_signs": ("Tanda coffee bar banyak dijual ($5-40) di Wayfair/Walmart/Kohl's", "https://www.wayfair.com/shop/o/coffee-bar-decor-ideas", "pihak_ketiga"),
 "bath_vol": ("'funny bathroom sign' ~8,100 carian/bulan, 36,886 listing Etsy (peluang 220)", "https://www.rankhero.com/keywords/funny-bathroom-sign", "pihak_ketiga"),
 "laundry_vol": ("'laundry room sign' ~2,900 carian/bulan", "https://www.rankhero.com/keywords/laundry-room-sign", "pihak_ketiga"),
 "laundry_trend": ("Tanda bilik dobi: trend 'design moment' kecil dalam rumah kecil (Jan 2026)", "https://www.coohom.com/article/laundry-room-sign-ideas-5-creative-options", "pihak_ketiga"),
 "mudroom": ("Sign art = trend hangat farmhouse; tanda mudroom & dobi disyorkan", "https://americanfarmhousestyle.com/shopping/sign-art", "pihak_ketiga"),
 "office_pin": ("Pinterest Fall 2025: 'chic cubicle decor' +1,543%, 'work office makeover' +2,652%", "https://newsroom.pinterest.com/news/the-2025-pinterest-fall-trend-report/", "rasmi"),
 "gelato_office": ("Home office: kategori carian wall art paling cepat berkembang sejak 2020", "https://www.gelato.com/de/blog/wall-decor-by-room-guide", "pihak_ketiga"),
 "gym_supply": ("Poster gym/motivasi banyak di Walmart, kebanyakan bawah $30; pemilik guna 3-5 poster", "https://www.walmart.com/c/kp/work-out-posters", "pihak_ketiga"),
 "book_tote": ("Bookish: carian 'book totes' +148%, romantasy +77% (Faire)", "https://www.somethingdifferentwholesale.com/uk/blog/book-gift-trend/", "lemah"),
 "mancave": ("Tin sign man cave/bar murah $6-9 membanjiri pasaran", "https://www.walmart.com/c/kp/man-caves", "pihak_ketiga"),
 "classroom_vol": ("'classroom posters' ~6,600 carian/bulan, 144,725 listing Etsy (peluang 46)", "https://www.rankhero.com/keywords/classroom-posters", "pihak_ketiga"),
 "teacher_spend": ("Cikgu belanja purata $600 duit sendiri setahun untuk kelas", "https://www.edweek.org/leadership/see-the-school-supplies-teachers-buy-for-students/2026/08", "rasmi"),
 "calm_corner": ("Set poster calm corner Walmart ~$10; bundle digital Etsy $3.50-16.81", "https://www.walmart.com/c/kp/classroom-calming-corner", "pihak_ketiga"),
 "dorm": ("Dorm 2026-27: 'hobby walls' dan dinding tersusun peribadi", "https://www.dormtherapy.com/what-is-a-hobby-wall-100013955", "pihak_ketiga"),
 "wedding_sign": ("Welcome sign antara dekor perkahwinan paling banyak difoto; seating chart 16×20 / 18×24", "https://bridebook.com/uk/article/wedding-signs", "pihak_ketiga"),
 "wedding_size": ("Seating chart biasa dalam saiz 16×20 dan 18×24", "https://www.minted.com/lp/wedding-signs", "rasmi"),
 "christmas_kw": ("'christmas' kata kunci #1 Etsy US, Oktober 2026", "https://help.erank.com/blog/top-keywords-on-etsy/", "rasmi"),
 "christmas_print": ("Printable Krismas di Etsy kebanyakan $2-3 (saingan harga tinggi)", "https://www.etsy.com/listing/1343560341", "rasmi"),
 "halloween_kw": ("'halloween' kata kunci #2 Etsy US, Q3 2026", "https://help.erank.com/blog/top-etsy-searches-q3-2026/", "rasmi"),
 "faith": ("Kedai Etsy ayat Bible 'KAM DesignHaus' ~26,289 jualan", "https://www.etsy.com/shop/KAMDesignHaus", "rasmi"),
 "quote_sat": ("Pasaran quote generik tepu; typography minimal tinggi permintaan tetapi saingan tinggi", "https://www.accio.com/business/inspirational-wall-decor", "pihak_ketiga"),
}
N = [  # id, nama, kumpulan, D,S,T,P,B,A, musim, bulan puncak, keputusan, bukti
 ("classroom", "Kelas (classroom)", "Pendidikan", 4,2,5,5,5,5, "Bermusim", "Jul-Ogos, Jan", "Gelombang 1", ["classroom_vol", "teacher_spend"]),
 ("bathroom", "Bilik air (lucu)", "Rumah", 4,3,5,4,4,5, "Sepanjang tahun", "Rata; naik Q4", "Gelombang 1", ["bath_vol"]),
 ("kitchen", "Dapur & coffee bar", "Rumah", 4,2,5,5,3,5, "Sepanjang tahun", "Q4, musim bunga", "Gelombang 1", ["kitchen_vol", "pinterest_spring", "coffee_signs"]),
 ("home_office", "Home office & cubicle", "Rumah / kerja", 4,3,5,4,3,5, "Sepanjang tahun", "Jan, Sep", "Gelombang 1", ["office_pin", "gelato_office"]),
 ("reading_nook", "Reading nook & bookish", "Rumah", 3,3,5,5,3,5, "Sepanjang tahun", "Q4", "Gelombang 1", ["pinterest_spring", "book_tote"]),
 ("bedroom", "Bilik tidur", "Rumah", 4,3,4,5,3,5, "Sepanjang tahun", "Jan-Apr, Feb (Valentine)", "Gelombang 1", ["gelato_living", "etsy_wallart"]),
 ("living_room", "Ruang tamu", "Rumah", 5,2,3,5,4,5, "Sepanjang tahun", "Jan-Apr, Q4", "Gelombang 1", ["etsy_wallart", "erank_wallart", "lowes_living"]),
 ("nursery", "Nursery", "Rumah", 4,3,4,5,3,4, "Sepanjang tahun", "Apr", "Gelombang 1", ["nursery_vol", "circus_nursery"]),
 ("laundry", "Bilik dobi", "Rumah", 3,3,5,4,3,5, "Sepanjang tahun", "Rata", "Gelombang 1", ["laundry_vol", "laundry_trend"]),
 ("seasonal_xmas", "Krismas & musim cuti", "Musim", 5,1,4,5,3,5, "Bermusim", "Okt-Dis", "Gelombang 1", ["christmas_kw", "christmas_print"]),
 ("wedding_signs", "Papan tanda perkahwinan", "Majlis", 4,3,5,5,4,2, "Bermusim", "Mac-Okt", "Fasa 2 (personalisasi)", ["wedding_sign", "wedding_size"]),
 ("home_gym", "Home gym", "Rumah", 3,2,5,3,4,5, "Sepanjang tahun", "Jan", "Gelombang 2", ["gym_supply"]),
 ("dorm", "Asrama / dorm", "Pendidikan", 3,3,4,4,3,5, "Bermusim", "Jul-Ogos", "Gelombang 2", ["dorm"]),
 ("counselor", "Bilik kaunselor / calm corner", "Pendidikan", 2,2,5,4,4,5, "Sepanjang tahun", "Ogos-Sep", "Gelombang 2", ["calm_corner"]),
 ("faith", "Iman / Kristian", "Tema", 3,2,5,4,3,5, "Sepanjang tahun", "Easter, Krismas", "Gelombang 2", ["faith"]),
 ("playroom", "Bilik anak & playroom", "Rumah", 3,3,4,4,3,4, "Sepanjang tahun", "Rata", "Gelombang 2", ["kids_design"]),
 ("dining", "Ruang makan", "Rumah", 3,3,4,4,2,5, "Sepanjang tahun", "Nov (Thanksgiving)", "Gelombang 2", ["pinterest_spring"]),
 ("entryway", "Pintu masuk & mudroom", "Rumah", 3,3,5,4,2,4, "Sepanjang tahun", "Musim bunga, Q4", "Gelombang 2", ["mudroom"]),
 ("affirmation", "Afirmasi & motivasi", "Tema", 3,1,5,4,3,5, "Sepanjang tahun", "Jan", "Gelombang 2", ["quote_sat"]),
 ("seasonal_other", "Halloween, Thanksgiving, Easter", "Musim", 4,1,4,4,2,5, "Bermusim", "Sep-Okt, Nov, Mac-Apr", "Gelombang 2", ["halloween_kw"]),
 ("teen", "Bilik remaja", "Rumah", 2,3,4,3,3,5, "Sepanjang tahun", "Ogos", "Kemudian", ["teen_curated"]),
 ("party_signs", "Papan tanda parti & baby shower", "Majlis", 3,3,5,4,3,2, "Sepanjang tahun", "Rata", "Fasa 2 (personalisasi)", ["wedding_sign"]),
 ("gym_b2b", "Gym & studio (bisnes)", "Bisnes", 2,3,5,2,3,5, "Sepanjang tahun", "Jan", "Kemudian", ["gym_supply"]),
 ("man_cave", "Man cave, garaj & bar", "Rumah", 3,1,5,2,3,5, "Sepanjang tahun", "Jun (Father's Day), Dis", "Elak buat masa ini", ["mancave"]),
 ("family_est", "Nama keluarga 'Est.'", "Tema", 3,2,5,4,2,2, "Sepanjang tahun", "Musim kahwin, Q4", "Fasa 2 (personalisasi)", ["gelato_living"]),
 ("salon_cafe", "Salon, kafe & klinik (bisnes)", "Bisnes", 2,3,4,2,2,3, "Sepanjang tahun", "Rata", "Elak buat masa ini", []),
]
rows = []
for n in N:
    i, name, grp, D, S, T, P, B, A, season, peak, wave, evk = n
    rows.append({"id": i, "niche": name, "group": grp, "demand": D, "competition": S, "typography_fit": T,
                 "pinterest_fit": P, "order_value": B, "automation": A, "total": D+S+T+P+B+A,
                 "season": season, "peak_months": peak, "decision": wave,
                 "evidence": [{"claim": E[k][0], "source": E[k][1], "level": E[k][2]} for k in evk]})
rows.sort(key=lambda r: -r["total"])
for k, r in enumerate(rows, 1): r["rank"] = k
out = {"stage": "P1", "title": "Niche poster ikut bilik, tempat dan tema", "updated": "2026-11-21",
       "scoring": "1-5 setiap kriteria (permintaan, saingan rendah, typography, padan Pinterest, nilai pesanan/set, automasi); jumlah maks 30; penilaian Claude berdasarkan bukti",
       "risk_note": [
         {"claim": "Printify tidak sokong pulangan kerana salah saiz atau tukar fikiran; kos ditanggung penjual", "source": "https://help.printify.com/hc/en-us/articles/4483630299025", "level": "rasmi"},
         {"claim": "Kerosakan semasa penghantaran / salah cetak: cetak semula atau refund percuma dalam 30 hari", "source": "https://help.printify.com/hc/en-us/articles/4483625769105", "level": "rasmi"},
         {"claim": "Saiz/fit = ~53% pulangan baju online (2023); ~56% (2026)", "source": "https://coresight.com/research/the-true-cost-of-apparel-returns/", "level": "pihak_ketiga"},
         {"claim": "Data 2026: fit/saiz 56% pulangan apparel", "source": "https://www.loopreturns.com/blog/items-returned-most-often-ecommerce/", "level": "pihak_ketiga"}],
       "niches": rows}
json.dump(out, open(os.path.join(ROOT, "data", "posters", "niches.json"), "w"), indent=2, ensure_ascii=False)
for r in rows: print(r["rank"], r["niche"], r["total"], r["decision"])
