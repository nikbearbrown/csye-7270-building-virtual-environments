# Planet Express ship - scripted build. Usage: blender -b -P build_pe.py -- ROUND [views...]
import bpy, bmesh, math, sys, os, json
import numpy as np
from mathutils import Vector, Matrix, Euler
HERE='/workspace/ships/planet-express'
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ROUND=argv[0] if argv else 'r1'
VIEWS=argv[1:]
P=json.load(open(f'{HERE}/params.json'))
SAMPLES=P.get('samples',32)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene

def pchip(xs,ys):
    xs=np.array(xs,float); ys=np.array(ys,float)
    o=np.argsort(xs); xs=xs[o]; ys=ys[o]
    h=np.diff(xs); dl=np.diff(ys)/h
    m=np.zeros_like(ys)
    for k in range(1,len(xs)-1):
        if dl[k-1]*dl[k]<=0: m[k]=0
        else:
            w1=2*h[k]+h[k-1]; w2=h[k]+2*h[k-1]
            m[k]=(w1+w2)/(w1/dl[k-1]+w2/dl[k])
    m[0]=dl[0]; m[-1]=dl[-1]
    def f(x):
        x=np.clip(np.asarray(x,float),xs[0],xs[-1])
        k=np.clip(np.searchsorted(xs,x)-1,0,len(xs)-2)
        t=(x-xs[k])/h[k]
        h00=2*t**3-3*t**2+1; h10=t**3-2*t**2+t; h01=-2*t**3+3*t**2; h11=t**3-t**2
        return h00*ys[k]+h10*h[k]*m[k]+h01*ys[k+1]+h11*h[k]*m[k+1]
    return f
T=P['tables']
fW=pchip(*zip(*T['w'])); fL=pchip(*zip(*T['lip'])); fT=pchip(*zip(*T['top'])); fB=pchip(*zip(*T['bot']))
XN=P['x_nose']; XT=P['x_tail']; NU=P['n_up']; NL=P['n_lo']
def _ell(x,x0,a,pw=2.0):
    if a<=0: return 1.0
    u=min(1,max(0,(x-x0)/a)); return math.sqrt(max(0,1-u**pw))
def nose_fac(x):
    # elliptic closure toward nose tip
    a=P['nose_len']; xs=XN-a
    if x<=xs: return 1.0
    u=min(1,(x-xs)/a); return math.sqrt(max(0,1-u**P['nose_pow']))
def S(x,th):
    w=float(fW(x)); zl=float(fL(x)); zt=float(fT(x)); zb=float(fB(x))
    c=math.cos(th); s=math.sin(th)
    if s>=0: n=NU; hz=zt-zl
    else: n=NL; hz=zl-zb
    y=w*math.copysign(abs(c)**(2/n),c)
    z=zl+math.copysign(hz*abs(s)**(2/n),s)
    return Vector((x,y,z))
def frame(x,th):
    p=S(x,th); e=1e-3
    dx=(S(x+e,th)-S(x-e,th)); dt=(S(x,th+e)-S(x,th-e))
    n=dx.cross(dt).normalized()
    if n.dot(p-Vector((x,0,float(fL(x)))))<0: n=-n
    return p,n,dx.normalized()
def th_for_z(x,z,side=1):
    zl=float(fL(x)); zt=float(fT(x)); zb=float(fB(x))
    if z>=zl: r=min(1,(z-zl)/(zt-zl)); th=math.asin(r**(NU/2))
    else: r=min(1,(zl-z)/(zl-zb)); th=-math.asin(r**(NL/2))
    return th if side>0 else math.pi-th
def th_for_y(x,y):  # upper surface
    w=float(fW(x)); r=min(1,abs(y)/w); th=math.acos(r**(NU/2))
    return th if y>=0 else math.pi-th

