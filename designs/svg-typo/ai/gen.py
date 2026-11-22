import sys, shutil, time, json
from gradio_client import Client
prompt=open(sys.argv[1]).read(); out=sys.argv[2]; seed=int(sys.argv[3]) if len(sys.argv)>3 else 0
# token is a placeholder: the session proxy injects the real HF token into the x-hf-authorization header
c=Client("Qwen/Qwen-Image-2512", token="hf_proxyinjectedplaceholder000000000000", verbose=False)
t=time.time()
res,sd=c.predict(prompt=prompt,seed=seed,randomize_seed=(seed==0),aspect_ratio="1:1",guidance_scale=4.0,num_inference_steps=40,prompt_enhance=False,api_name="/infer")
p=res['path'] if isinstance(res,dict) else res
shutil.copy(p,out); print('ok',out,'seed',sd,'secs',round(time.time()-t))
