# Sources: Godot Shaders

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** Two of the sources are third-party works. The film follows their order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/`. The two third-party sources are not named in the text Bear pasted; their creators are an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13:
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html`
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html`
  - Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html`
  - Your first 2D shader: `tutorials/shaders/your_first_shader/your_first_2d_shader.html` (the 4.4 page for the "New Shader" step)
  - ShaderMaterial class reference: `classes/class_shadermaterial.html`
- Microsoft Learn, "Pixel Shader Stage" (Direct3D 11): learn.microsoft.com/en-us/windows/win32/direct3d11/pixel-shader-stage, read 2026-10-13.
- Khronos: the Vulkan `VkShaderStageFlagBits` reference (registry.khronos.org/vulkan/specs/1.3-extensions/man/html/VkShaderStageFlagBits.html). The OpenGL wiki pages returned HTTP 403 to the fetch tool; the OpenGL definition of "fragment" rests on Khronos community threads quoting the specification (community.khronos.org: "Pixel vs. Fragment Shader", "what is a fragment in OpenGL?"). Marked secondary in FACTCHECK row 29.
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS. Renderer stated on every pixel value.
- Bear's own chapter on shader foundations (`csye-7270-building-virtual-environments/chapters/06-shader-foundations.md`) for earlier runs on 4.7.2 (hint does not clamp; defaults read back as null; `SCREEN_TEXTURE` removed). Not named on screen; the film is standalone.

## Third-party sources followed (not copied)

- A short introduction to Godot shaders, about 8 minutes (creator not named in the pasted text).
- A seven-hour course on 2D shaders in Godot, YouTube cut of a paid course (creator not named in the pasted text). The pasted text mentions Patreon, Udemy and Flip Normals pricing for the full course.
- **Not stored.** Neither transcript was saved to this folder or anywhere in the repository; the coverage map in `ACTS.md` paraphrases which ideas appear where, by timestamp. No sentence was reused; every demonstration was rebuilt and run.
- **Open for Bear:** the creators' names and URLs, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab render or an editor capture of a file in `lab-shaders/`; scripts and raw logs are in `evidence/planning-checks/`. Failed and inconclusive runs are kept: `run-5a-verify5-FAILED-uniform-never-set.log` (the tween failure) and the first `TIME` attempt in `run-1-verify.log`.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/`), Python with Pillow for pixel measurements, no paid generation.
