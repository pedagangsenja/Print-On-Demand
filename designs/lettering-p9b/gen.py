"""Ujian P9b: quote pendek 6 gaya x seed 42,7 (sama seperti ujian MOSS P9). Diubah daripada designs/model-test/gen.py.
Jana 10 prompt ujian dengan diffusers di CPU (bf16, AMX). Guna: python3 gen.py <klein4b|zimage|ernie> [id...]
Fasa 1: kod semua prompt dengan text encoder, buang dari RAM. Fasa 2: muat transformer, jana imej.
Transformer Z-Image & ERNIE dari GGUF Q8 (muat 15 GB RAM); klein dari bf16 asal."""
import gc, json, os, sys, time
from pathlib import Path
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import torch, diffusers
from diffusers import GGUFQuantizationConfig

HERE = Path(__file__).resolve().parent
M = Path(os.environ.get("MODELS", "/tmp/models"))
DT = torch.bfloat16
CFG = {
    "klein4b": dict(repo="black-forest-labs/FLUX.2-klein-4B", pipe="Flux2KleinPipeline", tr="Flux2Transformer2DModel", gguf=None, steps=4, guidance=1.0, extra={}),
    "zimage": dict(repo="Tongyi-MAI/Z-Image-Turbo", pipe="ZImagePipeline", tr="ZImageTransformer2DModel", gguf=M / "zimage-turbo-Q8_0.gguf", steps=9, guidance=0.0, extra={}),
    "ernie": dict(repo="baidu/ERNIE-Image-Turbo", pipe="ErnieImagePipeline", tr="ErnieImageTransformer2DModel", gguf=M / "ernie-image-turbo-Q8_0.gguf", steps=8, guidance=1.0, extra={"use_pe": False}),
}
SEEDS = [42, 7]


def main():
    name, only = sys.argv[1], set(sys.argv[2:])
    c = CFG[name]
    torch.set_num_threads(4)
    Pipe = getattr(diffusers, c["pipe"])
    prompts = [p for p in json.loads((HERE / "prompts.json").read_text()) if not only or p["id"] in only]
    out = HERE / "out" / name; out.mkdir(parents=True, exist_ok=True)
    jobs = [(p, s) for s in SEEDS for p in prompts if not (out / f"{p['id']}_{name}_s{s}.png").exists()]
    prompts = list({p['id']: p for p, _ in jobs}.values())
    if not prompts:
        return
    noext = {"pe": None} if name == "ernie" else {}
    # fasa 1
    t0 = time.time()
    pipe = Pipe.from_pretrained(c["repo"], transformer=None, vae=None, torch_dtype=DT, **noext)
    embs = {}
    with torch.inference_mode():
        for p in prompts:
            if name == "zimage":
                e, _ = pipe.encode_prompt(p["prompt"], device="cpu", do_classifier_free_guidance=False)
            elif name == "ernie":
                e = pipe.encode_prompt(p["prompt"], device="cpu")
            else:
                e = pipe.encode_prompt(p["prompt"], device="cpu")[0]
            embs[p["id"]] = e
    enc_s = round(time.time() - t0, 1)
    del pipe; gc.collect()
    # fasa 2
    if c["gguf"]:
        from diffusers.models.model_loading_utils import load_state_dict
        from diffusers.quantizers.gguf.utils import GGUFParameter, dequantize_gguf_tensor
        sd = load_state_dict(str(c["gguf"]))
        for k, v in list(sd.items()):
            if k.endswith("pad_token") and v.dim() == 1:  # GGUF sd.cpp simpan (3840,), diffusers mahu (1, 3840)
                sd[k] = v.reshape(1, -1)
            elif isinstance(v, GGUFParameter) and v.dim() == 4:  # conv tidak disokong GGUF: nyahmampat ke bf16
                sd[k] = dequantize_gguf_tensor(v).to(DT)
        tr = getattr(diffusers, c["tr"]).from_single_file(sd, quantization_config=GGUFQuantizationConfig(compute_dtype=DT),
                                                          config=c["repo"], subfolder="transformer", torch_dtype=DT)
    else:
        tr = getattr(diffusers, c["tr"]).from_pretrained(c["repo"], subfolder="transformer", torch_dtype=DT)
    kw = dict(text_encoder=None, tokenizer=None, **noext)
    pipe = Pipe.from_pretrained(c["repo"], transformer=tr, torch_dtype=DT, **kw)
    log = out / "times.json"
    times = json.loads(log.read_text()) if log.exists() else {}
    times["_encode_all_s"] = enc_s
    for p, seed in jobs:
        t0 = time.time()
        with torch.inference_mode():
            img = pipe(prompt_embeds=embs[p["id"]], height=p["h"], width=p["w"], num_inference_steps=c["steps"],
                       guidance_scale=c["guidance"], generator=torch.Generator("cpu").manual_seed(seed), **c["extra"]).images[0]
        key = f"{p['id']}_{name}_s{seed}"
        img.save(out / f"{key}.png")
        times[key] = {"seconds": round(time.time() - t0, 1), "ok": True}
        log.write_text(json.dumps(times, indent=1))
        print(key, times[key]["seconds"], "s", flush=True)


if __name__ == "__main__":
    main()
