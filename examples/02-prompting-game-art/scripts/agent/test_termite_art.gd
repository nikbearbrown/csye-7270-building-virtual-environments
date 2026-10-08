extends SceneTree
## Headless checks for the termite soldier art import pipeline.
## Run: godot --headless --path godot --script res://tests/test_termite_art.gd

const COLLIDER_W: float = 20.0
const COLLIDER_H: float = 34.0

var checks: int = 0
var failures: int = 0

func _initialize() -> void:
	call_deferred("run")

func check(passed: bool, label: String) -> void:
	checks += 1
	print("%s  %s" % ["PASS" if passed else "FAIL", label])
	if not passed:
		failures += 1
		push_error("FAIL: " + label)

func run() -> void:
	# --- 1. Import parameters ---
	var import_text: String = FileAccess.get_file_as_string(
		"res://features/termite/termite_soldiers.png.import"
	)
	check(not import_text.is_empty(), "import file readable")
	check(import_text.contains("compress/mode=0"), "import: lossless (compress/mode=0)")
	check(import_text.contains("mipmaps/generate=false"), "import: no mipmaps")

	# --- 2. Texture size ---
	var tex := load("res://features/termite/termite_soldiers.png") as Texture2D
	check(tex != null, "strip texture loads as Texture2D")
	if tex != null:
		check(tex.get_width() == 144, "strip width == 144")
		check(tex.get_height() == 48, "strip height == 48")

	# --- 3. SpriteFrames: three animations, one 48×48 frame each ---
	var frames := load("res://features/termite/termite_frames.tres") as SpriteFrames
	check(frames != null, "SpriteFrames loads")
	if frames != null:
		for anim: String in ["black", "red", "yellow"]:
			check(frames.has_animation(anim), "animation '%s' exists" % anim)
			if frames.has_animation(anim):
				check(frames.get_frame_count(anim) == 1,
					"animation '%s' has exactly 1 frame" % anim)
				var frame_tex: Texture2D = frames.get_frame_texture(anim, 0)
				check(frame_tex is AtlasTexture,
					"animation '%s' frame is AtlasTexture" % anim)
				if frame_tex is AtlasTexture:
					var region: Rect2 = (frame_tex as AtlasTexture).region
					check(region.size == Vector2(48, 48),
						"animation '%s' region 48×48 (got %s)" % [anim, region.size])

	# --- 4. Scene structure ---
	var packed := load("res://features/termite/termite.tscn") as PackedScene
	check(packed != null, "termite.tscn loads as PackedScene")
	if packed == null:
		_finish()
		return

	var scene: Node = packed.instantiate()
	check(scene is Area2D, "scene root is Area2D")
	if not (scene is Area2D):
		scene.queue_free()
		_finish()
		return

	var area := scene as Area2D

	# 5. Sprite: exists and has NEAREST filter
	var sprite: Node = area.get_node_or_null("AnimatedSprite2D")
	check(sprite != null and sprite is AnimatedSprite2D,
		"AnimatedSprite2D child of Area2D exists")
	if sprite is AnimatedSprite2D:
		check((sprite as AnimatedSprite2D).texture_filter == CanvasItem.TEXTURE_FILTER_NEAREST,
			"sprite texture_filter == NEAREST")

	# 6. Collider: exists as sibling (child of Area2D, NOT of sprite), correct shape & size
	var collider: Node = area.get_node_or_null("CollisionShape2D")
	check(collider != null and collider is CollisionShape2D,
		"CollisionShape2D exists in scene")
	if collider is CollisionShape2D:
		check(collider.get_parent() == area,
			"CollisionShape2D parent is Area2D (not sprite)")
		var shape: Shape2D = (collider as CollisionShape2D).shape
		check(shape is RectangleShape2D, "collider shape is RectangleShape2D")
		if shape is RectangleShape2D:
			var sz: Vector2 = (shape as RectangleShape2D).size
			check(sz == Vector2(COLLIDER_W, COLLIDER_H),
				"collider size == Vector2(%s, %s) (got %s)" % [COLLIDER_W, COLLIDER_H, sz])

	# 7. Hazard layer bit (project layer 4 = bit 3 = value 8)
	check((area.collision_layer & 8) != 0, "Hazard layer bit (layer 4, value 8) is set")

	area.queue_free()
	_finish()

func _finish() -> void:
	print("\ntest_termite_art: %d/%d passed" % [checks - failures, checks])
	quit(1 if failures else 0)
