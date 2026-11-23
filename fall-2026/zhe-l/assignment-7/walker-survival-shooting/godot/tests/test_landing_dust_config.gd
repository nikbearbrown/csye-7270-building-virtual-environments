# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed; it loads the effect scene itself
## A6 headless configuration test for Effect A (landing dust): loads effects/landing_dust.tscn and reads back every setting
## the CHANGE-BRIEF "Settings" tables name, from the loaded nodes and resources, against the brief's values.
## Run: ./scripts/run-test.sh test_landing_dust_config.gd 60
## What it can prove: the scene loads, the node types and layering are right, every property name exists on its class in this engine,
##           and every value (amounts, lifetimes, shapes, curves, ramps, materials, visibility_aabb, preprocess, local_coords) took effect.
## What it cannot prove: how the dust looks (headless mode draws no particles). Height, spread, colour and fade on screen need the frame strip.

# ============================================================
# Constants: the scene path and the brief's values, all from CHANGE-BRIEF "Effect A: landing dust"
# ============================================================
const EFFECT_SCENE := "res://effects/landing_dust.tscn"  # The effect scene under test
const EPS := 0.0001  # How close two floats must be to count as equal
const FLOOR_LIMIT := 0.30  # Scale against the character: including the quads, the dust stays within 0.30 m above the floor (mid-calf; brief revision 2026-11-11, applied when r1 was kept on 2026-11-12; was 0.10, ankle height)
const RING_FINAL_DIAMETER := 0.90  # Scale against the character: the ground wave's final outer diameter

# The Dust table
const DUST_AMOUNT := 24  # amount
const DUST_LIFETIME := 1.6  # lifetime, seconds
const DUST_LIFETIME_RANDOMNESS := 0.2  # lifetime_randomness (on the ParticleProcessMaterial)
const DUST_RING_RADIUS := 0.2  # emission_ring_radius
const DUST_RING_INNER_RADIUS := 0.05  # emission_ring_inner_radius
const DUST_SPREAD := 180.0  # spread, degrees
const DUST_FLATNESS := 1.0  # flatness
const DUST_VELOCITY := Vector2(0.6, 0.9)  # initial_velocity_min / max, m/s
const DUST_DAMPING := Vector2(1.4, 1.8)  # damping_min / max
const DUST_ANGLE := Vector2(0.0, 360.0)  # angle_min / max, degrees
const DUST_SCALE := Vector2(0.8, 1.2)  # scale_min / max
const DUST_SCALE_CURVE := Vector2(0.6, 1.0)  # scale_curve: 0.6 at birth -> 1.0 at death
const DUST_COLOR := Color(0.48, 0.45, 0.40)  # color
# color_ramp opacity keys in seconds -> opacity; the ramp is read over each particle's life, so we divide the seconds by the lifetime
const DUST_OPACITY_KEYS := [[0.0, 0.0], [0.15, 0.6], [0.8, 0.15], [1.6, 0.0]]
const DUST_QUAD := Vector2(0.32, 0.32)  # draw_pass_1 QuadMesh size, metres (Step 4 r1: 0.08 -> 0.32, for cloud puffs)
const DUST_HEIGHT := 0.04  # The emitter sits 0.04 m above the landing point
const DUST_AABB := AABB(Vector3(-0.6, -0.1, -0.6), Vector3(1.2, 0.3, 1.2))  # visibility_aabb

# The GroundRing table
const RING_AMOUNT := 1  # amount
const RING_LIFETIME := 0.45  # lifetime, seconds
const RING_GROWN_SECONDS := 0.30  # scale_curve reaches 1.0 at 0.30 s, then stays at 1.0
const RING_SCALE_START := 0.2  # scale_curve at 0 s
const RING_COLOR := Color(0.62, 0.59, 0.53)  # color
const RING_OPACITY_START := 0.35  # opacity 0.35 -> 0, falling linearly the whole time
const RING_QUAD := Vector2(0.9, 0.9)  # draw_pass_1 QuadMesh size, metres
const RING_HEIGHT := 0.01  # 0.01 m above the landing point, so it does not z-fight with the floor
const RING_AABB := AABB(Vector3(-0.5, -0.05, -0.5), Vector3(1.0, 0.1, 1.0))  # visibility_aabb

