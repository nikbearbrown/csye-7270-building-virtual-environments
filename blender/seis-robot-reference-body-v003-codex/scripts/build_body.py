"""Reference-first body study. New geometry; no dependency on v001/v002 geometry."""
import bpy, math, json, sys
from pathlib import Path
from mathutils import Vector
from math import sin,cos,pi
ROOT=Path(__file__).resolve().parent.parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):
 if col.name!='Collection': bpy.data.collections.remove(col)
export=bpy.data.collections.new('EXPORT');bpy.context.scene.collection.children.link(export)
studio=bpy.data.collections.new('PRESENTATION');bpy.context.scene.collection.children.link(studio)
parts=[]
def active(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o

def rgb(h):
 a=[int(h[i:i+2],16)/255 for i in (1,3,5)]
 return tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in a)
def mat(name,h,metal=.0,rough=.35):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*rgb(h),1)
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=m.diffuse_color
 bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
 return m
red=mat('NU_Red_C8102E','#C8102E',.28,.27)
gold=mat('NU_Bold_Gold_A4804A','#A4804A',.7,.27)
lightgold=mat('NU_Light_Gold_C8A978','#C8A978',.65,.28)
white=mat('NU_White','#FFFFFF',.15,.29)
black=mat('NU_Cool_Black_1E2028','#1E2028',.45,.26)
gray=mat('NU_Gray_49494D','#49494D',.28,.36)
steel=mat('NU_Gray_9B9C9E','#9B9C9E',.8,.26)
rubber=mat('Black_Joint_Seals','#08090B',.0,.55)
floor_mat=mat('Studio_Warm_Gray','#B8BABD',.0,.58)

def finish(o,name,m,bevel=0,smooth=False,group='body'):
 o.name=name
 for c in list(o.users_collection):c.objects.unlink(o)
 export.objects.link(o);o.data.materials.append(m);o['body_group']=group
 active(o);bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 if bevel:
  mod=o.modifiers.new('Edge_radius','BEVEL');mod.width=bevel;mod.segments=3
  bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in o.data.polygons:p.use_smooth=smooth
 parts.append(o)
 return o

def mesh(name,verts,faces,m,bevel=0,smooth=False,group='body'):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(name,me);export.objects.link(o)
 return finish(o,name,m,bevel,smooth,group)

def box(name,loc,size,m,bev=.01,group='body'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size
 return finish(o,name,m,bev,False,group)
def ball(name,loc,size,m,group='body'):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,location=loc);o=bpy.context.object;o.scale=size
 return finish(o,name,m,0,True,group)
def rod(name,a,b,r,m,group='body',vertices=40):
 a,b=Vector(a),Vector(b);bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=(b-a).length,location=(a+b)/2)
 o=bpy.context.object;o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
 return finish(o,name,m,.003,True,group)

def line(name,points,r,m,group='body'):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=3;cu.resolution_u=2
 sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,co in zip(sp.points,points):p.co=(*co,1)
 o=bpy.data.objects.new(name,cu);export.objects.link(o);active(o);bpy.ops.object.convert(target='MESH')
 return finish(bpy.context.object,name,m,0,True,group)

# Elliptic loft sections: z, center x, center y, x radius, y radius.
# Many short rings give smooth curved armor rather than box primitives.
def interp(sec,z):
 if z<=sec[0][0]:return sec[0]
 if z>=sec[-1][0]:return sec[-1]
 for a,b in zip(sec,sec[1:]):
  if a[0]<=z<=b[0]:
   t=(z-a[0])/(b[0]-a[0]);return tuple(x+(y-x)*t for x,y in zip(a,b))
def point(sec,z,angle,offset=0):
 zz,x,y,rx,ry=interp(sec,z)
 return (x+(rx+offset)*sin(angle),y-(ry+offset)*cos(angle),z)
def shell(name,sec,m,group='body',N=64):
 verts=[]
 for row in sec:
  z,x,y,rx,ry=row
  verts.extend([(x+rx*sin(2*pi*i/N),y-ry*cos(2*pi*i/N),z) for i in range(N)])
 faces=[tuple(reversed(range(N))),tuple(range((len(sec)-1)*N,len(sec)*N))]
 for j in range(len(sec)-1):
  for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
 return mesh(name,verts,faces,m,.004,True,group)

