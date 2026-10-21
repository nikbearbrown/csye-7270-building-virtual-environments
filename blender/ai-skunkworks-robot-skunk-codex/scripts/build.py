"""AI Skunkworks robot skunk — image-based first study, Blender 4.2.
Axes: X left/right; front -Y; Z up. Arbitrary design units, no physical scale evidence.
Run: blender --background --python scripts/build.py [-- --draft]
"""
import bpy, math, json, sys
from pathlib import Path
from mathutils import Vector
from math import sin,cos,pi
ROOT=Path(__file__).resolve().parents[1];DRAFT='--draft' in sys.argv
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
 if c.name!='Collection' and c.users==0:bpy.data.collections.remove(c)
model=bpy.data.collections.new('SKUNK • editable parts');bpy.context.scene.collection.children.link(model)
studio=bpy.data.collections.new('STUDIO • not exported');bpy.context.scene.collection.children.link(studio)
def mat(n,c,metal=0,rough=.4):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
ivory=mat('Ivory ceramic • inferred',(.73,.75,.69),.28,.32)
white=mat('Warm white stripe • inferred',(.91,.9,.79),.1,.4)
black=mat('Graphite shell • inferred',(.035,.045,.052),.5,.34)
rubber=mat('Joint rubber',(.012,.017,.02),.05,.6)
steel=mat('Brushed joint metal',(.28,.34,.36),.8,.27)
lens=mat('Smoked blue optical glass • inferred',(.045,.17,.21),.65,.18)
light=mat('Pale optical iris',(.48,.83,.82),.45,.22)
def link(o,n,m,coll=model):
 o.name=n
 for c in list(o.users_collection):c.objects.unlink(o)
 coll.objects.link(o)
 if m:o.data.materials.append(m)
 return o
def smooth(o):
 if o.type=='MESH':
  for f in o.data.polygons:f.use_smooth=True
 return o
def bevel(o,w=.06,seg=3):
 b=o.modifiers.new('Editable softened edges','BEVEL');b.width=w;b.segments=seg
 n=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o
def uv(n,loc,scale,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=loc);o=link(bpy.context.object,n,m);o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return smooth(o)
def box(n,loc,scale,m,b=.07):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=link(bpy.context.object,n,m);o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if b:bevel(o,b)
 return o
def cyl(n,a,b,r,m,r2=None):
 a,b=Vector(a),Vector(b);v=b-a;bpy.ops.mesh.primitive_cone_add(vertices=40,radius1=r,radius2=r if r2 is None else r2,depth=v.length,location=(a+b)/2);o=link(bpy.context.object,n,m);o.rotation_euler=v.to_track_quat('Z','Y').to_euler();bevel(o,.025,3);return smooth(o)
def ring(n,loc,major,minor,m,normal=(0,0,1)):
 bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=48,minor_segments=12,location=loc);o=link(bpy.context.object,n,m);o.rotation_euler=Vector(normal).to_track_quat('Z','Y').to_euler();return smooth(o)
def line(n,pts,r,m):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.resolution_u=16;c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
 for p,co in zip(s.bezier_points,pts):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(n,c);model.objects.link(o);c.materials.append(m);return o
def mesh(n,vs,fs,m):
 d=bpy.data.meshes.new(n);d.from_pydata(vs,[],fs);d.update();o=bpy.data.objects.new(n,d);model.objects.link(o);d.materials.append(m);return o
def profile(n,yz,width,m,b=.07,x=0):
 vs=[(x+s*width/2,y,z) for s in [-1,1] for y,z in yz];L=len(yz);fs=[tuple(reversed(range(L))),tuple(range(L,2*L))]+[(i,(i+1)%L,(i+1)%L+L,i+L) for i in range(L)];return bevel(mesh(n,vs,fs,m),b)
def loft(n,rows,m):
 # rows: (x,y,z, x-radius,z-radius), sections normal to Y
 N=40;vs=[]
 for x,y,z,rx,rz in rows:
  vs.extend((x+rx*cos(2*pi*j/N),y,z+rz*sin(2*pi*j/N)) for j in range(N))
 fs=[tuple(reversed(range(N)))]+[(i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j) for i in range(len(rows)-1) for j in range(N)]+[tuple(range((len(rows)-1)*N,len(rows)*N))]
 return smooth(mesh(n,vs,fs,m))
