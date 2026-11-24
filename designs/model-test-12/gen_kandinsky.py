"""Kandinsky 2.2 (Apache 2.0) di CPU melalui diffusers. Guna: python3 gen_kandinsky.py [id...]"""
import json, os, sys, time
from pathlib import Path

import torch
from diffusers import AutoPipelineForText2Image

HERE = Path(__file__).resolve().parent
S = Path(os.environ.get("POD_SCRATCH", "/tmp/claude-0/-home-user-Print-On-Demand/2d722db7-85d8-5f5a-9afd-4d1e293d123c/scratchpad"))
OUT = S / "out" / "kandinsky"
SEED, STEPS, GUIDE = 42, 50, 4.0


def main():
    only = set(sys.argv[1:])
    torch.set_num_threads(os.cpu_count() or 4)
    OUT.mkdir(parents=True, exist_ok=True)
    log = OUT / "times.json"
    times = json.loads(log.read_text()) if log.exists() else {}
    prompts = [p for p in json.loads((HERE / "prompts.json").read_text())
               if (not only or p["id"] in only) and not (OUT / f"{p['id']}.png").exists()]
    if not prompts:
        return
    pipe = AutoPipelineForText2Image.from_pretrained("kandinsky-community/kandinsky-2-2-decoder", torch_dtype=torch.float32)
    for p in prompts:
        t0 = time.time()
        with torch.inference_mode():
            img = pipe(prompt=p["prompt"][:900], height=p["h"], width=p["w"], num_inference_steps=STEPS,
                       guidance_scale=GUIDE, generator=torch.Generator("cpu").manual_seed(SEED)).images[0]
        img.save(OUT / f"{p['id']}.png")
        times[p["id"]] = {"seconds": round(time.time() - t0, 1), "ok": True}
        log.write_text(json.dumps(times, indent=1))
        print("kandinsky", p["id"], times[p["id"]]["seconds"], "s", flush=True)


if __name__ == "__main__":
    main()
