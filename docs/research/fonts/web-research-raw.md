# Free-for-commercial-use fonts: sources, licences, mood research (2026-11-22)

## 0. How this was checked (read first)
- **Network limit in this session:** most font sites were blocked (DNS/proxy refusal): fonts.google.com, openfontlicense.org, creativecommons.org, dafont, 1001fonts, fontspace, fontesk, befonts, typodermicfonts, creativefabrica, behance, collletttivo.it, open-foundry.com, uncut.wtf, design-research.be, losttype, fontsarena, atipo, tunera, pixelsurplus, freefaces.gallery, usemodify, fontlibrary.org, envato, creativemarket, all journal sites.
- **Opened directly (curl/WebFetch):** fontsquirrel.com (FAQ, licence pages, font pages), theleagueofmoveabletype.com, velvetyne.fr (it currently shows only a strike page), gitlab.com/velvetyne, raw.githubusercontent.com (google/fonts, theleagueof, indestructible-type, rektdeckard), apache.org, and one Microsoft Research PDF.
- **Evidence labels used:**
  - **official**: I opened the licence text or the rights holder's own page.
  - **3rd-party (opened)**: I opened a copy on another site, e.g. Font Squirrel's copy of the designer's licence.
  - **weak**: I only saw the page through a web-search summary and did not open it. This includes official pages seen only in search results. Re-check these before you rely on them.
- **Safe workflow for every font:** download the font. Read the LICENSE/OFL/readme file in the zip, take a screenshot of it, and save it with the date in `docs/`. Export printables as flattened PNG/JPG or as PDF with text converted to outlines. Never sell editable templates that contain the font, and never share the font file.

---

## TASK A: Resource websites (31 entries)

Legend for the "Print / Digital" columns: **Y** = selling printed posters or digital printable files made with the font is allowed by the licence. **Per font** = depends on each font's licence. **N** = not allowed for free.

