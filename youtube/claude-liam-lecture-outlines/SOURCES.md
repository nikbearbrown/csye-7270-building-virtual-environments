# Sources: Outlines

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One of the sources is a third-party work. The film follows its order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot documentation (the stable pages, read 2026-10-13), the installed Godot 4.7.2, and one 2005 reference chapter for the sentence about branching. Every number and every Godot result on screen comes from a run in `evidence/planning-checks/`. The third-party course is not named in what Bear supplied; its creator is an open question for Bear.

## Primary

- Godot documentation (docs.godotengine.org/en/stable), read 2026-10-13; the raw text of each page was searched, not only summarised. Third-party text is paraphrased in this folder, never quoted at length:
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html`
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html` (uniforms, uniform hints, per-instance uniforms, flow control, discarding)
  - Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (`UV`, `COLOR`, `TEXTURE`, `TEXTURE_PIXEL_SIZE`, `REGION_RECT`)
  - Shader functions: `tutorials/shaders/shader_reference/shader_functions.html` (`mix`, `min`, `clamp`, `texture`)
  - Class reference: `classes/class_canvasitem.html` (texture filters, `set_instance_shader_parameter`), `class_sprite2d.html` (the `region_enabled` note on `UV`), `class_animatedsprite2d.html`, `class_shadermaterial.html` (a uniform change reaches every instance), `class_image.html` (`create_empty`, `blit_rect`, `create` deprecated), `class_imagetexture.html`, `class_texture2d.html`, `class_resource.html` (`resource_local_to_scene`), `class_projectsettings.html` (default texture filter)
- GPU Gems 2, chapter 34, "GPU Flow-Control Idioms", Mark Harris (NVIDIA) and Ian Buck (Stanford), Addison-Wesley, 2005. Read on 2026-10-13 at developer.nvidia.com/gpugems/GPUGems2/gpugems2_chapter34.html through the fetch tool's extract of the page (no copy saved). Used for one statement only, paraphrased in the film and in `FACTCHECK.md`: on 2005 hardware a group of fragments runs one branch at a time, so a branch costs extra where neighboring pixels disagree, and is cheap where they agree. The film says "a book from two thousand five" and claims no figure for today's hardware.
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS, Metal 4.0, Forward+; Compatibility was used for one comparison (identical pixels). The renderer is stated wherever the film shows a pixel value.

## Third-party source followed (not copied)

- A long video course on 2D shaders in Godot, of which about 24 minutes build a sprite outline (creator not named in the brief Bear supplied). The brief states what the source does, in Bear's words; the film follows that order of ideas and nothing else.
- **Not stored.** No transcript of it was saved to this folder or anywhere in the repository. `ACTS.md` paraphrases which ideas appear where. No sentence was reused; the sprite, the shaders, the numbers and every demonstration were rebuilt and run.
- **Open for Bear:** the creator's name and address, if you want them credited in the YouTube description. Nothing in the film itself names the source.

## What this film's demonstrations come from

Every Godot picture is a render of a file in `lab-shaders/` (14 shaders, each passing the series' `lab/check_shader.sh`), played from a small data-driven scene spec in `evidence/planning-checks/scenes/` and measured at the film's own geometry. Scripts, logs and summaries are in `evidence/planning-checks/` (`RESULTS.md` is the index). Failed and inconclusive runs are kept and labelled there: the covered-window stress test (`run-g1-INVALID-covered-window-transcribed.txt`), the display-paced one (`run-g0-INCONCLUSIVE-display-paced-transcribed.txt`), the first thin-part sprite (`run-d0-mascot-v1-INCONCLUSIVE-transcribed.txt`) and the first select-script attempt (`run-j0-FAILED-first-attempt-test-harness-bug-transcribed.txt`).

## Tools used (all free)

Godot 4.7.2 (the series' Shader Lab at `../_godot-shaders-series/lab/` and throw-away scratch projects), Python with Pillow and numpy for measuring PNGs. No paid generation, no model calls from any script.
