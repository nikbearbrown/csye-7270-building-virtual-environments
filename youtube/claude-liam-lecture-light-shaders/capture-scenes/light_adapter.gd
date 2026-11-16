extends Node
# Adapter between the shared harness and the film's own scene script (evidence/planning-checks/light_scene.gd, used unchanged) driven by captures-build.json
# (captures.json with every event time scaled to the measured audio, see captures.py). Capture id from L_ID. Native route: 1920 x 1080 at scale 1.
var s
func harness_setup(c: Dictionary) -> void:
	var LS = load("/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-light-shaders/evidence/planning-checks/light_scene.gd")
	s = LS.new()
	s.manual = true
	s.setup(OS.get_environment("L_ID"), "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-light-shaders/lab-shaders", "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-light-shaders/capture-scenes/captures-build.json")
	add_child(s)
func harness_frame(t: float) -> void:
	s.step(1.0 / 30.0)