| # | Site / URL | Good for | Licence model | Print / Digital | Catch | Evidence URL (what I read) | Level |
|---|---|---|---|---|---|---|---|
| 1 | Google Fonts: fonts.google.com + github.com/google/fonts | All styles, incl. 78 "Brush", 29 "Blackletter", 40 "Woodtype", 286 "Handwritten" families (tag counts from families.csv) | OFL / Apache / UFL | Y / Y | Already known. Safest source. | https://raw.githubusercontent.com/google/fonts/main/ofl/abeezee/OFL.txt ; https://raw.githubusercontent.com/google/fonts/main/tags/all/families.csv | official |
| 2 | Fontshare: fontshare.com | Modern display, some serif and script | ITF FFL v2 | Y / Y | Already known. Licence page needs JavaScript, so I could not re-read it. No redistribution of font files. | https://www.fontshare.com/licenses/itf-ffl (JS only, not readable) | weak (re-check) |
| 3 | Font Squirrel: fontsquirrel.com | Every style; good "handdrawn", "script", "grunge" lists | Mixed; curated per font | Per font (mostly Y) | FAQ: "we can't [guarantee]… read the license on each font". Some listed fonts are **"Freeware License: found on the internet and did not come with a license"** (e.g. Brushstroke Plain, Scratch, Destroy, Copystruct). **Avoid those.** Some listed fonts are even **personal-use only** (HVD Peace, HVD Poster: "free for personal use. For commercial use please contact us"). | https://www.fontsquirrel.com/faq ; https://www.fontsquirrel.com/license/Brushstroke-Plain ; https://www.fontsquirrel.com/license/hvd-peace | official (site) |
| 4 | Velvetyne: velvetyne.fr + gitlab.com/velvetyne | Experimental display, brutal, retro, blackletter-ish (e.g. Bluu Next) | Mostly SIL OFL 1.1; per-font LICENSE in repo | Y / Y (OFL fonts) | Main site currently shows only a strike notice ("EN GRÈVE"). Use the GitLab repos and check each LICENSE.txt. | https://gitlab.com/velvetyne/ouroboros/-/blob/master/LICENSE.txt ("licensed under the SIL Open Font License 1.1"); https://velvetyne.fr/ (strike page) | official (per repo) |
| 5 | The League of Moveable Type: theleagueofmoveabletype.com + github.com/theleagueof | Retro condensed (League Gothic, Ostrich), script (League Script), display (Blackout) | OFL | Y / Y | None. Footer: "All the fonts… are free & open source, available to use commercially and subject to the Open Font License." | https://www.theleagueofmoveabletype.com/faq ; https://raw.githubusercontent.com/theleagueof/league-gothic/master/OFL.md ; https://www.fontsquirrel.com/license/league-script (OFL) | official |
| 6 | Collletttivo: collletttivo.it | Italian experimental display (Mattone, Ortica, Necto Mono) | OFL | Y / Y | Credit to designer and foundry is *requested*. OFL itself does not require it. | https://www.collletttivo.it/licensing (search summary: "free under Open Source OFL… personal and commercial projects on printed and digital media") | weak |
| 7 | Open Foundry: open-foundry.com | Curated specimens of open-source fonts | Directory; fonts hosted elsewhere | Per font (mostly OFL) | Not a host: check the licence at the source. | https://licenseorg.com/guide/fonts/open-foundry (search summary only) | weak |
| 8 | Uncut.wtf: uncut.wtf | Contemporary display, grotesk, experimental | Directory; mostly libre | Per font | Search summary: "some of the fonts do not have an explicit license". Check each one. | https://www.fontsquirrel.com/license/uncut-sans (search summary: Uncut Sans = OFL) | weak |
| 9 | Badass Libre Fonts by Womxn: design-research.be/by-womxn | Display, experimental | Directory of FLOSS-licensed fonts | Per font | Licence differs per font. | https://stockholmstypografiskagille.se/typonyheter/badass-libre-open-source-font-collection-womxn/ (search summary) | weak |
| 10 | Fontesk: fontesk.com | Brush, script, retro, display (large) | Mixed: each font page says "Desktop Commercial Use" or "Personal Use" | Per font | Many personal-use-only fonts sit next to commercial ones. Use the "free for commercial use" section, then read the font's own licence. | https://licenseorg.com/guide/fonts/fontesk (search summary) | weak |
| 11 | Fontfabric free fonts: fontfabric.com | Display, script (Nickainley), textured (Intro Rust) | Own "Fontfabric Free Font EULA" (FFF EULA) | Y / Y | FFF EULA 2.0: "can be used for both personal and commercial work (except 'Baron')". Allows printed material and T-shirts, plus PDFs and templates. You may **not** modify, resell or redistribute the font files. Newer v2.1 (2019) wording seen only via search. Some Fontfabric fonts are **trial/non-commercial**, so check each one. | https://www.fontsquirrel.com/license/nickainley (FFF EULA 2.0 text); https://www.fontfabric.com/fontfabric-non-commercial-eula-for-trial-fonts/ (search only) | 3rd-party (opened) |
| 12 | **Lost Type Co-op**: losttype.com | Retro/vintage display (excellent style) | Pay-what-you-want = **personal licence only** | **N at $0** / N | **RISKY at $0.** Search summary: personal use = "work without a monetary benefit". The commercial licence (covers "printed goods") is paid (~US$25+/font per a third-party guide). | https://losttype.com/contact ; https://licenseorg.com/guide/fonts/lost-type (search summaries) | weak |
| 13 | **Befonts**: befonts.com | Brush, script, vintage | Mixed; labels are only "a helpful indication" | Per font | **RISKY.** Many "personal use only" demo fonts; the site's own terms say it "does not guarantee that any font is free for commercial use". | https://befonts.com/licenses ; https://befonts.com/terms-of-use (search summaries) | weak |
| 14 | FreeFaces.gallery: freefaces.gallery | Trendy editorial display | Directory; mixed (OFL, "Free for commercial", **"Personal Use License"**) | Per font | Has personal-use entries. Check each font. | https://brandfetch.com/freefaces.gallery (search summary) | weak |
| 15 | Use & Modify: usemodify.com | Experimental libre display/serif | Directory of libre/open-source fonts (mostly OFL) | Per font (mostly Y) | Curator: Raphaël Bastide. Check each font's licence. | https://imjustcreative.com/use-modify/2020/07/16 (search summary) | weak |
| 16 | Font Library: fontlibrary.org | Many styles incl. handwriting, blackletter | Libre only: OFL, GPL+FE, MIT, public domain etc. | Y (OFL/MIT); GPL+FE also OK for documents | Guidebook warns that "public domain" claims for fonts can be doubtful. | https://fontlibrary.org/guidebook/supported_licenses (search summary) | weak |
| 17 | Typodermic (Raymond Larabie): typodermicfonts.com | Retro, sci-fi, horror, brush (Chinese Rocks), spray (Octin Spraypaint) | Free desktop fonts under a desktop EULA (Font Squirrel shows the Fontspring Desktop EULA 1.7) | Y / Y (as fixed graphics) | Desktop use only; no web/app/ebook embedding. Fontspring EULA forbids "alphabet or letterform products for resale" (stamps, stickers of single letters), but word/phrase products are OK. Some Typodermic fonts are CC0 (search). | https://www.fontsquirrel.com/license/chinese-rocks ; https://www.fontsquirrel.com/license/octin-spraypaint-free ; https://typodermicfonts.com/license/ (search only) | 3rd-party (opened) |
| 18 | Indestructible Type: indestructibletype.com + github.com/indestructible-type | Serif (Besley), mono (Drafting) | OFL | Y / Y | None. | https://raw.githubusercontent.com/indestructible-type/Drafting/main/OFL.txt ; Besley repo OFL.txt present (HTTP 200) | official |
| 19 | Departure Mono: departuremono.com + github.com/rektdeckard/departure-mono | Pixel/retro-computer | Font = SIL OFL; site code = MIT | Y / Y | None. | https://raw.githubusercontent.com/rektdeckard/departure-mono/main/README.md (Licenses table) | official |
| 20 | Production Type free fonts | Serif (Spectral) | OFL (Spectral) | Y / Y | Most of their fonts are paid; only the Google-commissioned ones are free. | https://www.fontsquirrel.com/license/spectral (search summary: OFL) | weak |
| 21 | Tunera Type Foundry: tunera.xyz | Libre display/serif | OFL (per third-party) | Y / Y (if OFL confirmed) | Confirm the OFL file in each download. | https://uiuxshowcase.com/resources/tunera (search summary) | weak |
| 22 | Atipo Foundry: atipofoundry.com | Display, geometric | Pay-what-you-want / "pay with tweet"; one free weight | **Unknown** | **CAUTION:** no source found that states commercial rights for the free weight. | https://ecomm.design/site/atipo (search summary) | weak |
| 23 | 1001 Fonts: 1001fonts.com | Huge; filter "free for commercial use" | Own FFC licence plus FFP (personal) and per-author terms | Y only for FFC fonts | FFC: "free of charge for personal and commercial use… as long as the use is not racist or illegal". FFP = no commercial use. Mostly personal-use catalogue. | https://www.1001fonts.com/licenses/ffc.html ; /ffp.html (search summaries) | weak |
| 24 | FontSpace: fontspace.com/commercial-fonts | Brush, script, kids, horror | Per designer (Freeware, OFL, PD, personal) | Per font | Site terms defer to designers: "contact the respective designers". Use the commercial filter, then read the licence. | https://www.fontspace.com/about/terms ; https://www.fontspace.com/commercial-fonts (search summaries) | weak |
| 25 | **DaFont**: dafont.com | Every novelty style | Mostly "Free for personal use"; filter "100% Free" / "Public domain" | **N for most**; Y only for 100% Free/PD, after checking | **RISKY.** "Free for personal use… If you want to use it for… commercial purpose you have to pay a license" (forum). There is no official definition of "100% Free" that I could read. | https://www.dafont.com/forum/read/8186-4/what-does-free-for-personal-use-mean (search summary) | weak |
| 26 | **Creative Fabrica**: creativefabrica.com | Brush, script, craft/POD fonts | Subscription licence; free-trial and "freebies" | Y while subscribed (POD allowed); freebie terms **unclear** | **CAUTION.** You need an active subscription to make new designs. Converting letters to SVG/embroidery for sale is forbidden. I found no clear licence text for "free" fonts. | https://creativefabrica.com/de/subscription-license ; https://www.creativefabrica.com/pod/ (search summaries) | weak |
| 27 | Creative Market "Free Goods": creativemarket.com | Brush, script (weekly freebies) | Free fonts come with the Desktop Licence | Y / Y (as end products) | The help centre says "Free Fonts come with the Desktop License: The Desktop License allows you to create End Products for sale." Keep the download receipt. Goods expire weekly. | https://support.creativemarket.com/hc/en-us/articles/115006136967 (search summary) | weak |
| 28 | **Envato free files**: elements.envato.com | Brush, script | Separate "Free Files Use Policy" | **Unclear** | **CAUTION.** Limited licence; no redistribution. I found no clear statement of commercial rights for free-file fonts. | https://help.elements.envato.com/hc/en-us/articles/31035932718489-Free-Files-Use-Policy (search summary) | weak |
| 29 | **Behance freebies**: behance.net | Trendy brush, script | Per designer; many are **demo / personal only** | Per font, often N | **AVOID unless** the download includes a licence file that clearly says commercial. Behance's own "Personal" licence = "non-commercial projects". | https://help.behance.net/hc/en-us/articles/7416981176603 (search summary) | weak |
| 30 | Pixel Surplus freebies: pixelsurplus.com | Retro, textured | Unknown | **Unverified** | Could not find or open their licence. Treat as unknown. | – (search returned no licence page) | weak |
| 31 | Fonts Arena / Fontget / Republi.sh | Mixed | Unknown | **Unverified** | Searches returned nothing about their licences, and the sites were blocked. Do not use until checked. | – | weak |

