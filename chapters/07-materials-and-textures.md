# Chapter 7 — Materials and Textures

## Executive summary

A 3D material is a stack of textures and numbers. Each texture leads two lives: how Godot imports it (compression, mipmaps, whether it is a normal map), and which material slot and colour channel reads it. This chapter explains both, using Godot 4.7.2's `StandardMaterial3D`, `ORMMaterial3D` and texture importer, and adds the lighting and global-illumination settings that decide what a material shows at all.

The hands-on work is on the Poly Haven "Dutch Ship Medium" model in `walker-3d-graphics-settings`:

- First an agent audits the ship's three materials, their nine textures and their attribution, and writes a headless test that pins what it found.
- Then it makes one change: the hull gets the ambient occlusion its textures carry but no material reads.

The machine evidence covers three things: the slots, channels, scalars and import settings are what the audit says; the normal maps really are normal maps; and after the change the hull uses an external `ORMMaterial3D`, with AO switched on, that survives a reimport. The worked run shows why that last clause needs checking by you. The agent that finished the change left AO off, and its 100-check test did not notice. What no headless check can show is whether the ship looks better, or looks like wood and iron at all. That is a judgement you make in the running scene, under lighting you control.

## The question

The ship's textures come in threes per part: `diff`, `nor_gl` and `arm`. The `arm` file packs ambient occlusion, roughness and metalness into its red, green and blue channels. Load the ship headless, though, and all three imported materials report `ao_enabled=false`. None of the three glTF materials declares an occlusion texture, so the red channel of every `arm` file is imported, uploaded and never read.

The sails are set to alpha scissor at 0.5, but their colour texture is a JPEG, and Godot reports it as `FORMAT_RGB8` with no alpha. All nine textures are imported Lossless, which Godot's own documentation calls the mode for 2D, and "Detect 3D", the setting that would fix that, is switched off.

None of this is visible in a screenshot at a glance, and all of it is visible in text files an agent can read. So the question is: **what can an agent actually establish about a material by reading and running it headlessly, what does it get wrong while doing so, and what is left for you to judge by looking?**

## Ideas you need

### A PBR material is a set of measurements, not a picture

Godot's 3D materials use the metallic–roughness model that glTF 2.0 also uses. A surface is described by a few quantities per pixel:

- **Base colour (albedo)**: the colour the surface reflects.
- **Metallic**: whether it behaves like a metal.
- **Roughness**: how blurred its reflections are.
- **Normal**: which way the surface faces at a detail smaller than the mesh.
- **Ambient occlusion**: how much of the surrounding light reaches a crevice.

A light and a camera then turn those quantities into a colour. Two consequences follow:

- A material that looks right under one light can look wrong under another, so judging a material is always judging it under stated lighting.
- The textures that hold these quantities are not all pictures. Only the base colour is a colour. The rest are data that happen to be stored in an image file.

The glTF 2.0 specification, the format the ship arrives in, spells out the encoding for each texture. It is worth reading once, because the whole chapter depends on it:

| Texture | glTF 2.0 rule |
|---|---|
| base colour | "MUST contain 8-bit values encoded with the sRGB opto-electronic transfer function", decoded to linear before use |
| metallic–roughness | "Its green channel contains roughness values and its blue channel contains metalness values. This texture MUST be encoded with linear transfer function" |
| normal | "stored with linear transfer function"; red, green and blue map to X, Y and Z, and "Normal textures SHOULD NOT contain blue values less than or equal to 0.5" |
| occlusion | "The red channel of the texture encodes the occlusion value"; it affects "indirect lighting from ambient sources. Direct lighting is not affected." |

### Colour versus data: why the decode matters

An 8-bit texel stores 0–255. For a colour, that number is sRGB-encoded: the steps are spaced for human eyes, not for arithmetic. The renderer decodes the value to linear before lighting. For data (a normal, a roughness), the number *is* the value, and decoding it as sRGB corrupts it.

In a custom shader you choose the decode with a hint. Godot's reference says that "any texture which contains sRGB color data requires a `source_color` hint", while `hint_normal` marks a normal map ([Shading language](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html)).

The size of the error is easy to compute. A perfectly flat normal-map texel is (128, 128, 255):

- Read linearly, 128/255 = 0.502. Unpacked with `2c − 1` that gives (0.004, 0.004, 1.0): flat.
- Decoded as sRGB, 0.502 becomes 0.216, which unpacks to (−0.568, −0.568, 1.0). Normalised, that surface is tilted 38.8° away from where it faces. A light shining straight along the true surface normal lights it at N·L = 0.779 instead of 1.0, 22% too dark, and lopsided.

The data was right, the file was right, and the lighting is wrong because of one word in a uniform declaration. Chapter 8 turns this into a check.

### StandardMaterial3D, ORMMaterial3D, ShaderMaterial

Godot gives you three ways to describe a 3D surface:

- **`StandardMaterial3D`** has a separate texture slot for each quantity, and lets you pick which channel of each texture to read (`roughness_texture_channel`, `metallic_texture_channel`, `ao_texture_channel`; red is 0, green 1, blue 2, alpha 3, grayscale 4).
- **`ORMMaterial3D`** uses "a single ORM texture", in which, per Godot's material guide, "the different color channels of that texture are used for each parameter" ([Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html)).
- **`ShaderMaterial`** is Chapter 6's custom shader, where you declare every uniform and hint yourself.

