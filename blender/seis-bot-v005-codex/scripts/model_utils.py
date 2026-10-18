"""SEIS Bot v005. Native parametric hard-surface reconstruction from Bear's references.
Blender 5.1.2; metres, Z up, front -Y. Original geometry in EXPORT.
Run: Blender --background --python-exit-code 1 --python scripts/build.py
"""
import bpy, bmesh, math, json, random, sys
from mathutils import Vector, Matrix
from math import sin, cos, pi, sqrt
from pathlib import Path

ROOT=Path(__import__('os').environ.get('SEIS_OUTPUT', str(Path(__file__).resolve().parents[1])))
ROOT.mkdir(parents=True,exist_ok=True)
for directory in ('renders','reports'): (ROOT/directory).mkdir(exist_ok=True)
FONT=ROOT/'assets'/'Lato-Bold.ttf'
if not FONT.exists():FONT=Path('/home/user/Documents/CoWork/bear-textbooks/books/seis-ai-lab/07-fonts/Lato/Lato-Bold.ttf')
# ROOT parents: blender, seis-bot, seis-ai-lab.
random.seed(64)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for block in list(bpy.data.collections):
    if block.name != 'Collection': bpy.data.collections.remove(block)
EXP=bpy.data.collections.get('Collection'); EXP.name='EXPORT'
PRES=bpy.data.collections.new('PRESENTATION'); bpy.context.scene.collection.children.link(PRES)
WORK=bpy.data.collections.new('WORK'); bpy.context.scene.collection.children.link(WORK)
scene=bpy.context.scene; scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
PARTS={}; BONE='chest'

def linear(h):
    vals=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in vals)+(1,)

def material(name, col, metal=.8, rough=.26, worn=False, emission=0):
    m=bpy.data.materials.new(name); m.diffuse_color=linear(col); m.use_nodes=True
    n=m.node_tree.nodes; l=m.node_tree.links; bs=n.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=linear(col); bs.inputs['Metallic'].default_value=metal
    bs.inputs['Roughness'].default_value=rough
    bs.inputs['Coat Weight'].default_value=.15 if metal<.7 else .08
    bs.inputs['Coat Roughness'].default_value=.17
    if emission:
        bs.inputs['Emission Color'].default_value=linear(col); bs.inputs['Emission Strength'].default_value=emission
    tc=n.new('ShaderNodeTexCoord'); tc.location=(-900,0)
    noise=n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value=165
    noise.inputs['Detail'].default_value=3; noise.inputs['Roughness'].default_value=.73
    l.new(tc.outputs['Object'],noise.inputs['Vector'])
    rr=n.new('ShaderNodeMapRange'); rr.inputs['To Min'].default_value=max(.05,rough-.065);rr.inputs['To Max'].default_value=rough+.09
    l.new(noise.outputs['Fac'],rr.inputs['Value']);l.new(rr.outputs['Result'],bs.inputs['Roughness'])
    micro=n.new('ShaderNodeTexNoise');micro.inputs['Scale'].default_value=4200;micro.inputs['Detail'].default_value=2
    l.new(tc.outputs['Object'],micro.inputs['Vector'])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.19;bump.inputs['Distance'].default_value=.00013
    l.new(micro.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal'])
    if worn:
        attr=n.new('ShaderNodeAttribute');attr.attribute_name='edge_wear'
        grain=n.new('ShaderNodeTexNoise');grain.inputs['Scale'].default_value=115;grain.inputs['Detail'].default_value=5;grain.inputs['Roughness'].default_value=.8
        l.new(tc.outputs['Object'],grain.inputs['Vector'])
        ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.37;ramp.color_ramp.elements[1].position=.68
        l.new(grain.outputs['Fac'],ramp.inputs['Fac'])
        mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(attr.outputs['Fac'],mul.inputs[0]);l.new(ramp.outputs[0],mul.inputs[1])
        mix=n.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[1].default_value=linear(col);mix.inputs[2].default_value=linear('a79a7b')
        l.new(mul.outputs[0],mix.inputs[0]);l.new(mix.outputs[0],bs.inputs['Base Color'])
    return m

M={
 'armor':material('MAT_Petrol_Enamel_Worn','284647',.85,.27,True),
 'dark':material('MAT_Graphite_Anodized','172021',.84,.29,True),
 'silver':material('MAT_Satin_Steel','afb9b7',.94,.32),
 'edge':material('MAT_Exposed_Champagne_Alloy','9d9379',.90,.30),
 'red':material('MAT_Northeastern_Red_Enamel','b80b24',.78,.32),
 'rubber':material('MAT_Joint_Elastomer','111719',.12,.47),
 'white':material('MAT_Porcelain_Six','e9ece6',.35,.23),
 'eye':material('MAT_Red_Optical_Glass','ba0920',.45,.21,.0,.12),
 'glass':material('MAT_Smoked_Optical_Glass','090c0e',.48,.12),
 'bronze':material('MAT_Oxidized_Bronze','655a3d',.9,.35),
}

def finish(o,name,mat,bone=None):
    name=__import__('re').sub('[^A-Za-z0-9_]','_',name)
    o.name=name
    if o.data: o.data.name=name
    for c in list(o.users_collection):c.objects.unlink(o)
    EXP.objects.link(o)
    o.data.materials.append(M[mat])
    for p in getattr(o.data,'polygons',[]):p.use_smooth=True
    o['part_role']=name; o['asset_id']='SEIS_BOT_V005'
    PARTS[o.name]=bone or BONE
    return o

def mesh(name,verts,faces,mat='armor',wear=None,bone=None):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);EXP.objects.link(o);finish(o,name,mat,bone)
    if wear:
        a=me.attributes.new('edge_wear','FLOAT','POINT')
        a.data.foreach_set('value',wear)
    return o

