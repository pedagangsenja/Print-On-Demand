"""Ujian lettering (prompt panjang 11-14 perkataan) di CPU. Guna: python3 gen.py <ernie|ernie_pe|moss> [id...]

ernie    : ERNIE-Image-Turbo GGUF Q8, 8 langkah, tanpa penambah prompt (sama seperti ujian 23 Nov).
ernie_pe : prompt ditulis semula dahulu oleh penambah prompt (PE) ERNIE, kemudian dijana seperti ernie.
moss     : MOSS-Image-SFT bf16 + LoRA 8 langkah lodestones (lora_latest, kekuatan 0.7, tanpa CFG),
           cara sama dengan Space hugging-apps/moss-image-8-step-dmd, diubah untuk CPU.
Fasa 1 kod prompt dan buang pengekod teks dari RAM; fasa 2 jana imej. Seed 42.
"""
import gc
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import torch

HERE = Path(__file__).resolve().parent
S = Path("/tmp/claude-0/-home-user-Print-On-Demand/9b462b96-1f96-5add-a3d4-6d6636007ee7/scratchpad")
DT = torch.bfloat16
SEED = 42
ERNIE = "baidu/ERNIE-Image-Turbo"
MOSS = "OpenMOSS-Team/MOSS-Image-SFT"
MOSS_LORA = ("lodestones/MOSS-Image-SFT-8-steps-dmd", "lora_latest.safetensors", 0.7)


def log_time(out, pid, sec, extra=None):
    f = out / "times.json"
    t = json.loads(f.read_text()) if f.exists() else {}
    t[pid] = {"seconds": round(sec, 1), **(extra or {})}
    f.write_text(json.dumps(t, indent=1, ensure_ascii=False))
    print(out.name, pid, round(sec, 1), "s", flush=True)


def enhance(prompts, out):
    """Tulis semula prompt dengan PE ERNIE; simpan supaya boleh disemak."""
    from diffusers import ErnieImagePipeline
    f = out / "enhanced.json"
    done = json.loads(f.read_text()) if f.exists() else {}
    todo = [p for p in prompts if p["id"] not in done]
    if todo:
        pipe = ErnieImagePipeline.from_pretrained(ERNIE, transformer=None, vae=None, text_encoder=None, tokenizer=None, torch_dtype=DT)
        for p in todo:
            t0 = time.time(); torch.manual_seed(SEED)
            with torch.inference_mode():
                done[p["id"]] = pipe._enhance_prompt_with_pe(p["prompt"], "cpu", width=p["w"], height=p["h"])
            f.write_text(json.dumps(done, indent=1, ensure_ascii=False))
            print("pe", p["id"], round(time.time() - t0, 1), "s", flush=True)
        del pipe; gc.collect()
    return [{**p, "prompt": done[p["id"]]} for p in prompts]


def run_ernie(prompts, out):
    import diffusers
    from diffusers import ErnieImagePipeline, ErnieImageTransformer2DModel, GGUFQuantizationConfig
    from diffusers.models.model_loading_utils import load_state_dict
    from diffusers.quantizers.gguf.utils import GGUFParameter, dequantize_gguf_tensor
    t0 = time.time()
    pipe = ErnieImagePipeline.from_pretrained(ERNIE, transformer=None, vae=None, pe=None, torch_dtype=DT)
    with torch.inference_mode():
        embs = {p["id"]: pipe.encode_prompt(p["prompt"], device="cpu") for p in prompts}
    enc = time.time() - t0
    del pipe; gc.collect()
    sd = load_state_dict(str(S / "models/ernie-turbo-Q8_0.gguf"))
    for k, v in list(sd.items()):
        if k.endswith("pad_token") and v.dim() == 1:
            sd[k] = v.reshape(1, -1)
        elif isinstance(v, GGUFParameter) and v.dim() == 4:
            sd[k] = dequantize_gguf_tensor(v).to(DT)
    tr = ErnieImageTransformer2DModel.from_single_file(sd, quantization_config=GGUFQuantizationConfig(compute_dtype=DT),
                                                        config=ERNIE, subfolder="transformer", torch_dtype=DT)
    pipe = ErnieImagePipeline.from_pretrained(ERNIE, transformer=tr, text_encoder=None, tokenizer=None, pe=None, torch_dtype=DT)
    for p in prompts:
        t0 = time.time()
        with torch.inference_mode():
            img = pipe(prompt_embeds=embs[p["id"]], height=p["h"], width=p["w"], num_inference_steps=8, guidance_scale=1.0,
                       generator=torch.Generator("cpu").manual_seed(SEED), use_pe=False).images[0]
        img.save(out / f"{p['id']}.png")
        log_time(out, p["id"], time.time() - t0, {"encode_all_s": round(enc, 1)})