# ---------- materials
def srgb(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return [ (v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4) for v in c]+[1]
def mat(name,hexc,rough=0.38,spec=0.5,coat=0.0,emit=0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=srgb(hexc); b.inputs['Roughness'].default_value=rough
    b.inputs['Specular IOR Level'].default_value=spec
    b.inputs['Coat Weight'].default_value=coat; b.inputs['Coat Roughness'].default_value=0.25
    if emit: b.inputs['Emission Color'].default_value=srgb(hexc); b.inputs['Emission Strength'].default_value=emit
    return m
C=P['colors']
M={k:mat(k,v[0],v[1]) for k,v in C.items()}
M['slot']=mat('slot','#7E7253',0.7)
M['teal'].node_tree.nodes['Principled BSDF'].inputs['Coat Weight'].default_value=0.25
# logo material
for key,fn in (('logo','logo.png'),('logo_m','logo_m.png')):
    lm=bpy.data.materials.new(key); lm.use_nodes=True; nt=lm.node_tree
    b=nt.nodes['Principled BSDF']; tex=nt.nodes.new('ShaderNodeTexImage'); tex.image=bpy.data.images.load(f'{HERE}/'+fn)
    nt.links.new(tex.outputs['Color'],b.inputs['Base Color']); nt.links.new(tex.outputs['Alpha'],b.inputs['Alpha'])
    b.inputs['Roughness'].default_value=0.4
    M[key]=lm

def mk(name,verts,faces,m,smooth=True,uvs=None):
    me=bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts],[],faces); me.validate()
    if uvs is not None:
        ul=me.uv_layers.new()
        for poly in me.polygons:
            for li in poly.loop_indices: ul.data[li].uv=uvs[me.loops[li].vertex_index]
    o=bpy.data.objects.new(name,me); scene.collection.objects.link(o)
    me.materials.append(m)
    if smooth:
        for p in me.polygons: p.use_smooth=True
    return o

def Sn(x,th):
    fw=nose_fac(x); fh=_ell(x,XN-P.get('top_nose_len',P['nose_len']),P.get('top_nose_len',P['nose_len']))
    ft=_ell(-x,-(XT+P.get('tail_len',0)),P.get('tail_len',0))
    fw*=ft; fh*=ft
    zl=float(fL(x)); p=S(x,th); p.y*=fw; p.z=zl+(p.z-zl)*(fh if p.z>zl else min(1,fw*1.0+0*fh)); return p
# ---------- hull
NX=P['nx']; NTH=P['nth']
u=np.linspace(0,1,NX)
xs=XT+(XN-XT)*(0.5-0.5*np.cos(np.pi*u))  # clustered at both ends
xs=xs[:-1]
ths=[2*math.pi*j/NTH for j in range(NTH)]
verts=[]; faces=[]
for x in xs:
    f=nose_fac(x)
    zl=float(fL(x))
    for th in ths:
        verts.append(Sn(x,th))
nos=len(verts); verts.append(Vector((XN,0,float(fL(XN)))))
for i in range(len(xs)-1):
    for j in range(NTH):
        a=i*NTH+j; b_=i*NTH+(j+1)%NTH
        faces.append((a,b_,b_+NTH,a+NTH))
L=(len(xs)-1)*NTH
for j in range(NTH): faces.append((L+j,L+(j+1)%NTH,nos))
tc=len(verts); verts.append(Vector((XT,0,float(fL(XT)))))
for j in range(NTH): faces.append(((j+1)%NTH,j,tc))
hull=mk('Hull',verts,faces,M['teal'])
# nose-adjusted surface for placement near the nose

def framen(x,th):
    p=Sn(x,th); e=1e-3
    dx=(Sn(x+e,th)-Sn(x-e,th)); dt=(Sn(x,th+e)-Sn(x,th-e))
    n=dx.cross(dt).normalized()
    c=Vector((x-0.5,0,float(fL(x))))
    if n.dot(p-c)<0: n=-n
    return p,n

def patch(name,xa,xb,tha,thb,off,m,nx=24,nt=16,uv=False):
    V=[];F=[];U=[]
    for i in range(nx+1):
        x=xa+(xb-xa)*i/nx
        for j in range(nt+1):
            th=tha+(thb-tha)*j/nt; p,n=framen(x,th); V.append(p+n*off); U.append((i/nx,j/nt))
    for i in range(nx):
        for j in range(nt):
            a=i*(nt+1)+j; F.append((a,a+nt+1,a+nt+2,a+1))
    o=mk(name,V,F,m,uvs=U if uv else None)
    md=o.modifiers.new('s','SOLIDIFY'); md.thickness=off*0.9; md.offset=-1
    return o

def orient(o,p,n,up=Vector((1,0,0))):
    z=n.normalized(); x=(up-z*up.dot(z)); 
    if x.length<1e-4: x=Vector((0,1,0))
    x.normalize(); y=z.cross(x)
    R=Matrix((x,y,z)).transposed().to_4x4()
    o.matrix_world=Matrix.Translation(p)@R@o.matrix_world
