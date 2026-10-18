"""seis_proxy - a plain grey mannequin built from seis_spec.SEGMENTS, so a part can be seen at the right scale and next
to its neighbours (run_part.py --context).  Not part of the final model."""
import seis_lib as L
import seis_spec as S


def _capsule(name, a, b, ra, rb):
    mid = (a + b) / 2
    sw = L.Sweep([a, mid, b], [(0.0, ra, ra * 0.85, 2.6), (1.0, rb, rb * 0.85, 2.6)])
    ob = sw.mesh(name, nring=24, nstations=8, caps=True, round_start=(ra * 0.8, 3), round_end=(rb * 0.8, 3))
    L.set_material(ob, "dark")
    return ob


def build():
    out = []
    for name, a, b, ra, rb, sided in S.SEGMENTS:
        if sided:
            for side in ("L", "R"):
                out.append(_capsule(f"proxy_{name}.{side}", S.J(f"{a}.{side}"), S.J(f"{b}.{side}"), ra, rb))
        else:
            out.append(_capsule(f"proxy_{name}", S.J(a), S.J(b), ra, rb))
    return out
