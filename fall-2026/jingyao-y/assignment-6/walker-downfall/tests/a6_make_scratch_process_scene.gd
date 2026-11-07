extends SceneTree
## A6 Step 6 helper (agent, 2026-11-07): writes previews/scratch_process_shader.tscn,
## one GPUParticles3D whose process material is a unique deep copy of
## effects/hit_spark.tscn Sparks'. The user converts that copy to a
## ShaderMaterial in the editor; the effect scene itself is never touched.
func _init() -> void:
	var src := (load("res://effects/hit_spark.tscn") as PackedScene).instantiate()
	var sparks := src.get_node("Sparks") as GPUParticles3D
	var node := GPUParticles3D.new()
	node.name = "ScratchSparksCopy"
	node.process_material = (sparks.process_material as ParticleProcessMaterial).duplicate(true)
	node.draw_pass_1 = QuadMesh.new()
	var packed := PackedScene.new()
	packed.pack(node)
	var err := ResourceSaver.save(packed, "res://previews/scratch_process_shader.tscn")
	print("saved scratch scene err=", err)
	node.free()
	src.free()
	quit(err)
