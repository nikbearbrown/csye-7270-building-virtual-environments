# blender -b FILE.blend -P render.py -- OUTDIR view1 view2 ...   (skips existing)
import bpy, math, sys, os, json
from mathutils import Vector
argv=sys.argv[sys.argv.index('--')+1:]; OUT=argv[0]; views=argv[1:]; os.makedirs(OUT,exist_ok=True)
sc=bpy.context.scene; cam=sc.camera
HP=json.load(open('/workspace/ships/enterprise-futurama/params.json')).get('hero',[55,9,6.0,38])
if os.environ.get('HERO'): HP=json.loads(os.environ['HERO'])
P_AZ,P_EL,P_D,P_L=HP
if os.environ.get('SAMPLES'): sc.cycles.samples=int(os.environ['SAMPLES'])
# name: (target, azimuth deg from +X, elevation, distance, lens, ortho_scale or 0, res)
V={}
V.update({'hero':((-0.70,0,-0.16),P_AZ,P_EL,P_D,P_L,0,(1024,576)),
 'side':((-1.15,0,-0.2),90,0,10,50,4.6,(1280,560)),
 'top':((-1.15,0,0),90,89.99,10,50,4.6,(1280,840)),
 'front':((0,0,-0.2),0,0,10,50,2.6,(700,800)),
 'rear34':((-1.2,0,-0.1),-140,18,8.5,50,0,(1280,720)),
 'front34':((-1.0,0,-0.1),-35,16,8.5,50,0,(1280,720)),
 'below':((-1.0,0,-0.2),40,-30,8.5,50,0,(1280,720)),
 'detail_bridge':((0.05,0,0.47),60,18,2.6,60,0,(1280,720)),
 'detail_nacelle':((-1.25,0.72,0.25),40,14,2.6,60,0,(1280,720)),
 'detail_deflector':((-0.55,0,-0.68),30,4,2.2,60,0,(1280,720))})
for v in views:
    t,az,el,d,lens,osc,res=V[v]; out=f'{OUT}/{v}.png'
    if os.path.exists(out): continue
    t=Vector(t); a=math.radians(az); e=math.radians(el)
    cam.location=t+d*Vector((math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)))
    cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler()
    if v=='top': cam.rotation_euler=(0,0,math.pi)
    cam.data.type='ORTHO' if osc else 'PERSP'; cam.data.ortho_scale=osc or 1; cam.data.lens=lens
    sc.render.resolution_x,sc.render.resolution_y=res
    gnd=bpy.data.objects.get('Ground')
    if gnd: gnd.hide_render = v in ('below','side','front','top')
    sc.render.filepath=out; bpy.ops.render.render(write_still=True); print('RENDERED',out,flush=True)