def patch(name,sec,rows,m,offset=.015,group='body',edge=False):
 # rows: z, start-angle, end-angle; follows parent surface.
 # Sample at every parent ring as well as densely between them. This keeps
 # the shell outside convex changes of slope rather than cutting through.
 rows=[(z,min(a,b),max(a,b)) for z,a,b in rows]
 dense=[]
 for ra,rb in zip(rows,rows[1:]):
  za,a0,b0=ra;zb,a1,b1=rb
  steps=max(1,math.ceil((zb-za)/.012))
  zs={za+(zb-za)*i/steps for i in range(steps)}
  zs.update(r[0] for r in sec if za<=r[0]<zb)
  for z in sorted(zs):
   t=(z-za)/(zb-za);dense.append((z,a0+(a1-a0)*t,b0+(b1-b0)*t))
 rows=dense+[rows[-1]]
 N=48;v=[]
 for z,a,b in rows:
  v.extend([point(sec,z,a+(b-a)*i/N,offset) for i in range(N+1)])
 f=[]
 for j in range(len(rows)-1):
  for i in range(N):f.append((j*(N+1)+i,j*(N+1)+i+1,(j+1)*(N+1)+i+1,(j+1)*(N+1)+i))
 o=mesh(name,v,f,m,0,True,group);active(o)
 sol=o.modifiers.new('Armor_thickness','SOLIDIFY');sol.thickness=.016;bpy.ops.object.modifier_apply(modifier=sol.name)
 bev=o.modifiers.new('Polished_panel_edges','BEVEL');bev.width=.004;bev.segments=2;bpy.ops.object.modifier_apply(modifier=bev.name)
 if edge:
  line(name+'_outer_edge',[point(sec,z,b,offset+.006) for z,a,b in rows],.008,gold,group)
 return o

def panel(name,outline,m,thickness=.025,group='body',bev=.009):
 # Explicit sculpted front vertices in x,y,z; depth points toward back.
 n=len(outline);v=outline+[(x,y+thickness,z) for x,y,z in outline]
 f=[tuple(reversed(range(n))),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,v,f,m,bev,False,group)

# Reference scale: approximately 3.8 units before final 1.9 m scaling.
# Slim dark hourglass torso, broad chest, floating layered shoulder shells.
torso=[(2.18,0,.025,.20,.14),(2.32,0,.015,.205,.15),(2.43,0,.01,.22,.16),(2.56,0,0,.26,.19),(2.72,0,0,.34,.235),(2.90,0,0,.40,.25),(3.02,0,0,.35,.20),(3.09,0,0,.23,.16)]
shell('Torso_Sculpted_Core',torso,black)
patch('Abdomen_Gray_Taper',torso,[(2.23,-.55,.55),(2.35,-.70,.70),(2.52,-.72,.72),(2.65,-.55,.55),(2.73,-.25,.25)],gray,.012)
for sign,side in [(1,'l'),(-1,'r')]:
 # Two compound breast plates, pointed at the waist and underarm.
 outline=[(sign*.055,-.264,2.91),(sign*.34,-.218,3.012),(sign*.395,-.181,2.90),(sign*.34,-.222,2.73),(sign*.23,-.238,2.70),(sign*.19,-.252,2.83)]
 panel('Chest_Swept_Armor_'+side,outline,red,.055,bev=.016)
 line('Chest_Gold_Lip_'+side,[(sign*.06,-.274,2.925),(sign*.34,-.231,3.024),(sign*.394,-.19,2.91)],.009,lightgold)
 line('Waist_Contour_Trim_'+side,[point(torso,z,sign*a,.024) for z,a in [(2.24,.75),(2.39,.8),(2.55,.73),(2.69,.66)]],.009,gold)
 # Scapular service pods follow source back silhouette.
 box('Back_Service_Pod_'+side,(sign*.225,.237,2.86),(.22,.16,.34),red,.045)
 box('Back_Gold_Rail_'+side,(sign*.32,.295,2.87),(.035,.055,.29),gold,.009)
 for i in range(5):box('Back_Vent_'+side+str(i),(sign*.225,.324,2.76+i*.045),(.14,.012,.012),rubber,.003)

