#!/usr/bin/env bash
# K3H: sambungan run_k3h.sh + percubaan prompt khas setiap model (khas.py), CPU, 3 seed.
# Setiap enjin: prompt kad (jika belum dijana) dan prompt khas dijana berturut-turut SEBELUM cache model dibuang,
# supaya model dimuat turun sekali sahaja. Hasil: raw/k3h-cpu (prompt kad), raw/k3h-khas-cpu (prompt khas).
# Guna: TUNGGU_PID=<pid gen.py zturbo yang sedang jalan> bash run_k3h2.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
export GEN_DEVICE=cpu GEN_SEEDS=42,7,123 HF_HUB_DISABLE_XET=1
HUB="${HF_HOME:-$HOME/.cache/huggingface}/hub"
catat() { echo "{\"enjin\": \"$1\", \"rc\": $2, \"saat\": $3, \"peranti\": \"cpu\", \"prompt\": \"$4\", \"nota\": \"$5\", \"masa\": \"$(date +%Y-%m-%dT%H:%M:%S)\"}" >> "$6/enjin_masa.jsonl"; }
jalan() {  # jalan <enjin> <kad|khas> <nota>
  local e1=$1 v=$2 out t0 rc=1 cubaan
  if [ "$v" = khas ]; then out="$HERE/raw/k3h-khas-cpu"; else out="$HERE/raw/k3h-cpu"; fi
  mkdir -p "$out"; t0=$(date +%s)
  for cubaan in 1 2 3; do  # muat turun kadang-kadang terputus; cache disimpan antara cubaan
    if [ "$e1" = moss ]; then GEN_VARIAN=$v GEN_OUT="$out" python3 "$HERE/gen_moss.py" K3H
    else GEN_VARIAN=$v GEN_OUT="$out" python3 "$HERE/gen.py" "$e1" K3H; fi
    rc=$?; [ $rc -eq 0 ] && break
    echo "== $e1 $v gagal rc=$rc, cubaan $cubaan/3"; sleep 30
  done
  catat "$e1" $rc $(( $(date +%s) - t0 )) "$v" "$3" "$out"
  echo "== $e1 $v selesai rc=$rc"
}
buang() { rm -rf "$HUB"/models--* /tmp/moss-offload; }
if [ -n "${TUNGGU_PID:-}" ]; then  # zturbo prompt kad dimulakan oleh run_k3h.sh; tunggu ia siap
  t0=$(( $(date +%s) - $(ps -o etimes= -p "$TUNGGU_PID" 2>/dev/null || echo 0) ))
  while kill -0 "$TUNGGU_PID" 2>/dev/null; do sleep 10; done
  n=$(ls "$HERE/raw/k3h-cpu/zturbo/"*.png 2>/dev/null | wc -l); rc=1; [ "$n" -ge 3 ] && rc=0
  catat zturbo $rc $(( $(date +%s) - t0 )) kad "termasuk muat turun" "$HERE/raw/k3h-cpu"
fi
jalan zturbo khas "model dari cache"; buang
jalan ernie kad "termasuk muat turun"; jalan ernie khas "transformer dari cache; PE dimuat turun"; buang
jalan moss kad "termasuk muat turun"; jalan moss khas "model dari cache"; buang
jalan klein4b khas "termasuk muat turun"; buang
