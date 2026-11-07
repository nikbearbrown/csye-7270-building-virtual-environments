extends Node3D
## Effect A `hit_spark` root (CHANGE-BRIEF.md, Effect A; Revisions r1 (b)).
## It only restarts its three one-shot emitters when it enters the tree, counts
## its own processed time and frees itself after FREE_AFTER seconds (the longest
## emitter lifetime, 0.45 s, plus 0.1 s). It does not wait for `finished`, which
## never fires headlessly. Every particle setting lives in hit_spark.tscn.

const FREE_AFTER := 0.55

var _age := 0.0

func _ready() -> void:
	for child in get_children():
		if child is GPUParticles3D:
			(child as GPUParticles3D).restart()

func _process(delta: float) -> void:
	_age += delta
	if _age >= FREE_AFTER:
		queue_free()
