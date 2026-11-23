"""Tab Setup (checklist, disemak & ditanda oleh Claude) dan tab Workflow (harian/mingguan/bulanan).
Jalankan: python3 scripts/build_setup.py  ->  data/export/setup/{setup_checklist,workflow}.json
setup_checklist ditulis ke stor dashboard (data/setup/checklist/<id>); Claude kemas kini status selepas setiap semakan."""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "data", "export", "setup")
os.makedirs(OUT, exist_ok=True)
CHECKED = "2026-11-21"
PH = {0: "Riset & perancangan", 1: "Asas laman web", 2: "Kedai & bayaran", 3: "Pinterest", 4: "Analisa", 5: "Kandungan & pelancaran"}

# (fasa, langkah, siapa, sambung, cara Claude semak, status, hasil semakan)
S = [
 (0, "Riset pasaran, niche, kata kunci dan model untung", "Claude", "–", "Fail riset dalam repo", "Siap", "Riset utama + poster P1–P8 siap"),
 (0, "Dashboard dan peraturan repo (CLAUDE.md)", "Claude", "–", "Versi dashboard & commit repo", "Siap", "Dashboard 4 tab; CLAUDE.md di-push"),
 (1, "Pilih nama brand", "Bersama", "–", "Keputusan anda dalam chat", "Perlu keputusan anda", "Cadangan awal: Warmly Said; belum dipilih"),
 (1, "Beli domain di Cloudflare Registrar (~$11/tahun)", "Anda", "Cloudflare", "Semak DNS domain menghala ke Cloudflare", "Belum", "Tiada domain lagi (domain lama tamat)"),
 (1, "Beli hosting Hostinger Business (~$19/bulan)", "Anda", "Hostinger", "Laman hosting menjawab", "Belum", "Belum dibeli"),
 (1, "Sambung domain → Cloudflare → hosting, SSL aktif", "Bersama", "Cloudflare DNS", "Laman dibuka dengan https", "Belum", "Menunggu domain dan hosting"),
 (1, "Pasang WordPress + WooCommerce", "Anda", "Hostinger", "API kedai WooCommerce menjawab", "Belum", "Menunggu hosting"),
 (1, "Tetapan Cloudflare: jangan cache troli/checkout, Bot Fight Mode OFF, Turnstile", "Bersama", "Cloudflare", "Header cache BYPASS pada /cart dan /checkout", "Belum", "Claude sediakan tetapan bila domain siap"),
 (2, "Akaun Printify", "Anda", "Printify", "Claude boleh senarai kedai Printify", "Sedang", "Ada (kata anda); belum disahkan Claude"),
 (2, "Sambung Printify ke WooCommerce (plugin)", "Anda", "Printify plugin", "Produk ujian muncul di WooCommerce", "Belum", "Menunggu WooCommerce"),
 (2, "Sambung Printify ke Claude (klik link izin)", "Anda", "Composio Printify", "Claude boleh senarai kedai Printify", "Belum", "Tiada sambungan (semakan Composio 21 Nov)"),
 (2, "Stripe + PayPal untuk terima bayaran", "Anda", "Stripe, PayPal", "Checkout ujian berjaya", "Belum", "Belum didaftar"),
 (2, "Halaman kedai: homepage, koleksi, polisi shipping/refund/privacy, About", "Bersama", "WordPress", "Halaman wujud dan dipautkan di menu", "Belum", "Claude tulis teks; anda semak dan tampal"),
 (2, "Order sampel poster (matte 18×24, berbingkai 11×14, canvas 16×20)", "Anda", "Printify", "Gambar sampel diterima", "Belum", "Untuk sahkan kualiti dan foto produk"),
 (3, "Buka semula akaun Pinterest Business", "Anda", "Pinterest", "Akaun Business aktif", "Belum", "Perlu dibuka semula (kata anda)"),
 (3, "Claim domain + Pinterest Tag + Rich Pins", "Bersama", "Pinterest", "Domain disahkan; pin tunjuk harga", "Belum", "Menunggu domain dan akaun Pinterest"),
 (3, "App Pinterest Developers → mohon akses Standard (auto-pin)", "Bersama", "Pinterest API", "App ada akses Standard", "Belum", "Claude tulis permohonan; anda hantar"),
 (3, "Sambung Pinterest ke Claude (klik link izin)", "Anda", "Composio Pinterest", "Claude boleh baca board", "Belum", "Tiada sambungan (semakan Composio 21 Nov)"),
 (3, "Cipta 10–15 board ikut niche", "Claude", "Pinterest API", "Board wujud dengan nama berkata kunci", "Belum", "Selepas Pinterest disambung"),
 (4, "Google Analytics 4 (plugin Site Kit)", "Anda", "Google Analytics", "Tag GA4 ada pada laman", "Belum", "Menunggu laman web"),
 (4, "Google Search Console", "Anda", "Google", "Domain disahkan", "Belum", "Menunggu domain"),
 (4, "Microsoft Clarity", "Anda", "Clarity", "Skrip Clarity ada pada laman", "Belum", "Menunggu laman web"),
 (4, "MailPoet + borang emel", "Bersama", "MailPoet", "Borang emel tampil; emel ujian diterima", "Belum", "Claude tulis emel alu-aluan"),
 (4, "Templat UTM untuk setiap pin", "Claude", "–", "Link pin ada utm_source=pinterest", "Belum", "Bila domain siap"),
 (5, "Senarai frasa emosi (100 pertama, kemudian 3,000)", "Bersama", "–", "Fail senarai frasa dalam repo", "Belum", "Claude jana; anda luluskan"),
 (5, "Semak trademark setiap frasa (USPTO)", "Bersama", "USPTO", "Setiap frasa ada status semakan", "Belum", "Sebelum upload"),
 (5, "Pilih 10 font OFL + templat poster", "Claude", "Google Fonts", "Fail templat dan lesen font dalam repo", "Belum", "–"),
 (5, "Mockup bilik (foto Unsplash/Pexels)", "Claude", "–", "Mockup dijana untuk setiap produk", "Belum", "Dynamic Mockups belum disambung (pilihan)"),
 (5, "30 produk pertama live", "Bersama", "Printify, WooCommerce", "30 produk aktif di kedai", "Belum", "–"),
 (5, "Mula pin: 5 sehari pada 30 hari pertama", "Claude", "Pinterest API", "Pin dijadualkan dan diterbitkan", "Belum", "–"),
]
READY = {3, 4, 5, 9, 11, 14, 15, 25, 26, 27, 28}   # boleh dibuat sekarang, tidak menunggu langkah lain
checklist = [{"id": f"s{i:02d}", "no": i, "phase_no": p, "phase": PH[p], "step": st, "who": w, "connect": c, "how_check": h,
              "status": s, "checked_at": CHECKED, "result": r} for i, (p, st, w, c, h, s, r) in enumerate(S, 1)]
