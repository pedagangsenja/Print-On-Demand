#!/usr/bin/env bash
# Kitaran QC pusingan 1 (28 Nov 2026): FLUX 3 Klein + calon 3.15 'klein3_frasa_bentuk' (huruf lebar K51m, K54p), seed sama.
HERE="$(cd "$(dirname "$0")" && pwd)"
export GEN_OUT="$HERE/raw/v12-cpu-k50k54-p1" PEMBINA_UJI=klein3_frasa_bentuk
IDS="K51m K54p" GEN_SEEDS=42,7,123 bash "$HERE/run_v12.sh" klein3
echo "== P1B SIAP"