# Every property name this test reads, by class: checked against this engine's ClassDB before any value is read
const PROPERTY_NAMES := {
	"GPUParticles3D": ["emitting", "amount", "lifetime", "one_shot", "explosiveness", "preprocess", "local_coords",
		"visibility_aabb", "process_material", "draw_pass_1", "cast_shadow"],
	"ParticleProcessMaterial": ["lifetime_randomness", "emission_shape", "emission_ring_axis", "emission_ring_radius",
		"emission_ring_inner_radius", "emission_ring_height", "direction", "spread", "flatness", "initial_velocity_min",
		"initial_velocity_max", "damping_min", "damping_max", "gravity", "angle_min", "angle_max", "scale_min", "scale_max",
		"scale_curve", "color", "color_ramp"],
	"QuadMesh": ["size", "orientation", "material"],
	"StandardMaterial3D": ["shading_mode", "transparency", "vertex_color_use_as_albedo", "billboard_mode",
		"billboard_keep_scale", "albedo_texture"],
	"GradientTexture2D": ["gradient", "fill", "fill_from", "fill_to"],
}

var _failures := 0  # How many checks have failed so far; _init() turns it into the exit code at the end
var _passes := 0  # How many checks have passed so far; printed in the summary line


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (the entry points)
# ============================================================
## Called by Godot once, when run with --script and the scene tree is created.
## We check the property names first, then load the scene and read back the root, both emitters, and the brief's derived limits; then we print the summary and quit.
func _init() -> void:
	_check_property_names()  # First we make sure every name we are about to read exists in this engine, so a wrong name shows up as a FAIL and not as a silent null
	var packed := load(EFFECT_SCENE) as PackedScene  # Then we load the effect scene from disk, the same file the game will instance
	if not _check("%s loads as a PackedScene" % EFFECT_SCENE, packed != null):  # If it does not load, there is nothing to read back
		_finish()  # So we print the summary and stop here
		return
	var root := packed.instantiate()  # We build the scene's nodes in memory; they are not added to the tree, so nothing runs or emits
	_check_root(root)  # We check the layering: one Node3D root with Dust and GroundRing under it
	var dust := root.get_node_or_null("Dust") as GPUParticles3D  # The dust emitter; null if the node is missing or of another type
	var ring := root.get_node_or_null("GroundRing") as GPUParticles3D  # The ground-wave emitter; null if missing or of another type
	if dust != null:  # If the dust emitter is there, we read back its whole table
		_check_dust(dust)
	if ring != null:  # If the ground-wave emitter is there, we read back its whole table
		_check_ring(ring)
	if dust != null and ring != null:  # If both are there, we also check the brief's scale limits worked out from the two tables together
		_check_derived(dust, ring)
	_report_initial_velocity()  # We print, without judging, whether ClassDB still lists the old single initial_velocity name (brief "Unconfirmed")
	root.free()  # The nodes were never in the tree, so we free them by hand before quitting
	_finish()  # Finally we print the summary and quit with the exit code


# ============================================================
# Feature functions: the checks, called by _init()
# ============================================================
## Called by _init() first. For each class, we look up every property name this test reads in this engine's ClassDB.
## A missing name is a FAIL with the name printed, instead of us guessing a replacement.
func _check_property_names() -> void:
	for cls_name in PROPERTY_NAMES:  # We go through the classes one by one
		var known := {}  # The names this engine really has on this class, including inherited ones; filled just below
		for prop in ClassDB.class_get_property_list(cls_name):  # ClassDB gives us every property of the class and its parents
			known[prop.name] = true  # We remember each name so the lookup below is a plain dictionary check
		for prop_name in PROPERTY_NAMES[cls_name]:  # Then for every name we read on this class
			_check("ClassDB: %s.%s exists" % [cls_name, prop_name], known.has(prop_name))  # If the engine does not have it, this line says which one


