#!/usr/bin/env bash
# Standard v1.2, langkah 4, larian 27 Nov 2026 petang (K9-K13): seed ikut laluan bagi setiap id.
# Laluan 2 (K14X K15E K16C): seed 42,7,123. Laluan 1 (K17Z K18U): seed 42,7. Satu enjin pada satu masa; cache enjin
# disimpan antara dua kumpulan seed dan dibuang selepas enjin itu (run_v12.sh). Peraturan langkau: run_v12.sh.
# Guna: GEN_OUT=<folder> bash run_v12b.sh [enjin...]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
export GEN_OUT="${GEN_OUT:-$HERE/raw/v12-cpu-k14}"
for e in ${@:-moss ernie klein3 zturbo klein4b}; do
  IDS="K14X K15E K16C" GEN_SEEDS=42,7,123 SIMPAN_CACHE=1 bash "$HERE/run_v12.sh" "$e"
  IDS="K17Z K18U" GEN_SEEDS=42,7 bash "$HERE/run_v12.sh" "$e"
done