Two details of the first two are not on the reference pages, but are plain in the generated shader code in `scene/resources/material.cpp` at the 4.7.2 commit:

1. **ORM channel order.** The ORM path emits `AO = orm_tex.r;`, `ROUGHNESS = orm_tex.g;` and `METALLIC = orm_tex.b;`, the same red–green–blue order as a Poly Haven `arm` file. AO is emitted only when the AO feature (`ao_enabled`) is on. An `ORMMaterial3D` with an ORM texture and AO switched off uses the texture for roughness and metalness only.
2. **Scalars behave differently.** In `StandardMaterial3D` the code is `ROUGHNESS = roughness_tex * roughness;` (and likewise for metallic): the scalar multiplies the texture. In `ORMMaterial3D` the texture channels are used directly and the `metallic` and `roughness` scalars do not enter. Converting a Standard material to ORM therefore preserves its look only when both scalars were 1.0. For the ship they are, because glTF's default metallic factor is 1.0.

Other settings that change the look, from the [BaseMaterial3D reference](https://docs.godotengine.org/en/stable/classes/class_basematerial3d.html):

- `ao_light_affect` defaults to 0.0, so AO darkens ambient light, not direct light, unless you raise it.
- The `ALPHA_SCISSOR` transparency mode "will cut off all values below a threshold, the rest will remain opaque". The guide calls it "faster to render than Alpha".
- Cull mode `Disabled` draws both sides of every triangle, which the guide warns "can decrease performance".

### Texture import: the half an agent forgets

Every image has a `.import` file beside it, and that file decides what reaches the GPU. It is text an agent can read and diff. The options that matter here, with the integer values the file stores (from `editor/import/resource_importer_texture.cpp` at the 4.7.2 commit):

| Option | Values | Meaning |
|---|---|---|
| `compress/mode` | 0 Lossless, 1 Lossy, 2 VRAM Compressed, 3 VRAM Uncompressed, 4 Basis Universal | Lossless is "the default and most common compression mode for 2D assets". VRAM Compressed is "the default and most common compression mode for 3D assets", and reduces video memory "usually by a factor between 4 and 6" ([Importing images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)). |
| `compress/normal_map` | 0 Detect, 1 Enable, 2 Disabled | Enable forces RGTC compression, keeping only red and green. That applies to VRAM compression; under Lossless, the hull's normal map imported as plain `FORMAT_RGB8`. |
| `mipmaps/generate` | true / false | "It's recommended to enable mipmaps in 3D." Without them, distant surfaces shimmer. |
| `roughness/mode` | 0 Detect, 1 Disabled, 2 Red … 6 Gray | Roughness limiting based on a normal map |
| `process/normal_map_invert_y` | true / false | Converts DirectX-style normal maps (Y−) to the OpenGL style (Y+) that "Godot requires" |
| `detect_3d/compress_to` | 0 Disabled, 1 VRAM Compressed, 2 Basis Universal | What to switch to when the texture is detected in 3D |

**The detection trap.** "Detect 3D" and "Normal Map: Detect" sound like import-time analysis. They are not. The importer's code registers callbacks (`_texture_reimport_3d`, `_texture_reimport_normal`) that the *renderer* calls when it draws a texture in a 3D material inside the editor. Only then does the editor rewrite the `.import` file and reimport.

Headless, nothing is drawn, so nothing is detected. In this book's experiment, a scene using two decal textures as albedo and normal map was run headless, reimported, and opened with `--headless --editor`; both `.import` files stayed byte-identical. An agent that wires a texture into a material by editing text leaves that texture's import settings exactly as they were, until someone opens the scene in a real editor. After that first editor session, `git diff` your `.import` files and read what changed.

### Decals project materials onto other surfaces

A `Decal` node projects albedo, normal, ORM and emission textures onto whatever surfaces its box touches, with no extra geometry. Godot's decal guide ([Using decals](https://docs.godotengine.org/en/stable/tutorials/3d/using_decals.html)) records the limits you need before promising one in a design:

- "Decals are only supported in the Forward+ and Mobile renderers, not the Compatibility renderer."
- They "cannot affect material properties other than the ones listed above".
- They "cannot employ custom shaders". A decal's material is fixed-function.
- Their texture filtering comes from one project setting (Rendering › Textures › Decals › Filter).

`walker-3d-decals` exercises all four kinds of texture.

### Lighting and global illumination decide what a material can show

An AO texture that only affects ambient light does nothing visible in a scene lit only by a strong directional light. A rough metal looks like plastic without something to reflect. So the lighting setup is part of the material test.

Godot's techniques, with their renderer support from [Introduction to global illumination](https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/introduction_to_global_illumination.html):

| Technique | Kind | Renderers |
|---|---|---|
| ReflectionProbe | optionally real-time | all |
| LightmapGI | baked | all (baking needs a RenderingDevice) |
| VoxelGI | real-time | not Mobile or Compatibility |
| SDFGI | semi-real-time | not Mobile or Compatibility |
| Screen-space indirect lighting (SSIL) | real-time | not Mobile or Compatibility |

Screen-space AO (SSAO) is a post-process in the `Environment`, and it is separate from a material's AO texture. When you judge texture AO, turn SSAO off, or you will not know which one you are seeing.

### Attribution is part of the material

A texture's licence travels with it. `walker-3d-decals` shows the range in one project. Its README lists:

- Kenney's checker texture, CC0;
- johndn's paint splatter, CC-BY 3.0;
- Alex Foster's painted arrow, CC-BY-SA 3.0;
- Yughues's sci-fi panels, CC0;

and it tells you to "review asset license obligations before distribution". CC-BY requires credit. CC-BY-SA adds share-alike terms on adaptations. CC0 requires nothing, and Poly Haven's licence page says "you do not need to give credit or attribution when using them (although it is appreciated)".

This course asks for provenance regardless of licence: where the file came from, who made it, under which licence, and on which date you checked. The same rule covers textures you prompt from an image model (Chapter 2). A generated "normal map" is a picture that looks like a normal map, and nothing guarantees its vectors are unit length or its blue channel is above 0.5. The pixel check in this chapter's test is exactly the check to run on one.

## The Walker example: walker-3d-graphics-settings

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-3d-graphics-settings`](https://github.com/nikbearbrown/walker-3d-graphics-settings), [`walker-3d-decals`](https://github.com/nikbearbrown/walker-3d-decals), [`walker-3d-global-illumination`](https://github.com/nikbearbrown/walker-3d-global-illumination), [`walker-compute-texture`](https://github.com/nikbearbrown/walker-compute-texture), [`walker-compute-heightmap`](https://github.com/nikbearbrown/walker-compute-heightmap). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

`walker-3d-graphics-settings` is a Walker adaptation of Godot's `3d/graphics_settings` demo (MIT), public at [github.com/nikbearbrown/walker-3d-graphics-settings](https://github.com/nikbearbrown/walker-3d-graphics-settings). Its upstream source is [github.com/godotengine/godot-demo-projects](https://github.com/godotengine/godot-demo-projects), commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, path `3d/graphics_settings`.

A recursive diff against the local checkout of that commit shows the Walker copy differs in two ways only:

- `config/name` changed from `"3D Graphics Settings"` to `"Walker — 3D Graphics Settings"`;
- a headless harness, `test_settings.gd`, was added (reproduced in `../examples/07-materials-and-textures/tests/`).

The demo is a settings menu over a 3D scene: a directional, an omni and a spot light, a fog volume, a mirror, a reflective sphere, and the Poly Haven ship under `polyhaven/`. Its README says "Renderer: Forward+".

What its checks establish, per its own `FRICTIONAL.md`: "17 assertions pass", covering five slider endpoints and the show/hide button, driven by synthetic keyboard and mouse input. The same record says "headless stored settings are not pixel, renderer support, performance, hardware, or human verification", and that the "asset-specific license audit remain[s] outstanding". That open audit is where this chapter starts.

The ship itself:

- It is "Dutch Ship Medium" from Poly Haven, CC0. Poly Haven's API credits James Ray Cock (model, textures, cleanup), Rico Cilliers (sails model, textures) and Nicolò Zubbini (original model), with a publication timestamp of 2022-05-25.
- The upstream demo ships it with no attribution file at all. Its README does not mention it.
- The `.gltf` was written by "Khronos glTF Blender I/O v1.7.33".
- Nine 1024 × 1024 JPEG textures sit in `polyhaven/textures/`.

The other Walker builds named for this chapter each demonstrate one idea above. Each is public at `github.com/nikbearbrown/<build name>`, and each starts from the same upstream commit.

| Build (upstream path) | What it shows | What its record verifies, and what it does not |
|---|---|---|
| `walker-3d-decals` (`3d/decals`) | Decals with albedo, normal, ORM (`puddles_orm.png`) and emission textures; four credited assets under three licences (CC0, CC-BY 3.0, CC-BY-SA 3.0) | 25 headless checks, including real P-key ray placement. "Forward+ GPU appearance and both native-4K Liam films remain unverified/pending." |
| `walker-3d-global-illumination` (`3d/global_illumination`) | VoxelGI, SDFGI, LightmapGI and reflection probes on one map | 42 headless mode-state assertions. "GPU lighting, reflection appearance, camera interaction, performance and both native-4K Liam films remain unverified." |
| `walker-compute-texture` (`compute/texture`) | A texture written every frame by a compute shader (rain on water) | "Eleven headless state checks pass." They found and fixed "a script error when no RenderingDevice exists" and "rain drops that could land one texel outside the texture" (19 of 5,000 in the reproduction). "The ripple effect itself has not yet been seen running on a GPU." |
| `walker-compute-heightmap` (`compute/heightmap`) | An island heightmap generated from noise "either with a CPU loop or with a GLSL compute shader" | A real click on Create (CPU) produced a 512 × 512 island, and the same seed repeated byte for byte. An arithmetic check found "54,757 out-of-range gradient indices among 262,144 pixels in the original shader", fixed with a clamp. "GPU execution, CPU/GPU parity and actual visual capture remain pending." |

The last two matter for this course's old "procedural texture generation" week. A texture a shader writes is still a texture, and the record of each build shows the same boundary: the arithmetic can be checked headless, and the image cannot.

## Hands-on: audit the ship's materials, then give the hull its AO

### Predict

1. The hull's `arm` texture has a red channel between 0.827 and 1.0, with a mean of 0.99 (a headless pixel probe measured this). If AO only darkens ambient light, how visible will the change be, and under what lighting would you even see it?
2. The imported hull material has metallic and roughness scalars of 1.0. If you convert it to `ORMMaterial3D`, what happens to those scalars? What would have to be true for the conversion to change the look?
3. An agent wires a texture into a new material by editing text and never opens the editor. What happens to that texture's import settings?
4. The sails use alpha scissor at 0.5, and their colour texture is a JPEG. What do you expect at the edges of each sail?

### Build It

Get the demo at the exact commit. Only the one demo folder is needed, so a sparse, blobless clone keeps the download small. These commands were not run for this book; the book's run started from the `walker-3d-graphics-settings` adaptation, which matches this checkout apart from the project title and `test_settings.gd` (which you copy in below).

```bash
git clone --filter=blob:none --no-checkout https://github.com/godotengine/godot-demo-projects.git
```

```bash
cd godot-demo-projects
```

```bash
git sparse-checkout set 3d/graphics_settings
```

```bash
git checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

Copy `3d/graphics_settings` into a folder of your own as `godot/`, `git init` it, and commit that as your baseline. As in Chapter 6, test commands are wrapped in `timeout 120` so that a script error cannot leave headless Godot running. Copy `test_settings.gd` from `../examples/07-materials-and-textures/tests/` into `godot/`. Then import and run the baseline:

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://test_settings.gd --fixed-fps 60
```

The baseline prints `RESULT 17 checks, 0 failures; headless state only, no pixel/performance proof`.

**Prompt 1 — the audit.** Paste this into Claude Code. The attribution facts in it are ones you check yourself on polyhaven.com first. The agent records them; it does not source them.

```text
This is a scratch copy of walker-3d-graphics-settings, a Walker adaptation of
Godot's 3d/graphics_settings demo (Godot 4.7.2, GDScript, project in godot/).
Inspect before editing. Always run Godot with --headless; never add
--rendering-driver. A headless run uses a dummy renderer: it draws nothing.

Task: audit the Dutch ship's materials and textures, then write a headless
test that pins what you found. Do not change any material, scene or .import
file in this task.

1. Read godot/polyhaven/dutch_ship_medium_1k.gltf (the materials, textures
   and images arrays), every .import file in godot/polyhaven/, and the
   lighting and environment in godot/3d_scene.tscn and godot/settings.gd.
2. Write godot/MATERIALS.md with:
   - one table row per material slot actually used by each of the three
     imported materials: slot, texture file, channel, whether the data is
     color (sRGB) or non-color (linear) per the glTF 2.0 rules, and the
     texture's import settings (compress/mode, compress/normal_map,
     mipmaps/generate, detect_3d/compress_to);
   - the material flags that change the look (transparency, alpha scissor,
     cull mode, metallic and roughness scalars);
   - the lights and environment effects that light the ship, and which of
     them the settings UI can switch;
   - findings: anything in the files that looks wrong, wasteful or unused,
     each with the evidence line;
   - attribution, using exactly these facts, which I checked on
     polyhaven.com and api.polyhaven.com on 2026-09-27: "Dutch Ship Medium"
     from Poly Haven; credits James Ray Cock (model, textures, cleanup),
     Rico Cilliers (sails model, textures), Nicolò Zubbini (original
     model); license CC0 1.0; published 2022-05-25.
