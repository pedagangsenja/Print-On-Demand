"""Standard Lettering v1, langkah 4 (Jana): MOSS-Image-SFT + LoRA 8 langkah, CPU.
Diubah daripada scripts/lettering/gen_moss.py (cawangan affectionate-wright, 24 Nov); prompt dari kad.bina, log sama gen.py.
Fasa 1: Qwen3.5-9B (sebahagian di cakera) kod semua prompt. Fasa 2: transformer bf16 + LoRA, 8 langkah tanpa CFG.
Guna: python3 gen_moss.py [id...]
"""
import gc, os, sys, time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import torch  # noqa: E402
import torch.nn as nn  # noqa: E402
import torch.nn.functional as F  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import kad  # noqa: E402

DT = gen.DT
DEV = gen.DEV
NAME = "moss"
C = dict(repo="OpenMOSS-Team/MOSS-Image-SFT", varian="bf16 asal", steps=8, guidance=None,
         lora="lodestones/MOSS-Image-SFT-8-steps-dmd lora_latest.safetensors x0.7", penambah="thinking hidup")
LORA = ("lodestones/MOSS-Image-SFT-8-steps-dmd", "lora_latest.safetensors", 0.7)
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
    torch.set_num_threads(os.cpu_count() or 4)
    out, jobs = gen.jobs_for(NAME, set(sys.argv[1:]))
    if not jobs:
        print(NAME, "tiada kerja"); return
    from huggingface_hub import hf_hub_download, snapshot_download
    from safetensors.torch import load_file
    from transformers import AutoModel, AutoTokenizer
    from diffusers import AutoencoderKLFlux2
    from diffusers.image_processor import VaeImageProcessor

    M = snapshot_download(C["repo"])
    sys.path.insert(0, M)
    from pipeline_moss_image import MOSSImageScheduler, MOSSImageTransformer

    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(M, subfolder="tokenizer")
    mem = {"cpu": "9GiB"} if DEV == "cpu" else {**{i: "14GiB" for i in range(torch.cuda.device_count())}, "cpu": "20GiB"}
    te = AutoModel.from_pretrained(M, subfolder="text_encoder", dtype=DT, device_map="auto",
                                   max_memory=mem, offload_folder=str(OFFLOAD)).eval()
    dev0 = te.get_input_embeddings().weight.device
    embs, prompts = {}, {}
    with torch.inference_mode():
        for kid, aid, _ in jobs:
            key = f"{kid}{aid}"
            if key in embs:
                continue
            p, _ = kad.bina(kid, aid)
            txt = tok.apply_chat_template([{"role": "user", "content": p}], tokenize=False,
                                          add_generation_prompt=True, enable_thinking=True)
            h = te(**tok(txt, return_tensors="pt", truncation=True, max_length=4096).to(dev0), use_cache=False,
                   return_dict=True).last_hidden_state.to(DT).cpu()
            embs[key], prompts[key] = (h, torch.ones(1, h.shape[1], dtype=torch.bool)), p
            print("enc", key, tuple(h.shape), round(time.time() - t0, 1), flush=True)
    del te; gc.collect()
    if DEV != "cpu":
        torch.cuda.empty_cache()

    tr = MOSSImageTransformer.from_pretrained(M, subfolder="transformer", torch_dtype=DT).eval()
    repo, fname, strength = LORA
    lora = load_file(hf_hub_download(repo, fname)); pre = "diffusion_model."
    for name in sorted({k[len(pre):-len(".lora_down.weight")] for k in lora if k.endswith(".lora_down.weight")}):
        parent, _, child = name.rpartition(".")
        par = tr.get_submodule(parent)
        setattr(par, child, LoRALinear(getattr(par, child), lora[f"{pre}{name}.lora_down.weight"],
                                       lora[f"{pre}{name}.lora_up.weight"], float(lora[f"{pre}{name}.alpha"]), strength))
    del lora; gc.collect()
    tr.to(DEV)
    cfg = MOSSImageScheduler.load_config(M, subfolder="scheduler")
    sargs = {k: cfg[k] for k in ("num_train_timesteps", "shift", "training_shift")}
    vae = AutoencoderKLFlux2.from_pretrained(M, subfolder="vae", torch_dtype=torch.float32).eval().to(DEV)
    proc = VaeImageProcessor(vae_scale_factor=16)
    for kid, aid, seed in jobs:
        key = f"{kid}{aid}"
        t1 = time.time()
        pe, pm = (t.to(DEV) for t in embs[key])
        lat = torch.randn(1, 128, gen.H // 16, gen.W // 16, generator=torch.Generator("cpu").manual_seed(seed)).to(DEV)
        sch = MOSSImageScheduler(**sargs); sch.set_timesteps(C["steps"], device=DEV)
        with torch.inference_mode():
            for ts in sch.timesteps:
                with torch.autocast("cpu" if DEV == "cpu" else "cuda", dtype=DT):
                    v = tr(lat, ts, pe, pm).sample.float()
                lat = sch.step(v, ts, lat, return_dict=False)[0]
            z = lat.to(torch.float32); bn = vae.bn; eps = vae.config.batch_norm_eps
            z = z * (bn.running_var + eps).sqrt().view(1, -1, 1, 1) + bn.running_mean.view(1, -1, 1, 1)
            b, c, h, w = z.shape
            z = z.reshape(b, c // 4, 2, 2, h, w).permute(0, 1, 4, 2, 5, 3).reshape(b, c // 4, 2 * h, 2 * w)
            px = vae.decode(z, return_dict=False)[0].clamp(-1, 1)
        proc.postprocess(px, output_type="pil")[0].save(out / f"{key}_s{seed}.png")
        sec = round(time.time() - t1, 1)
        gen.log_row(out, gen.base_row(NAME, C, kid, aid, seed, prompts[key], [], sec))
        print(NAME, key, seed, sec, "s", flush=True)


if __name__ == "__main__":
    main()
