"""seis_rig - the rigid FK rig for the SEIS bot.

    rig = seis_rig.build_rig(objs)         create the armature at the standing A-pose and bind every mesh rigidly
    seis_rig.bone_names(rig)               the list of bone names
    seis_rig.pose(rig, {"upperarm.R": (rx, ry, rz) ...}, world=True)   (degrees, rotation about WORLD axes at the joint)
    seis_rig.clear_pose(rig)

Each mesh is bound to the single bone named in its custom property "bone" (set by L.finish(..., bone=...)): a vertex
group of that name with weight 1.0 on every vertex + an Armature modifier.  Finger phalanges get bones derived from the
object itself (head = object origin = proximal joint, tail = far end of the mesh).
The rig is FK only: no IK, no facial bones, no constraints, no collision.
"""
import math
import bpy
from mathutils import Vector, Matrix, Euler

import seis_lib as L
import seis_spec as S

_FINGERS = ("thumb", "index", "middle", "ring", "pinky")


def _chain():
    """(name, head, tail, parent) for the structural bones, from seis_spec.J()."""
    J = S.J
    out = [
        ("root", J("root"), J("spine_waist"), None),
        ("abdomen", J("spine_waist"), J("spine_chest"), "root"),
        ("chest", J("spine_chest"), J("neck_base"), "abdomen"),
        ("neck", J("neck_base"), J("head_pivot"), "chest"),
        ("head", J("head_pivot"), J("head_top"), "neck"),
    ]
    for side in ("L", "R"):
        sh, el, wr, fi = J(f"shoulder.{side}"), J(f"elbow.{side}"), J(f"wrist.{side}"), J(f"fingertip.{side}")
        hip, kn, an, he, to = J(f"hip.{side}"), J(f"knee.{side}"), J(f"ankle.{side}"), J(f"heel.{side}"), J(f"toe.{side}")
        ball = an.lerp(to, 0.62)
        ball.z = S.hh(0.12)
        out += [
            (f"pauldron.{side}", sh, sh + Vector((0, 0, S.hh(0.6))), "chest"),
            (f"upperarm.{side}", sh, el, f"pauldron.{side}"),
            (f"forearm.{side}", el, wr, f"upperarm.{side}"),
            (f"hand.{side}", wr, wr.lerp(fi, 0.8), f"forearm.{side}"),
            (f"thigh.{side}", hip, kn, "root"),
            (f"shin.{side}", kn, an, f"thigh.{side}"),
            (f"foot.{side}", an, ball, f"shin.{side}"),
            (f"toes.{side}", ball, to, f"foot.{side}"),
        ]
    return out


def _finger_bones(objs):
    """Derive (name, head, tail, parent) for every object whose bone is a finger phalanx."""
    res = []
    for ob in objs:
        b = ob.get("bone")
        if not b or b[-2] != ".":
            continue
        base = b[:-2]
        if len(base) < 2 or base[:-1] not in _FINGERS or not base[-1].isdigit():
            continue
        side = b[-1]
        fing, idx = base[:-1], int(base[-1])
        head = ob.matrix_world.translation.copy()
        far, best = head + Vector((0, -0.02, 0)), -1.0
        for v in ob.data.vertices:
            w = ob.matrix_world @ v.co
            d = (w - head).length
            if d > best:
                best, far = d, w
        parent = f"hand.{side}" if idx == 1 else f"{fing}{idx - 1}.{side}"
        res.append((b, head, far, parent, fing, idx))
    # one bone per name (several meshes may share a bone, keep the longest)
    uniq = {}
    for r in res:
        if r[0] not in uniq or (r[2] - r[1]).length > (uniq[r[0]][2] - uniq[r[0]][1]).length:
            uniq[r[0]] = r
    return [(n, h, t, p) for n, h, t, p, *_ in sorted(uniq.values(), key=lambda r: (r[0][-1], r[4], r[5]))]