3. Write godot/tests/test_materials.gd (extends SceneTree) that loads the
   imported ship scene headlessly and asserts the table: every slot's
   texture path and channel, the flags and scalars, the import settings
   read from the .import files with ConfigFile, and a pixel check that each
   *_nor_gl texture is a plausible tangent-space normal map (decode with
   Image.load_from_file; blue above 0.5 on at least 95% of sampled texels)
   while each *_diff texture is not. Print one PASS/FAIL line per check and
   exit 1 on any failure.
4. Run it with: godot --headless --path godot --script res://tests/test_materials.gd --fixed-fps 60
   and the existing: godot --headless --path godot --script res://test_settings.gd --fixed-fps 60
   Show the real output. Say what the test cannot establish headlessly.
Do not commit.
```

```bash
claude -p "$(cat prompt-1-audit.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot --headless:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(grep:*)" --max-turns 60 --output-format stream-json --verbose > session-1-audit.jsonl
```

**Review the audit before you trust it.** For every sentence in `MATERIALS.md` that names a value, check it against the file or against Godot:

- An enum written as an integer in a `.tscn` means nothing until you look it up. `Environment.TONE_MAPPER_AGX` is 4.
- A claim about what an import setting "stores" is checkable with `get_image().get_format()`.
- A number of megabytes the agent did not measure should come out.

Commit the agent's draft and your corrections separately.

**Prompt 2 — the change.**

```text
Read godot/MATERIALS.md and godot/tests/test_materials.gd first.

