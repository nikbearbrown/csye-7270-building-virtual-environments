extends Node
## The cost of being seen. Recognition and the calendar are the same meter
## filling: every contact raises recognition and tears days off the calendar
## toward the anniversary, and the frost level follows the calendar.
##
## This node owns the numbers. It changes them first and then emits, so sound
## and HUD are both consequences of state, never causes of it.

signal day_torn(days_left: int)
signal recognition_changed(recognition: int)
signal night_ended(reason: String)

const DAYS_AT_START := 7
const RECOGNITION_TO_WIN := 4

var days_left := DAYS_AT_START
var recognition := 0
var ended := false


func spend(days_cost: int, recognition_gain: int) -> void:
	if ended:
		return

	recognition += recognition_gain
	recognition_changed.emit(recognition)

	for i in days_cost:
		days_left = maxi(0, days_left - 1)
		day_torn.emit(days_left)

	if recognition >= RECOGNITION_TO_WIN:
		ended = true
		night_ended.emit("seen")
	elif days_left <= 0:
		ended = true
		night_ended.emit("anniversary")


## 0.0 at the start of the night, 1.0 when the calendar runs out. The HUD uses
## this for the frost vignette, so the cost is legible with the sound muted.
func frost_level() -> float:
	return 1.0 - float(days_left) / float(DAYS_AT_START)
