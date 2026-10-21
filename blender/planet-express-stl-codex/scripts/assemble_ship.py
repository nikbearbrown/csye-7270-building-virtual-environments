import bpy, math, json
from mathutils import Matrix,Vector
from pathlib import Path
R=Path('/Users/bear/Downloads/planet-express-stl-build');scene=bpy.context.scene
O=lambda n:bpy.data.objects['GOODesign_'+n]
T=lambda v:Matrix.Translation(Vector(v))
RX=lambda a:Matrix.Rotation(math.radians(a),4,'X')
RY=lambda a:Matrix.Rotation(math.radians(a),4,'Y')
RZ=lambda a:Matrix.Rotation(math.radians(a),4,'Z')
def place(n,rot=Matrix.Identity(4),origin=(0,0,0),target=(0,0,0)):
 o=O(n);o.matrix_world=T(target)@rot@T(tuple(-v for v in origin));o.hide_render=False;return o
def material(name,color,metal=0,rough=.35):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
hull=material('Turquoise enamel',(.008,.32,.24),.05);fin=material('Deep teal enamel',(.004,.07,.065),.08);ivory=material('Warm ivory fittings',(.72,.66,.44),.08);red=material('Signal red',(.58,.018,.01),.15);dark=material('Graphite',(.025,.03,.032),.3);glazing=material('Blue cockpit glazing',(.15,.35,.42),.6,.18);logoWhite=material('Logo ivory',(.9,.9,.79));logoRed=red
for o in bpy.data.objects:
 if o.type=='MESH':
  o.hide_render=True
  name=o.name;mat=hull
  if any(s in name for s in ['Wing','Window_Frame','Turret_A']):mat=fin
  if 'Silver' in name or 'Nozzle_A' in name:mat=ivory
  if any(s in name for s in ['Nozzle_B','Turret_B','Stair','Cargo_A']):mat=dark
  if 'Ring' in name or 'Red_Parts' in name:mat=red
  if name.endswith('_Window') or name.endswith('_Dome'):mat=glazing
  if 'Logo_A' in name:mat=logoWhite
  if 'Logo_B' in name:mat=logoRed
  if 'Logo_C' in name:mat=hull
  o.data.materials.clear();o.data.materials.append(mat)
for n in ['Hull_Front.part1','Hull_Front.part2','Hull_Front.part3']:place(n,RX(90),target=(0,-9.845,72.287))
for n in ['Hull_Rear.part1','Hull_Rear.part2']:place(n,RX(-90),target=(0,17.179,79.218))
for n in ['Ring','Cargo_A','Cargo_B','Stair_A.part1','Stair_A.part2','Stair_B','Stand_Cover','Window','Dome','Turret_A.part1','Turret_A.part2']:place(n)
place('Window_Frame',RX(30),origin=(0,-56,45),target=(0,-56,41))
place('Wing_Top',RX(-30),origin=(125,60,0),target=(0,34,50))
# Side-fin coordinates: their long printed Z dimension runs along the ship.
for n,s,xcenter in [('Wing_Left',1,128.8),('Wing_Right',-1,121.2)]:
 rot=Matrix(((0,-s,0,0),(0,0,1,0),(-s,0,0,0),(0,0,0,1)))
 place(n,rot,origin=(xcenter,115.9,0),target=(0,31,21))
place('Nozzle_A',RX(-90),origin=(0,102.18,13.024),target=(0,31.6,0))
# Axis of nozzle after rotation is +Y.
place('Nozzle_A',RX(-90),origin=(0,102.18,13.024),target=(0,93.2,31.6))
place('Nozzle_B',RX(-90),origin=(0,106.59,33.5),target=(0,115.1,31.6))
# Turret cannon printed sideways; point its barrel forward.
place('Turret_B',RZ(90),origin=(16.8,-28.684,60.93),target=(0,-15,55.9))
# Landing gear pair; place on the underside near the rear of the nose.
for n,s,xc in [('Landing_Gear.part1',1,133.597),('Landing_Gear.part2',-1,116.403)]:place(n,RX(180),origin=(xc,105,0),target=(s*16,61,17))
for n,s,xc in [('LG_Cover.part1',1,132.299),('LG_Cover.part2',-1,117.7)]:place(n,RX(180),origin=(xc,105,0),target=(s*16,61,17))
place('Silver_Parts_A.part14',origin=(130.574,92.515,0),target=(0,-9.37,60))
# Fine hardware placements are refined in the inspection pass.
for n in ['Silver_Parts_A.part1','Silver_Parts_A.part2']:
 o=O(n);vs=[v.co for v in o.data.vertices];cx=(min(v.x for v in vs)+max(v.x for v in vs))/2;cy=(min(v.y for v in vs)+max(v.y for v in vs))/2
 s=1 if n.endswith('1') else -1
 place(n,RY(s*65)@Matrix.Diagonal((1,1,.35,1)),origin=(cx,cy,1.4),target=(s*21,62,40))
