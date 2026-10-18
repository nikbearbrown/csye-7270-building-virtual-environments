"""Small final surface/camera adjustments shared by native build and finishing."""
import bpy, math, sys, json
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from cleanup_geometry import _prune_mesh_triangles_by_audit

def refine(scene,waist_compaction=.052):
    repairs=[]
    for name in ['Pectoral_Deep_Gasket_L','Pectoral_Deep_Gasket_R']:
        gasket=bpy.data.objects.get(name)
        if gasket and not gasket.get('recessed_under_frame'):
            xs=[v.co.x for v in gasket.data.vertices];zs=[v.co.z for v in gasket.data.vertices]
            cx=(min(xs)+max(xs))/2;cz=(min(zs)+max(zs))/2
            for v in gasket.data.vertices:
                v.co.x=cx+(v.co.x-cx)*.96;v.co.z=cz+(v.co.z-cz)*.96;v.co.y+=.006
            gasket.data.update();gasket['recessed_under_frame']=True
        if gasket:
            removed=_prune_mesh_triangles_by_audit(gasket.data)
            repairs.append({'object':gasket.name,'zero_area_faces_removed_after_final_recess':removed})
    ob=bpy.data.objects.get('Chest_Six_Lato')
    def surface(x,z):return -.188+.67*x*x-.025*math.exp(-((z-1.68)/.115)**2)
    if ob and not ob.get('surface_conformed'):
        anchor=surface(0,1.664)
        for v in ob.data.vertices:
            x=v.co.x+ob.location.x
            z=v.co.z+ob.location.z+waist_compaction
            v.co.y+=surface(x,z)-anchor
        ob.data.update();ob['surface_conformed']=True
        ob['lettering']='Lato Bold, projected as shallow physical relief onto the centered dark sternum badge'
    cam=bpy.data.objects['CAM_Hero']
    cam.data.type='PERSP';cam.data.sensor_fit='VERTICAL';cam.data.sensor_height=24
    distance=(cam.location-Vector((0,0,1.10))).length
    cam.data.lens=24*distance/2.47
    scene['waist_compaction_metres']=waist_compaction
    if bpy.data.filepath:
        p=Path(bpy.data.filepath).parent/'reports'/'final-surface-adjustments.json'
        p.write_text(json.dumps({'gasket_recess_metres':.006,'gasket_planar_scale':.96,'audit_cross_length_limit':1e-13,'repairs':repairs},indent=2)+'\n')

if __name__=='__main__':
    refine(bpy.context.scene)
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
