# Layout engine v3: pieces with real geometry -> collision-aware tight packing (interlock), pocket ornaments
import math
from PIL import Image, ImageDraw, ImageFilter
from t2 import Word, _split_q, lerp, tail as _tail, sparkle as _sp
SC=0.5; OFF=400; CAN=(1800,2400)   # raster scale/offset for collision masks
class Piece:
    def __init__(s,svg,polys): s.svg=svg; s.polys=polys
    def bbox(s):
        xs=[p[0] for q in s.polys for p in q]; ys=[p[1] for q in s.polys for p in q]; return min(xs),min(ys),max(xs),max(ys)
def word_piece(wd,x,y,w,h=None,rot=0,top=None,bot=None,fill=None,polar=None):
    h=h or w/wd.ar; X0,Y0,X1,Y1=wd.b; top=top or (lambda t:0); bot=bot or (lambda t:0)
    pcx,pcy=x+w/2,y+h/2; ca,sa=math.cos(math.radians(rot)),math.sin(math.radians(rot))
    def base(p):
        u=(p[0]-X0)/(X1-X0); v=(Y1-p[1])/(Y1-Y0)
        if polar:
            qx,qy,R,side=polar; th=(u-0.5)*w/R
            if side=='top': r=R-v*h; return (qx+r*math.sin(th),qy-r*math.cos(th))
            r=R+v*h; return (qx+r*math.sin(th),qy+r*math.cos(th))
        px=x+u*w; yt=y+top(u); yb=y+h+bot(u); py=yt+v*(yb-yt)
        dx,dy=px-pcx,py-pcy; return (pcx+dx*ca-dy*sa, pcy+dx*sa+dy*ca)
    d=[]; polys=[]
    for c,gidx in zip(wd.cs,wd.gi):
        if gidx in wd.bn:
            gx,gy,a,ddy,k=wd.bn[gidx]; c_,s_=math.cos(a),math.sin(a)
            m=(lambda p,gx=gx,gy=gy,c_=c_,s_=s_,ddy=ddy,k=k: base((gx+k*((p[0]-gx)*c_-(p[1]-gy)*s_), gy+k*((p[0]-gx)*s_+(p[1]-gy)*c_)+ddy)))
        else: m=base
        p0=m(c[0][1]); d.append(f"M{p0[0]:.2f},{p0[1]:.2f}"); poly=[p0]
        for seg in c:
            if seg[0]=='L':
                a,b=seg[1],seg[2]; n=max(1,int(math.hypot(b[0]-a[0],b[1]-a[1])/wd.upm*12))
                for i in range(1,n+1): q=m(lerp(a,b,i/n)); d.append(f"L{q[0]:.2f},{q[1]:.2f}"); poly.append(q)
            elif seg[0]=='Q':
                for a,cc,b in _split_q(seg[1],seg[2],seg[3],3):
                    c2,b2=m(cc),m(b); d.append(f"Q{c2[0]:.2f},{c2[1]:.2f} {b2[0]:.2f},{b2[1]:.2f}"); poly.append(b2)
            else:
                _,a,c1,c2,b=seg; q1,q2,q3=m(c1),m(c2),m(b); d.append(f"C{q1[0]:.2f},{q1[1]:.2f} {q2[0]:.2f},{q2[1]:.2f} {q3[0]:.2f},{q3[1]:.2f}"); poly.append(q3)
        d.append('Z'); polys.append(poly)
    f=f' fill="{fill}" stroke="none"' if fill else ''
    return Piece(f'<path d="{"".join(d)}"{f}/>',polys)
def tail_piece(pts,wmax,w0=0,w1=0):
    sv=_tail(pts,wmax,w0,w1); ds=sv.split('"')[1][1:-1].split(' L')
    poly=[tuple(map(float,p.split(','))) for p in ds]; return Piece(sv,[poly])
