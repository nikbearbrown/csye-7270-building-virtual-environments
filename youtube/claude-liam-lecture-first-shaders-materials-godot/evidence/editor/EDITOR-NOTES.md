# EDITOR-NOTES: real Godot 4.7.2 editor frames for "first shaders and materials"

**What this is.** Real frames of the real Godot 4.7.2 editor, recorded by script, for the film's walkthrough of the shaders-and-materials assignment. The example is the instructor example in Bear's project `walker-claude` (AI-authored, never "hand-written"), opened as a scratch copy. Every frame is a native 3456x1944 PNG in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/captures/editor/`. Every label below was read from the driver's own dumps (`logs/*/states.json`), then checked against the frame by looking at it.

**Why.** SHOW-THE-THING: a tool is shown as itself. The film names the Shader Editor, the Inspector's shader-parameter groups, the Import dock and the Convert menu; each of these now exists as a real frame.

**Found.** All five wanted frames are DONE (F1 to F5), none is a reconstruction. Four things in the real editor differ from what a reader of the assignment would expect, and the film's wording has to follow the frames (section 3):

1. **The Inspector has no "Shader Parameters" group for this shader.** Because `surface.gdshader` uses `group_uniforms`, the uniforms sit in groups named **Surface** and **Pattern** directly under the Shader slot.
2. **The Import dock does not show a "Normal Map" row for these textures.** With Compress Mode **Lossless** (what both textures use) the Compress section holds only **Mode** and **Channel Pack**. The row **Normal Map** (Detect / Enable / Disabled) appears only when Compress Mode is **VRAM Compressed**. `compress/normal_map=2` is in the `.import` file, but the dock cannot show or set it in Lossless mode.
3. **"Convert to ShaderMaterial" is real** and is the last entry of the Material slot's dropdown menu, after Copy. It appears only when the slot holds a StandardMaterial3D.
4. **The StandardMaterial3D Inspector's category heading reads "BaseMaterial3D"**, not "StandardMaterial3D", and the three texture slots are all labelled just **Texture** (the group header, Albedo / Roughness / Normal Map, says which).

Nothing in Bear's project was opened, edited or saved. No audio, no video, nothing published.

---

## 1. Verdicts

All frames: 3456x1944, editor scale 200 %, Godot 4.7.2.stable.official (ed1daf0bf), Apple M4 Pro, **renderer `gl_compatibility`** (Bear's project setting; "OpenGL API 4.1 Metal - Compatibility" in `logs/*/run.log`). Window title in every frame: `conversion-scratch.tscn - walker-claude`. Single Window Mode on (popups drawn inside the window). Folder: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/captures/editor/` (called `CAP` below). Every frame has a 1920x1080 Lanczos downscale of the same PNG in `CAP/1920x1080/` (derived, not re-recorded; multiply boxes by 0.5556).

| Row | Verdict | Main file (in `CAP/`) |
|---|---|---|
| **F1** Shader Editor on standard_generated.gdshader, line numbers, lines 1 to 35, then the fragment function | **DONE** | `ed_F1a_shader-editor_standard-generated_lines-1-35.png`, `ed_F1b_shader-editor_standard-generated_fragment-lines-14-49.png` |
| **F2** Shader Editor on signal.gdshader, all 11 lines, cursor on line 10 | **DONE** | `ed_F2_shader-editor_signal_cursor-on-line-10.png` |
| **F3** Inspector of matte.tres, groups Surface and Pattern open, and coated.tres | **DONE** | `ed_F3a_inspector_matte-tres.png`, `ed_F3b_inspector_coated-tres.png` |
| **F4** Import dock for gate-color.png and gate-roughness.png | **DONE**, with the Normal Map difference (item 2 above) | `ed_F4a_import-dock_gate-color-png.png`, `ed_F4b_import-dock_gate-roughness-png.png` (+ tall variants F4c to F4f, extra F4x) |
| **F5** standard-source.tres Inspector, then the menu holding "Convert to ShaderMaterial" | **DONE**, menu recorded OPEN | `ed_F5a...folded.png`, `ed_F5b...unfolded.png`, `ed_F5d_inspector_material-override-menu-open_convert-to-shadermaterial.png`, `ed_F5e...highlighted.png` |