Change one thing: give the hull ambient occlusion from the red channel of
its ARM texture, without changing anything else about how the hull looks.

- Create godot/materials/dutch_ship_medium_hull.tres as an ORMMaterial3D
  using the hull's diff, nor_gl and arm textures.
- Wire it through the glTF importer's per-material "Use External" setting in
  godot/polyhaven/dutch_ship_medium_1k.gltf.import, so a reimport keeps it.
  Do not edit the .gltf file or any texture.
- Every property the imported hull material had (see MATERIALS.md) must keep
  its value unless ORM packing requires otherwise; say which ones changed
  and why.
- Rigging and sails must stay exactly as they were.
- Reimport with: godot --headless --path godot --import
- Update test_materials.gd so it proves the hull now uses the external
  material with AO from the red channel, that the other hull properties
  match the audited values, and that rigging and sails are unchanged. Run it
  and test_settings.gd with --fixed-fps 60 and show the real output.
- List the human checks needed to judge the AO in the running scene.
Do not commit.
```

**Codex difference.** Codex has no `CLAUDE.md` here and reads any `AGENTS.md` instead. This demo has none, so everything the agent needs must be in the prompt, which this one is. Run it with a writable sandbox and closed stdin:

```bash
codex exec -s workspace-write "$(cat prompt-2-ao.txt)" < /dev/null
```

### Use It

This is the only place the material is judged. Open `godot/project.godot` in the Godot 4.7.2 editor; the demo uses the Forward+ renderer.

1. **Control the lighting.** Run the project (F5). In the settings panel, confirm SSAO, SSIL and SDFGI are off; `control.tscn` ships them off. Otherwise you cannot tell texture AO from screen-space AO. The ambient light comes from the grey background colour.
2. **A/B the AO.** In the editor, open `materials/dutch_ship_medium_hull.tres`. Frame the hull in the 3D viewport and toggle *Ambient Occlusion* in the Inspector. Take a screenshot with it on and with it off, from the same camera. Look at plank seams, gun ports and fittings. Your prediction from question 1 says the difference is small. Write down whether you can see it at all, and where.
3. **Everything else unchanged.** The hull's colour, gloss, metal fittings and normal detail should look exactly as before the change. The rigging and sails should not change at all.
4. **The sails.** Look at the edge of each sail. Are they cut to a shape, or solid quads? Compare with the finding about the JPEG and alpha scissor, and record what you see. The headless evidence says no texel can be cut away; only your eyes can say whether that matters here.
5. **Import settings after the editor ran.** Close the editor and run `git status`. Any `.import` file that changed was rewritten by the editor's detection, which never runs headless. Read the diff before you commit. In the book's run these textures have `detect_3d/compress_to=0`, so none should change; if one did, find out why.

### Ship It

- **Commit.** Commit in the order the work happened: the agent's audit, your review corrections, the agent's change, your fix of the change. A reviewer should be able to see exactly which lines an agent wrote.
- **Attribution.** Add a credits file next to the asset (for example `godot/polyhaven/ATTRIBUTION.md`) with the name, the source URL, the three credited people and their roles, the licence, and the date you checked. The upstream demo ships none. CC0 does not require one; this course does.
- **FRICTIONAL entry.** Record which claims in the agent's audit you corrected and how you checked each, and what the A/B screenshots showed. Do not write "AO looks better" unless you compared the two images.
- **Brutalist skill.** `godot-gamedev` pairs a code or resource excerpt with the visible result it produces. Here the excerpt is the `.tres` and the `.import` change, and the visible result is your two screenshots.

### Verify

Reimport from an empty cache, so you know the external material survives a fresh import and not just a warm one. Delete the `godot/.godot` folder first; it is Godot's import cache.

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_materials.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://test_settings.gd --fixed-fps 60
```

