extends Node3D
# Stage scene for the editor and for a quick look: a sphere and a torus wearing one lesson shader.
# Left / Right arrow (or A / D) steps through the lessons; the label shows the file name. Nothing here is part of the lesson shaders.

@export_range(0, 15) var lesson := 2
var rig: Dictionary
var label: Label

func _ready() -> void:
	RenderingServer.set_default_clear_color(Rig.CLEAR)
	rig = Rig.build(self)
	var layer := CanvasLayer.new()
	add_child(layer)
	label = Label.new()
	label.position = Vector2(16, 12)
	layer.add_child(label)
	apply()

func apply() -> void:
	var mat := Lessons.material(lesson)
	rig["sphere"].material_override = mat
	rig["torus"].material_override = mat
	label.text = "%s   (Left / Right: change lesson)" % Lessons.NAMES[lesson]

func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_RIGHT or event.keycode == KEY_D:
			lesson = (lesson + 1) % Lessons.NAMES.size()
			apply()
		elif event.keycode == KEY_LEFT or event.keycode == KEY_A:
			lesson = (lesson + Lessons.NAMES.size() - 1) % Lessons.NAMES.size()
			apply()
