# Futurama-toy Enterprise - scripted parametric build. blender -b -P build.py -- ROUND [views...]
import bpy, bmesh, math, sys, os, json
from mathutils import Vector, Matrix
HERE='/workspace/ships/enterprise-futurama'
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ROUND=argv[0] if argv else 'r1'; VIEWS=argv[1:]
P=json.load(open(f'{HERE}/params.json'))
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
col=bpy.data.collections.new('Ship'); scene.collection.children.link(col)

def srgb(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return [(v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4) for v in c]+[1]
def mat(name,hexc,rough):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=srgb(hexc); b.inputs['Roughness'].default_value=rough
    b.inputs['Coat Weight'].default_value=0.35; b.inputs['Coat Roughness'].default_value=0.12
    m.diffuse_color=srgb(hexc)
    return m
M={k:mat(k,v[0],v[1]) for k,v in P['colors'].items()}
g=bpy.data.materials.new('glass'); g.use_nodes=True; b=g.node_tree.nodes['Principled BSDF']
b.inputs['Transmission Weight'].default_value=1.0; b.inputs['Roughness'].default_value=0.02; b.inputs['IOR'].default_value=1.45
b.inputs['Base Color'].default_value=(0.97,0.98,1,1); g.diffuse_color=(0.9,0.95,1,0.3); M['glass']=g

def new_obj(name,bm,m,smooth=True,sub=0,parent=None):
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons: p.use_smooth=True
    me.materials.append(M[m]); o=bpy.data.objects.new(name,me); col.objects.link(o)
    if sub:
        md=o.modifiers.new('sub','SUBSURF'); md.levels=sub; md.render_levels=sub
    return o

def lathe(name,prof,m,seg=96,axis='Z',origin=(0,0,0),cap=True,sub=0):
    """prof: list of (h along axis, r). Revolve."""
    bm=bmesh.new(); rings=[]
    for h,r in prof:
        ring=[]
        if r<1e-6:
            rings.append([bm.verts.new(_ax(axis,h,0,0,origin))]); continue
        for i in range(seg):
            a=2*math.pi*i/seg; ring.append(bm.verts.new(_ax(axis,h,r*math.cos(a),r*math.sin(a),origin)))
        rings.append(ring)
    for A,B in zip(rings,rings[1:]):
        if len(A)==1 and len(B)==1: continue
        if len(A)==1:
            for i in range(seg): bm.faces.new((A[0],B[i],B[(i+1)%seg]))
        elif len(B)==1:
            for i in range(seg): bm.faces.new((A[i],A[(i+1)%seg],B[0]))
        else:
            for i in range(seg): bm.faces.new((A[i],A[(i+1)%seg],B[(i+1)%seg],B[i]))
    if cap:
        for R_ in (rings[0],rings[-1]):
            if len(R_)>2: bm.faces.new(R_)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    return new_obj(name,bm,m,sub=sub)
def _ax(axis,h,u,v,o):
    o=Vector(o)
    if axis=='Z': return o+Vector((u,v,h))
    if axis=='X': return o+Vector((h,u,v))
    if axis=='Y': return o+Vector((u,h,v))

def torus(name,R,r,m,loc,normal=(0,0,1),seg=64,mseg=16,sz=1.0):
    bm=bmesh.new(); rings=[]
    for i in range(seg):
        a=2*math.pi*i/seg; ring=[]
        for j in range(mseg):
            b=2*math.pi*j/mseg
            ring.append(bm.verts.new(((R+r*math.cos(b))*math.cos(a),(R+r*math.cos(b))*math.sin(a),r*math.sin(b)*sz)))
        rings.append(ring)
    for i in range(seg):
        A=rings[i]; B=rings[(i+1)%seg]
        for j in range(mseg): bm.faces.new((A[j],B[j],B[(j+1)%mseg],A[(j+1)%mseg]))
    o=new_obj(name,bm,m); orient(o,loc,normal); return o
def orient(o,loc,normal):
    q=Vector((0,0,1)).rotation_difference(Vector(normal).normalized())
    o.matrix_world=Matrix.Translation(Vector(loc))@q.to_matrix().to_4x4()
def sphere(name,r,m,loc,scale=(1,1,1),seg=48):
    bm=bmesh.new(); bmesh.ops.create_uvsphere(bm,u_segments=seg,v_segments=seg//2,radius=r)
    o=new_obj(name,bm,m); o.location=loc; o.scale=scale; return o
def disk(name,r,m,loc,normal,depth=0.004,seg=32):
    bm=bmesh.new(); bmesh.ops.create_cone(bm,cap_ends=True,segments=seg,radius1=r,radius2=r,depth=depth)
    o=new_obj(name,bm,m,smooth=False); orient(o,loc,normal); return o
def tube(name,pts,r,m,res=8):
    cu=bpy.data.curves.new(name,'CURVE'); cu.dimensions='3D'; cu.bevel_depth=r; cu.bevel_resolution=4
    sp=cu.splines.new('POLY'); sp.points.add(len(pts)-1)
    for p,c in zip(sp.points,pts): p.co=(*c,1)
    cu.use_fill_caps=True
    o=bpy.data.objects.new(name,cu); col.objects.link(o); cu.materials.append(M[m]); return o

# ---------------- SAUCER (revolve around Z) ----------------
R=P['R']; Ht=P['Ht']; Hb=P['Hb']; nt=P['n_top']; nb=P['n_bot']
def saucer_pt(t):  # t in [0,pi]: 0 = top centre, pi/2 = rim, pi = bottom centre
    s=math.sin(t); c=math.cos(t)
    r=R*abs(s)**(2/(nt if c>=0 else nb)); n=nt if c>=0 else nb; H=Ht if c>=0 else Hb
    z=math.copysign(H*abs(c)**(2/n),c)
    return r,z
prof=[(saucer_pt(math.pi*i/120)[1],saucer_pt(math.pi*i/120)[0]) for i in range(121)]
prof[0]=(Ht,0); prof[-1]=(-Hb,0)
saucer=lathe('Saucer',prof,'body',seg=128)
def saucer_surf(r,top=True):
    n=nt if top else nb; H=Ht if top else Hb
    u=min(0.9999,r/R); z=H*(1-u**n)**(1/n)
    dz=-H*(1-u**n)**(1/n-1)*u**(n-1)/R
    if not top: z=-z; dz=-dz
    nrm=Vector((-dz,0,1)) if top else Vector((dz,0,-1))
    return z,nrm.normalized()
# red bumper
bump=torus('Bumper',R-0.005,P['bumper_r'],'red',(0,0,P['bumper_z']+0.012),seg=160,mseg=20,sz=1.15)
torus('BumperLower',R-0.04,0.034,'red',(0,0,P['bumper_z']-0.075),seg=160,mseg=14,sz=1.0)
# lights on bumper
for ang,mm in ((math.radians(-70),'white'),(math.radians(-25),'cream'),(math.radians(25),'cream'),(math.radians(70),'white')):
    rr=R+P['bumper_r']*0.95
    bm=bmesh.new(); bmesh.ops.create_cube(bm,size=1)
    o=new_obj('BumperLight',bm,mm); o.scale=(0.03,0.075,0.035); o.location=(rr*math.cos(ang),rr*math.sin(ang),P['bumper_z'])
    o.rotation_euler=(0,0,ang); md=o.modifiers.new('bev','BEVEL'); md.width=0.012; md.segments=3
# top portholes ring
def porthole_ring(n,r,top,size,prefix,a0=0.0,skip=None):
    for i in range(n):
        a=a0+2*math.pi*i/n
        if skip and skip(a): continue
        z,nr=saucer_surf(r,top)
        nr=Matrix.Rotation(a,3,'Z')@nr; loc=Vector((r*math.cos(a),r*math.sin(a),z))
        torus(f'{prefix}Rim',size,size*0.32,'cream',loc+nr*0.004,nr,seg=24,mseg=8,sz=0.8)
        disk(f'{prefix}Glass',size*0.95,'dark',loc+nr*0.002,nr,depth=0.01,seg=20)
aft=lambda a: abs(((a-math.pi+math.pi)%(2*math.pi))-math.pi)<math.radians(28)  # skip rear where neck is
porthole_ring(P.get('n_top_ports',24),0.78,True,0.052,'TopPort')
porthole_ring(P.get('n_bot_ports',20),0.76,False,0.040,'BotPort',a0=math.pi/20,skip=aft)
# cream line ring on top
rr=0.60; z,_=saucer_surf(rr,True)
torus('TopLine',rr,0.010,'cream',(0,0,z+0.004),seg=128,mseg=8,sz=0.6)
# little cream dots on top surface
for i in range(8):
    a=2*math.pi*(i+0.5)/8; r_=0.70; z,nr=saucer_surf(r_,True)
    sphere('TopDot',0.014,'cream',(r_*math.cos(a),r_*math.sin(a),z),scale=(1,1,0.6),seg=12)
# bridge: cream ring, clear dome, inner dome + knob
zt=Ht
lathe('BridgeRing',[(zt-0.03,P['ring_r']+0.05),(zt+0.02,P['ring_r']+0.05),(zt+0.05,P['ring_r']+0.02),(zt+0.055,P['ring_r']-0.03),(zt+0.04,0.0)],'cream',seg=96)
dr=P['dome_r']; dz0=zt+0.05
lathe('BridgeDome',[(dz0+dr*math.cos(math.pi/2*i/24)*1.0, dr*math.sin(math.pi/2*i/24)) for i in range(25)][::-1] if False else
      [(dz0+dr*1.0*math.sin(math.pi/2*(1-i/24)), dr*math.cos(math.pi/2*(1-i/24))) for i in range(25)],'glass',seg=96,cap=False)
lathe('BridgeCore',[(dz0,0.10),(dz0+0.05,0.095),(dz0+0.085,0.07),(dz0+0.10,0.0)],'body',seg=64)
lathe('BridgeCollar',[(dz0+0.08,0.05),(dz0+0.11,0.045),(dz0+0.12,0.0)],'cream',seg=48)
sphere('BridgeKnob',0.03,'body',(0,0,dz0+0.13),seg=24)
# bottom: sensor hub
zb=-Hb
lathe('BottomHub',[(zb+0.04,0.24),(zb-0.02,0.22),(zb-0.05,0.16),(zb-0.06,0.0)],'body',seg=96)
torus('BottomHubRing',0.22,0.022,'cream',(0,0,zb-0.015),(0,0,-1),seg=96,mseg=10)
lathe('BottomLight',[(zb-0.05,0.06),(zb-0.085,0.045),(zb-0.095,0.0)],'cream',seg=32)

# ---------------- SECONDARY HULL (revolve around X) ----------------
hx=P['hull_x']; hz=P['hull_z']; hp=P['hull_prof']
# smooth profile via Catmull-Rom-ish dense interpolation (pchip-lite)
def interp(pts,n=60):
    out=[]
    for k in range(len(pts)-1):
        p0=pts[max(0,k-1)]; p1=pts[k]; p2=pts[k+1]; p3=pts[min(len(pts)-1,k+2)]
        for i in range(n//len(pts)+2):
            t=i/(n//len(pts)+2)
            def cr(a,b,c,d): return 0.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t**3)
            out.append((cr(p0[0],p1[0],p2[0],p3[0]),max(0,cr(p0[1],p1[1],p2[1],p3[1]))))
    out.append(tuple(pts[-1])); return out
hprof=interp(hp,80)
def hull_r(s):
    for (a,ra),(b,rb) in zip(hprof,hprof[1:]):
        if a<=s<=b: return ra+(rb-ra)*(s-a)/max(1e-9,b-a)
    return 0.0
hull=lathe('SecondaryHull',[(hx-s,r) for s,r in hprof],'body',seg=96,axis='X',origin=(0,0,hz))
# deflector
r0=hp[0][1]
lathe('DeflectorHousing',[(hx+0.02,r0-0.02),(hx+0.10,r0-0.03),(hx+0.13,r0-0.07),(hx+0.12,r0-0.10),(hx-0.04,r0-0.10)],'cream',seg=96,axis='X',origin=(0,0,hz),cap=False)
torus('DeflectorRingOuter',r0-0.005,0.045,'cream',(hx+0.01,0,hz),(1,0,0),seg=96,mseg=16)
torus('DeflectorRingMid',r0-0.06,0.035,'cream',(hx+0.12,0,hz),(1,0,0),seg=96,mseg=12)
torus('DeflectorRingInner',r0-0.135,0.028,'cream',(hx+0.11,0,hz),(1,0,0),seg=96,mseg=12)
lathe('DeflectorDish',[(hx+0.11,r0-0.10),(hx+0.06,r0-0.16),(hx+0.03,0.07),(hx+0.025,0.0)],'dark',seg=96,axis='X',origin=(0,0,hz))
lathe('DeflectorCone',[(hx+0.03,0.10),(hx+0.08,0.085),(hx+0.15,0.045),(hx+0.17,0.0)],'body',seg=48,axis='X',origin=(0,0,hz))
for i in range(6):
    a=2*math.pi*i/6+0.5; s_=Vector((0,math.cos(a),math.sin(a)))
    o,_=None,None
    tube('DeflectorSpoke',[(hx+0.05,(0.09)*math.cos(a),hz+0.09*math.sin(a)),(hx+0.09,(r0-0.15)*math.cos(a),hz+(r0-0.15)*math.sin(a))],0.012,'body')
sphere('DeflectorTip',0.04,'cream',(hx+0.17,0,hz),seg=24)
# rear: cream end cap ring + small dark hangar
s_end=hp[-2][0]
torus('HullRearRing',hp[-2][1]+0.0,0.03,'cream',(hx-s_end,0,hz),(1,0,0),seg=64,mseg=10)
# hull side red stripe panels (stadium patch on revolve surface)
def stadium(L,W,n=40):
    pts=[]; rr=W/2; hl=L/2-rr
    for i in range(n):
        a=-math.pi/2+math.pi*i/(n-1); pts.append((hl+rr*math.cos(a),rr*math.sin(a)))
    for i in range(n):
        a=math.pi/2+math.pi*i/(n-1); pts.append((-hl+rr*math.cos(a),rr*math.sin(a)))
    return pts
def surf_panel(name,outline,mapf,off,m,th=0.012,rings=6):
    """outline: 2D pts (s,t) closed. mapf(s,t,off)->(Vector pos). Builds curved patch by concentric shrink."""
    bm=bmesh.new(); cs=sum(p[0] for p in outline)/len(outline); ct=sum(p[1] for p in outline)/len(outline)
    layers=[]
    for k in range(rings+1):
        f=1-k/rings
        layers.append([(cs+(s-cs)*f, ct+(t-ct)*f) for s,t in outline])
    def mk(lay,o): return [bm.verts.new(mapf(s,t,o)) for s,t in lay]
    top=[mk(l,off+th) for l in layers]; bot=mk(layers[0],off-0.004)
    n=len(outline)
    for A,B in zip(top,top[1:]):
        for i in range(n):
            try: bm.faces.new((A[i],A[(i+1)%n],B[(i+1)%n],B[i]))
            except ValueError: pass
    for i in range(n): bm.faces.new((bot[i],bot[(i+1)%n],top[0][(i+1)%n],top[0][i]))
    bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=1e-6)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    return new_obj(name,bm,m)
def hull_map(side):
    def f(s,t,o):
        x=hx-s; r=hull_r(s)+o; a=side*(t/max(0.01,hull_r(s)))   # t = arc length from side meridian
        return Vector((x, side*r*math.cos(a)*1.0 if False else r*math.cos(a)*side, hz+r*math.sin(a)))
    return f
for side in (1,-1):
    sc_=P.get('hull_stripe_s',0.80); L_=P.get('hull_stripe_L',0.55); W_=P.get('hull_stripe_W',0.13)
    out=[(sc_+s,t-0.02) for s,t in stadium(L_+0.05,W_+0.05)]
    surf_panel('HullStripeCream',out,hull_map(side),0.0,'cream',th=0.010)
    inn=[(sc_+s,t-0.02) for s,t in stadium(L_-0.01,W_-0.03)]
    surf_panel('HullStripeRed',inn,hull_map(side),0.012,'red',th=0.008)
    # row of cream dots above stripe, and a little grey light
    for i in range(7):
        s=0.34+i*0.05; r=hull_r(s); a=math.radians(38)
        sphere('HullDot',0.014,'cream',(hx-s,side*r*math.cos(a),hz+r*math.sin(a)),seg=12)
    s=0.98; r=hull_r(s); a=math.radians(-5)
    bm=bmesh.new(); bmesh.ops.create_cube(bm,size=1)
    o=new_obj('HullLight',bm,'white'); o.scale=(0.10,0.03,0.04); o.location=(hx-s,side*(r+0.005)*math.cos(a),hz+r*math.sin(a))
    md=o.modifiers.new('bev','BEVEL'); md.width=0.014; md.segments=3

# ---------------- beams (neck, pylons): loft of rounded-rect sections ----------------
def beam(name,A,B,chord_ref,a0,a1,th0,th1,m,n=24,seg=32,pw=4.0,ext=0.0):
    A=Vector(A); B=Vector(B); d=(B-A); L=d.length; d.normalize()
    A=A-d*ext; B=B+d*ext; L+=2*ext
    c=Vector(chord_ref); c=(c-d*c.dot(d)).normalized(); tdir=d.cross(c).normalized()
    bm=bmesh.new(); rings=[]
    for i in range(n+1):
        u=i/n; p=A+d*(L*u); a=a0+(a1-a0)*u; th=th0+(th1-th0)*u; ring=[]
        for j in range(seg):
            q=2*math.pi*j/seg; cq=math.cos(q); sq=math.sin(q)
            x=a*math.copysign(abs(cq)**(2/pw),cq); y=th*math.copysign(abs(sq)**(2/pw),sq)
            ring.append(bm.verts.new(p+c*x+tdir*y))
        rings.append(ring)
    for R1,R2 in zip(rings,rings[1:]):
        for j in range(seg): bm.faces.new((R1[j],R1[(j+1)%seg],R2[(j+1)%seg],R2[j]))
    bm.faces.new(rings[0]); bm.faces.new(rings[-1][::-1])
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    o=new_obj(name,bm,m); return o,(A,d,c,tdir,L)
# neck: thin in Y, chord roughly along X
na=P['neck_a']; nbv=P['neck_b']
neck,(NA,Nd,Nc,Nt,NL)=beam('Neck',na,nbv,(-1,0,0),P['neck_chord'],P['neck_chord_b'],P['neck_th'],P['neck_th']*1.1,'body',ext=0.08)
for sgn in (1,-1):  # cream piping along leading & trailing edges
    pts=[tuple(NA+Nd*(NL*u)+Nc*sgn*(P['neck_chord']+(P['neck_chord_b']-P['neck_chord'])*u)*0.98) for u in [i/10 for i in range(2,10)]]
    tube('NeckPipe',pts,0.022,'cream')
for side in (1,-1):
    for i in range(5):
        u=0.35+i*0.09; p=NA+Nd*(NL*u)+Nt*side*(P['neck_th']*1.05)+Nc*0.05
        sphere('NeckDot',0.014,'cream',tuple(p),seg=12)

# ---------------- NACELLES ----------------
ny=P['nac_y']; nz=P['nac_z']; x0=P['nac_x0']; NLn=P['nac_len']; nr=P['nac_r']; cr=P['cap_r']
for side,tag in ((1,'P'),(-1,'S')):
    y=side*ny
    prof=[(x0-0.02,nr*0.70),(x0-0.05,nr*0.95),(x0-0.12,nr),(x0-NLn+0.12,nr),(x0-NLn+0.05,nr*0.92),(x0-NLn,nr*0.6),(x0-NLn-0.01,0.0)]
    lathe(f'Nacelle{tag}',interp(prof,40),'body',seg=72,axis='X',origin=(0,y,nz))
    sphere(f'NacelleCap{tag}',cr,'red',(x0+0.02,y,nz),scale=(0.92,1,1),seg=48)
    torus(f'NacelleFrontRing{tag}',nr+0.005,0.042,'cream',(x0-0.10,y,nz),(1,0,0),seg=64,mseg=12)
    torus(f'NacelleRing2{tag}',nr+0.002,0.025,'cream',(x0-0.20,y,nz),(1,0,0),seg=64,mseg=10)
    torus(f'NacelleRearRing{tag}',nr-0.005,0.04,'cream',(x0-NLn+0.10,y,nz),(1,0,0),seg=64,mseg=12)
    sphere(f'NacelleRearCap{tag}',nr*0.70,'red',(x0-NLn+0.04,y,nz),scale=(0.75,1,1),seg=32)
    # rivets on front ring band
    for i in range(16):
        a=2*math.pi*i/16
        sphere('Rivet',0.011,'cream',(x0-0.20,y+(nr+0.026)*math.cos(a),nz+(nr+0.026)*math.sin(a)),seg=10)
    # outboard stripe panel (cream frame + red insert); also inboard
    def nac_map(sd):
        def f(s,t,o):
            x=x0-s; r=nr+o; a=t/nr
            return Vector((x,y+sd*r*math.cos(a),nz+r*math.sin(a)))
        return f
    for sd in (1,-1):
        sc_=NLn*0.55; L_=NLn*0.55; W_=0.13
        surf_panel('NacStripeCream',[(sc_+s,t) for s,t in stadium(L_+0.06,W_+0.06)],nac_map(sd),0.0,'cream',th=0.010)
        surf_panel('NacStripeRed',[(sc_+s,t) for s,t in stadium(L_-0.02,W_-0.035)],nac_map(sd),0.012,'red',th=0.008)
    # top cream trim strip with rivets (inboard upper)
    a=math.radians(90)
    pts=[(x0-0.26-i*0.1,y+(nr+0.004)*math.cos(a),nz+(nr+0.004)*math.sin(a)) for i in range(int((NLn-0.45)/0.1))]
    tube('NacTopTrim',pts,0.018,'cream')
    for p in pts[::2]: sphere('Rivet',0.010,'cream',(p[0],p[1],p[2]+0.017),seg=10)
    # pylon
    pr=Vector(P['pyl_root']); pt=Vector(P['pyl_top']); pr.y*=side; pt.y*=side
    pyl,(PA,Pd,Pc,Pt,PL)=beam(f'Pylon{tag}',pr,pt,(-1,0,0),P['pyl_chord'],P['pyl_chord']*0.9,P['pyl_th'],P['pyl_th'],'body',ext=0.05)
    for sgn in (1,-1):
        pts=[tuple(PA+Pd*(PL*u)+Pc*sgn*P['pyl_chord']*0.97) for u in [i/10 for i in range(1,10)]]
        tube('PylonPipe',pts,0.026,'cream')
    # rivets along the pylon piping
    for sgn in (1,-1):
        for k in range(6):
            u=0.18+k*0.13; p=PA+Pd*(PL*u)+Pc*sgn*P['pyl_chord']*0.80
            for tt in (1,-1): sphere('Rivet',0.010,'cream',tuple(p+Pt*tt*P['pyl_th']*0.95),seg=10)
# ---------------- staging ----------------
for o in col.objects:
    pass
w=bpy.data.worlds.new('W'); scene.world=w; w.use_nodes=True
bg=w.node_tree.nodes['Background']; bg.inputs[0].default_value=srgb('#E4E4E4'); bg.inputs[1].default_value=0.6
bm=bmesh.new(); bmesh.ops.create_grid(bm,x_segments=1,y_segments=1,size=30)
gnd=new_obj('Ground',bm,'ground',smooth=False); gnd.location=(0,0,P.get('ground_z',-1.55))
def area(name,loc,size,energy,target=(-1,0,-0.2),color=(1,1,1)):
    L=bpy.data.lights.new(name,'AREA'); L.size=size; L.energy=energy; L.color=color
    o=bpy.data.objects.new(name,L); scene.collection.objects.link(o); o.location=loc
    o.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler()
area('Key',(3,6,6),8,800); area('Fill',(-3,-6,3),9,220); area('Top',(-1,0,8),10,350); area('Rim',(-7,4,2),6,250); area('Front',(7,3,1),7,320)
camd=bpy.data.cameras.new('Cam'); cam=bpy.data.objects.new('Cam',camd); scene.collection.objects.link(cam); scene.camera=cam
scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=P['samples']
scene.cycles.use_denoising=True; scene.cycles.denoiser='OPENIMAGEDENOISE'
scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
scene.render.film_transparent=True; gnd.is_shadow_catcher=True
scene.render.resolution_x=1024; scene.render.resolution_y=576
bpy.ops.wm.save_as_mainfile(filepath=f'{HERE}/enterprise_{ROUND}.blend',compress=True)
print('SAVED',flush=True)
