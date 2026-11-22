import subprocess, sys, json, time, os
subprocess.run([sys.executable,"-m","pip","install","-q","-U","git+https://github.com/huggingface/diffusers","transformers","accelerate"],check=False)
import torch
from diffusers import ZImagePipeline
print("cuda", torch.cuda.is_available(), torch.cuda.device_count(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "")
JOBS=json.loads(open("/kaggle/working/jobs.json").read()) if os.path.exists("/kaggle/working/jobs.json") else JOBS_INLINE
dtype=torch.bfloat16
pipe=ZImagePipeline.from_pretrained("Tongyi-MAI/Z-Image-Turbo",torch_dtype=dtype,low_cpu_mem_usage=True)
pipe.enable_model_cpu_offload()
os.makedirs("/kaggle/working/out",exist_ok=True)
for j in JOBS:
    for seed in j["seeds"]:
        t=time.time()
        img=pipe(prompt=j["prompt"],height=1024,width=1024,num_inference_steps=9,guidance_scale=0.0,generator=torch.Generator("cuda").manual_seed(seed)).images[0]
        fn=f"/kaggle/working/out/{j['id']}_{seed}.png"; img.save(fn); print("saved",fn,round(time.time()-t,1),"s",flush=True)
print("DONE")
