extends Node
## Presentation only: maps Player.invulnerable to the hurt-tint shader's `intensity` every frame
## (CHANGE-BRIEF section 2, driver mapping). Reads Player state, never writes it; never sets `tint_color`.
## Default process mode, so it pauses with the level and the value holds while paused (R7).

@onready var player: Player = get_parent()
@onready var material: ShaderMaterial = player.get_node("Sprite2D").material


func _process(_delta: float) -> void:
	var t := 0.0
	# fail() freezes `invulnerable` without clearing it, so failing and cleared both force 0.0 (R8, F4).
	if player.invulnerable > 0.0 and not player.is_failing and not player.is_cleared:
		t = player.invulnerable / Tuning.INVULNERABLE_TIME
	material.set_shader_parameter("intensity", t)
