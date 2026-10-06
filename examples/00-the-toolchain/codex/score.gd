extends Node2D

var left_score := 0
var right_score := 0

@onready var _left_label: Label = $LeftScore
@onready var _right_label: Label = $RightScore


func _ready() -> void:
	_update_labels()


func _on_left_wall_ball_exited() -> void:
	right_score += 1
	_update_labels()


func _on_right_wall_ball_exited() -> void:
	left_score += 1
	_update_labels()


func _update_labels() -> void:
	_left_label.text = str(left_score)
	_right_label.text = str(right_score)