def smooth_path(points,steps=10,closed=False):
    pts=[Vector(p) for p in points];out=[]
    n=len(pts)
    for i in range(n if closed else n-1):
        a,b,c,d=[pts[j%n] if closed else pts[max(0,min(n-1,j))] for j in (i-1,i,i+1,i+2)]
        for k in range(steps):
            t=k/steps;t2=t*t;t3=t2*t
            out.append((b*2+(c-a)*t+(a*2-b*5+c*4-d)*t2+(-a+b*3-c*3+d)*t3)*.5)
    if not closed:out.append(pts[-1])
    return out

def sweep(name,points,width=.012,depth=None,mat='armor',normal=(0,-1,0),steps=10,profile=16,power=4.0,trim=False,bone=None):
    # Optional fourth coordinate gives per-section width multiplier.
    four=len(points[0])==4
    p=smooth_path(points,steps);xyz=[Vector(q[:3]) for q in p]
    depth=depth if depth is not None else width
    vs=[];fs=[];ws=[];edges=[[],[]]
    for i,c in enumerate(xyz):
        t=(xyz[min(i+1,len(xyz)-1)]-xyz[max(0,i-1)]).normalized()
        nn=Vector(normal);u=t.cross(nn).normalized()
        if u.length<.5:u=t.cross(Vector((1,0,0))).normalized()
        v=u.cross(t).normalized();mult=max(.01,p[i][3]) if four else 1
        for j in range(profile):
            th=2*pi*j/profile
            a=math.copysign(abs(cos(th))**(2/power),cos(th));b=math.copysign(abs(sin(th))**(2/power),sin(th))
            vs.append(c+u*width*mult*a+v*depth*sqrt(mult)*b)
            # Wear follows the profile's corners, not the broad face centre.
            ws.append(min(1,abs(sin(2*th))**14*.82 + (.25 if i<2 or i>len(xyz)-3 else 0)))
        edges[0].append(tuple(c+u*width*mult+v*depth*.3));edges[1].append(tuple(c-u*width*mult+v*depth*.3))
    for i in range(len(xyz)-1):
        for j in range(profile):
            a=i*profile+j;b=i*profile+(j+1)%profile;fs.append((a,b,b+profile,a+profile))
    fs.append(tuple(reversed(range(profile))));fs.append(tuple(range((len(xyz)-1)*profile,len(xyz)*profile)))
    obj=mesh(name,vs,fs,mat,ws,bone)
    if trim:
        for k,edge in enumerate(edges):sweep(name+'_Lip_'+str(k),edge,width=.00065,mat='edge',steps=1,profile=6,power=2,bone=bone)
    return obj