# boots, leg mechanics, hip plates
for s,side in [(-1,'L'),(1,'R')]:
 x=s*.72
 sole=uv(side+' boot sole',(x,-.42,.28),(.64,1.12,.25),rubber)
 boot=loft(side+' boot armored toe',[(x,-1.5,.48,.27,.25),(x,-1.42,.57,.49,.4),(x,-1.1,.66,.59,.48),(x,-.5,.73,.6,.56),(x,.25,.78,.48,.6),(x,.49,.65,.35,.39)],ivory)
 box(side+' boot toe brow',(x,-1.35,.73),(.7,.16,.13),steel,.04)
 line(side+' boot seam',[(x+s*.43,-1.28,.68),(x+s*.54,-.83,.88),(x+s*.5,-.55,.8),(x+s*.44,-.4,1.12),(x+s*.38,.2,1.18)],.025,black)
 box(side+' toe inset',(x-s*.22,-1.38,.66),(.19,.07,.16),black,.025)
 cyl(side+' shin core',(x,.02,1.04),(x+s*.02,.08,2.08),.29,steel)
 uv(side+' shin armor',(x,-.08,1.48),(.43,.42,.7),ivory)
 cyl(side+' ankle axle',(x-s*.46,.02,1.13),(x+s*.51,.02,1.13),.31,black)
 ring(side+' ankle bearing',(x+s*.54,.02,1.13),.25,.055,steel,(s,0,0));cyl(side+' ankle hub',(x+s*.53,.02,1.13),(x+s*.59,.02,1.13),.11,ivory)
 for z in [1.48,1.68]:uv(side+' shin rivet',(x+s*.35,-.29,z),(.045,.035,.045),steel)
 uv(side+' knee joint',(x,-.05,2.13),(.38,.36,.35),rubber)
 knee=uv(side+' vented kneecap',(x,-.35,2.19),(.43,.18,.28),steel)
 for z,w in [(2.08,.25),(2.19,.32),(2.29,.24)]:line(side+' knee vent',[(x-w,-.51,z),(x,-.55,z-.025),(x+w,-.51,z)],.023,black)
 cyl(side+' thigh skeleton',(x,.04,2.3),(s*.52,.12,3.25),.3,rubber)
 thigh=uv(side+' thigh armor',(s*.66,-.02,2.82),(.48,.49,.7),ivory);thigh.rotation_euler[1]=s*-.18
 line(side+' thigh plate seam',[(s*.92,-.4,2.5),(s*1.03,-.37,2.9),(s*.83,-.42,3.24)],.028,black)
 cyl(side+' hip pin',(s*.36,.04,3.35),(s*.81,.04,3.35),.3,steel)
# pelvis and torso, armor is split around abdominal bellows
uv('Pelvis flexible core',(0,.1,3.38),(.7,.45,.52),rubber)
uv('Pelvis front armor',(0,-.21,3.42),(.65,.3,.43),ivory)
for z,w in [(3.71,.64),(3.91,.57),(4.11,.59),(4.30,.68)]:
 box('Abdomen graphite separator',(0,-.02,z),(w*2,.68,.16),rubber,.07)
 box('Floating abdominal armor',(0,-.37,z+.025),(w*1.8,.16,.13),ivory,.055)
uv('Thorax under-shell',(0,.02,4.83),(.89,.57,.9),black)
shield=uv('Broad single chest shield',(0,-.12,4.99),(.86,.52,.7),ivory)
# Taper the lower portion of the shield toward the waist.
for v in shield.data.vertices:
 if v.co.z<0:v.co.x*=1+v.co.z*.3
line('Chest center split',[(0,-.54,5.5),(.12,-.64,5.22),(0,-.665,4.96),(-.1,-.61,4.71)],.023,black)
for sign in [-1,1]:
 line('Chest lower edge',[(sign*.08,-.55,4.56),(sign*.39,-.53,4.6),(sign*.67,-.43,4.8)],.022,black)
