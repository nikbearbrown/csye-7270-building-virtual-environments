# Source and asset provenance

The `signal-garden` directory is the isolated copy of Walker Claude's current Signal Garden. `SOURCE-PROVENANCE.json` preserves its original repository HEAD, working-tree status and copied-file hashes. This source was already dirty; the original repository is untouched. `baseline-effects` holds original resources, while `historical-tuned` preserves the later course-series resources separately.

The teaching lab is newly derived from that source geometry by `bake_editor_lab.gd`; it is not an earlier historical revision. The diagnostic controls, tests, ramps and revised effect resources were authored locally for this lecture. Primitive meshes and Godot-generated gradients require no downloaded textures. The installed Godot engine is 4.7.2 stable.

Course authority: `/Users/bear/Downloads/seis-course-publish/assignments/07-particle-effects.md` and the related supplied chapter 09 and example 09 snapshot. The course working copy now uses different numbering; this lecture follows the supplied brief.

Primary API references: https://docs.godotengine.org/en/stable/classes/class_cpuparticles3d.html , https://docs.godotengine.org/en/stable/classes/class_renderingserver.html and https://docs.godotengine.org/en/stable/classes/class_input.html .

Native visual comparison and real-renderer pricing remain pending while the Mac is locked. No appearance acceptance, interactive performance, submission, upload or human review is implied by state-test results.