def ellipsoid(name,loc,scale,mat='dark',bone=None,seg=40,rings=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=loc)
    o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return finish(o,name,mat,bone)

def cylinder(name,loc,radius,depth,mat='silver',axis=(0,0,1),vertices=48,bone=None,bevel=.0008):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
    o=bpy.context.object;o.rotation_mode='QUATERNION';o.rotation_quaternion=Vector(axis).to_track_quat('Z','Y')
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);finish(o,name,mat,bone)
    if bevel:
        m=o.modifiers.new('Machined_Edge_Radius','BEVEL');m.width=min(bevel,depth*.20,radius*.20);m.segments=3
        m=o.modifiers.new('Face_Weighted_Normals','WEIGHTED_NORMAL')
    return o

def torus(name,loc,major,minor,mat='edge',axis=(0,0,1),bone=None):
    bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=12,location=loc,major_radius=major,minor_radius=minor)
    o=bpy.context.object;o.rotation_mode='QUATERNION';o.rotation_quaternion=Vector(axis).to_track_quat('Z','Y');bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    return finish(o,name,mat,bone)

def bolt(name,loc,axis=(0,-1,0),r=.004,bone=None):
    v=Vector(axis).normalized();p=Vector(loc)
    cylinder(name+'_Seat',p,r*1.48,.0014,'dark',axis,bone=bone,bevel=.0003)
    cylinder(name+'_Head',p+v*.0012,r,.002,'silver',axis,vertices=6,bone=bone,bevel=.00025)
    cylinder(name+'_Socket',p+v*.0023,r*.47,.0005,'rubber',axis,vertices=6,bone=bone,bevel=.0001)

def hub(name,loc,r,axis=(0,-1,0),bone=None,detail=12):
    p=Vector(loc);a=Vector(axis).normalized();u=a.cross(Vector((0,0,1))).normalized()
    if u.length<.5:u=a.cross(Vector((0,1,0))).normalized()
    v=a.cross(u)
    cylinder(name+'_Housing',p,r,r*.30,'dark',a,bone=bone)
    for i,(rr,dd,ma) in enumerate([(1,.13,'armor'),(.84,.19,'edge'),(.73,.22,'rubber'),(.63,.23,'silver'),(.49,.255,'dark')]):
        torus(name+'_Ring_'+str(i),p+a*r*dd,r*rr,r*.035,ma,a,bone)
    cylinder(name+'_Hub',p+a*r*.24,r*.48,r*.12,'dark',a,bone=bone)
    cylinder(name+'_Axle',p+a*r*.315,r*.20,r*.04,'silver',a,vertices=12,bone=bone)
    cylinder(name+'_Hex',p+a*r*.34,r*.105,r*.045,'rubber',a,vertices=6,bone=bone)
    for j in range(detail):
        t=2*pi*j/detail;q=p+(u*cos(t)+v*sin(t))*r*.6+a*r*.25
        cylinder(name+'_Bearing_'+str(j),q,r*.045,r*.045,'bronze',a,vertices=10,bone=bone,bevel=.0001)
    for j in range(6):
        t=2*pi*j/6;q=p+(u*cos(t)+v*sin(t))*r*.87+a*r*.16
        bolt(name+'_Bolt_'+str(j),q,a,r*.04,bone)

def line(name,points,r=.001,mat='silver',bone=None):return sweep(name,points,r,r,mat,steps=6,profile=8,power=2,bone=bone)

def mirror(points,s):return [(s*p[0],)+tuple(p[1:]) for p in points]

