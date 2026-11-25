"""Standard Lettering v1, langkah 4 (Jana): ujian kelayakan model, text-to-image penuh di CPU (diffusers, bf16 + AMX).
Diubah daripada designs/model-test-12/gen_diffusers.py dan designs/lettering-p9b/gen.py (cawangan lain, 24 Nov).
Profil model dikunci di PROFIL; seed tetap 42 dan 7 (peraturan Tukar model: setiap gaya x ayat x 2 seed).
Fasa 1: kod semua prompt, buang pengekod teks. Fasa 2: muat transformer, jana satu demi satu, log setiap imej.
Guna: python3 gen.py <klein4b|zturbo|ernie|schnell|chroma_flash|kandinsky> [id...]
"""
import gc, json, os, sys, time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import torch, diffusers, transformers  # noqa: E402
from huggingface_hub import hf_hub_download, snapshot_download  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kad  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
DT = torch.bfloat16
# Peranti: GEN_DEVICE=cpu (lalai) atau cuda (Kaggle GPU); GEN_DTYPE=fp16 pilihan; GEN_OUT = folder hasil.
DEV = os.environ.get("GEN_DEVICE", "cpu")
if os.environ.get("GEN_DTYPE") == "fp16":
    DT = torch.float16
OUT = Path(os.environ.get("GEN_OUT", str(OUT)))
SEEDS = [42, 7]
W, H = 768, 1024
PROFIL = {
    "klein4b": dict(repo="black-forest-labs/FLUX.2-klein-4B", pipe="Flux2KleinPipeline", tr="Flux2Transformer2DModel",
                    varian="bf16 asal", steps=4, guidance=1.0, max_tok=512,
                    pat=["*.json", "text_encoder/*", "tokenizer/*", "vae/*", "scheduler/*", "transformer/*"]),
    "zturbo": dict(repo="Tongyi-MAI/Z-Image-Turbo", pipe="ZImagePipeline", tr="ZImageTransformer2DModel",
                   gguf=("leejet/Z-Image-Turbo-GGUF", "z_image_turbo-Q8_0.gguf"), varian="GGUF Q8_0", steps=9,
                   guidance=0.0, max_tok=512,
                   pat=["*.json", "text_encoder/*", "tokenizer/*", "vae/*", "scheduler/*", "transformer/*.json"]),
    "ernie": dict(repo="baidu/ERNIE-Image-Turbo", pipe="ErnieImagePipeline", tr="ErnieImageTransformer2DModel",
                  gguf=("unsloth/ERNIE-Image-Turbo-GGUF", "ernie-image-turbo-Q8_0.gguf"), varian="GGUF Q8_0", steps=8,
                  guidance=1.0, extra={"use_pe": False}, noext={"pe": None}, max_tok=512, penambah="mati",
                  pat=["*.json", "text_encoder/*", "tokenizer/*", "vae/*", "scheduler/*", "transformer/*.json"]),
    "schnell": dict(repo="unsloth/FLUX.1-schnell", pipe="FluxPipeline", tr="FluxTransformer2DModel",
                    gguf=("city96/FLUX.1-schnell-gguf", "flux1-schnell-Q6_K.gguf"), varian="GGUF Q6_K", steps=4,
                    guidance=0.0, extra={"max_sequence_length": 256}, max_tok=256,
                    pat=["*.json", "text_encoder/*", "text_encoder_2/*", "tokenizer/*", "tokenizer_2/*", "vae/*",
                         "scheduler/*", "transformer/*.json"]),
    "chroma_flash": dict(repo="lodestones/Chroma1-Flash", pipe="ChromaPipeline", tr="ChromaTransformer2DModel",
                         gguf=("silveroxides/Chroma1-Flash-GGUF", "Chroma1-HD-Flash-Q8_0.gguf"), varian="GGUF Q8_0",
                         steps=10, guidance=1.0, max_tok=512,
                         pat=["*.json", "tokenizer/*", "vae/*", "scheduler/*", "transformer/*.json", "text_encoder/*.json"]),
    "kandinsky": dict(repo="kandinsky-community/kandinsky-2-2-decoder", varian="fp32 asal", steps=50, guidance=4.0,
                      max_tok=77),
}