parts=[]
def prim(kind,m,**kw):
    if kind=='torus': bpy.ops.mesh.primitive_torus_add(**kw)
    elif kind=='cyl': bpy.ops.mesh.primitive_cylinder_add(**kw)
    elif kind=='sph': bpy.ops.mesh.primitive_uv_sphere_add(**kw)
    elif kind=='ico': bpy.ops.mesh.primitive_ico_sphere_add(**kw)
    elif kind=='cube': bpy.ops.mesh.primitive_cube_add(**kw)
    elif kind=='circle': bpy.ops.mesh.primitive_circle_add(**kw)
    o=bpy.context.active_object; o.data.materials.append(m)
    if kind in('torus','cyl','sph'): bpy.ops.object.shade_smooth()
    return o
def apply_tf(o):
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)

# ---------- lip band (curve along widest line wrapping the nose)
def tube(name,pts,r,m,res=6,closed=False):
    cu=bpy.data.curves.new(name,'CURVE'); cu.dimensions='3D'; cu.bevel_depth=r; cu.bevel_resolution=res
    cu.use_fill_caps=True
    sp=cu.splines.new('POLY'); sp.points.add(len(pts)-1)
    for k,p in enumerate(pts): sp.points[k].co=(p.x,p.y,p.z,1)
    sp.use_cyclic_u=closed
    o=bpy.data.objects.new(name,cu); scene.collection.objects.link(o); cu.materials.append(m)
    return o
LR=P['lip_r']; lp=[]
xa=P['lip_x0']
xl=list(np.linspace(xa,XN-0.002,140))
for x in xl:
    p,n=framen(x,0.0); g=math.exp(-((XN-x)/P.get('beak_len',0.35))**2)
    tp=P.get('lip_taper',0); ramp=1.0 if tp<=0 else min(1,(x-xa)/tp)
    lp.append(p+n*LR*(P['lip_out']*ramp-1.3*(1-ramp))+Vector((P.get('beak_fwd',0)*g,0,-P.get('beak_drop',0)*g)))
tip=Vector((XN,0,float(fL(XN))))+Vector((1,0,0))*LR*P['lip_out']+Vector((P.get('beak_fwd',0),0,-P.get('beak_drop',0)))
pts=lp+[tip]+[Vector((q.x,-q.y,q.z)) for q in reversed(lp)]
lip=tube('Lip',pts,LR,M['red'],res=6)
lip.data.bevel_mode='ROUND'
# flatten lip a bit vertically via scale about its own line -> use a taper-free approach: scale z of whole object around lip z
# (kept round; toy lip is a rounded bead)

# ---------- portholes
def porthole(x,zz,r,side):
    t=th_for_z(x,zz,side)
    p,n=framen(x,t)
    o=prim('torus',M['cream'],major_radius=r,minor_radius=r*0.32,major_segments=32,minor_segments=10)
    orient(o,p+n*r*0.08,n); apply_tf(o)
    g=prim('cyl',M['port'],radius=r*0.82,depth=0.02,vertices=32)
    orient(g,p-n*0.01,n); apply_tf(g)
    k=prim('cyl',M['dteal'],radius=r*0.86,depth=0.03,vertices=32); orient(k,p-n*0.02,n); apply_tf(k)
for side in (1,-1):
    for (x,zz,r) in P['ports']: porthole(x,zz,r,side)

# ---------- cockpit window (in x,y on the upper nose)
CW=P['cockpit']
def surf_xy(x,y,off):
    th=th_for_y(x,y/ max(1e-6,nose_fac(x))) if nose_fac(x)>0.05 else math.pi/2
    p,n=framen(x,th); return p+n*off
if CW.get('mode')=='yz':
    def _zs(x,y):
        fw=nose_fac(x); w=float(fW(x))*fw
        if abs(y)>=w*0.999: return float(fL(x)), None
        th=th_for_y(x,y/max(1e-6,fw)); return Sn(x,th).z, th
    def surf_xy(y,z,off):
        lo,hi=2.5,XN-0.005
        for _ in range(40):
            m=0.5*(lo+hi); zz,_t=_zs(m,y)
            if zz>z: lo=m
            else: hi=m
        x=0.5*(lo+hi); zz,th=_zs(x,y)
        if th is None: th=0.05 if y>0 else math.pi-0.05
        p,n=framen(x,th); return p+n*off
