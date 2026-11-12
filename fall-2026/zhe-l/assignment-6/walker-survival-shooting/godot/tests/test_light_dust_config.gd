# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed; it loads the effect scene itself
## A6 headless configuration test for Effect B (dust under the ceiling light): loads effects/light_dust.tscn and reads back every setting
## the CHANGE-BRIEF "Effect B" settings table names, from the loaded node and resources, against the brief's values.
## Run: ./scripts/run-test.sh test_light_dust_config.gd 60
## What it can prove: the scene loads, the node type and layering are right, every property name exists on its class in this engine,
##           and every value (amount, lifetime, box, turbulence, ramp, ADD material, visibility_aabb, preprocess, local_coords) took effect.
## What it cannot prove: how the dust looks (headless mode draws no particles), whether preprocess fills the box on the first visible frame,
##           or whether a pause freezes the specks. Those need the frame strip.

# ============================================================
# Constants: the scene path and the brief's values, all from CHANGE-BRIEF "Effect B: dust under the ceiling light"
# ============================================================
const EFFECT_SCENE := "res://effects/light_dust.tscn"  # The effect scene under test
const EPS := 0.0001  # How close two floats must be to count as equal

const AMOUNT := 3000  # amount; also the brief's peak particle count (redesign 2026-11-12: the whole room)
const LIFETIME := 6.0  # lifetime, seconds
const LIFETIME_RANDOMNESS := 0.5  # lifetime_randomness (on the ParticleProcessMaterial)
const BOX_EXTENTS := Vector3(7.0, 1.3, 4.5)  # emission_box_extents: half sizes, so the full box is 14 x 2.6 x 9 m (the whole room)
const BOX_FULL_SIZE := Vector3(14.0, 2.6, 9.0)  # The intent's full box size, checked against the extents
const BOX_OFFSET := Vector3(0.0, 0.15, 3.2)  # emission_shape_offset: moves the box from the node at (0, 1.45, -3.2) to the room centre (0, 1.6, 0)
const SPREAD := 180.0  # spread, degrees: "direction random"
const VELOCITY := Vector2(0.01, 0.04)  # initial_velocity_min / max, m/s
const TURBULENCE_STRENGTH := 1.0  # turbulence_noise_strength
const TURBULENCE_SCALE := 4.0  # turbulence_noise_scale
const TURBULENCE_INFLUENCE := Vector2(0.02, 0.06)  # turbulence_influence_min / max
const SCALE := Vector2(0.1, 1.0)  # scale_min / max
const COLOR := Color(0.78, 0.86, 1.0)  # color: the fixed cool white
# color_ramp opacity keys as a fraction of life -> opacity: several rises and falls, so each speck twinkles
const OPACITY_KEYS := [[0.0, 0.0], [0.10, 0.6], [0.25, 0.15], [0.40, 0.9], [0.55, 0.2], [0.70, 0.7], [0.85, 0.1], [1.0, 0.0]]
const QUAD := Vector2(0.03, 0.03)  # draw_pass_1 QuadMesh size, metres
const SPECK_SIZE := Vector2(0.003, 0.03)  # Scale against the character: each speck's quad is 0.003-0.03 m across
const AABB_BOX := AABB(Vector3(-7.3, -1.45, -1.6), Vector3(14.6, 3.2, 9.6))  # visibility_aabb: the offset box plus 0.3 m on every side
const PREPROCESS := 6.0  # preprocess, seconds

# Every property name this test reads, by class: checked against this engine's ClassDB before any value is read
const PROPERTY_NAMES := {
	"GPUParticles3D": ["emitting", "amount", "lifetime", "one_shot", "explosiveness", "preprocess", "local_coords",
		"visibility_aabb", "process_material", "draw_pass_1", "cast_shadow"],
	"ParticleProcessMaterial": ["lifetime_randomness", "emission_shape", "emission_box_extents", "direction", "spread", "flatness",
		"initial_velocity_min", "initial_velocity_max", "gravity", "turbulence_enabled", "turbulence_noise_strength",
		"turbulence_noise_scale", "turbulence_influence_min", "turbulence_influence_max", "scale_min", "scale_max",
		"color", "color_ramp", "emission_shape_offset"],
	"QuadMesh": ["size", "material"],
	"StandardMaterial3D": ["shading_mode", "transparency", "blend_mode", "vertex_color_use_as_albedo", "billboard_mode",
		"billboard_keep_scale", "albedo_texture"],
	"GradientTexture2D": ["gradient", "fill", "fill_from", "fill_to"],
}

