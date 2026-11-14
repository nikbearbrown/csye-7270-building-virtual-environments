extends SceneTree
## Writes two depth variants of the A2 run contact pose (Assignment 7, run cycle), from mage_run_contact.png only
## (read, never written). In pixel art the far leg is drawn darker:
##   res://assets/sprites/mage/mage_run_contact_far_back.png   the trailing leg darkened (forward leg = near leg)
##   res://assets/sprites/mage/mage_run_contact_far_front.png  the forward leg darkened (trailing leg = near leg)
## Same silhouette and same pixels everywhere else. The legs are the opaque pixels of rows 51-66 minus the staff shaft
## (x >= 37 on rows 50-57), split into their two 4-connected parts: the one with the smaller mean x trails behind.
## Darkening moves a colour one step down its own ramp in the two A2 run images' palette (DARKER below); a colour at the
## bottom of its ramp (the tunic shade, the skin shade, the outline) has no darker fill tone and stays.
## From fall-2026/zhefan-z/assignment-7/, run once:
##   Godot_v4.7.2-stable_win64_console.exe --headless --path walker-magic-zhefan --script res://tools/make_contact_far_legs.gd
## Image.load_from_file prints an engine WARNING ("will not work on export"); it is expected here.
## Kept as evidence only (2026-11-12): both outputs were judged in captures/run/analysis/run_4pose_compare_8x.png, the
## alternation did not read (19 px differ, at the boot tips), and they were removed from assets/ unused.

const SRC := "res://assets/sprites/mage/mage_run_contact.png"
const OUT_FAR_BACK := "res://assets/sprites/mage/mage_run_contact_far_back.png"
const OUT_FAR_FRONT := "res://assets/sprites/mage/mage_run_contact_far_front.png"
const LEG_ROWS := Vector2i(51, 66)
const STAFF := Rect2i(37, 50, 62 - 37, 8)   # x 37-61, rows 50-57
## One step darker within each ramp of the palette (base -> shade), CHARACTER-SHEET colours.
const DARKER := {
	"6b5a4e": "4d3931",   # tunic / boots highlight -> tunic shade
	"f5dccd": "e0b8a6",   # skin -> skin shade
	"d4a63a": "995e11",   # gold -> gold shade
	"3a40a0": "261e8a",   # indigo -> indigo shade
	"e8e6f0": "9f9cad",   # hair -> hair shade
	"d62839": "9a0225",   # red -> red shade
}


func _initialize() -> void:
	var src := Image.load_from_file(ProjectSettings.globalize_path(SRC))
	src.convert(Image.FORMAT_RGBA8)
	var legs := _leg_parts(src)
	if legs.size() != 2:
		printerr("expected 2 leg parts, found %d" % legs.size())
		quit(1)
		return
	legs.sort_custom(func(a: Array, b: Array) -> bool: return _mean_x(a) < _mean_x(b))
	var trailing: Array = legs[0]
	var forward: Array = legs[1]
	var report := {"legs": {"trailing": _describe(src, trailing), "forward": _describe(src, forward)}}
	var ok := true
	for job: Array in [[OUT_FAR_BACK, trailing, "far_back"], [OUT_FAR_FRONT, forward, "far_front"]]:
		var img := src.duplicate() as Image
		var moved := {}
		for p: Vector2i in job[1]:
			var from := img.get_pixelv(p).to_html(false)
			if DARKER.has(from):
				img.set_pixelv(p, Color.html(DARKER[from]))
				moved["%s->%s" % [from, DARKER[from]]] = moved.get("%s->%s" % [from, DARKER[from]], 0) + 1
		var err := img.save_png(ProjectSettings.globalize_path(job[0]))
		var back := Image.load_from_file(ProjectSettings.globalize_path(job[0]))
		back.convert(Image.FORMAT_RGBA8)
		var changed := 0
		var outside := 0
		var in_leg := {}
		for p: Vector2i in job[1]:
			in_leg[p] = true
		for y in src.get_height():
			for x in src.get_width():
				if back.get_pixel(x, y) != src.get_pixel(x, y):
					changed += 1
					if not in_leg.has(Vector2i(x, y)):
						outside += 1
		report[job[2]] = {"file": job[0], "save": error_string(err), "pixels_changed": changed,
			"changed_outside_that_leg": outside, "moves": moved}
		ok = ok and err == OK and outside == 0
	print(JSON.stringify(report, " "))
	quit(0 if ok else 1)


## The leg pixels split into 4-connected parts.
func _leg_parts(img: Image) -> Array:
	var mask := {}
	for y in range(LEG_ROWS.x, LEG_ROWS.y + 1):
		for x in img.get_width():
			if img.get_pixel(x, y).a8 > 0 and not STAFF.has_point(Vector2i(x, y)):
				mask[Vector2i(x, y)] = true
	var parts := []
	var seen := {}
	for start: Vector2i in mask:
		if seen.has(start):
			continue
		var part := []
		var stack := [start]
		seen[start] = true
		while not stack.is_empty():
			var p: Vector2i = stack.pop_back()
			part.append(p)
			for d: Vector2i in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
				var q := p + d
				if mask.has(q) and not seen.has(q):
					seen[q] = true
					stack.append(q)
		parts.append(part)
	return parts


func _mean_x(part: Array) -> float:
	return part.reduce(func(s: float, p: Vector2i) -> float: return s + p.x, 0.0) / part.size()


func _describe(img: Image, part: Array) -> Dictionary:
	var xs := part.map(func(p: Vector2i) -> int: return p.x)
	var ys := part.map(func(p: Vector2i) -> int: return p.y)
	var colours := {}
	for p: Vector2i in part:
		var c := img.get_pixelv(p).to_html(false)
		colours[c] = colours.get(c, 0) + 1
	return {"pixels": part.size(), "x": [xs.min(), xs.max()], "rows": [ys.min(), ys.max()], "colours": colours}