**Best low-risk picks for non-sans styles:** Google Fonts (Brush, Handwritten, Blackletter, Woodtype, Vintage tags), League of Moveable Type, Velvetyne (GitLab), Font Library, Fontfabric free fonts, Typodermic free desktop fonts, and Font Squirrel (only after reading each licence page).

---

## TASK B: Licence cheat-sheet

| Licence | Sell printed posters? | Sell digital printable (PNG/PDF)? | Share the font file? | Attribution? | Source (level) |
|---|---|---|---|---|---|
| **SIL OFL 1.1** | Yes | Yes. OFL FAQ 1.13: "creating any kind of graphic using a font under OFL does not make the resulting artwork subject to the OFL." Embedding in a PDF is allowed (FAQ 1.12). | Yes, free, with the licence and copyright notice. Condition 1: the font "may [not] be sold by itself". | Not required. FAQ 1.1: mention the font "if you wish, but that is not required". | https://raw.githubusercontent.com/google/fonts/main/ofl/abeezee/OFL.txt ; https://raw.githubusercontent.com/theleagueof/licenses/master/OFL-FAQ.md (official) |
| **Apache 2.0** | Yes | Yes | Yes. §4: give recipients a copy of the licence and keep the notices. | Only when you redistribute the font (NOTICE file), not on artwork | https://www.apache.org/licenses/LICENSE-2.0.txt (official) |
| **Ubuntu Font Licence 1.0** | Yes | Yes. §4: "does not affect any document created using the Font Software" | Yes, with notice and licence. Renaming rules apply to modified versions. | Not for artwork | https://raw.githubusercontent.com/google/fonts/main/ufl/ubuntu/UFL.txt (official) |
| **ITF FFL (Fontshare)** | Yes (already known) | Yes | **No** redistribution of files | – | https://www.fontshare.com/licenses/itf-ffl (JS-only page, not re-read) (weak) |
| **CC0 / public domain** | Yes | Yes | Yes | No | Search summary of CC0 explainer (casrai.org) (weak). Note: Font Library warns that some "public domain" font claims are doubtful: https://fontlibrary.org/guidebook/supported_licenses (weak) |
| **CC-BY (3.0/4.0)** | Yes | Yes | Yes | **Yes**: "appropriate credit… in any reasonable manner". Put a credit in the listing description or file info. | https://creativecommons.org/licenses/by/ (search summary, weak). Example font: Snickles = "Creative Commons attribution license": https://www.fontsquirrel.com/license/Snickles (opened) |
| **CC-BY-ND** | Yes (commercial not excluded) | Yes | Yes, unmodified only | Yes | WC Mano Negra/WC Rhesus: https://www.fontsquirrel.com/license/WC-Mano-Negra-Bta (3rd-party opened). Attribution on products is awkward, so avoid it. |
| **"Freeware"** (generic word) | **Depends on the actual text.** Some say "commercial or non-commercial" (e.g. Dirty Ego, Gesso, Orchidee). Others are just "found on the internet… no license". | Same | Usually allowed free with the readme. Usually no sale and no modification. | Usually not | https://www.fontsquirrel.com/license/dirty-ego ; https://www.fontsquirrel.com/license/Scratch (3rd-party opened) |
| **"Free for personal use"** | **No** | **No** | Usually no | – | e.g. HVD licence: "free for personal use. For commercial use please contact us" https://www.fontsquirrel.com/license/hvd-peace (opened); DaFont forum (weak) |
| **DaFont "100% Free"** | Probably yes, but no official DaFont definition found. **Check the readme inside the zip.** | Same | Per readme | Per readme | DaFont forum and third-party guides via search (weak) |
| **1001fonts FFC** | Yes ("personal and commercial use… not racist or illegal") | Yes | Not stated in the text I saw | No (not stated) | https://www.1001fonts.com/licenses/ffc.html (search summary, weak) |
| **Fontspring Desktop EULA** (Typodermic free fonts on Font Squirrel) | Yes: "physical products… fixed size (JPG, PNG) or static vector (outlines)" | Yes, as flattened images or outlines. Embedded documents must be read-only. | No | No | https://www.fontsquirrel.com/license/chinese-rocks (opened) |
| **Fontfabric FFF EULA 2.0** | Yes ("printed material, T-shirts") | Yes (embedding in PDFs and templates allowed) | **No** resale or redistribution of the font; no modification of the font file | No | https://www.fontsquirrel.com/license/nickainley (opened) |
| **Creative Fabrica** (subscription / free trial) | Yes, for designs made while subscribed (POD allowed) | Yes ("sell those designs digitally as well as physically") | No; no SVG letter sets | No | creativefabrica.com subscription-license / pod pages (search summary, weak). **Freebie-specific terms not found.** |
| **Envato free files** | Unclear | Unclear | No | – | Free Files Use Policy (search summary, weak) |
| **Creative Market free goods** | Yes ("Desktop License allows you to create End Products for sale") | Yes, as end products; embedding limited | No | No | support.creativemarket.com article 115006136967 (search summary, weak) |

