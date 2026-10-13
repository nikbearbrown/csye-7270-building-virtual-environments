extends RefCounted
# C01 (beat B01): the hook: stars that ride along against stars that stay put. Scene script for the capture harness's --scene option (see CAPTURE-PLAN.md).
# Contract: build(parent, audio_length) once, then at(t) before every frame. Copy capture_scenes.gd, scenes_lib.gd, sky_lib.gd and
# probe-free wrappers like this one into the harness project's root (they load each other as res://...). Set LOCAL_WORLD_SHADERS if
# the film's lab-shaders folder is not at the absolute path written in scenes_lib.gd.
const CS := preload("res://capture_scenes.gd")
var sc = CS.make("C01")


func build(parent: Node, audio_length: float) -> void:
	sc.build(parent, audio_length)


func at(t: float) -> void:
	sc.at(t)


func route() -> Dictionary:
	return sc.route()
