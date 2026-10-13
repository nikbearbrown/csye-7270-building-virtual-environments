# Godot Shading Language
CSYE 7270 Building Virtual Environments · Liam, in for Bear · @NikBearBrown

**Status: lecture authored and evidence checked; audio and final film are not rendered.**

- NARRATION.md: every spoken line.
- ACTS.md and SHOTLIST.md: coverage and visual decisions.
- beat_sheet.json and make_sheet.py: executable film plan.
- scenes.py: eleven authored Manim scenes; other beats use registered Remotion components.
- godot/: 20 working shader examples, a capture harness, and an editor preview scene.
- FACTCHECK.md, SOURCES.md, evidence/: review and reproducible results.
- BUILD-PROMPT.md: stage-two instructions for the 4K master.

## Try the tint effect
Open godot/project.godot in Godot. Open preview.tscn, select ColorRect, expand its ShaderMaterial and Shader Parameters. Change amount among 0, 0.5 and 1; tint changes the target color. The source is shaders/flash.gdshader. The program preserves incoming alpha. To exercise all examples and regenerate evidence, use CAPTURE.md. The default main scene is a scripted capture lab, not an interactive game.

The negative.gd test is deliberately invalid and separate from the main scene. It exists to demonstrate why diagnostics matter. No nonterminating shader is included.

## Learning links
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
