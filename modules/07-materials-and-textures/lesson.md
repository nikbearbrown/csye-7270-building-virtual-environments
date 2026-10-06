# Module 7 — Materials and textures

CSYE 7270 · Fall 2026 · Week 7

## Executive summary

A 3D material is a stack of textures and numbers. Each texture leads two lives: how Godot imports it (compression, mipmaps, whether it is a normal map) and which material slot and colour channel reads it. This module explains both using Godot 4.7.2's `StandardMaterial3D`, `ORMMaterial3D` and texture importer, plus the lighting settings that decide what a material shows. You direct Claude Code to audit the three materials and nine textures of a Poly Haven ship, then to make one change: give the hull the ambient occlusion (AO) its textures already carry. Headless checks (run with no window) cover the slots, channels, scalars and import settings, whether the normal maps really are normal maps, and whether the hull ends with an external `ORMMaterial3D`, a material that reads roughness, metalness and AO from one packed texture, with AO switched on. They cannot show whether the ship looks better, or like wood and iron at all; that judgement is yours, made in the running scene.

## The question

The ship's textures come in threes per part: `diff`, `nor_gl` and `arm`. The `arm` file packs ambient occlusion, roughness and metalness into its red, green and blue channels. Load the ship headless, though, and all three imported materials report `ao_enabled=false`. None of the three glTF materials declares an occlusion texture, so the red channel of every `arm` file is imported, uploaded and never read.

The sails are set to alpha scissor at 0.5, but their colour texture is a JPEG, reported as `FORMAT_RGB8` with no alpha. All nine textures are imported Lossless, the mode Godot's documentation describes for 2D assets, and the "Detect 3D" setting that would fix that is off.

None of this shows in a screenshot at a glance, and all of it shows in text files an agent can read. So: **what can an agent establish about a material by reading and running it headlessly, what does it get wrong while doing so, and what is left for you to judge by looking?**

## The ideas

### A PBR material is a set of measurements, not a picture

Godot's 3D materials use the metallic-roughness model that glTF 2.0 also uses. A surface is described per pixel by a few quantities: **base colour** (what it reflects), **metallic**, **roughness** (how blurred reflections are), **normal** (which way the surface faces at a detail smaller than the mesh) and **ambient occlusion** (how much surrounding light reaches a crevice). A light and a camera turn those into a colour, so judging a material is always judging it under stated lighting. Only base colour is a colour; the rest are data stored in an image file.

The [glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html), the format the ship arrives in, fixes the encoding for each texture:

| Texture | glTF 2.0 rule (paraphrased) |
|---|---|
| Base colour | 8-bit sRGB-encoded values, decoded to linear before use |
| Metallic-roughness | Roughness in green, metalness in blue, linear encoding |
| Normal | Linear encoding; red, green, blue map to X, Y, Z; blue should be above 0.5 |
| Occlusion | Red channel; affects indirect (ambient) lighting only, not direct light |

### Colour versus data: why the decode matters

An 8-bit texel stores 0 to 255. For a colour, that number is sRGB-encoded and the renderer decodes it to linear before lighting. For data, the number is the value, and decoding it as sRGB corrupts it. In a custom shader you choose the decode with a hint: Godot's [shading language reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html) requires `source_color` for sRGB colour data and offers `hint_normal` for normal maps.

The size of the error is easy to compute. A perfectly flat normal-map texel is (128, 128, 255). Read linearly, 128/255 is 0.502, which unpacks with `2c - 1` to (0.004, 0.004, 1.0): flat. Decoded as sRGB, 0.502 becomes 0.216, which unpacks to (-0.568, -0.568, 1.0). Normalised, that surface is tilted 38.8 degrees from where it faces, and a light shining straight along the true normal lights it at N·L = 0.779 instead of 1.0, 22% too dark and lopsided. The data and the file were right; one word in a uniform declaration made the lighting wrong. Module 8 turns this into a review check.

