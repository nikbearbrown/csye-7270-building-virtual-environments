extends "res://rts_scene.gd"
# C14 (beat B26): two windows over a meadow that scrolls (a camera pan): WorldRoot holds the meadow and both windows and moves down 140 px and back.
#  left  13-ripple-ride:  the ripples use the window's own address, sin(UV.y * 25)        -> they travel with the window
#  right 09-ripple-still: the ripples use the screen address, sin(SCREEN_UV.y * 60)       -> they stay fixed to the screen
# Both are frozen (no TIME), so the only motion is the pan. Same ripple size in both (about 80 px per wave).
var pan_root: Node2D
var ride: ColorRect
var glued: ColorRect

func build() -> void:
	pan_root = Node2D.new()
	pan_root.name = "WorldRoot"
	add_child(pan_root)
	world = L.build_world(pan_root, canvas_size, 2)
	ride = L.rect(pct(0.08, 0.14), pct(0.30, 0.46), Color.WHITE, "RideWindow")
	ride.material = L.mat_file("13-ripple-ride.gdshader")
	pan_root.add_child(ride)
	frame_of(ride)
	glued = L.rect(pct(0.58, 0.14), pct(0.30, 0.46), Color.WHITE, "GluedWindow")
	glued.material = L.mat_file("09-ripple-still.gdshader")
	pan_root.add_child(glued)
	frame_of(glued)

func set_time(t: float) -> void:
	var u := u_of(t)
	pan_root.position.y = 140.0 * (ramp(u, 0.12, 0.52) - ramp(u, 0.60, 0.96))