## Called by _init() after loading. Checks the layering rule: a Node3D root with exactly the two emitters Dust and GroundRing under it, in that order.
func _check_root(root: Node) -> void:
	_check("root is a Node3D (got %s)" % root.get_class(), root.get_class() == "Node3D")  # The root must be a plain Node3D, so the effect can be placed in the world
	var names: Array[String] = []  # The children's names in scene order; compared with the brief's layering below
	for child in root.get_children():  # We go through the root's children
		names.append(child.name)  # And note each name
	_check("root children are [Dust, GroundRing] (got %s)" % [names], names == ["Dust", "GroundRing"])  # Exactly two emitters, dust first, ring second
	for child in root.get_children():  # Then for each child
		_check("%s is a GPUParticles3D (got %s)" % [child.name, child.get_class()], child.get_class() == "GPUParticles3D")  # Both must be GPU emitters, as the brief chose


## Called by _init(). Reads back the Dust table: node settings, process material, draw mesh and draw material.
func _check_dust(dust: GPUParticles3D) -> void:
	_check_emitter_node(dust, DUST_AMOUNT, DUST_LIFETIME, DUST_HEIGHT, DUST_AABB)  # First the settings that live on the node itself
	var pm := dust.process_material as ParticleProcessMaterial  # Then the process material, where movement and change over life are set
	if not _check("Dust process_material is a ParticleProcessMaterial", pm != null):  # If it is missing or of another type, we cannot read the rest
		return
	_near("Dust lifetime_randomness", pm.lifetime_randomness, DUST_LIFETIME_RANDOMNESS)  # Each particle's life is cut by up to 20% at random
	_check("Dust emission_shape is RING (got %d)" % pm.emission_shape, pm.emission_shape == ParticleProcessMaterial.EMISSION_SHAPE_RING)  # Spawn on a flat ring around the feet
	_vec("Dust emission_ring_axis", pm.emission_ring_axis, Vector3(0, 1, 0))  # The ring's axis points up, so the ring lies flat on the floor
	_near("Dust emission_ring_radius", pm.emission_ring_radius, DUST_RING_RADIUS)  # Outer radius of the spawn ring
	_near("Dust emission_ring_inner_radius", pm.emission_ring_inner_radius, DUST_RING_INNER_RADIUS)  # Inner radius: no dust spawns right under the feet
	_near("Dust emission_ring_height", pm.emission_ring_height, 0.0)  # Height 0: every speck spawns at the same height
	_vec("Dust direction", pm.direction, Vector3(1, 0, 0))  # Base direction along X; the spread below turns it all the way round
	_near("Dust spread", pm.spread, DUST_SPREAD)  # 180 degrees: every horizontal direction is possible
	_near("Dust flatness", pm.flatness, DUST_FLATNESS)  # Flatness 1: the spread stays in the floor plane, so the dust does not rise
	_near("Dust initial_velocity_min", pm.initial_velocity_min, DUST_VELOCITY.x)  # Slowest outward speed
	_near("Dust initial_velocity_max", pm.initial_velocity_max, DUST_VELOCITY.y)  # Fastest outward speed
	_near("Dust damping_min", pm.damping_min, DUST_DAMPING.x)  # The damping pair slows the dust so it stops at about 0.9 m across
	_near("Dust damping_max", pm.damping_max, DUST_DAMPING.y)
	_vec("Dust gravity", pm.gravity, Vector3.ZERO)  # No gravity: the default (0, -9.8, 0) would pull the dust into the floor
	_near("Dust angle_min", pm.angle_min, DUST_ANGLE.x)  # Random starting rotation, from 0 ...
	_near("Dust angle_max", pm.angle_max, DUST_ANGLE.y)  # ... to a full turn
	_near("Dust scale_min", pm.scale_min, DUST_SCALE.x)  # Random size, from 0.8 ...
	_near("Dust scale_max", pm.scale_max, DUST_SCALE.y)  # ... to 1.2 times the quad
	var curve := _curve_of(pm.scale_curve, "Dust scale_curve")  # The size-over-life curve; null if it is not a CurveTexture with a Curve
	if curve != null:  # If it is there, we sample it at birth, at mid-life and at death
		_near("Dust scale_curve at life 0", curve.sample(0.0), DUST_SCALE_CURVE.x)  # Each quad is born at 0.6 ...
		_near("Dust scale_curve at life 0.5", curve.sample(0.5), lerpf(DUST_SCALE_CURVE.x, DUST_SCALE_CURVE.y, 0.5))  # ... grows evenly (0.8 halfway) ...
		_near("Dust scale_curve at life 1", curve.sample(1.0), DUST_SCALE_CURVE.y)  # ... and reaches 1.0 at the end
	_color("Dust color", pm.color, DUST_COLOR)  # The fixed grey-brown; the ramp below only changes opacity
	var ramp := _ramp_of(pm.color_ramp, "Dust color_ramp")  # The opacity-over-life ramp; null if it is not a GradientTexture1D with a Gradient
	if ramp != null:  # If it is there, we read it at each of the brief's keys
		for key in DUST_OPACITY_KEYS:  # Each key is [seconds, opacity]
			var life: float = key[0] / DUST_LIFETIME  # We turn the brief's seconds into a fraction of life, which is how the ramp is read
			var c := ramp.sample(life)  # The ramp's colour at that point of life
			_near("Dust opacity at %.2f s (life %.4f)" % [key[0], life], c.a, key[1])  # Its alpha must be the brief's opacity
			_color("Dust ramp rgb at %.2f s stays white" % key[0], Color(c.r, c.g, c.b), Color.WHITE)  # Its colour stays white, so the hue stays the dust colour
	var mesh := _quad_of(dust, "Dust")  # The draw mesh; null if it is not a QuadMesh
	if mesh != null:  # If it is there, we check its size and its material
		_vec2("Dust QuadMesh size", mesh.size, DUST_QUAD)  # 32 cm quads
		var mat := _material_of(mesh, "Dust")  # The draw material on the quad; null if it is not a StandardMaterial3D
		if mat != null:  # If it is there, we check the switches the brief names
			_check_draw_switches(mat, "Dust", BaseMaterial3D.BILLBOARD_PARTICLES)  # Unshaded, alpha, vertex colour, billboard PARTICLES
			# Not in the brief: without keep_scale, BILLBOARD_PARTICLES drops the particle's scale, so scale_min/max and scale_curve would show no effect
			_check("Dust billboard_keep_scale is on (added, not in the brief)", mat.billboard_keep_scale)
			_check_round_texture(mat.albedo_texture, "Dust")  # A round, soft-edged dot


