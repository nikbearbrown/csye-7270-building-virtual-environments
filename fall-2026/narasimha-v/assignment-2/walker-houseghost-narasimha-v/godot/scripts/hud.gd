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


func _ready() -> void:
	_banner.visible = false
	_frost.color = Color(0.78, 0.86, 0.92, 0.0)


func set_days(days_left: int, total: int) -> void:
	_days.text = "DAYS UNTIL THE ANNIVERSARY   %d / %d" % [days_left, total]
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


func set_hint(text: String) -> void:
	_hint.text = text


func show_banner(text: String) -> void:
	_banner.text = text
	_banner.visible = true
	_banner.modulate.a = 0.0
	var tween := create_tween()
	tween.tween_property(_banner, "modulate:a", 1.0, 0.9)
