# Lettering engine v2: outline text -> warp (envelope) -> SVG path. Coordinates: screen px, y down.
import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
FD=os.environ['FD']; _c={}
def F(spec):
    if spec not in _c:
        n,w,st=(spec.split(':')+['400','normal'])[:3] if spec.count(':')>=1 else (spec,'400','normal')
        if spec.count(':')==1: st='normal'
        f=TTFont(f"{FD}/{n}/files/{n}-latin-{w}-{st}.woff"); _c[spec]=(f.getGlyphSet(),f.getBestCmap(),f['head'].unitsPerEm,f)
    return _c[spec]
def kern_pairs(f):
    return {}
def outline(text,spec,track=0.0):
    """returns list of contours; each contour list of segments in font units (y up), plus advance"""
    gs,cm,upm,f=F(spec); x=0; segs=[]
    for ch in text:
        g=cm.get(ord(ch))
        if g is None: continue
        rp=DecomposingRecordingPen(gs); gs[g].draw(rp)
        segs.append((x,rp.value)); x+=gs[g].width+track*upm
    return segs,x-track*upm,upm
def _quads(p0,pts):
    # expand TrueType implied on-curve points: pts = off..., on
    out=[]; offs=pts[:-1]; last=pts[-1]
    if not offs: return [('L',p0,last)]
    cur=p0
    for i,c in enumerate(offs):
        nxt=last if i==len(offs)-1 else ((c[0]+offs[i+1][0])/2,(c[1]+offs[i+1][1])/2)
        out.append(('Q',cur,c,nxt)); cur=nxt
    return out
def contours(text,spec,track=0.0):
    segs,adv,upm=outline(text,spec,track); cs=[]; global _GI; _GI=[]
    for gi,(gx,val) in enumerate(segs):
        cur=None; start=None; c=[]
        for op,args in val:
            a=[(p[0]+gx,p[1]) if p is not None else None for p in args]
            if op=='qCurveTo' and a[-1] is None:
                offs=a[:-1]; st=((offs[-1][0]+offs[0][0])/2,(offs[-1][1]+offs[0][1])/2)
                c=_quads(st,offs+[st]); cs.append(c); _GI.append(gi); continue
            if op=='moveTo': cur=start=a[0]; c=[]
            elif op=='lineTo': c.append(('L',cur,a[0])); cur=a[0]
            elif op=='qCurveTo':
                c+= _quads(cur,a); cur=a[-1]
            elif op=='curveTo': c.append(('C',cur,a[0],a[1],a[2])); cur=a[2]
            elif op in('closePath','endPath'):
                if cur!=start: c.append(('L',cur,start))
                if c: cs.append(c); _GI.append(gi)
                c=[]
    return cs,adv,upm
def bounds(cs):
    xs=[p[0] for c in cs for s in c for p in s[1:]]; ys=[p[1] for c in cs for s in c for p in s[1:]]
    return min(xs),min(ys),max(xs),max(ys)
