"""Clean empty build collections and set an uncluttered opening viewport."""
import bpy
from pathlib import Path
for c in list(bpy.data.collections):
    if not c.objects and not c.children:bpy.data.collections.remove(c)
for c in bpy.data.collections:
    if c.name.startswith('USS ENTERPRISE'):c.name='USS ENTERPRISE • NCC-1701'
    if c.name.startswith('STUDIO'):c.name='STUDIO • cameras and lights'
bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=False,do_recursive=True)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            s=area.spaces.active;s.overlay.show_overlays=False;s.shading.type='MATERIAL';s.region_3d.view_perspective='CAMERA';s.region_3d.view_camera_zoom=18
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath,compress=False)
print('Clean opening view saved:',bpy.data.filepath)
