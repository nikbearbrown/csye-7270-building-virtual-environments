extends SceneTree
## A3-R3 evidence: renders the room from the start view, from behind and from
## below through the room's own orbit() method. Needs a window (not --headless):
## a headless run has no renderer and never reaches frame_post_draw.

const VIEWS := [
	["front", 0.0, 0.0],
	["behind", PI, 0.0],
	["below", 0.0, -1.2],
]

func _initialize() -> void:
	call_deferred("capture")

func capture() -> void:
	var room = load("res://a3/lantern_gate_room.tscn").instantiate()
	root.add_child(room)
	var out := ProjectSettings.globalize_path("res://../evidence/a3/orbit")
	DirAccess.make_dir_recursive_absolute(out)
	var start := Vector2(room.yaw, room.pitch)
	var failed := 0
	for view in VIEWS:
		room.yaw = start.x
		room.pitch = start.y
		room.orbit(view[1], view[2])
		for i in 6:
			await process_frame
		await RenderingServer.frame_post_draw
		var path: String = "%s/a3-room-%s.png" % [out, view[0]]
		var err := root.get_viewport().get_texture().get_image().save_png(path)
		failed += int(err != OK)
		print("A3_ORBIT view=%s camera=%s floor_mesh_visible=%s error=%d" % [view[0], room.camera.position, room.floor_mesh.visible, err])
	quit(1 if failed else 0)
