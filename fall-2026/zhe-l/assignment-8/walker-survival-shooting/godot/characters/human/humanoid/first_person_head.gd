extends SkeletonModifier3D

@export var head_bone: StringName = &"head.x"
@export var hidden_scale: float = 0.001

func _process_modification_with_delta(_delta: float) -> void:
	var skeleton := get_skeleton()
	if skeleton == null:
		return
	var bone := skeleton.find_bone(head_bone)
	if bone < 0:
		return
	skeleton.set_bone_pose_scale(bone, Vector3.ONE * hidden_scale)
