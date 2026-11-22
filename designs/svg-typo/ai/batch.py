"""Batch local generation (FLUX.2 klein 4B, CPU). Builds prompts from layout templates.
usage: python3 batch.py quotes.json out_dir [seeds=3] [only_id]
Encodes all prompts first, then loads the transformer once (fits ~15 GB RAM)."""
import sys, json, time, gc, pathlib, torch
from diffusers import Flux2KleinPipeline
REPO = "black-forest-labs/FLUX.2-klein-4B"; dt = torch.bfloat16
LAYOUT = {
 "stack": "the words stacked into one compact square lockup",
 "circle": "the words arranged inside one round circular composition, top line curved along the top edge and bottom line curved along the bottom edge",
 "banner": "the words stacked into one compact square lockup with one black ribbon banner across the middle",
 "box": "the words stacked into one compact tall rectangular lockup with thin horizontal rules between some lines",
}
def prompt(q):
    lines = "\n".join(f'"{t}" ({s})' for t, s in q["lines"])
    return ("Black ink vector typography quote design for a t-shirt SVG cut file, on a plain pure white background. "
            "No frame, no border, no outline box around the design.\nThe text reads exactly, top to bottom:\n" + lines +
            f"\nLayout: {LAYOUT[q['layout']]}. Professional hand-lettered sarcastic SVG bundle style: strong size contrast "
            "between words, mix of condensed sans capitals, bold brush script and tiny connector words, every word locked "
            "tightly together with almost no gaps, filling the shape densely. Small decorations hugging the letters: tiny "
            "four-point sparkles, short dash burst lines, small stars, little swashes. Solid black only, crisp clean edges, "
            "no gray, no shading, no texture, no mockup, no extra words, correct spelling.")
qs = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 3
if len(sys.argv) > 4: qs = [q for q in qs if q["id"] == sys.argv[4]]
torch.set_num_threads(4); t = time.time()
te = Flux2KleinPipeline.from_pretrained(REPO, transformer=None, vae=None, torch_dtype=dt)
with torch.no_grad(): embs = {q["id"]: te.encode_prompt(prompt(q), device="cpu")[0] for q in qs}
del te; gc.collect()
pipe = Flux2KleinPipeline.from_pretrained(REPO, text_encoder=None, tokenizer=None, torch_dtype=dt)
pipe.set_progress_bar_config(disable=True)
for q in qs:
    (out / f"{q['id']}.prompt.txt").write_text(prompt(q))
    for s in range(1, seeds + 1):
        img = pipe(prompt_embeds=embs[q["id"]], height=1024, width=1024, num_inference_steps=4, guidance_scale=1.0,
                   generator=torch.Generator("cpu").manual_seed(s)).images[0]
        img.save(out / f"{q['id']}_s{s}.png"); print("ok", q["id"], s, round(time.time() - t), flush=True)
