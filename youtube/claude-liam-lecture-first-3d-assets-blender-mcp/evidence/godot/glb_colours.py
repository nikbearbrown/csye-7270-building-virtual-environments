# glb_colours.py - plain Python (no Blender, no Godot): reads the JSON chunk of each .glb and prints every material's
# baseColorFactor (linear) and the sRGB hex that corresponds to it, i.e. the colour that is in the exported file.
#   python3 glb_colours.py <file.glb> ...
import json, struct, sys

def to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055

for path in sys.argv[1:]:
    data = open(path, "rb").read()
    magic, version, length = struct.unpack("<4sII", data[:12])
    clen, ctype = struct.unpack("<II", data[12:20])
    js = json.loads(data[20:20 + clen])
    print("%s  (glTF %s, %d bytes)" % (path.split("/")[-1], js["asset"]["version"], len(data)))
    for m in js.get("materials", []):
        f = m["pbrMetallicRoughness"].get("baseColorFactor", [1, 1, 1, 1])
        hexs = "#%02X%02X%02X" % tuple(round(to_srgb(c) * 255) for c in f[:3])
        print("  material %-12s baseColorFactor (linear) = %s  -> sRGB %s | metallic %s roughness %s"
              % (m.get("name"), [round(c, 4) for c in f], hexs, m["pbrMetallicRoughness"].get("metallicFactor"), m["pbrMetallicRoughness"].get("roughnessFactor")))
