extends "res://rts_scene.gd"
# C13 (beat B25): a window (14-blur: filter_linear_mipmap, textureLod) over the meadow. The `blur` level sweeps from 0 to exactly 4.0 between u = 0.58
# and 0.84 and is held, so the readout "level 4" (u = 0.88) is the uniform's real value. THIS CAPTURE USES THE NATIVE ROUTE (a 1920 x 1080 SubViewport at
# scale 1, the scene built for a 1920 x 1080 canvas): a mip level counts texels of the screen texture, so on the 3840 x 2160 route the same level is
# less than half as blurred (verify10 A).
var w: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	w = win(0.20, 0.14, 0.56, 0.56, "14-blur.gdshader", "FrostedWindow")

func set_time(t: float) -> void:
	uni(w, "blur", 4.0 * ramp(u_of(t), 0.58, 0.84))