def fit(pipe_tok, kid, aid, max_tok):
    """Turutan potong v1 bila melebihi had token: buang ekor, ruang tepi, hiasan, hierarki, larangan (teks kekal)."""
    drop = []
    for part in [None, "tail", "margin", "hiasan", "hierarki", "larangan"]:
        if part:
            drop.append(part)
        p, q = kad.bina(kid, aid, drop=drop)
        if pipe_tok is None or len(pipe_tok(p).input_ids) <= max_tok:
            return p, q, drop
    return p, q, drop


def encode(name, pipe, prompt):
    if name == "zturbo":
        return pipe.encode_prompt(prompt, device=DEV, do_classifier_free_guidance=False)[0]
    if name == "ernie":
        return pipe.encode_prompt(prompt, device=DEV)
    if name == "schnell":
        pe, ppe, _ = pipe.encode_prompt(prompt=prompt, prompt_2=None, device=DEV, max_sequence_length=256)
        return {"prompt_embeds": pe, "pooled_prompt_embeds": ppe}
    if name == "chroma_flash":
        r = pipe.encode_prompt(prompt=prompt, device=DEV, do_classifier_free_guidance=False)
        return {"prompt_embeds": r[0], "prompt_attention_mask": r[2]} if len(r) > 2 else {"prompt_embeds": r[0]}
    return pipe.encode_prompt(prompt, device=DEV)[0]


def load_transformer(c):
    Tr = getattr(diffusers, c["tr"])
    if not c.get("gguf"):
        return Tr.from_pretrained(c["repo"], subfolder="transformer", torch_dtype=DT)
    from diffusers import GGUFQuantizationConfig
    from diffusers.models.model_loading_utils import load_state_dict
    from diffusers.quantizers.gguf.utils import GGUFParameter, dequantize_gguf_tensor
    sd = load_state_dict(hf_hub_download(*c["gguf"]))
    for k, v in list(sd.items()):
        if k.endswith("pad_token") and v.dim() == 1:
            sd[k] = v.reshape(1, -1)
        elif isinstance(v, GGUFParameter) and v.dim() == 4:
            sd[k] = dequantize_gguf_tensor(v).to(DT)
    return Tr.from_single_file(sd, quantization_config=GGUFQuantizationConfig(compute_dtype=DT), config=c["repo"],
                               subfolder="transformer", torch_dtype=DT)


def jobs_for(name, only):
    out = OUT / name
    out.mkdir(parents=True, exist_ok=True)
    ids = [(k, a) for k in kad.KAD for a in kad.AYAT if not only or f"{k}{a}" in only]
    return out, [(k, a, s) for k, a in ids for s in SEEDS if not (out / f"{k}{a}_s{s}.png").exists()]


