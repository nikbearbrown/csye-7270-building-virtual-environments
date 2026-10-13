# make_showcase_tscn.py - writes project_src/showcase.tscn: a floor, ONE light, a camera, and the three assets side by side.
# Plain text scene; the transforms are computed here (look-at camera, tilted sun) so the numbers are not guesses.
import math, os

def norm(v):
    l = math.sqrt(sum(c * c for c in v)); return tuple(c / l for c in v)
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

def look_at(pos, target, up=(0, 1, 0)):
    z = norm(tuple(p - t for p, t in zip(pos, target)))     # camera / light looks down its own -Z
    x = norm(cross(up, z))
    y = cross(z, x)
    return x, y, z

def transform(x, y, z, o):
    # Godot text format: the 3x3 basis row by row (columns are the x, y, z axes), then the origin
    return "Transform3D(%s)" % ", ".join("%.6f" % v for v in (x[0], y[0], z[0], x[1], y[1], z[1], x[2], y[2], z[2], o[0], o[1], o[2]))

target = (-0.12, 0.22, 0.0)
az, el, dist = math.radians(12), math.radians(20), 3.7
cam_pos = (target[0] + dist * math.cos(el) * math.sin(az), target[1] + dist * math.sin(el), target[2] + dist * math.cos(el) * math.cos(az))
cx, cy, cz = look_at(cam_pos, target)
# one sun, from above-left-front: shining toward (+0.45, -0.75, -0.5)
sun_dir = norm((0.45, -0.75, -0.5))
sx, sy, sz = look_at((0, 0, 0), sun_dir)                    # its -Z axis points along sun_dir
sz_back = tuple(-c for c in sun_dir)
sx, sy, sz = look_at(tuple(-c for c in sun_dir), (0, 0, 0))

placed = [("Crate", "crate", -0.65), ("Lantern", "lantern", 0.05), ("Coin", "coin", 0.50)]
lines = ['[gd_scene load_steps=%d format=3]' % (5 + len(placed)), '']
for i, (_, f, _) in enumerate(placed, 1):
    lines.append('[ext_resource type="PackedScene" path="res://assets/%s.glb" id="%d"]' % (f, i))
lines += ['',
          '[sub_resource type="PlaneMesh" id="PlaneMesh_floor"]', 'size = Vector2(8, 5)', '',
          '[sub_resource type="StandardMaterial3D" id="Mat_floor"]', 'albedo_color = Color(0.36, 0.38, 0.34, 1)', '',
          '[sub_resource type="Environment" id="Env_camera"]', 'background_mode = 1', 'background_color = Color(0.93, 0.92, 0.89, 1)',
          'ambient_light_source = 2', 'ambient_light_color = Color(0.82, 0.84, 0.9, 1)', 'ambient_light_energy = 0.55', '',
          '[node name="Showcase" type="Node3D"]', '',
          '[node name="Floor" type="MeshInstance3D" parent="."]', 'mesh = SubResource("PlaneMesh_floor")', 'surface_material_override/0 = SubResource("Mat_floor")', '',
          '[node name="Sun" type="DirectionalLight3D" parent="."]', 'transform = ' + transform(sx, sy, sz, (0, 3, 0)), 'light_energy = 1.4', 'shadow_enabled = true', '',
          '[node name="Camera" type="Camera3D" parent="."]', 'transform = ' + transform(cx, cy, cz, cam_pos), 'environment = SubResource("Env_camera")', 'current = true', 'fov = 32.0', '']
for i, (name, f, x) in enumerate(placed, 1):
    lines += ['[node name="%s" parent="." instance=ExtResource("%d")]' % (name, i), 'transform = ' + transform((1, 0, 0), (0, 1, 0), (0, 0, 1), (x, 0, 0)), '']
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "project_src", "showcase.tscn"), "w") as fh:
    fh.write("\n".join(lines))
print("camera at (%.3f, %.3f, %.3f) looking at %s; sun direction %s" % (*cam_pos, target, tuple(round(c, 3) for c in sun_dir)))
