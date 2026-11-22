"""Generate typography designs with Qwen-Image-2512 (Apache-2.0) on Modal GPUs.

Run by .github/workflows/modal-gen.yml. Every designs/svg-typo/ai/queue/<name>.txt
without an output yet becomes designs/svg-typo/out/<name>_s<seed>.png (N_VARIANTS each).
Local: modal run designs/svg-typo/ai/modal_gen.py
"""
import io, os, pathlib, random
import modal

MODEL = "Qwen/Qwen-Image-2512"
NEG = "blurry text, misspelled words, extra words, gibberish letters, distorted letters, gray, shading, gradient, texture, photo, mockup, low quality"

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git")
    .pip_install("torch==2.8.0", "transformers>=4.51", "accelerate", "safetensors",
                 "sentencepiece", "huggingface_hub[hf_xet]",
                 "git+https://github.com/huggingface/diffusers")
    .env({"HF_HOME": "/cache", "HF_XET_HIGH_PERFORMANCE": "1"})
)
cache = modal.Volume.from_name("qwen-image-cache", create_if_missing=True)
app = modal.App("pod-typo-gen", image=image)


@app.cls(gpu="H100", volumes={"/cache": cache}, timeout=3600, scaledown_window=60)
class Gen:
    @modal.enter()
    def load(self):
        import torch
        from diffusers import DiffusionPipeline
        self.torch = torch
        self.pipe = DiffusionPipeline.from_pretrained(MODEL, torch_dtype=torch.bfloat16).to("cuda")
        cache.commit()

    @modal.method()
    def run(self, prompt: str, seed: int, steps: int = 50, size: int = 1328) -> bytes:
        g = self.torch.Generator(device="cuda").manual_seed(seed)
        img = self.pipe(prompt=prompt, negative_prompt=NEG, width=size, height=size,
                        num_inference_steps=steps, true_cfg_scale=4.0, generator=g).images[0]
        buf = io.BytesIO(); img.save(buf, "PNG"); return buf.getvalue()


@app.local_entrypoint()
def main(queue: str = "designs/svg-typo/ai/queue", out: str = "designs/svg-typo/out"):
    n = int(os.environ.get("N_VARIANTS", "2"))
    q, o = pathlib.Path(queue), pathlib.Path(out); o.mkdir(parents=True, exist_ok=True)
    jobs = []
    for f in sorted(q.glob("*.txt")):
        if any(o.glob(f"{f.stem}_s*.png")):
            continue
        p = f.read_text().strip()
        jobs += [(f.stem, p, random.randint(1, 2**31 - 1)) for _ in range(n)]
    if not jobs:
        print("nothing to do"); return
    gen = Gen()
    for (stem, _, seed), png in zip(jobs, gen.run.map([j[1] for j in jobs], [j[2] for j in jobs])):
        path = o / f"{stem}_s{seed}.png"; path.write_bytes(png); print("saved", path)
