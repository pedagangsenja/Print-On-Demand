"""Fix a misspelled word in a generated design with FLUX.2 klein 4B edit mode (CPU).
usage: python3 fix.py in.png out.png "WRONG" "RIGHT" [seed]"""
import sys, time, gc, torch
from PIL import Image
from diffusers import Flux2KleinPipeline
REPO = "black-forest-labs/FLUX.2-klein-4B"; dt = torch.bfloat16
src, out, wrong, right = sys.argv[1:5]; seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
p = (f'Correct the spelling in this black and white typography design: the word "{wrong}" must read exactly "{right}". '
     "Keep the same lettering style, size, position, layout, decorations and every other word exactly the same. "
     "Solid black on white, crisp edges.")
torch.set_num_threads(4); t = time.time()
te = Flux2KleinPipeline.from_pretrained(REPO, transformer=None, vae=None, torch_dtype=dt)
with torch.no_grad(): pe = te.encode_prompt(p, device="cpu")[0]
del te; gc.collect()
pipe = Flux2KleinPipeline.from_pretrained(REPO, text_encoder=None, tokenizer=None, torch_dtype=dt)
pipe.set_progress_bar_config(disable=True)
img = pipe(image=Image.open(src).convert("RGB"), prompt_embeds=pe, height=1024, width=1024, num_inference_steps=4,
           guidance_scale=1.0, generator=torch.Generator("cpu").manual_seed(seed)).images[0]
img.save(out); print("ok", out, round(time.time() - t), "s")