Full file names (every one is `CAP/<name>.png`; crops are `CAP/<name>.crop-<tag>.png`):

- `ed_F1a_shader-editor_standard-generated_lines-1-35`
- `ed_F1b_shader-editor_standard-generated_fragment-lines-14-49`
- `ed_F2_shader-editor_signal_cursor-on-line-10`
- `ed_F3a_inspector_matte-tres`
- `ed_F3b_inspector_coated-tres`
- `ed_F3x_EXTRA_inspector_matte-tres_forward-plus` and `ed_F3y_EXTRA_inspector_coated-tres_forward-plus` (extras, section 4)
- `ed_F4a_import-dock_gate-color-png`
- `ed_F4b_import-dock_gate-roughness-png`
- `ed_F4c_import-dock-tall_gate-color-png_top`
- `ed_F4d_import-dock-tall_gate-color-png_scrolled-to-bottom`
- `ed_F4e_import-dock-tall_gate-roughness-png_top`
- `ed_F4f_import-dock-tall_gate-roughness-png_scrolled-to-bottom`
- `ed_F4x_EXTRA_import-dock_pending-VRAM-Compressed-shows-Normal-Map-row`
- `ed_F5a_inspector_standard-source-tres_groups-folded`
- `ed_F5b_inspector_standard-source-tres_albedo-roughness-normal-unfolded`
- `ed_F5c_inspector_mesh-material-override-slot_standard-material`
- `ed_F5d_inspector_material-override-menu-open_convert-to-shadermaterial`
- `ed_F5e_inspector_material-override-menu_convert-entry-highlighted`

Every frame passed the settle test, and I looked at each one. F3, F4, F5 and the extras: the marked frame is pixel-identical to the same state 25 frames later and to the next frame (F5d is the later twin, see trap 7). F1a: identical to the same state 63 frames later and to the next frame. F1b and F2: identical to the next frame (no later twin was recorded).

---

## 2. What is on screen, frame by frame (labels read from the dumps)

### F1: the shader Godot wrote (standard_generated.gdshader)

How it was framed: the Shader Editor is a bottom panel (tabs **Output**, **Debugger**, **Audio**, **Animation**, **Shader Editor**; version label **4.7.2.stable**). At its default height it shows only 9 lines and clips the two long lines (failed attempt, `failed/F1_attempt1...png`). So the driver pressed the panel's expand button (a scripted click) and the editor's own **Toggle Files Panel** button to hide the file list. The 3D viewport is covered while the panel is expanded.

- Menus above the code: **File**, **Edit**, **Search**, **Go To**; at the right **Online Docs**. Below the code: **100 %**, a line:column readout (`1 : 1` in F1a, `31 : 1` in F1b), **Tabs**.
- Gutters: line numbers, a fold arrow beside `void vertex() {` (line 27) and `void fragment() {` (line 31), and a breakpoint/bookmark gutter.
- **F1a**: lines **1 to 35** fully visible (line 36 is the blank line below). Line 1 `// NOTE: Shader automatically converted from Godot Engine 4.7.2.stable's StandardMaterial3D.`; line 3 `shader_type spatial;`; line 4 `render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;`; lines 6 to 9 the albedo uniforms (`uniform vec4 albedo : source_color;` ... `uniform float point_size : hint_range(0.1, 128.0, 0.1);`); 11 to 14 roughness/metallic-texture uniforms; 16, 17 specular and metallic; 19, 20 `texture_normal`, `normal_scale`; 22 to 25 `uv1_*`, `uv2_*`; 27 `void vertex() {`; 31 `void fragment() {`; 35 `ALBEDO = albedo.rgb * albedo_tex.rgb;`. Caret on line 1, steady (blink turned off in the script so the frame is stable).
- **F1b**: lines **14 to 49** visible, caret on line **31** (`void fragment() {`, highlighted band). The whole fragment function, lines **31 to 48**, is visible: 32 `vec2 base_uv = UV;`; 34 and 35 the albedo lines; 37 to 39 metallic and `SPECULAR = specular;`; 41 to 43 roughness (`ROUGHNESS = roughness_tex * roughness;`); 45 `// Normal Map: Enabled`; 46 `NORMAL_MAP = texture(texture_normal, base_uv).rgb;`; 47 `NORMAL_MAP_DEPTH = normal_scale;`; 48 `}`.
- **Difference from the assignment/film wording:** the file is **48 lines** (`wc -l`), but the editor numbers a 49th, empty line (the trailing newline), visible at the bottom of F1b. Say "48 lines". The editor cannot scroll past the end, so "first visible line 26" clamped to 14; there is no frame with the fragment function alone at the top.
- Right dock in these frames is the Inspector on the shader resource: `standard_generated.gd...` (truncated), categories **Resource**, **RefCounted**, **Script** `<empty>`, **Add Metadata**. It is not informative; crop it away (see boxes).
- This is the **saved file** in Bear's repo (the 48 lines Godot generated earlier). I did not press Convert in this session.

