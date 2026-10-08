## Prints what import options the scene importer actually exposes for a GLB.
extends SceneTree

func _initialize() -> void:
	# Ask ResourceImporterScene what options it recognises
	var importer := ResourceImporterScene.new()
	var opts := []
	importer.get_import_options("", opts, 0)
	for o in opts:
		if "use_name" in str(o.get("name","")) or "suffix" in str(o.get("name","")) \
		   or "physics" in str(o.get("name","")) or "body" in str(o.get("name","")) \
		   or "collision" in str(o.get("name","")).to_lower():
			print(o)
	quit(0)
