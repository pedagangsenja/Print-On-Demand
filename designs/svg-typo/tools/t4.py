# v4: HarfBuzz-shaped text (kerning + ligatures), cap-height envelopes, no jitter
import io, math, os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from t2 import _quads, bounds
from t3 import *
FD=os.environ['FD']; _fc={}
def font(spec):
    if spec not in _fc:
        p=spec.split(':'); n=p[0]; w=p[1] if len(p)>1 else '400'; st=p[2] if len(p)>2 else 'normal'
        tt=TTFont(f"{FD}/{n}/files/{n}-latin-{w}-{st}.woff"); tt.flavor=None; b=io.BytesIO(); tt.save(b)
        hf=hb.Font(hb.Face(b.getvalue())); gs=tt.getGlyphSet(); cm=tt.getBestCmap()
        try: cap=tt['OS/2'].sCapHeight
        except Exception: cap=0
        if not cap:
            from fontTools.pens.boundsPen import BoundsPen
            bp=BoundsPen(gs); gs[cm[ord('H')]].draw(bp); cap=bp.bounds[3]
        _fc[spec]=(tt,gs,hf,tt['head'].unitsPerEm,cap)
    return _fc[spec]
class W:
    def __init__(s,text,spec,track=0.0,caps=False,shear=0.0):
        tt,gs,hf,upm,cap=font(spec); buf=hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(hf,buf,{"kern":True,"liga":True,"calt":True})
        x=0; s.cs=[]; s.gi=[]; s.bn={}; s.upm=upm; s.pos=[]; s.text=text
        for gi,(info,pos) in enumerate(zip(buf.glyph_infos,buf.glyph_positions)):
            g=tt.getGlyphName(info.codepoint); rp=DecomposingRecordingPen(gs); gs[g].draw(rp)
            ox,oy=x+pos.x_offset,pos.y_offset; cur=start=None; c=[]; s.pos.append((info.cluster,x,pos.x_advance))
            for op,args in rp.value:
                a=[(p[0]+ox,p[1]+oy) if p is not None else None for p in args]
                if op=='qCurveTo' and a[-1] is None:
                    offs=a[:-1]; st=((offs[-1][0]+offs[0][0])/2,(offs[-1][1]+offs[0][1])/2)
                    s.cs.append(_quads(st,offs+[st])); s.gi.append(gi); continue
                if op=='moveTo': cur=start=a[0]; c=[]
                elif op=='lineTo': c.append(('L',cur,a[0])); cur=a[0]
                elif op=='qCurveTo': c+=_quads(cur,a); cur=a[-1]
                elif op=='curveTo': c.append(('C',cur,a[0],a[1],a[2])); cur=a[2]
                elif op in('closePath','endPath'):
                    if cur!=start: c.append(('L',cur,start))
                    if c: s.cs.append(c); s.gi.append(gi)
                    c=[]
            x+=pos.x_advance+track*upm
        if shear:
            s.cs=[[tuple([sg[0]]+[(q[0]+shear*q[1],q[1]) for q in sg[1:]]) for sg in c] for c in s.cs]
        b=bounds(s.cs); s.ink=b
        s.b=(b[0],0,b[2],cap) if caps else b
        s.ar=(s.b[2]-s.b[0])/(s.b[3]-s.b[1])
def wp(wd,x,y,w,h,sw=None,fill=None,**kw):
    p=word_piece(wd,x,y,w,h,**kw)
    att=''
    if fill: att+=f' fill="{fill}" stroke="{fill}"'
    if sw is not None: att+=f' stroke-width="{sw:.1f}"'
    p.svg=p.svg.replace('<path d=','<path'+att+' d=',1); return p
# ---- ornaments
def star5_piece(x,y,r,rot=-90):
    pts=[]
    for i in range(10):
        rr=r if i%2==0 else r*0.45; a=math.radians(rot+i*36); pts.append((x+rr*math.cos(a),y+rr*math.sin(a)))
    return poly_piece(pts)