# neck and shoulders
cyl('Neck swivel',(0,.05,5.39),(0,.05,5.94),.26,steel)
for z in [5.5,5.66,5.81]:ring('Neck collar',(0,.05,z),.27,.045,rubber)
for s,side in [(-1,'L'),(1,'R')]:
 shoulder=(s*.98,.02,5.26);elbow=(s*1.28,-.04,4.28);wrist=(s*1.43,-.32,3.63)
 uv(side+' shoulder spherical joint',shoulder,(.42,.43,.43),rubber)
 o=uv(side+' shoulder cap',(s*.99,-.03,5.34),(.49,.47,.46),ivory)
 ring(side+' shoulder socket',(s*1.39,.08,5.23),.26,.055,steel,(s,0,0))
 cyl(side+' shoulder hub',(s*1.37,.08,5.23),(s*1.46,.08,5.23),.1,black)
 cyl(side+' upper arm',shoulder,elbow,.31,ivory,.36)
 uv(side+' elbow',elbow,(.34,.34,.3),rubber)
 cyl(side+' forearm inner piston',elbow,wrist,.26,steel)
 o=uv(side+' forearm shell',(s*1.37,-.18,3.96),(.39,.4,.51),ivory);o.rotation_euler[1]=s*-.12
 # broad, tall projecting forearm blade from drawing, behind glove
 yz=[(.12,3.01),(.47,3.2),(.64,3.72),(.59,4.37),(.43,4.6),(.35,4.17),(.04,3.63)]
 profile(side+' forearm dorsal fin',yz,.15,black,.045,x=s*1.55)
 profile(side+' forearm fin face',[(y-.025,z-.02) for y,z in yz],.035,ivory,.025,x=s*1.65)
 # huge gauntlets, three curled segmented fingers and thumb
 uv(side+' glove palm',(s*1.43,-.35,3.25),(.54,.38,.57),ivory)
 ring(side+' wrist trim',(s*1.42,-.28,3.64),.32,.06,black)
 for j in range(3):
  xx=s*(1.05+j*.33)
  uv(side+f' curled finger {j+1}',(xx,-.57,2.96),(.19,.26,.34),ivory)
  box(side+f' knuckle frame {j+1}',(xx,-.78,3.16),(.3,.19,.29),black,.065)
  box(side+f' knuckle cap {j+1}',(xx,-.895,3.19),(.25,.08,.25),ivory,.035)
  line(side+f' finger seam {j+1}',[(xx-.12,-.76,2.87),(xx,-.81,2.84),(xx+.12,-.76,2.87)],.021,steel)
 uv(side+' bent thumb',(s*.96,-.48,3.28),(.23,.27,.35),ivory)
 # conspicuous glove piston running toward forearm
 a=(s*1.68,-.5,3.5);b=(s*1.72,-.29,4.05)
 cyl(side+' glove hydraulic barrel',a,b,.18,steel)
 cyl(side+' glove piston sleeve',(s*1.68,-.51,3.52),(s*1.71,-.33,3.98),.21,ivory)
 cyl(side+' glove piston rod',(s*1.71,-.33,3.98),(s*1.74,-.21,4.27),.065,steel)
 box(side+' piston cap',(s*1.74,-.22,4.28),(.24,.13,.09),black,.02)
 line(side+' glove cable',[(s*1.65,-.5,3.5),(s*1.82,-.47,3.3),(s*1.81,-.64,3.16)],.045,rubber)
# backpack silhouette and shoulder hoses
box('Backpack chassis',(0,.72,4.55),(1.28,.65,1.91),black,.15)
box('Backpack rear plate',(0,1.07,4.56),(1.13,.16,1.66),ivory,.1)
for z in [4.1,4.55,5.01]:
 box('Pack horizontal vent',(0,1.168,z),(.73,.035,.055),black,.015)
for s,side in [(-1,'L'),(1,'R')]:
 cyl(side+' pack top connector',(s*.43,.74,5.4),(s*.43,.74,5.68),.12,steel)
 line(side+' shoulder hose',[(s*.43,.74,5.65),(s*.67,.52,5.84),(s*.98,-.01,5.63),(s*1.11,-.24,5.42)],.065,black)
 ring(side+' hose shoulder mount',(s*1.11,-.26,5.43),.12,.035,steel,(0,-1,0))