var _failures := 0  # How many checks have failed so far; _init() turns it into the exit code at the end
var _passes := 0  # How many checks have passed so far; printed in the summary line


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (the entry points)
# ============================================================
## Called by Godot once, when run with --script and the scene tree is created.
## We check the property names first, then load the scene and read back the emitter, its process material and its draw pass; then we print the summary and quit.
func _init() -> void:
	_check_property_names()  # First we make sure every name we are about to read exists in this engine, so a wrong name shows up as a FAIL and not as a silent null
	var packed := load(EFFECT_SCENE) as PackedScene  # Then we load the effect scene from disk, the same file the game will instance
	if not _check("%s loads as a PackedScene" % EFFECT_SCENE, packed != null):  # If it does not load, there is nothing to read back
		_finish()  # So we print the summary and stop here
		return
	var root := packed.instantiate()  # We build the scene's nodes in memory; they are not added to the tree, so nothing runs or emits
	var dust := _check_root(root)  # We check the layering: one GPUParticles3D and nothing under it; null if the root is another type
	if dust != null:  # If the emitter is there, we read back the whole table
		_check_node(dust)
		_check_process(dust)
		_check_draw(dust)
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


## Called by _init() after loading. Checks the layering rule: one emitter, because there is only one thing here (dust). Returns it, or null.
func _check_root(root: Node) -> GPUParticles3D:
	_check("root is a GPUParticles3D (got %s)" % root.get_class(), root.get_class() == "GPUParticles3D")  # The brief's node type; only GPU nodes have turbulence
	_check("root has no children (got %d)" % root.get_child_count(), root.get_child_count() == 0)  # One emitter, no extra layers
	return root as GPUParticles3D  # The caller reads the table from it


## Called by _init(). Reads back the settings the table puts on the GPUParticles3D node itself.
func _check_node(p: GPUParticles3D) -> void:
	_check("amount = %d (got %d)" % [AMOUNT, p.amount], p.amount == AMOUNT)  # 90 specks, which is also the peak count
	_near("lifetime", p.lifetime, LIFETIME)  # Each speck lives up to 6 s
	_check("one_shot is off", not p.one_shot)  # A steady stream while the light is on, not a burst
	_near("explosiveness", p.explosiveness, 0.0)  # Births spread evenly over the lifetime, so the box never empties and refills at once
	_near("preprocess", p.preprocess, PREPROCESS)  # 6 s run in advance, so the first visible frame already shows a steady distribution
	_check("local_coords is off", not p.local_coords)  # The dust belongs to the room and follows nothing
	_check("visibility_aabb = %s (got %s)" % [AABB_BOX, p.visibility_aabb], p.visibility_aabb.is_equal_approx(AABB_BOX))  # Set by hand to the brief's box
	_check("cast_shadow is OFF", p.cast_shadow == GeometryInstance3D.SHADOW_CASTING_SETTING_OFF)  # The node casts no shadow
	# Not in the brief: the light state decides when it runs, so the scene file starts it off and the listener starts it (restart()) when the lights are on
	_check("emitting is off in the scene file (added, not in the brief)", not p.emitting)
	var emission_box := AABB(BOX_OFFSET - BOX_EXTENTS, BOX_EXTENTS * 2.0)  # The emission box in the emitter's own space, moved by the shape offset
	_check("visibility_aabb encloses the emission box", p.visibility_aabb.encloses(emission_box))  # One size larger, because turbulence carries specks out of the box


## Called by _init(). Reads back the process material: spawn box, motion, turbulence, size, colour and the twinkling opacity ramp.
func _check_process(p: GPUParticles3D) -> void:
	var pm := p.process_material as ParticleProcessMaterial  # Movement and change over life are set here
	if not _check("process_material is a ParticleProcessMaterial", pm != null):  # If it is missing or of another type, we cannot read the rest
		return
	_near("lifetime_randomness", pm.lifetime_randomness, LIFETIME_RANDOMNESS)  # Lives cut by up to half at random, so the specks twinkle out of step
	_check("emission_shape is BOX (got %d)" % pm.emission_shape, pm.emission_shape == ParticleProcessMaterial.EMISSION_SHAPE_BOX)  # Spawn anywhere inside a box
	_vec("emission_box_extents", pm.emission_box_extents, BOX_EXTENTS)  # Half sizes of the box ...
	_vec("emission box full size", pm.emission_box_extents * 2.0, BOX_FULL_SIZE)  # ... so the full box is the intent's 14 x 2.6 x 9 m
	_vec("emission_shape_offset", pm.emission_shape_offset, BOX_OFFSET)  # The box is centred on the room, not on the node
	_near("spread", pm.spread, SPREAD)  # 180 degrees: any direction from the base direction, so the direction is random
	# Not in the brief by name: flatness 0 keeps the spread a full sphere (1 would flatten it into a plane)
	_near("flatness (added, not in the brief)", pm.flatness, 0.0)
	_near("initial_velocity_min", pm.initial_velocity_min, VELOCITY.x)  # Slowest drift
	_near("initial_velocity_max", pm.initial_velocity_max, VELOCITY.y)  # Fastest drift
	_vec("gravity", pm.gravity, Vector3.ZERO)  # No gravity: the default (0, -9.8, 0) would drop the dust to the floor
	_check("turbulence_enabled is on", pm.turbulence_enabled)  # The wandering path; a feature Effect A does not use
	_near("turbulence_noise_strength", pm.turbulence_noise_strength, TURBULENCE_STRENGTH)
	_near("turbulence_noise_scale", pm.turbulence_noise_scale, TURBULENCE_SCALE)
	_near("turbulence_influence_min", pm.turbulence_influence_min, TURBULENCE_INFLUENCE.x)  # Light turbulence: it only nudges each speck ...
	_near("turbulence_influence_max", pm.turbulence_influence_max, TURBULENCE_INFLUENCE.y)  # ... between 2% and 6%
	_near("scale_min", pm.scale_min, SCALE.x)  # Random size, from half ...
	_near("scale_max", pm.scale_max, SCALE.y)  # ... to the full quad
	_color("color", pm.color, COLOR)  # The fixed cool white; the ramp below only changes opacity
	var gt := pm.color_ramp as GradientTexture1D  # The opacity-over-life ramp must be a GradientTexture1D holding a Gradient
	if not _check("color_ramp is a GradientTexture1D with a Gradient", gt != null and gt.gradient != null):  # If not, there is no ramp to read
		return
	for key in OPACITY_KEYS:  # Each key is [fraction of life, opacity]
		var c := gt.gradient.sample(key[0])  # The ramp's colour at that point of life
		_near("opacity at life %.2f" % key[0], c.a, key[1])  # Its alpha must be the brief's opacity
		_color("ramp rgb at life %.2f stays white" % key[0], Color(c.r, c.g, c.b), Color.WHITE)  # Its colour stays white, so the hue stays the dust colour