# Eight porthole inserts match the two rows of four molded bores.
ports=[o.name for o in bpy.data.objects if o.name.startswith('GOODesign_Silver_Parts_A.part') and 2500<len(o.data.polygons)<3000]
ports=sorted(ports)
for n,(s,y,x,z) in zip(ports,[(s,y,x,z) for s in [-1,1] for y,x,z in [(-36,18.6,43.6),(-21,21.7,44.7),(-6,22.8,45),(8.5,23,44.8)]]):
 o=bpy.data.objects[n];vs=[v.co for v in o.data.vertices];center=((min(v.x for v in vs)+max(v.x for v in vs))/2,(min(v.y for v in vs)+max(v.y for v in vs))/2,6.6)
 place(n.removeprefix('GOODesign_'),RY(s*65),origin=center,target=(s*x,y,z))
# Top fin trim (third component is the longer profiled root).
place('Silver_Parts_B.part3',RX(-8)@RY(180),origin=(108.062,79.03,0),target=(0,32,53.5))
for n,s,cx in [('Silver_Parts_B.part1',1,124.981),('Silver_Parts_B.part2',-1,141.919)]:
 place(n,RY(s*115),origin=(cx,79.03,2.5),target=(s*22,32,23))
# Place the three-layer emblems on opposite faces of the tail.
for layer in ['A','B','C']:
 for part in [1,2]:
  n=f'Logo_{layer}.part{part}';o=O(n);vs=[v.co for v in o.data.vertices];cx=(min(v.x for v in vs)+max(v.x for v in vs))/2;s=1 if cx>0 else -1
  # Keep all three colored layers in their shared source coordinates.
  base=(9.39 if s>0 else -13.78,86.4 if s>0 else 85.87,58.855)
  place(n,RX(30)@RY(s*90)@RZ(s*90),origin=base,target=(s*3.8,79,60))
# Red caps attach to the ends of the three long fin spars.
for n,rot,tip in [('Red_Parts.part1',RX(-86),(0,150.2,75.3)),('Red_Parts.part2',RX(-90),(11,110,21)),('Red_Parts.part3',RX(-90),(-11,110,21))]:
 o=O(n);vs=[v.co for v in o.data.vertices];origin=((min(v.x for v in vs)+max(v.x for v in vs))/2,160.456,74.139);place(n,rot,origin,tip)
scene.name='Planet Express • assembly draft'
for o in bpy.data.objects:
 if o.type=='MESH' and not o.hide_render:
  for p in o.data.polygons:p.use_smooth=True
  o.data.set_sharp_from_angle(angle=math.radians(35))
# Refine the printing-fold seam of the cannon into its assembled cylindrical form.
gun=O('Turret_B')
if not gun.get('folded'):
 for v in gun.data.vertices:
  if v.co.x>-.2:v.co.x=-.4-v.co.x;v.co.z=2*59.952-v.co.z
 gun.data.update();gun['folded']=True
place('Turret_B',RX(-15)@RZ(90),origin=(-.2,-28.684,59.952),target=(0,-14,56.8))
# Appearance corrections: the kit inserts sit in the bores, not outside them.
for n in ports:
 o=bpy.data.objects[n];o.data.materials.append(glazing)
 vs=[v.co for v in o.data.vertices];cx=(min(v.x for v in vs)+max(v.x for v in vs))/2;cy=(min(v.y for v in vs)+max(v.y for v in vs))/2
 for poly in o.data.polygons:
  c=poly.center
  if (c.x-cx)**2+(c.y-cy)**2<1.8**2 and c.z>5:poly.material_index=1
# Make kit support pins and all spare components available but hidden in flight presentation.
for o in bpy.data.objects:
 if o.type=='MESH' and any(k in o.name for k in ['Landing_Gear','LG_Cover','Hull_Front.part2','Hull_Front.part3']):o.hide_render=True
for o in bpy.data.objects:
 if o.type=='LIGHT':o.data.energy={'Key':600000,'Fill':650000,'Rim':850000}.get(o.name,600000)
scene.cycles.samples=32
bpy.ops.wm.save_as_mainfile(filepath=str(R/'planet-express-assembly-draft.blend'),compress=True)
print('Assembly draft saved; inspection and fitting still required.')
