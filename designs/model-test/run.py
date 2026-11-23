"""Jana 10 prompt ujian dengan satu model melalui stable-diffusion.cpp (CPU). Guna: python3 run.py <model> [id...]"""
import json, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = Path("/tmp/claude-0/-home-user-Print-On-Demand/9b462b96-1f96-5add-a3d4-6d6636007ee7/scratchpad")
CLI = S / "sdcpp/build/bin/sd-cli"
M = S / "models"
MODELS = {
    "klein4b": dict(diffusion=M / "klein4b-Q8_0.gguf", llm=M / "qwen3-4b-Q8_0.gguf", vae=M / "flux2-vae.safetensors", steps=4),
    "zimage": dict(diffusion=M / "zimage-turbo-Q8_0.gguf", llm=M / "qwen3-4b-instruct-Q8_0.gguf", vae=M / "flux1-ae.safetensors", steps=8),
    "ernie": dict(diffusion=M / "ernie-turbo-Q8_0.gguf", llm=M / "ministral3-3b-Q8_0.gguf", vae=M / "flux2-vae.safetensors", steps=8),
}
SEED = 42


def main():
    name, only = sys.argv[1], set(sys.argv[2:])
    cfg = MODELS[name]
    out = HERE / "out" / name
    out.mkdir(parents=True, exist_ok=True)
    log = out / "times.json"
    times = json.loads(log.read_text()) if log.exists() else {}
    for p in json.loads((HERE / "prompts.json").read_text()):
        if only and p["id"] not in only:
            continue
        png = out / f"{p['id']}.png"
        if png.exists():
            continue
        cmd = [str(CLI), "--diffusion-model", str(cfg["diffusion"]), "--llm", str(cfg["llm"]), "--vae", str(cfg["vae"]),
               "-p", p["prompt"], "--cfg-scale", "1.0", "--steps", str(cfg["steps"]), "-W", str(p["w"]), "-H", str(p["h"]),
               "-s", str(SEED), "-t", "4", "-o", str(png)]
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True)
        dt = round(time.time() - t0, 1)
        (out / f"{p['id']}.log").write_text(r.stdout[-4000:] + "\n" + r.stderr[-4000:])
        times[p["id"]] = {"seconds": dt, "ok": png.exists(), "code": r.returncode}
        log.write_text(json.dumps(times, indent=1))
        print(name, p["id"], dt, "s", "OK" if png.exists() else f"FAIL {r.returncode}", flush=True)


if __name__ == "__main__":
    main()
