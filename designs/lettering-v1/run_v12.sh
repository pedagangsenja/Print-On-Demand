#!/usr/bin/env bash
# Standard v1.2: ujian pembina ikut model (pembina.py) di CPU, 3 seed. K3H = ulang contoh tulisan tangan (khas.py);
# K6P = kad lain + ayat pendek. Setiap enjin dimuat sekali untuk semua id, kemudian cache dibuang.
# Guna: bash run_v12.sh [enjin...]   (lalai: klein4b zturbo moss ernie)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
export GEN_DEVICE=cpu GEN_SEEDS=42,7,123 HF_HUB_DISABLE_XET=1 GEN_VARIAN=pembina GEN_OUT="$HERE/raw/v12-pembina-cpu"
IDS="${IDS:-K3H K6P}"
HUB="${HF_HOME:-$HOME/.cache/huggingface}/hub"
mkdir -p "$GEN_OUT"
for e in "${@:-klein4b zturbo moss ernie}"; do for e1 in $e; do
  t0=$(date +%s); rc=1
  for cubaan in 1 2 3; do
    if [ "$e1" = moss ]; then python3 "$HERE/gen_moss.py" $IDS; else python3 "$HERE/gen.py" "$e1" $IDS; fi
    rc=$?; [ $rc -eq 0 ] && break
    echo "== $e1 gagal rc=$rc, cubaan $cubaan/3"; sleep 30
  done
  echo "{\"enjin\": \"$e1\", \"rc\": $rc, \"saat\": $(( $(date +%s) - t0 )), \"peranti\": \"cpu\", \"prompt\": \"pembina\", \"id\": \"$IDS\", \"nota\": \"termasuk muat turun\", \"masa\": \"$(date +%Y-%m-%dT%H:%M:%S)\"}" >> "$GEN_OUT/enjin_masa.jsonl"
  echo "== $e1 selesai rc=$rc"
  rm -rf "$HUB"/models--* /tmp/moss-offload
done; done
