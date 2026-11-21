"""Poster P2: kata kunci & volum carian. Tulis data/posters/keywords.json"""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")
R = "https://www.rankhero.com/keywords/"
K = [  # niche_id, kata kunci, carian/bulan, listing Etsy, niat, nota, sumber
 ("counselor", "calm corner", 6600, 23904, "khusus", "", R+"calm-corner"),
 ("counselor", "calming wall art", 880, None, "khusus", "", R+"calming-wall-art"),
 ("bathroom", "funny bathroom sign", 8100, 36886, "khusus", "US 81%", R+"funny-bathroom-sign"),
 ("bathroom", "bathroom sign", 22200, 145867, "khusus", "", R+"bathroom-sign"),
 ("bathroom", "bath wall decor", 22200, None, "khusus", "", R+"bath-wall-decor"),
 ("bathroom", "toilet wall art", 1600, None, "khusus", "", R+"toilet-wall-art"),
 ("bathroom", "cat bathroom art", 1100, None, "khusus", "Julat 880-1,300", R+"cat-bathroom-art"),
 ("bathroom", "funny bathroom", 720, None, "khusus", "", R+"funny-bathroom"),
 ("bathroom", "bath decor", 60500, 244859, "luas", "Termasuk aksesori bilik air", R+"bath-decor"),
 ("classroom", "classroom posters", 6600, 144725, "khusus", "US 55%", R+"classroom-posters"),
 ("classroom", "teacher decorations", 1000, None, "khusus", "", R+"teacher-decorations"),
 ("kitchen", "kitchen art", 22200, None, "khusus", "", R+"kitchen-art"),
 ("kitchen", "kitchen sign", 5400, None, "khusus", "", R+"kitchen-sign"),
 ("kitchen", "kitchen poster", 1450, None, "khusus", "Julat 1,300-1,600 (Sep-Dis 2025)", R+"kitchen-poster"),
 ("kitchen", "coffee bar", 165000, 107184, "luas", "Niat utama perabot/stesen kopi; anggaran bulanan rata", R+"coffee-bar"),
 ("home_office", "office decor", 18100, None, "khusus", "Puncak setiap Februari (Treendly)", "https://treendly.com/trend/office-decor"),
 ("home_office", "office wall décor", 8100, None, "khusus", "US 54%", R+"office-wall-décor"),
 ("home_office", "office art", 5400, 4860615, "khusus", "Sangat sesak di Etsy", R+"office-art"),
 ("home_office", "wall decor for home office", 880, None, "khusus", "", R+"wall-decor-for-home-office"),
 ("reading_nook", "bookish print", 40500, None, "khusus", "Angka tinggi luar biasa; perlu disemak", R+"bookish-print"),
 ("reading_nook", "bookish wall art", 1300, 112165, "khusus", "", R+"bookish-wall-art"),
 ("reading_nook", "reading wall art", 210, None, "khusus", "", R+"reading-wall-art"),
 ("reading_nook", "book nook", 450000, None, "luas", "Niat utama diorama 'book nook', bukan wall art", R+"book-nook"),
 ("living_room", "livingroom art", 27100, None, "khusus", "27,100-33,100 (Sep 2025-Mac 2026)", R+"livingroom-art"),
 ("living_room", "wall art decor", 24650, None, "khusus", "Julat 22,200-27,100", R+"wall-art-decor"),
 ("living_room", "home decor wall art", 6600, None, "khusus", "", R+"home-decor-wall-art"),
 ("living_room", "home wall art", 2900, None, "khusus", "", R+"home-wall-art"),
 ("bedroom", "bedroom art", 8100, None, "khusus", "Jan 2026", R+"bedroom-art"),
 ("bedroom", "above bed art", 1900, 63000, "khusus", "US 68%", R+"above-bed-art"),
 ("bedroom", "bedroom decor", 60500, None, "luas", "Puncak Ogos 2026", R+"bedroom-decor"),
 ("nursery", "nursery art", 8100, None, "khusus", "", "https://adtargeting.io/industry/wall-decoration-keywords"),
 ("nursery", "nursery wall sticker", 8100, 110571, "khusus", "Produk sticker, bukan poster", R+"nursery-wall-sticker"),
 ("nursery", "baby nursery wall decor", 480, None, "khusus", "", "https://unicornseo.com/best-keywords-niche/Baby%20Nursery"),
 ("nursery", "bible verse nursery", 480, None, "khusus", "", R+"bible-verse-nursery"),
 ("nursery", "nursery wall print", 390, None, "khusus", "Menurun", R+"nursery-wall-print"),
 ("laundry", "laundry room sign", 2900, None, "khusus", "US 66%", R+"laundry-room-sign"),
 ("laundry", "laundry wall art", 590, None, "khusus", "", R+"laundry-wall-art"),
 ("seasonal_xmas", "christmas art", 22200, 4118220, "khusus", "Sep 8,100 -> Dis 135,000", R+"christmas-art"),
 ("wedding_signs", "wedding sign", 27100, 554302, "khusus", "US 45%", R+"wedding-sign"),
 ("entryway", "welcome sign", 33100, None, "khusus", "Campuran rumah & majlis; US 55%", R+"welcome-sign"),
 ("home_gym", "gym poster", 9900, None, "khusus", "Puncak 12,100 (Sep 2025)", R+"gym-poster"),
 ("home_gym", "home gym decor", 1900, 94913, "khusus", "US 53%", R+"home-gym-decor"),
 ("dorm", "dorm decor", 8100, 2366012, "khusus", "US 96%", R+"dorm-decor"),
 ("dorm", "dorm posters", 1000, 773960, "khusus", "", R+"dorm-posters"),
 ("faith", "bible art", 12100, None, "khusus", "", R+"bible-art"),
 ("faith", "bible poster", 2900, None, "khusus", "", R+"bible-poster"),
 ("faith", "church wall decor", 390, None, "khusus", "", R+"church-wall-decor"),
 ("faith", "bible verse", 1220000, 682584, "luas", "Carian maklumat, bukan niat beli", R+"bible-verse"),
 ("playroom", "playroom wall art", 1000, 203381, "khusus", "", R+"playroom-wall-art"),
 ("dining", "kitchen dining room", 880, None, "khusus", "", R+"kitchen-dining-room"),
 ("dining", "dining room", 150000, None, "luas", "Julat 135,000-165,000; niat perabot", R+"dining-room"),
 ("sets", "wall art printable", 14800, 3422402, "khusus", "", R+"wall-art-printable"),
 ("sets", "printable wallart", 6600, None, "khusus", "", R+"printable-wallart"),
 ("sets", "wall art set of 3", 5400, 369018, "khusus", "", R+"wall-art-set-of-3"),
 ("sets", "set of three prints", 260, 22161, "khusus", "", R+"set-of-three-prints"),
]
NAMES = {r["id"]: r["niche"] for r in json.load(open(os.path.join(ROOT, "data", "posters", "niches.json")))["niches"]}
NAMES["sets"] = "Set & printable (semua bilik)"
rows = []
for nid, kw, vol, lst, intent, note, src in K:
    opp = round(vol / lst * 1000) if (lst and intent == "khusus") else None
    rows.append({"niche_id": nid, "niche": NAMES.get(nid, nid), "keyword": kw, "google_monthly": vol, "etsy_listings": lst,
                 "opportunity": opp, "intent": intent, "note": note, "source": src})
out = {"stage": "P2", "title": "Kata kunci poster dan volum carian", "updated": "2026-11-21",
       "method": "Volum: anggaran RankHero (global) kecuali dinyatakan. Peluang = carian/bulan ÷ 1,000 listing Etsy, hanya untuk kata kunci berniat khusus. Pinterest: tiada volum mutlak awam (indeks relatif 0-100 sahaja).",
       "keywords": rows,
       "decision_updates": [
         {"niche_id": "counselor", "from": "Gelombang 2", "to": "Gelombang 1", "reason": "'calm corner' 6,600 carian/bulan dengan hanya 23,904 listing (peluang 276, tertinggi)"},
         {"niche_id": "home_office", "note": "Pertumbuhan Pinterest besar tetapi 'office art' sangat sesak di Etsy (4.86 juta listing): sasar long-tail (cubicle decor, funny office sign)"},
         {"niche_id": "dorm", "note": "Sesak (peluang 1-3); kekal Gelombang 2"}]}
json.dump(out, open(os.path.join(ROOT, "data", "posters", "keywords.json"), "w"), indent=2, ensure_ascii=False)
for r in sorted([r for r in rows if r["opportunity"]], key=lambda r: -r["opportunity"]): print(r["keyword"], r["opportunity"])
