"""Ujian K6 di GPU Hugging Face ZeroGPU (Space awam), untuk banding kelajuan dengan CPU.
Prompt sama (kad.bina), seed 42, 768x1024, langkah sama dengan profil V1. Masa = jam dinding setiap panggilan
(termasuk barisan dan rangkaian), jadi ia had atas masa GPU sebenar. Kuota: akaun Free 5 minit GPU sehari.
Guna: python3 gen_hf_space.py [zturbo|moss ...]
"""
import json, shutil, sys, time
from pathlib import Path

from gradio_client import Client

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kad  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "out_gpu_hf"
W, H, SEED = 768, 1024, 42
SPACE = {
    "zturbo": dict(url="https://mrfakename-z-image-turbo.hf.space", api="/generate_image",
                   args=lambda p: dict(prompt=p, height=H, width=W, num_inference_steps=9, seed=SEED, randomize_seed=False)),
    "moss": dict(url="https://hugging-apps-moss-image-8-step-dmd.hf.space", api="/generate",
                 args=lambda p: dict(prompt=p, height=H, width=W, num_steps=8, seed=SEED, randomize_seed=False,
                                     lora_strength=0.7)),
}


def main():
    for name in sys.argv[1:] or list(SPACE):
        s = SPACE[name]
        out = OUT / name
        out.mkdir(parents=True, exist_ok=True)
        c = Client(s["url"], verbose=False)
        for aid in "PDL":
            key = f"K6{aid}"
            f = out / f"{key}_s{SEED}.png"
            if f.exists():
                continue
            p, _ = kad.bina("K6", aid)
            t0 = time.time()
            try:
                img, seed_used = c.predict(**s["args"](p), api_name=s["api"])
            except Exception as e:  # kuota habis atau Space sibuk: rekod dan teruskan
                print(name, key, "GAGAL", type(e).__name__, str(e)[:200], flush=True)
                continue
            sec = round(time.time() - t0, 1)
            shutil.copy(img, f)
            row = dict(id=key, kad="K6", ayat=aid, model=name, space=s["url"], seed=SEED, seed_used=seed_used, w=W, h=H,
                       saat=sec, saat_jenis="jam dinding (termasuk barisan + rangkaian)", peranti="HF ZeroGPU",
                       prompt=p, pembina=kad.VERSI_PEMBINA, masa=time.strftime("%Y-%m-%dT%H:%M:%S"))
            with open(out / "log.jsonl", "a") as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(name, key, SEED, sec, "s", flush=True)


if __name__ == "__main__":
    main()
