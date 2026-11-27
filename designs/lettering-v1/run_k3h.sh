#!/usr/bin/env bash
# Standard Lettering v1, langkah 4: kad K3 v1.2 x ayat H ("Patience Builds What Hurry Breaks"), laluan 2 = 3 seed.
# 4 enjin di CPU (tanpa ZeroGPU), satu demi satu; cache model dibuang selepas setiap enjin (cakera terhad).
# Guna: bash run_k3h.sh [klein4b zturbo ernie moss]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
export GEN_DEVICE=cpu GEN_SEEDS=42,7,123 GEN_OUT="$HERE/raw/k3h-cpu" HF_HUB_DISABLE_XET=1
mkdir -p "$GEN_OUT"
HUB="${HF_HOME:-$HOME/.cache/huggingface}/hub"
for e in "${@:-klein4b zturbo ernie moss}"; do
  for e1 in $e; do
    t0=$(date +%s); rc=1
    for cubaan in 1 2 3; do  # muat turun kadang-kadang terputus; cache disimpan antara cubaan
      if [ "$e1" = moss ]; then python3 "$HERE/gen_moss.py" K3H; else python3 "$HERE/gen.py" "$e1" K3H; fi
      rc=$?; [ $rc -eq 0 ] && break
      echo "== $e1 gagal rc=$rc, cubaan $cubaan/3"; sleep 30
    done
    sec=$(( $(date +%s) - t0 ))
    echo "{\"enjin\": \"$e1\", \"rc\": $rc, \"saat\": $sec, \"peranti\": \"cpu\", \"masa\": \"$(date +%Y-%m-%dT%H:%M:%S)\"}" >> "$GEN_OUT/enjin_masa.jsonl"
    echo "== $e1 selesai rc=$rc $sec s"
    rm -rf "$HUB"/models--* /tmp/moss-offload
  done
done
