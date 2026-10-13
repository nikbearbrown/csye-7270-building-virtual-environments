extends "res://scene_c06_spot_oval.gd"
# C07 (beat B19): the same walk. The oval (06-spotlight-oval) becomes a circle at u = 0.72, when the shader is swapped for 07-spotlight
# (both addresses multiplied by width over height from SCREEN_PIXEL_SIZE). The radius uniform is carried over.
const SWAP := 0.72
var oval_mat: ShaderMaterial
var round_mat: ShaderMaterial

func build() -> void:
	super.build()
	oval_mat = filter_rect.material
	round_mat = L.mat_file("07-spotlight.gdshader")
	round_mat.set_shader_parameter("radius", 0.25)

func set_time(t: float) -> void:
	super.set_time(t)
	filter_rect.material = round_mat if u_of(t) >= SWAP else oval_mat
