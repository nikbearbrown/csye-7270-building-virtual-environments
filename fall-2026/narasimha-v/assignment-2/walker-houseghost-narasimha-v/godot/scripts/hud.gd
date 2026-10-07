extends CanvasLayer
## Everything the player needs to understand the slice with the sound off:
## how many days are left, how close to being seen they are, how cold the house
## is getting, and whether audio is muted.

@onready var _days: Label = $Days
@onready var _recognition: Label = $Recognition
@onready var _frost: ColorRect = $Frost
@onready var _mutes: Label = $Mutes
@onready var _banner: Label = $Banner
@onready var _hint: Label = $Hint
@onready var _opening: Label = $Opening


func _ready() -> void:
	_banner.visible = false
	_opening.visible = false
	_frost.color = Color(0.78, 0.86, 0.92, 0.0)


func set_days(days_left: int, total: int) -> void:
	_days.text = "%d NIGHTS LEFT" % days_left
	# A visible tear: the label jolts when a day is lost, so the cost reads muted.
	var tween := create_tween()
	_days.scale = Vector2(1.12, 1.12)
	tween.tween_property(_days, "scale", Vector2.ONE, 0.35).set_trans(Tween.TRANS_BACK)


func set_recognition(recognition: int, needed: int) -> void:
	var filled := "".rpad(0)
	for i in needed:
		filled += "●  " if i < recognition else "○  "
	_recognition.text = "THINGS OF HIS, FOUND   " + filled


func set_frost(level: float) -> void:
	var tween := create_tween()
	tween.tween_property(_frost, "color:a", clampf(level, 0.0, 1.0) * 0.38, 0.8)


func set_mutes(music_muted: bool, sfx_muted: bool) -> void:
	var parts := []
	if music_muted:
		parts.append("MUSIC MUTED (M)")
	if sfx_muted:
		parts.append("SFX MUTED (N)")
	_mutes.text = "   ".join(parts)


## One beat of the counter per heartbeat, so the sound and the number are
## visibly the same thing: the night running out.
func pulse_days() -> void:
	var tween := create_tween()
	_days.modulate = Color(1.0, 0.72, 0.62, 1.0)
	_days.scale = Vector2(1.06, 1.06)
	tween.set_parallel(true)
	tween.tween_property(_days, "modulate", Color(0.86, 0.88, 0.9, 0.92), 0.45)
	tween.tween_property(_days, "scale", Vector2.ONE, 0.45)


## The opening: three lines over the house as it really is, shown once.
func show_opening(lines: Array) -> void:
	_opening.visible = true
	_opening.modulate.a = 0.0
	for i in lines.size():
		_opening.text = "\n".join(lines.slice(0, i + 1))
		var t := create_tween()
		t.tween_property(_opening, "modulate:a", 1.0, 0.9)
		await t.finished
		await _opening.get_tree().create_timer(1.1).timeout
	var out := create_tween()
	out.tween_property(_opening, "modulate:a", 0.0, 1.2)
	await out.finished
	_opening.visible = false


func set_hint(text: String) -> void:
	_hint.text = text


func show_banner(text: String) -> void:
	_banner.text = text
	_banner.visible = true
	_banner.modulate.a = 0.0
	var tween := create_tween()
	tween.tween_property(_banner, "modulate:a", 1.0, 0.9)
