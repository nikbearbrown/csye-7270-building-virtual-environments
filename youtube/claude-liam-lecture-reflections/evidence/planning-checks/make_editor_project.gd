extends SceneTree
# make_editor_project.gd: builds a SCRATCH Godot project that holds the pond as a real scene file (pond.tscn), so the editor frames
# E1 (Scene dock) and E2 (Inspector of the BackBufferCopy) can be captured from Godot's own editor. It never touches any other project.
# Use make-editor-project.sh, which runs the two modes in order:
#   mode "assets"  writes project.godot, label-map.png, ground.png, character.png and 02-reflection.gdshader into the output dir
#   (then the shell runs `godot --headless --path <output dir> --import` so the PNGs are imported)
#   mode "scene"   (run with --path <output dir>) builds pond.tscn from those files, so the scene references them as external resources
#
# Tree (the order every beat uses):
#   Pond (Node2D)
#     LabelMap (Sprite2D)        label-map.png  (flat red water, flat green coast)
#     BackBufferCopy             Copy Mode = Viewport
#     Ground (Sprite2D)          ground.png (opaque art)
#     Player (Sprite2D)          character.png at (300, 278)
#       RemoteTransform2D        Remote Path = ../../Reflection, position (0, 144)
#     Reflection (Sprite2D)      character.png, Flip V, ShaderMaterial = 02-reflection.gdshader
const P = preload("res://pond_common.gd")
const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"

func _initialize() -> void:
	call_deferred("run")

func write_assets(out: String) -> void:
	DirAccess.make_dir_recursive_absolute(out)
	var layers := P.make_layers(1)
	(layers["mask"] as Image).save_png(out + "/label-map.png")
	(layers["ground"] as Image).save_png(out + "/ground.png")
	P.make_character_image().save_png(out + "/character.png")
	var f := FileAccess.open(out + "/02-reflection.gdshader", FileAccess.WRITE)
	f.store_string(FileAccess.get_file_as_string(SHADERS + "02-reflection.gdshader"))
	f.close()
	var pj := FileAccess.open(out + "/project.godot", FileAccess.WRITE)
	pj.store_string("config_version=5\n\n[application]\n\nconfig/name=\"Pond\"\nrun/main_scene=\"res://pond.tscn\"\nconfig/features=PackedStringArray(\"4.7\")\n\n[display]\n\nwindow/size/viewport_width=1280\nwindow/size/viewport_height=720\n")
	pj.close()
	print("RESULT " + JSON.stringify({"mode": "assets", "dir": out}))

func write_scene(out: String) -> void:
	var mask_tex: Texture2D = load("res://label-map.png")
	var ground_tex: Texture2D = load("res://ground.png")
	var char_tex: Texture2D = load("res://character.png")
	var sh: Shader = load("res://02-reflection.gdshader")
	var rootn := Node2D.new()
	rootn.name = "Pond"
	var mask := Sprite2D.new()
	mask.name = "LabelMap"
	mask.texture = mask_tex
	mask.centered = false
	var bbc := BackBufferCopy.new()
	bbc.name = "BackBufferCopy"
	bbc.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	var ground := Sprite2D.new()
	ground.name = "Ground"
	ground.texture = ground_tex
	ground.centered = false
	var player := Sprite2D.new()
	player.name = "Player"
	player.texture = char_tex
	player.position = Vector2(300, P.PLAYER_Y)
	var rt := RemoteTransform2D.new()
	rt.name = "RemoteTransform2D"
	rt.position = Vector2(0, P.REFLECT_OFFSET)
	var refl := Sprite2D.new()
	refl.name = "Reflection"
	refl.texture = char_tex
	refl.flip_v = true
	var mat := ShaderMaterial.new()
	mat.shader = sh
	refl.material = mat
	for n in [mask, bbc, ground, player, refl]:
		rootn.add_child(n)
	player.add_child(rt)
	for n in [mask, bbc, ground, player, refl, rt]:
		n.owner = rootn
	rt.remote_path = rt.get_path_to(refl)
	var ps := PackedScene.new()
	var err := ps.pack(rootn)
	var err2 := ResourceSaver.save(ps, out + "/pond.tscn")
	print("RESULT " + JSON.stringify({"mode": "scene", "pack_error": err, "save_error": err2, "remote_path": str(rt.remote_path)}))

func run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() < 2:
		print("usage: -- <output dir> assets|scene")
		quit(2)
		return
	if args[1] == "assets":
		write_assets(String(args[0]))
	else:
		write_scene(String(args[0]))
	quit(0)