# Central badge is deliberately small: body massing remains the focal point.
panel('Sternum_White_Badge',[(-.095,-.266,2.93),(.095,-.266,2.93),(.074,-.278,2.76),(0,-.282,2.72),(-.074,-.278,2.76)],white,.012,bev=.008)
cu=bpy.data.curves.new('Lato_6','FONT');cu.body='6';cu.align_x='CENTER';cu.size=.18;cu.extrude=.001
cu.font=bpy.data.fonts.load('<seis-ai-lab>/07-fonts/Lato/Lato-Bold.ttf')
o=bpy.data.objects.new('Chest_Six_Lato',cu);export.objects.link(o);o.location=(0,-.287,2.79);o.rotation_euler.x=pi/2;active(o);bpy.ops.object.convert(target='MESH');finish(bpy.context.object,'Chest_Six_Lato',red)

# Pelvis has rounded hip cups and a pointed center, not a box belt.
shell('Pelvis_Core',[(1.98,0,.025,.20,.155),(2.08,0,.02,.30,.20),(2.20,0,.02,.31,.19),(2.29,0,.02,.23,.155)],black)
panel('Pelvis_Gray_Center',[(-.15,-.19,2.22),(.15,-.19,2.22),(.13,-.214,2.10),(0,-.205,1.97),(-.13,-.214,2.10)],gray,.04,bev=.02)
for sign,side in [(1,'l'),(-1,'r')]:
 ball('Hip_Cup_'+side,(sign*.25,0,2.115),(.18,.21,.18),black,'leg_'+side)
 panel('Hip_Red_Inset_'+side,[(sign*.21,-.204,2.21),(sign*.31,-.189,2.19),(sign*.31,-.203,2.12),(sign*.26,-.219,2.13)],red,.02,bev=.005)

# Broad curved shoulder caps with hollow lower rim, thin upper arms, large gauntlets.
for sign,side in [(1,'l'),(-1,'r')]:
 group='arm_'+side
 shoulder=(sign*.52,0,3.005);elbow=(sign*.70,0,2.63);wrist=(sign*.80,-.015,2.11)
 ball('Shoulder_Ball_'+side,shoulder,(.215,.235,.21),black,group)
 # Elliptic shoulder dome, black top and deep red outer wrap.
 sh=[(2.84,sign*.55,0,.19,.20),(2.91,sign*.55,0,.245,.255),(3.06,sign*.535,0,.25,.26),(3.15,sign*.52,0,.18,.20),(3.19,sign*.515,0,.07,.10)]
 shell('Shoulder_Dome_'+side,sh,black,group)
 rows=[(2.86,-1.22,1.25),(2.94,-1.32,1.45),(3.07,-1.16,1.42),(3.14,-.75,1.12),(3.165,-.20,.70)]
 if sign<0:rows=[(z,-b,-a) for z,a,b in rows]
 patch('Shoulder_Red_Shell_'+side,sh,rows,red,.016,group,True)
 line('Shoulder_White_Edge_'+side,[point(sh,2.9,a,.03) for a in [-1.12+i*2.24/24 for i in range(25)]],.013,white,group)
 rod('Upper_Arm_Core_'+side,shoulder,elbow,.091,black,group)
 ua=[(2.67,sign*.685,0,.095,.10),(2.79,sign*.635,0,.108,.12),(2.91,sign*.575,0,.12,.135)]
 shell('Upper_Arm_Gray_Sleeve_'+side,ua,gray,group)
 patch('Upper_Arm_Gold_Stripe_'+side,ua,[(2.69,sign*.12,sign*.28),(2.80,sign*.22,sign*.39),(2.90,sign*.15,sign*.32)],gold,.009,group)
 ball('Elbow_Joint_'+side,elbow,(.10,.12,.105),rubber,group)
 rod('Elbow_Hinge_'+side,(sign*.61,0,2.63),(sign*.79,0,2.63),.083,steel,group)
 ga=[(2.10,sign*.80,-.015,.145,.16),(2.16,sign*.80,-.015,.205,.21),(2.29,sign*.78,-.01,.22,.23),(2.46,sign*.745,0,.165,.19),(2.56,sign*.715,0,.105,.125)]
 shell('Gauntlet_Curved_Core_'+side,ga,black,group)
 patch('Gauntlet_Red_Side_'+side,ga,[(2.13,sign*.42,sign*1.8),(2.25,sign*.65,sign*1.95),(2.40,sign*.84,sign*1.90),(2.51,sign*.50,sign*1.60)],red,.018,group,True)
 patch('Gauntlet_White_Front_'+side,ga,[(2.18,-.48,.48),(2.28,-.52,.52),(2.43,-.34,.34),(2.51,-.12,.12)],white,.014,group)
 patch('Gauntlet_Gold_Cuff_'+side,ga,[(2.105,-pi,pi),(2.14,-pi,pi),(2.17,-pi,pi)],gold,.022,group)
 rod('Wrist_Seal_'+side,(sign*.80,-.015,2.07),(sign*.80,-.015,2.14),.10,rubber,group)
 # Closed articulated hand, both sides. No cannon or connector in this body pass.
 pc=Vector((sign*.81,-.015,1.99))
 box('Palm_'+side,pc,(.215,.16,.23),black,.043,group)
 box('Backhand_Gray_'+side,pc+Vector((0,-.083,.012)),(.175,.025,.14),gray,.014,group)
 for j in range(4):
  x=pc.x+(j-1.5)*.048
  ball('Knuckle_'+side+str(j),(x,-.085,1.91),(.026,.034,.031),black,group)
  box('Curled_Finger_'+side+str(j),(x,-.085,1.88),(.043,.070,.078),gray,.014,group)
 ball('Thumb_Joint_'+side,(pc.x-sign*.11,-.02,2.015),(.045,.06,.06),black,group)
 box('Thumb_'+side,(pc.x-sign*.105,-.08,1.96),(.07,.08,.12),black,.025,group)

