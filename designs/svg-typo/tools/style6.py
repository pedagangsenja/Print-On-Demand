# Calibrated style (matched against reference "IT'S FiNE" replica): uniform cap height, one stroke weight,
# rounded condensed caps + emboldened monoline script, thin-line ornaments in the side pockets.
import sys; sys.path.insert(0,sys.argv[1]); from lay4 import *
OUT=sys.argv[2]; CAPS='fredoka-c75:700'; SCR='cookie'; VS=1.3; SY=1.15; BW=800; SHEAR=-0.14
from PIL import Image, ImageDraw, ImageFilter, ImageChops
def build(rows,name,tilt=0,scr=SCR,sy=SY,small=0.68):
    L=L4(BW=BW,caps=CAPS,scr=scr,rs=0)
    ws={r['t']:W(r['t'].replace('i','ı'),CAPS,0.0 if r['k']=='caps' else 0.06,caps=True) for r in rows if r['k']!='script'}
    H=min([0.94*BW*VS/ws[r['t']].ar/0.88 for r in rows if r['k']=='caps']+[180])
    for r in rows:
        if r['k']=='caps' and 's' not in r: r['s']=max(0.88,min(1.22,0.94*BW*VS/ws[r['t']].ar/H))
    T=None; info=[]; prev=None
    for r in rows:
        k=r['k']; xo=r.get('xo',0)*BW; rot=r.get('rot',0)
        if k=='ribbon':
            L.M=0.40*T; i=L.ribbon(r['t'],h=H*0.50,pad=H*0.2,tail=H*0.26,track=0.06); info.append((r,i,None,0,0,H*0.5)); prev=k; continue
        if k in('caps','small'):
            wd=ws[r['t']]; h=H*(r.get('s',1.0) if k=='caps' else small); w=h*wd.ar/VS
            t=thick(wp(wd,0,0,w,h))
            if T is None: T=t/(h/H)+1.5
            sw=max(1.5,min(T-t,0.20*T if k=='caps' else 0.16*T)); L.M=0.34*T+sw/2
            mk=lambda xx:(lambda y:[wp(wd,xx,y,w,h,sw=sw,rot=rot)])
            x=cx-w/2+xo
            if prev=='script' and w<0.8*BW and 'xo' not in r:
                best=None
                for f in (0,-0.05,0.05,-0.1,0.1,-0.15,0.15,-0.2,0.2):
                    xx=cx-w/2+f*BW
                    if xx<cx-BW*0.52 or xx+w>cx+BW*0.52: continue
                    yy=L.find(mk(xx))+abs(f)*BW*0.25
                    if best is None or yy<best[0]-1: best=(yy,xx)
                x=best[1]
            i=L.drop(mk(x)); info.append((r,i,wd,x,w,h)); prev=k
        else:
            sd=W(r['t'],scr,shear=SHEAR); w=BW*r.get('f',1.0); h=w/sd.ar*sy; x=cx-w/2+xo
            ssw=max(0,min(0.90*T,0.25*w/len(r['t']))-thick(wp(sd,x,0,w,h))); L.M=0.26*T+ssw/2
            i=L.drop(lambda y:[wp(sd,x,y,w,h,sw=ssw,rot=rot if rot else -2)]); info.append((r,i,sd,x,w,h))
            if r.get('swash'):
                a,b=r['swash']; bx0,by0,bx1,by1=L.bands[i]; base=by0+h*sd.b[3]/(sd.b[3]-sd.b[1])
                for dy in range(int(T*0.5),200,4):
                    yy=base+dy; tp=[(x+w*a,yy+4),(x+w*(a+(b-a)*0.3),yy+h*0.035),(x+w*(a+(b-a)*0.7),yy+h*0.02),(x+w*b,yy-h*0.03)]
                    p=tail_piece(rot_pts(tp,-2,x+w/2,by0+h/2),T*0.62,T*0.2,T*0.15)
                    if not L.bd.hits([p],T*0.3): break
                L.bd.add([p])
            prev=k
    ow=0.42*T; x0,_,x1,_=L.bd.bbox(); blk=(min(x0,cx-BW*0.46),max(x1,cx+BW*0.46))
    for r,i,wd,x,w,h in info:   # heart dots
        if r['k'] in('caps','small') and 'i' in r['t']:
            for ci,ch in enumerate(r['t']):
                if ch=='i': L.bd.add([heart_solid(gx(wd,x,w,ci),L.bands[i][1]+h*0.105,h*0.105)])
    def put(ps):
        if ps and not L.bd.hits(ps,ow*0.9): L.bd.add(ps); return True
        return False
    for r,i,wd,x,w,h in info:
        o=r.get('orn'); 
        if not o: continue
        bx0,by0,bx1,by1=L.bands[i]; my=(by0+by1)/2; hh=by1-by0
        for side,edge,lim in((-1,bx0,blk[0]),(1,bx1,blk[1])):
            room=abs(lim-edge)+0.25*H
            if o=='rays': put(rays3(edge-side*0.28*H,by0+hh*0.42,180 if side<0 else 0,0.30*H,ow,spread=30,r0=0.28*H+ow*2.4,lens=(0.8,1,0.8)))
            elif o=='rays_up': put(rays3(edge-side*0.1*H,by0+0.2*hh,(205 if side<0 else -25),0.34*H,ow,spread=25,r0=0.34*H))
            elif o=='hearts': put([heart_line(edge+side*(0.30*H+ow),my,0.19*H,ow,rot=side*16)])
            elif o=='stars':
                put([sparkle_piece(edge+side*(0.26*H+ow),my,0.2*H)]); put([sparkle_piece(edge+side*(0.56*H+ow),my-0.18*hh,0.09*H)])
            elif o=='star5':
                put([star5_piece(edge+side*(0.27*H+ow),my,0.2*H,rot=-90+side*8)]); put([sparkle_piece(edge+side*(0.62*H+ow),my+0.12*hh,0.10*H)])
            elif o=='lines': put([stroke_piece(edge+side*ow*2.2,my,lim,my,ow)])
            elif o=='starline':
                r5=min(0.2*H,hh*0.42); sxp=edge+side*(r5+ow*1.6)
                put([star5_piece(sxp,my,r5,rot=-90+side*8)])
                if abs(lim-sxp)>r5+ow*5: put([stroke_piece(sxp+side*(r5+ow*1.8),my,lim,my,ow)])
            elif o=='arrows':
                rm=abs(lim-edge)-ow*3; a0=edge+side*ow*2.4
                if rm>0.5*H:
                    put(arrow(a0+side*rm,my-0.30*hh,a0,my-0.14*hh,ow)); put(arrow(a0+side*0.05*H,my+0.22*hh,a0+side*rm*0.8,my+0.34*hh,ow,fl=0))
                elif rm>0.22*H: put([heart_line(edge+side*(rm*0.5+ow*2),my,min(0.19*H,rm*0.42),ow,rot=side*16)])
            elif o=='hearts2':
                put([heart_solid(edge+side*(0.22*H+ow),my+0.1*hh,0.1*H,rot=side*12)]); put([sparkle_piece(edge+side*(0.50*H+ow),my-0.15*hh,0.12*H)])
    def biggest_hole():
        x0,y0,x1,y1=L.bd.bbox(); m=L.bd.mask; W_,H_=m.size
        dom=Image.new('1',m.size,0); ImageDraw.Draw(dom).rectangle([(x0+OFF)*SC,(y0+OFF)*SC,(x1+OFF)*SC,(y1+OFF)*SC],fill=1)
        free=ImageChops.logical_and(dom,ImageChops.invert(m)).convert('L'); n=0; last=free
        while n<90:
            nx=free.filter(ImageFilter.MinFilter(3))
            if nx.getbbox() is None: break
            last=nx; free=nx; n+=1
        import numpy as np
        ys,xs=np.nonzero(np.array(last))
        if len(xs)==0: return 0,(0,0)
        j=int(np.argmin(np.abs(xs-((x0+x1)/2+OFF)*SC)*0+ys*1000+xs)); px,py=float(xs[j]),float(ys[j])
        return n/SC,(px/SC-OFF,py/SC-OFF)
    kinds=0; placed=0
    while placed<12:
        rad,(px,py)=biggest_hole()
        if rad<0.36*H: break
        r_=min(rad*0.62,0.26*H)
        def mkorn(x,y,kind):
            if kind%3==0: return [sparkle_piece(x,y,r_)]
            if kind%3==1: return [heart_line(x,y,r_*0.78,ow,rot=12 if x>cx else -12)]
            return [star5_piece(x,y,r_*0.9,rot=-90+(8 if x>cx else -8))]
        if not put(mkorn(px,py,kinds)): L.bd.add([dot_piece(px,py,ow*0.9)])
        placed+=1
        mxp=2*cx-px
        if abs(mxp-px)>2.2*r_ and put(mkorn(mxp,py,kinds)): placed+=1
        kinds+=1
    L.hole=biggest_hole()[0]/H
    return L,T,H,info