## Called by _init(). Reads back the GroundRing table: node settings, process material, draw mesh and draw material.
func _check_ring(ring: GPUParticles3D) -> void:
	_check_emitter_node(ring, RING_AMOUNT, RING_LIFETIME, RING_HEIGHT, RING_AABB)  # First the settings that live on the node itself
	var pm := ring.process_material as ParticleProcessMaterial  # Then the process material
	if not _check("GroundRing process_material is a ParticleProcessMaterial", pm != null):  # If it is missing, we cannot read the rest
		return
	_near("GroundRing lifetime_randomness", pm.lifetime_randomness, 0.0)  # No randomness: the landing cue is the same every time
	_near("GroundRing initial_velocity_min", pm.initial_velocity_min, 0.0)  # The ring does not move; it only grows
	_near("GroundRing initial_velocity_max", pm.initial_velocity_max, 0.0)
	_vec("GroundRing gravity", pm.gravity, Vector3.ZERO)  # No gravity, so it stays on the floor
	_check("GroundRing scale_min/max stay 1 (fixed size)", is_equal_approx(pm.scale_min, 1.0) and is_equal_approx(pm.scale_max, 1.0))  # The size comes only from the curve, never at random
	var grown := RING_GROWN_SECONDS / RING_LIFETIME  # The brief's 0.30 s as a fraction of the 0.45 s life (0.667), where the curve reaches 1.0
	var curve := _curve_of(pm.scale_curve, "GroundRing scale_curve")  # The growth curve
	if curve != null:  # If it is there, we sample it at the brief's points
		_near("GroundRing scale_curve at 0 s", curve.sample(0.0), RING_SCALE_START)  # It starts as a small ring, 0.2 of its final size
		_near("GroundRing scale_curve at 0.15 s", curve.sample(0.15 / RING_LIFETIME), lerpf(RING_SCALE_START, 1.0, 0.15 / RING_GROWN_SECONDS))  # It grows evenly (0.6 halfway to 0.30 s)
		_near("GroundRing scale_curve at 0.30 s", curve.sample(grown), 1.0)  # It reaches its final size at 0.30 s
		_near("GroundRing scale_curve at 0.40 s", curve.sample(0.40 / RING_LIFETIME), 1.0)  # And then stays at 1.0 ...
		_near("GroundRing scale_curve at 0.45 s", curve.sample(1.0), 1.0)  # ... until it is gone
	_color("GroundRing color", pm.color, RING_COLOR)  # The lighter grey-brown
	var ramp := _ramp_of(pm.color_ramp, "GroundRing color_ramp")  # The opacity ramp
	if ramp != null:  # If it is there, we read it at the start, the middle and the end
		_near("GroundRing opacity at 0 s", ramp.sample(0.0).a, RING_OPACITY_START)  # It starts at 0.35
		_near("GroundRing opacity at mid-life", ramp.sample(0.5).a, RING_OPACITY_START * 0.5)  # Halfway it is half, so it falls in a straight line
		_near("GroundRing opacity at 0.45 s", ramp.sample(1.0).a, 0.0)  # And it is gone at the end of its life
		_color("GroundRing ramp rgb stays white", Color(ramp.sample(0.5).r, ramp.sample(0.5).g, ramp.sample(0.5).b), Color.WHITE)  # Only opacity changes, not the colour
	var mesh := _quad_of(ring, "GroundRing")  # The draw mesh
	if mesh != null:  # If it is there, we check its size, orientation and material
		_vec2("GroundRing QuadMesh size", mesh.size, RING_QUAD)  # 0.9 m square
		_check("GroundRing QuadMesh orientation is FACE_Y (got %d)" % mesh.orientation, mesh.orientation == PlaneMesh.FACE_Y)  # Lying flat on the floor
		var mat := _material_of(mesh, "GroundRing")  # The draw material
		if mat != null:  # If it is there, we check the switches and the ring texture
			_check_draw_switches(mat, "GroundRing", BaseMaterial3D.BILLBOARD_DISABLED)  # Unshaded, alpha, vertex colour, billboard off
			_check_ring_texture(mat.albedo_texture)  # Transparent centre, one thin bright band near the outer edge


