import seis_lib as L, seis_spec as S, math
def build():
    sw = L.Sweep([S.J("elbow.L"), S.J("wrist.L")], [(0, S.hh(0.25), S.hh(0.2), 3), (1, S.hh(0.14), S.hh(0.12), 2.6)])
    core = sw.mesh("arm_core.L", nring=40, round_end=(0.01, 2)); L.finish(core, "dark", bevel=0, bone="forearm.L")
    p = sw.panel("arm_plate.L", 0.05, 0.95, math.radians(40), math.radians(140), thickness=0.006, inflate=0.004, height=0.008, ends=0.2)
    L.finish(p, "teal", bevel=0.002, bone="forearm.L", wear=0.7)
    return [core, p, L.mirror_x(p)]
