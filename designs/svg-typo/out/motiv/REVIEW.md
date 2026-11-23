# Motivational posters - review (30/30 pass)
Model: FLUX.2 [klein] 4B (Apache 2.0), CPU, 864x1152 (3:4 -> 18x24 in). 30 quotes x 4 seeds + 15 restyled retries x 4.
Picks: `picks.json`. Final: `final/<id>.png` + `final/<id>.svg` (potrace). Sheet: `FINAL_30.png`. Quotes: `FINAL_30.txt`.

Pass as generated (12): limit, tired, try, excuse, fall, wish, dayone, energy, climb (retry), champion, comeback, chase, idols (retry), keepgoing (retry).
Repaired with glyph surgery (`ai/surgery.py`):
- dream: HUMBILE->HUMBLE, word spaces DREAM BIG / NEVER GIVE UP
- steps: RESULLS->RESULTS (T from STEPS)
- push: ESLE->ELSE + space
- comfort: THIINGS->THINGS
- silence (retry): SILENIE->SILENCE (C from SUCCESS), bad R in HARD replaced
- doubt: FABLLRE->FAILURE (I, U from KILLS/DOUBT), "ever wil"->"ever will" (script l copied)
- pain: TIHE->THE, STRETNGH->STRENGTH
- purpose: BEAD->BED
- future: WHHAT->WHAT
- futureself (retry): SOMETHIIING->SOMETHING, FUTUR SELE->FUTURE SELF
- progress: PROFRESS->PROGRESS (G from other seed)
- doubting: stray mark removed
- harder (retry, new quote): UCKIER->LUCKIER
- goal (retry): stray mark removed
- success (retry): SUCESS->SUCCESS, DOESN'TT->DOESN'T
- winners (retry, new quote): script g->q in "quitters"
Quote changes: harder -> "The harder you work, the luckier you get"; winners -> "Winners never quit and quitters never win" (originals misspelled in every seed).
