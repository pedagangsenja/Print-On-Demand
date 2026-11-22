import sys, numpy as np, potrace, time
from PIL import Image
src,out=sys.argv[1],sys.argv[2]; t=time.time()
im=Image.open(src).convert('L'); W,H=im.size
a=np.array(im)>=128
bm=potrace.Bitmap(a); plist=bm.trace(turdsize=12,turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,alphamax=1.0,opticurve=True,opttolerance=0.2)
parts=[]
for curve in plist:
    fs=curve.start_point; d=[f"M{fs.x:.2f},{fs.y:.2f}"]
    for seg in curve.segments:
        if seg.is_corner: d.append(f"L{seg.c.x:.2f},{seg.c.y:.2f}L{seg.end_point.x:.2f},{seg.end_point.y:.2f}")
        else: d.append(f"C{seg.c1.x:.2f},{seg.c1.y:.2f} {seg.c2.x:.2f},{seg.c2.y:.2f} {seg.end_point.x:.2f},{seg.end_point.y:.2f}")
    d.append('Z'); parts.append(''.join(d))
open(out,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><path fill="#000" fill-rule="evenodd" d="{"".join(parts)}"/></svg>')
print('paths',len(plist),'secs',round(time.time()-t))
