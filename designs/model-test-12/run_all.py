"""Jalankan semua model fasa 1 mengikut giliran. Fail model seterusnya dimuat turun semasa model semasa menjana,
dan fail yang tidak diperlukan lagi dipadam (disk terhad). Boleh disambung semula: imej sedia ada dilangkau.
Guna: python3 run_all.py [model_mula]"""
import os, shutil, subprocess, sys, threading, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run  # noqa: E402

S = run.S
os.environ.setdefault("HF_HOME", str(S / "hf"))
os.environ.setdefault("MOSS_OFFLOAD", str(S / "moss-offload"))
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
PY = sys.executable
ORDER = ["klein4b", "klein4b_ref", "zturbo", "ernie", "schnell", "chroma_flash", "kandinsky", "moss"]
FREE_AFTER = {
    "klein4b_ref": ["klein4b-Q8_0.gguf", "qwen3-4b-Q8_0.gguf"],
    "zturbo": ["zimage-turbo-Q8_0.gguf", "qwen3-4b-instruct-2507-Q8_0.gguf"],
    "ernie": ["ernie-turbo-Q8_0.gguf", "ministral3-3b-Q8_0.gguf", "flux2-vae.safetensors"],
    "schnell": ["flux1-schnell-Q8_0.gguf", "clip_l.safetensors"],
    "chroma_flash": ["chroma1-flash-Q8_0.gguf", "t5xxl-Q8_0.gguf", "flux1-vae.safetensors"],
}
HF_REPOS = {"kandinsky": ["kandinsky-community/kandinsky-2-2-decoder", "kandinsky-community/kandinsky-2-2-prior"],
            "moss": ["OpenMOSS-Team/MOSS-Image-SFT", "lodestones/MOSS-Image-SFT-8-steps-dmd"]}


def prefetch(name):
    try:
        if name in run.MODELS:
            for f in run.MODELS[name]["args"].values():
                run.fetch(f)
        else:
            from huggingface_hub import snapshot_download
            for r in HF_REPOS[name]:
                t0 = time.time(); snapshot_download(r); print("muat turun", r, round(time.time() - t0), "s", flush=True)
    except Exception as e:  # cuba lagi semasa giliran model itu
        print("prefetch gagal", name, e, flush=True)


def gen(name):
    if name in run.MODELS:
        cmd = [PY, str(HERE / "run.py"), name]
    elif name == "kandinsky":
        cmd = [PY, str(HERE / "gen_kandinsky.py")]
    else:
        cmd = [PY, str(HERE / "gen_moss.py"), str(HERE / "prompts.json"), str(S / "out" / "moss"), "--seeds", "42"]
    t0 = time.time()
    r = subprocess.run(cmd)
    print("SIAP", name, "kod", r.returncode, round((time.time() - t0) / 60, 1), "min", flush=True)


def main():
    order = ORDER[ORDER.index(sys.argv[1]):] if len(sys.argv) > 1 else ORDER
    prefetch(order[0])
    for i, name in enumerate(order):
        nxt = order[i + 1] if i + 1 < len(order) else None
        th = threading.Thread(target=prefetch, args=(nxt,)) if nxt else None
        if th:
            th.start()
        gen(name)
        for f in FREE_AFTER.get(name, []):
            (run.M / f).unlink(missing_ok=True)
        if name in HF_REPOS:
            for r in HF_REPOS[name]:
                shutil.rmtree(S / "hf" / "hub" / ("models--" + r.replace("/", "--")), ignore_errors=True)
        if th:
            th.join()
    print("SEMUA SIAP", flush=True)


if __name__ == "__main__":
    main()
