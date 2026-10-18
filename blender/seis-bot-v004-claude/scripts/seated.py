"""seated - the Thinker pose study (spec/ONMODEL.md section 4, frames 01/02): the robot's RIGHT hand covers its mouth,
the right elbow rests on the right thigh just above the knee, the LEFT elbow rests on the left knee with the forearm
sloping down and inward, hand limp; it sits on the three-part stone plinth, feet flat on the pale dais.

    rig = bpy.data.objects["SEIS_rig"]
    info = seated.apply(rig)         # poses the bones (FK, no IK), grounds the feet, builds the plinth, returns a dict

Poses are given as ABSOLUTE world directions for limb bones (aim) and absolute lean angles for the spine; the elbow
targets are solved so the elbows really touch the thighs (a tiny two-bone solve, still pure FK in the end).
"""
import math
import bpy
from mathutils import Vector, Euler

import seis_lib as L
import seis_spec as S
import seis_rig

LEAN = 24.0          # degrees: chest forward lean (hip -> neck base ~20 deg, spec); solved below to make the elbow touch
HEAD_BOW = 30.0      # on-model: bowed 30 deg (25-40)
HEAD_ROLL = -4.0     # toward the supporting (right = -X) hand, small
THIGH_Z = 0.08      # z component of the thigh direction (0.08 = 4.6 deg above horizontal; stills say ~9 but then the pelvis sits 4 cm below the
                    # plinth top: scanned 2026-10-18 so the pelvis bottom lands on the 0.442 m seat)
ELBOW_T = 0.52       # where along the thigh (0 = hip, 1 = knee) the elbows rest. ONMODEL says just above the knee (~0.8) but our
                     # arm is short against the thigh, so 0.8 needs a 52 deg hunch; 0.64 gives a believable ~35 deg lean


def aim(rig, bone, d):
    """Euler XYZ degrees (about world axes) that turn the bone's REST direction onto world direction d."""
    b = rig.data.bones[bone]
    rest = (b.tail_local - b.head_local).normalized()
    q = rest.rotation_difference(Vector(d).normalized())
    e = q.to_euler("XYZ")
    return tuple(math.degrees(a) for a in e)


def _spine(lean):
    # spine bones point UP: a forward lean is a POSITIVE rotation about world X
    return {"root": (0.40 * lean, 0, 0), "abdomen": (0.70 * lean, 0, 0), "chest": (lean, 0, 0),
            "neck": (1.25 * lean, 0, 0), "head": (HEAD_BOW, HEAD_ROLL, 0)}


def _legs(rig):
    r = {}
    for side, sx in (("L", +1), ("R", -1)):
        r[f"thigh.{side}"] = aim(rig, f"thigh.{side}", (sx * 0.33, -0.95, THIGH_Z))     # 9 deg above horizontal, knees ~0.58 m apart
        r[f"shin.{side}"] = aim(rig, f"shin.{side}", (sx * 0.0, -0.05, -1.0))         # near vertical
        r[f"foot.{side}"] = aim(rig, f"foot.{side}", (sx * 0.12, -0.99, 0.0))        # flat, slight toe-out
    return r


def _posed_point(rig, bone, rest_point):
    b = rig.data.bones[bone]
    pb = rig.pose.bones[bone]
    return pb.matrix @ (b.matrix_local.inverted() @ rest_point)


def _along_thigh(rig, side, t):
    pb = rig.pose.bones[f"thigh.{side}"]
    return pb.head.lerp(pb.tail, t)


def _solve(rig, lean_range=(8, 60)):
    """Find the chest lean for which the right elbow target (on the right thigh, 0.2 U behind the knee) is exactly one
    upper-arm length from the right shoulder.  Returns (lean, info)."""
    l1 = (S.J("elbow.R") - S.J("shoulder.R")).length
    best = None
    for lean in range(int(lean_range[0] * 2), int(lean_range[1] * 2) + 1):
        lean = lean / 2.0
        rots = {}
        rots.update(_spine(lean))
        rots.update(_legs(rig))
        seis_rig.pose_abs(rig, rots)
        E = _along_thigh(rig, "R", ELBOW_T) + Vector((0, 0, 0.19))
        Sh = rig.pose.bones["upperarm.R"].head.copy()
        f = abs((E - Sh).length - l1)
        if best is None or f < best[0]:
            best = (f, lean, E.copy(), Sh.copy())
    return best


