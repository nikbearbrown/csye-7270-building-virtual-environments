# PROP-TABLET rugged tablet (built 2026-10-12 local time)
# Every execute_blender_code body Claude Code (Claude Opus 5.5) ran through the
# Blender MCP for this asset, copied verbatim from the session transcript, in order.
# Each section was a separate call in the same live Blender session; run top to bottom.
# Call 1 built a single grey version; Call 2 deleted it and rebuilt with a green/black shell
# and a black screen. The .blend (now design/item_resource/tablet/Pad_model.blend) was saved by hand afterwards.
# Copy for the course repo: the absolute output paths on my machine were replaced with paths
# relative to this folder (run Blender from walker-survival-shooting/); nothing else was changed.

# ======================================================================
# Call 1 of 2, run at 2026-10-12T23:44:42.394Z (UTC)
# ======================================================================
import bpy, bmesh
from mathutils import Vector

bpy.data.objects["Cube"].hide_set(True); bpy.data.objects["Cube"].hide_render=True

col = bpy.data.collections.new("Tablet"); bpy.context.scene.collection.children.link(col)
parts=[]
def box(name, size, loc, bevel=0.0, seg=1):
    me=bpy.data.meshes.new(name); bm=bmesh.new()
    bmesh.ops.create_cube(bm,size=1.0)
    for v in bm.verts: v.co=Vector((v.co.x*size[0],v.co.y*size[1],v.co.z*size[2]))+Vector(loc)
    if bevel>0:
        bmesh.ops.bevel(bm,geom=bm.edges[:],offset=bevel,segments=seg,affect='EDGES',profile=0.5)
    bm.to_mesh(me); bm.free()
    o=bpy.data.objects.new(name,me); col.objects.link(o); parts.append(o); return o

W,H,T = 0.230,0.150,0.020   # main body (X width, Z height, Y thickness)
# main body
box("Body",(W,T,H),(0,0,0),bevel=0.004)
# front bezel frame raised slightly, screen recessed: frame = 4 strips
fy=-T/2-0.0015; ft=0.003
sw,sh=0.180,0.108  # screen opening
bw=(W-0.012-sw)/2; bh=(H-0.012-sh)/2
box("BezelTop",(W-0.012,ft,bh),(0,fy,sh/2+bh/2),bevel=0.001)
box("BezelBot",(W-0.012,ft,bh),(0,fy,-sh/2-bh/2),bevel=0.001)
box("BezelL",(bw,ft,sh),(-sw/2-bw/2,fy,0),bevel=0.001)
box("BezelR",(bw,ft,sh),(sw/2+bw/2,fy,0),bevel=0.001)
# screen panel (slightly below bezel surface)
box("Screen",(sw,0.001,sh),(0,-T/2-0.0005,0))
# back raised panel
box("BackPanel",(0.190,0.002,0.118),(0,T/2+0.001,0),bevel=0.004,seg=1)
# corner bumpers
cb=0.040; ct=0.028
for sx in (-1,1):
    for sz in (-1,1):
        box(f"Bumper_{'R' if sx>0 else 'L'}{'T' if sz>0 else 'B'}",(cb,ct,cb),
            (sx*(W/2-cb/2+0.006),0,sz*(H/2-cb/2+0.006)),bevel=0.009,seg=1)
# edge strips top/bottom (front side, both)
for sz in (-1,1):
    for sx in (-1,1):
        box(f"EdgeStrip_{sx}_{sz}",(0.062,0.024,0.008),(sx*0.058,0,sz*(H/2+0.002)),bevel=0.003)
# left side buttons
for z in (0.022,-0.020):
    box(f"SideButton_{z}",(0.006,0.014,0.034),(-W/2-0.003,0,z),bevel=0.0015)
# side rails between bumpers (left/right)
for sx in (-1,1):
    box(f"SideRail_{sx}",(0.004,0.022,0.080),(sx*(W/2+0.001),0,0),bevel=0.0012)

