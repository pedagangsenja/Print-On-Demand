"""Jana lettering dengan Qwen-Image-2512 melalui Space Hugging Face rasmi (kuota ZeroGPU percuma).
Guna: python3 qwen_space.py <id...>. 50 langkah, guidance 4.0, seed 42, nisbah 3:4, Prompt Enhance dimatikan."""
import json, shutil, sys, time
from pathlib import Path
from gradio_client import Client

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "qwen2512"; OUT.mkdir(parents=True, exist_ok=True)
P = {p["id"]: p for p in json.loads((HERE / "prompts.json").read_text())}
client = Client("https://qwen-qwen-image-2512.hf.space/", verbose=False)
for pid in sys.argv[1:]:
    if (OUT / f"{pid}.png").exists():
        continue
    t0 = time.time()
    try:
        img, seed = client.predict(P[pid]["prompt"], 42, False, "3:4", 4.0, 50, False, api_name="/infer")
    except Exception as e:  # kuota habis atau Space sibuk: rekod dan teruskan
        print("gagal", pid, str(e)[:300], flush=True)
        continue
    src = img if isinstance(img, str) else (img.get("path") or img.get("value"))
    shutil.copy(src, OUT / f"{pid}.png")
    f = OUT / "times.json"; t = json.loads(f.read_text()) if f.exists() else {}
    t[pid] = {"seconds": round(time.time() - t0, 1), "seed": seed, "note": "masa menunggu Space, bukan CPU"}
    f.write_text(json.dumps(t, indent=1))
    print("qwen2512", pid, t[pid], flush=True)
