extends "res://tests/test_fire_shader.gd"

var capture_index := 0

func press(keycode: Key) -> void:
	await super.press(keycode)
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://evidence/a5/use-it/menu-input-%d.png" % capture_index)
	capture_index += 1

func run() -> void:
	game = GameManager.new()
	game.save_enabled = false
	game.fixed_map_seed = 1729
	root.add_child(game)
	await frames_n(4)
	await game.start_contract("city")
	p = game.player
	p.set_physics_process(false)
	p._sprite.set_process(false)
	SystemScreens.settings["auto_potion"] = ""
	obs = Observer.new()
	obs.game = game
	root.add_child(obs)
	await reset()
	await _pause_and_loot()
	var result := {"checks": checks, "failures": failures, "adapter": RenderingServer.get_video_adapter_name(), "renderer": RenderingServer.get_current_rendering_method(), "captures": capture_index}
	var file := FileAccess.open("res://evidence/a5/use-it/menu-input.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(result, "\t"))
	file.close()
	print("A5_RENDERED_MENU_RESULT ", JSON.stringify(result))
	quit(0 if failures == 0 else 1)
