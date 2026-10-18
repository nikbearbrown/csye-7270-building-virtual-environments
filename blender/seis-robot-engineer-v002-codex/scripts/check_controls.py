import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];s=bpy.context.scene;rig=bpy.data.objects['SEIS_Engineer_Rig']
def center(name):
    o=bpy.data.objects['SEIS_Engineer_'+name].evaluated_get(bpy.context.evaluated_depsgraph_get())
    return sum((o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8
states=[]
for dep in [0,.25,.5,.75,1]:
    rig['tool_deployed']=dep;rig.update_tag();s.frame_set(1);bpy.context.view_layer.update()
    states.append({'deployment':dep,'tip_center':list(center('Jack_Rounded_Solid_Tip')),'palm_center':list(center('Split_Palm_-1')),'finger_rotation':rig.pose.bones['tool_finger_0'].rotation_euler.x})
assert abs(states[0]['tip_center'][2]-states[-1]['tip_center'][2]-.24)<.001
assert abs(states[0]['finger_rotation'])<.001 and states[-1]['finger_rotation']>2.69
assert len([o for o in bpy.data.objects if o.name.startswith('SEIS_Engineer_Spool_Cap_')])==6
mouth=bpy.data.objects['SEIS_Engineer_Waveform_Mouth']
assert {'Speaking','Emphasis'}<=set(mouth.data.shape_keys.key_blocks.keys())
assert tuple(mouth.active_material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value[:3])==(0,0,0)
screen=bpy.data.objects['SEIS_Engineer_Wrist_Status_0'];rig['screen_orient']=0;rig.update_tag();s.frame_set(1);z1=screen.location.z;s.frame_set(21);z2=screen.location.z
assert abs(z1-z2)>.005
bad=[]
for o in bpy.data.collections['EXPORT'].objects:
    if o.type!='MESH':continue
    if any(len(v.groups)!=1 or abs(v.groups[0].weight-1)>1e-5 for v in o.data.vertices):bad.append(o.name)
assert not bad
report={'status':'PASS','tool_states':states,'connector_travel_m':.24,'spool_caps':6,'mouth':'Black with Speaking and Emphasis morphs','wrist_scroll_positions':[z1,z2],'invalid_weight_meshes':bad,'limits':'Visual controls only; no simulation, real agent connection or audio synchronization.'}
(R/'reports/controls.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