### F2: the pad shader (signal.gdshader)

How it was framed: normal layout (3D viewport above, grid and sphere), bottom panel raised 341 px by a scripted drag of the split bar so 17 lines fit. The file list on the left of the panel shows the one open file **signal.gdshader**.

- All 11 lines are visible, plus line 12, the empty line from the trailing newline. Line 1 `shader_type spatial;`; 2 `render_mode unshaded;`; 3 `uniform float activation : hint_range(0.0, 1.0) = 0.0;`; 4 `uniform vec4 quiet_color : source_color = vec4(0.40, 0.16, 0.09, 1.0);`; 5 `uniform vec4 active_color : source_color = vec4(0.12, 0.72, 0.52, 1.0);`; 6 `uniform float stripe_count : hint_range(1.0, 16.0, 1.0) = 8.0;`; 7 `void fragment() {`; 8 `float stripe = step(0.5, fract(UV.x * stripe_count));`; 9 `vec3 base = quiet_color.rgb * mix(0.65, 1.0, stripe);`; **10 `ALBEDO = mix(base, active_color.rgb, activation);`** (the colour line); 11 `}`.
- Cursor on **line 10**: the highlighted band and the caret are on line 10 and the readout says **`10 : 1`**.

### F3: Inspector of the two materials

Layout: the right dock widened by script from 560 to **900 px** so the labels are not cut ("Roughness Gain" showed as "Roughness G" at the default width: `failed/F3_attempt1...png`). Inspector header: **matte.tres** / **coated.tres**, preview sphere on a checkerboard, class header **ShaderMaterial**.

Rows, top to bottom (identical in both frames): **Shader** `surface.gdshader` (with a link icon and the resource dropdown); group **Surface** (open): **Color Map** (thumbnail of gate-color.png, striped teal), **Roughness Map** (thumbnail of gate-roughness.png, grey stripes), **Tint** (colour swatch), **Roughness Gain** (number with slider bar); group **Pattern** (open): **UV Scale**, **Metallic Gain**; category **Material**: **Render Priority** `0`, **Next Pass** `<empty>`; category **Resource**, a folded group **Resource** "(1 change)"; category **RefCounted**: **Script** `<empty>`; **Add Metadata**.

| Row | matte.tres | coated.tres |
|---|---|---|
| Tint | white swatch, (1, 1, 1, 1), no revert arrow | green swatch, (0.45, 0.95, 0.72, 1), revert arrow |
| Roughness Gain | **0.9** | **0.25** |
| UV Scale | **1.0** | **2.0** |
| Metallic Gain | **0.0** | **0.4** |

The two sampler rows show a 128 px thumbnail, not a bare slot. Matches the files' values and `MATERIALS.md` (matte: tint white, roughness .9, scale 1, metallic 0; coated: tint (.45,.95,.72), .25, 2, .4). The preview sphere is rendered by the Compatibility renderer here (the Forward+ look is in the extras, section 4).

### F4: the Import dock