outline=[tuple(v) for v in CW['outline']]
def bil(poly,u,v):
    # quad poly: (rear-left, rear-right, front-right, front-left) in x,y
    a,b,c,d=[Vector((q[0],q[1])) for q in poly]
    return (a*(1-u)+b*u)*(1-v)+(d*(1-u)+c*u)*v
nu,nv=20,10; V=[];F=[]
for i in range(nu+1):
    for j in range(nv+1):
        q=bil(outline,i/nu,j/nv); V.append(surf_xy(q.x,q.y,0.012))
for i in range(nu):
    for j in range(nv):
        a=i*(nv+1)+j; F.append((a,a+nv+1,a+nv+2,a+1))
glass=mk('CockpitGlass',V,F,M['glass'])
def edge_pts(p0,p1,k=24,off=0.055):
    return [surf_xy(p0[0]+(p1[0]-p0[0])*t/k, p0[1]+(p1[1]-p0[1])*t/k, off) for t in range(k+1)]
fr=CW['frame_r']
frm=[tuple(v) for v in CW.get('frame',CW['outline'])]
ol=frm+[frm[0]]
fpts=[]
for k in range(len(frm)): fpts+=edge_pts(ol[k],ol[k+1])[:-1]
tube('CockpitFrame',fpts,fr,M['dteal'],res=1,closed=True)
for mm in CW['mullions']: tube('Mullion',edge_pts(mm[0],mm[1]),fr*0.8,M['dteal'],res=1)

# ---------- turret
TU=P['turret']; tx=TU['x']; tz=float(fT(tx))
prof=[(r,tz+dz) for r,dz in TU['base']]
def lathe(name,prof,m,seg=48,axis='z',center=Vector((0,0,0))):
    V=[];F=[]
    for i in range(seg):
        a=2*math.pi*i/seg
        for (r,h) in prof:
            if axis=='z': V.append(center+Vector((r*math.cos(a),r*math.sin(a),h)))
            else: V.append(center+Vector((h,r*math.cos(a),r*math.sin(a))))
    n=len(prof)
    for i in range(seg):
        for k in range(n-1):
            a=i*n+k; b_=((i+1)%seg)*n+k; F.append((a,b_,b_+1,a+1))
    return mk(name,V,F,m)
lathe('TurretBase',prof,M['dteal'],center=Vector((tx,0,0)))
zr=tz+TU['base'][-1][1]
o=prim('cyl',M['cream'],radius=TU['ring_r'],depth=TU['ring_h'],vertices=48,location=(tx,0,zr+TU['ring_h']/2))
zd=zr+TU['ring_h']
o=prim('sph',M['dome'],radius=TU['dome_r'],segments=48,ring_count=24,location=(tx,0,zd)); o.scale.z=TU['dome_sz']
o=prim('cyl',M['black'],radius=0.022,depth=TU['ant_h'],vertices=12,location=(tx,0,zd+TU['ant_h']/2))
o=prim('sph',M['black'],radius=0.05,location=(tx,0,zd+TU['ant_h']))
g=TU['gun']; ang=math.radians(g['elev'])
base=Vector((tx+g['dx'],g['dy'],zd+g['dz']))
d=Vector((math.cos(ang),0,math.sin(ang)))
o=prim('cube',M['black'],size=1,location=base); o.scale=(0.34,0.22,0.24); o.rotation_euler=(0,-ang,0)
o=prim('cyl',M['black'],radius=g['r'],depth=g['len'],vertices=20,location=base+d*(g['len']/2+0.1)); o.rotation_euler=(0,math.pi/2-ang,0)
o=prim('cyl',M['black'],radius=g['r']*1.35,depth=0.12,vertices=20,location=base+d*(g['len']+0.08)); o.rotation_euler=(0,math.pi/2-ang,0)
o=prim('cyl',M['black'],radius=g['r']*1.25,depth=0.1,vertices=20,location=base+d*(0.35)); o.rotation_euler=(0,math.pi/2-ang,0)

