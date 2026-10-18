"""_proxy - grey mannequin parts WITH bone assignments, used to test the rig and the seated pose before real parts exist."""
import seis_lib as L, seis_spec as S, seis_proxy
BONE = {"pelvis": "root", "abdomen": "abdomen", "chest": "chest", "neck": "neck", "head": "head",
        "upperarm": "upperarm", "forearm": "forearm", "hand": "hand", "thigh": "thigh", "shin": "shin", "foot": "foot"}
def build():
    objs = seis_proxy.build()
    for ob in objs:
        base = ob.name.replace("proxy_", "")
        side = base[-2:] if base[-2:] in (".L", ".R") else ""
        key = base[:-2] if side else base
        ob["bone"] = BONE[key] + side
        ob.name = "proxy_" + key + side
    return objs
