import sys
from PIL import Image
import numpy as np
k=1170/924
def analyse(name,im,thr=90):
    a=np.array(im.convert('L')); ink=a<thr
    ys,xs=np.where(ink)
    if len(xs)==0: return
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max(); ink=ink[y0:y1+1,x0:x1+1]; H,W=ink.shape
    prof=ink.sum(1); on=prof>max(2,0.01*W)
    runs=[];i=0
    while i<H:
        if on[i]:
            j=i
            while j<H and on[j]: j+=1
            runs.append((i,j)); i=j
        else: i+=1
    # merge tiny gaps (<1.5% H)
    m=[]
    for r in runs:
        if m and r[0]-m[-1][1]<=max(1,int(0.012*H)): m[-1]=(m[-1][0],r[1])
        else: m.append(r)
    print(f"\n{name}: block {W}x{H} aspect {W/H:.2f} ink-density {ink.mean():.2f} rows={len(m)}")
    for (a_,b_) in m:
        seg=ink[a_:b_]; cols=np.where(seg.any(0))[0]
        print(f"  y {a_/H:5.2f}-{b_/H:5.2f}  h={(b_-a_)/H:5.2f}H  w={(cols.max()-cols.min())/W:4.2f}W  dens={seg.mean():.2f}")
    gaps=[(m[i+1][0]-m[i][1])/H for i in range(len(m)-1)]
    print("  gaps:",' '.join(f"{g:.3f}" for g in gaps))
src=Image.open(sys.argv[1])
boxes={ # display coords (924 wide)
 'its_fine':(15,1038,238,1228),'drama':(255,1033,447,1232),'hold_on':(12,1235,132,1338),
 'sorry_late':(252,1338,358,1458),'control_freak':(578,1028,688,1132),'keep_talking':(8,828,122,948),
 'love_sleep':(660,833,765,952),'mouth_face':(797,828,912,958),'fresh_daily':(250,692,362,826),'admit_it':(378,692,505,822)}
for n,b in boxes.items():
    c=src.crop(tuple(int(v*k) for v in b)); c.save(f"{sys.argv[2]}/{n}.png"); analyse(n,c)
for p in sys.argv[3:]:
    analyse(p.split('/')[-1],Image.open(p))