def sparkle_piece(x,y,r):
    return Piece(_sp(x,y,r),[[(x,y-r),(x+r*.3,y),(x,y+r),(x-r*.3,y)],[(x-r,y),(x,y-r*.3),(x+r,y),(x,y+r*.3)]])
def stroke_piece(x1,y1,x2,y2,w=8):
    dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1; nx,ny=-dy/L*w/2,dx/L*w/2
    return Piece(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#111" stroke-width="{w}" stroke-linecap="round"/>',[[(x1+nx,y1+ny),(x2+nx,y2+ny),(x2-nx,y2-ny),(x1-nx,y1-ny)]])
def rect_piece(x,y,w,h,rot=0,cx=None,cy=None,svg_extra=''):
    cx=cx if cx is not None else x+w/2; cy=cy if cy is not None else y+h/2; a=math.radians(rot)
    pts=[(x,y),(x+w,y),(x+w,y+h),(x,y+h)]; pts=[(cx+(p[0]-cx)*math.cos(a)-(p[1]-cy)*math.sin(a),cy+(p[0]-cx)*math.sin(a)+(p[1]-cy)*math.cos(a)) for p in pts]
    return Piece(f'<path d="M{" L".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)}Z"{svg_extra}/>',[pts])
class Board:
    def __init__(s): s.mask=Image.new('1',(int(CAN[0]*SC),int(CAN[1]*SC)),0); s.pieces=[]
    def _m(s,pieces):
        im=Image.new('1',s.mask.size,0); dr=ImageDraw.Draw(im)
        for p in pieces:
            for q in p.polys:
                if len(q)>2: dr.polygon([((a+OFF)*SC,(b+OFF)*SC) for a,b in q],fill=1)
        return im
    def hits(s,pieces,margin):
        key=(len(s.pieces),margin)
        if getattr(s,"_dk",None)!=key:
            s._dk=key; kk=max(1,int(margin*SC))*2+1; s._dil=s.mask.filter(ImageFilter.MaxFilter(kk)) if margin>0 else s.mask
        from PIL import ImageChops as _IC
        return _IC.logical_and(s._m(pieces),s._dil).getbbox() is not None
        im=s._m(pieces); k=max(1,int(margin*SC))*2+1
        dil=s.mask.filter(ImageFilter.MaxFilter(k)) if margin>0 else s.mask
        from PIL import ImageChops
        return ImageChops.logical_and(im,dil).getbbox() is not None
    def add(s,pieces):
        from PIL import ImageChops
        s.mask=ImageChops.logical_or(s.mask,s._m(pieces)); s.pieces+=pieces
    def drop(s,make,y_lo,y_hi,margin=5,it=14):
        """make(y)->list of pieces; find smallest y in [y_lo,y_hi] with no collision"""
        if not s.pieces: s.add(make(y_lo)); return y_lo
        lo,hi=y_lo,y_hi
        for _ in range(it):
            mid=(lo+hi)/2
            if s.hits(make(mid),margin): lo=mid
            else: hi=mid
        s.add(make(hi)); return hi
    def free_x(s,y0,y1,x_from,direction,limit):
        """distance from x_from moving in direction until ink hit within band [y0,y1]"""
        px=s.mask.load(); W,H=s.mask.size
        for dist in range(0,int(limit),2):
            xx=int((x_from+direction*dist+OFF)*SC)
            if xx<0 or xx>=W: return dist
            for yy in range(int((y0+OFF)*SC),int((y1+OFF)*SC)):
                if 0<=yy<H and px[xx,yy]: return dist
        return limit
    def bbox(s):
        xs=[];ys=[]
        for p in s.pieces:
            b=p.bbox(); xs+=[b[0],b[2]]; ys+=[b[1],b[3]]
        return min(xs),min(ys),max(xs),max(ys)
    def svg(s,size=1000,fill_frac=0.92,stroke=2.5,rot=0):
        x0,y0,x1,y1=s.bbox(); c0=((x0+x1)/2,(y0+y1)/2)
        if rot:
            a=math.radians(rot); ca,sa=math.cos(a),math.sin(a); xs=[];ys=[]
            for p in s.pieces:
                for q in p.polys:
                    for (x,y) in q:
                        xs.append(c0[0]+(x-c0[0])*ca-(y-c0[1])*sa); ys.append(c0[1]+(x-c0[0])*sa+(y-c0[1])*ca)
            x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
        k=min(size*fill_frac/(x1-x0),size*fill_frac/(y1-y0))
        tx=size/2-(x0+x1)/2*k; ty=size/2-(y0+y1)/2*k
        body=''.join(p.svg for p in s.pieces); r=f' rotate({rot} {c0[0]:.1f} {c0[1]:.1f})' if rot else ''
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}"><rect width="{size}" height="{size}" fill="#fff"/>'
                f'<g transform="translate({tx:.1f},{ty:.1f}) scale({k:.4f}){r}" fill="#111" stroke="#111" stroke-width="{stroke}" stroke-linejoin="round" stroke-linecap="round">{body}</g></svg>')
