#!/usr/bin/env bash
# Larian 27 Nov 2026: lima gambar upload (K9-K13), CPU, hitam putih, standard v1.2. Seed ikut laluan:
# laluan 1 (K50k K51m K52A K53n) = 42,7; laluan 2 (K54p) = 42,7,123. Satu muat turun bagi setiap enjin.
HERE="$(cd "$(dirname "$0")" && pwd)"
export GEN_OUT="$HERE/raw/v12-cpu-k50k54"
for e in ${@:-moss ernie klein3 zturbo klein4b}; do
  SIMPAN_CACHE=1 IDS="K50k K51m K52A K53n" GEN_SEEDS=42,7 bash "$HERE/run_v12.sh" $e
  IDS="K54p" GEN_SEEDS=42,7,123 bash "$HERE/run_v12.sh" $e
done
echo "== SEMUA SIAP"
