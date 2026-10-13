extends Node2D
# rts_scene.gd: base class of every capture scene of "Reading the Screen".
#
# A scene is a PURE FUNCTION OF TIME. The capture harness (or scene_runner.gd) sets `duration` (the measured length of the beat, in seconds)
# and `canvas_size` (1280 x 720), adds the scene to a viewport, then calls set_time(t) once per frame and lets one frame render.
# All keyframes are written as fractions u = t / duration, so the same scene fits any beat length.
# Free-running (auto = true, the default) the scene plays itself in real time, for a quick look.
# TIME-driven shaders (ripples, the pool) run on the engine's clock, so they only repeat exactly under a fixed tick rate (--fixed-fps 30).
const L = preload("res://rts_lib.gd")

var canvas_size := Vector2(1280, 720)
var duration := 8.0
var auto := true
var clock := 0.0
var world: Node2D
var frame_layer: CanvasLayer       # picture frames live on a high layer so no screen reader ever copies them
var framed: Array = []             # [window, frame] pairs, kept in step with the windows every frame

func _ready() -> void:
	build()
	set_time(0.0)

func build() -> void:
	pass

func set_time(_t: float) -> void:
	pass

func _process(_delta: float) -> void:
	_sync_frames()

func _physics_process(delta: float) -> void:
	if auto:
		clock += delta
		set_time(clock)

# ---- helpers shared by the scenes ----
func pct(fx: float, fy: float) -> Vector2:
	return Vector2(fx * canvas_size.x, fy * canvas_size.y)

func u_of(t: float) -> float:
	return clampf(t / maxf(duration, 0.001), 0.0, 1.0)

static func ramp(u: float, u0: float, u1: float) -> float:
	# 0 before u0, 1 after u1, smooth in between
	var k := clampf((u - u0) / maxf(u1 - u0, 0.0001), 0.0, 1.0)
	return k * k * (3.0 - 2.0 * k)

static func lin(u: float, u0: float, u1: float) -> float:
	return clampf((u - u0) / maxf(u1 - u0, 0.0001), 0.0, 1.0)

func add_filter_layer(shader: String, layer_index: int = 1) -> ColorRect:
	# a full-screen ColorRect on its own CanvasLayer, with the given shader; returns the ColorRect
	var layer := CanvasLayer.new()
	layer.name = "Layer"
	layer.layer = layer_index
	add_child(layer)
	var f := ColorRect.new()
	f.name = "Filter"
	layer.add_child(f)
	f.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	f.mouse_filter = Control.MOUSE_FILTER_IGNORE
	f.material = L.mat_file(shader)
	return f

func win(fx: float, fy: float, fw: float, fh: float, shader: String, name: String = "Window", with_frame: bool = true) -> ColorRect:
	var r := L.rect(pct(fx, fy), pct(fw, fh), Color.WHITE, name)
	if shader != "":
		r.material = L.mat_file(shader)
	add_child(r)
	if with_frame:
		frame_of(r)
	return r

func frame_of(window: Control, color: Color = L.CREAM, width: float = -1.0) -> void:
	# Draws a picture frame round a window ON A HIGH CANVAS LAYER (index 50), so the frame is never part of any copy of the screen.
	# The default width is 6 px on a 1280 px canvas and scales with the canvas (the native 1920 x 1080 route gets 9 px).
	if width < 0.0:
		width = 6.0 * canvas_size.x / 1280.0
	if frame_layer == null:
		frame_layer = CanvasLayer.new()
		frame_layer.name = "FrameLayer"
		frame_layer.layer = 50
		add_child(frame_layer)
	var fr := ReferenceRect.new()
	fr.name = "Frame_" + window.name
	fr.editor_only = false
	fr.border_color = color
	fr.border_width = width
	fr.mouse_filter = Control.MOUSE_FILTER_IGNORE
	frame_layer.add_child(fr)
	framed.append([window, fr])
	_sync_frames()

func _sync_frames() -> void:
	for pair in framed:
		var w: Control = pair[0]
		var fr: ReferenceRect = pair[1]
		fr.global_position = w.global_position
		fr.size = w.size
		fr.visible = w.is_visible_in_tree()

func uni(node: CanvasItem, name: String, value: Variant) -> void:
	(node.material as ShaderMaterial).set_shader_parameter(name, value)
