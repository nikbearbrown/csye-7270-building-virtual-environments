"""Enterprise exterior reconstructed from user-supplied Constitution-class plans.
Run via MCP execute_code in a fresh Blender 4.2+ scene. +Y aft, +Z dorsal, metres.
No image-generation or downloaded ship mesh is used.
"""
import bpy, math, json, os
from pathlib import Path
from mathutils import Vector
from math import sin,cos,pi
ROOT=Path(os.environ.get('ENTERPRISE_OUTPUT','/Users/bear/Downloads/enterprise-build'))
ROOT.mkdir(exist_ok=True,parents=True)
for sub in ['renders','compare','references','scripts']: (ROOT/sub).mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):
    if col.name != 'Collection' and col.users==0: bpy.data.collections.remove(col)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
ship=bpy.data.collections.new('USS ENTERPRISE • NCC-1701'); scene.collection.children.link(ship)
studio=bpy.data.collections.new('STUDIO • cameras and lights');scene.collection.children.link(studio)
def mat(name,color,metal=0,rough=.5,emission=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    if emission: p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
    return m
hull=mat('01 • Warm pearl-gray hull',(.43,.49,.50),.16,.46)
edge=mat('02 • Saucer edge and machinery',(.39,.46,.48),.25,.48)
panel=mat('03 • Restrained panel lines',(.30,.37,.38),.12,.55)
dark=mat('04 • Charcoal lettering and vents',(.018,.027,.034),.12,.49)
red=mat('05 • Starfleet vermilion',(.55,.035,.018),.16,.42)
gold=mat('06 • Copper navigation deflector',(.48,.24,.075),.68,.30)
amber=mat('07 • Bussard amber glass',(.65,.055,.008),.25,.30,.45)
window=mat('08 • Warm cabin lights',(.82,.76,.53),.08,.30,1.2)
win_dark=mat('09 • Unlit windows',(.035,.065,.075),.15,.3)
green=mat('10 • Starboard navigation light',(.018,.63,.23),.08,.2,3)
navred=mat('11 • Port navigation light',(.9,.025,.012),.08,.2,3)
white=mat('12 • Sensor glass',(.65,.78,.81),.35,.23,.2)
materials=[hull,edge,panel,dark,red,gold,amber,window,win_dark,green,navred,white]
def link(obj,material=None,collection=ship):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    collection.objects.link(obj)
    if material: obj.data.materials.append(material)
    return obj
def mesh(name,verts,faces,material,smooth=False):
    d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update();o=bpy.data.objects.new(name,d);ship.objects.link(o);d.materials.append(material)
    if smooth:
        for p in d.polygons:p.use_smooth=True
    return o
def lathe(name,profile,material,axis='Z',center=(0,0,0),n=128):
    verts=[]
    for r,z in profile:
        for j in range(n):
            a=2*pi*j/n
            p=(r*cos(a),r*sin(a),z) if axis=='Z' else (r*cos(a),z,r*sin(a))
            verts.append(tuple(p[k]+center[k] for k in range(3)))
    faces=[]
    for i in range(len(profile)-1):
        for j in range(n):
            a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
    return mesh(name,verts,faces,material,True)
def sphere(name,loc,scale,material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;link(o,material)
    for p in o.data.polygons:p.use_smooth=True
    return o
def box(name,loc,size,material,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);link(o,material)
    if bevel:
        b=o.modifiers.new('Soft machined edges','BEVEL');b.width=bevel;b.segments=3
        o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return o
def tube(name,pts,r,material,closed=False):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=1;c.bevel_depth=r;c.bevel_resolution=1
    s=c.splines.new('POLY');s.points.add(len(pts)-1)
    for p,co in zip(s.points,pts):p.co=(*co,1)
    s.use_cyclic_u=closed;o=bpy.data.objects.new(name,c);ship.objects.link(o);c.materials.append(material);return o
def ring(name,r,z,material,thick=.06,center=(0,0,0),axis='Z'):
    pts=[]
    for j in range(192):
        a=2*pi*j/192
        p=(r*cos(a),r*sin(a),z) if axis=='Z' else (r*cos(a),z,r*sin(a))
        pts.append(tuple(p[k]+center[k] for k in range(3)))
    return tube(name,pts,thick,material,True)
def prism(name,outline,half,material):
    # Outline in YZ, extruded across X.
    verts=[(x,y,z) for x in [-half,half] for y,z in outline];n=len(outline)
    faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
    o=mesh(name,verts,faces,material);b=o.modifiers.new('Rounded leading edges','BEVEL');b.width=.42;b.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o
def text(name,body,loc,size,material,rot=(0,0,0),align='CENTER'):
    c=bpy.data.curves.new(name,'FONT');c.body=body;c.size=size;c.align_x=align;c.align_y='CENTER';c.extrude=.008;c.resolution_u=5
    o=bpy.data.objects.new(name,c);ship.objects.link(o);o.location=loc;o.rotation_euler=rot;c.materials.append(material)
    return o
# Primary hull: a shallow lens with a distinct bevelled rim and lower dish.
saucer_profile=[(0,8.2),(5,8.2),(8,8.7),(11,9.8),(16,12.3),(22,15.5),(28,17.8),(34,19.0),(45,19.1),(60.7,19.1),(62.4,19.5),(64,24.8),(63.5,25.2),(60.0,25.35),(55,25.45),(49,25.7),(42,26.1),(35,26.8),(28,27.7),(22,28.5),(17,29.0),(0,29.0)]
lathe('Saucer • continuous contoured primary hull',saucer_profile,hull,n=192)
# Low-contrast hull grids on upper and lower surfaces.
def upper(r):
    arr=[(17,29),(22,28.5),(28,27.7),(35,26.8),(42,26.1),(49,25.7),(55,25.45),(60,25.35),(63.5,25.2)]
    for (a,z),(b,w) in zip(arr,arr[1:]):
        if a<=r<=b:return z+(w-z)*(r-a)/(b-a)
    return 29 if r<17 else 25.2
for r in [20,28,36,44,52,60]:ring('Saucer dorsal concentric seam',r,upper(r)+.025,panel,.035)
for j in range(36):
    a=2*pi*j/36;pts=[(r*cos(a),r*sin(a),upper(r)+.025) for r in [18,22,28,35,42,49,55,60,63]]
    tube('Saucer radial panel seam',pts,.026,panel)
ring('Saucer upper rim seam',63.65,24.6,panel,.07)
ring('Saucer lower rim seam',62.0,19.45,edge,.09)
for r,z in [(10,9.5),(16,12.32),(22,15.53),(28,17.84),(34,19.03),(45,19.14),(57,19.14)]:ring('Ventral panel ring',r,z-.03,panel,.04)
lathe('Ventral sensor housing',[(0,7.65),(5,7.65),(7.4,8.05),(7.6,8.7),(0,8.7)],edge)
sphere('Ventral sensor dome',(0,0,7.75),(4.3,4.3,.85),white)
# Bridge decks with flatter sloping cap, aft turbolift bustle.
lathe('Bridge • B C deck superstructure',[(0,28.8),(18.5,28.8),(18.3,30),(16.4,33.8),(14.0,35),(0,35)],hull)
lathe('Bridge upper drum',[(0,35),(7.5,35),(7.5,37.1),(6.5,37.4),(0,37.4)],hull)
sphere('Bridge sensor cap',(0,0,37.35),(5.2,5.2,1.2),white)
box('Bridge aft elevator',(0,7.8,35.7),(3.5,4.2,3.3),hull,.5)
# Neck swept aft in side view. Multiple horizontal window rows.
prism('Interconnecting dorsal • swept neck',[(25,19.2),(54,21.1),(83,-2.2),(54,-2.2)],2.7,hull)
# Secondary hull loft: circular sections taper and lift at the stern.
stations=[(39,9.7,-14.5),(42,12.6,-14.5),(48,14.2,-14.7),(54,14.6,-14.8),(62,14.6,-14.8),(79,13.4,-14.2),(97,11.5,-12.8),(116,9.0,-11),(124,8.4,-9.1),(136,7.6,-7.6),(143,5.6,-7.0)]
verts=[];N=128
for y,r,z in stations:
    for j in range(N):
        a=2*pi*j/N;verts.append((r*cos(a),y,z+r*sin(a)))
faces=[]
for i in range(len(stations)-1):
    for j in range(N):a=i*N+j;b=i*N+(j+1)%N;faces.append((a,a+N,b+N,b))
faces += [tuple(range(N-1,-1,-1)),tuple(range((len(stations)-1)*N,len(stations)*N))]
mesh('Engineering hull • tapered compound loft',verts,faces,hull,True)
for y,r,z in [stations[1],stations[3],stations[5],stations[7]]:ring('Engineering hull ring',r+.025,y,panel,.055,(0,0,z),'Y')
# Stacked forward collar and bronze concave deflector dish.
lathe('Deflector mounting collar',[(0,37.5),(8.8,37.5),(8.8,39),(10.2,39),(10.2,41),(0,41)],edge,'Y',(0,0,-14.5))
lathe('Deflector dish • shallow concave copper',[(0,35.5),(2,35.3),(4,34.8),(6,34.0),(8.5,32.7),(8.6,32.3),(6,33.6),(4,34.3),(2,34.7),(0,34.9)],gold,'Y',(0,0,-14.5))
ring('Deflector rim',8.55,32.5,gold,.18,(0,0,-14.5),'Y')
lathe('Deflector center spike',[(0,27.8),(.22,27.8),(.40,34.8),(1.3,35.4),(0,35.4)],gold,'Y',(0,0,-14.5),64)
# Swept lateral support pylons; same longitudinal station as side blueprint.
for side,label in [(-1,'Port'),(1,'Starboard')]:
    quad=[(side*6.0,108,-9),(side*7.0,117,-9),(side*48,117,31),(side*48,107,31)]
    verts=[(x,y,z+d) for d in [-.7,.7] for x,y,z in quad]
    o=mesh(label+' • nacelle support pylon',verts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],hull)
    b=o.modifiers.new('Soft pylon edges','BEVEL');b.width=.4;b.segments=3;o.modifiers.new('Pylon weighted normals','WEIGHTED_NORMAL')
    tube(label+' pylon inlaid seam',[(side*7.5,112,-7.2),(side*46,112,29.8)],.07,panel)
# Nacelles, 154 m length, hemispherical forecaps, slightly tapered cylinders.
for side,label in [(-1,'Port'),(1,'Starboard')]:
    x=side*48;z=38.8
    profile=[(0,82),(8.65,82),(8.65,90),(8.4,96),(8.1,162),(7.8,193),(7.9,212),(7.5,218),(6.1,222),(3.5,225),(0,226)]
    lathe(label+' warp nacelle • main casing',profile,hull,'Y',(x,0,z),128)
    cap=[(0,71.8)]+[(8.56*sin(t*pi/2/16),82-10.2*cos(t*pi/2/16)) for t in range(1,17)]+[(0,82)]
    lathe(label+' Bussard collector',cap,amber,'Y',(x,0,z),128)
    for y in [82,84.1,86.6]:ring(label+' collector collar',8.72,y,edge,.23,(x,0,z),'Y')
    # Fine ribs behind front cap.
    for j in range(24):
        a=2*pi*j/24
        tube(label+' collector rib',[(x+8.72*cos(a),82.7,z+8.72*sin(a)),(x+8.72*cos(a),86.3,z+8.72*sin(a))],.11,gold)
    for y in [94,162,194,216]:ring(label+' nacelle casing seam',8.35 if y<190 else 7.9,y,panel,.05,(x,0,z),'Y')
    # Gray longitudinal inboard grille, copper slits.
    box(label+' inboard warp grille',(x-side*7.85,146,z),( .48,99,3.2),dark,.28)
    for dz in [-.85,0,.85]:box(label+' grille rail',(x-side*8.12,146,z+dz),(.16,96,.12),edge,.025)
    for yy in range(102,193,4):box(label+' grille transverse ribs',(x-side*8.20,yy,z),(.13,.28,2.9),edge,.03)
    box(label+' upper aft intercooler',(x,204,z+7.4),(3.0,28,2.2),edge,.7)
    box(label+' lower forward service box',(x,91,z-8.3),(3.7,11.5,1.8),edge,.45)
    # Aft nozzle with concentric cap and a dark central inset.
    lathe(label+' aft end ring',[(0,223),(5.8,223),(5.8,224.5),(0,224.5)],edge,'Y',(x,0,z))
    sphere(label+' aft sensor cap',(x,224.6,z),(4.5,1.7,4.5),hull)
    ring(label+' aft black ring',4.7,224.65,dark,.14,(x,0,z),'Y')
    # External pennant stripes and legible registry.
    outside=x+side*8.46
    for zz in [z-.28,z+.28]:tube(label+' red identification stripe',[(outside,100,zz),(outside,132,zz)],.11,red)
    arrow=[(outside,98,z),(outside,104,z+1.6),(outside,103,z+.45),(outside,133,z+.45),(outside,133,z-.45),(outside,103,z-.45),(outside,104,z-1.6)]
    mesh(label+' Starfleet pennant',arrow,[tuple(range(7))],red)
    text(label+' nacelle registry','NCC-1701',(outside+side*.06,151,z),4.1,dark,(pi/2,0,pi/2 if side==1 else -pi/2))
    tube(label+' trailing stripe',[(outside,169,z),(outside,187,z)],.13,red)
# Hangar at stern: segmented clamshell face, rim and landing shelf.
lathe('Shuttle bay stern rim',[(0,143),(5.6,143),(5.6,144),(0,144)],edge,'Y',(0,0,-7))
sphere('Shuttle bay clamshell doors',(0,144,-6.5),(5.15,.65,4.9),hull)
for xx in [-3.4,-1.7,0,1.7,3.4]:
    height=math.sqrt(max(0,4.9**2-(xx/5.15*4.9)**2))
    tube('Shuttle bay door segment',[(xx,144.65,-6.5-height),(xx,144.65,-6.5+height)],.08,panel)
box('Shuttle bay landing ledge',(0,144.3,-10.7),(12.6,4.5,.7),hull,.2)
for x in [-4,-2,0,2,4]:box('Hangar approach lights',(x,146.6,-10.2),(.45,.16,.23),window,.04)
sphere('Stern navigation beacon',(0,135,1),(1.0,1.0,.6),white)
# Aft saucer impulse housing.
box('Impulse drive housing',(0,60.1,22.4),(25,7.1,4.4),edge,.7)
for x in [-6.5,6.5]:
    box('Impulse exhaust inset',(x,63.7,22.6),(10,.30,2.5),dark,.35)
    for dx in [-3,-1,1,3]:box('Impulse exhaust red louvre',(x+dx,63.9,22.6),(.6,.17,1.8),red,.08)
# Window geometry batched per material keeps scene manageable.
window_batches={window:([],[]),win_dark:([],[])}
def pane(center,u,v,w,h,lit=True):
    verts,faces=window_batches[window if lit else win_dark];i=len(verts);c=Vector(center);U=Vector(u)*w/2;V=Vector(v)*h/2
    verts.extend([tuple(c-U-V),tuple(c+U-V),tuple(c+U+V),tuple(c-U+V)]);faces.append((i,i+1,i+2,i+3))
for j in range(150):
    a=2*pi*j/150
    # Leave aft drive section free.
    if sin(a)>.96:continue
    for dz in ([0] if j%7<4 else [-.8,.8]):pane((63.1*cos(a),63.1*sin(a),22+dz),(-sin(a),cos(a),0),(0,0,1),.72,.42,(j%5!=0))
for j in range(28):
    a=2*pi*j/28
    pane((17.25*cos(a),17.25*sin(a),32.3),(-sin(a),cos(a),0),(0,0,1),.9,.55,j%4!=0)
for side in [-1,1]:
    for row in range(5):
        z=3+row*3.2;ymin=53-row*3.1
        for j in range(4):pane((side*2.76,ymin+j*3.4,z),(0,1,0),(0,0,1),1.0,.65,(row+j)%3!=0)
    for iy,(y,r,z) in enumerate(stations[3:-1]):
        for dy in [-2,0,2]:
            for dz in [-5,0,5]:
                xr=math.sqrt(max(0,r*r-dz*dz))+.035
                pane((side*xr,y+dy,z+dz),(0,1,0),(0,0,1),.8,.55,(iy+int(dz))%3!=0)
for material,(vs,fs) in window_batches.items():mesh('Cabin windows • '+material.name,vs,fs,material)
# Dorsal registry arc, body label and navigation lamps.
for body,r,size,z in [('NCC-1701',43,7.2,26.3),('U.S.S. ENTERPRISE',30,2.5,27.6)]:
    spacing=size*.72/r
    for i,ch in enumerate(body):
        a=(i-(len(body)-1)/2)*spacing
        if ch!=' ':text('Saucer marking '+body+' '+str(i),ch,(r*sin(a),-r*cos(a),upper(r)+.13),size,dark,(0,0,a))
for side,label,material in [(-1,'Port',navred),(1,'Starboard',green)]:
    sphere(label+' saucer navigation light',(side*61.2,0,25.6),(.65,1.05,.35),material)
    # Engineering hull pennants, side-facing flat insignia.
    x=side*14.68
    mesh(label+' engineering red pennant',[(x,54,-13),(x,60,-10.6),(x,59,-12.6),(x,78,-12.6),(x,78,-13.4),(x,59,-13.4),(x,60,-15.4)],[tuple(range(7))],red)
    text(label+' engineering ship name','U.S.S. ENTERPRISE',(x,69,-9.7),1.4,dark,(pi/2,0,pi/2 if side==1 else -pi/2))
sphere('Forward running light',(0,-63.2,25.4),(.6,.6,.5),white)
# Convert details to real meshes and apply modifiers for consistent glTF export.
bpy.ops.object.select_all(action='DESELECT')
for o in list(ship.objects):o.select_set(True)
bpy.context.view_layer.objects.active=next(iter(ship.objects));bpy.ops.object.convert(target='MESH')
# Conform registry mesh vertices to the curved saucer (round-1 correction).
for o in ship.objects:
    if o.type=='MESH' and o.name.startswith('Saucer marking'):
        inv=o.matrix_world.inverted()
        for v in o.data.vertices:
            world=o.matrix_world@v.co
            world.z=upper(math.hypot(world.x,world.y))+.08
            v.co=inv@world
# Correct winding of longitudinal lathes for portable shading.
import bmesh
for o in ship.objects:
    if o.type=='MESH':
        bm=bmesh.new();bm.from_mesh(o.data)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# Add a master transform for rigid animation and named components for editing.
root=bpy.data.objects.new('ENTERPRISE • master transform',None);ship.objects.link(root)
for o in list(ship.objects):
    if o!=root:o.parent=root
root['construction']='Blueprint-based exterior reconstruction; no interior or rig.'
root['reference_note']='Main geometry follows user high-resolution Constitution-class side plan; NCC-1701 Enterprise markings substituted.'
# Studio.
world=bpy.data.worlds.new('Deep navy studio');scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.022,.032,.05,1);world.node_tree.nodes['Background'].inputs[1].default_value=.38

