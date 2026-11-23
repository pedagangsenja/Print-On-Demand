"""Poster hibrid: teks fon sebenar (SVG, Chromium) + aset AI tanpa teks.
Guna:
  python3 render.py prep            # besarkan aset AI (Real-ESRGAN x4, CPU) -> ai_up/
  python3 render.py <r4a|r5a> [--dpr N]   # DPR 4 = 5400x7200 (18x24 in @300 DPI); DPR 1 = pratonton cepat
Hasil: out/<ID>_hybrid_<w>x<h>.jpg + out/<ID>_hybrid_preview.jpg"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
AI, UP, OUT = HERE / "ai", HERE / "ai_up", HERE / "out"
W, H = 1350, 1800
RNG = np.random.default_rng(42)


def shot(name, dpr, transparent=False):
    """Chromium (Playwright Node) lukis layout/<name>.html; pulangkan imej + data susun atur."""
    import subprocess, tempfile
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "s.png"
        r = subprocess.run(["node", str(HERE / "layout" / "shot.js"), str(HERE / "layout" / f"{name}.html"), str(dpr),
                            "1" if transparent else "0", str(png)], capture_output=True, text=True, check=True,
                           env={**__import__("os").environ, "NODE_PATH": "/opt/node-tools/node_modules"})
        img = Image.open(png); img.load()
    return img, json.loads(r.stdout.strip().splitlines()[-1])


def noise(h, w, sigma=0.0, scale=1):
    """Hingar normal (min 0, sisihan 1), boleh dikasarkan (scale) dan dikaburkan (sigma)."""
    n = RNG.standard_normal((max(1, h // scale), max(1, w // scale))).astype(np.float32)
    if scale > 1 or sigma:
        im = Image.fromarray(np.clip(n * 40 + 128, 0, 255).astype(np.uint8))
        if scale > 1:
            im = im.resize((w, h), Image.BICUBIC)
        if sigma:
            im = im.filter(ImageFilter.GaussianBlur(sigma))
        n = np.asarray(im, np.float32)
    return (n - n.mean()) / (n.std() + 1e-6)


def upscale_x4(img):
    """Real-ESRGAN x4 (ai-forever, BSD-3) melalui spandrel, berjubin supaya muat RAM."""
    import torch
    from huggingface_hub import hf_hub_download
    from spandrel import ModelLoader
    m = ModelLoader().load_from_file(hf_hub_download("ai-forever/Real-ESRGAN", "RealESRGAN_x4.pth")).model.eval()
    torch.set_num_threads(4)
    x = torch.from_numpy(np.asarray(img.convert("RGB"), np.float32) / 255).permute(2, 0, 1)[None]
    _, _, h, w = x.shape
    out, T, P = torch.zeros(1, 3, h * 4, w * 4), 192, 16
    with torch.inference_mode():
        for y in range(0, h, T):
            for x0 in range(0, w, T):
                ya, xa = max(0, y - P), max(0, x0 - P)
                yb, xb = min(h, y + T + P), min(w, x0 + T + P)
                r = m(x[:, :, ya:yb, xa:xb])
                oy, ox = (y - ya) * 4, (x0 - xa) * 4
                th, tw = min(T, h - y) * 4, min(T, w - x0) * 4
                out[:, :, y * 4:y * 4 + th, x0 * 4:x0 * 4 + tw] = r[:, :, oy:oy + th, ox:ox + tw]
    return Image.fromarray((out[0].permute(1, 2, 0).clamp(0, 1).numpy() * 255).round().astype(np.uint8))


def prep():
    """Hiasan emas: besarkan x4, titik hitam ditetapkan 0 (supaya 'screen' tidak tinggalkan kotak), tepi dilembutkan."""
    UP.mkdir(exist_ok=True)
    for f in sorted(AI.glob("gold_*.png")):
        dst = UP / f.name
        if dst.exists():
            continue
        a = np.asarray(upscale_x4(Image.open(f)), np.float32) / 255
        a = np.clip((a - 0.06) / 0.94, 0, 1)
        h, w = a.shape[:2]
        fy = np.clip(np.minimum(np.arange(h), np.arange(h)[::-1]) / (0.06 * h), 0, 1)
        fx = np.clip(np.minimum(np.arange(w), np.arange(w)[::-1]) / (0.06 * w), 0, 1)
        a *= (np.outer(fy, fx) ** 1.5)[..., None]
        Image.fromarray((a * 255).round().astype(np.uint8)).save(dst)
        print("prep", f.name, a.shape, flush=True)


def chalk(fg):
    """Tekstur kapur: tepi kasar + butir + calit menyerong pada alfa lapisan kapur."""
    a = np.asarray(fg.getchannel("A"), np.float32) / 255
    h, w = a.shape
    s = w / 5400
    fine = noise(h, w, sigma=1.6 * s)
    streak = noise(h, w, scale=1)
    st = Image.fromarray(np.clip(streak * 40 + 128, 0, 255).astype(np.uint8))
    st = st.resize((max(1, w // 10), h)).resize((w, h), Image.BICUBIC).rotate(-20, resample=Image.BICUBIC)
    streak = np.asarray(st, np.float32); streak = (streak - streak.mean()) / (streak.std() + 1e-6)
    coarse = noise(h, w, scale=max(1, int(90 * s)))
    ab = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6 * s)), np.float32) / 255
    edge = np.clip((ab - 0.5) * 2.4 + 0.5 + 0.22 * fine, 0, 1)
    grain = np.clip(0.82 + 0.13 * fine + 0.18 * streak + 0.08 * coarse, 0, 1)
    grain[(fine + 0.8 * streak) < -2.1] *= 0.25
    out = np.asarray(fg, np.float32).copy()
    out[..., 3] = edge * grain * 255
    return Image.fromarray(out.round().astype(np.uint8), "RGBA")


def finish(img, name, dpr):
    OUT.mkdir(exist_ok=True)
    w, h = img.size
    if dpr >= 4:
        img.save(OUT / f"{name}_hybrid_{w}x{h}.jpg", quality=92, subsampling=0, dpi=(300, 300))
    img.resize((1350, 1800), Image.LANCZOS).save(OUT / f"{name}_hybrid_preview.jpg", quality=88)
    print("siap", name, img.size, flush=True)


def r4a(dpr):
    img, layout = shot("r4a", dpr)
    a = np.asarray(img.convert("RGB"), np.float32)
    a += noise(*a.shape[:2], sigma=0.7 * dpr / 4)[..., None] * 2.2  # butir halus, elak 'vektor rata'
    finish(Image.fromarray(np.clip(a, 0, 255).round().astype(np.uint8)), "R4a", dpr)
    return layout


def r5a(dpr):
    fg, layout = shot("r5a", dpr, transparent=True)
    w, h = fg.size
    bg = Image.open(AI / "slate_board.png").convert("RGB").resize((w, h), Image.LANCZOS)
    b = np.asarray(bg, np.float32)
    lum = b @ np.array([0.299, 0.587, 0.114], np.float32)
    b = (lum[..., None] * 0.7 + b * 0.3) * np.array([0.80, 0.84, 0.84], np.float32)  # kurangkan biru, gelapkan
    b += noise(h, w, sigma=0.8 * dpr / 4)[..., None] * 5 + noise(h, w, scale=max(1, 6 * dpr))[..., None] * 3
    fg = chalk(fg)
    f = np.asarray(fg, np.float32)
    al = f[..., 3:] / 255
    out = b * (1 - al) + f[..., :3] * al
    finish(Image.fromarray(np.clip(out, 0, 255).round().astype(np.uint8)), "R5a", dpr)
    return layout


if __name__ == "__main__":
    cmd = sys.argv[1]
    dpr = int(sys.argv[sys.argv.index("--dpr") + 1]) if "--dpr" in sys.argv else 4
    if cmd == "prep":
        prep()
    else:
        print(json.dumps({"r4a": r4a, "r5a": r5a}[cmd](dpr)))