def text_mesh(name,body,loc,size,mat='white',rot=(pi/2,0,0),bone=None):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=size;cu.extrude=.0005;cu.bevel_depth=.00025;cu.bevel_resolution=3
    if FONT.exists():cu.font=bpy.data.fonts.load(str(FONT),check_existing=True)
    ob=bpy.data.objects.new(name,cu);EXP.objects.link(ob);ob.location=loc;ob.rotation_euler=rot
    bpy.context.view_layer.objects.active=ob;ob.select_set(True)
    for x in bpy.context.selected_objects:
        if x!=ob:x.select_set(False)
    bpy.ops.object.convert(target='MESH');bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    return finish(ob,name,mat,bone)

def patch(name,outline,surface_y,mat='armor',thickness=.005,bevel=.001,smooth=3,bone=None):
    """Constrained polygon fill with uniformly refined triangles on an analytic surface.
    Real curved broad plates; no radial fan, no pillow dome, no concave fan folds.
    """
    from mathutils.geometry import tessellate_polygon
    from mathutils.kdtree import KDTree
    boundary=smooth_path(outline,smooth,True) if smooth else [Vector(p) for p in outline]
    flat=[Vector((q.x,0,q.y)) for q in boundary]
    tris=tessellate_polygon([flat]);verts=[];faces=[];wear=[]
    # Densely sampled boundary supplies a true millimetre-scale edge-wear mask.
    kd=KDTree(len(flat)*8)
    for k,a in enumerate(flat):
        b=flat[(k+1)%len(flat)]
        for j in range(8):kd.insert(a.lerp(b,j/8),k*8+j)
    kd.balance();n=7
    for ia,ib,ic in tris:
        a,b,c=flat[ia],flat[ib],flat[ic]
        if (b-a).cross(c-a).length<1e-12:continue
        ids={}
        for i in range(n+1):
            for j in range(n+1-i):
                q=a*(1-(i+j)/n)+b*(i/n)+c*(j/n)
                ids[i,j]=len(verts);verts.append((q.x,surface_y(q.x,q.z),q.z))
                dist=kd.find(q)[2];wear.append(max(0,1-dist/.0035))
        for i in range(n):
            for j in range(n-i):
                faces.append((ids[i,j],ids[i+1,j],ids[i,j+1]))
                if i+j<n-1:faces.append((ids[i+1,j],ids[i+1,j+1],ids[i,j+1]))
    ob=mesh(name,verts,faces,mat,wear,bone)
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0000007)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    # These patches are analytical front surfaces. A mirrored outline must not
    # reverse the wall extrusion and bury an inset or create a projecting fin.
    if sum(face.normal.y*face.calc_area() for face in bm.faces)>0:
        bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
    bm.to_mesh(ob.data);bm.free()
    sol=ob.modifiers.new('Cast_Wall','SOLIDIFY');sol.thickness=thickness;sol.offset=-1
    if bevel:
        be=ob.modifiers.new('Perimeter_Fillet','BEVEL');be.width=min(bevel,thickness*.25);be.segments=3
        be.limit_method='ANGLE';be.angle_limit=.60;be.use_clamp_overlap=True
    return ob

def loft(name,rows,mat='armor',start=-pi,end=pi,segments=48,steps=4,thickness=.005,bone=None):
    """Continuous elliptical casing with front at theta=0. Open angular sectors
    are genuine cavities; full circumference shells have closed top and bottom.
    """
    rr=smooth_path(rows,steps);full=abs(end-start-2*pi)<.001
    n=segments if full else segments+1;verts=[];faces=[];wear=[]
    for j,r in enumerate(rr):
        cx,cy,z,rx,ry=r
        for i in range(n):
            th=start+(end-start)*i/segments
            verts.append((cx+rx*sin(th),cy-ry*cos(th),z))
            edge=min(j/(max(1,len(rr)-1)),1-j/(max(1,len(rr)-1)))
            a=0 if full else min(i/segments,1-i/segments)
            wear.append(max(0,1-edge*14,0 if full else 1-a*14))
    for j in range(len(rr)-1):
        for i in range(segments):
            a=j*n+i;b=j*n+((i+1)%n)
            faces.append((a,b,b+n,a+n))
    if full:
        faces.append(tuple(reversed(range(n))));faces.append(tuple(range((len(rr)-1)*n,len(rr)*n)))
    ob=mesh(name,verts,faces,mat,wear,bone)
    if not full:
        sol=ob.modifiers.new('Cast_Wall','SOLIDIFY');sol.thickness=thickness;sol.offset=-1
    be=ob.modifiers.new('Shell_Edge_Fillet','BEVEL');be.width=min(.001,thickness*.2);be.segments=2;be.limit_method='ANGLE';be.angle_limit=.4
    return ob