def lerp(a,b,t): return (a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
def _split_q(p0,c,p1,n):
    out=[]
    for i in range(n):
        t0,t1=i/n,(i+1)/n
        def B(t): return ((1-t)**2*p0[0]+2*(1-t)*t*c[0]+t*t*p1[0],(1-t)**2*p0[1]+2*(1-t)*t*c[1]+t*t*p1[1])
        def D(t): return (2*(1-t)*(c[0]-p0[0])+2*t*(p1[0]-c[0]),2*(1-t)*(c[1]-p0[1])+2*t*(p1[1]-c[1]))
        a,b=B(t0),B(t1); d=D(t0); h=(t1-t0)/2
        out.append((a,(a[0]+d[0]*h,a[1]+d[1]*h),b))
    return out
class Word:
    """text block: box (x,y,w,h) in px, optional envelope warp functions top(t)/bot(t) as px offsets"""
    def __init__(s,text,spec,track=0.0,skew=0.0):
        s.cs,s.adv,s.upm=contours(text,spec,track); s.gi=list(_GI); s.skew=skew
        s.b=bounds(s.cs); s.ar=(s.b[2]-s.b[0])/(s.b[3]-s.b[1])
        s.bn={}
    def bounce(s,amp=0.03,rot=2.5,seed=1,scale=0.0):
        import random; r=random.Random(seed); n=max(s.gi)+1; H=s.b[3]-s.b[1]
        gb={}
        for c,g in zip(s.cs,s.gi):
            bb=bounds([c]); o=gb.get(g,bb); gb[g]=(min(o[0],bb[0]),min(o[1],bb[1]),max(o[2],bb[2]),max(o[3],bb[3]))
        for g in range(n):
            if g not in gb: continue
            x0,y0,x1,y1=gb[g]; a=math.radians(r.uniform(-rot,rot)); k=1+r.uniform(-scale,scale)
            s.bn[g]=((x0+x1)/2,(y0+y1)/2,a,r.uniform(-amp,amp)*H,k)
        return s
    def place(s,x,y,w,h=None,top=None,bot=None,rot=0,cx=None,cy=None,polar=None):
        h=h or w/s.ar; X0,Y0,X1,Y1=s.b
        top=top or (lambda t:0); bot=bot or (lambda t:0)
        def m(p):
            u=(p[0]-X0)/(X1-X0); v=(Y1-p[1])/(Y1-Y0)   # v=0 top, 1 bottom
            if polar:   # polar=(pcx,pcy,R,'top'|'bottom'); R = radius of text top edge
                pcx,pcy,R,side=polar; th=(u-0.5)*w/R
                if side=='top': r=R-v*h; return (pcx+r*math.sin(th),pcy-r*math.cos(th))
                r=R+v*h; return (pcx+r*math.sin(th),pcy+r*math.cos(th))
            u2=u+s.skew*(1-v)*(Y1-Y0)/(X1-X0)*0  # placeholder
            px=x+u*w + s.skew*(0.5-v)*h
            yt=y+top(u); yb=y+h+bot(u); py=yt+v*(yb-yt)
            return (px,py)
        d=[]; m0=m
        for c,gidx in zip(s.cs,s.gi):
            if gidx in s.bn:
                gx,gy,a,dy,k=s.bn[gidx]; ca,sa=math.cos(a),math.sin(a)
                m=(lambda p,gx=gx,gy=gy,ca=ca,sa=sa,dy=dy,k=k: m0((gx+k*((p[0]-gx)*ca-(p[1]-gy)*sa), gy+k*((p[0]-gx)*sa+(p[1]-gy)*ca)+dy)))
            else: m=m0
            p0=m(c[0][1]); d.append(f"M{p0[0]:.2f},{p0[1]:.2f}")
            for seg in c:
                if seg[0]=='L':
                    a,b=seg[1],seg[2]; L=math.hypot(b[0]-a[0],b[1]-a[1]); n=max(1,int(L/s.upm*12))
                    for i in range(1,n+1):
                        q=m(lerp(a,b,i/n)); d.append(f"L{q[0]:.2f},{q[1]:.2f}")
                elif seg[0]=='Q':
                    for a,cc,b in _split_q(seg[1],seg[2],seg[3],3):
                        c2,b2=m(cc),m(b); d.append(f"Q{c2[0]:.2f},{c2[1]:.2f} {b2[0]:.2f},{b2[1]:.2f}")
                else:
                    _,a,c1,c2,b=seg; q1,q2,q3=m(c1),m(c2),m(b); d.append(f"C{q1[0]:.2f},{q1[1]:.2f} {q2[0]:.2f},{q2[1]:.2f} {q3[0]:.2f},{q3[1]:.2f}")
            d.append('Z')
        s.box=(x,y,w,h); s.d=''.join(d)
        r=f' transform="rotate({rot} {cx if cx is not None else x+w/2} {cy if cy is not None else y+h/2})"' if rot else ''
        return f'<path d="{s.d}"{r}/>'
def arch(b):   return lambda t: -b*(1-(2*t-1)**2)        # positive b bends up (arc)
def smile(b):  return lambda t:  b*(1-(2*t-1)**2)
def circ(R,W,up=True):  # true circular arc offset over width W
    def f(t):
        x=(t-0.5)*W; d=R-math.sqrt(max(R*R-x*x,0)); return d if up else -d
    return f
def sparkle(x,y,r,k=0.16):
    d=f"M{x},{y-r} Q{x+r*k},{y-r*k} {x+r},{y} Q{x+r*k},{y+r*k} {x},{y+r} Q{x-r*k},{y+r*k} {x-r},{y} Q{x-r*k},{y-r*k} {x},{y-r}Z"
    return f'<path d="{d}"/>'
def tail(pts,wmax,w0=0.0,w1=0.0,n=80):
    """tapered brush stroke along cubic bezier pts=[p0,p1,p2,p3]; width profile w0->wmax->w1"""
    p0,p1,p2,p3=pts
    def B(t): return tuple((1-t)**3*p0[i]+3*(1-t)**2*t*p1[i]+3*(1-t)*t*t*p2[i]+t**3*p3[i] for i in range(2))
    L=[];R=[]
    for i in range(n+1):
        t=i/n; a=B(max(t-1e-3,0)); b=B(min(t+1e-3,1)); dx,dy=b[0]-a[0],b[1]-a[1]; l=math.hypot(dx,dy) or 1
        nx,ny=-dy/l,dx/l
        prof=math.sin(math.pi*t)**0.9; base=w0*(1-t)+w1*t; w=(base+(wmax-base)*prof)/2
        p=B(t); L.append((p[0]+nx*w,p[1]+ny*w)); R.append((p[0]-nx*w,p[1]-ny*w))
    pts=L+R[::-1]
    return '<path d="M'+' L'.join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)+'Z"/>'
