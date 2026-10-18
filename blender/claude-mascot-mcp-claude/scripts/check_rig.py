import bpy
rig = bpy.data.objects.get("ClaudeMascotRig")
print("rig:", rig.name if rig else None, "bones:", [b.name for b in rig.data.bones] if rig else None)
for pb in rig.pose.bones:
    print("pose bone %-6s loc %s scale %s" % (pb.name, tuple(round(v, 4) for v in pb.location), tuple(round(v, 4) for v in pb.scale)))
for n in ("Torso","ArmL","ArmR","EyeL","EyeR","Leg1","Leg2","Leg3","Leg4"):
    o = bpy.data.objects[n]
    w = o.matrix_world.translation
    print("%-6s parent=%s/%s  world (%.4f %.4f %.4f) dims (%.3f %.3f %.3f)  modifiers=%s vgroups=%d" % (n, o.parent.name if o.parent else None, o.parent_bone, *w, *o.dimensions, [m.type for m in o.modifiers], len(o.vertex_groups)))
