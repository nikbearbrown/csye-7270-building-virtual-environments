# Decode the JSON chunk of the three Act-I probe .glb files: what the exporter really wrote.   python3 glb_json.py
import json, struct, glob, os
here = os.path.dirname(os.path.abspath(__file__))
for p in sorted(glob.glob(os.path.join(here, "..", "probe", "godot", "column_*.glb"))):
    b = open(p, "rb").read()
    ln, typ = struct.unpack("<II", b[12:20]); j = json.loads(b[20:20 + ln])
    n = j["nodes"][0]
    pos = j["accessors"][j["meshes"][0]["primitives"][0]["attributes"]["POSITION"]]
    print(os.path.basename(p), "node:", {k: n[k] for k in n if k in ("name", "scale", "rotation", "translation")},
          "POSITION min", pos["min"], "max", pos["max"])
