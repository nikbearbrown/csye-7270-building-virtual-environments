extends "res://rts_scene.gd"
# C08 (beat B20): the finished spotlight (07-spotlight). The four lines of _process below are EXACTLY the code shown on screen:
# the game reads the screen size, takes the player's position ON THE SCREEN (the canvas transform includes the camera), divides it by the screen size and
# sends the result to the shader every frame. verify8.gd shows why not plain position: with a moved Camera2D the circle lands on the world position.
# Node names matter: the root has a child CanvasLayer "Layer" holding the ColorRect "Filter", and a Sprite2D "Player".
const CENTER := Vector2(0.50, 0.50)
const LAP := Vector2(0.20, 0.12)

func build() -> void:
	world = L.build_world(self, canvas_size)
	add_child(L.make_player(pct(CENTER.x, CENTER.y)))
	var f := add_filter_layer("07-spotlight.gdshader")
	uni(f, "radius", 0.25)

func set_time(t: float) -> void:
	var a := TAU * u_of(t) + PI
	$Player.position = pct(CENTER.x + LAP.x * cos(a), CENTER.y + LAP.y * sin(a))

func _process(_delta):
	var size := get_viewport_rect().size
	var on_screen: Vector2 = $Player.get_global_transform_with_canvas().origin
	$Layer/Filter.material.set_shader_parameter("player", on_screen / size)