# Slender thighs and visible knee hinges above huge flared lower-leg armor.
for sign,side in [(1,'l'),(-1,'r')]:
 group='leg_'+side
 thigh=[(1.43,sign*.335,0,.12,.135),(1.55,sign*.315,0,.135,.155),(1.80,sign*.278,.015,.16,.18),(1.99,sign*.25,.02,.165,.18),(2.04,sign*.25,.02,.14,.15)]
 shell('Thigh_Long_Gray_'+side,thigh,gray,group)
 patch('Thigh_Side_Dark_'+side,thigh,[(1.49,sign*.95,sign*2.50),(1.74,sign*.95,sign*2.45),(1.98,sign*.95,sign*2.35)],black,.008,group)
 # Broken angular striping hugs the long thigh.
 for idx,(za,zb) in enumerate([(1.74,1.79),(1.89,1.94)]):
  patch('Thigh_Red_Marking_'+side+str(idx),thigh,[(za,-.8,.35),(zb,-.8,.35)],red,.013,group)
 ball('Knee_Joint_'+side,(sign*.34,0,1.39),(.14,.15,.135),black,group)
 rod('Knee_Axle_'+side,(sign*.21,0,1.39),(sign*.475,0,1.39),.105,steel,group)
 rod('Knee_Outer_Cap_'+side,(sign*.465,0,1.39),(sign*.49,0,1.39),.083,black,group)
 rod('Knee_Cap_Red_Center_'+side,(sign*.49,0,1.39),(sign*.496,0,1.39),.039,red,group)
 # Front-facing knee guard, bridging into the calf armor.
 panel('Knee_Guard_'+side,[(sign*(.34-.09),-.145,1.44),(sign*(.34+.09),-.145,1.44),(sign*(.34+.10),-.19,1.28),(sign*.34,-.215,1.20),(sign*(.34-.10),-.19,1.28)],black,.045,group,.015)
 calf=[(.15,sign*.425,.02,.31,.31),(.24,sign*.425,.015,.36,.36),(.42,sign*.415,.02,.355,.35),(.66,sign*.395,.025,.31,.30),(.94,sign*.37,.02,.245,.25),(1.17,sign*.345,.015,.18,.19),(1.30,sign*.34,.01,.145,.16)]
 shell('Calf_Flared_Sculpted_'+side,calf,black,group)
 # Red rear/side casing: sweeping diagonally from knee to wide heel.
 rows=[(.19,.50,2.88),(.35,.66,2.9),(.61,.93,2.9),(.89,1.13,2.85),(1.12,1.0,2.55),(1.25,.55,2.22)]
 if sign<0:rows=[(z,-b,-a) for z,a,b in rows]
 patch('Calf_Red_Outer_Armor_'+side,calf,rows,red,.018,group,True)
 # White narrow inset on inside shin defines the stretched proportions.
 rows=[(.23,-1.1,-.78),(.44,-1.04,-.64),(.75,-.95,-.59),(1.06,-.76,-.40),(1.21,-.53,-.32)]
 if sign<0:rows=[(z,-b,-a) for z,a,b in rows]
 patch('Calf_White_Inner_Strip_'+side,calf,rows,white,.015,group)
 # Three-dimensional overlapping front greave, broad near ankle, blade point toward knee.
 rows=[(.32,-.64,.60),(.55,-.71,.73),(.82,-.55,.52),(1.06,-.26,.25),(1.13,-.035,.035)]
 patch('Shin_Gray_Swept_Plate_'+side,calf,rows,gray,.038,group)
 # Sweeping red chevrons, cut into two separate plates on the curved greave.
 patch('Shin_Red_Chevron_Left_'+side,calf,[(.59,-.61,-.54),(.76,-.49,-.35),(.91,-.05,.005)],red,.062,group)
 patch('Shin_Red_Chevron_Right_'+side,calf,[(.66,.57,.63),(.80,.31,.44),(.91,-.005,.05)],red,.062,group)
 # Fine gold border at the ankle, gray rear vent and heel support.
 patch('Ankle_Gold_Rim_'+side,calf,[(.165,-pi,pi),(.205,-pi,pi),(.23,-pi,pi)],gold,.026,group)
 for j in range(4):
  z=.40+j*.055;v=point(calf,z,pi,.012)
  box('Rear_Calf_Vent_'+side+str(j),v,(.18,.025,.016),rubber,.004,group)
 rod('Achilles_Link_'+side,(sign*.40,.27,.30),(sign*.36,.24,1.02),.045,steel,group)
 # Continuous elongated domed toe, substantially wider than the knee.
 foot=[(.075,sign*.425,-.16,.345,.52),(.13,sign*.425,-.16,.37,.54),(.22,sign*.425,-.14,.35,.51),(.32,sign*.425,-.10,.29,.43),(.42,sign*.42,-.04,.20,.30)]
 shell('Boot_Domed_Toe_'+side,foot,black,group)
 patch('Boot_Red_Toe_Armor_'+side,foot,[(.12,-1.60,1.60),(.20,-1.45,1.45),(.29,-.95,.95),(.36,-.45,.45)],red,.015,group)
 patch('Boot_White_Toe_Center_'+side,foot,[(.15,-.20,.20),(.24,-.20,.20),(.33,-.13,.13)],white,.033,group)
 sole=[(.025,sign*.425,-.16,.36,.53),(.07,sign*.425,-.16,.38,.55),(.105,sign*.425,-.16,.38,.55),(.125,sign*.425,-.16,.365,.535)]
 shell('Boot_Gold_Sole_'+side,sole,gold,group)
 # Small sole separations set into lower rim, not oversized cubes.
 for j in range(5):
  a=-1.15+j*.575;p=point(sole,.055,a,.007)
  box('Sole_Groove_'+side+str(j),p,(.016,.025,.036),rubber,.002,group)

