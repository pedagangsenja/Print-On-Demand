#!/usr/bin/env bash
# 27 Nov 2026 (arahan pengguna "ya"): bagi setiap enjin, (1) uji ubahan calon belajar.py (3.15) pada kad, ayat dan seed
# cacat asal -> raw/v12-cpu-uji; (2) seed 7 dan 123 bagi 6 gaya upload -> raw/v12-cpu-ref6. Cache dibuang selepas (2).
set -u
H="$(cd "$(dirname "$0")" && pwd)"; U="$H/raw/v12-cpu-uji"; R="$H/raw/v12-cpu-ref6"; IDS6="K9A K10B K11C K2E K12F K4Q"
uji() { SIMPAN_CACHE=1 PEMBINA_UJI="$1" IDS="$2" GEN_SEEDS="$3" GEN_OUT="$U" bash "$H/run_v12.sh" "$4"; }
uji klein4b_hiasan_kedudukan "K3K" 42,7,123 klein4b
IDS="$IDS6" GEN_SEEDS=42,7,123 GEN_OUT="$R" bash "$H/run_v12.sh" klein4b
uji zturbo_had_positif "K7M K8G" 42,7 zturbo
IDS="$IDS6" GEN_SEEDS=42,7,123 GEN_OUT="$R" bash "$H/run_v12.sh" zturbo
uji ernie_had_positif "K11C" 42 ernie
uji ernie_had_positif "K3K" 7 ernie
IDS="$IDS6" GEN_SEEDS=42,7,123 GEN_OUT="$R" bash "$H/run_v12.sh" ernie
IDS="$IDS6" GEN_SEEDS=42,7,123 GEN_OUT="$R" bash "$H/run_v12.sh" moss
IDS="$IDS6" GEN_SEEDS=42,7,123 GEN_OUT="$R" bash "$H/run_v12.sh" klein3
echo "== SEMUA SIAP"