# head, muzzle, cheek plates; muzzle is a long tapered skunk snout, not a human face
uv('Head skull',(0,.02,6.42),(.67,.62,.74),black)
loft('Muzzle ceramic bridge',[(0,.08,6.42,.59,.53),(0,-.38,6.38,.57,.48),(0,-.72,6.25,.43,.33),(0,-1.1,6.2,.25,.19),(0,-1.48,6.27,.13,.11)],ivory)
uv('Round black nose',(0,-1.56,6.3),(.21,.18,.19),black)
uv('Nose highlight',( .065,-1.7,6.37),(.055,.023,.035),white)
loft('Lower jaw',[(0,.04,6.06,.47,.25),(0,-.43,6.03,.45,.2),(0,-.83,6.08,.32,.11),(0,-1.2,6.16,.15,.035)],ivory)
for s,side in [(-1,'L'),(1,'R')]:
 # ocular side face, axis angled toward the muzzle
 normal=Vector((s*.78,-.63,.03));center=Vector((s*.47,-.46,6.59))+normal*.18
 uv(side+' pale eye mask',(s*.44,-.34,6.64),(.28,.34,.47),ivory)
 cyl(side+' dark eye socket',center,center+normal*.13,.22,black)
 ring(side+' orbital rim',center+normal*.14,.185,.035,steel,normal)
 cyl(side+' optical iris',center+normal*.15,center+normal*.165,.13,light)
 cyl(side+' pupil',center+normal*.168,center+normal*.18,.071,black)
 uv(side+' eye glint',center+normal*.19+Vector((0,0,.06)),(.035,.035,.04),white)
 line(side+' expressive brow',[(s*.39,-.68,6.89),(s*.55,-.54,6.94),(s*.64,-.32,6.83)],.065,black)
 line(side+' cheek panel seam',[(s*.42,-.73,6.35),(s*.55,-.56,6.25),(s*.6,-.18,6.2),(s*.5,.32,6.26)],.022,black)
 # smiling mouth with a few mechanical teeth
 pts=[(s*.15,-1.21,6.13),(s*.29,-.98,6.04),(s*.4,-.72,5.99),(s*.45,-.43,6.04)]
 line(side+' smile dark opening',pts,.045,black)
 for j in range(4):
  t=j/4;y=-1.08+t*.6;x=s*(.21+t*.24);z=6.065-.06*sin(t*pi)
  box(side+' tooth',(x,y,z),(.07,.13,.065),white,.015)
 for y,x,z in [(-1.14,.22,6.22),(-.94,.32,6.18)]:uv(side+' muzzle dot',(s*x,y,z),(.035,.04,.035),black)
 # ears behind lenses
 ear=uv(side+' ear shell',(s*.68,.24,6.86),(.22,.16,.29),ivory);ear.rotation_euler[1]=s*-.3
 uv(side+' ear inner',(s*.71,.095,6.87),(.12,.055,.17),black)
# goggle strap and two mechanical lenses lifted onto forehead
line('Goggle headband',[(-.61,.26,7.01),(-.62,-.22,7.07),(0,-.55,7.1),(.62,-.22,7.07),(.61,.26,7.01)],.085,steel)
for s,side in [(-1,'L'),(1,'R')]:
 c=Vector((s*.34,-.43,7.15));n=Vector((0,-.7,.71))
 cyl(side+' goggle housing',c,c+n*.13,.255,black)
 ring(side+' goggle silver rim',c+n*.14,.22,.055,steel,n)
 cyl(side+' goggle glass',c+n*.145,c+n*.16,.194,lens)
 line(side+' goggle lens glint',[(s*.34-.1,-.55,7.38),(s*.34+.07,-.55,7.39)],.018,white)