**Rule of thumb for this business:** only use OFL, Apache, UFL, ITF FFL, CC0, Fontfabric FFF, Typodermic desktop, or fonts whose licence text clearly says "commercial" plus print. Export flattened files. Keep a licence screenshot for every font.

---

## TASK C: Font mood / psychology

| Mood claim | What the evidence says | Source | Level |
|---|---|---|---|
| Serif = stable, traditional, mature, practical | Shaikh, Chaparro & Fox (2006): 561 people rated 20 fonts on 15 adjective pairs. Traits clustered by design family into 5 factors: **Serif, Sans-Serif, Modern, Monospace, Script/Funny**. Times New Roman traits: "stable, conformist, mature, practical". Georgia: "assertive, formal, practical". | Hazlett, Larson, Shaikh & Chaparro (2013), *Information Design Journal* 20(3) 207–219: https://www.microsoft.com/en-us/research/uploads/prod/2021/06/Hazlett-Larson-Shaikh-Chaparo-2013-two-studies-on-how-a-typeface-congruent-with-content-can-enhance-onscreen-communication.pdf | official (PDF opened) |
| Script = elegant, feminine, attractive | Monotype Corsiva traits (Shaikh et al. 2006): "feminine, elegant, and attractive". Brumberger (2003): typefaces grouped into **Elegance** (CounselorScript, Harrington), **Directness** (Arial, Garamond) and **Friendliness** (Bauhaus, Comic Sans). | Hazlett 2013 (above); Brumberger, *Technical Communication* 50(2) 206–223, summary via https://understandinggraphics.com/?p=459 | official (Hazlett) / weak (Brumberger summary) |
| Funny / novelty = its own personality group | Factor "Script/Funny" in Shaikh et al. 2006 | Hazlett 2013 (above) | official |
| Matching font to message works (key for posters) | Study 1: readers were faster with trait words in a *congruent* font. Study 2: a 700 ms glance at a page changed the perceived emotional tone, depending on the font. Shaikh (2007): a fitting font made e-commerce sites look more professional and believable. | Hazlett 2013 (above) | official |
| Appropriate font raises choice | Doyle & Bottomley (2004): brands were picked **about twice as often** in an appropriate font; in a field test, 75% picked chocolates in the appropriate font. Doyle & Bottomley (2006): fit depends on potency/activity match between font and product. | https://ideas.repec.org/a/eee/jbrese/v57y2004i8p873-880.html ; https://orca.cardiff.ac.uk/2577 (search summaries) | weak |
| Handwritten / rounded = friendly, casual | Mackiewicz (2005): "friendly" fonts show imperfection, simplicity, roundness like handwriting (Bradley Hand, Comic Sans). "Professional" fonts show perfection and balance (Times, Helvetica). Shaikh ClearType study: sans = more casual. | https://editingresearch.byu.edu/2021/05/21/choosing-a-font-can-be-a-daunting-task-but-with-the-proper-instruction-it-doesnt-have-to-be/ ; https://portfolio.erau.edu/en/publications/personality-of-cleartype-fonts/ (search summaries) | weak |
| Round = sweet/soft; angular = sharp/sour | Velasco, Woods, Hyndman & Spence (2015) "The Taste of Typeface", *i-Perception*: rounder fonts matched with "sweet"; angular fonts with bitter, salty, sour. | https://pmc.ncbi.nlm.nih.gov/articles/PMC4934647 (search summary) | weak |
| Soft fonts = positive feeling | Monotype × Neurons (2021, 400+ UK participants, 3 fonts): typeface changed positive response by up to 13%. "Softer and more recognizable" fonts gave more positive response; "pointy and sharp" fonts triggered negative emotion. Vendor study, small. | https://www.monotype.com/resources/can-fonts-affect-our-feelings ; Fast Company coverage (search summaries) | weak (vendor) |
| Condensed / bold = strong, motivational | **No direct study found.** Henderson, Giese & Cote (2004, *J. Marketing* 68(4)) list typeface dimensions including "weight" and "compressed", but I could not read their mood results. Google tag data: bold condensed families such as Bebas Neue score "Loud" and "Vintage". | Henderson et al. via search; families.csv (opened) | weak / official (tag data) |