def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
def area(name,loc,power,color,size):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);studio.objects.link(o);o.location=loc;aim(o,(0,60,5));return o
area('Key softbox',(-110,-100,230),1500000,(.83,.91,1),180)
area('Starboard warm fill',(150,10,130),1100000,(1,.84,.69),150)
area('Aft cool rim',(-40,245,120),1800000,(.48,.66,1),120)
area('Ventral fill',(40,-40,-130),650000,(.64,.76,1),160)
def camera(name,loc,target,scale,reso=(1600,1000),up=None):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);studio.objects.link(o);o.location=loc;aim(o,target);d.type='ORTHO';d.ortho_scale=scale;d.clip_end=3000
    o['resolution']=list(reso);return o
cams={
'hero':camera('01 • Hero fore quarter',(240,-340,145),(0,72,6),330),
'side':camera('02 • Blueprint side',(480,81,10),(0,81,10),320,(1600,620)),
'top':camera('03 • Dorsal plan',(0,81,480),(0,81,0),320,(1600,1100)),
'front':camera('04 • Forward elevation',(0,-350,8),(0,70,8),155,(1600,900)),
'aft':camera('05 • Aft quarter',(-215,340,160),(0,80,7),325),
'underside':camera('06 • Ventral fore quarter',(205,-260,-160),(0,70,4),320),
'detail':camera('07 • Saucer and bridge',(100,-150,170),(0,0,23),160,(1600,1000))}
# Top plan with ship's nose to the left to match supplied plan.
cams['top'].rotation_euler=(0,0,pi/2)
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
scene.render.resolution_percentage=100
scene.camera=cams['hero'];scene.render.resolution_x=1600;scene.render.resolution_y=1000
# Set viewport to hero for immediate useful opening.
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.clip_end=3000
bpy.ops.object.select_all(action='DESELECT');root.select_set(True);bpy.context.view_layer.objects.active=root
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'enterprise-ncc-1701.blend'),compress=False)
meshes=[o for o in ship.objects if o.type=='MESH']
triangles=0
for o in meshes:o.data.calc_loop_triangles();triangles+=len(o.data.loop_triangles)
coords=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
mins=[min(c[k] for c in coords) for k in range(3)];maxs=[max(c[k] for c in coords) for k in range(3)]
audit={'blender':bpy.app.version_string,'mesh_objects':len(meshes),'triangles':triangles,'materials':len(materials),'dimensions_m':[round(b-a,3) for a,b in zip(mins,maxs)],'bounds_min':mins,'bounds_max':maxs,'cameras':{k:o.name for k,o in cams.items()},'textures':0,'builder':'Codex','human_review':'Professor Bear — pending'}
(ROOT/'audit.json').write_text(json.dumps(audit,indent=2))
bpy.ops.object.select_all(action='DESELECT')
for o in ship.objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'enterprise-ncc-1701.glb'),export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False)
print('ENTERPRISE BUILD COMPLETE',json.dumps(audit),flush=True)