def bar(x,y,w,h): return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}"/>'
def svg(body,W=1000,H=1000,bg='#fff',fg='#111',extra=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{bg}"/>{extra}<g fill="{fg}">{body}</g></svg>'

def burst(x,y,side,n=3,L=46,spread=28,gap=0,w=8):
    """radiating short strokes; side=-1 left, 1 right"""
    out=[]
    for i in range(n):
        a=math.radians((i-(n-1)/2)*spread); dx,dy=side*math.cos(a),math.sin(a)
        x1,y1=x+dx*gap,y+dy*gap; x2,y2=x1+dx*L,y1+dy*L
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#111" stroke-width="{w}" stroke-linecap="round"/>')
    return ''.join(out)
def heart(x,y,r,fill=False,w=6):
    d=f"M{x},{y+r*0.9} C{x-r*1.6},{y-r*0.1} {x-r*0.7},{y-r*1.3} {x},{y-r*0.35} C{x+r*0.7},{y-r*1.3} {x+r*1.6},{y-r*0.1} {x},{y+r*0.9}Z"
    return f'<path d="{d}"/>' if fill else f'<path d="{d}" fill="none" stroke="#111" stroke-width="{w}" stroke-linejoin="round"/>'
def ribbon(cx,cy,w,h,tail=34,notch=14,lift=10):
    """banner: centre band + folded tails"""
    x0,x1,y0,y1=cx-w/2,cx+w/2,cy-h/2,cy+h/2
    t=f'<path d="M{x0-tail},{y0+lift} L{x0+4},{y0+lift} L{x0+4},{y1+lift} L{x0-tail},{y1+lift} L{x0-tail+notch},{(y0+y1)/2+lift}Z"/>'
    t+=f'<path d="M{x1+tail},{y0+lift} L{x1-4},{y0+lift} L{x1-4},{y1+lift} L{x1+tail},{y1+lift} L{x1+tail-notch},{(y0+y1)/2+lift}Z"/>'
    fold=f'<path d="M{x0+4},{y1} L{x0+4},{y1+lift} L{x0+18},{y1}Z" fill="#fff"/><path d="M{x1-4},{y1} L{x1-4},{y1+lift} L{x1-18},{y1}Z" fill="#fff"/>'
    return t+f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="4" stroke="#fff" stroke-width="5"/>'+fold
