"""Ujian K6: 6 enjin x 3 ayat (P, D, L) x 2 seed, di CPU atau GPU (GEN_DEVICE). Satu enjin pada satu masa;
cache model dibuang selepas setiap enjin (cakera terhad). Masa keseluruhan setiap enjin (muat turun + muat + jana)
direkod dalam <GEN_OUT>/enjin_masa.jsonl.
Guna: GEN_DEVICE=cpu GEN_OUT=out_cpu python3 run_k6.py [enjin...]
"""
import json, os, shutil, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
IDS = ["K6P", "K6D", "K6L"]
ENJIN = sys.argv[1:] or ["klein4b", "zturbo", "ernie", "schnell", "chroma_flash", "moss"]
OUT = Path(os.environ.get("GEN_OUT", str(HERE / "out")))
HUB = Path(os.environ.get("HF_HOME", str(Path.home() / ".cache/huggingface"))) / "hub"
KEEP = {"schnell": {"models--unsloth--FLUX.1-schnell"}}  # T5 dikongsi dengan Chroma

OUT.mkdir(parents=True, exist_ok=True)
for e in ENJIN:
    t0 = time.time()
    script = "gen_moss.py" if e == "moss" else "gen.py"
    cmd = [sys.executable, str(HERE / script)] + ([] if e == "moss" else [e]) + IDS
    rc = subprocess.run(cmd).returncode
    sec = round(time.time() - t0)
    with open(OUT / "enjin_masa.jsonl", "a") as f:
        f.write(json.dumps(dict(enjin=e, rc=rc, saat=sec, peranti=os.environ.get("GEN_DEVICE", "cpu"),
                                masa=time.strftime("%Y-%m-%dT%H:%M:%S"))) + "\n")
    print(f"== {e} selesai rc={rc} {sec} s", flush=True)
    for d in HUB.glob("models--*"):
        if d.name not in KEEP.get(e, set()):
            shutil.rmtree(d, ignore_errors=True)
