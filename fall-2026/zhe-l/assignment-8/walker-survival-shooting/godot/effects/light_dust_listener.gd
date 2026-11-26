extends GPUParticles3D

@export var ceiling_lights: CeilingLights

var restart_count := 0


func _ready() -> void:
	if ceiling_lights == null:
		return
	if not ceiling_lights.is_node_ready():
		await ceiling_lights.ready
	visibility_changed.connect(_on_visibility_changed)
	ceiling_lights.lights_changed.connect(_on_lights_changed)
	_on_lights_changed(ceiling_lights.is_lights_on())


func _on_lights_changed(lights_on: bool) -> void:
	if lights_on:
		if visible:
			_restart()
		else:
			visible = true
	else:
		visible = false
		emitting = false


func _on_visibility_changed() -> void:
	if not is_visible_in_tree():
		emitting = false
	elif ceiling_lights.is_lights_on():
		_restart()


func _restart() -> void:
	restart_count += 1
	restart()
