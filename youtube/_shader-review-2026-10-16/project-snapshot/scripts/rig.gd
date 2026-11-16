class_name Rig
extends RefCounted
# The test rig shared by the stage scene and the verification scripts: one camera, a sphere and a torus.
# Everything is in WORLD units; the camera looks down -Z from +Z, Y is up (the same as Maya, so no axis flip was needed in the conversion).

const CAM_POS := Vector3(0.0, 0.0, 5.5)
const FOV_DEG := 30.0                       # vertical field of view (Godot's default keep-aspect is KEEP_HEIGHT)
const SPHERE_POS := Vector3(-1.3, 0.0, 0.0)
const SPHERE_RADIUS := 1.0
const TORUS_POS := Vector3(1.3, 0.0, 0.0)
const CLEAR := Color("#D9D5CA")             # warm light grey, the series Lab's stage colour
const LIGHT_TRAVEL := Vector3(0.5, -0.8, -0.6)   # the shaders' default light_direction (the direction the light travels)

static func build(parent: Node3D, with_torus := true) -> Dictionary:
	var cam := Camera3D.new()
	cam.fov = FOV_DEG
	cam.position = CAM_POS
	parent.add_child(cam)
	cam.current = true
	var sphere := MeshInstance3D.new()
	var sm := SphereMesh.new()
	sm.radius = SPHERE_RADIUS
	sm.height = 2.0 * SPHERE_RADIUS
	sm.radial_segments = 128
	sm.rings = 64
	sphere.mesh = sm
	sphere.position = SPHERE_POS
	parent.add_child(sphere)
	var torus: MeshInstance3D = null
	if with_torus:
		torus = MeshInstance3D.new()
		var tm := TorusMesh.new()
		tm.inner_radius = 0.45
		tm.outer_radius = 1.0
		tm.rings = 96
		tm.ring_segments = 48
		torus.mesh = tm
		torus.position = TORUS_POS
		torus.rotation_degrees = Vector3(60.0, 0.0, 0.0)   # tilt the ring toward the camera so the hole shows
		parent.add_child(torus)
	return {"camera": cam, "sphere": sphere, "torus": torus}

# Exact ray / sphere hit for the CENTRE of integer pixel (px, py): returns {} on a miss, else {pos, normal, e (unit, toward camera), dist}
static func hit_sphere(cam: Camera3D, px: int, py: int, center := SPHERE_POS, radius := SPHERE_RADIUS) -> Dictionary:
	var o := cam.project_ray_origin(Vector2(px + 0.5, py + 0.5))
	var d := cam.project_ray_normal(Vector2(px + 0.5, py + 0.5))
	var oc := o - center
	var b := oc.dot(d)
	var c := oc.dot(oc) - radius * radius
	var disc := b * b - c
	if disc < 0.0:
		return {}
	var t := -b - sqrt(disc)
	var p := o + d * t
	return {"pos": p, "normal": (p - center) / radius, "e": (cam.global_position - p).normalized(), "dist": t}

# the pixel (float) a point of the world lands on
static func project(cam: Camera3D, world_pos: Vector3) -> Vector2:
	return cam.unproject_position(world_pos)

# sRGB transfer functions (what Godot applies when it writes linear light to an 8-bit screen)
static func lin_to_srgb(x: float) -> float:
	return 12.92 * x if x <= 0.0031308 else 1.055 * pow(x, 1.0 / 2.4) - 0.055

static func srgb_to_lin(x: float) -> float:
	return x / 12.92 if x <= 0.04045 else pow((x + 0.055) / 1.055, 2.4)

static func enc(c: Color) -> Color:   # linear Color -> what the 8-bit screen holds, as 0..1 floats
	return Color(lin_to_srgb(clampf(c.r, 0, 1)), lin_to_srgb(clampf(c.g, 0, 1)), lin_to_srgb(clampf(c.b, 0, 1)), 1.0)