# ---------- tail fin
FN=P['fin']
def fin_mesh():
    ol=[Vector((a,0,b)) for a,b in FN['outline']]
    # subdivide outline with a closed catmull-rom for soft corners
    pts=[]; n=len(ol)
    for i in range(n):
        p0,p1,p2,p3=ol[i-1],ol[i],ol[(i+1)%n],ol[(i+2)%n]
        for t in np.linspace(0,1,10,endpoint=False):
            t2=t*t;t3=t2*t
            pts.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3))
    bm=bmesh.new()
    vs=[bm.verts.new(p) for p in pts]; f=bm.faces.new(vs)
    bmesh.ops.triangulate(bm,faces=[f])
    me=bpy.data.meshes.new('Fin'); bm.to_mesh(me); bm.free()
    o=bpy.data.objects.new('Fin',me); scene.collection.objects.link(o); me.materials.append(M['dteal'])
    s=o.modifiers.new('sol','SOLIDIFY'); s.thickness=FN['thick']; s.offset=0
    bv=o.modifiers.new('bev','BEVEL'); bv.width=FN['thick']*0.45; bv.segments=3; bv.limit_method='ANGLE'
    for p in me.polygons: p.use_smooth=True
    return pts
fpts=fin_mesh()
# cream riveted leading edge
le=[] if not FN.get('leading') else [Vector((a,0,b)) for a,b in FN['leading']]
lep=[]
for i in range(len(le)-1):
    for t in np.linspace(0,1,12,endpoint=False): lep.append(le[i].lerp(le[i+1],t))
if le:
  lep.append(le[-1])
  lo=tube('FinLeadingEdge',lep,FN['thick']*0.75,M['cream'],res=4)
  for i in range(1,len(lep)-1,3):
    for sy in (1,-1):
        prim('ico',M['black'],radius=0.028,subdivisions=1,location=(lep[i].x,sy*FN['thick']*0.72,lep[i].z))
# logo decals
lc=FN['logo']; 
for sy in (1,-1):
    o=prim('circle',M['logo' if sy>0 else 'logo_m'],vertices=64,radius=lc[2],fill_type='NGON',location=(lc[0],sy*(FN['thick']/2+0.012),lc[1]))
    o.rotation_euler=(math.pi/2*sy,0,0 if sy>0 else math.pi)  # toy decal reads mirrored on +y side (ref05/ref12) via UV flip
    me=o.data; ul=me.uv_layers.new()
    for poly in me.polygons:
        for li in poly.loop_indices:
            v=me.vertices[me.loops[li].vertex_index].co; ul.data[li].uv=(0.5+v.x/(2*lc[2]),0.5+v.y/(2*lc[2]))
# fin root fairing strip (cream) along the hull top, with rivets
FS=P['fin_strip']
for side in (1,-1):
    xs_=np.linspace(FS['x0'],FS['x1'],40); pts=[]
    for x in xs_:
        th=th_for_y(x,side*FS['y']); p,n=framen(x,th); pts.append(p+n*0.03)
    tube('FinStrip',pts,FS['r'],M['cream'],res=3)
    for x in np.linspace(FS['x0']+0.15,FS['x1']-0.1,9):
        th=th_for_y(x,side*FS['y']); p,n=framen(x,th)
        prim('ico',M['black'],radius=0.035,subdivisions=1,location=p+n*(0.03+FS['r']*0.9))

