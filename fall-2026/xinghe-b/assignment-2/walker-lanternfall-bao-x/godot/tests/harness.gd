extends SceneTree
## Shared headless test harness. Subclasses set `suite` and override run().

var suite := "unnamed"
var results: Array[Dictionary] = []
var failures := 0
## Each suite sets this as the last line of run(); a script error aborts run() early and leaves it false.
var completed := false

func _initialize() -> void:
	call_deferred("_main")

func _main() -> void:
	await run()
	if not completed:
		check("suite-ran-to-end", false, {"hint": "run() aborted early - look for SCRIPT ERROR above"})
	var out_dir := ProjectSettings.globalize_path("res://../evidence")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var path := "%s/%s.json" % [out_dir, suite]
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string(JSON.stringify({
		"suite": suite,
		"engine": Engine.get_version_info().string,
		"utc": Time.get_datetime_string_from_system(true),
		"checks": results.size(),
		"failures": failures,
		"results": results,
	}, "  "))
	f.close()
	print("%s: %d checks, %d failures -> %s" % [suite, results.size(), failures, path])
	quit(1 if failures else 0)

func run() -> void:
	pass

func check(id: String, passed: bool, observed: Dictionary = {}) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(("PASS " if passed else "FAIL ") + id + " " + JSON.stringify(observed))
