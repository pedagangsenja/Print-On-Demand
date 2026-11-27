#!/usr/bin/env bash
# Kitaran QC pusingan 1 (27 Nov 2026): ERNIE + calon 3.15 'ernie_hiasan_tepat' (bingkai putih K11A, K13S), seed sama.
HERE="$(cd "$(dirname "$0")" && pwd)"
export GEN_OUT="$HERE/raw/v12-cpu-k9k13-p1" PEMBINA_UJI=ernie_hiasan_tepat
IDS="K11A K13S" GEN_SEEDS=42,7,123 bash "$HERE/run_v12.sh" ernie
echo "== P1 SIAP"