# Temporary reference helmet. Final box head / antenna / waveform belong to the later pass.
rod('Neck_Joint',(0,0,3.06),(0,0,3.29),.105,rubber,'head_placeholder')
head=[(3.20,0,.005,.13,.13),(3.28,0,.02,.205,.195),(3.47,0,.03,.245,.235),(3.65,0,.04,.225,.215),(3.77,0,.04,.15,.165),(3.81,0,.04,.045,.07)]
shell('Reference_Helmet_Placeholder',head,black,'head_placeholder')
patch('Helmet_Red_Crest',head,[(3.45,-.19,.19),(3.63,-.22,.22),(3.77,-.25,.25),(3.803,-.3,.3)],red,.018,'head_placeholder')
line('Helmet_Crest_Gold_Trim',[point(head,z,.24,.024) for z in [3.49,3.59,3.68,3.75,3.79]],.007,gold,'head_placeholder')
# White blank sculpted face shield in place of copyrighted human facial details.
panel('Reference_White_Face_Plate',[(-.15,-.172,3.48),(.15,-.172,3.48),(.13,-.213,3.32),(.065,-.218,3.23),(0,-.24,3.20),(-.065,-.218,3.23),(-.13,-.213,3.32)],white,.03,'head_placeholder',.02)
for sign,side in [(1,'l'),(-1,'r')]:
 rows=[(3.28,.65,1.5),(3.45,.5,1.8),(3.62,.5,1.9),(3.72,.55,1.45)]
 if sign<0:rows=[(z,-b,-a) for z,a,b in rows]
 patch('Helmet_Red_Cheek_'+side,head,rows,red,.016,'head_placeholder',True)
 rod('Helmet_Ear_'+side,(sign*.22,.04,3.48),(sign*.265,.04,3.48),.095,black,'head_placeholder')
 rod('Helmet_Ear_Gold_Ring_'+side,(sign*.263,.04,3.48),(sign*.275,.04,3.48),.067,gold,'head_placeholder')
 rod('Helmet_Ear_Red_Inset_'+side,(sign*.275,.04,3.48),(sign*.28,.04,3.48),.045,red,'head_placeholder')

