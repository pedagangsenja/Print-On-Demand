"""Jana imej ujian dengan diffusers di CPU (bf16 + AMX; jauh lebih laju daripada stable-diffusion.cpp di mesin ini).
Fasa 1: kod semua prompt dengan pengekod teks, buang dari RAM. Fasa 2: muat transformer (GGUF Q8), jana imej.
Diubah daripada designs/model-test/gen.py (cawangan sharp-franklin, 23 Nov).
Guna: python3 gen_diffusers.py <klein4b|klein4b_ref|zturbo|ernie|schnell|chroma_flash> [id...]"""
import gc, json, os, sys, time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import torch, diffusers  # noqa: E402
from diffusers import GGUFQuantizationConfig  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
S = Path(os.environ.get("POD_SCRATCH", "/tmp/claude-0/-home-user-Print-On-Demand/2d722db7-85d8-5f5a-9afd-4d1e293d123c/scratchpad"))
M, OUT = S / "models", S / "out"
DT = torch.bfloat16
CFG = {
    "klein4b": dict(repo="black-forest-labs/FLUX.2-klein-4B", pipe="Flux2KleinPipeline", tr="Flux2Transformer2DModel",
                    gguf="klein4b-Q8_0.gguf", dequant=True, steps=4, guidance=1.0),
    "klein4b_ref": dict(repo="black-forest-labs/FLUX.2-klein-4B", pipe="Flux2KleinPipeline", tr="Flux2Transformer2DModel",
                        gguf="klein4b-Q8_0.gguf", dequant=True, steps=4, guidance=1.0, ref=True),
    "zturbo": dict(repo="Tongyi-MAI/Z-Image-Turbo", pipe="ZImagePipeline", tr="ZImageTransformer2DModel",
                   gguf="zimage-turbo-Q8_0.gguf", steps=9, guidance=0.0),
    "ernie": dict(repo="baidu/ERNIE-Image-Turbo", pipe="ErnieImagePipeline", tr="ErnieImageTransformer2DModel",
                  gguf="ernie-turbo-Q8_0.gguf", steps=8, guidance=1.0, extra={"use_pe": False}, noext={"pe": None}),
    "schnell": dict(repo="unsloth/FLUX.1-schnell", pipe="FluxPipeline", tr="FluxTransformer2DModel",
                    gguf="flux1-schnell-city96-Q8_0.gguf", steps=4, guidance=0.0, extra={"max_sequence_length": 256}),
    "chroma_flash": dict(repo="lodestones/Chroma1-Flash", pipe="ChromaPipeline", tr="ChromaTransformer2DModel",
                         gguf="chroma1-flash-Q8_0.gguf", steps=10, guidance=1.0),
}
SEED = 42


def encode(name, pipe, prompt):
    if name == "zturbo":
        return pipe.encode_prompt(prompt, device="cpu", do_classifier_free_guidance=False)[0]
    if name == "ernie":
        return pipe.encode_prompt(prompt, device="cpu")
    if name in ("schnell",):
        pe, ppe, _ = pipe.encode_prompt(prompt=prompt, prompt_2=None, device="cpu", max_sequence_length=256)
        return {"prompt_embeds": pe, "pooled_prompt_embeds": ppe}
    if name == "chroma_flash":
        r = pipe.encode_prompt(prompt=prompt, device="cpu", do_classifier_free_guidance=False)
        return {"prompt_embeds": r[0], "prompt_attention_mask": r[2]} if len(r) > 2 else {"prompt_embeds": r[0]}
    return pipe.encode_prompt(prompt, device="cpu")[0]


def load_transformer(c):
    from diffusers.models.model_loading_utils import load_state_dict
    from diffusers.quantizers.gguf.utils import GGUFParameter, dequantize_gguf_tensor
    sd = load_state_dict(str(M / c["gguf"]))
    for k, v in list(sd.items()):
        if k.endswith("pad_token") and v.dim() == 1:  # GGUF sd.cpp simpan (3840,), diffusers mahu (1, 3840)
            sd[k] = v.reshape(1, -1)
        elif isinstance(v, GGUFParameter) and (c.get("dequant") or v.dim() == 4):
            sd[k] = dequantize_gguf_tensor(v).to(DT)
    Tr = getattr(diffusers, c["tr"])
    q = {} if c.get("dequant") else {"quantization_config": GGUFQuantizationConfig(compute_dtype=DT)}
    return Tr.from_single_file(sd, config=c["repo"], subfolder="transformer", torch_dtype=DT, **q)


def main():
    name, only = sys.argv[1], set(sys.argv[2:])
    c = CFG[name]
    torch.set_num_threads(os.cpu_count() or 4)
    Pipe = getattr(diffusers, c["pipe"])
    out = OUT / name
    out.mkdir(parents=True, exist_ok=True)
    prompts = [p for p in json.loads((HERE / "prompts.json").read_text())
               if (not only or p["id"] in only) and not (out / f"{p['id']}.png").exists()]
    if not prompts:
        return
    key = "prompt_ref" if c.get("ref") else "prompt"
    noext = c.get("noext", {})
    t0 = time.time()
    if name == "chroma_flash":  # T5 Chroma sama hash dengan T5 schnell: guna semula, jimat 9.5 GB muat turun
        from transformers import T5EncoderModel, T5TokenizerFast
        noext = dict(noext, text_encoder=T5EncoderModel.from_pretrained("unsloth/FLUX.1-schnell", subfolder="text_encoder_2", torch_dtype=DT),
                     tokenizer=T5TokenizerFast.from_pretrained("unsloth/FLUX.1-schnell", subfolder="tokenizer_2"))
    pipe = Pipe.from_pretrained(c["repo"], transformer=None, vae=None, torch_dtype=DT, **noext)
    noext = c.get("noext", {})
    embs = {}
    with torch.inference_mode():
        for p in prompts:
            embs[p["id"]] = encode(name, pipe, p[key])
    enc_s = round(time.time() - t0, 1)
    print(name, "kod prompt", enc_s, "s", flush=True)
    del pipe; gc.collect()
    tr = load_transformer(c)
    kw = dict(text_encoder=None, tokenizer=None, **noext)
    if name == "schnell":
        kw.update(text_encoder_2=None, tokenizer_2=None)
    pipe = Pipe.from_pretrained(c["repo"], transformer=tr, torch_dtype=DT, **kw)
    log = out / "times.json"
    times = json.loads(log.read_text()) if log.exists() else {}
    times["_encode_all_s"] = enc_s
    for p in prompts:
        e = embs[p["id"]]
        args = dict(e) if isinstance(e, dict) else {"prompt_embeds": e}
        if c.get("ref"):
            args["image"] = [Image.open(HERE / p["ref"]).convert("RGB")]
        t0 = time.time()
        with torch.inference_mode():
            img = pipe(**args, height=p["h"], width=p["w"], num_inference_steps=c["steps"], guidance_scale=c["guidance"],
                       generator=torch.Generator("cpu").manual_seed(SEED), **c.get("extra", {})).images[0]
        img.save(out / f"{p['id']}.png")
        times[p["id"]] = {"seconds": round(time.time() - t0, 1), "ok": True}
        log.write_text(json.dumps(times, indent=1))
        print(name, p["id"], times[p["id"]]["seconds"], "s", flush=True)


if __name__ == "__main__":
    main()