def rot_pts(pts,rot,cx,cy):
    a=math.radians(rot); c,s=math.cos(a),math.sin(a)
    return [(cx+(x-cx)*c-(y-cy)*s, cy+(x-cx)*s+(y-cy)*c) for x,y in pts]
def poly_piece(pts,extra=''):
    return Piece(f'<path d="M{" L".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)}Z"{extra}/>',[pts])
def burst_pieces(x,y,side,n=3,L=40,spread=24,start=0,w=8):
    out=[]
    for i in range(n):
        a=math.radians((i-(n-1)/2)*spread); dx,dy=side*math.cos(a),math.sin(a)
        out.append(stroke_piece(x+dx*start,y+dy*start,x+dx*(start+L),y+dy*(start+L),w))
    return out
def heart_piece(x,y,r,w=6,fill=False):
    from t2 import heart
    sv=heart(x,y,r,fill=fill,w=w); pts=[(x+r*1.1*math.cos(t),y+r*math.sin(t)) for t in [i*math.pi/8 for i in range(16)]]
    return Piece(sv,[pts])
def line_band(board,piece_list):
    xs=[];ys=[]
    for p in piece_list:
        b=p.bbox(); xs+=[b[0],b[2]]; ys+=[b[1],b[3]]
    return min(xs),min(ys),max(xs),max(ys)
def fill_pockets(board,band,block,kind,seed=0,margin=14,cap=56):
    """decorate free space left & right of a line inside block width"""
    x0,y0,x1,y1=band; bl,br=block; cy=(y0+y1)/2; h=y1-y0; out=[]
    for side,inner in ((-1,x0),(1,x1)):
        outer=bl if side<0 else br
        room=abs(inner-outer)
        if room<40: continue
        # actual free distance from text edge outward (respect neighbours)
        free=board.free_x(cy-h*0.25,cy+h*0.25,inner+side*margin,side,room)
        room=min(room,free)
        if room<36: continue
        start=inner+side*margin
        if kind=='burst':
            vc=inner-side*40; LL=min(room*0.6,cap)
            while LL>14:
                bp=burst_pieces(vc,cy,side,n=3,L=LL,spread=22,start=40+margin+4,w=8)
                if not board.hits(bp,4): break
                LL-=6
            else: bp=[]
            out+=bp
        elif kind=='stars':
            r=min(h*0.34,room*0.32,32); out.append(sparkle_piece(start+side*(r+4),cy-h*0.12,r))
            out.append(sparkle_piece(start+side*(r*2.4+6),cy+h*0.22,r*0.5))
        elif kind=='hearts':
            r=min(h*0.24,room*0.26,22); out.append(heart_piece(start+side*(r*1.4),cy,r))
            out.append(sparkle_piece(start+side*(r*3.6),cy-h*0.2,r*0.7))
        elif kind=='lines':
            out.append(stroke_piece(start,cy,start+side*min(room*0.8,120),cy,8))
    board.add(out); return out
