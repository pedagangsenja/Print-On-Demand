"""Ujian 12 model (fasa 1: 7 model laju) di CPU container. 3 teks x 3 gaya, seed 42, 768x1024.
Guna: python3 run.py <model> [id...]   model: klein4b | klein4b_ref | zturbo | ernie | schnell | chroma_flash
Model dimuat turun bila perlu (repo berlesen Apache 2.0 sahaja, disemak 24 Nov 2026) dan imej siap disimpan serta-merta.
MOSS guna gen_moss.py, Kandinsky guna gen_kandinsky.py."""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = Path(os.environ.get("POD_SCRATCH", "/tmp/claude-0/-home-user-Print-On-Demand/2d722db7-85d8-5f5a-9afd-4d1e293d123c/scratchpad"))
CLI = Path(os.environ.get("SD_CLI", "/home/user/Print-On-Demand/sdcpp/build/bin/sd-cli"))
M, OUT = S / "models", S / "out"
H = "https://huggingface.co"
FILES = {  # nama tempatan: repo/fail (semua Apache 2.0)
    "klein4b-Q8_0.gguf": "leejet/FLUX.2-klein-4B-GGUF/resolve/main/flux-2-klein-4b-Q8_0.gguf",
    "qwen3-4b-Q8_0.gguf": "Qwen/Qwen3-4B-GGUF/resolve/main/Qwen3-4B-Q8_0.gguf",
    "flux2-vae.safetensors": "black-forest-labs/FLUX.2-klein-4B/resolve/main/vae/diffusion_pytorch_model.safetensors",
    "zimage-turbo-Q8_0.gguf": "leejet/Z-Image-Turbo-GGUF/resolve/main/z_image_turbo-Q8_0.gguf",
    "qwen3-4b-instruct-2507-Q8_0.gguf": "unsloth/Qwen3-4B-Instruct-2507-GGUF/resolve/main/Qwen3-4B-Instruct-2507-Q8_0.gguf",
    "flux1-vae.safetensors": "Tongyi-MAI/Z-Image-Turbo/resolve/main/vae/diffusion_pytorch_model.safetensors",
    "ernie-turbo-Q8_0.gguf": "unsloth/ERNIE-Image-Turbo-GGUF/resolve/main/ernie-image-turbo-Q8_0.gguf",
    "ministral3-3b-Q8_0.gguf": "mistralai/Ministral-3-3B-Instruct-2512-GGUF/resolve/main/Ministral-3-3B-Instruct-2512-Q8_0.gguf",
    "flux1-schnell-Q8_0.gguf": "leejet/FLUX.1-schnell-gguf/resolve/main/flux1-schnell-q8_0.gguf",
    "clip_l.safetensors": "comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors",
    "t5xxl-Q8_0.gguf": "city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q8_0.gguf",
    "chroma1-flash-Q8_0.gguf": "silveroxides/Chroma1-Flash-GGUF/resolve/main/Chroma1-HD-Flash-Q8_0.gguf",
}
MODELS = {
    "klein4b": dict(args={"--diffusion-model": "klein4b-Q8_0.gguf", "--llm": "qwen3-4b-Q8_0.gguf", "--vae": "flux2-vae.safetensors"}, steps=4, cfg=1.0),
    "klein4b_ref": dict(args={"--diffusion-model": "klein4b-Q8_0.gguf", "--llm": "qwen3-4b-Q8_0.gguf", "--vae": "flux2-vae.safetensors"}, steps=4, cfg=1.0, ref=True),
    "zturbo": dict(args={"--diffusion-model": "zimage-turbo-Q8_0.gguf", "--llm": "qwen3-4b-instruct-2507-Q8_0.gguf", "--vae": "flux1-vae.safetensors"}, steps=8, cfg=1.0),
    "ernie": dict(args={"--diffusion-model": "ernie-turbo-Q8_0.gguf", "--llm": "ministral3-3b-Q8_0.gguf", "--vae": "flux2-vae.safetensors"}, steps=8, cfg=1.0),
    "schnell": dict(args={"--diffusion-model": "flux1-schnell-Q8_0.gguf", "--clip_l": "clip_l.safetensors", "--t5xxl": "t5xxl-Q8_0.gguf", "--vae": "flux1-vae.safetensors"},
                    steps=4, cfg=1.0, extra=["--sampling-method", "euler"]),
    "chroma_flash": dict(args={"--diffusion-model": "chroma1-flash-Q8_0.gguf", "--t5xxl": "t5xxl-Q8_0.gguf", "--vae": "flux1-vae.safetensors"},
                         steps=10, cfg=1.0, extra=["--sampling-method", "euler", "--model-args", "chroma_use_dit_mask=false"]),
}
SEED = 42


def fetch(name):
    dst = M / name
    if dst.exists() and dst.stat().st_size > 0:
        return dst
    M.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(dst.suffix + ".part")
    t0 = time.time()
    subprocess.run(["curl", "-sfL", "--retry", "4", "-o", str(tmp), f"{H}/{FILES[name]}"], check=True)
    tmp.rename(dst)
    print("muat turun", name, round(dst.stat().st_size / 1e9, 2), "GB", round(time.time() - t0), "s", flush=True)
    return dst


def main():
    name, only = sys.argv[1], set(sys.argv[2:])
    c = MODELS[name]
    paths = {k: fetch(v) for k, v in c["args"].items()}
    out = OUT / name
    out.mkdir(parents=True, exist_ok=True)
    log = out / "times.json"
    times = json.loads(log.read_text()) if log.exists() else {}
    for p in json.loads((HERE / "prompts.json").read_text()):
        if only and p["id"] not in only:
            continue
        png = out / f"{p['id']}.png"
        if png.exists():
            continue
        prompt = p["prompt_ref"] if c.get("ref") else p["prompt"]
        cmd = [str(CLI)] + [x for k, v in paths.items() for x in (k, str(v))]
        cmd += ["-p", prompt, "--cfg-scale", str(c["cfg"]), "--steps", str(c["steps"]), "-W", str(p["w"]), "-H", str(p["h"]),
                "-s", str(SEED), "-t", str(os.cpu_count() or 4), "-o", str(png)] + c.get("extra", [])
        if c.get("ref"):
            cmd += ["-r", str(HERE / p["ref"])]
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True)
        dt = round(time.time() - t0, 1)
        (out / f"{p['id']}.log").write_text(r.stdout[-3000:] + "\n" + r.stderr[-3000:])
        times[p["id"]] = {"seconds": dt, "ok": png.exists(), "code": r.returncode}
        log.write_text(json.dumps(times, indent=1))
        print(name, p["id"], dt, "s", "OK" if png.exists() else f"GAGAL {r.returncode}", flush=True)


if __name__ == "__main__":
    main()
