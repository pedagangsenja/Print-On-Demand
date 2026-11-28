#!/bin/bash
# Kitaran 3.15 (28 Nov 2026, keputusan pengguna): uji 4 calon ubahan prompt daripada larian K14-K18.
# Satu calon setiap model; kad, ayat dan seed sama dengan larian asal (raw/v12-cpu-k14). Hasil: raw/v12-cpu-k14-uji/<model>.
HERE="$(cd "$(dirname "$0")" && pwd)"
export GEN_OUT="$HERE/raw/v12-cpu-k14-uji"
PEMBINA_UJI=zturbo_had_positif IDS="K16C" GEN_SEEDS=42,7,123 SIMPAN_CACHE=1 bash "$HERE/run_v12.sh" zturbo
PEMBINA_UJI=zturbo_had_positif IDS="K17Z" GEN_SEEDS=42,7 bash "$HERE/run_v12.sh" zturbo
PEMBINA_UJI=ernie_hiasan_tepat IDS="K14X" GEN_SEEDS=42,7,123 bash "$HERE/run_v12.sh" ernie
PEMBINA_UJI=klein3_hiasan_kedudukan IDS="K14X" GEN_SEEDS=42,7,123 bash "$HERE/run_v12.sh" klein3
PEMBINA_UJI=klein4b_frasa_bentuk IDS="K15E K16C" GEN_SEEDS=42,7,123 bash "$HERE/run_v12.sh" klein4b
echo "== uji selesai"
