class_name Common
# Helpers shared by the SubViewports planning checks. Every check prints one "RESULT {json}" line per measurement.

const FILM_SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/lab-shaders/"
const STAGE := Color("#D9D5CA")        # the Lab's stage colour
const CLEAR := Color("#A8A090")        # default clear colour used where the picture's box must be visible
const TEAL := Color("#5FA391")

static func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

static func rgba(c: Color) -> Array:
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001), snappedf(c.a, 0.001)]

static func rgb(c: Color) -> Array:
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

static func diff(a: Color, b: Color) -> float:
	return maxf(absf(a.r - b.r), maxf(absf(a.g - b.g), absf(a.b - b.b)))

static func shader_text(file: String) -> String:
	return FileAccess.get_file_as_string(FILM_SHADERS + file)

static func material_from_file(file: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = shader_text(file)
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

static func material_from_code(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

# a rectangle that writes the shader built-in TIME into its colour: TIME = red + green * 255 (red = fract(TIME), green = floor(TIME) / 255).
const TIME_PROBE_CODE := "shader_type canvas_item;\nvoid fragment() { COLOR = vec4(fract(TIME), floor(TIME) / 255.0, 0.0, 1.0); }\n"

static func time_of(img: Image, x: int = 5, y: int = 5) -> float:
	var c := img.get_pixel(x, y)
	return c.r + floorf(c.g * 255.0 + 0.5)
