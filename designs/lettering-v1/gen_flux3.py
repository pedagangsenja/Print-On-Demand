"""Standard Lettering v1.2, langkah 4 (Jana): FLUX 3 Image Klein (suling, 16 langkah, tanpa guidance) di CPU.
Aturan prompt 3.8 (rev r1 sejak 27 Nov 2026): kapsyen penuh + jadual kotak JSON daripada pembina; blok penambah prompt DIBUANG
(kad model: "for any prompt that already is a full caption, remove the upsampler step").
Pipeline modular diffusers (kad model rasmi). RAM 15 GB: pengekod teks (Qwen3-VL-4B) dimuat dan dibuang dahulu,
kemudian transformer 5.6B bf16. Lesen: FLUX Kommunity v1.0 (hasil komersial bersyarat).
Guna: python3 gen_flux3.py [id...]     (GEN_VARIAN=pembina)
"""
import gc, os, sys, time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import torch  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402

NAME = "klein3"
REPO = "black-forest-labs/flux-3-image-klein"
C = dict(repo=REPO, varian="bf16 asal (suling)", steps=16, guidance=None,
         penambah="dimatikan (blok prompt_upsampler dibuang)")
DT = gen.DT


def main():
    torch.set_num_threads(os.cpu_count() or 4)
    out, jobs = gen.jobs_for(NAME, set(sys.argv[1:]))
    if not jobs:
        print(NAME, "tiada kerja"); return
    gen.NAMA[0] = NAME
    from diffusers import ModularPipeline
    t0 = time.time()
    blocks = ModularPipeline.from_pretrained(REPO).blocks
    blocks.sub_blocks.pop("prompt_upsampler")
    print(NAME, "blok:", list(blocks.sub_blocks), flush=True)
    te_block = blocks.sub_blocks.pop("text_encoder")
    te = te_block.init_pipeline(REPO)
    te.load_components(dtype={"default": DT})
    te.to(gen.DEV)
    nama_keluar = [o.name for o in te_block.intermediate_outputs]
    embs, prompts = {}, {}
    with torch.inference_mode():
        for kid, aid, _ in jobs:
            key = f"{kid}{aid}"
            if key in embs:
                continue
            p, _, drop = gen.fit(None, kid, aid, None)
            st = te(prompt=p)
            embs[key] = {n: st.get(n) for n in nama_keluar if st.get(n) is not None}
            prompts[key] = (p, drop)
            print(NAME, "kod", key, {n: tuple(v.shape) for n, v in embs[key].items() if hasattr(v, "shape")},
                  round(time.time() - t0, 1), "s", flush=True)
    del te; gc.collect()
    pipe = blocks.init_pipeline(REPO)
    pipe.load_components(dtype={"vae": torch.float32, "default": DT})
    pipe.to(gen.DEV)
    print(NAME, "muat", round(time.time() - t0, 1), "s", flush=True)
    for kid, aid, seed in jobs:
        key = f"{kid}{aid}"
        t1 = time.time()
        with torch.inference_mode():
            img = pipe(**embs[key], height=gen.H, width=gen.W, num_inference_steps=C["steps"],
                       generator=torch.Generator("cpu").manual_seed(seed), output="images")[0]
        img.save(out / f"{key}_s{seed}.png")
        sec = round(time.time() - t1, 1)
        gen.log_row(out, gen.base_row(NAME, C, kid, aid, seed, *prompts[key], sec))
        print(NAME, key, seed, sec, "s", flush=True)


if __name__ == "__main__":
    main()
