extends SceneTree
# The loop shown on screen in B04, exactly as shown (Image.create_empty, the 4.7 name; Image.create is the deprecated one).
# Run 3 times: godot --headless --path <scratch project> --script verify-b04-create-empty.gd
func _init():
	var t0 := Time.get_ticks_usec()
	var big := Image.create_empty(1920, 1080, false, Image.FORMAT_RGBA8)
	for y in range(1080):
		for x in range(1920):
			big.set_pixel(x, y, Color(x / 1919.0, 0.0, 0.0))
	var ms := (Time.get_ticks_usec() - t0) / 1000.0
	print("B04 LOOP create_empty: %.1f ms; pixel (1919,0) r=%.4f; size=%s" % [ms, big.get_pixel(1919, 0).r, big.get_size()])
	quit()
