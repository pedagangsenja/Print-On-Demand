"""Cara 'panduan susun atur': setiap model melukis semula panduan (guides/<id>.png) dalam gaya imej rujukan.
klein 4B: imej rujukan terus (panduan + imej gaya). Z-Image, schnell, Chroma, Kandinsky: img2img diffusers.
ERNIE: img2img manual (model flow-matching: mula pada sigma = kekuatan). Hasil: out/guide_<model>/<id>.png
Guna: python3 gen_guide.py <klein4b|zturbo|ernie|schnell|chroma_flash|kandinsky> [id...]"""
import copy, gc, json, os, sys, time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import torch, diffusers  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen_diffusers as gd  # noqa: E402

DT, SEED = torch.bfloat16, 42
GEN = {  # kelas penjana, langkah, kekuatan (1.0 = abaikan panduan)
    "klein4b": dict(pipe="Flux2KleinPipeline", steps=4, strength=None),
    "zturbo": dict(pipe="ZImageImg2ImgPipeline", steps=9, strength=0.6),
    "ernie": dict(pipe="ErnieImagePipeline", steps=8, strength=0.6),
    "schnell": dict(pipe="FluxImg2ImgPipeline", steps=6, strength=0.6),
    "chroma_flash": dict(pipe="ChromaImg2ImgPipeline", steps=10, strength=0.6),
}
KLEIN = ("Image 1 shows the text and layout, image 2 shows the style. Redraw image 1 with exactly the same words, spelling, "
         "line order and layout, but make it look exactly like image 2: same letter shapes, colors, textures and ornaments.")


def tail(p):
    return " The poster text has %d lines, spelled exactly, in this order: %s. No other text." % (
        len(p["lines"]), " ".join(f'"{x}"' for x in p["lines"]))


def ernie_img2img(pipe, guide, p, steps, strength, gen, args):
    """img2img manual untuk ERNIE: kod panduan ke latent, campur hingar pada sigma mula, langkau langkah awal."""
    sch = pipe.scheduler
    probe = copy.deepcopy(sch)
    probe.set_timesteps(sigmas=torch.linspace(1.0, 0.0, steps + 1)[:-1], device="cpu")
    k = int((probe.sigmas[:-1] > strength).sum())
    s0 = float(probe.sigmas[k])
    with torch.inference_mode():
        px = pipe.image_processor.preprocess(guide, height=p["h"], width=p["w"]).to(pipe.vae.dtype)
        z = pipe._patchify_latents(pipe.vae.encode(px).latent_dist.mode())
        bn = pipe.vae.bn
        x0 = (z - bn.running_mean.view(1, -1, 1, 1)) / torch.sqrt(bn.running_var.view(1, -1, 1, 1) + 1e-5)
        lat = (s0 * torch.randn(x0.shape, generator=gen) + (1 - s0) * x0.float()).to(DT)
    orig = sch.set_timesteps

    def patched(*a, **kw):
        orig(*a, **kw)
        sch.timesteps, sch.sigmas = sch.timesteps[k:], sch.sigmas[k:]
        sch._step_index = sch._begin_index = None
    sch.set_timesteps = patched
    try:
        with torch.inference_mode():
            return pipe(**args, latents=lat, height=p["h"], width=p["w"], num_inference_steps=steps, guidance_scale=1.0,
                        use_pe=False).images[0]
    finally:
        sch.set_timesteps = orig


def run_kandinsky(prompts, out, times, log):
    from diffusers import AutoPipelineForImage2Image
    pipe = AutoPipelineForImage2Image.from_pretrained("kandinsky-community/kandinsky-2-2-decoder", torch_dtype=torch.float32)
    for p in prompts:
        t0 = time.time()
        with torch.inference_mode():
            img = pipe(prompt=p["prompt"], image=Image.open(HERE / "guides" / f"{p['id']}.png").convert("RGB"), strength=0.5,
                       height=p["h"], width=p["w"], num_inference_steps=50, guidance_scale=4.0,
                       generator=torch.Generator("cpu").manual_seed(SEED)).images[0]
        img.save(out / f"{p['id']}.png")
        times[p["id"]] = {"seconds": round(time.time() - t0, 1), "ok": True}
        log.write_text(json.dumps(times, indent=1))
        print("guide_kandinsky", p["id"], times[p["id"]]["seconds"], "s", flush=True)


def main():
    name, only = sys.argv[1], set(sys.argv[2:])
    torch.set_num_threads(os.cpu_count() or 4)
    out = gd.OUT / f"guide_{name}"
    out.mkdir(parents=True, exist_ok=True)
    log = out / "times.json"
    times = json.loads(log.read_text()) if log.exists() else {}
    prompts = [p for p in json.loads((HERE / "prompts.json").read_text())
               if (not only or p["id"] in only) and not (out / f"{p['id']}.png").exists()]
    if not prompts:
        return
    if name == "kandinsky":
        return run_kandinsky(prompts, out, times, log)
    c, g = gd.CFG[name], GEN[name]
    text = {p["id"]: (KLEIN + tail(p)) if name == "klein4b" else p["prompt"] for p in prompts}
    noext = dict(c.get("noext", {}))
    if name == "chroma_flash":
        from transformers import T5EncoderModel, T5TokenizerFast
        noext.update(text_encoder=T5EncoderModel.from_pretrained("unsloth/FLUX.1-schnell", subfolder="text_encoder_2", torch_dtype=DT),
                     tokenizer=T5TokenizerFast.from_pretrained("unsloth/FLUX.1-schnell", subfolder="tokenizer_2"))
    t0 = time.time()
    enc = getattr(diffusers, c["pipe"]).from_pretrained(c["repo"], transformer=None, vae=None, torch_dtype=DT, **noext)
    with torch.inference_mode():
        embs = {i: gd.encode(name, enc, t) for i, t in text.items()}
    times["_encode_all_s"] = round(time.time() - t0, 1)
    print(name, "kod prompt", times["_encode_all_s"], "s", flush=True)
    del enc; gc.collect()
    tr = gd.load_transformer(c)
    kw = dict(text_encoder=None, tokenizer=None, **c.get("noext", {}))
    if name == "schnell":
        kw.update(text_encoder_2=None, tokenizer_2=None)
    pipe = getattr(diffusers, g["pipe"]).from_pretrained(c["repo"], transformer=tr, torch_dtype=DT, **kw)
    for p in prompts:
        e = embs[p["id"]]
        args = dict(e) if isinstance(e, dict) else {"prompt_embeds": e}
        guide = Image.open(HERE / "guides" / f"{p['id']}.png").convert("RGB")
        gen = torch.Generator("cpu").manual_seed(SEED)
        t0 = time.time()
        if name == "ernie":
            img = ernie_img2img(pipe, guide, p, g["steps"], g["strength"], gen, args)
        else:
            if name == "klein4b":
                args["image"] = [guide, Image.open(HERE / p["ref"]).convert("RGB")]
            else:
                args.update(image=guide, strength=g["strength"])
            with torch.inference_mode():
                img = pipe(**args, height=p["h"], width=p["w"], num_inference_steps=g["steps"], guidance_scale=c["guidance"],
                           generator=gen, **{k: v for k, v in c.get("extra", {}).items() if k != "use_pe"}).images[0]
        img.save(out / f"{p['id']}.png")
        times[p["id"]] = {"seconds": round(time.time() - t0, 1), "ok": True}
        log.write_text(json.dumps(times, indent=1))
        print(f"guide_{name}", p["id"], times[p["id"]]["seconds"], "s", flush=True)


if __name__ == "__main__":
    main()
