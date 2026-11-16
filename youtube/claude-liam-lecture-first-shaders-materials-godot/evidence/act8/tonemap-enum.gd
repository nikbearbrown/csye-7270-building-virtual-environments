extends SceneTree
# B57: the assignment says "4 is TONE_MAPPER_AGX, not ACES". Ask the engine (Godot 4.7.2) for the values.
func _initialize() -> void:
	print("Godot ", Engine.get_version_info()["string"])
	print("TONE_MAPPER_LINEAR ", Environment.TONE_MAPPER_LINEAR)
	print("TONE_MAPPER_REINHARDT ", Environment.TONE_MAPPER_REINHARDT)
	print("TONE_MAPPER_FILMIC ", Environment.TONE_MAPPER_FILMIC)
	print("TONE_MAPPER_ACES ", Environment.TONE_MAPPER_ACES)
	print("TONE_MAPPER_AGX ", Environment.TONE_MAPPER_AGX)
	quit(0)
