class_name CharacterIntent
extends RefCounted

enum TabletPress {
	NONE,
	SHORT,
	LONG,
}

var move := Vector2.ZERO
var look_yaw := 0.0
var sprint := false
var jump := false
var aim := false
var tablet_press := TabletPress.NONE
var interact := false