def save(L,name,tilt=0): open(f"{OUT}/{name}.svg",'w').write(L.bd.svg(stroke=0,rot=tilt))
def metrics(L):
    import numpy as np
    x0,y0,x1,y1=L.bd.bbox(); m=np.array(L.bd.mask.convert('L'))>0
    ys,xs=np.nonzero(m); cxm=xs.mean()/SC-OFF; box=m[int((y0+OFF)*SC):int((y1+OFF)*SC),int((x0+OFF)*SC):int((x1+OFF)*SC)]
    return dict(aspect=round((x1-x0)/(y1-y0),2),ink=round(float(box.mean()),2),lr_off=round((cxm-(x0+x1)/2)/(x1-x0),3),hole=round(L.hole,2))
if __name__=='__main__':
    D={
    'f1':[dict(t="I'M NOT",k='caps',orn='rays'),dict(t="ANTiSOCiAL.",k='caps'),dict(t="I'M JUST",k='ribbon',orn='starline'),
          dict(t="Selectively",k='script',f=1.0,swash=(0.08,0.70)),dict(t="SOCiAL",k='caps',orn='arrows')],
    'f2':[dict(t="DON'T TALK",k='caps'),dict(t="TO ME",k='small',orn='starline'),dict(t="BEFORE MY",k='caps'),
          dict(t="Coffee",k='script',f=0.80,orn='hearts')],
    'f3':[dict(t="I'M SiLENTLY",k='caps'),dict(t="Correcting",k='script',f=1.0,swash=(0.05,0.60)),
          dict(t="YOUR",k='small',orn='starline'),dict(t="GRAMMAR",k='caps')],
    'f4':[dict(t="MENTALLY",k='caps'),dict(t="ON",k='small',orn='starline'),dict(t="Vacation",k='script',f=0.92,swash=(0.22,0.95)),
          dict(t="PHYSiCALLY",k='small',orn='starline'),dict(t="AT WORK",k='caps',orn='arrows')]}
    for n,rows in D.items():
        L,T,H,_=build(rows,n); save(L,n); print(n,metrics(L))