def run_moss(prompts, out):
    import torch.nn as nn
    import torch.nn.functional as F
    from huggingface_hub import hf_hub_download, snapshot_download
    from safetensors.torch import load_file
    from transformers import AutoModel, AutoTokenizer
    from diffusers import AutoencoderKLFlux2
    from diffusers.image_processor import VaeImageProcessor

    base = Path(snapshot_download(MOSS, allow_patterns=["pipeline_moss_image.py"]))
    sys.path.insert(0, str(base)); M = str(base)  # laluan tempatan (tokenizer tiada config.json)
    from pipeline_moss_image import MOSSImageScheduler, MOSSImageTransformer

    # fasa 1: pengekod teks Qwen3.5-9B (~17 GB) > RAM, jadi sebahagian lapisan di cakera
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(M, subfolder="tokenizer")
    te = AutoModel.from_pretrained(M, subfolder="text_encoder", dtype=DT, device_map="auto",
                                   max_memory={"cpu": "9GiB"}, offload_folder=str(S / "offload")).eval()
    embs = {}
    with torch.inference_mode():
        for p in prompts:
            txt = tok.apply_chat_template([{"role": "user", "content": p["prompt"]}], tokenize=False,
                                          add_generation_prompt=True, enable_thinking=True)
            ids = tok(txt, return_tensors="pt", truncation=True, max_length=4096)
            h = te(**ids, use_cache=False, return_dict=True).last_hidden_state.to(DT).cpu()
            embs[p["id"]] = (h, torch.ones(1, h.shape[1], dtype=torch.bool))
            print("enc", p["id"], h.shape, round(time.time() - t0, 1), flush=True)
    enc = time.time() - t0
    del te; gc.collect()

    # fasa 2: transformer bf16 + LoRA 8 langkah (sama seperti app.py Space)
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

    tr = MOSSImageTransformer.from_pretrained(M, subfolder="transformer", torch_dtype=DT).eval()
    repo, fname, strength = MOSS_LORA
    lora = load_file(hf_hub_download(repo, fname)); pre = "diffusion_model."
    mods = sorted({k[len(pre):-len(".lora_down.weight")] for k in lora if k.endswith(".lora_down.weight")})
    for name in mods:
        parent, _, child = name.rpartition(".")
        par = tr.get_submodule(parent)
        setattr(par, child, LoRALinear(getattr(par, child), lora[f"{pre}{name}.lora_down.weight"],
                                       lora[f"{pre}{name}.lora_up.weight"], float(lora[f"{pre}{name}.alpha"]), strength))
    del lora; gc.collect()
    print("lora on", len(mods), "linears", flush=True)
    cfg = MOSSImageScheduler.load_config(M, subfolder="scheduler")
    sargs = {k: cfg[k] for k in ("num_train_timesteps", "shift", "training_shift")}
    vae = AutoencoderKLFlux2.from_pretrained(M, subfolder="vae", torch_dtype=torch.float32).eval()
    proc = VaeImageProcessor(vae_scale_factor=16)
    for p in prompts:
        t0 = time.time()
        pe, pm = embs[p["id"]]
        lat = torch.randn(1, 128, p["h"] // 16, p["w"] // 16, generator=torch.Generator("cpu").manual_seed(SEED))
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
        proc.postprocess(px, output_type="pil")[0].save(out / f"{p['id']}.png")
        log_time(out, p["id"], time.time() - t0, {"encode_all_s": round(enc, 1)})


def main():
    name, only = sys.argv[1], set(sys.argv[2:])
    torch.set_num_threads(4)
    out = HERE / "out" / name; out.mkdir(parents=True, exist_ok=True)
    prompts = [p for p in json.loads((HERE / "prompts.json").read_text()) if not only or p["id"] in only]
    prompts = [p for p in prompts if not (out / f"{p['id']}.png").exists()]
    if not prompts:
        return
    if name == "ernie_pe":
        prompts = enhance(prompts, out)
    (run_moss if name == "moss" else run_ernie)(prompts, out)


if __name__ == "__main__":
    main()