## Called by _check_dust() and _check_ring(). Reads back the settings both tables put on the GPUParticles3D node itself.
func _check_emitter_node(p: GPUParticles3D, amount: int, lifetime: float, height: float, aabb: AABB) -> void:
	_check("%s amount = %d (got %d)" % [p.name, amount, p.amount], p.amount == amount)  # Particle count of one burst
	_near("%s lifetime" % p.name, p.lifetime, lifetime)  # Seconds each particle lives
	_check("%s one_shot is on" % p.name, p.one_shot)  # One burst per trigger, not a stream
	_near("%s explosiveness" % p.name, p.explosiveness, 1.0)  # Every particle is born on the same frame
	_check("%s emitting is off in the scene file" % p.name, not p.emitting)  # It must not fire on scene load; only restart() at a landing starts it
	_near("%s preprocess" % p.name, p.preprocess, 0.0)  # A landing effect does not run in advance
	_check("%s local_coords is off" % p.name, not p.local_coords)  # The dust stays at the landing point when the player walks off
	_check("%s visibility_aabb = %s (got %s)" % [p.name, aabb, p.visibility_aabb], p.visibility_aabb.is_equal_approx(aabb))  # Set by hand to the brief's box
	_check("%s cast_shadow is OFF" % p.name, p.cast_shadow == GeometryInstance3D.SHADOW_CASTING_SETTING_OFF)  # The node casts no shadow
	_vec("%s position" % p.name, p.position, Vector3(0, height, 0))  # Its height above the landing point (the root sits on the landing point)


