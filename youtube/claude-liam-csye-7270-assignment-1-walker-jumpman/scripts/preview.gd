extends SceneTree
## Native vector inspection. Poses and diagnostic overlays, NOT a played route.
class ColliderOutline extends Node2D:
	var bounds: Rect2
	func _draw() -> void:
		draw_rect(bounds, Color("e35835"), false, 0.10)
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	root.size = Vector2i(3840,2160)
	root.content_scale_size = Vector2i(3840,2160)
	var view := SubViewport.new()
	view.size = Vector2i(3840,2160)
	view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(view)
	var bg := ColorRect.new()
	bg.color = Color("FAF9F5")
	bg.size = Vector2(3840,2160)
	view.add_child(bg)
	var figures: Array = []
	for i in range(2):
		var player = load("res://features/player/player.gd").new()
		view.add_child(player)
		player.position = Vector2(1100+i*1640, 1810)
		player.scale = Vector2(44,44)
		player.facing = 1.0 if i == 0 else -1.0
		player.enabled = false
		player.queue_redraw()
		figures.append(player)
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var err := view.get_texture().get_image().save_png(ProjectSettings.globalize_path("res://../media/player-art.png"))
	assert(err == OK)
	for player in figures:
		var collider: CollisionShape2D = player.get_child(0)
		var outline := ColliderOutline.new()
		outline.bounds = Rect2(collider.position-collider.shape.size/2,collider.shape.size)
		player.add_child(outline)
	await process_frame
	await RenderingServer.frame_post_draw
	err = view.get_texture().get_image().save_png(ProjectSettings.globalize_path("res://../media/player-collider.png"))
	print("Native 3840x2160 art + collision-node diagnostic preview; result=",err)
	quit(err)
