"""seis_spec - the master measurements (DIM updated 2026-10-18 from spec/ONMODEL.md section 3: head skull 0.70, waist 1.00, upper arm 0.38, elbow pod 0.45, forearm 0.32/0.34, wrist 0.22; JOINT positions unchanged) and skeleton of the SEIS bot (from spec/proportions.md, 6 clean frontals).

READ THIS FIRST.  Everything is in the STANDING A-POSE figure, in WORLD metres:
  Z up, feet on z = 0, the figure FACES -Y, its LEFT is +X (so its right is -X).  x = 0 is the centre line,
  y = 0 runs through the hip joints.  Total height 2.12 m = 8.3 head-heights.
  H = head height (skull top to the bottom of the silver mask) = 0.2554 m.  Use  hh(1.5)  for "1.5 H" in metres.

    S.J("shoulder.L")      world position (Vector) of a joint ('.L' = +X, '.R' = -X; unsided = on the centre line)
    S.hh(x)                x head-heights in metres
    S.Z(h)                 world height z (m) of "h head-heights above the floor"
    S.DIM[...]             widths / depths as full sizes in metres (see table below)
Depth (y) values carry the biggest uncertainty (+-0.15 H); widths and heights are good to ~ +-3 %.

HEIGHTS (H above the floor): sole 0, ankle 0.35, knee 2.45, hip joint 4.75, crotch 4.07+... see JOINTS,
belt top 5.15, waist 5.45, chest 6.2, neck base 6.9, shoulder joint 6.45, chin 7.3, skull top 8.3.
"""
from mathutils import Vector

HEIGHT = 2.12
UNITS_TOTAL = 8.3
H = HEIGHT / UNITS_TOTAL          # 0.2554 m


def hh(x):
    return x * H


def Z(h):
    return h * H


# (x, y, z) in head-heights; x for the LEFT (+X) joint, mirror for the right
_JOINTS = {
    "root":        (0.00, 0.00, 4.90),     # pelvis centre
    "spine_waist": (0.00, 0.02, 5.45),
    "spine_chest": (0.00, 0.03, 6.20),
    "neck_base":   (0.00, 0.05, 6.90),
    "head_pivot":  (0.00, -0.05, 7.40),    # atlas
    "chin":        (0.00, -0.30, 7.30),
    "head_top":    (0.00, -0.05, 8.30),    # head modelled LEVEL; pitch is added as a pose
    "shoulder":    (1.12, 0.05, 6.45),     # centre of the shoulder joint disc
    "elbow":       (1.18, -0.05, 5.50),    # the round elbow bolt axis
    "wrist":       (1.27, -0.12, 4.44),
    "fingertip":   (1.22, -0.22, 3.83),    # curled
    "hip":         (0.40, 0.00, 4.75),
    "knee":        (0.55, -0.10, 2.45),
    "ankle":       (0.58, 0.00, 0.35),
    "heel":        (0.58, 0.35, 0.00),
    "toe":         (0.58, -1.00, 0.00),
}

_UNSIDED = {"root", "spine_waist", "spine_chest", "neck_base", "head_pivot", "chin", "head_top"}


def J(name):
    """World position of a joint: 'shoulder.L', 'knee.R', 'neck_base', ..."""
    if name in _UNSIDED:
        x, y, z = _JOINTS[name]
        return Vector((x * H, y * H, z * H))
    base, side = name[:-2], name[-1]
    x, y, z = _JOINTS[base]
    return Vector(((x if side == "L" else -x) * H, y * H, z * H))


# full sizes in metres (width = along x, depth = along y).  Source: proportions.md section 2 and 3.3
DIM = {
    "head_width_skull": hh(0.70), "head_width_blades": hh(0.93), "head_depth": hh(1.0), "head_height": hh(1.0),
    "neck_width": hh(0.60), "neck_depth": hh(0.55),
    "shoulder_span": hh(2.90),               # pauldron tip to tip
    "chest_width": hh(1.90), "chest_depth": hh(1.35),
    "waist_width": hh(1.00), "waist_depth": hh(0.90),
    "pelvis_width": hh(1.45), "pelvis_depth": hh(1.15),
    "upper_arm_width": hh(0.38), "upper_arm_depth": hh(0.38),
    "elbow_pod_width": hh(0.45),
    "forearm_width": hh(0.32), "forearm_depth": hh(0.34),
    "wrist_width": hh(0.22),
    "thigh_width": hh(0.90), "thigh_depth": hh(1.00),
    "both_thighs_width": hh(1.75),
    "shin_width": hh(0.58), "shin_depth": hh(0.75),
    "foot_width": hh(0.70), "foot_length": hh(1.35),
    "pauldron_height": hh(0.95), "pauldron_depth": hh(1.0), "pauldron_width_each": hh(1.4),
}

# plain proxy capsules for run_part.py --context :  name, joint a, joint b, radius at a, radius at b, sided
SEGMENTS = [
    ("pelvis", "root", "spine_waist", hh(0.72), hh(0.62), False),
    ("abdomen", "spine_waist", "spine_chest", hh(0.62), hh(0.90), False),
    ("chest", "spine_chest", "neck_base", hh(0.95), hh(0.62), False),
    ("neck", "neck_base", "head_pivot", hh(0.30), hh(0.28), False),
    ("head", "chin", "head_top", hh(0.36), hh(0.38), False),
    ("upperarm", "shoulder", "elbow", hh(0.24), hh(0.23), True),
    ("forearm", "elbow", "wrist", hh(0.27), hh(0.15), True),
    ("hand", "wrist", "fingertip", hh(0.14), hh(0.09), True),
    ("thigh", "hip", "knee", hh(0.45), hh(0.32), True),
    ("shin", "knee", "ankle", hh(0.30), hh(0.20), True),
    ("foot", "ankle", "toe", hh(0.20), hh(0.14), True),
]


def mirror_point(p):
    return Vector((-p.x, p.y, p.z))