# join
bpy.ops.object.select_all(action='DESELECT')
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.join()
tab=bpy.context.active_object; tab.name="PROP_Tablet"; tab.data.name="PROP_Tablet"
mat=bpy.data.materials.new("Tablet_White"); mat.use_nodes=True
b=next(n for n in mat.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
b.inputs["Base Color"].default_value=(0.8,0.8,0.8,1); b.inputs["Roughness"].default_value=0.8
tab.data.materials.append(mat)
print(tab.dimensions, len(tab.data.polygons))

# ======================================================================
# Call 2 of 2, run at 2026-10-12T23:47:03.757Z (UTC)
# ======================================================================
import bpy, bmesh
from mathutils import Vector
old=bpy.data.objects.get("PROP_Tablet")
if old: bpy.data.objects.remove(old)
col=bpy.data.collections["Tablet"]

def mk(name,rgb,rough):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes=True
    b=next(n for n in m.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value=(*rgb,1); b.inputs["Roughness"].default_value=rough
    m.diffuse_color=(*rgb,1); return m
GREEN=mk("Tablet_ShellGreen",(0.035,0.075,0.04),0.8)
BLACK=mk("Tablet_ShellBlack",(0.015,0.015,0.015),0.85)
SCREEN=mk("Tablet_Screen",(0.002,0.002,0.003),0.15)
old_white=bpy.data.materials.get("Tablet_White")
if old_white and old_white.users==0: bpy.data.materials.remove(old_white)

parts=[]
def box(name,size,loc,mat,bevel=0.0,seg=1):
    me=bpy.data.meshes.new(name); bm=bmesh.new()
    bmesh.ops.create_cube(bm,size=1.0)
    for v in bm.verts: v.co=Vector((v.co.x*size[0],v.co.y*size[1],v.co.z*size[2]))+Vector(loc)
    if bevel>0: bmesh.ops.bevel(bm,geom=bm.edges[:],offset=bevel,segments=seg,affect='EDGES',profile=0.5)
    bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o=bpy.data.objects.new(name,me); col.objects.link(o); parts.append(o)

W,H,T=0.230,0.150,0.020
box("Body",(W,T,H),(0,0,0),GREEN,bevel=0.004)
fy=-T/2-0.0015; ft=0.003; sw,sh=0.180,0.108
bw=(W-0.012-sw)/2; bh=(H-0.012-sh)/2
box("BezelTop",(W-0.012,ft,bh),(0,fy,sh/2+bh/2),GREEN,bevel=0.001)
box("BezelBot",(W-0.012,ft,bh),(0,fy,-sh/2-bh/2),GREEN,bevel=0.001)
box("BezelL",(bw,ft,sh),(-sw/2-bw/2,fy,0),GREEN,bevel=0.001)
box("BezelR",(bw,ft,sh),(sw/2+bw/2,fy,0),GREEN,bevel=0.001)
box("Screen",(sw,0.001,sh),(0,-T/2-0.0005,0),SCREEN)
box("BackPanel",(0.190,0.002,0.118),(0,T/2+0.001,0),GREEN,bevel=0.004)
cb=0.040; ct=0.028
for sx in (-1,1):
    for sz in (-1,1):
        box("Bumper",(cb,ct,cb),(sx*(W/2-cb/2+0.006),0,sz*(H/2-cb/2+0.006)),BLACK,bevel=0.009)
for sz in (-1,1):
    for sx in (-1,1):
        box("EdgeStrip",(0.062,0.024,0.008),(sx*0.058,0,sz*(H/2+0.002)),BLACK,bevel=0.003)
for z in (0.022,-0.020):
    box("SideButton",(0.006,0.014,0.034),(-W/2-0.003,0,z),BLACK,bevel=0.0015)
for sx in (-1,1):
    box("SideRail",(0.004,0.022,0.080),(sx*(W/2+0.001),0,0),BLACK,bevel=0.0012)

bpy.ops.object.select_all(action='DESELECT')
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.join()
t=bpy.context.active_object; t.name="PROP_Tablet"; t.data.name="PROP_Tablet"
print([m.name for m in t.data.materials], t.dimensions)

# --- 2026-10-15 revision (later session) ---

# ======================================================================
# Call 3 of 3, run at 2026-10-15T04:19:01.891Z (UTC)
# Rebuilt from scratch: same parts, sizes and colours as call 2, bevels kept only on body and corner bumpers (804 -> 388 tris). Saves tablet.blend and tablet.glb to design/item_resource/tablet/.
# ======================================================================
import bpy, bmesh, os
from mathutils import Vector
# Fresh scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.actions):
    for b in list(coll): coll.remove(b)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 1.0
col = bpy.data.collections.new("Tablet"); sc.collection.children.link(col)

# Same parts, sizes and colours as the 2026-10-12 version (build_tablet.py call 2).
# Triangle cut (804 -> under 500): only the body and the four corner bumpers keep a bevel;
# the bezel, back panel, edge strips, buttons and rails become plain boxes (12 tris each).
def mk(name,rgb,rough):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=next(n for n in m.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value=(*rgb,1); b.inputs["Roughness"].default_value=rough
    m.diffuse_color=(*rgb,1); return m
GREEN=mk("Tablet_ShellGreen",(0.035,0.075,0.04),0.8)
BLACK=mk("Tablet_ShellBlack",(0.015,0.015,0.015),0.85)
SCREEN=mk("Tablet_Screen",(0.002,0.002,0.003),0.15)

parts=[]
def box(name,size,loc,mat,bevel=0.0,seg=1):
    me=bpy.data.meshes.new(name); bm=bmesh.new()
    bmesh.ops.create_cube(bm,size=1.0)
    for v in bm.verts: v.co=Vector((v.co.x*size[0],v.co.y*size[1],v.co.z*size[2]))+Vector(loc)
    if bevel>0: bmesh.ops.bevel(bm,geom=bm.edges[:],offset=bevel,segments=seg,affect='EDGES',profile=0.5)
    bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o=bpy.data.objects.new(name,me); col.objects.link(o); parts.append(o)

W,H,T=0.230,0.150,0.020
box("Body",(W,T,H),(0,0,0),GREEN,bevel=0.004)
fy=-T/2-0.0015; ft=0.003; sw,sh=0.180,0.108
bw=(W-0.012-sw)/2; bh=(H-0.012-sh)/2
box("BezelTop",(W-0.012,ft,bh),(0,fy,sh/2+bh/2),GREEN)
box("BezelBot",(W-0.012,ft,bh),(0,fy,-sh/2-bh/2),GREEN)
box("BezelL",(bw,ft,sh),(-sw/2-bw/2,fy,0),GREEN)
box("BezelR",(bw,ft,sh),(sw/2+bw/2,fy,0),GREEN)
box("Screen",(sw,0.001,sh),(0,-T/2-0.0005,0),SCREEN)
box("BackPanel",(0.190,0.002,0.118),(0,T/2+0.001,0),GREEN)
cb=0.040; ct=0.028
for sx in (-1,1):
    for sz in (-1,1):
        box("Bumper",(cb,ct,cb),(sx*(W/2-cb/2+0.006),0,sz*(H/2-cb/2+0.006)),BLACK,bevel=0.009)
for sz in (-1,1):
    for sx in (-1,1):
        box("EdgeStrip",(0.062,0.024,0.008),(sx*0.058,0,sz*(H/2+0.002)),BLACK)
for z in (0.022,-0.020):
    box("SideButton",(0.006,0.014,0.034),(-W/2-0.003,0,z),BLACK)
for sx in (-1,1):
    box("SideRail",(0.004,0.022,0.080),(sx*(W/2+0.001),0,0),BLACK)

bpy.ops.object.select_all(action='DESELECT')
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.join()
t=bpy.context.active_object; t.name="PROP_Tablet"; t.data.name="PROP_Tablet"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

OUT=r".\design\item_resource\tablet"
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,"tablet.blend"), check_existing=False)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,"tablet.glb"), export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
dg=bpy.context.evaluated_depsgraph_get(); m=t.evaluated_get(dg).to_mesh(); m.calc_loop_triangles()
print(t.name, tuple(round(d,3) for d in t.dimensions), "tris", len(m.loop_triangles), [x.name for x in t.data.materials], "loc", tuple(t.location), "scale", tuple(t.scale))