box('Goggle bridge',(0,-.51,7.18),(.2,.14,.12),steel,.04)
# swept jagged mane / crest, a custom closed profile rather than primitive spikes
crest=[(-.36,6.85),(-.69,7.28),(-.78,7.85),(-.53,7.56),(-.43,8.03),(-.29,7.7),(-.02,8.28),(.7,8.72),(.47,8.12),(1.02,8.24),(.76,7.87),(1.42,7.98),(1.18,7.56),(1.61,7.67),(1.32,7.33),(1.73,7.4),(1.4,7.09),(1.76,7.13),(1.34,6.82),(1.66,6.76),(1.14,6.5),(1.44,6.39),(.9,6.24),(1.13,6.08),(.57,6.14),(.39,6.38)]
# Rounded mane with a thin perimeter and convex sides, keeping pointed swept tips.
def mane(yz):
 boundary=[]
 for i in range(len(yz)):
  p0=Vector(yz[(i-1)%len(yz)]);p1=Vector(yz[i]);p2=Vector(yz[(i+1)%len(yz)]);p3=Vector(yz[(i+2)%len(yz)])
  for k in range(5):
   t=k/5;boundary.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
 center=Vector((.45,7.1));L=len(boundary);vs=[];fs=[]
 radii=[.06,.25,.5,.72,.88,.97,1]
 for sign in [-1,1]:
  for r in radii:
   for q in boundary:
    co=center+(q-center)*r
    # Smooth convex cheek of the mane; narrow at the high quiff.
    width=.57*math.sqrt(max(0,1-r*r))+.012
    vs.append((sign*width,co.x,co.y))
 for side in range(2):
  base=side*L*len(radii)
  fs.append(tuple(base+j for j in range(L)))
  for k in range(len(radii)-1):
   for j in range(L):fs.append((base+k*L+j,base+k*L+(j+1)%L,base+(k+1)*L+(j+1)%L,base+(k+1)*L+j))
 for j in range(L):
  a=(len(radii)-1)*L+j;b=(2*len(radii)-1)*L+j
  fs.append((a,(len(radii)-1)*L+(j+1)%L,(2*len(radii)-1)*L+(j+1)%L,b))
 o=smooth(mesh('Sculpted swept mane • convex editable mesh',vs,fs,white))
 # Recalculate consistently for export and shading.
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
 return o
mane(crest)
# A few graphite groove curves describe the sweep without pretending to be fur.
for sign in [-1,1]:
 line('Mane swept groove',[(sign*.57,.19,6.88),(sign*.55,.65,7.14),(sign*.4,1.05,7.51)],.019,steel)
 line('Mane lower groove',[(sign*.52,.3,6.54),(sign*.49,.76,6.7),(sign*.32,1.22,6.92)],.018,steel)
# Enlarge gauntlets as an assembly around their wrist attachment.
for o in list(model.objects):
 if any(token in o.name for token in ['glove','curled finger','knuckle','finger seam','bent thumb','piston cap']):
  sign=-1 if o.name.startswith('L ') else 1
  pivot=Vector((sign*1.42,-.28,3.64));o.location=pivot+(o.location-pivot)*1.16;o.scale*=1.16
# Curved, thick skunk tail with a continuous stripe. Catmull-Rom center line.
control=[(0,.52,3.26,.25,.24),(0,1.15,3.0,.36,.32),(0,2.05,3.03,.52,.52),(0,2.72,3.55,.62,.68),(0,3.06,4.42,.62,.72),(0,3.49,4.86,.44,.49),(0,4.02,4.62,.03,.035)]
points=[]
for i in range(len(control)-1):
 p0=Vector(control[max(0,i-1)]);p1=Vector(control[i]);p2=Vector(control[i+1]);p3=Vector(control[min(len(control)-1,i+2)])
 for k in range(10):
  t=k/10;points.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
points.append(Vector(control[-1]));vs=[];N=48
for i,p in enumerate(points):
 tangent=Vector(points[min(i+1,len(points)-1)][:3])-Vector(points[max(0,i-1)][:3]);tangent.normalize();norm=Vector((0,-tangent.z,tangent.y))
 for j in range(N):
  a=2*pi*j/N;v=Vector(p[:3])+Vector((cos(a)*p[3],0,0))+norm*sin(a)*p[4];vs.append(tuple(v))
fs=[tuple(reversed(range(N)))]+[(i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j) for i in range(len(points)-1) for j in range(N)]+[tuple(range((len(points)-1)*N,len(points)*N))]
tail=smooth(mesh('Sweeping skunk tail • continuous loft',vs,fs,black));tail.data.materials.append(white)
for f in tail.data.polygons:
 if len(f.vertices)==4:
  j=f.vertices[0]%N
  if abs(cos(2*pi*(j+.5)/N))<.53:f.material_index=1
