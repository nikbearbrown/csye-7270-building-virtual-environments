# executed inside build_robot.py (uses arm, set_rot, q_world, R, V)
PEDESTAL_TOP = 0.45
PEDESTAL_LOC = (0.0, 0.03, 0.0)
SEAT_DROP = -0.545
CHIN = (0.0, -0.07, 1.89)
SEAT_Z = None

def set_loc_world(name, vec):
    pb = arm.pose.bones[name]
    pb.location = pb.bone.matrix_local.to_3x3().inverted() @ V(vec)

def posed_point(bone_name, rest_pt):
    bpy.context.view_layer.update()
    pb = arm.pose.bones[bone_name]
    return arm.matrix_world @ (pb.matrix @ pb.bone.matrix_local.inverted() @ (V(rest_pt) * GS))

def curl(sd, a1, a2, a3, thumb=(20, 20, 20), spread=0.0):
    sgn = 1 if sd == '.L' else -1
    for j in range(4):
        for k, a in enumerate((a1, a2, a3)):
            q = q_world((0, 1, 0), sgn * a)
            if k == 0 and spread:
                q = q_world((1, 0, 0), (j - 1.5) * spread) @ q
            set_rot('f%d_%d%s' % (j, k + 1, sd), q)
    for k, a in enumerate(thumb):
        set_rot('thumb_%d%s' % (k + 1, sd), q_world((0, 0, 1), -sgn * a) if k == 0 else q_world((1, -sgn * 0.3, 0), a))

def pose_standing():
    for s, sd in ((1, '.L'), (-1, '.R')):
        set_rot('upper_arm' + sd, q_world((0, 1, 0), -s * 4))
        set_rot('forearm' + sd, q_world((1, 0, 0), -10))
        set_rot('hand' + sd, q_world((1, 0, 0), -4))
        curl(sd, 18, 22, 15, thumb=(10, 10, 10))
        set_rot('thigh' + sd, q_world((0, 1, 0), -s * 2))
    set_rot('head', q_world((1, 0, 0), 4))

def ik_apply(chain_end, target, pole_pt, elbow_goal):
    tgt = bpy.data.objects.new('IK_tgt_' + chain_end, None); bpy.context.scene.collection.objects.link(tgt)
    tgt.location = target
    pol = bpy.data.objects.new('IK_pole_' + chain_end, None); bpy.context.scene.collection.objects.link(pol)
    pol.location = pole_pt
    pb = arm.pose.bones[chain_end]
    c = pb.constraints.new('IK'); c.target = tgt; c.pole_target = pol; c.chain_count = 2
    best = None
    for ang in range(-180, 180, 15):
        c.pole_angle = R(ang)
        bpy.context.view_layer.update()
        e = arm.matrix_world @ pb.head
        d = (e - V(elbow_goal)).length
        if best is None or d < best[0]: best = (d, ang)
    c.pole_angle = R(best[1]); bpy.context.view_layer.update()
    names = [pb.parent.name, pb.name]
    mats = {n: arm.pose.bones[n].matrix.copy() for n in names}
    pb.constraints.remove(c)
    for n in names:
        arm.pose.bones[n].matrix = mats[n]
        bpy.context.view_layer.update()
    bpy.data.objects.remove(tgt); bpy.data.objects.remove(pol)
    tip = arm.matrix_world @ pb.tail
    print('IK', chain_end, 'pole', best[1], 'elbow err', round(best[0], 3), 'wrist err', round((tip - V(target)).length, 3))

def torso(a, b, hd):
    set_rot('spine', q_world((1, 0, 0), a) @ q_world((0, 1, 0), -3))
    set_rot('chest', q_world((1, 0, 0), a * 0.8) @ q_world((0, 0, 1), 8))
    set_rot('neck', q_world((1, 0, 0), 22))
    set_rot('head', q_world((0, 0, 1), -6) @ q_world((1, 0, 0), hd) @ q_world((0, 1, 0), 6))
    set_rot('shoulder.R', q_world((0, 0, 1), b) @ q_world((0, 1, 0), -b * 0.4))