## Called by _check_dust() and _check_ring(). Checks the draw-material switches both tables name; only the billboard mode differs.
func _check_draw_switches(mat: StandardMaterial3D, label: String, billboard: int) -> void:
	_check("%s shading_mode is UNSHADED" % label, mat.shading_mode == BaseMaterial3D.SHADING_MODE_UNSHADED)  # Lighting does not change the dust colour
	_check("%s transparency is ALPHA" % label, mat.transparency == BaseMaterial3D.TRANSPARENCY_ALPHA)  # Without this the opacity ramp would not fade anything
	_check("%s vertex_color_use_as_albedo is on" % label, mat.vertex_color_use_as_albedo)  # Without this the particle colour and ramp would not reach the quad
	_check("%s blend_mode is MIX" % label, mat.blend_mode == BaseMaterial3D.BLEND_MODE_MIX)  # Ordinary blending; ADD is Effect B's feature, not A's
	_check("%s billboard_mode = %d (got %d)" % [label, billboard, mat.billboard_mode], mat.billboard_mode == billboard)  # PARTICLES for the dust, off for the ring


## Called by _check_dust(). Checks the dust's albedo_texture is a radial GradientTexture2D that is solid in the middle and clear at the edge.
func _check_round_texture(tex: Texture2D, label: String) -> void:
	var g := tex as GradientTexture2D  # We need it as a GradientTexture2D to read its fill and gradient
	if not _check("%s albedo_texture is a GradientTexture2D" % label, g != null and g.gradient != null):  # If not, there is no dot to check
		return
	_check("%s texture fill is RADIAL" % label, g.fill == GradientTexture2D.FILL_RADIAL)  # Radial: the gradient runs from the centre outward, so the dot is round
	_vec2("%s texture fill_from (centre)" % label, g.fill_from, Vector2(0.5, 0.5))  # The gradient starts in the middle of the quad
	_near("%s texture radius reaches the edge" % label, g.fill_from.distance_to(g.fill_to), 0.5)  # And ends at the quad's edge, so the dot fills the quad
	_near("%s texture alpha at centre" % label, g.gradient.sample(0.0).a, 1.0)  # Solid in the middle ...
	_near("%s texture alpha at edge" % label, g.gradient.sample(1.0).a, 0.0)  # ... clear at the edge, so there are no square corners
	_check("%s texture edge is soft (alpha at half radius is between)" % label, g.gradient.sample(0.5).a > 0.1 and g.gradient.sample(0.5).a < 0.9)  # A soft fade, not a hard disc


## Called by _check_ring(). Checks the ring's albedo_texture: radial, clear in the centre, one bright band near the outer edge, clear beyond it.
func _check_ring_texture(tex: Texture2D) -> void:
	var g := tex as GradientTexture2D  # We need it as a GradientTexture2D to read its fill and gradient
	if not _check("GroundRing albedo_texture is a GradientTexture2D", g != null and g.gradient != null):  # If not, there is no ring to check
		return
	_check("GroundRing texture fill is RADIAL", g.fill == GradientTexture2D.FILL_RADIAL)  # Radial, so the band is a circle
	_vec2("GroundRing texture fill_from (centre)", g.fill_from, Vector2(0.5, 0.5))  # Centred on the quad
	_near("GroundRing texture radius reaches the edge", g.fill_from.distance_to(g.fill_to), 0.5)  # Offset 1 is the quad's edge, so the band's outer size is the quad's 0.9 m
	var peak := 0.0  # The brightest alpha along the radius; found just below
	var peak_at := 0.0  # Where along the radius (0 = centre, 1 = edge) that brightest alpha is
	var wide := 0  # How many of the 100 samples are more than half bright: the band's width in hundredths of the radius
	for i in 101:  # We walk from the centre to the edge in 100 steps
		var a := g.gradient.sample(i / 100.0).a  # The alpha at this point of the radius
		if a > peak:  # If it is brighter than anything so far, we remember it and where it is
			peak = a
			peak_at = i / 100.0
		if a > 0.5:  # If it is more than half bright, it is inside the band
			wide += 1
	_near("GroundRing texture alpha at centre", g.gradient.sample(0.0).a, 0.0)  # Transparent centre
	_check("GroundRing texture band is bright (peak %.2f)" % peak, peak > 0.9)  # One bright band ...
	_check("GroundRing texture band is near the outer edge (at %.2f of the radius)" % peak_at, peak_at >= 0.8 and peak_at < 1.0)  # ... near the outer edge ...
	_check("GroundRing texture band is thin (%d%% of the radius above half alpha)" % wide, wide > 0 and wide <= 20)  # ... and thin
	_near("GroundRing texture alpha at edge", g.gradient.sample(1.0).a, 0.0)  # Clear again at the edge, so the corners stay empty