Layout: the left dock widened from 560 to **760 px** so "sRGB Friendly" is not cut; the Import tab is selected next to **Scene**; the FileSystem dock below shows the selected file (path `res://course-series/material-textures/...`; `gate-color.png` highlighted in F4a, `gate-roughness.png` in F4b). In F4a and F4b the driver moved the FileSystem tree's scroll bar so the tree starts at `course-series` (a first version showed the driver's `addons` folder row, which is not in Bear's project: kept in `failed/F4a_attempt2...png` and `failed/F4b_attempt2...png`).

Labels, top to bottom (identical for both files except the file name at the top): file name label (**gate-color.png** / **gate-roughness.png**); **Import As:** dropdown **Texture2D** and a **Preset** menu button; group **Compress**: **Mode** = **Lossless**, **Channel Pack** = **sRGB Friendly**; group **Mipmaps**: **Generate** = unticked (the box is labelled **On**); group **Roughness**: **Mode** = **Detect**, **Src Normal** = empty; group **Process**: sub-group **Channel Remap** (**Red**=Red, **Green**=Green, **Blue**=Blue, **Alpha**=Alpha), **Fix Alpha Border** ticked, **Premult Alpha**, **Normal Map Invert Y**, **HDR as sRGB**, **HDR Clamp Exposure** unticked, **Size Limit** 0; group **Detect 3D**: **Compress To** = **Disabled**; button **Reimport**.