def pose_dict(rig, lean=None):
    f, lean_s, E_R, S_R = _solve(rig)
    lean = lean_s if lean is None else lean
    rots = {}
    rots.update(_spine(lean))
    rots.update(_legs(rig))
    seis_rig.pose_abs(rig, rots)
    # elbow targets on each thigh, 0.2 U behind the knee
    E_R = _along_thigh(rig, "R", ELBOW_T) + Vector((0, 0, 0.19))
    E_L = _along_thigh(rig, "L", ELBOW_T) + Vector((0, 0, 0.19))
    S_R = rig.pose.bones["upperarm.R"].head.copy()
    S_L = rig.pose.bones["upperarm.L"].head.copy()
    # mouth point = just below the muzzle, carried by the posed head bone
    mouth_rest = S.J("chin") + Vector((0, -S.hh(0.28), S.hh(0.15)))
    M = _posed_point(rig, "head", mouth_rest)
    rots["upperarm.R"] = aim(rig, "upperarm.R", E_R - S_R)
    rots["forearm.R"] = aim(rig, "forearm.R", M - E_R)
    rots["hand.R"] = aim(rig, "hand.R", (M - E_R) + Vector((0.0, -0.25, 0.1)))
    rots["upperarm.L"] = aim(rig, "upperarm.L", E_L - S_L)
    rots["forearm.L"] = aim(rig, "forearm.L", (-0.42, -0.72, -0.55))      # slopes ~35 deg below horizontal, down and inward
    rots["hand.L"] = aim(rig, "hand.L", (-0.10, -0.35, -0.93))            # hand limp, fingers hanging
    return rots, {"lean": lean, "solve_err_m": round(f, 4), "elbow_R": tuple(round(x, 3) for x in E_R),
                  "elbow_L": tuple(round(x, 3) for x in E_L), "mouth": tuple(round(x, 3) for x in M)}


def _eval_zmin(rig, bone_prefixes, axis_filter=None):
    dg = bpy.context.evaluated_depsgraph_get()
    zmin = 1e9
    for ob in bpy.data.objects:
        if ob.type != "MESH" or ob.parent != rig or ob.get("static"):
            continue
        if not str(ob.get("bone", "")).startswith(bone_prefixes):
            continue
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        w = ob.matrix_world
        for v in me.vertices:
            p = w @ v.co
            if axis_filter is None or axis_filter(p):
                zmin = min(zmin, p.z)
        ev.to_mesh_clear()
    return zmin


def apply(rig, block=True):
    rots, info = pose_dict(rig)
    seis_rig.pose_abs(rig, rots)
    z_feet = _eval_zmin(rig, ("foot", "toes"))
    import pedestal
    dz = pedestal.DAIS_T - z_feet                       # feet stand on the dais top
    seis_rig.pose_abs(rig, rots, root_offset=(0, 0, dz))
    bpy.context.view_layer.update()
    info["floor_shift_z"] = round(dz, 4)
    if block:
        d = pedestal.dims()
        z_seat = _eval_zmin(rig, ("root",), lambda p: abs(p.x) < 0.25)      # lowest point of the pelvis centre
        hip_y = rig.pose.bones["thigh.L"].head.y
        rear_y = hip_y + 0.1 * d["U"]                                         # the hip joint sits 0.1 U inside the rear face
        cy = rear_y - d["depth"] / 2
        L.set_collection(L.collection("PEDESTAL", L.collection("SEIS_BOT")))
        objs = pedestal.build(center=(0.0, cy), seat_z=z_seat)
        info.update(seat_z_pelvis_bottom=round(z_seat, 4), plinth_top_z=round(pedestal.DAIS_T + d["height"], 4),
                    plinth_center_y=round(cy, 4), plinth=d)
    return info
