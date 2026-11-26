#!/usr/bin/env bash
# Standard v1.2, langkah 4: jana ikut pembina (pembina.py) di CPU, satu enjin pada satu masa, dengan PERATURAN LANGKAU.
# Guna: IDS="K3H" GEN_OUT=<folder hasil> bash run_v12.sh [enjin...]
#   Lalai dan turutan enjin: moss ernie zturbo klein4b (turutan lulus QC, AI Image Test 2). Seed: GEN_SEEDS (lalai 42,7,123).
# Peraturan langkau (standard, langkah 4): enjin DILANGKAU dan enjin seterusnya terus dijalankan apabila
#   (a) masa enjin melebihi HAD_SAAT (lalai: 20 minit muat turun + 13 minit bagi setiap imej), atau
#   (b) enjin gagal 3 cubaan berturut-turut (ralat muat turun, RAM, semakan 3.11).
# Setiap langkau direkod dalam <GEN_OUT>/langkau.jsonl dan dicetak di hujung; Claude melaporkannya dalam chat.
# Cache model dibuang selepas setiap enjin (SIMPAN_CACHE=1 untuk menyimpannya).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
export GEN_DEVICE="${GEN_DEVICE:-cpu}" GEN_SEEDS="${GEN_SEEDS:-42,7,123}" HF_HUB_DISABLE_XET=1 GEN_VARIAN=pembina
export GEN_OUT="${GEN_OUT:-$HERE/raw/v12-cpu}"
IDS="${IDS:?nyatakan id, contoh IDS=\"K3H\"}"
HUB="${HF_HOME:-$HOME/.cache/huggingface}/hub"
NIMEJ=$(( $(echo $IDS | wc -w) * $(echo "$GEN_SEEDS" | tr ',' ' ' | wc -w) ))
HAD_SAAT="${HAD_SAAT:-$(( 1200 + 780 * NIMEJ ))}"
mkdir -p "$GEN_OUT"
rekod() { echo "{\"enjin\": \"$1\", \"rc\": $2, \"saat\": $3, \"peranti\": \"$GEN_DEVICE\", \"prompt\": \"pembina\", \"id\": \"$IDS\", \"masa\": \"$(date +%Y-%m-%dT%H:%M:%S)\"}" >> "$GEN_OUT/enjin_masa.jsonl"; }
langkau() { echo "{\"enjin\": \"$1\", \"sebab\": \"$2\", \"saat\": $3, \"had_saat\": $HAD_SAAT, \"id\": \"$IDS\", \"masa\": \"$(date +%Y-%m-%dT%H:%M:%S)\"}" >> "$GEN_OUT/langkau.jsonl"; echo "== LANGKAU $1: $2"; }
for e1 in ${@:-moss ernie zturbo klein4b}; do
  t0=$(date +%s); rc=1
  for cubaan in 1 2 3; do
    baki=$(( HAD_SAAT - ($(date +%s) - t0) )); [ $baki -le 0 ] && { rc=124; break; }
    if [ -n "${PERINTAH_UJI:-}" ]; then timeout "$baki" bash -c "$PERINTAH_UJI" _ "$e1"   # ujian skrip ini sahaja
    elif [ "$e1" = moss ]; then timeout "$baki" python3 "$HERE/gen_moss.py" $IDS
    elif [ "$e1" = klein3 ]; then timeout "$baki" python3 "$HERE/gen_flux3.py" $IDS
    else timeout "$baki" python3 "$HERE/gen.py" "$e1" $IDS; fi
    rc=$?; [ $rc -eq 0 ] && break; [ $rc -eq 124 ] && break
    echo "== $e1 gagal rc=$rc, cubaan $cubaan/3"; sleep "${JEDA:-30}"
  done
  saat=$(( $(date +%s) - t0 )); rekod "$e1" $rc $saat
  if [ $rc -eq 124 ]; then langkau "$e1" "melebihi had masa" $saat
  elif [ $rc -ne 0 ]; then langkau "$e1" "gagal 3 cubaan (rc=$rc)" $saat
  else echo "== $e1 selesai, $saat s"; fi
  [ -n "${SIMPAN_CACHE:-}" ] || [ -n "${PERINTAH_UJI:-}" ] || rm -rf "$HUB"/models--* /tmp/moss-offload
done
if [ -f "$GEN_OUT/langkau.jsonl" ]; then echo "== RINGKASAN LANGKAU"; cat "$GEN_OUT/langkau.jsonl"; else echo "== tiada enjin dilangkau"; fi