## Called by _init(). Reads back the draw pass: the quad, its ADD material and the round soft texture.
func _check_draw(p: GPUParticles3D) -> void:
	var mesh := p.draw_pass_1 as QuadMesh  # Each speck is drawn as this quad
	if not _check("draw_pass_1 is a QuadMesh (got %s)" % [p.draw_pass_1.get_class() if p.draw_pass_1 else "null"], mesh != null):  # If not, we say what it is instead
		return
	_vec2("QuadMesh size", mesh.size, QUAD)  # 30 mm quads
	var pm := p.process_material as ParticleProcessMaterial  # For the scale pair, to work out the smallest and largest speck
	if pm != null:  # If it is there, we check the brief's speck size against the character
		_near("smallest speck (quad x scale_min, m)", mesh.size.x * pm.scale_min, SPECK_SIZE.x)  # 3 mm, about 1/533 of the character's 1.6 m
		_near("largest speck (quad x scale_max, m)", mesh.size.x * pm.scale_max, SPECK_SIZE.y)  # 30 mm, about 1/53
	var mat := mesh.material as StandardMaterial3D  # The draw material sits on the quad mesh
	if not _check("draw material is a StandardMaterial3D", mat != null):  # If not, there are no switches to read
		return
	_check("shading_mode is PER_PIXEL (lit)", mat.shading_mode == BaseMaterial3D.SHADING_MODE_PER_PIXEL)  # Lit by the ceiling lights (redesign 2026-11-12): bright near a light, faint far from it
	_check("blend_mode is ADD", mat.blend_mode == BaseMaterial3D.BLEND_MODE_ADD)  # Additive: each speck adds light to what is behind it; a feature Effect A does not use
	_check("transparency is ALPHA", mat.transparency == BaseMaterial3D.TRANSPARENCY_ALPHA)  # Without this the opacity ramp would not fade anything
	_check("vertex_color_use_as_albedo is on", mat.vertex_color_use_as_albedo)  # Without this the particle colour and ramp would not reach the quad
	_check("billboard_mode is PARTICLES (got %d)" % mat.billboard_mode, mat.billboard_mode == BaseMaterial3D.BILLBOARD_PARTICLES)  # Each speck faces the camera
	# Not in the brief: without keep_scale, BILLBOARD_PARTICLES drops the particle's scale, so scale_min/max would show no effect (same as Effect A)
	_check("billboard_keep_scale is on (added, not in the brief)", mat.billboard_keep_scale)
	var g := mat.albedo_texture as GradientTexture2D  # The round soft-edged dot
	if not _check("albedo_texture is a GradientTexture2D", g != null and g.gradient != null):  # If not, there is no dot to check
		return
	_check("texture fill is RADIAL", g.fill == GradientTexture2D.FILL_RADIAL)  # Radial: the gradient runs from the centre outward, so the dot is round
	_vec2("texture fill_from (centre)", g.fill_from, Vector2(0.5, 0.5))  # The gradient starts in the middle of the quad
	_near("texture radius reaches the edge", g.fill_from.distance_to(g.fill_to), 0.5)  # And ends at the quad's edge, so the dot fills the quad
	_near("texture alpha at centre", g.gradient.sample(0.0).a, 1.0)  # Solid in the middle ...
	_near("texture alpha at edge", g.gradient.sample(1.0).a, 0.0)  # ... clear at the edge, so there are no square corners
	_check("texture edge is soft (alpha at half radius is between)", g.gradient.sample(0.5).a > 0.1 and g.gradient.sample(0.5).a < 0.9)  # A soft fade, not a hard disc


# ============================================================
# Helper functions: small comparers used by the checks above
# ============================================================
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