## Called by _init() once both emitters are read. Checks the brief's "Scale against the character" limits worked out from both tables together.
func _check_derived(dust: GPUParticles3D, ring: GPUParticles3D) -> void:
	var pm := dust.process_material as ParticleProcessMaterial  # The dust's process material, for its largest scale
	var mesh := dust.draw_pass_1 as QuadMesh  # The dust's quad, for its size
	if pm == null or mesh == null or not (pm.scale_curve is CurveTexture):  # If any part is missing, the checks above already failed; there is nothing to work out
		return
	var curve := (pm.scale_curve as CurveTexture).curve  # The size-over-life curve
	if curve == null:  # If the texture holds no curve, _curve_of() already failed it
		return
	var curve_max := 0.0  # The curve's largest value over life; found just below
	for i in 101:  # We walk through the whole life in 100 steps
		curve_max = maxf(curve_max, curve.sample(i / 100.0))  # And keep the largest size factor we meet (1.0 at death for this curve)
	# Top of the highest quad: emitter height + half of the largest quad (quad size x scale_max x the curve's largest value); flatness 1 means no speck rises above the emitter
	var top := dust.position.y + mesh.size.y * pm.scale_max * curve_max * 0.5
	_check("Dust top including quads = %.3f m <= %.2f m (mid-calf)" % [top, FLOOR_LIMIT], top <= FLOOR_LIMIT + EPS)  # The brief's 0.30 m limit; the quad top is an upper bound on the visible top edge
	var ring_pm := ring.process_material as ParticleProcessMaterial  # The ring's process material, for its final scale
	var ring_mesh := ring.draw_pass_1 as QuadMesh  # The ring's quad, for its size
	if ring_pm == null or ring_mesh == null or not (ring_pm.scale_curve is CurveTexture):  # If any part is missing, the checks above already failed
		return
	var final_diameter := ring_mesh.size.x * (ring_pm.scale_curve as CurveTexture).curve.sample(1.0)  # The ring quad's size times the curve's final value
	_near("GroundRing final outer diameter (m)", final_diameter, RING_FINAL_DIAMETER)  # The brief's 0.90 m, 1.5 times the capsule diameter


## Called by _init(). The brief's "Unconfirmed" list says 4.7.2's ClassDB still lists initial_velocity; we print what this engine says, without a PASS/FAIL.
func _report_initial_velocity() -> void:
	var names := {}  # Every property name on ParticleProcessMaterial in this engine
	for prop in ClassDB.class_get_property_list("ParticleProcessMaterial"):  # We collect them all
		names[prop.name] = prop  # And keep the full entry, so we can print its type and usage too
	if names.has("initial_velocity"):  # If the single name is still there, we print what it is so its reason can be looked into
		var p: Dictionary = names["initial_velocity"]
		print("  INFO  ParticleProcessMaterial lists initial_velocity: type %d, usage %d (the scene sets initial_velocity_min / max only)" % [p.type, p.usage])
	else:  # Otherwise we say it is gone in this engine
		print("  INFO  ParticleProcessMaterial does not list initial_velocity in this engine")