def pose_thinker():
    set_loc_world('root', (0, 0, SEAT_DROP * GS))
    for s, sd in ((1, '.L'), (-1, '.R')):
        set_rot('thigh' + sd, q_world((0, 0, 1), s * 21) @ q_world((1, 0, 0), -122))
        set_rot('shin' + sd, q_world((0, 1, 0), -s * 3) @ q_world((1, 0, 0), 96))
        set_rot('foot' + sd, q_world((0, 0, 1), -s * 14) @ q_world((1, 0, 0), 26))
    bpy.context.view_layer.update()
    global SEAT_Z
    fz = min(posed_point('foot' + sd, (s * 0.12, y, z)).z for s, sd in ((1, '.L'), (-1, '.R')) for y, z in ((0.06, 0.003), (-0.19, 0.012), (-0.06, 0.003)))
    set_loc_world('root', (0, 0, SEAT_DROP * GS - fz + 0.004)); bpy.context.view_layer.update()
    SEAT_Z = min(posed_point('thigh' + sd, (s * 0.12, 0.11, zz)).z for s, sd in ((1, '.L'), (-1, '.R')) for zz in (1.0, 0.95, 0.9)) + 0.004
    print('SEAT_Z', SEAT_Z, 'footz', fz)
    Lu = arm.pose.bones['upper_arm.R'].bone.length; Lf = arm.pose.bones['forearm.R'].bone.length
    E = posed_point('thigh.R', (-0.12, -0.1, 0.72)) + V((0, 0, 0.045))
    best = None
    for a in range(4, 26, 2):
        for b in range(0, 36, 4):
            for hd in (-10, -4, 2):
                torso(a, b, hd)
                bpy.context.view_layer.update()
                S = arm.matrix_world @ arm.pose.bones['upper_arm.R'].head
                W = posed_point('head', CHIN) + V((-0.006, -0.045, -0.10))
                cost = ((S - E).length - Lu * 0.97) ** 2 + ((W - E).length - Lf * 0.97) ** 2 + 0.0004 * b / 10 + 0.0012 * abs(a - 10) / 10
                if best is None or cost < best[0]: best = (cost, a, b, hd)
    print('TORSO best', best)
    torso(best[1], best[2], best[3]); bpy.context.view_layer.update()
    S = arm.matrix_world @ arm.pose.bones['upper_arm.R'].head
    W = posed_point('head', CHIN) + V((-0.006, -0.045, -0.10))
    ik_apply('forearm.R', W, E + (E - (S + W) / 2).normalized() * 0.6, E)
    # left arm: forearm along left thigh, wrist over the knee
    kneeT = posed_point('thigh.L', KNEE_T)
    EL = V(ELB_W) * GS
    SL = arm.matrix_world @ arm.pose.bones['upper_arm.L'].head
    WL = kneeT + V(WL_OFF)
    print('LEFT kneeT', kneeT, 'EL', EL, 'WL', WL)
    ik_apply('forearm.L', WL, EL + (EL - (SL + WL) / 2).normalized() * 0.6, EL)
    set_rot('hand.R', HAND_R)
    curl('.R', 95, 100, 85, thumb=(50, 55, 45))
    set_rot('hand.L', HAND_L)
    curl('.L', 30, 40, 30, thumb=(20, 20, 15), spread=3)

HAND_R = q_world((0, 0, 1), 90) @ q_world((1, 0, 0), -12)
HAND_L = q_world((1, 0, 0), 70) @ q_world((0, 0, 1), -60)
KNEE_T = (0.12, -0.10, 0.64); ELB_W = (0.33, -0.12, 0.90); WL_OFF = (0.03, -0.06, 0.04)

def cameras():
    bpy.context.view_layer.update()
    head = posed_point('head', (0, 0.0, 2.03))
    chest = posed_point('chest', (0, -0.05, 1.62))
    c = {}
    c['Cam_Front'] = ((0, -4.6, 1.0), (0, -0.14, 0.84), 80)
    c['Cam_34'] = ((-2.7, -3.75, 1.2), (0, -0.12, 0.84), 80)
    c['Cam_Side'] = ((-4.6, -0.15, 1.0), (0, -0.12, 0.84), 80)
    mid = (head + chest) / 2
    c['Cam_Shoulder34'] = ((-1.5, -1.9, 1.75 * GS), (-0.2, 0.0, 1.66 * GS), 100)
    c['Cam_Close'] = ((mid.x + 0.75, mid.y - 2.05, mid.z - 0.12), (mid.x, mid.y, mid.z - 0.06), 85)
    c['Cam_Back34'] = ((3.6, 4.2, 1.6), (0, 0.0, 0.9), 80)
    c['Cam_Stand_Front'] = ((0, -6.8, 1.15), (0, 0, 1.1), 85)
    c['Cam_Stand_34'] = ((-3.8, -5.6, 1.35), (0, 0, 1.1), 85)
    c['Cam_HeadFront'] = ((0, -2.3, 2.04 * GS), (0, 0.0, 2.04 * GS), 150)
    c['Cam_HeadSide'] = ((-2.3, 0.02, 2.04 * GS), (0, 0.02, 2.04 * GS), 150)
    c['Cam_Head34'] = ((-1.4, -1.85, 2.06 * GS), (0, 0.0, 2.03 * GS), 120)
    c['Cam_Chest'] = ((0.25, -2.6, 1.62 * GS), (0, 0.0, 1.62 * GS), 100)
    return c
