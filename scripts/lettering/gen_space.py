"""Jana melalui Space rasmi Qwen-Image-2512 (ZeroGPU percuma: kuota ~5 min GPU sehari, cukup 1-3 imej).
Token HF disuntik oleh proxy sesi (header x-hf-authorization); tiada kunci dalam kod.

Guna: python3 scripts/lettering/gen_space.py <prompts.json> <out_dir> <id> [seed] [steps]
"""
import json
import shutil
import sys
import time
from pathlib import Path

from gradio_client import Client

SPACE = "https://qwen-qwen-image-2512.hf.space"


def main():
    src, out, pid = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 42
    steps = int(sys.argv[5]) if len(sys.argv) > 5 else 30
    p = next(x for x in json.loads(Path(src).read_text()) if x["id"] == pid)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    img, used_seed = Client(SPACE, verbose=False).predict(
        prompt=p["prompt"], seed=seed, randomize_seed=False, aspect_ratio="3:4",
        guidance_scale=4.0, num_inference_steps=steps, prompt_enhance=False, api_name="/infer")
    path = img["path"] if isinstance(img, dict) else img
    dst = out / f"{pid}_qwen_s{int(used_seed)}.png"
    shutil.copy(path, dst)
    print(dst, round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
