"""Free, no-signup generation via AI Horde (aihorde.net, anonymous key).
usage: python3 horde_gen.py prompt.txt out.png [model] [steps] [cfg]
Note: anonymous prompts/outputs are shared with LAION by AI Horde (ToS)."""
import sys, time, json, base64, io, urllib.request
from PIL import Image
API = "https://aihorde.net/api/v2"; KEY = "0000000000"
prompt = open(sys.argv[1]).read().strip(); out = sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "Qwen-Image_fp8"
steps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
cfg = float(sys.argv[5]) if len(sys.argv) > 5 else 2.5
def call(path, data=None):
    req = urllib.request.Request(API + path, data=json.dumps(data).encode() if data else None,
        headers={"apikey": KEY, "Content-Type": "application/json", "Client-Agent": "pod-typo:1.0:anon", "User-Agent": "pod-typo/1.0"},
        method="POST" if data else "GET")
    return json.load(urllib.request.urlopen(req, timeout=60))
job = call("/generate/async", {"prompt": prompt, "models": [model], "r2": False, "nsfw": False,
    "params": {"width": 1024, "height": 1024, "steps": steps, "cfg_scale": cfg, "sampler_name": "k_euler", "karras": False, "n": 1}})
jid = job["id"]; print("job", jid, job.get("kudos"), job.get("message", ""), flush=True); t = time.time()
while True:
    s = call(f"/generate/check/{jid}")
    if s.get("done") or s.get("faulted") or not s.get("is_possible", True): break
    print("wait", s.get("queue_position"), s.get("wait_time"), flush=True); time.sleep(15)
r = call(f"/generate/status/{jid}")
g = r["generations"][0]
Image.open(io.BytesIO(base64.b64decode(g["img"]))).save(out)
print("ok", out, "model", g["model"], "worker", g["worker_name"], "secs", round(time.time() - t))
