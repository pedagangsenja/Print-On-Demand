"""Free local CPU generation with FLUX.2 [klein] 4B (Apache-2.0) via diffusers. No account, no quota.
usage: python3 local_gen.py prompt.txt out.png [seed] [steps] [size]
Loads text encoder and transformer one after another to fit in ~15 GB RAM."""
import sys, time, gc, torch
from diffusers import Flux2KleinPipeline
REPO = "black-forest-labs/FLUX.2-klein-4B"; dt = torch.bfloat16
prompt = open(sys.argv[1]).read().strip(); out = sys.argv[2]
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
steps = int(sys.argv[4]) if len(sys.argv) > 4 else 4
size = int(sys.argv[5]) if len(sys.argv) > 5 else 1024
torch.set_num_threads(4); t = time.time()
te = Flux2KleinPipeline.from_pretrained(REPO, transformer=None, vae=None, torch_dtype=dt)
with torch.no_grad(): pe = te.encode_prompt(prompt, device="cpu")[0]
del te; gc.collect(); print("encoded", round(time.time() - t), "s", flush=True)
pipe = Flux2KleinPipeline.from_pretrained(REPO, text_encoder=None, tokenizer=None, torch_dtype=dt)
img = pipe(prompt_embeds=pe, height=size, width=size, num_inference_steps=steps, guidance_scale=1.0,
           generator=torch.Generator("cpu").manual_seed(seed)).images[0]
img.save(out); print("ok", out, "seed", seed, "secs", round(time.time() - t))
