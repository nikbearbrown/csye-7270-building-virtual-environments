# Assignment 5 — Sources

Earlier project write-ups are preserved under a5/archive/pre-final-documents/. Asset attribution and manifests remain beside their assets.

## Assets and technical sources

Cargo textures: [Rusty Metal Sheet, Poly Haven](https://polyhaven.com/a/rusty_metal_sheet). Its [CC0 license](https://polyhaven.com/license) permits redistribution. The 1K diffuse, roughness, GL normal and DX normal PNGs retain their hashes in textures/cargo_panel/ATTRIBUTION.md. The corrected-DX copy has identical image bytes and a different Y-inversion import setting. The hint texture contains literal 64, 128 and 192 bytes.

The technical references are Godot's [shading language](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html), [spatial shader](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html), [shader introduction](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html), [ShaderMaterial](https://docs.godotengine.org/en/stable/classes/class_shadermaterial.html), and [Movie Maker](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html) documentation. Actual engine measurements establish this build's behavior; recording does not establish real-time FPS.

## Assistance and decisions

Codex also completed the initial CHANGE-BRIEF from the supplied skeleton, including
the color statement, numeric predictions and question answers, after inspecting
the game and measuring the calibration background. The later guides in the
conversation were the instructions used for the shader implementations; they do
not establish that the earlier specification was written without assistance.

I supplied interfaces, formulas and step-by-step shader guides in the conversation and approved the requirement revisions. Codex wrote the three custom shaders from those guides, performed shader mutations/restoration, drafted LANGUAGE-NOTES, and exported the generated shader through Godot's native editor material-conversion actions. The export was not an Inspector mouse session. Its program, logs and earlier notes are retained.

The four Claude subagent records cover project guidance, driver/test planning, implementation and material auditing. Prompts and records are under a5/. The oversized implementation record stays local with an annotated excerpt in the course copy. At my request Codex completed the remaining verification tools, measurements, report drafts, film assembly and delivery preparation.

I chose to retain the existing gameplay timer, the exact color statement and the supplied normal map. I accepted the dated R3/R1 clarifications, crate_stack substitution and raking-light comparison. I did not replace the original pixel predictions with measured values. The performance failure remains beside its isolated passing repeat.

Assistance is not a claim of unaided implementation or a human-only playtest. Earlier messages or historical commit wording describing a shader edit as exclusively manual do not describe the full recorded workflow. FRICTIONAL.md records the count audit and document history.

## Film

The film follows the local Brutalist godot-gamedev workflow with verbatim source excerpts, real engine imagery and local Kokoro am_onyx narration. Its SOURCES, FACTCHECK, SHOTLIST, media hashes and export receipt accompany the reel. Earlier Downfall films remain separate.