### Google Fonts tags (github.com/google/fonts)
- File exists: `tags/all/families.csv` (opened; about 34,000 rows: `Family, axis-position, /Category/Tag, score`). The README in that folder says: "families.csv – expressive and typographic tags, **human assessed**; quant.csv – measured values, machine assessed; skip.csv – signals to machine assessors". Source: https://raw.githubusercontent.com/google/fonts/main/tags/all/README.md (official).
- Scores range up to 100 and rank a font *within* a tag. The GF guide says a percentage is assigned "to rank the font relative to others in the same category" using the "GF Tagger" tool. Source: https://googlefonts.github.io/gf-guide/tags.html (search summary only, weak; host blocked).
- **Categories (from the CSV):**
  - **Expressive** (mood): Active, Artistic, Awkward, Business, Calm, Childlike, Competent, Cute, Excited, Fancy, Futuristic, Happy, Innovative, Loud, Playful, Rugged, Sincere, Sophisticated, Stiff, Vintage.
  - **Script**: Formal, Handwritten, Informal, Upright Script.
  - **Theme**: Art Deco, Art Nouveau, Blackletter, Blobby, Brush (78), Distressed, Inline, Medieval, Pixel, Shaded, Stencil, Techno, Tuscan, Wacky, Woodtype.
  - **Seasonal**: Christmas, Halloween, Valentine's Day, Diwali, Holi, Hanukkah, Kwanzaa, Lunar New Year.
  - **Serif, Sans and Slab** sub-classes.
  - **Purpose**: Easy Reading, Learn To Write.
  - **Quality**, **Monospace** and **Special use** (internal or technical).
