extends RefCounted
# The same two waves as wave() in the shader: the height of the water surface at ground point p (x and z) at clock t.

static func height(p: Vector2, t: float, wave_height: float, wave_length: float, wave_speed: float) -> float:
	var d1 := Vector2(1.0, 0.3).normalized()
	var d2 := Vector2(-0.4, 1.0).normalized()
	var k1 := TAU / wave_length
	var k2 := TAU / (0.6 * wave_length)
	var p1 := k1 * (d1.dot(p) - wave_speed * t)
	var p2 := k2 * (d2.dot(p) - 0.8 * wave_speed * t)
	return wave_height * (sin(p1) + 0.6 * sin(p2))