# ============================================================
# Helper functions: small readers and comparers used by the checks above
# ============================================================
## Called by the dust and ring checks. Returns the Curve inside a CurveTexture, or null (with a FAIL) if it is not one.
func _curve_of(tex: Texture2D, label: String) -> Curve:
	var ct := tex as CurveTexture  # scale_curve must be a CurveTexture holding a Curve
	_check("%s is a CurveTexture with a Curve" % label, ct != null and ct.curve != null)  # If not, we say so here
	return ct.curve if ct != null else null  # The caller samples this curve over life


## Called by the dust and ring checks. Returns the Gradient inside a GradientTexture1D, or null (with a FAIL) if it is not one.
func _ramp_of(tex: Texture2D, label: String) -> Gradient:
	var gt := tex as GradientTexture1D  # color_ramp must be a GradientTexture1D holding a Gradient
	_check("%s is a GradientTexture1D with a Gradient" % label, gt != null and gt.gradient != null)  # If not, we say so here
	return gt.gradient if gt != null else null  # The caller samples this gradient over life


## Called by the dust and ring checks. Returns the emitter's draw_pass_1 as a QuadMesh, or null (with a FAIL) if it is not one.
func _quad_of(p: GPUParticles3D, label: String) -> QuadMesh:
	var q := p.draw_pass_1 as QuadMesh  # Each particle is drawn as this quad
	_check("%s draw_pass_1 is a QuadMesh (got %s)" % [label, p.draw_pass_1.get_class() if p.draw_pass_1 else "null"], q != null)  # If not, we say what it is instead
	return q  # The caller reads its size and material


## Called by the dust and ring checks. Returns the quad's material as a StandardMaterial3D, or null (with a FAIL) if it is not one.
func _material_of(mesh: QuadMesh, label: String) -> StandardMaterial3D:
	var m := mesh.material as StandardMaterial3D  # The draw material sits on the quad mesh
	_check("%s draw material is a StandardMaterial3D" % label, m != null)  # If not, we say so here
	return m  # The caller reads its switches and texture


## Prints one PASS / FAIL line and counts it; returns ok, so callers can stop early when a resource is missing.
func _check(label: String, ok: bool) -> bool:
	print(("  PASS  " if ok else "  FAIL  ") + label)  # One line per check, the same form as the other tests
	if ok:  # If it passed, we add it to the passes
		_passes += 1
	else:  # Otherwise we add it to the failures; _finish() turns them into the exit code
		_failures += 1
	return ok


## Compares two floats within EPS and prints the expected and actual values.
func _near(label: String, got: float, want: float) -> void:
	_check("%s = %s (got %s)" % [label, want, got], absf(got - want) <= EPS)


## Compares two Vector3s within EPS per axis.
func _vec(label: String, got: Vector3, want: Vector3) -> void:
	_check("%s = %s (got %s)" % [label, want, got], absf(got.x - want.x) <= EPS and absf(got.y - want.y) <= EPS and absf(got.z - want.z) <= EPS)


## Compares two Vector2s within EPS per axis.
func _vec2(label: String, got: Vector2, want: Vector2) -> void:
	_check("%s = %s (got %s)" % [label, want, got], absf(got.x - want.x) <= EPS and absf(got.y - want.y) <= EPS)


## Compares the RGB of two colours within EPS (alpha is checked separately where the brief names it).
func _color(label: String, got: Color, want: Color) -> void:
	var ok := absf(got.r - want.r) <= EPS and absf(got.g - want.g) <= EPS and absf(got.b - want.b) <= EPS  # Each channel must match
	_check("%s = (%.2f, %.2f, %.2f) (got (%.4f, %.4f, %.4f))" % [label, want.r, want.g, want.b, got.r, got.g, got.b], ok)


## Called by _init() at the end. Prints the summary line and quits; the exit code is 1 when any check failed.
func _finish() -> void:
	print("== %d passed, %d failed ==" % [_passes, _failures])  # The real counts, so a failure is never reported as "all pass"
	quit(1 if _failures > 0 else 0)  # run-test.sh passes this exit code on
