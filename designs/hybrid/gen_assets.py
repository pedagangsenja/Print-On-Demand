"""Jana aset latar/hiasan (tanpa teks) dengan FLUX.2-klein-4B (Apache-2.0) di CPU.
Guna: python3 gen_assets.py [id...]. Hasil: ai/<id>.png + ai/times.json.
Fasa 1 kod semua prompt lalu buang text encoder dari RAM; fasa 2 jana imej (4 langkah, guidance 1.0)."""
import gc, json, os, sys, time
from pathlib import Path
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import torch
from diffusers import Flux2KleinPipeline, Flux2Transformer2DModel

HERE = Path(__file__).resolve().parent
OUT = HERE / "ai"; OUT.mkdir(exist_ok=True)
REPO, DT = "black-forest-labs/FLUX.2-klein-4B", torch.bfloat16


def main():
    only = set(sys.argv[1:])
    items = [a for a in json.loads((HERE / "assets.json").read_text())
             if (not only or a["id"] in only) and not (OUT / f"{a['id']}.png").exists()]
    if not items:
        return
    torch.set_num_threads(os.cpu_count())
    t0 = time.time()
    pipe = Flux2KleinPipeline.from_pretrained(REPO, transformer=None, vae=None, torch_dtype=DT)
    with torch.inference_mode():
        embs = {a["id"]: pipe.encode_prompt(a["prompt"], device="cpu")[0] for a in items}
    enc = round(time.time() - t0, 1)
    del pipe; gc.collect()
    tr = Flux2Transformer2DModel.from_pretrained(REPO, subfolder="transformer", torch_dtype=DT)
    pipe = Flux2KleinPipeline.from_pretrained(REPO, transformer=tr, text_encoder=None, tokenizer=None, torch_dtype=DT)
    log = OUT / "times.json"
    times = json.loads(log.read_text()) if log.exists() else {}
    times["_encode_all_s"] = enc
    for a in items:
        t0 = time.time()
        with torch.inference_mode():
            img = pipe(prompt_embeds=embs[a["id"]], height=a["h"], width=a["w"], num_inference_steps=4,
                       guidance_scale=1.0, generator=torch.Generator("cpu").manual_seed(a["seed"])).images[0]
        img.save(OUT / f"{a['id']}.png")
        times[a["id"]] = {"seconds": round(time.time() - t0, 1), "seed": a["seed"], "size": f"{a['w']}x{a['h']}"}
        log.write_text(json.dumps(times, indent=1))
        print(a["id"], times[a["id"]], flush=True)


if __name__ == "__main__":
    main()