# Applied uniform model scaling: 1.91 m tall, meters and -Y forward.
for o in parts:
 o.location*=.5
 for v in o.data.vertices:v.co*=.5
 # Store clean editable anatomical groups on all parts.
 o['revision']='v003_reference_body';o['status']='body proportion study; head and wrist redesign deferred'
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
# Studio floor and lights are kept out of export.
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,0));floor=bpy.context.object;floor.name='Studio_Floor'
for c in list(floor.users_collection):c.objects.unlink(floor)
studio.objects.link(floor);floor.data.materials.append(floor_mat)

def area(name,loc,energy,size,color):
 data=bpy.data.lights.new(name,'AREA');data.energy=energy;data.shape='DISK';data.size=size;data.color=color
 o=bpy.data.objects.new(name,data);studio.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
area('Key',(-3,-4,5),450,4,(1,.95,.9));area('Fill',(3,-2,3),300,3,(.9,.95,1));area('Rim',(1,3,4),550,3,(1,1,1))
world=bpy.data.worlds.new('Studio_World');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.23,.23,.23,1);world.node_tree.nodes['Background'].inputs[1].default_value=.45;scene.world=world
camera_data=bpy.data.cameras.new('Review_Camera');camera=bpy.data.objects.new('Review_Camera',camera_data);studio.objects.link(camera);scene.camera=camera
camera_data.type='ORTHO';camera_data.ortho_scale=2.18;camera.location=(3,-5,2.65);camera.rotation_euler=(Vector((0,0,.95))-camera.location).to_track_quat('-Z','Y').to_euler()
scene.render.engine='CYCLES';scene.cycles.samples=56;scene.cycles.use_denoising=True
scene.render.resolution_x=1400;scene.render.resolution_y=1800;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.2
scene.render.image_settings.file_format='PNG'
# Helpful native viewport: material colors, camera framing.
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.shading.type='MATERIAL';a.spaces.active.region_3d.view_distance=3
scene['study']='Body silhouette based on the seven supplied armored-robot images. Two hands; mascot head and tool arm deferred.'
scene['head_status']='Temporary reference helmet. Not the final SEIS head.'
scene['provenance']='Created from scratch with local Blender Python; no v001/v002 geometry reused.'
scene['palette']='NU Red C8102E; Bold Gold A4804A; Light Gold C8A978; gray; white; cool black.'
active(parts[0]);bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'seis_robot_reference_body_v003.blend'))
manifest={'blender':bpy.app.version_string,'meshes':len(parts),'triangles':sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),'materials':sorted({m.name for o in parts for m in o.data.materials}),'groups':sorted({o['body_group'] for o in parts}),'status':'static editable body study; no rig or speech controls','old_geometry_reused':False}
(ROOT/'reports'/'model.json').write_text(json.dumps(manifest,indent=2))
scene.render.filepath=str(ROOT/'renders'/'body-three-quarter.png');bpy.ops.render.render(write_still=True)
print('BODY_BUILD_COMPLETE',json.dumps(manifest))
