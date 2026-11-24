"""Giliran ujian versi diffusers (lebih laju di CPU ini). Model seterusnya dimuat turun semasa model semasa menjana;
fail yang tidak diperlukan lagi dipadam. Boleh disambung semula. Guna: python3 run_all2.py [model_mula]"""
import os, shutil, subprocess, sys, threading, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = Path(os.environ.get("POD_SCRATCH", "/tmp/claude-0/-home-user-Print-On-Demand/2d722db7-85d8-5f5a-9afd-4d1e293d123c/scratchpad"))
M = S / "models"
os.environ.setdefault("HF_HOME", str(S / "hf"))
os.environ.setdefault("MOSS_OFFLOAD", str(S / "moss-offload"))
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
H = "https://huggingface.co"
ORDER = ["klein4b", "klein4b_ref", "zturbo", "ernie", "schnell", "chroma_flash", "kandinsky", "moss"]
GGUF = {"zturbo": ("zimage-turbo-Q8_0.gguf", "leejet/Z-Image-Turbo-GGUF/resolve/main/z_image_turbo-Q8_0.gguf"),
        "ernie": ("ernie-turbo-Q8_0.gguf", "unsloth/ERNIE-Image-Turbo-GGUF/resolve/main/ernie-image-turbo-Q8_0.gguf"),
        "schnell": ("flux1-schnell-city96-Q8_0.gguf", "city96/FLUX.1-schnell-gguf/resolve/main/flux1-schnell-Q8_0.gguf"),
        "chroma_flash": ("chroma1-flash-Q8_0.gguf", "silveroxides/Chroma1-Flash-GGUF/resolve/main/Chroma1-HD-Flash-Q8_0.gguf")}
REPOS = {  # (repo, allow_patterns): pengekod teks, tokenizer, VAE dan config sahaja
    "zturbo": [("Tongyi-MAI/Z-Image-Turbo", ["*.json", "text_encoder/*", "tokenizer/*", "vae/*", "scheduler/*", "transformer/*.json"])],
    "ernie": [("baidu/ERNIE-Image-Turbo", ["*.json", "text_encoder/*", "tokenizer/*", "vae/*", "scheduler/*", "transformer/*.json"])],
    "schnell": [("unsloth/FLUX.1-schnell", ["*.json", "text_encoder/*", "text_encoder_2/*", "tokenizer/*", "tokenizer_2/*", "vae/*", "scheduler/*", "transformer/*.json"])],
    "chroma_flash": [("lodestones/Chroma1-Flash", ["*.json", "tokenizer/*", "vae/*", "scheduler/*", "transformer/*.json", "text_encoder/*.json"])],
    "kandinsky": [("kandinsky-community/kandinsky-2-2-decoder", None), ("kandinsky-community/kandinsky-2-2-prior", None)],
    "moss": [("OpenMOSS-Team/MOSS-Image-SFT", None), ("lodestones/MOSS-Image-SFT-8-steps-dmd", None)],
}
FREE_AFTER = {"klein4b_ref": ["klein4b-Q8_0.gguf", ("black-forest-labs/FLUX.2-klein-4B",)],
              "zturbo": ["zimage-turbo-Q8_0.gguf", ("Tongyi-MAI/Z-Image-Turbo",)],
              "ernie": ["ernie-turbo-Q8_0.gguf", ("baidu/ERNIE-Image-Turbo",)],
              "schnell": ["flux1-schnell-city96-Q8_0.gguf"],
              "chroma_flash": ["chroma1-flash-Q8_0.gguf", ("unsloth/FLUX.1-schnell",), ("lodestones/Chroma1-Flash",)],
              "kandinsky": [("kandinsky-community/kandinsky-2-2-decoder",), ("kandinsky-community/kandinsky-2-2-prior",)]}


def fetch(local, path):
    dst = M / local
    if dst.exists():
        return
    tmp = M / (local + ".part")
    t0 = time.time()
    subprocess.run(["curl", "-sfL", "--retry", "4", "-o", str(tmp), f"{H}/{path}"], check=True)
    tmp.rename(dst)
    print("muat turun", local, round(dst.stat().st_size / 1e9, 2), "GB", round(time.time() - t0), "s", flush=True)


def prefetch(name):
    try:
        from huggingface_hub import snapshot_download
        if name in GGUF:
            fetch(*GGUF[name])
        for repo, pat in REPOS.get(name, []):
            t0 = time.time(); snapshot_download(repo, allow_patterns=pat); print("muat turun", repo, round(time.time() - t0), "s", flush=True)
    except Exception as e:  # dicuba lagi semasa giliran model itu
        print("prefetch gagal", name, e, flush=True)


def gen(name):
    if name == "kandinsky":
        cmd = [sys.executable, str(HERE / "gen_kandinsky.py")]
    elif name == "moss":
        cmd = [sys.executable, str(HERE / "gen_moss.py"), str(HERE / "prompts.json"), str(S / "out" / "moss"), "--seeds", "42"]
    else:
        cmd = [sys.executable, str(HERE / "gen_diffusers.py"), name]
    t0 = time.time()
    r = subprocess.run(cmd)
    print("SIAP", name, "kod", r.returncode, round((time.time() - t0) / 60, 1), "min", flush=True)


def free(name):
    for x in FREE_AFTER.get(name, []):
        if isinstance(x, tuple):
            shutil.rmtree(S / "hf" / "hub" / ("models--" + x[0].replace("/", "--")), ignore_errors=True)
        else:
            (M / x).unlink(missing_ok=True)


def main():
    order = ORDER[ORDER.index(sys.argv[1]):] if len(sys.argv) > 1 else ORDER
    for i, name in enumerate(order):
        nxt = order[i + 1] if i + 1 < len(order) else None
        th = threading.Thread(target=prefetch, args=(nxt,)) if nxt else None
        if th:
            th.start()
        prefetch(name)
        gen(name)
        free(name)
        if th:
            th.join()
    print("SEMUA SIAP", flush=True)


if __name__ == "__main__":
    main()