def aster_piece(x,y,r,w=6):
    out=[]
    for i in range(4):
        a=i*math.pi/4; dx,dy=r*math.cos(a),r*math.sin(a); out.append(stroke_piece(x-dx,y-dy,x+dx,y+dy,w))
    return out
def dot_piece(x,y,r): return Piece(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>',[[(x+r*math.cos(i*math.pi/4),y+r*math.sin(i*math.pi/4)) for i in range(8)]])
def rays(x,y,side,L=44,w=9,r0=0,ang=(-26,0,26),lens=(0.72,1,0.72),tilt=0):
    out=[]
    for a,l in zip(ang,lens):
        t=math.radians(a+tilt); dx,dy=side*math.cos(t),math.sin(t)
        out.append(stroke_piece(x+dx*r0,y+dy*r0,x+dx*(r0+L*l),y+dy*(r0+L*l),w))
    return out
arch=lambda a: (lambda t: -a*(1-(2*t-1)**2))
smile=lambda a: (lambda t: a*(1-(2*t-1)**2))
flat=lambda t: 0.0
slope=lambda d: (lambda t: d*(t-0.5))

def thick(piece):
    """approx stroke thickness of a monoline shape: 2*area/perimeter"""
    A=0;P=0
    for q in piece.polys:
        n=len(q)
        for i in range(n):
            x1,y1=q[i]; x2,y2=q[(i+1)%n]; A+=x1*y2-x2*y1; P+=math.hypot(x2-x1,y2-y1)
    return abs(A)/max(P,1)
def gx(wd,x,w,ci):
    """px centre-x of glyph for character index ci"""
    for cl,g0,adv in wd.pos:
        if cl==ci: return x+((g0+adv/2)-wd.b[0])/(wd.b[2]-wd.b[0])*w
def heart_solid(x,y,r,rot=0):
    pts=[]
    for i in range(40):
        t=2*math.pi*i/40; px=16*math.sin(t)**3; py=-(13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t))
        pts.append((x+px*r/16,y+py*r/16))
    return poly_piece(rot_pts(pts,rot,x,y))
def heart_line(x,y,r,w,rot=0):
    p=heart_solid(x,y,r,rot); p.svg=p.svg.replace('<path ','<path fill="none" stroke-width="%.1f" '%w,1); return p
def arrow(x1,y1,x2,y2,w,head=None,fl=3):
    """shaft from tail (x1,y1) to tip (x2,y2), solid head at tip, fletching at tail"""
    L=math.hypot(x2-x1,y2-y1); ux,uy=(x2-x1)/L,(y2-y1)/L; nx,ny=-uy,ux; hd=head or w*3.2
    out=[stroke_piece(x1,y1,x2-ux*hd*0.6,y2-uy*hd*0.6,w)]
    out.append(poly_piece([(x2,y2),(x2-ux*hd+nx*hd*0.62,y2-uy*hd+ny*hd*0.62),(x2-ux*hd*0.72,y2-uy*hd*0.72),(x2-ux*hd-nx*hd*0.62,y2-uy*hd-ny*hd*0.62)]))
    for i in range(fl):
        bx,by=x1+ux*(i*w*2.3),y1+uy*(i*w*2.3)
        for sgn in (-1,1):
            out.append(stroke_piece(bx,by,bx-ux*w*2.2+sgn*nx*w*2.4,by-uy*w*2.2+sgn*ny*w*2.4,w*0.9))
    return out
def rays3(x,y,ang,L,w,spread=26,r0=0,lens=(0.75,1,0.75)):
    out=[]
    for k,l in zip((-1,0,1),lens):
        t=math.radians(ang+k*spread); dx,dy=math.cos(t),math.sin(t)
        out.append(stroke_piece(x+dx*r0,y+dy*r0,x+dx*(r0+L*l),y+dy*(r0+L*l),w))
    return out
