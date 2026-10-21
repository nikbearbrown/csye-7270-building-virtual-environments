# Gallery + GLB + stats from planet_express.blend. blender -b planet_express.blend -P final.py -- [gallery|export]
import bpy, math, sys, json, os
from mathutils import Vector
H='/workspace/ships/planet-express'; argv=sys.argv[sys.argv.index('--')+1:]
sc=bpy.context.scene; cam=sc.camera
if 'gallery' in argv:
    os.makedirs(f'{H}/gallery',exist_ok=True)
    sc.render.resolution_x=1600; sc.render.resolution_y=900; sc.cycles.samples=24
    shots={'side':((-1.2,0,0.6),90,4,42,85),'side_left':((-1.2,0,0.6),-90,4,42,85),'front':((1,0,0.4),0,8,34,85),
      'rear34':((-3,0,0.5),-145,14,30,70),'front34':((0,0,0.5),-38,16,32,70),'top':((-1.5,0,0.5),0.01,89,40,70),
      'detail_cockpit':((3.9,0,0.9),-25,22,9,85),'detail_turret':((0,0,2.0),-60,15,7,85),
      'detail_engine':((-7.4,0,-0.4),-160,10,8,85),'detail_fin_logo':((-5.4,0,1.9),90,3,9,85),
      'detail_vent_wing':((-4.5,0,-0.2),-70,8,11,85)}
    for n,(t,az,el,d,lens) in shots.items():
        out=f'{H}/gallery/{n}.png'
        if os.path.exists(out): continue
        t=Vector(t); a=math.radians(az); e=math.radians(el)
        cam.location=t+d*Vector((math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)))
        cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.lens=lens
        cam.data.shift_x=0; cam.data.shift_y=0
        if n=='top': cam.rotation_euler=(0,0,math.pi/2)
        sc.render.filepath=out; bpy.ops.render.render(write_still=True); print('RENDERED',out,flush=True)
if 'export' in argv:
    dg=bpy.context.evaluated_depsgraph_get(); tris=0; meshes=0
    mn=Vector((1e9,)*3); mx=Vector((-1e9,)*3)
    for o in sc.objects:
        if o.type not in ('MESH','CURVE'): continue
        ev=o.evaluated_get(dg); me=ev.to_mesh()
        if me is None: continue
        meshes+=1; me.calc_loop_triangles(); tris+=len(me.loop_triangles)
        for v in me.vertices:
            w=ev.matrix_world@v.co; mn=Vector(map(min,mn,w)); mx=Vector(map(max,mx,w))
        ev.to_mesh_clear()
    st={'objects':meshes,'triangles':tris,'bbox_min':list(mn),'bbox_max':list(mx),'size':list(mx-mn),
        'materials':len(bpy.data.materials)}
    json.dump(st,open(f'{H}/stats.json','w'),indent=1); print(st)
    bpy.ops.export_scene.gltf(filepath=f'{H}/planet_express.glb',export_format='GLB',export_apply=True)