for row in checklist: row["ready"] = row["no"] in READY or row["status"] == "Siap"

# (kekerapan, siapa, tugas, minit anda, alat)
WF = [
 ("Harian", "Claude", "Jana 8–10 design lettering baru (gaya S1–S6, 4 seed setiap quote; SOP P9)", 0, "Kaggle GPU / MOSS CPU (scripts/lettering)"),
 ("Harian", "Claude", "Semak trademark frasa baru", 0, "USPTO"),
 ("Harian", "Claude", "Jana mockup bilik dan pin untuk produk baru", 0, "Skrip mockup"),
 ("Harian", "Claude", "Upload produk baru ke Printify / WooCommerce sebagai draf", 0, "Printify API"),
 ("Harian", "Claude", "Jadualkan 10 pin (1 URL setiap 7 hari, tag UTM)", 0, "Pinterest API"),
 ("Harian", "Claude", "Semak pesanan dan masalah Printify; beritahu jika ada isu", 0, "Printify"),
 ("Harian", "Anda", "Luluskan design, produk dan pin hari ini", 15, "Dashboard / chat"),
 ("Harian", "Anda", "Jawab emel pelanggan", 10, "Emel"),
 ("Mingguan", "Claude", "Laporan prestasi mingguan ke tab Prestasi (Pinterest, GA4, WooCommerce)", 0, "Dashboard"),
 ("Mingguan", "Claude", "Cari pin dan produk yang menang; jana variasi baru", 0, "Pinterest Analytics"),
 ("Mingguan", "Claude", "Cadang 3–5 tindakan untuk peringkat corong paling lemah", 0, "Dashboard"),
 ("Mingguan", "Claude", "Semak kelajuan laman dan tetapan Cloudflare", 0, "PageSpeed, Cloudflare"),
 ("Mingguan", "Anda", "Baca laporan dan pilih tindakan", 15, "Dashboard"),
 ("Mingguan", "Anda", "Semak 10 produk di telefon (gambar, harga, checkout)", 15, "Laman web"),
 ("Bulanan", "Claude", "Banding jualan dengan milestone; kemas kini ramalan", 0, "Dashboard"),
 ("Bulanan", "Claude", "Rancang tema musim 45–90 hari ke depan (kata kunci, board, design)", 0, "Pinterest Trends"),
 ("Bulanan", "Claude", "Arkibkan produk tanpa paparan selepas 90 hari", 0, "WooCommerce"),
 ("Bulanan", "Claude", "Semak kemas kini plugin, backup dan kos", 0, "WordPress"),
 ("Bulanan", "Anda", "Order 1–2 sampel produk baru untuk semak kualiti", 15, "Printify"),
 ("Bulanan", "Anda", "Semak bayaran Stripe/PayPal dan kos (hosting, sampel)", 15, "Stripe, PayPal"),
 ("Bulanan", "Anda", "Luluskan tema musim seterusnya", 10, "Chat"),
 ("Harian", "Claude", "QC lettering: ejaan 100% + 9 ciri gaya pada helaian semakan; gagal = seed baharu (maks 4)", 0, "sheet.py"),
 ("Harian", "Claude", "Siapkan design lulus: vektor SVG, palet tepat, tekstur, PNG 300 DPI 8×10 hingga 24×36", 0, "finish.py (potrace)"),
 ("Mingguan", "Claude", "Tulis 50 quote Inggeris 3–7 perkataan untuk minggu depan + semak trademark", 0, "Claude, USPTO"),
]
workflow = [{"id": f"w{i:02d}", "frequency": f, "freq_no": {"Harian": 1, "Mingguan": 2, "Bulanan": 3}[f], "who": w, "task": t,
             "user_min": m, "tool": tool} for i, (f, w, t, m, tool) in enumerate(WF, 1)]

def W(name, rows):
    with open(os.path.join(OUT, name), "w") as f:
        f.write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n")
    print(name, len(rows))
W("setup_checklist.json", checklist)
W("workflow.json", workflow)
from collections import Counter
print(Counter(r["status"] for r in checklist), Counter(r["who"] for r in checklist))
print({f: sum(r["user_min"] for r in workflow if r["frequency"] == f) for f in ("Harian", "Mingguan", "Bulanan")})
