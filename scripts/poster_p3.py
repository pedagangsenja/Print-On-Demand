"""Poster P3: gaya design & pin wall art. Tulis data/posters/styles.json"""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")
PIN_STUDY = "https://create.pinterest.com/blog/home-decor-content-ideas-examples/"
rules = [
 ("Pin imej membawa lebih banyak klik keluar berbanding pin video (kajian home decor Pinterest, Ogos 2026)", PIN_STUDY, "rasmi"),
 ("Pin yang menunjukkan gaya keseluruhan bilik lebih kerap dalam kandungan engagement tinggi berbanding close-up satu item", PIN_STUDY, "rasmi"),
 ("Teks overlay: namakan bilik, projek atau hasil dalam beberapa perkataan", PIN_STUDY, "rasmi"),
 ("Deskripsi lebih informatif cenderung dapat lebih banyak klik", PIN_STUDY, "rasmi"),
 ("Pin wall art sebagai 'Home Decor' (cth. 'Art for a Scandinavian living room'), bukan sebagai 'Art'", "https://www.wildlifeartstore.com/selling-art-on-pinterest/", "lemah"),
 ("Typography kini staple wall art: quote berani, type minimal, mesej peribadi", "https://www.hakyarts.com/blogs/general/top-wall-art-poster-trends-to-watch-in-2026", "pihak_ketiga"),
 ("Poster teks lebih 'deliberate': serif elegan dan ruang lapang", "https://posterscape.com/blogs/wall-decor/poster-trends-the-must-have-decorative-wall-art-styles", "pihak_ketiga"),
 ("Fon tulisan tangan dan estetik analog berterusan ke 2026; arah ke typography berani dan playful, bukan minimal semata-mata", "https://wix.com/wixel/resources/typography-trends", "pihak_ketiga"),
 ("Quote 'kitchen' generik dengan fon klise semakin tidak digemari", "https://aboutwallart.com/blogs/news-articles-home-decor-inspiration/kitchen-wall-art-expert-interior-design-tips-trends-2026", "pihak_ketiga"),
 ("Kertas tanpa bingkai melengkung dalam kelembapan bilik air dalam beberapa minggu; bingkai/akrilik lebih selamat", "https://www.gelato.com/au/blog/bathroom-wall-art-ideas", "pihak_ketiga"),
]
S = [  # niche_id, gaya, palet, kategori fon (cadangan Google Fonts OFL), contoh jenis ayat, adegan mockup, format disyorkan, contoh overlay pin, bukti
 ("classroom", "Retro berwarna atau boho neutral; set bertema", "Pastel (hijau, biru lembut) atau neutral + aksen retro", "Rounded/playful: Fredoka, Baloo 2; retro: Shrikhand", "Peraturan kelas, growth mindset, sambutan", "Dinding kelas dengan set 6-12 poster", "Set poster matte + bundle printable", "Retro Classroom Decor Set of 12",
  [("Kelas pastel antara trend dekor terbesar 2026; neutral kekal digemari", "https://missjacobslittlelearners.com/blogs/blog/2026-classroom-decor-trends", "pihak_ketiga"), ("Bilik darjah retro berwarna lawan minimalis", "https://www.twinkl.com/blog/back-to-school-2025-classroom-decor-ideas", "pihak_ketiga")]),
 ("counselor", "Lembut, tenang, botanikal; ikon perasaan ringkas", "Hijau sage, biru lembut, krim", "Rounded sans: Nunito, Quicksand", "Kemahiran tenang, afirmasi, carta perasaan", "Sudut calm corner dengan bantal & tumbuhan", "Bundle printable + set poster", "Calm Corner Posters Set",
  [("Sempadan botanikal memberi rasa tenang dan neutral yang tidak mengganggu deria", "https://www.twinkl.com/resource/pampas-grass-boho-neutral-editable-poster-t-ag-1688820834", "pihak_ketiga")]),
 ("bathroom", "Vintage / Art Deco + humor; set 3", "Hitam-putih, hijau jade, aksen emas", "Art Deco: Poiret One, Limelight; serif klasik: Playfair Display", "Tanda lucu bilik air", "Dinding atas tandas / tepi cermin", "Poster berbingkai (tahan lembap) + set 3", "Funny Bathroom Wall Art Set of 3",
  [("Gaya vintage untuk bilik air berkarakter (2026)", "https://mixtiles.com/blog/wall-art-home-decor/trending-bathroom-home-decors-ideas", "pihak_ketiga"), ("Penjual Etsy gabung humor dengan Art Deco/maximalist", "https://www.etsy.com/listing/1161346307", "rasmi")]),
 ("kitchen", "Retro bistro / gaya 'menu'; elak quote klise", "Krim, merah tomato, hijau zaitun", "Retro serif: Fraunces; slab vintage: Alfa Slab One", "Menu kopi, quote dapur lucu, hidangan keluarga", "Coffee bar atau dinding dapur", "Poster matte / berbingkai, set 2-3", "Retro Coffee Bar Sign Print",
  [("Kitchen 2026: tekstur, warna, nostalgia; papan gaya menu", "https://aboutwallart.com/blogs/news-articles-home-decor-inspiration/kitchen-wall-art-expert-interior-design-tips-trends-2026", "pihak_ketiga"), ("Gaya bistro Paris vintage dalam gallery wall dapur", "https://www.homesandgardens.com/celebrity-homes/ina-garten-kitchen-wall-art", "pihak_ketiga")]),
 ("home_office", "Neo Deco / luxe office; motivasi elegan", "Hijau emerald, biru safir, burgundy + emas/brass", "Art Deco: Poiret One; serif mewah: Cormorant Garamond", "Motivasi kerja, humor pejabat", "Meja kerja / cubicle dengan aksesori brass", "Poster berbingkai, poster matte kecil", "Chic Cubicle Decor Print",
  [("Pinterest Fall 2025: Art Deco Revival & Chic Cubicle Decor; palet jewel tone + brass", "https://www.aol.com/articles/pinterest-predicts-biggest-interior-design-211700524.html", "rasmi")]),
 ("reading_nook", "Poetcore / akademik vintage; ikut trope buku", "Coklat, hijau gelap, krim kertas lama", "Serif klasik: Cormorant Garamond, EB Garamond", "Quote buku, trope romantasy, 'just one more chapter'", "Sudut membaca dengan rak buku & lampu", "Poster matte, set 2-3, printable", "Reading Nook Wall Art Print",
  [("Estetik poetcore 2026", "https://dynamicmockups.com/trends/poetcore-mockups-2026-aesthetic/", "pihak_ketiga"), ("Design ikut trope lebih laku", "https://printify.com/knowledge-hub/booktok-trope-merch-2026-playbook-high-margin-print-on-demand-profit/", "pihak_ketiga")]),
 ("bedroom", "Script romantik / serif elegan, ruang lapang", "Neutral hangat, plum gelap (Plum Noir)", "Script: Dancing Script, Great Vibes; serif: Playfair Display", "Quote cinta, tidur, pasangan", "Dinding atas kepala katil (penempatan paling dicari)", "Set 2 berbingkai / canvas", "Above Bed Wall Art Set of 2",
  [("Dinding atas kepala katil = penempatan bilik tidur paling dicari", "https://www.gelato.com/ja/blog/wall-decor-by-room-guide", "pihak_ketiga"), ("Plum Noir antara warna Pinterest 2026", "https://www.homesandgardens.com/interior-design/pinterest-palette-2026", "rasmi")]),
 ("living_room", "Typography besar minimal atau dalam bingkai hiasan; gabung abstrak", "Cool Blue, Jade, neutral", "Serif besar: Fraunces; sans bersih: Montserrat", "Quote keluarga, rumah, 'gather'", "Ruang tamu penuh (gaya bilik keseluruhan)", "Canvas / berbingkai besar, set gallery wall", "Living Room Gallery Wall Set",
  [("Cool Blue +85% minat (Pinterest 2026)", "https://www.homesandgardens.com/interior-design/pinterest-palette-2026", "rasmi"), ("Tema ruang tamu didominasi foto/landskap/abstrak", "https://www.lowes.com/n/buying-guide/wall-art-decor-buying-guide", "pihak_ketiga")]),
 ("nursery", "Boho neutral atau circus/Funhaus", "Oat, krim, sage; atau merah-krim circus", "Script lembut: Caveat; rounded: Fredoka", "Afirmasi bayi, nama (fasa 2), ayat iman", "Nursery neutral dengan satu poster berbingkai", "Poster berbingkai, canvas, set 3", "Neutral Nursery Wall Art Print",
  [("Gender-neutral boho: oat, cream, tan, sage", "https://www.nestig.com/blogs/get-inspired/the-nursery-and-kids-room-trends-designers-are-backing-in-2026", "pihak_ketiga"), ("'circus nursery' +50% (Pinterest)", "https://www.aol.com/articles/pinterests-2026-interior-design-trends-171800656.html", "rasmi")]),
 ("laundry", "Tanda vintage / farmhouse, ikon ringkas", "Biru pudar, krim, hitam", "Vintage sign: Rye, Alfa Slab One", "Humor dobi, arah zon", "Rak dobi kecil", "Poster matte, set 2", "Vintage Laundry Room Sign",
  [("Trend 'design moment' kecil di bilik dobi; tanda minimalis/ikon", "https://www.coohom.com/article/laundry-room-sign-ideas-5-creative-options", "pihak_ketiga")]),
 ("seasonal_xmas", "Vintage, neutral atau gothic Victorian", "Merah gelap, hijau pine, krim", "Serif vintage: Playfair Display; script: Great Vibes", "Ucapan Krismas, lagu, nostalgia", "Mantel / dinding ruang tamu berhias", "Printable + poster matte", "Vintage Christmas Wall Art Printable",
  [("Printable Krismas vintage, neutral, gothic antara yang tersenarai di Etsy ($2-3)", "https://www.etsy.com/listing/1343560341", "rasmi")]),
 ("home_gym", "Bold condensed, motivasi; tahan lembap", "Hitam, kelabu, satu warna terang", "Condensed: Bebas Neue, Oswald", "Motivasi latihan", "Dinding gym rumah", "Poster laminasi/berbingkai, set 3-5", "Home Gym Motivation Poster Set",
  [("Prints kalis air/akrilik/laminasi sesuai gym lembap", "https://www.wallpics.com/blogs/news/transform-your-workout-space-home-gym-wall-art-trends", "pihak_ketiga")]),
]
out = {"stage": "P3", "title": "Gaya design & pin wall art", "updated": "2026-11-21",
       "font_note": "Fon ialah cadangan keluarga Google Fonts berlesen SIL OFL; sahkan lesen setiap fon sebelum digunakan (termasuk untuk jualan fail digital).",
       "pin_rules": [{"rule": r, "source": s, "level": l} for r, s, l in rules],
       "pin_templates_wallart": [
         {"id": "W1", "template": "Mockup bilik penuh + overlay nama bilik", "share_pct": 40},
         {"id": "W2", "template": "Gallery wall / set 3 dalam bilik", "share_pct": 20},
         {"id": "W3", "template": "Close-up typography + tekstur kertas/bingkai", "share_pct": 15},
         {"id": "W4", "template": "Kolaj pilihan warna/saiz", "share_pct": 10},
         {"id": "W5", "template": "Video pendek (zoom ke bilik)", "share_pct": 15}],
       "styles": [{"niche_id": n, "style": st, "palette": p, "fonts": f, "phrases": ph, "mockup": m, "format": fm, "pin_overlay": o,
                   "evidence": [{"claim": c, "source": s, "level": l} for c, s, l in ev]} for n, st, p, f, ph, m, fm, o, ev in S]}
json.dump(out, open(os.path.join(ROOT, "data", "posters", "styles.json"), "w"), indent=2, ensure_ascii=False)
print(len(S), "gaya;", len(rules), "peraturan")