# studio is separate from exported character
floor=mat('Studio floor',(.14,.17,.19),.05,.7)
bpy.ops.mesh.primitive_plane_add(size=2000,location=(0,0,.015));link(bpy.context.object,'Studio floor',floor,studio)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24 if DRAFT else 48;scene.cycles.use_denoising=True
scene.world.color=(.24,.24,.24)
def area(n,loc,power,size,color):
 d=bpy.data.lights.new(n,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(n,d);studio.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,4))-o.location).to_track_quat('-Z','Y').to_euler()
area('Large warm key',(4,-7,11),1700,6,(1,.89,.77));area('Cool fill',(-5,-3,7),1300,5,(.69,.82,1));area('Tail rim',(3,6,10),2100,5,(.85,.93,1))
def camera(n,loc,target,scale):
 d=bpy.data.cameras.new(n);o=bpy.data.objects.new(n,d);studio.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=scale;return o
cams={
 'hero':camera('CAM hero / reference A',(15,-12,8),(0,.7,4.35),10.6),
 'side':camera('CAM side / reference B',(16,-.4,4.9),(0,.85,4.35),10.3),
 'front':camera('CAM front',(0,-20,6.4),(0,.2,4.3),10),
 'rear':camera('CAM rear quarter',(-11,16,9),(0,1,4.3),10.7),
 'head':camera('CAM face detail',(10,-14,8.7),(0,-.05,6.95),3.8),
 'gauntlet':camera('CAM glove detail',(9,-13,6),(1.0,-.15,3.58),3.25)}
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.resolution_percentage=100
scene.render.resolution_x=900 if DRAFT else 1400;scene.render.resolution_y=1000 if DRAFT else 1550
scene.camera=cams['hero'];scene['model_status']='First interpretation from two line drawings; human review pending.';scene['color_status']='Graphite and ivory colors inferred, not specified by line-art references.'
# Store a convenient material-preview viewport.
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_distance=13;a.spaces.active.region_3d.view_location=(0,.5,4.3)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'ai-skunkworks-robot-skunk.blend'))
# Export only character, applying modifiers. Curves converted in export duplicate scene later.
# Export evaluated mesh copies so curves, hoses and seams also survive in GLB.
bpy.ops.object.select_all(action='DESELECT')
export_objects=[];dg=bpy.context.evaluated_depsgraph_get()
for source in list(model.objects):
 if source.type not in {'MESH','CURVE'}:continue
 data=bpy.data.meshes.new_from_object(source.evaluated_get(dg),depsgraph=dg)
 obj=bpy.data.objects.new(source.name,data);scene.collection.objects.link(obj);obj.matrix_world=source.matrix_world;obj.select_set(True);export_objects.append(obj)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'ai-skunkworks-robot-skunk.glb'),export_format='GLB',use_selection=True,export_apply=False,export_cameras=False,export_lights=False)
for obj in export_objects:
 data=obj.data;bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(data)
# evaluated geometry census (curves included)
dg=bpy.context.evaluated_depsgraph_get();tri=0;vcount=0;bounds=[];mats=set();count=0
for o in model.objects:
 if o.type in {'MESH','CURVE'}:
  ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();tri+=len(me.loop_triangles);vcount+=len(me.vertices);count+=1
  bounds.extend(tuple(o.matrix_world@v.co) for v in me.vertices);mats.update(m.name for m in o.data.materials if m);ev.to_mesh_clear()
lo=[min(p[i] for p in bounds) for i in range(3)];hi=[max(p[i] for p in bounds) for i in range(3)]
(ROOT/'audit.json').write_text(json.dumps({'blender_version':bpy.app.version_string,'mesh_objects':sum(o.type=='MESH' for o in model.objects),'curve_objects':sum(o.type=='CURVE' for o in model.objects),'evaluated_geometry_objects':count,'evaluated_triangles':tri,'evaluated_vertices':vcount,'materials':len(mats),'material_names':sorted(mats),'bounds_min':lo,'bounds_max':hi,'dimensions':[hi[i]-lo[i] for i in range(3)],'units':'arbitrary design units; scale not established by drawings','rigged':False,'animated':False,'image_textures':False},indent=2))
for name in (['hero','side'] if DRAFT else list(cams)):
 scene.camera=cams[name];scene.render.filepath=str(ROOT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)
print('BUILD COMPLETE',ROOT)
