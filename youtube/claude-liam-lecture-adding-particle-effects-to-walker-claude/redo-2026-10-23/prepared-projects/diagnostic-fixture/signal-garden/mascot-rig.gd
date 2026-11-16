extends Node3D
var animator: AnimationPlayer
var skeleton: Skeleton3D
var current := ""
var bone_path: String
func _ready() -> void:
	var model := preload("res://signal-garden/assets/claude-mascot.glb").instantiate()
	model.name = "Model"
	add_child(model)
	skeleton = model.find_children("*", "Skeleton3D", true, false)[0]
	bone_path = str(get_path_to(skeleton))
	animator = AnimationPlayer.new()
	animator.name = "AnimationPlayer"
	animator.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(animator)
	var library := AnimationLibrary.new()
	for mode in ["idle", "walk", "charge", "celebrate"]:
		var anim := Animation.new()
		anim.length = 0.6 if mode == "charge" else 0.8
		anim.loop_mode = Animation.LOOP_NONE if mode == "charge" else Animation.LOOP_LINEAR
		for bone in ["Arm.L", "Arm.R", "Leg.1", "Leg.2", "Leg.3", "Leg.4"]:
			var track := anim.add_track(Animation.TYPE_ROTATION_3D)
			anim.track_set_path(track, NodePath(bone_path + ":" + bone))
			var amp := 0.035
			if mode == "walk": amp = 0.45 if bone.begins_with("Leg") else 0.15
			if mode == "charge": amp = 0.65 if bone.begins_with("Arm") else 0.0
			if mode == "celebrate": amp = 0.85 if bone.begins_with("Arm") else 0.18
			var sign_value := -1.0 if bone in ["Arm.R", "Leg.2", "Leg.4"] else 1.0
			for j in range(5):
				var angle := sin(j * PI / 2.0) * amp * sign_value
				anim.rotation_track_insert_key(track, anim.length * j / 4.0, Quaternion(Vector3.FORWARD if bone.begins_with("Arm") else Vector3.RIGHT, angle))
		library.add_animation(mode, anim)
	animator.add_animation_library("", library)
	set_state("idle")
func set_state(next: String) -> void:
	if next != current:
		current = next
		animator.play(next, 0.08)
