import math
from t4 import *
cx=500
class L4:
    def __init__(s,BW=800,M=10,caps='londrina-solid:900',scr='pacifico',rs=3,scr_sw=2,sx=1.0):
        s.bd=Board(); s.BW=BW; s.M=M; s.CAPS=caps; s.SCR=scr; s.rs=rs; s.scr_sw=scr_sw; s.sx=sx; s.bands=[]; s.blk=(cx-BW/2,cx+BW/2)
    def find(s,make,extra=300):
        bd=s.bd
        if not bd.pieces: return 0
        x0,y0,x1,y1=bd.bbox(); lo,hi=y0,y1+extra
        for _ in range(15):
            mid=(lo+hi)/2
            if bd.hits(make(mid),s.M): lo=mid
            else: hi=mid
        return hi
    def drop(s,make,extra=300,at=None):
        bd=s.bd; ps=make(s.find(make,extra) if at is None else at)
        bd.add(ps); s.bands.append(line_band(bd,ps)); return len(s.bands)-1
    def caps(s,text,frac=1.0,vs=1.0,hmax=None,top=flat,bot=flat,xo=0,rot=0,track=0.0,sw=None,font=None,h=None,at=None,probe=False):
        wd=W(text,font or s.CAPS,track,caps=True); w=s.BW*frac; h=h or w/wd.ar*vs
        if hmax and h>hmax: h=hmax; w=h*wd.ar/vs
        x=cx-w/2+xo; b0=s.blk[0]; BW=s.BW
        tf=lambda u: top((x+u*w-b0)/BW); bf=lambda u: bot((x+u*w-b0)/BW)
        mk=lambda y:[wp(wd,x,y,w,h,sw=sw if sw is not None else s.rs,rot=rot,top=tf,bot=bf)]
        if probe: return s.find(mk)
        return s.drop(mk,at=at)
    def script(s,text,frac=1.0,rot=-4,xo=0,swash=None,sw=None,font=None,sx=None):
        wd=W(text,font or s.SCR); w=s.BW*frac; h=w/wd.ar/(sx or s.sx); x=cx-w/2+xo
        i=s.drop(lambda y:[wp(wd,x,y,w,h,sw=sw if sw is not None else s.scr_sw,rot=rot)])
        if swash:
            a,b,thick=swash; bx0,by0,bx1,by1=s.bands[i]; base=by0+h*wd.b[3]/(wd.b[3]-wd.b[1]); L=x
            for dy in range(8,140,4):
                yy=base+dy
                tp=[(L+w*a,yy),(L+w*(a+(b-a)*0.3),yy+h*0.07),(L+w*(a+(b-a)*0.7),yy+h*0.05),(L+w*b,yy-h*0.05)]
                p=tail_piece(rot_pts(tp,rot,x+w/2,by0+h/2),thick,2,1)
                if not s.bd.hits([p],5): break
            s.bd.add([p]); s.bands[i]=line_band(s.bd,[s.bd.pieces[-2],p])
        return i
    def ribbon(s,text,h=44,rot=0,xo=0,track=0.05,pad=30,tail=34):
        wd=W(text,s.CAPS,track,caps=True); w=h*wd.ar; band=w+2*pad; bh=h*1.62
        def mk(y):
            ccx,ccy=cx+xo,y+bh/2; x0,x1,y0,y1=ccx-band/2,ccx+band/2,y,y+bh; n=tail*0.42; Lf=bh*0.16
            P=lambda pts: poly_piece(rot_pts(pts,rot,ccx,ccy))
            return [P([(x0-tail,y0+Lf),(x0+3,y0+Lf),(x0+3,y1+Lf),(x0-tail,y1+Lf),(x0-tail+n,(y0+y1)/2+Lf)]),
                    P([(x1+tail,y0+Lf),(x1-3,y0+Lf),(x1-3,y1+Lf),(x1+tail,y1+Lf),(x1+tail-n,(y0+y1)/2+Lf)]),
                    poly_piece(rot_pts([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],rot,ccx,ccy),' stroke="#fff" stroke-width="5"'),
                    wp(wd,ccx-w/2,ccy-h/2,w,h,sw=1.5,fill='#fff',rot=rot)]
        return s.drop(mk)
    def pockets(s,i,kind,blk=None,**kw): return fill_pockets(s.bd,s.bands[i],blk or s.blk,kind,**kw)
    def svg(s,**kw): return s.bd.svg(stroke=s.rs,**kw)
def icon_piece(svg,x0,y0,x1,y1): return Piece(svg,[[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]])
