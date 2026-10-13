# Sources and provenance

Reviewed 13 October 2026. User's pasted transcript is preserved verbatim in sources/user-transcript.txt; its creator, exact video title, and URL were not provided. No attribution has been invented. The user's learning-path notes are preserved in sources/request-notes.md. Narration is an original teaching rewrite, not the transcript read aloud.

Course context: ../../book.md and ../../modules/06-shader-foundations/lesson.md. These orient the course credit and verification emphasis; this film does not claim to adapt that entire separate module or teach the full assignment.

## Primary references
- [language](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html)
- [canvas](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html)
- [spatial](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html)
- [intro](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html)
- [migration](https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html)
- [first2d](https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_first_2d_shader.html)
- [first3d](https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_first_3d_shader.html)
- [visual](https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html)
- [compute](https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html)
- [book](https://thebookofshaders.com/)
- [community](https://godotshaders.com/)

## Executed evidence
- Godot 4.7.2.stable.official.ed1daf0bf, OpenGL 4.1 Metal / Compatibility, Apple M4 Pro. Actual stdout/stderr: evidence/godot-run.log. Twenty positive shader files, with actual GPU-rendered SubViewport captures at 3840×2160.
- godot/lab.gd is a deterministic teaching harness, not human gameplay. It sets material values, renders, and reads selected pixels. It does not establish real-time performance.
- evidence/negative-type.log is a real, deliberately invalid assignment. The small negative program exits normally after Godot logs the shader failure. Never interpret exit code alone as validity.
- evidence/godot-first-attempt.log preserves the initial switch failures. Adding explicit default breaks corrected both examples; the clean run overwrote only the canonical positive log, not the preserved first attempt.
- verify_evidence.py performs 24 pixel checks with 2/255 tolerance and checks diagnostics. Report and numeric samples are in evidence/verification.txt and evidence/pixel-checks.json.
- captures/godot-editor.png is a native editor screenshot obtained through computer use. It shows preview.tscn with ColorRect and its Material field. Do not claim the screenshot shows expanded uniform controls.
- capture_docs.py captured public pages at 1600×900 CSS and DPR 2.4. The URL/date/status manifest is evidence/web-captures.json. Godot Shaders returned HTTP 454 while rendering the actual homepage and gallery; the captured pixels were inspected. Do not claim an authenticated session or a successful HTTP 200 for that site.
- Godot and browser source captures were visually inspected on evidence/capture-contact-sheet.jpg; the final cube camera framing was enlarged afterward and inspected separately.
- evidence/sha256.json identifies the source and capture files. Regenerate it after any evidence change.

## Asset rights and provenance
The shader code, test harness, checker texture and conceptual drawings were authored for this lesson. Public documentation and homepage captures are short contextual teaching references, not republication of full articles or redistribution of community shader code. No community shader was downloaded or incorporated. The Professor Bear opening portrait comes from the approved local library, selected by slug seed: professor-bear-1x1-93.png. No paid generation, cloned third-party voice, or stock imagery is used. Liam uses the skill's local Kokoro am_onyx voice in stage two.

## Corrections to the supplied material
- A fragment is a candidate contribution, not invariably a one-to-one final pixel. No promised invocation order or absolute ban on reading stored texture data.
- Vertex displacement changes rendering, not scene transforms or collision geometry.
- TIME is an engine clock, not an elapsed-damage timer; no claim that it increases forever without rollover or ignores time scale.
- Alpha transparency alone is not a glass material or refraction.
- Matrix constructor vectors are columns. mat2(vec2(1,2),vec2(3,4)) has rows (1,3) and (2,4).
- vec2 c.xx is valid; assigning three components into vec2 is not. Do not mix .x and .r naming families in one swizzle.
- Separate ShaderMaterials can share one Shader. Copying the shader code is unnecessary for independent values.
- hint_range is an Inspector hint, not runtime clamping. The executed harness stores 7.0.
- Current checked stable documentation permits per-instance uniforms in canvas_item and spatial; avoid promising the feature for every old Godot release.
- Explicit breaks are retained in every terminating switch case in the tested examples. Fallthrough is demonstrated deliberately, without crashing anything.
- Loops are supported; termination and bounded work are required. No infinite loop is executed.
- Five shader types named in the user notes are examples, not an exhaustive current count.
- Compute requires a RenderingDevice renderer; the Compatibility shader lab does not claim a compute test.
