#!/usr/bin/env python3
"""derive_geometry.py — reproduces, from the real exported asset, every geometry number Act V part 2 shows.
Run:  python3 derive_geometry.py > derive_geometry.out.txt
Inputs (read-only): examples/03-blender-mcp-to-godot/checkpoint_post.glb, scripts/agent/build_checkpoint_post.py
No Godot needed: the physics-server counts in logs/verify*-independent.log are checked against plain geometry.
"""
import json, struct, sys, math
from pathlib import Path
EX = Path(__file__).resolve().parents[3].parent / "examples" / "03-blender-mcp-to-godot"   # .../csye-7270-building-virtual-environments/examples/03-...
glb = (EX / "checkpoint_post.glb").read_bytes()
magic, ver, length = struct.unpack("<III", glb[:12]); assert magic == 0x46546C67
off = 12; js = None; bin_ = None
while off < length:
    clen, ctype = struct.unpack("<II", glb[off:off+8]); chunk = glb[off+8:off+8+clen]; off += 8 + clen
    if ctype == 0x4E4F534A: js = json.loads(chunk)
    elif ctype == 0x004E4942: bin_ = chunk
def positions(mesh_name):
    m = next(m for m in js["meshes"] if m["name"] == mesh_name)
    acc = js["accessors"][m["primitives"][0]["attributes"]["POSITION"]]
    bv = js["bufferViews"][acc["bufferView"]]; o = bv.get("byteOffset", 0) + acc.get("byteOffset", 0)
    return [struct.unpack_from("<fff", bin_, o + 12 * i) for i in range(acc["count"])]
print("glb nodes:", [n["name"] for n in js["nodes"]])
col_name = next(n["mesh"] for n in js["nodes"] if "Collision" in n["name"] and "mesh" in n)
col = positions(js["meshes"][col_name]["name"])
uniq = sorted(set((round(x, 4), round(y, 4), round(z, 4)) for x, y, z in col))
print(f"collision mesh '{js['meshes'][col_name]['name']}': {len(col)} glTF vertices, {len(uniq)} unique (Godot axes: x, y up, z)")
for v in uniq: print("  vertex", v)
ys = sorted(set(v[1] for v in uniq)); print("distinct vertex heights (y, m):", ys)
top = [v for v in uniq if v[1] >= 1.55 - 0.01]
print("vertices at or above the pennant's lower edge (y >= 1.54), what the agent's check read:", top)
print("  max x among them =", max(v[0] for v in top), " -> pennant length inside = max(0, min(0.48, %.2f) - 0.08) = %.4f m" % (max(v[0] for v in top), max(0, min(0.48, max(v[0] for v in top)) - 0.08)))

# half-width of the tapered hull as a function of height: base slab to y = 0.1 at +-0.30, then a straight slope to +-0.08 at y = 1.8
def hw(y):
    if y <= 0.1: return 0.30
    return 0.30 - (0.30 - 0.08) * (y - 0.1) / (1.8 - 0.1)
print("\nhull half-width (x) by height:")
for y in (0.0, 0.1, 0.5, 0.9, 0.95, 1.0, 1.55, 1.7, 1.8): print(f"  y = {y:4.2f} m: +-{hw(y):.4f} m   beyond the pole's 0.08 m: {hw(y)-0.08:.4f} m")
print("invisible collision each side of the pole: at the middle of the taper (y = 0.95 m) = %.3f m; at half the post's height (y = 0.90 m) = %.4f m" % (hw(0.95) - 0.08, hw(0.90) - 0.08))
print("(the taper starts at y = 0.1, not 0.0: the base slab is a straight +-0.30 block)")

# the sampling grid of logs/verify*-independent.log
xs = [round(0.08 + 0.01 * i, 2) for i in range(41)]; ys_ = [round(1.55 + 0.01 * j, 2) for j in range(26)]
print(f"\nsample grid: {len(xs)} x-values (0.08..0.48) x {len(ys_)} y-values (1.55..1.80) = {len(xs)*len(ys_)} points (log says 1066)")
EPS = 1e-9
box_in = sum(1 for x in xs for y in ys_ if x < 0.30 - EPS)
box_on = sum(1 for x in xs for y in ys_ if abs(x - 0.30) < EPS)
print(f"BOX collider (x <= 0.30): points strictly inside = {box_in}  (log: 572); points exactly on the face x = 0.30: {box_on} (a surface hit is not 'inside'); furthest inside x = {max(x for x in xs if x < 0.30 - EPS)} (log: 0.29)")
hull_in = sum(1 for x in xs for y in ys_ if x < hw(y) - EPS)
hull_on = [(x, y) for x in xs for y in ys_ if abs(x - hw(y)) < 1e-7]
print(f"HULL collider: points strictly inside = {hull_in}  (log: 55); points on the surface: {hull_on}; furthest inside x = {max(x for x in xs for y in ys_ if x < hw(y)-EPS)} (log: 0.11)")
cols = {}
for x in xs:
    n = sum(1 for y in ys_ if x < hw(y) - EPS)
    if n: cols[x] = n
print("  inside points per x column:", cols, " total", sum(cols.values()))
print("  hull half-width at the pennant's lower edge y = 1.55: %.4f m; at its top y = 1.80: %.4f m" % (hw(1.55), hw(1.80)))
print("  sliver: pennant root x = 0.08, deepest sample inside x = 0.11 -> %.2f m = %d cm" % (0.11 - 0.08, round((0.11-0.08)*100)))
# floor / ray numbers from the logs
print("\nray geometry from logs/verify1-test_checkpoint_post.log: ray from y = -0.2; post base y = -4.0; post top = -4.0 + 1.8 = -2.2; ray start above post top = -0.2 - (-2.2) = %.1f m; hit y = -2.2" % (-0.2 + 2.2))
print("our ray (verify_post_independent.gd): from post origin + 0.5 m = y -3.5, post StaticBody3D excluded, to origin - 3 m; floor y -4.0; gap = -4.0 - (-4.0) = 0.0 m")
