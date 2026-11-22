import time, sys
from kagglesdk import KaggleClient
from kagglesdk.kernels.types.kernels_api_service import ApiGetKernelSessionStatusRequest
c=KaggleClient(); t0=time.time(); last=None
while time.time()-t0<3000:
    r=ApiGetKernelSessionStatusRequest(); r.user_name="abdulazim1411"; r.kernel_slug="pod-typo-gen"
    try:
        s=c.kernels.kernels_api_client.get_kernel_session_status(r); st=str(s.status); fm=getattr(s,'failure_message','')
    except Exception as e: st='ERR '+str(e)[:120]; fm=''
    if st!=last: print(round(time.time()-t0),'s',st,fm,flush=True); last=st
    if any(k in st.upper() for k in ['COMPLETE','ERROR','CANCEL']): break
    time.sleep(30)