# ---------- vents, hatches
for side in (1,-1):
    V_=P['vent']
    tha=th_for_z(0.5*(V_['x0']+V_['x1']),V_['z0']); thb=th_for_z(0.5*(V_['x0']+V_['x1']),V_['z1'])
    if side<0: tha,thb=math.pi-tha,math.pi-thb
    patch('Vent',V_['x0'],V_['x1'],tha,thb,0.07,M['cream'])
    # rounded raised border around the vent panel
    bl=[]
    for k in range(17): bl.append((V_['x0']+(V_['x1']-V_['x0'])*k/16,tha))
    for k in range(9): bl.append((V_['x1'],tha+(thb-tha)*k/8))
    for k in range(17): bl.append((V_['x1']-(V_['x1']-V_['x0'])*k/16,thb))
    for k in range(9): bl.append((V_['x0'],thb-(thb-tha)*k/8))
    bp=[]
    for (x,t) in bl:
        pp,nn=framen(x,t); bp.append(pp+nn*0.085)
    tube('VentRim',bp,0.065,M['cream'],res=3,closed=True)
    for x in np.linspace(V_['x0']+0.16,V_['x1']-0.16,V_['ribs']):
        t1=tha+(thb-tha)*0.2; t2=tha+(thb-tha)*0.8
        pa,na=framen(x,t1); pb,nb=framen(x,t2)
        tube('VentSlot',[pa+na*0.075,pb+nb*0.075],0.038,M['slot'],res=3)
        tube('VentRib',[pa+na*0.085+(V_['x1']-V_['x0'])/abs(V_['x1']-V_['x0'])*Vector((0.06,0,0)),pb+nb*0.085+(V_['x1']-V_['x0'])/abs(V_['x1']-V_['x0'])*Vector((0.06,0,0))],0.022,M['cream'],res=3)
    for h in P['hatches']:
        t1=th_for_z(h['x0'],h['z0']); t2=th_for_z(h['x0'],h['z1'])
        if side<0: t1,t2=math.pi-t1,math.pi-t2
        if h.get('m','cream')=='cream':
            patch('Hatch',h['x0'],h['x1'],t1,t2,0.03,M['cream'])
            xm=0.5*(h['x0']+h['x1']); pd,nd=framen(xm,t1+(t2-t1)*0.68)
            dl=prim('cyl',M['cream2'],radius=0.07,depth=0.04,vertices=24); orient(dl,pd+nd*0.05,nd); apply_tf(dl)
            dk=prim('cyl',M['dteal'],radius=0.035,depth=0.05,vertices=16); orient(dk,pd+nd*0.06,nd); apply_tf(dk)
        else:
            for k in range(3):
                zz=h['z0']+(h['z1']-h['z0'])*(k+0.5)/3
                ta=th_for_z(h['x0'],zz,side); tb=th_for_z(h['x1'],zz,side)
                pa,na=framen(h['x0'],ta); pb,nb=framen(h['x1'],tb)
                tube('HatchSlat',[pa+na*0.03,pb+nb*0.03],0.035,M['dteal'],res=2)

# ---------- side wings / landing struts
WG=P['wing']
def wing(side):
    r0=Vector(WG['root_le']); r1=Vector(WG['root_te']); t0=Vector(WG['tip_le']); t1=Vector(WG['tip_te'])
    for v in (r0,r1,t0,t1): v.y*=side
    th0=WG['root_t']; th1=WG['tip_t']
    nu=10; nv=12; V=[];F=[]
    # build as a lofted section along span with airfoil-ish thickness
    span=[]
    for i in range(nu+1):
        s=i/nu; le=r0.lerp(t0,s); te=r1.lerp(t1,s); th=th0+(th1-th0)*s
        sec=[]
        for j in range(nv):
            a=2*math.pi*j/nv
            c=0.5-0.5*math.cos(a); tt=math.sin(a)*th*0.5*(1-abs(2*c-1)**3)**0.5
            p=le.lerp(te,c)
            # thickness direction = normal of wing plane
            nrm=(t0-r0).cross(r1-r0).normalized()*side
            sec.append(p+nrm*tt)
        span.append(sec)
    for sec in span: V+=sec
    for i in range(nu):
        for j in range(nv):
            a=i*nv+j; b_=i*nv+(j+1)%nv; F.append((a,b_,b_+nv,a+nv))
    F.append(tuple(range(nu*nv,nu*nv+nv)))
    o=mk('Wing',V,F,M['dteal'])
    sd=o.modifiers.new('sub','SUBSURF'); sd.levels=2; sd.render_levels=2
    # cream trim on leading edge
    pts=[r0.lerp(t0,s/20) for s in range(21)]
    tube('WingTrim',pts,th0*0.3,M['cream'],res=3)
    # root ring (cream ellipse on hull) with rivets
    R=WG['ring']; pts=[]
    for k in range(48):
        a=2*math.pi*k/48
        x=R['xc']+R['ax']*math.cos(a); z=R['zc']+R['az']*math.sin(a)
        th=th_for_z(x,z,side); p,n=framen(x,th); pts.append(p+n*0.04)
    tube('WingRootRing',pts,R['r'],M['cream'],res=3,closed=True)
    for k in range(0,48,4):
        a=2*math.pi*k/48; x=R['xc']+R['ax']*math.cos(a); z=R['zc']+R['az']*math.sin(a)
        th=th_for_z(x,z,side); p,n=framen(x,th)
        prim('ico',M['black'],radius=0.04,subdivisions=1,location=p+n*(0.04+R['r']))
for s in (1,-1): wing(s)