### StandardMaterial3D, ORMMaterial3D, ShaderMaterial

Godot gives you three ways to describe a 3D surface, covered in the [Standard Material 3D guide](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html). `StandardMaterial3D` has a texture slot per quantity and lets you pick which channel each reads. `ORMMaterial3D` uses one ORM texture whose channels serve each parameter. `ShaderMaterial` is Module 6's custom shader. Two details of the first two are not on the reference pages but are plain in the generated shader code (`scene/resources/material.cpp` at the 4.7.2 commit):

1. **ORM channel order and the AO switch.** The ORM path emits AO from red, roughness from green and metallic from blue, the same order as a Poly Haven `arm` file. But AO is emitted only when the AO feature (`ao_enabled`) is on. An `ORMMaterial3D` with an ORM texture and AO off uses the texture for roughness and metalness only.
2. **Scalars behave differently.** In `StandardMaterial3D` the scalar multiplies the texture. In `ORMMaterial3D` the texture channels are used directly and the `metallic` and `roughness` scalars do not enter. Converting preserves the look only when both scalars were 1.0, which they are for the ship, because glTF's default metallic factor is 1.0.

Other settings that change the look, from the [BaseMaterial3D reference](https://docs.godotengine.org/en/stable/classes/class_basematerial3d.html): `ao_light_affect` defaults to 0.0, so AO darkens ambient light, not direct light; `ALPHA_SCISSOR` cuts off values below a threshold and is cheaper than full alpha; and cull mode `Disabled` draws both sides of every triangle, which can cost performance.

### Texture import: the half an agent forgets

Every image has a `.import` file beside it, and that text file decides what reaches the GPU. The options that matter here, with the integers the file stores:

| Option | Values | Meaning |
|---|---|---|
| `compress/mode` | 0 Lossless, 1 Lossy, 2 VRAM Compressed, 3 VRAM Uncompressed, 4 Basis Universal | Lossless is the common 2D default; VRAM Compressed is the common 3D choice and cuts video memory by roughly 4 to 6 times ([Importing images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)). |
| `compress/normal_map` | 0 Detect, 1 Enable, 2 Disabled | Enable forces two-channel compression under VRAM compression; under Lossless, the hull's normal map imported as plain `FORMAT_RGB8`. |
| `mipmaps/generate` | true or false | Recommended in 3D; without them, distant surfaces shimmer. |
| `process/normal_map_invert_y` | true or false | Converts DirectX-style normal maps to the OpenGL style Godot requires. |
| `detect_3d/compress_to` | 0 Disabled, 1 VRAM Compressed, 2 Basis Universal | What to switch to when the texture is detected in 3D. |

**The detection trap.** "Detect 3D" and "Normal Map: Detect" sound like import-time analysis. They are not. The importer registers callbacks that the renderer calls when it draws a texture in a 3D material inside the editor, and only then does the editor rewrite the `.import` file. Headless, nothing is drawn: in this course's experiment, a scene using two decal textures was run headless, reimported and opened with `--headless --editor`, and both `.import` files stayed byte-identical. An agent that wires a texture into a material by editing text leaves its import settings as they were until someone opens the scene in a real editor.

### Decals, lighting and global illumination

A `Decal` node projects albedo, normal, ORM and emission textures onto the surfaces its box touches. The [decal guide](https://docs.godotengine.org/en/stable/tutorials/3d/using_decals.html) lists the limits to know before promising one in a design: Forward+ and Mobile renderers only, no Compatibility; no properties beyond those textures; no custom shaders.

An AO texture that only affects ambient light does nothing visible under a strong directional light, and a rough metal looks like plastic with nothing to reflect, so the lighting setup is part of the material test. The [global illumination overview](https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/introduction_to_global_illumination.html) compares ReflectionProbe, LightmapGI, VoxelGI, SDFGI and screen-space indirect lighting, whose renderer support differs. Screen-space AO (SSAO) is a separate post-process in the `Environment`; turn it off when you judge texture AO.

### Attribution is part of the material

A texture's licence travels with it. `walker-3d-decals` shows the range in one project: CC0, CC-BY 3.0 and CC-BY-SA 3.0, with a README that says to review licence obligations before distribution. CC-BY requires credit, CC-BY-SA adds share-alike terms on adaptations, and CC0 requires nothing. This course asks for provenance regardless: where the file came from, who made it, under which licence, and the date you checked. The same rule covers textures you prompt from an image model (Module 2). A generated "normal map" is a picture that looks like one; nothing guarantees its vectors are unit length or its blue channel is above 0.5, and this module's pixel check is the one to run on it.

## The Walker example: walker-3d-graphics-settings

[`walker-3d-graphics-settings`](https://github.com/nikbearbrown/walker-3d-graphics-settings) is a Walker adaptation of Godot's `3d/graphics_settings` demo (upstream MIT licence kept) in the public `godot-demo-projects` collection at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`. A recursive diff run for this course shows two changes against that commit: the project name, and a headless harness, `test_settings.gd`. The demo is a settings menu over a 3D scene with directional, omni and spot lights, a fog volume, a mirror, a reflective sphere, and the Poly Haven ship under `polyhaven/`. Its README says the renderer is Forward+.

Its own `FRICTIONAL.md` says 17 assertions pass, covering five slider endpoints and the show/hide button, and that headless stored settings are not pixel, renderer, performance or human verification. It lists the asset-specific licence audit as outstanding, and that is where this module starts.

The ship is "Dutch Ship Medium" from Poly Haven, CC0. Poly Haven's API credits James Ray Cock (model, textures, cleanup), Rico Cilliers (sails model, textures) and Nicolò Zubbini (original model), published 2022-05-25. The upstream demo ships it with no attribution file. Nine 1024 × 1024 JPEG textures sit in `polyhaven/textures/`.

Four more public Walker builds each demonstrate one idea above, all from the same upstream commit. [`walker-3d-decals`](https://github.com/nikbearbrown/walker-3d-decals) has four texture kinds and four assets under three licences (25 headless checks), and [`walker-3d-global-illumination`](https://github.com/nikbearbrown/walker-3d-global-illumination) has VoxelGI, SDFGI, LightmapGI and reflection probes (42 mode-state assertions); both leave GPU appearance unverified. [`walker-compute-texture`](https://github.com/nikbearbrown/walker-compute-texture) writes a texture every frame from a compute shader; its eleven headless checks found a script error when no RenderingDevice exists, and the ripple effect has not been seen on a GPU. [`walker-compute-heightmap`](https://github.com/nikbearbrown/walker-compute-heightmap) generates an island from noise; an arithmetic check found 54,757 out-of-range gradient indices among 262,144 pixels, fixed with a clamp. A texture a shader writes is still a texture, and the boundary holds: arithmetic can be checked headless, the image cannot.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

1. The hull's `arm` texture has a red channel between 0.827 and 1.0, with a mean of 0.99 (a headless pixel probe measured this). If AO only darkens ambient light, how visible will the change be, and under what lighting would you see it?
2. The imported hull material has metallic and roughness scalars of 1.0. If you convert it to `ORMMaterial3D`, what happens to those scalars? What would have to be true for the conversion to change the look?
3. An agent wires a texture into a new material by editing text and never opens the editor. What happens to that texture's import settings?
4. The sails use alpha scissor at 0.5, and their colour texture is a JPEG. What do you expect at the edges of each sail?

### 2. Build It

Get the demo at the exact commit. A sparse, blobless clone keeps the download small, since only one demo folder is needed. These commands were not run for this module; the run used the local Walker adaptation of that commit.

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

Copy `3d/graphics_settings` into a folder of your own as `godot/`, run `git init`, and commit it as your baseline. The public Walker repository already has the same `godot/` layout with `test_settings.gd` in it; if you started from upstream, copy [`test_settings.gd`](../../examples/07-materials-and-textures/tests/test_settings.gd) into `godot/`. As in Module 6, test commands are wrapped in `timeout 120` so a script error cannot leave headless Godot running. Import and run the baseline:

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://test_settings.gd --fixed-fps 60
```

The baseline prints `RESULT 17 checks, 0 failures; headless state only, no pixel/performance proof`.

**Prompt 1: the audit.** Paste this into Claude Code. Check the attribution facts in it yourself on polyhaven.com first; the agent records them, it does not source them.

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

**Review the audit before you trust it.** Check every sentence in `MATERIALS.md` that names a value against the file or Godot. An enum written as an integer in a `.tscn` means nothing until you look it up (`Environment.TONE_MAPPER_AGX` is 4), a claim about what an import setting "stores" is checkable with `get_image().get_format()`, and a number of megabytes the agent did not measure should come out. Commit the agent's draft and your corrections separately.

**Prompt 2: the change.** Run it the same way, with Claude Code and the same flags as Prompt 1.

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

### 3. Use It

This is the only place the material is judged. Open `godot/project.godot` in the Godot 4.7.2 editor; the demo uses the Forward+ renderer. Every item is a **HUMAN CHECK**.

1. **Control the lighting.** HUMAN CHECK: run the project (F5) and, in the settings panel, confirm SSAO, SSIL and SDFGI are off; `control.tscn` ships them off. Otherwise you cannot tell texture AO from screen-space AO.
2. **A/B the AO.** HUMAN CHECK: open `materials/dutch_ship_medium_hull.tres`, frame the hull in the 3D viewport, and toggle *Ambient Occlusion* in the Inspector. Screenshot it on and off from the same camera, looking at plank seams, gun ports and fittings. Prediction 1 says the difference is small; write down whether you can see it at all, and where.
3. **Everything else unchanged.** HUMAN CHECK: the hull's colour, gloss, metal fittings and normal detail should look as before, and the rigging and sails should not change at all.
4. **The sails.** HUMAN CHECK: look at each sail's edge. Are they cut to a shape, or solid quads? The headless evidence says no texel can be cut away; only your eyes can say whether that matters here.
5. **Import settings after the editor ran.** Close the editor and run `git status`. Any `.import` file that changed was rewritten by the editor's detection, which never runs headless. Read the diff before committing; in the run these textures have `detect_3d/compress_to=0`, so none should change.

### 4. Ship It

- **Commit** in the order the work happened: the agent's audit, your review corrections, the agent's change, your fix of the change. A reviewer should see exactly which lines an agent wrote.
- **Attribution.** Add a credits file next to the asset, for example `godot/polyhaven/ATTRIBUTION.md`, with the name, source URL, the three credited people and roles, the licence, and the date you checked. The upstream demo ships none. CC0 does not require one; this course does.
- **FRICTIONAL entry.** Record which claims in the agent's audit you corrected and how you checked each, and what the A/B screenshots showed. Do not write "AO looks better" unless you compared the two images.
- **Brutalist skill.** `godot-gamedev` pairs a code or resource excerpt with the visible result it produces. Here the excerpt is the `.tres` and the `.import` change, and the visible result is your two screenshots. The skills come from the course-provided Brutalist checkout; if yours lacks one, ask for the update.

### 5. Verify

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

**What a pass proves:** after a fresh import the hull is the external `ORMMaterial3D` with AO on and the right textures; the rigging and sails keep their audited slots, channels, scalars and flags; every audited import setting is what the files say; and the normal maps pass the blue-channel plausibility check while the colour maps fail it.

**What it does not prove:** that the AO is visible, that the hull looks as it did apart from the AO, that the sails look right, or that the ship looks like wood and iron.

## What the agents got wrong

This record is from 27 September 2026: Claude Code 2.1.150 (default model `claude-sonnet-4-6`) and Codex CLI 0.153.4 (`gpt-5.6-sol`, reasoning effort `low`).

**The audit made four claims that did not hold.** Claude's `MATERIALS.md` found real problems (AO unused, sails that cannot be cut out, Lossless 3D imports), but it also named the tonemapper "ACES Fitted" when `tonemap_mode = 4` is AgX, said `compress/normal_map=1` stores a two-channel format when the Lossless import returns `FORMAT_RGB8`, gave video-memory figures nothing had measured, and proposed a menu "fix" that would have mislabelled every option. Checking each value against the file or Godot caught them.

**The first change used a key the importer ignores.** Claude's session was cut off by an account usage limit after 23 turns. Its partial work wrote the per-material setting as a flat key, but the 4.7.2 importer reads a nested dictionary, so the hull stayed an internal `StandardMaterial3D` and the agent's own test failed 4 checks.

**Codex finished the change, and the AO was still off.** Its test passed 100 checks and its summary said the ARM channels now map red to AO. The hull loaded as the external `ORMMaterial3D` with `ao_enabled=false`: the test asserted that the ORM texture was bound and the AO channel was red, and neither turns AO on. It had also pinned two channel properties the ORM code path never reads. A human added `ao_enabled = true` and one assertion, then confirmed by reimporting from an empty cache and by mutation.

**A hand-typed UID happened to work.** Claude Code typed the new material's resource UID itself; Godot's decoder is lenient, so it accepted the string and reported the canonical spelling. Strings an agent types by hand are not ones Godot generated.

## If you know Unity or Unreal

*Unity and Unreal were not run for this module; this comparison comes from their official documentation, checked on 27 September 2026.*

| Godot 4.7 | Unity 6.6 | Unreal Engine 5.8 |
|---|---|---|
| `StandardMaterial3D` / `ORMMaterial3D` | URP Lit / HDRP Lit material | Material with a packed mask texture |
| ORM texture: R AO, G roughness, B metallic | HDRP mask map: R metallic, G AO, B detail, A smoothness | Packed masks sampled as Linear Color |
| Slot or `source_color` decides colour versus data | Per-texture "sRGB (Color Texture)" setting | Texture `srgb` flag and sampler type |
| `.import` text file beside the asset | `.meta` text file beside the asset | Texture `.uasset` properties, read via Editor Python |
| `compress/mode`, `mipmaps/generate` | `textureCompression`, `mipmapEnabled` | `compression_settings`, `mip_gen_settings` |

The biggest difference for an agent workflow is where import settings live. Godot's `.import` and Unity's `.meta` are text files an agent can read, diff and assert in a headless test; Unreal textures are `.uasset` binaries, so the audit goes through the editor's Python API. The packing differs too: a Poly Haven `arm` file cannot drop into an HDRP mask slot without repacking and inverting roughness to smoothness. The [chapter](../../chapters/07-materials-and-textures.md) has the full comparison.

## Practice assessment (ungraded)

Answer these in your own words, then take the Canvas practice quiz for this module. Do not paste Claude's explanation as proof of your understanding.

1. All three imported ship materials report `ao_enabled=false`. Explain, using the glTF occlusion rule, why the AO in the `arm` textures was never used.
2. Codex's change passed 100 checks and added no AO. Which assertions gave false confidence, and which single assertion would have caught it?
3. A flat normal-map texel is sampled with `source_color`. Work out the tilt and the lighting error, and say what an agent should read to catch the mistake before rendering.
4. You add a texture to a material by editing a `.tscn`. Which three `.import` settings do you read before committing, and why will they not have changed on their own?
5. Why must you turn SSAO off before judging the hull's texture AO?

## The next step

This module completes Assignment 5, "A Shader and a Material That Say Something About Your Game", which covers Modules 6 and 7 and is due about Day 50. Module 6 covered the shader half; Module 8 turns to reviewing a shader change that looks right and is not. Read the companion chapter, [Chapter 7 — Materials and Textures](../../chapters/07-materials-and-textures.md), for the full run, the transcripts and the Unity and Unreal comparison.