Then prove the key assertion can fail: set `ao_enabled = false` in the `.tres`, rerun the materials test, and see it exit 1. Restore the file.

**What a pass proves:**

- After a fresh import the hull is the external `ORMMaterial3D` with AO on and the right textures.
- The rigging and sails keep their audited slots, channels, scalars and flags.
- Every import setting in the audit is what the files say.
- The normal maps pass the blue-channel plausibility check and the colour maps fail it.

**What it does not prove:**

- That the AO is visible.
- That the hull looks as it did apart from the AO.
- That the sails look right.
- That the ship looks like wood and iron.

## What we actually ran

**Date and tools.** 2026-09-27, Godot 4.7.2.stable.official.ed1daf0bf. Claude Code 2.1.150 ran with its default model `claude-sonnet-4-6`. Codex CLI 0.153.4 ran with the account's configured model `gpt-5.6-sol` at reasoning effort `low`. The starting point was `walker-3d-graphics-settings/godot`, identical to upstream `3d/graphics_settings` at `a3b5c11` apart from the title and `test_settings.gd`, copied into a scratch Git repository. The full record is in [`../examples/07-materials-and-textures/`](../examples/07-materials-and-textures/).

**Baseline.** Headless import exited 0 with no warnings or errors, and `test_settings.gd` reported 17 checks, 0 failures.