def log_row(out, row):
    with open(out / "log.jsonl", "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def base_row(name, c, kid, aid, seed, prompt, drop, sec):
    return dict(id=f"{kid}{aid}", kad=kid, ayat=aid, laluan=kad.AYAT[aid]["laluan"], model=name, repo=c["repo"],
                varian=c["varian"], langkah=c["steps"], guidance=c["guidance"], lora=c.get("lora"),
                penambah=c.get("penambah"), peranti=DEV if DEV == "cpu" else torch.cuda.get_device_name(0),
                dtype=str(DT).replace("torch.", ""), seed=seed, w=W, h=H, saat=sec, prompt=prompt, potong=drop,
                pembina=kad.VERSI_PEMBINA, versi=dict(torch=torch.__version__, diffusers=diffusers.__version__,
                                                      transformers=transformers.__version__),
                masa=time.strftime("%Y-%m-%dT%H:%M:%S"))


def run_kandinsky(c, out, jobs):
    from diffusers import AutoPipelineForText2Image
    pipe = AutoPipelineForText2Image.from_pretrained(c["repo"], torch_dtype=torch.float32)
    for kid, aid, seed in jobs:
        p, _, drop = fit(None, kid, aid, None)
        t0 = time.time()
        with torch.inference_mode():
            img = pipe(prompt=p, height=H, width=W, num_inference_steps=c["steps"], guidance_scale=c["guidance"],
                       generator=torch.Generator("cpu").manual_seed(seed)).images[0]
        img.save(out / f"{kid}{aid}_s{seed}.png")
        log_row(out, base_row("kandinsky", c, kid, aid, seed, p, ["dipotong CLIP 77 token"], round(time.time() - t0, 1)))
        print("kandinsky", kid, aid, seed, round(time.time() - t0, 1), "s", flush=True)


def main():
    name, only = sys.argv[1], set(sys.argv[2:])
    c = PROFIL[name]
    torch.set_num_threads(os.cpu_count() or 4)
    out, jobs = jobs_for(name, only)
    if not jobs:
        print(name, "tiada kerja"); return
    if name == "kandinsky":
        return run_kandinsky(c, out, jobs)
    snapshot_download(c["repo"], allow_patterns=c.get("pat"))
    Pipe = getattr(diffusers, c["pipe"])
    noext = dict(c.get("noext", {}))
    t0 = time.time()
    if name == "chroma_flash":  # T5 Chroma sama hash dengan T5 schnell
        from transformers import T5EncoderModel, T5TokenizerFast
        snapshot_download("unsloth/FLUX.1-schnell", allow_patterns=["text_encoder_2/*", "tokenizer_2/*"])
        noext.update(text_encoder=T5EncoderModel.from_pretrained("unsloth/FLUX.1-schnell", subfolder="text_encoder_2", torch_dtype=DT),
                     tokenizer=T5TokenizerFast.from_pretrained("unsloth/FLUX.1-schnell", subfolder="tokenizer_2"))
    pipe = Pipe.from_pretrained(c["repo"], transformer=None, vae=None, torch_dtype=DT, **noext).to(DEV)
    tok = getattr(pipe, "tokenizer_2", None) if name == "schnell" else pipe.tokenizer
    embs, prompts = {}, {}
    with torch.inference_mode():
        for kid, aid, _ in jobs:
            key = f"{kid}{aid}"
            if key not in embs:
                p, _, drop = fit(tok, kid, aid, c["max_tok"])
                prompts[key] = (p, drop)
                embs[key] = encode(name, pipe, p)
    print(name, "kod prompt", round(time.time() - t0, 1), "s", flush=True)
    del pipe; gc.collect()
    if DEV != "cpu":
        torch.cuda.empty_cache()
    tr = load_transformer(c)
    kw = dict(text_encoder=None, tokenizer=None, **c.get("noext", {}))
    if name == "schnell":
        kw.update(text_encoder_2=None, tokenizer_2=None)
    pipe = Pipe.from_pretrained(c["repo"], transformer=tr, torch_dtype=DT, **kw).to(DEV)
    for kid, aid, seed in jobs:
        key = f"{kid}{aid}"
        e = embs[key]
        args = dict(e) if isinstance(e, dict) else {"prompt_embeds": e}
        t0 = time.time()
        with torch.inference_mode():
            img = pipe(**args, height=H, width=W, num_inference_steps=c["steps"], guidance_scale=c["guidance"],
                       generator=torch.Generator("cpu").manual_seed(seed), **c.get("extra", {})).images[0]
        img.save(out / f"{key}_s{seed}.png")
        sec = round(time.time() - t0, 1)
        log_row(out, base_row(name, c, kid, aid, seed, *prompts[key], sec))
        print(name, key, seed, sec, "s", flush=True)


if __name__ == "__main__":
    main()