def build_rig(objs, name="SEIS_rig", collection=None):
    prev_mode = None
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    ad = bpy.data.armatures.new(name)
    ad.display_type = "OCTAHEDRAL"
    rig = bpy.data.objects.new(name, ad)
    (collection or L._COLL or bpy.context.scene.collection).objects.link(rig)
    rig.show_in_front = True
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bones = _chain() + _finger_bones(objs)
    made = {}
    for nm, head, tail, parent in bones:
        eb = ad.edit_bones.new(nm)
        eb.head, eb.tail = head, tail
        if (tail - head).length < 1e-4:
            eb.tail = head + Vector((0, 0, 0.01))
        made[nm] = eb
    for nm, head, tail, parent in bones:
        if parent and parent in made:
            made[nm].parent = made[parent]
    bpy.ops.object.mode_set(mode="OBJECT")
    # bind
    unbound = []
    for ob in objs:
        b = ob.get("bone")
        if not b or b not in ad.bones:
            unbound.append(ob.name)
            continue
        for vg in list(ob.vertex_groups):
            ob.vertex_groups.remove(vg)
        vg = ob.vertex_groups.new(name=b)
        vg.add(list(range(len(ob.data.vertices))), 1.0, "REPLACE")
        for m in [m for m in ob.modifiers if m.type == "ARMATURE"]:
            ob.modifiers.remove(m)
        mod = ob.modifiers.new("Armature", "ARMATURE")
        mod.object = rig
        ob.parent = rig
        ob.parent_type = "OBJECT"
        ob.matrix_parent_inverse = rig.matrix_world.inverted()
    rig["unbound_objects"] = ", ".join(unbound)
    return rig


def bone_names(rig):
    return [b.name for b in rig.data.bones]


def clear_pose(rig):
    for pb in rig.pose.bones:
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)
    bpy.context.view_layer.update()


def pose(rig, rots, world=True):
    """Rotate bones.  rots = {bone: (rx, ry, rz) degrees}.  With world=True each rotation is about the WORLD axes
    through the bone's own joint (head), applied on top of its parent's pose, so 'flexion' of the elbow is simply a
    rotation about world X.  Bones are processed parent-first."""
    clear_pose(rig)
    order = []

    def visit(b):
        order.append(b)
        for c in b.children:
            visit(c)
    for b in rig.data.bones:
        if b.parent is None:
            visit(b)
    for b in order:
        r = rots.get(b.name)
        if not r:
            continue
        pb = rig.pose.bones[b.name]
        bpy.context.view_layer.update()
        cur = pb.matrix.copy()                         # armature space (pose)
        head = cur.translation.copy()
        R = Euler([math.radians(a) for a in r], "XYZ").to_matrix().to_4x4()
        T1, T0 = Matrix.Translation(head), Matrix.Translation(-head)
        new = T1 @ R @ T0 @ cur if world else cur @ R
        pb.matrix = new
    bpy.context.view_layer.update()


def pose_abs(rig, rots, root_offset=(0.0, 0.0, 0.0)):
    """ABSOLUTE FK posing.  rots = {bone: (rx, ry, rz) degrees}: the bone's orientation relative to its REST orientation,
    as a rotation about the WORLD axes (XYZ order), NOT relative to the parent.  A bone not listed keeps the orientation
    of its parent's delta (it follows its parent rigidly).  Head positions follow the parent chain.  root_offset moves the
    whole figure.  Example: thigh {-99,0,0} = thigh points 9 degrees above horizontal toward the front (-Y)."""
    clear_pose(rig)
    order = []

    def visit(b):
        order.append(b)
        for c in b.children:
            visit(c)
    for b in rig.data.bones:
        if b.parent is None:
            visit(b)
    delta = {}                                    # bone name -> world rotation matrix (3x3) currently applied
    for b in order:
        pb = rig.pose.bones[b.name]
        if b.name in rots:
            R = Euler([math.radians(a) for a in rots[b.name]], "XYZ").to_matrix()
        else:
            R = delta[b.parent.name] if b.parent else Matrix.Identity(3)
        delta[b.name] = R
        # head position: rest head carried through the parent's rigid pose
        if b.parent:
            ppb = rig.pose.bones[b.parent.name]
            rel = b.head_local - b.parent.head_local
            head = ppb.matrix.translation + delta[b.parent.name] @ rel
            head = head
        else:
            head = b.head_local + Vector(root_offset)
        rest3 = b.matrix_local.to_3x3()
        M = (R @ rest3).to_4x4()
        M.translation = head
        pb.matrix = M
        bpy.context.view_layer.update()
    bpy.context.view_layer.update()