**Session 1 (Claude Code, audit).** 30 turns, about 10 minutes. The scoped permissions held: `godot --headless …` ran, and a plain `godot --version` was refused. The agent wrote a 167-line `MATERIALS.md` and a 238-line `test_materials.gd` that passed 95 checks. We ran the test ourselves (95 PASS), and changed one import setting (the hull normal map's `compress/normal_map` from 1 to 0) to confirm it fails (1 FAIL).

Four of its findings held up when checked:

- **F-1, AO unused.** Confirmed: all three imported materials report `ao_enabled=false`, and the glTF declares no occlusion texture.
- **F-2, sails cannot be cut out.** Confirmed: `Image.detect_alpha()` on the sails JPEG returns `ALPHA_NONE`, and the format is `FORMAT_RGB8`. The glTF even names that image `dutch_ship_medium_sails_diff-dutch_ship_medium_sails_alpha`, a trace of an alpha map that a JPEG could not carry.
- **F-3, Lossless imports for 3D textures.** True.
- **F-4, a mislabelled glTF image name.** True.

Four claims did not hold up, and were corrected in a separate commit:

- It named the environment's tonemapper "ACES Fitted" (`tonemap_mode = 4`). In Godot 4.7.2, 4 is `TONE_MAPPER_AGX`; ACES is 3.
- It said `compress/normal_map=1` stores the normal map "in two-channel RG normal format". Under Lossless, `get_image()` on the imported texture returns `FORMAT_RGB8` with mipmaps.
- It gave video-memory figures ("≈ 36 MB actual vs ≈ 4.5–9 MB") that nothing had measured.
- It reported dead code in `settings.gd` (F-5) and proposed shifting every branch of the model-quality handler by one. The UI offers four items (`item_count = 4`: Low, Medium, High, Ultra), the effective mapping already matches the labels, and the project's own `FRICTIONAL.md` had reached that conclusion the day before. The proposed "fix" would have mislabelled every option.

**Session 2 (Claude Code, the change), cut off.** After 23 turns and about 14 minutes, the session ended with `You've hit your session limit · resets 6:40pm (America/New_York)`. Other agents were sharing the account. The half-finished work was committed unedited. It contained:

- an `ORMMaterial3D` `.tres` with a UID typed by hand, `uid://b7r5mqhdf3j9k`;
- `_subresources` written as a flat key, `"materials/dutch_ship_medium_hull"`;
- an updated test, and a scratch `diag.gd`.

The agent's own updated test failed 4 checks, including `hull material is ORMMaterial3D (external tres)`. The probe showed why: the hull was still the importer's internal `StandardMaterial3D`. The 4.7.2 scene importer reads `subresources["materials"]`, a nested dictionary, so the flat key was ignored.

**Session 2b (Codex, same task with a handoff paragraph).** Twenty shell commands. Codex:

- rewrote `_subresources` as a nested `"materials": {"dutch_ship_medium_hull": {…}}` with `use_external/path` set to `uid://b7r5mqhdf3kak` and a `fallback_path`;
- deleted cached `.scn` files under `godot/.godot/imported/` to force reimports;
- at one point searched the Godot binary with `strings` for the importer's key names;
- deleted `diag.gd`.

Its test reported 100 checks, 0 failures, and its summary said "ARM channels now map as R=AO".

The two UIDs are the same resource. Godot's UID alphabet is `a`–`y` and `0`–`8` (`core/io/resource_uid.cpp`), and the decoder is lenient: the hand-typed `…j9k` contains a `9`, which carries into `…kak`. Godot accepted it and reported the canonical spelling. An agent typing UIDs by hand produces strings Godot did not generate; here it happened to work.

**The error neither agent caught.** Loading the result headless showed the hull as `ORMMaterial3D`, path `res://materials/dutch_ship_medium_hull.tres`, and `ao_enabled=false`. Trimmed from `logs/codex-state-probe_hull.log`:

```text
dutch_ship_medium_hull class=ORMMaterial3D path=res://materials/dutch_ship_medium_hull.tres ao_enabled=false metallic=1.0 roughness=1.0 cull=2 transparency=0
   orm_texture=res://polyhaven/textures/dutch_ship_medium_hull_arm_1k.jpg ao_texture=none
```

Godot's generated shader code reads the ORM red channel for AO only when the AO feature is on (`scene/resources/material.cpp`). So the change that existed to add AO added none.

Codex's test passed because it asserted that the ORM texture was bound and that `ao_texture_channel` was red. Neither property turns AO on. Its comment, "ORMMaterial3D always maps its orm_texture as R=AO", is what the source contradicts. The test also pinned `metallic_texture_channel` and `roughness_texture_channel` on the ORM material, two properties the ORM code path never reads. The `.tres` set them only so the test would pass.

**Our fix.** We added `ao_enabled = true` to the `.tres` and one assertion to the test, then:

- deleted `godot/.godot` and reimported from an empty cache;
- ran `test_materials.gd`: 101 PASS, 0 FAIL;
- ran `test_settings.gd`: 17 checks, 0 failures;
- ran the probe: hull `ORMMaterial3D`, `ao_enabled=true`, orm texture `dutch_ship_medium_hull_arm_1k.jpg`; rigging and sails still importer `StandardMaterial3D`s with their audited values;
- mutated `ao_enabled = false`: 1 FAIL, `hull ao_enabled = true (ORM red channel is read only when AO is on)`.

No texture `.import` file changed.

Put that next to Predict question 1. The effect was expected to be subtle, at most 17% of the ambient light on the hull. A student who opened the editor and saw almost no difference could easily have written "AO is subtle, as predicted" about a material in which AO was switched off. Here the machine check was the one that could tell "subtle" from "absent". Your eyes are still needed for everything after that.

**What we did not do.** No window was opened. None of the *Use It* checks was performed. We do not know from observation whether the AO is visible, whether the sails look wrong, or whether anything else about the hull changed.

## Check your understanding (ungraded)

1. In `MATERIALS.md`, find the row for `dutch_ship_medium_sails_arm_1k.jpg`. Using the pixel statistics in `../examples/07-materials-and-textures/logs/probe_pixels.log`, explain why its blue channel is consistent with the sails' `metallicFactor: 0`.
2. Set the imported hull material's metallic scalar to 0.5 in a `StandardMaterial3D` copy, then convert it to `ORMMaterial3D`. Which line of `material.cpp` tells you what will change, and what will the metal fittings look like?
3. Replace `hint_normal` with `source_color` on a normal-map uniform in a small spatial shader, and render a flat plane lit from straight above in the editor. Compare the brightness with the chapter's figure of 0.779. What would you need to control to make that comparison fair?
4. `walker-3d-decals` puts `paint_normal.png` in a decal's normal slot, and its `.import` has `process/normal_map_invert_y=true`. What does that setting assume about how the image was authored, and how would you check it?
5. Your agent adds a new texture to a material by editing a `.tscn`. List the three `.import` settings you would read before committing, and say what each should be for an albedo, a normal map and an ORM texture in 3D.
6. Explain, citing the glTF 2.0 occlusion rule and Godot's `ao_light_affect` default, why AO did nothing visible in a scene lit only by a directional light.

## Doing the same thing in Unity

*Unity was not run for this chapter. This comparison comes from Unity's documentation (Unity 6.6 manual, and the HDRP 17.3 and URP package manuals), checked on 2026-09-27.*

### Similarities

- **Same model, same kinds of texture.** URP's Lit shader takes a Base Map, a Metallic Map, a Normal Map and an Occlusion Map, and can read "a single RGBA texture for the metallic, smoothness, and occlusion properties".
- **Import settings are text beside the asset.** Unity creates a `.meta` file for every asset, and it "contain[s] the unique ID assigned to the asset, and values for all the asset's import settings". An agent can read and diff it the way it reads Godot's `.import`.
- **An audit can run headless.** The `TextureImporter` API exposes `textureType`, `sRGBTexture` ("whether this texture stores data in sRGB (also called gamma) color space"), `mipmapEnabled` and `textureCompression`. An EditMode test under `-batchmode` can assert them, as `test_materials.gd` asserts the `.import` values.

### Differences

- **Colour versus data is an import checkbox.** In Unity you declare it per texture ("sRGB (Color Texture)"). In Godot it follows from the slot, or from a shader hint.
- **The packing differs.** HDRP's mask map packs Red = Metallic, Green = Ambient Occlusion, Blue = Detail mask, Alpha = Smoothness. Its manual says to "disable sRGB (Color Texture)" and set Texture Type to Default when importing one. Smoothness runs the opposite way to roughness, and the channel order is not Godot's R = AO, G = roughness, B = metallic. A Poly Haven `arm` file cannot be dropped into an HDRP mask slot. It must be repacked, and the roughness channel inverted.
- **URP differs again.** URP's Lit shader reads smoothness from the Metallic map's alpha or the albedo's alpha.
- **Asset identity.** Unity's GUIDs live in `.meta` files. Godot's UIDs live in `.uid` files and inside `.import` and resource headers. An agent that invents either is guessing.

| Godot 4.7 | Unity 6.6 |
|---|---|
| `StandardMaterial3D` / `ORMMaterial3D` | URP Lit / HDRP Lit material |
| ORM texture: R AO, G roughness, B metallic | HDRP mask map: R metallic, G AO, B detail, A smoothness |
| slot or `source_color` decides colour vs data | per-texture "sRGB (Color Texture)" import setting |
| `.import` file | `.meta` file (import settings + GUID) |
| `compress/mode`, `mipmaps/generate` | `textureCompression`, `mipmapEnabled` |
| headless `test_materials.gd` | EditMode test using `TextureImporter` |

## Doing the same thing in Unreal Engine

*Unreal Engine was not run for this chapter. This comparison comes from Epic's documentation for Unreal Engine 5.8 and the Unreal Python 5.8 API, checked on 2026-09-27.*

### Similarities

- **The same quantities.** A material's main node takes Base Color, Metallic, Roughness, Normal and Ambient Occlusion inputs. Ambient Occlusion is "used to help simulate the self-shadowing that happens within the crevices of a surface".
- **Packed masks.** Several masks in one texture is standard practice. Epic's texture-masking guide says to "uncheck sRGB in the Texture Editor, as masks should not be gamma corrected".
- **Scriptable audit.** Editor Python exposes each texture's `srgb`, `compression_settings` (including `TC_NORMALMAP` and `TC_MASKS`) and `mip_gen_settings`, so an audit like this chapter's can be scripted.

### Differences

- **Unreal refuses what Godot accepts.** If you turn sRGB off on a texture already used in a material, "the sample type is not automatically updated in existing 2D Texture Sampler nodes", and unless you change it from Color to Linear Color, "your Material will fail to compile". Godot's equivalent mistake, a wrong or missing hint, compiles and silently decodes the data wrong.
- **AO can be silently ignored.** Epic's material-inputs page says the Ambient Occlusion input relies on light sources with Static or Stationary mobility, and is "silently ignored when its Material is used in conjunction with any Movable light sources". In Godot, AO affects ambient light and, through `ao_light_affect`, can be allowed to affect direct light. Both engines can leave a correct-looking AO texture with no visible effect.
- **Default global illumination.** Lumen is "the default global illumination and reflections system". Godot's defaults leave SDFGI, SSIL and SSAO off in this demo.
- **Assets are binary.** Materials and textures are `.uasset` files, so the audit must go through the editor.

| Godot 4.7 | Unreal Engine 5.8 |
|---|---|
| `ORMMaterial3D` | Material with a packed mask texture sampled as Linear Color / Masks |
| `hint_normal` / normal slot | Compression Settings `TC_NORMALMAP`; Normal sampler type |
| `source_color` | texture `srgb` flag and Color sampler type |
| `.import` text | texture `.uasset` properties, via Editor Python |
| SDFGI / VoxelGI / LightmapGI | Lumen (default), baked lighting |
| `Decal` (Forward+ and Mobile only) | Decal actors with a deferred-decal material |

## Sources

Godot (official documentation, 4.7, and source at the 4.7.2 commit):

- Standard Material 3D and ORM Material 3D — https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html
- BaseMaterial3D class — https://docs.godotengine.org/en/stable/classes/class_basematerial3d.html
- ORMMaterial3D class — https://docs.godotengine.org/en/stable/classes/class_ormmaterial3d.html
- Importing images — https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html
- ResourceImporterTexture class — https://docs.godotengine.org/en/stable/classes/class_resourceimportertexture.html
- Advanced Import Settings (Use External, Extract Materials) — https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/advanced_import_settings.html
- Shading language (source_color, hint_normal) — https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html
- Using decals — https://docs.godotengine.org/en/stable/tutorials/3d/using_decals.html
- Introduction to global illumination — https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/introduction_to_global_illumination.html
- Godot source at `ed1daf0bf001b61586d9930840f2f1394092c079`: `scene/resources/material.cpp`, `editor/import/resource_importer_texture.cpp`, `editor/import/3d/resource_importer_scene.cpp`, `core/io/resource_uid.cpp` — https://github.com/godotengine/godot
- Godot demo projects, commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` (`3d/graphics_settings`, `3d/decals`, `3d/global_illumination`, `compute/texture`, `compute/heightmap`), MIT — https://github.com/godotengine/godot-demo-projects

Formats and assets:

- glTF 2.0 specification (material textures) — https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
- Poly Haven, Dutch Ship Medium — https://polyhaven.com/a/dutch_ship_medium and https://api.polyhaven.com/info/dutch_ship_medium
- Poly Haven licence — https://polyhaven.com/license
- Poly Haven texture requirements ("normal (OpenGL standard)") — https://docs.polyhaven.com/en/technical-standards/textures

Walker:

- walker-3d-graphics-settings, walker-3d-decals, walker-3d-global-illumination, walker-compute-texture, walker-compute-heightmap — public adaptations at `github.com/nikbearbrown/<name>`; `README.md` and `FRICTIONAL.md` of each
- This chapter's record — `../examples/07-materials-and-textures/`

Agents:

- Claude Code, "How Claude remembers your project" — https://code.claude.com/docs/en/memory
- Codex, "Custom instructions with AGENTS.md" — https://learn.chatgpt.com/docs/agent-configuration/agents-md

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 2026-09-27:

- Unity asset metadata (`.meta`) — https://docs.unity3d.com/Manual/AssetMetadata.html
- `TextureImporter` — https://docs.unity3d.com/ScriptReference/TextureImporter.html
- URP Lit shader — https://docs.unity3d.com/6000.5/Documentation/Manual/urp/lit-shader.html
- HDRP mask and detail maps — https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.3/manual/Mask-Map-and-Detail-Map.html
- Unreal material inputs — https://dev.epicgames.com/documentation/en-us/unreal-engine/material-inputs-in-unreal-engine
- Using texture masks in Unreal Engine — https://dev.epicgames.com/documentation/en-us/unreal-engine/using-texture-masks-in-unreal-engine
- Unreal Python `Texture` and `TextureCompressionSettings` — https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/Texture and https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/TextureCompressionSettings
- Lumen global illumination and reflections — https://dev.epicgames.com/documentation/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine
- Working with assets (`.uasset`) — https://dev.epicgames.com/documentation/en-us/unreal-engine/working-with-assets-in-unreal-engine
- Decal materials (Deferred Decal material domain) — https://dev.epicgames.com/documentation/en-us/unreal-engine/decal-materials-in-unreal-engine