- The `.import` files hold `compress/mode=0` (Lossless), `compress/normal_map=2` (Disabled), `mipmaps/generate=false`: Mode and Mipmaps are visible and match; **Normal Map is not shown** (see item 2 in "Found").
- F4a and F4b are the default dock height: they show Compress, Mipmaps, Roughness and the start of Process. F4c and F4e (dock made 1569 px tall by a scripted drag of the left split bar) show everything down to Size Limit and the **Detect 3D** header; F4d and F4f are the same dock scrolled to the bottom (down to **Compress To** = Disabled and **Reimport**). The FileSystem dock is squeezed to a strip in the tall frames.
- **F4x (EXTRA, not the file's state):** the Compress Mode dropdown was changed in the dock to **VRAM Compressed** (never pressed Reimport, the button reads **Reimport (\*)**). Then these rows appear: **High Quality**, **HDR Compression** (Opaque Only), **Normal Map** (options **Detect**, **Enable**, **Disabled**; shows **Disabled**), **Channel Pack**. This is the evidence for item 2; do not present it as the project's setting.

### F5: standard-source.tres and the Convert menu

- **F5a** (Inspector, right dock 900 px): header **standard-source.tres**; category heading **BaseMaterial3D** with groups folded: **Transparency**, **Shading**, **Vertex Color**, **Albedo** (2 changes), **Metallic** (1 change), **Roughness** (2 changes), **Emission** (On, unticked), **Normal Map** (1 change; **On** ticked, revert arrow), **Bent Normal Map**, **Rim**, **Clearcoat**, **Anisotropy**, **Ambient Occlusion**, **Height**, **Subsurf Scatter**, **Back Lighting**, **Refraction**, **Detail**, **UV1**, **UV2**, **Sampling**, **Shadows**, **Billboard**, **Grow**, **Transform**, **Proximity Fade** ... (the dump also lists a **StandardMaterial3D** category at the very bottom).
- **F5b**: Albedo, Roughness and Normal Map unfolded and scrolled to show them together: **Albedo**: **Color** (beige swatch, (0.85, 0.8, 0.7)), **Texture** (gate-color.png thumbnail), **Texture Force sRGB**, **Texture MSDF**; **Metallic** (1 change, folded); **Roughness**: **Roughness** 0.65, **Texture** (gate-roughness.png thumbnail), **Texture Channel** **Red**; **Emission**; **Normal Map** with its **On** box ticked: **Scale** 1.0, **Texture** (the purple-blue analytic-normal-gl.png thumbnail). Values from the dump: albedo (0.85, 0.8, 0.7, 1), metallic 0.2, roughness 0.65, normal scale 1.0.
- **F5c**: the scratch scene's `Sample` MeshInstance3D selected, its Inspector with group **Geometry** open: **Material Override** shows a StandardMaterial3D thumbnail with a cube icon.
- **F5d**: the Material Override slot's dropdown menu OPEN. Exact entries top to bottom: a **Search** box; heading **New**; **StandardMaterial3D**; **ORMMaterial3D**; **ShaderMaterial**; (divider); **Quick Load...**; **Load...**; **Edit**; **Clear**; **Make Unique**; **Make Unique (Recursive)**; **Save**; **Save As...**; (divider); **Show in FileSystem**; (divider); **Copy**; (divider); **Convert to ShaderMaterial** (item id 1000). There is no "Convert" anywhere else in this menu.
- **F5e**: the same menu with **Convert to ShaderMaterial** highlighted (the driver sets the real menu's hover highlight; no mouse pointer exists in these recordings).
- **How F5c to F5e were set up (disclose in the film notes):** the project's `conversion-scratch.tscn` already holds the converted ShaderMaterial in `Sample.material_override`, so the menu would not offer Convert there. In the scratch copy only, the driver assigned `standard-source.tres` to that slot in memory (`set_property`, `value_resource`) and opened the slot's menu. The scene was never saved. I did not press Convert. I did not open the Inspector header's "Extra resource options" menu, so I cannot say whether it also lists Convert.

---

## 3. What differs from the assignment or the film's likely wording

| The text may say | The real editor shows |
|---|---|
| uniforms are under "Shader Parameters" | for a shader with `group_uniforms`, groups **Surface** and **Pattern** directly under the Shader slot; there is no Shader Parameters group (the earlier editor-capture README saw that heading only for ungrouped uniforms) |
| set `compress/normal_map` in the Import dock (assignment: "set them rather than leaving them on Detect") | the dock offers **Normal Map** only in VRAM Compressed mode; in Lossless it is hidden. Lossless textures: Mode and Channel Pack only. The key `compress/normal_map` stays in the `.import` file |
| Normal Map "Detect" | the dropdown is **Detect / Enable / Disabled** (F4x); the files hold Disabled |
| the generated shader has line numbers "from line 1" | the file is 48 lines; the editor shows a blank line 49 |
| "StandardMaterial3D" heading | the Inspector's visible heading is **BaseMaterial3D** |
| a material's textures are "slots" | each is a 128 px thumbnail row, labelled Color Map / Roughness Map (ShaderMaterial) or just **Texture** (StandardMaterial3D, under a group header) |
| "Convert to ShaderMaterial" | real; last entry of the Material slot's menu; needs a StandardMaterial3D in the slot |
| the Roughness texture channel | **Texture Channel** = **Red** (a dropdown) |

Never write "hand-written" about these files: they are the instructor example.

Also in the frames and not Bear's project: the FileSystem dock's `addons` row (the driver's folder), `created` and `state_script.json` (driver artefacts). They are visible in the bottom-left of the full frames F1, F2, F3 and F5 (and F3x, F3y). In F4a and F4b the tree was scrolled past them; in F4c to F4f and F4x the FileSystem dock is squeezed to a strip showing only "Favorites". Use the crops below: none of them contains those rows. If a scene needs the FileSystem dock in a frame other than F4a/F4b, ask for a re-record with the tree scrolled (one short run).

---

## 4. Extras

- **F3 in Forward+ (extra):** `ed_F3x_EXTRA_inspector_matte-tres_forward-plus.png` and `ed_F3y_EXTRA_inspector_coated-tres_forward-plus.png`. The same two Inspector states recorded with `--renderer forward_plus` (log: `Metal 4.0 - Forward+ - Using Device #0: Apple - Apple M4 Pro`, `logs/f3fp/run.log`; 0 driver errors; same twin test). I compared them pixel by pixel with F3a/F3b: **the Inspector dock is identical** (no pixel in x >= 2548 differs by more than 30 levels), including the material preview sphere. Only the 3D viewport behind it differs (the sphere and grid render a little differently). So for the Inspector frames the renderer does not matter; the Compatibility frames are the ones to use because they are what Bear's project (`gl_compatibility`) shows. Values are identical to F3a/F3b (0.9, 1.0, 0.0 and 0.25, 2.0, 0.4; tint white and (0.45, 0.95, 0.72)).
- **F4x** is described above.

---

## 5. Pixel boxes (native frame, x,y,w,h)

All crops exist as `CAP/<name>.crop-<tag>.png`, cut from the same frame (never redrawn).

| Frame | Tag | Box x,y,w,h | What it holds |
|---|---|---|---|
| F1a, F1b | `panel` | 582, 99, 2292, 1757 | the whole expanded Shader Editor panel: menus, code, line numbers, status row |
| F1a, F1b | `code-only` | 582, 164, 2292, 1627 | the code and gutters only (the CodeEdit control) |
| F2 | `panel` | 582, 915, 2292, 941 | menus, file list `signal.gdshader`, the 11 lines, status row |
| F2 | `code-only` | 988, 980, 1886, 811 | the code and gutters (the CodeEdit control) |
| F3a, F3b | `dock` | 2548, 87, 900, 1849 | the whole Inspector dock |
| F3a, F3b | `material-block` | 2548, 200, 900, 1110 | preview sphere down to Metallic Gain |
| F3a, F3b | `shader-parameters-rows` | 2548, 640, 900, 670 | Shader row, Surface, Pattern, all six rows |
| F4a, F4b | `import-dock` | 8, 87, 760, 921 | the Import dock at default height |
| F4a, F4b | `left-column` | 8, 87, 760, 1849 | Import dock plus FileSystem dock (tree starts at `course-series`, the selected file highlighted at about y=1536 in F4a and y=1585 in F4b) |
| F3x, F3y (extras) | `dock`, `material-block` | 2548, 87, 900, 1849 and 2548, 200, 900, 1110 | the Forward+ twins of F3a, F3b |
| F4c, F4d, F4e, F4f, F4x | `import-dock` | 8, 87, 760, 1569 | the tall Import dock |
| F5a, F5b, F5c, F5d, F5e | `dock` | 2548, 87, 900, 1849 | the whole Inspector dock |
| F5c | `slot` | 2548, 760, 900, 260 | the Material Override slot |
| F5d, F5e | `menu` | 2910, 914, 498, 870 | the open menu only |
| F5d, F5e | `slot-and-menu` | 2548, 760, 900, 1050 | slot with the menu hanging below it |

Row boxes inside those frames (native pixels, from the dumps):

- **F3a, F3b** (dock x 2548): Shader row 2560,646,876,57; **Surface** header 2560,707,876,45; Color Map 2584,752,852,128; Roughness Map 2584,884,852,128; Tint 2584,1016,852,57; Roughness Gain 2584,1077,852,57; **Pattern** header 2560,1138,876,45; UV Scale 2584,1183,852,57; Metallic Gain 2584,1244,852,57; Material category rows Render Priority 2560,1378,876,57, Next Pass 2560,1439,876,57; preview sphere about 2548,366,900,204.
- **F4a, F4b, F4c, F4e** (scroll at top): file label 20,163,736,57; **Import As:** 20,228,736,57; Texture2D dropdown 20,293,611,65; **Compress** group 20,378,708,163 (Mode row 44,423,684,57; Channel Pack 44,484,684,57); **Mipmaps** 20,545,708,102 (Generate 44,590,684,57); **Roughness** 20,651,708,163 (Mode 44,696,684,57; Src Normal 44,757,684,57); **Process** 20,818,708,696; **Detect 3D** 20,1518,708,102 (Compress To 44,1563,684,57). In F4a/F4b only the top of the dock is visible (to about y=1008); in F4c/F4e the dock is visible to about y=1650. Reimport button: F4a/F4b 312,931,151,65.
- **F5b**: **Albedo** group 2560,387,848,356 (Color 2584,432,824,57; Texture 2584,493,824,128); **Metallic** header 2560,747,848,45; **Roughness** group 2560,796,848,295 (Roughness 2584,841,824,57; Texture 2584,902,824,128; Texture Channel 2584,1034,824,57); **Emission** header 2560,1095,848,45; **Normal Map** group 2560,1144,848,234 (Scale 2584,1189,824,57; Texture 2584,1250,824,128).
- **F5c, F5d, F5e**: Material Override row 2584,786,824,128; the menu's **Convert to ShaderMaterial** row (highlighted in F5e) about 2929,1719,460,46.
- **Code line centres:** F1a line n at y = 206 + 45.0 x (n - 1); F1b line n at y = 938 + 45.0 x (n - 31); F2 line n at y = 1023 + 45.0 x (n - 1) (about 3 px accuracy; line pitch 45 px).

---

## 6. Capture facts

Recorded with the existing driver (`/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/`) on a scratch copy at `/private/tmp/claude-501/a5-editor-capture/a5proj/` (the copy of `walker-claude/godot` without `.godot`, with the driver addon and its enabling line added). Settings file `editor_settings-single-window.tres`. Window set by the driver to 3456x1944; movie 3456x1944 at 30 fps; editor scale 200 %. 0 driver errors in every final run. The launcher took the Lab lock around every run (waited 0 s each time). The driver steps I added, with their diff, are in `plugin.gd.diff` and `COMMANDS.md`.

Every frame also shows two scene tabs, **main** (the project's own main scene, which the editor opens by itself) and **conversion-scratch**, and the Scene dock tree **ConversionScratch** > **Sample**; those are the scratch copy's real state.

Differences from a stock editor on a student's Mac, all inherited from the driver: Single Window Mode is on (stock: popups are separate windows); the macOS menu bar is outside the window and not recorded; no mouse pointer exists; caret blink is off in F1 and F2 (a steady caret); panels were resized by scripted drags and `dock_split`; Inspector folds were opened by the driver's `unfold` (what a click on the header does). Call these "scripted editor session" frames in any label, as the series rules already say.

Not tested: Forward+ for anything except the F3 extra; a non-English editor; Windows or Linux; the Inspector header's "Extra resource options" menu; pressing Convert, Save or Reimport (never pressed).

## 7. Traps hit (failed attempts are in `failed/`)

1. **Default Shader Editor height shows only 9 lines** and clips the long lines 1 and 4 (`failed/F1_attempt1...png`). Fixed by expanding the bottom panel and hiding the file list.
2. **`dock_split` with `offset` on the vertical bottom-panel split read back `-330` but moved nothing** (my first F2). Fixed with a scripted drag (`drag` step) of the split bar.
3. **`unfold_group` opens only the innermost section**; nested groups need every ancestor unfolded (new `unfold_sections`).
4. **Default Inspector width truncates labels** ("Roughness M", "Roughness G"): `failed/F3_attempt1...png`. Widened to 900 px.
5. **Unsettled previews:** the material preview sphere and the FileSystem thumbnails arrive late; three early frames were flagged "differs from the next frame" (`failed/F3_attempt2...`, `failed/F4_attempt1...`). Every kept frame has a twin 25 to 70 frames later that is pixel-identical.
6. **The Albedo header scrolled off the top** in my first F5b (`failed/F5_attempt1...png`); fixed with a bigger scroll margin.
7. **`open_picker_menu`**: the first marked frame, 45 frames after the press, did not show the menu while the dump said it was visible; the twin 25 frames later did. F5d is that twin. If a future run shows no menu, wait longer before the mark.
8. **The frame offset between `Engine.get_process_frames()` and the file index was 1 in some runs and 0 in others**; `extract_marks.py` finds it from the magenta flash and handles it.
9. **The FileSystem dock shows the driver's own folders** (`addons`, `created`) and `state_script.json`: not Bear's project. Fixed for F4a/F4b by scrolling the tree (new `scroll_tree` step). `Tree` has no scroll-bar accessor in 4.7.2, so the step finds the internal VScrollBar child. My first version of that step did not parse (`Cannot infer the type of "sb"`), the editor ran with the plugin disabled and the run produced no log: a 6-minute run lost; check `run.log` for `Parse Error` first when a run prints "NO states.json".
10. **A recording is 0.4 to 1.2 GB of frames** (3456x1944 PNG, 8 to 12 % of real time, 2 to 7 minutes a run): frames were deleted after extraction; only the marked PNGs and logs are kept.