- **Top examples (scores from the CSV):**
  - Sophisticated: Pinyon Script 91, Monsieur La Doulaise 90.
  - Childlike: Short Stack 95, Comic Relief 94, Playpen Sans 94.
  - Happy: DynaPuff 94, Fontdiner Swanky 93, Henny Penny 92.
  - Rugged: Black Ops One 95, Rubik Dirt 92.
  - Vintage: Cinzel 92, Smokum 92.
  - Woodtype: Rye 100.
  - Brush: Chela One, Covered By Your Grace, Dokdo 100.
- **Use:** this CSV can map poster mood to font automatically, and every font in it is OFL/Apache/UFL.

---

## TASK D: Brush / watercolour / dry-brush fonts not on Google Fonts

I checked each font against the Google families list (families.csv) to confirm it is not a Google font. I read every licence below on Font Squirrel's licence page (3rd-party copy of the designer's licence, opened). The download page is the Font Squirrel font page; most link off-site to the designer.

| # | Font (style tags from Font Squirrel) | Download page | Licence (quoted) | Verdict |
|---|---|---|---|---|
| 1 | **Paint the Sky** (Display, **Dry Brush**) | https://www.fontsquirrel.com/fonts/Paint-the-Sky | "Free for Personal and Commercial Use… please email me the link to your final work… STRICTLY NO REDISTRIBUTION… NO RESALE" | OK. Email the designer as asked. |
| 2 | **Gesso** (Paint, Grunge, Distressed, caps) | https://www.fontsquirrel.com/fonts/Gesso | Flat-it: "freeware… use it on your commercial or non-commercial works for free" | OK |
| 3 | **Dirty Ego** (Grunge, Graffiti, Stencil) | https://www.fontsquirrel.com/fonts/dirty-ego | Misprinted Type: "freeware… commercial or non-commercial work for free"; credit optional | OK |
| 4 | **Nautilus Pompilius** (Brushed Script) | https://www.fontsquirrel.com/fonts/nautilus-pompilius | SIL OFL 1.1, Reserved Font Name "Nautilus Pompilius" | OK (safest) |
| 5 | **Florida Vibes** (script) | https://www.fontsquirrel.com/fonts/florida-vibe | SIL OFL 1.1, RFN "Florida Vibes" | OK (safest) |
| 6 | **Chinese Rocks** (Typodermic, rough dry brush) | https://www.fontsquirrel.com/fonts/Chinese-Rocks | Fontspring Desktop EULA 1.7: graphics "on… physical products"; no single-letter products | OK (desktop only) |
| 7 | **Octin Spraypaint** (Spray Paint, Distressed) | https://www.fontsquirrel.com/fonts/octin-spraypaint-free | Fontspring Desktop EULA 1.7 | OK (desktop only) |
| 8 | **Intro Rust** (Fontfabric; textured, condensed, inline) | https://www.fontsquirrel.com/fonts/Intro-Rust | Fontspring Desktop/Webfont EULA | OK |
| 9 | **Edo** (Brushed, Paint, Grunge, Handwritten) | https://www.fontsquirrel.com/fonts/edo | Vic Fieger: "freeware… used by anyone… You don't have to ask for my permission" | OK, but wording is informal |
| 10 | **Lilac Malaria** (Distressed, Rough) | https://www.fontsquirrel.com/fonts/Lilac-Malaria | Vic Fieger licence (as above) | OK, informal |
| 11 | **Tinet** (Brushed, Marker, Handwritten) | https://www.fontsquirrel.com/fonts/Tinet | "Anyone can use this font as they like, for commercial purposes and whatever." | OK |
| 12 | **Gong!** (Brushed, Graffiti, Handwritten) | https://www.fontsquirrel.com/fonts/Gong | Nyek!: "can be use for commercial and non-commercial purposes" (beta quality) | OK; check the glyphs |
| 13 | **AnuDaw** (Brush, Comic, Grunge) | https://www.fontsquirrel.com/fonts/AnuDaw | Nyek! licence (as above) | OK; check the glyphs |
| 14 | **Florante at Laura** (Brushed, Calligraphic) | https://www.fontsquirrel.com/fonts/Florante-at-Laura | Nyek! licence (as above) | OK; check the glyphs |
| 15 | **Hetilica** (Brushed, Fat, Handwritten) | https://www.fontsquirrel.com/fonts/Hetilica | Unlicensed originally; the author told Font Squirrel by email: "It IS available for commercial use." | Medium risk (second-hand statement) |
| 16 | **Nymphette** (Brushed, Calligraphic, Elegant) | https://www.fontsquirrel.com/fonts/nymphette | "Free for commercial and personal use." Credit optional | OK |
| 17 | **Belligerent Madness** (Brushed, Distressed, marker) | https://www.fontsquirrel.com/fonts/Belligerent-Madness | Font Monkey: "free for all commercial or non-commercial use" | OK |
| 18 | **District** (Distressed, Rough) | https://www.fontsquirrel.com/fonts/District | "free to use personal and commercial works… can't sell them directly" | OK |
| 19 | **Yozakura JP** (Brush, Japanese) | https://www.fontsquirrel.com/fonts/yozakura-jp | Kotonoha Works: "personal and commercial projects… without attribution. They may not be redistributed." | OK |
| 20 | **OrchideeLight** (Brushed, Calligraphic, Rough) | https://www.fontsquirrel.com/fonts/Orchidee | Floodfonts: "every kind of publication (electronic/print)… commercial or not" | OK |
| 21 | Komika Axis (Brushed, Casual, comic) | https://www.fontsquirrel.com/fonts/Komika-Axis | Apostrophic Labs: "can be used as they are in any context"; "Under no circumstance shall any… font design be sold" | Medium: the wording is ambiguous, so ask the author or skip |

**Do NOT use (found during the search):**
- **Brushstroke Plain, Scratch, Destroy, Copystruct:** no licence at all.
- **HVD Peace, HVD Poster:** personal use only.
- **Tkachenko Sketch 4F, Cartwheel:** MyFonts paid-licence text.
- **WC Mano Negra, WC Rhesus:** CC BY-ND; attribution is required.
- **Aquiline Two:** Manfred Klein licence asks for a donation if you make a profit.
- **Gist Rough:** Yellow Design Studio paid EULA.

**Watercolour:** I found **no** genuinely watercolour (colour-texture) font with a clear commercial licence on reachable sites. Most watercolour "fonts" are SVG/OpenType-colour products sold on Creative Fabrica or Creative Market. Safer option: set the text in an OFL brush font (e.g. Google "Brush" tag families, or Nautilus Pompilius), then apply your own watercolour texture as an image layer.