def box(name,loc,size,mat='dark',bevel=.002,bone=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    ob=bpy.context.object;ob.scale=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    finish(ob,name,mat,bone)
    if bevel:
        mod=ob.modifiers.new('Machined_Fillet','BEVEL');mod.width=min(bevel,min(size)*.25);mod.segments=3
        ob.modifiers.new('Face_Normals','WEIGHTED_NORMAL')
    return ob

BONES={
 'root':((0,0,0),(0,0,.15),None),
 'pelvis':((0,0,1.045),(0,0,1.16),'root'),
 'chest':((0,0,1.16),(0,0,1.78),'pelvis'),
 'neck':((0,0,1.78),(0,0,1.90),'chest'),
 'head':((0,0,1.90),(0,0,2.20),'neck'),
}
for sign,suf in ((1,'l'),(-1,'r')):
    sh=(sign*.373,0,1.77);el=(sign*.425,0,1.35);wr=(sign*.443,-.008,1.01)
    hi=(sign*.165,0,1.045);kn=(sign*.19,-.006,.585);an=(sign*.20,0,.145)
    BONES['upper_arm_'+suf]=(sh,el,'chest');BONES['forearm_'+suf]=(el,wr,'upper_arm_'+suf)
    BONES['hand_'+suf]=(wr,(sign*.45,-.02,.90),'forearm_'+suf)
    BONES['thigh_'+suf]=(hi,kn,'pelvis');BONES['shin_'+suf]=(kn,an,'thigh_'+suf)
    BONES['foot_'+suf]=(an,(sign*.20,-.17,.065),'shin_'+suf)

def enhance_materials():
    """Clean workshop enamel and machined metal matching the supplied video frames.
    Millimetre geometry makes the edges; sparse roughness variation supplies finish.
    """
    palette={'armor':('284647',.87,.23),'dark':('172021',.82,.25),
             'red':('b80b24',.38,.21),'silver':('c0c5c1',.93,.26),
             'edge':('a89f88',.92,.27)}
    for key,(col,metal,roughness) in palette.items():
        m=M[key];n=m.node_tree.nodes;l=m.node_tree.links
        n.clear();out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled')
        l.new(bs.outputs['BSDF'],out.inputs['Surface'])
        m.diffuse_color=linear(col);bs.inputs['Base Color'].default_value=linear(col)
        bs.inputs['Metallic'].default_value=metal
        bs.inputs['Coat Weight'].default_value=.25 if key in ('red','armor') else .07
        bs.inputs['Coat Roughness'].default_value=.19
        tc=n.new('ShaderNodeTexCoord');grain=n.new('ShaderNodeTexNoise')
        grain.inputs['Scale'].default_value=240;grain.inputs['Detail'].default_value=2
        l.new(tc.outputs['Object'],grain.inputs['Vector'])
        rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=roughness-.018;rough.inputs['To Max'].default_value=roughness+.024
        l.new(grain.outputs['Fac'],rough.inputs['Value']);l.new(rough.outputs['Result'],bs.inputs['Roughness'])
        micro=n.new('ShaderNodeTexNoise');micro.inputs['Scale'].default_value=5200;micro.inputs['Detail'].default_value=2
        l.new(tc.outputs['Object'],micro.inputs['Vector'])
        bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.045;bump.inputs['Distance'].default_value=.000035
        l.new(micro.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal'])
    eye=M['eye'].node_tree.nodes.get('Principled BSDF')
    eye.inputs['Base Color'].default_value=linear('ba0920')
    eye.inputs['Emission Color'].default_value=linear('ed0019');eye.inputs['Emission Strength'].default_value=1.8
