"""Jana lettering di CPU container dengan MOSS-Image-SFT (Apache 2.0) + LoRA 8 langkah lodestones.
Diubah daripada designs/lettering-test/gen.py (cawangan sharp-franklin, 23 Nov): pengekod teks
dijalankan sekali bagi setiap prompt unik, kemudian semua seed dijana. ~6 min/imej 768x1024 (4 teras).

Guna: python3 scripts/lettering/gen_moss.py <prompts.json> <out_dir> [--seeds 42,7] [id...]
"""
import gc
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import torch  # noqa: E402
import torch.nn as nn  # noqa: E402
import torch.nn.functional as F  # noqa: E402

DT = torch.bfloat16
MOSS = "OpenMOSS-Team/MOSS-Image-SFT"
MOSS_LORA = ("lodestones/MOSS-Image-SFT-8-steps-dmd", "lora_latest.safetensors", 0.7)
OFFLOAD = Path(os.environ.get("MOSS_OFFLOAD", "/tmp/moss-offload"))


class LoRALinear(nn.Module):
    def __init__(self, b, down, up, alpha, strength):
        super().__init__()
        self.base = b
        self.register_buffer("down", down.to(b.weight.dtype), persistent=False)
        self.register_buffer("up", up.to(b.weight.dtype), persistent=False)
        self.scale = alpha / down.shape[0] * strength

    @property
    def weight(self):
        return self.base.weight

    def forward(self, x):
        return self.base(x) + F.linear(F.linear(x, self.down), self.up) * self.scale


def main():
    args = sys.argv[1:]
    src, out = Path(args.pop(0)), Path(args.pop(0))
    seeds = [42]
    if args and args[0] == "--seeds":
        args.pop(0); seeds = [int(x) for x in args.pop(0).split(",")]
    only = set(args)
    torch.set_num_threads(os.cpu_count() or 4)
    out.mkdir(parents=True, exist_ok=True)
    prompts = [p for p in json.loads(src.read_text()) if not only or p["id"] in only]
    jobs = [(p, s) for s in seeds for p in prompts if not (out / f"{p['id']}_moss_s{s}.png").exists()]
    if not jobs:
        return

    from huggingface_hub import hf_hub_download, snapshot_download
    from safetensors.torch import load_file
    from transformers import AutoModel, AutoTokenizer
    from diffusers import AutoencoderKLFlux2
    from diffusers.image_processor import VaeImageProcessor

    base = Path(snapshot_download(MOSS))
    sys.path.insert(0, str(base)); M = str(base)
    from pipeline_moss_image import MOSSImageScheduler, MOSSImageTransformer

    # Fasa 1: pengekod teks Qwen3.5-9B (~17 GB) melebihi RAM -> sebahagian lapisan di cakera.
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(M, subfolder="tokenizer")
    te = AutoModel.from_pretrained(M, subfolder="text_encoder", dtype=DT, device_map="auto",
                                   max_memory={"cpu": "9GiB"}, offload_folder=str(OFFLOAD)).eval()
    embs = {}
    with torch.inference_mode():
        for p in {p["id"]: p for p, _ in jobs}.values():
            txt = tok.apply_chat_template([{"role": "user", "content": p["prompt"]}], tokenize=False,
                                          add_generation_prompt=True, enable_thinking=True)
            ids = tok(txt, return_tensors="pt", truncation=True, max_length=4096)
            h = te(**ids, use_cache=False, return_dict=True).last_hidden_state.to(DT).cpu()
            embs[p["id"]] = (h, torch.ones(1, h.shape[1], dtype=torch.bool))
            print("enc", p["id"], tuple(h.shape), round(time.time() - t0, 1), flush=True)
    del te; gc.collect()

    # Fasa 2: transformer bf16 + LoRA 8 langkah (tanpa CFG), seperti Space moss-image-8-step-dmd.
    tr = MOSSImageTransformer.from_pretrained(M, subfolder="transformer", torch_dtype=DT).eval()
    repo, fname, strength = MOSS_LORA
    lora = load_file(hf_hub_download(repo, fname)); pre = "diffusion_model."
    mods = sorted({k[len(pre):-len(".lora_down.weight")] for k in lora if k.endswith(".lora_down.weight")})
    for name in mods:
        parent, _, child = name.rpartition(".")
        par = tr.get_submodule(parent)
        setattr(par, child, LoRALinear(getattr(par, child), lora[f"{pre}{name}.lora_down.weight"],
                                       lora[f"{pre}{name}.lora_up.weight"],
                                       float(lora[f"{pre}{name}.alpha"]), strength))
    del lora; gc.collect()
    cfg = MOSSImageScheduler.load_config(M, subfolder="scheduler")
    sargs = {k: cfg[k] for k in ("num_train_timesteps", "shift", "training_shift")}
    vae = AutoencoderKLFlux2.from_pretrained(M, subfolder="vae", torch_dtype=torch.float32).eval()
    proc = VaeImageProcessor(vae_scale_factor=16)
    log = out / "times_moss.json"
    times = json.loads(log.read_text()) if log.exists() else {}
    for p, seed in jobs:
        t1 = time.time()
        pe, pm = embs[p["id"]]
        lat = torch.randn(1, 128, p["h"] // 16, p["w"] // 16, generator=torch.Generator("cpu").manual_seed(seed))
        sch = MOSSImageScheduler(**sargs); sch.set_timesteps(8, device="cpu")
        with torch.inference_mode():
            for ts in sch.timesteps:
                with torch.autocast("cpu", dtype=DT):
                    v = tr(lat, ts, pe, pm).sample.float()
                lat = sch.step(v, ts, lat, return_dict=False)[0]
            z = lat.to(torch.float32); bn = vae.bn; eps = vae.config.batch_norm_eps
            z = z * (bn.running_var + eps).sqrt().view(1, -1, 1, 1) + bn.running_mean.view(1, -1, 1, 1)
            b, c, h, w = z.shape
            z = z.reshape(b, c // 4, 2, 2, h, w).permute(0, 1, 4, 2, 5, 3).reshape(b, c // 4, 2 * h, 2 * w)
            px = vae.decode(z, return_dict=False)[0].clamp(-1, 1)
        key = f"{p['id']}_moss_s{seed}"
        proc.postprocess(px, output_type="pil")[0].save(out / f"{key}.png")
        times[key] = round(time.time() - t1, 1)
        log.write_text(json.dumps(times, indent=1))
        print("img", key, times[key], "s", flush=True)


if __name__ == "__main__":
    main()
