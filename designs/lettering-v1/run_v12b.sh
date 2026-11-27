#!/usr/bin/env bash
# Larian v1.2 kedua (27 Nov 2026): 5 kad baharu K9-K13, CPU, hitam putih. Laluan 2 = seed 42,7,123; laluan 1 = 42,7.
# Satu enjin pada satu masa; cache disimpan antara dua panggilan run_v12.sh bagi enjin yang sama, kemudian dibuang.
HERE="$(cd "$(dirname "$0")" && pwd)"
export GEN_OUT="${GEN_OUT:-$HERE/raw/v12b-cpu}"
HUB="${HF_HOME:-$HOME/.cache/huggingface}/hub"
for e in ${@:-moss ernie klein3 zturbo klein4b}; do
  SIMPAN_CACHE=1 IDS="K9Q K11R K13V" GEN_SEEDS=42,7,123 bash "$HERE/run_v12.sh" "$e"
  SIMPAN_CACHE=1 IDS="K10F K12O" GEN_SEEDS=42,7 bash "$HERE/run_v12.sh" "$e"
  rm -rf "$HUB"/models--* /tmp/moss-offload
done
echo "== SEMUA ENJIN SELESAI"