# ---------- engine
EN=P['engine']; ec=Vector((0,0,EN['zc']))
lathe('EngineBell',[(r,x) for x,r in EN['bell']],M['cream'],seg=64,axis='x',center=ec)
o=prim('cyl',M['exhaust'],radius=EN['inner_r'],depth=0.1,vertices=48,location=(EN['disk_x'],0,EN['zc'])); o.rotation_euler=(0,math.pi/2,0)
o=prim('cyl',M['exhaust'],radius=EN['hub_r'],depth=0.5,vertices=24,location=(EN['disk_x']-0.25,0,EN['zc'])); o.rotation_euler=(0,math.pi/2,0)
for k in range(4):
    a=math.pi/4+k*math.pi/2
    o=prim('cube',M['exhaust'],size=1,location=(EN['disk_x']-0.2,math.cos(a)*EN['inner_r']*0.5,EN['zc']+math.sin(a)*EN['inner_r']*0.5))
    o.scale=(0.3,EN['inner_r']*0.95,EN.get('spoke_w',0.13)); o.rotation_euler=(a,0,0)
if EN.get('rim_r'):
    o=prim('torus',M['cream'],major_radius=EN['rim_R'],minor_radius=EN['rim_r'],major_segments=64,minor_segments=16,location=(EN['rim_x'],0,EN['zc'])); o.rotation_euler=(0,math.pi/2,0)
if EN.get('n_pods2'):
    for k in range(EN['n_pods2']):
        a=2*math.pi*(k+0.5)/EN['n_pods2']
        prim('sph',M['exhaust'],radius=EN['pod_r']*0.8,segments=12,ring_count=8,location=(EN['disk_x']-0.12,math.cos(a)*EN['pod_ring2'],EN['zc']+math.sin(a)*EN['pod_ring2']))
for k in range(EN['n_pods']):
    a=2*math.pi*k/EN['n_pods']
    o=prim('cyl',M['exhaust'],radius=EN['pod_r'],depth=EN['pod_len'],vertices=16,
           location=(EN['disk_x']-EN['pod_len']/2,math.cos(a)*EN['pod_ring'],EN['zc']+math.sin(a)*EN['pod_ring']))
    o.rotation_euler=(0,math.pi/2,0)
    o=prim('sph',M['exhaust'],radius=EN['pod_r'],segments=16,ring_count=8,
           location=(EN['disk_x']-EN['pod_len'],math.cos(a)*EN['pod_ring'],EN['zc']+math.sin(a)*EN['pod_ring']))

# ---------- studio
w=bpy.data.worlds.new('W'); scene.world=w; w.use_nodes=True
bg=w.node_tree.nodes['Background']; bg.inputs[0].default_value=srgb(P['bg']); bg.inputs[1].default_value=P['world_str']
def area(name,loc,size,energy,target=(0,0,0)):
    l=bpy.data.lights.new(name,'AREA'); l.size=size; l.energy=energy
    o=bpy.data.objects.new(name,l); scene.collection.objects.link(o); o.location=loc
    d=Vector(target)-Vector(loc); o.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    o.visible_glossy=P.get('lights_glossy',True)
for L_ in P['lights']: area(*L_)
scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=SAMPLES
scene.cycles.use_denoising=True; scene.cycles.denoiser='OPENIMAGEDENOISE'
scene.view_settings.view_transform=P.get('vt','Standard')
scene.render.resolution_x=P.get('rx',848); scene.render.resolution_y=P.get('ry',304)
scene.render.film_transparent=False
cam_d=bpy.data.cameras.new('Cam'); cam=bpy.data.objects.new('Cam',cam_d); scene.collection.objects.link(cam); scene.camera=cam

os.makedirs(f'{HERE}/renders/{ROUND}',exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=f'{HERE}/planet_express_{ROUND}.blend')
for name,cv in P['cams'].items():
    if VIEWS and name not in VIEWS: continue
    out=f'{HERE}/renders/{ROUND}/{name}.png'
    tgt=Vector(cv['t']); az=math.radians(cv['az']); el=math.radians(cv['el'])
    cam.location=tgt+cv['d']*Vector((math.cos(el)*math.cos(az),math.cos(el)*math.sin(az),math.sin(el)))
    q=(tgt-cam.location).to_track_quat('-Z','Y'); cam.rotation_euler=q.to_euler()
    cam.rotation_euler.rotate_axis('Z',math.radians(cv.get('roll',0)))
    cam_d.lens=cv['lens']; cam_d.sensor_width=36
    cam_d.shift_x=cv.get('sx',0); cam_d.shift_y=cv.get('sy',0)
    scene.render.filepath=out; bpy.ops.render.render(write_still=True)
    print('RENDERED',out,flush=True)
