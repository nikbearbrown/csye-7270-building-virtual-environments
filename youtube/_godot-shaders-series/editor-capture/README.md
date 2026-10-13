# Editor capture: recording the real Godot 4.7.2 editor by script

**What this is.** A way to record Godot's own editor, with no human clicking, so a film can show real Inspector, dropdown, dialog and shader-editor frames. An `EditorPlugin` (the "driver") runs a JSON state script inside the real editor while Godot's Movie Maker records the editor window; a launcher takes the shared Lab lock around every run; a helper cuts one named PNG per `mark` step. Everything here was recorded on 2026-10-13 on this Mac (Apple M4 Pro, Godot 4.7.2.stable, Metal, Forward+), in a scratch project, never in a project Bear works in. Nothing was installed, published, paid for or sent.

**Why.** Eight editor rows in four films were waiting on "Godot's own editor" frames, and their fact-check rows were OPEN: the pilot's B10 click path and its B27 and B29 widgets (rows 14, 38, 39), the Drawing Shapes B44 sliders (row 69), the Local, World and Screen Space B11 Transform labels (row 23), and the Textures and Color B18, B34 and B40 menus (rows 52, 94, 107). The question was whether a script can choose what the Inspector shows, or whether Bear has to record it by hand.

**Found.** Yes: every one of those rows is recorded by script, 40 real editor states, each recorded twice (1920x1080 and the native 3456x1944), no human click. Dropdowns, the Create Shader dialog, the colour picker and the renderer menu are opened through the editor's own widgets and are recorded **only if the editor setting Single Window Mode is on** (with it off they are separate OS windows and Movie Maker does not see them; I tested both, and with it on, every frame without a popup in the two scripts I compared is pixel-identical to the default). The frames also **correct** several words the film text uses, quoted below: there is no "New ShaderMaterial" entry (the menu says **ShaderMaterial** under a heading **New**), the Shader slot's entry is **New Shader...**, the Create Shader dialog defaults to Mode **Spatial** (a Sprite2D shader needs **Canvas Item**), the uniform shows as **Red** not red, the clouds preview is not in the NoiseTexture2D view, and the renderer name is **hidden by default** in 4.7.2. A run takes 17 to 56 seconds; the Compatibility renderer does not change the editor's look.

---

## 1. Verdict for every editor row

Folders (1920x1080 stills; the same names exist under `png/3456x1944/`, native size, and as `.dock.png` crops of the whole right dock):

- `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/godot-shaders/`
- `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/drawing-shapes-with-math/`
- `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/local-world-and-screen-space/`
- `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/textures-and-color/`
- native: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/3456x1944/<same four folders>/`

| Row | Beat | Verdict | Frame files (in the folder above) |
|---|---|---|---|
| **Godot Shaders E1** | B10, four states of a Sprite2D's Inspector | **DONE**, all four, plus the click path | state 1 `godot-shaders_E1-1_material-empty.png`; state 2 `godot-shaders_E1-2b_shadermaterial-in-slot.png`; state 3 `godot-shaders_E1-3e_shader-in-slot-editor-closed.png` (the Shader slot lives inside the ShaderMaterial view, see 2.1); state 4 `godot-shaders_E1-4_shader-editor-open-after-Create.png`. Extras: `E1-2a_material-dropdown-open`, `E1-3a_inside-shadermaterial-shader-empty`, `E1-3b_shader-dropdown-open`, `E1-3c_create-shader-dialog-defaults`, `E1-3d_create-shader-dialog-filled` |
| **Godot Shaders E2** | B27, `red` at 0.2, 0.5, 0.9 | **DONE** | `godot-shaders_E2-2_red-0.2.png`, `godot-shaders_E2-3_red-0.5-after-0.2.png` (pixel-identical to `E2-1_red-0.5-default`), `godot-shaders_E2-4_red-0.9.png`; also `E2-0_inside-shadermaterial-group-collapsed` |
| **Godot Shaders E3** | evidence only, `source_color` | **DONE** | `godot-shaders_E3-1_source-color-swatch-next-to-red-slider.png`, `godot-shaders_E3-2_color-picker-popup-open.png` |
| **Drawing Shapes E1** | B44, three frames | **DONE** (two Inspector widths) | `drawing-shapes_E1-1_defaults-<width>.png`, `drawing-shapes_E1-2_dot_size-1.0-<width>.png`, `drawing-shapes_E1-3_ring_distance-0.2-<width>.png`, and `drawing-shapes_E1-3b_dot_size-1.0-and-ring_distance-0.2-<width>.png` (the plan's frame 3 is ambiguous: with or without dot_size 1.0 still set, so both are recorded). `<width>` is `default-width` or `wide-inspector` (the wide one reads "Ring Distance" in full) |
| Drawing Shapes E2 (optional) | B32, real shader-editor error | **DONE** | `drawing-shapes_E2_shader-editor-error-16-uv-inside-function.png` |
| **Local, World E1** | B11, child then parent | **DONE** (two scene shapes) | `local-world_E1-1_child-selected-clean-root.png`, `local-world_E1-2_parent-selected-clean-root.png`; and the plan-exact scene (root is Parent, the editor shows a warning triangle on a transformed root): `local-world_E1-1_child-selected-plan-exact-root-is-Parent.png`, `local-world_E1-2_parent-selected-plan-exact-root-is-Parent.png` |
| Local, World E2 (optional) | B14, real shader-editor error | **DONE** | `local-world_E2_shader-editor-error-04-broken-matrix-in-fragment.png` |
| **Textures and Color E1** | B18, three states | **DONE**, with one correction (2.7) | 1 `textures-and-color_E1-1a_noise_tex-slot-empty.png` and `E1-1b_noise_tex-dropdown-open.png`; 2 `E1-2a_noise_tex-holds-NoiseTexture2D.png`, `E1-2b_inside-NoiseTexture2D-noise-empty.png`, `E1-2c_noise-dropdown-open.png`; 3 `E1-3a_NoiseTexture2D-width-height-noise-FastNoiseLite.png` and `E1-3b_inside-FastNoiseLite-preview-clouds.png` |
| **Textures and Color E2** | B34, Picked and Typed | **DONE** | `textures-and-color_E2_picked-swatch-and-typed-four-boxes.png` |
| **Textures and Color E3** | B40, renderer name and its menu | **DONE**, needs one editor setting (2.9) | `textures-and-color_E3-1_renderer-name-upper-right.png`, `textures-and-color_E3-2_renderer-menu-open.png` |

PARTLY: none. NOT POSSIBLE by script: none. So there is no human recording script to write for these rows; section 9 gives an optional one for a visible mouse pointer.

What the frames cannot show: the real mouse pointer (Movie Maker draws the window, not the pointer). The hover highlight on a menu entry is real (the driver sets it on the real menu), but nothing moves a pointer. Label every clip "scripted editor session" in the film's `videoLabel`, as the series rules already say for scripted input.

On this Mac the colour picker also prints "Screen Recording permission missing!" at the bottom (the eyedropper needs a macOS permission). It is in `E3-2`; crop above that line or grant the permission to Godot before the master.

## 2. What the real frames confirm or correct (quote exactly)

Each item names the FACTCHECK row it answers. I did not edit any film file; these are the corrections to make.

### 2.1 Godot Shaders row 14 (B10): "Material slot, New ShaderMaterial; Shader slot, New Shader; Godot opens the shader editor"

Real path, in the frames:

1. Sprite2D selected. Inspector: category **CanvasItem** > group **Material** > row **Material** showing `<empty>` and a dropdown arrow. The **Material** group is folded until clicked (it opens by itself only when something in it differs from its default). Frame `E1-1`.
2. The arrow's menu (frame `E1-2a`, the entry **ShaderMaterial** highlighted): a heading **New**, then **CanvasItemMaterial**, **ShaderMaterial**, a divider, **Quick Load...**, **Load...**. **There is no entry called "New ShaderMaterial"**: the words are the heading plus the class name.
3. After choosing it (`E1-2b`) the slot shows a ShaderMaterial thumbnail. The Shader slot is **not** in the Sprite2D's Inspector. Click the thumbnail and the Inspector switches to the ShaderMaterial itself (back and forward arrows at its top), whose first row is **Shader** `<empty>` with a dropdown arrow (`E1-3a`).
4. That arrow's menu (`E1-3b`): **New Shader...** (with the ellipsis, no "New" heading), a divider, **Quick Load...**, **Load...**.
5. **New Shader...** opens a dialog titled **Create Shader** (`E1-3c`, `E1-3d`): **Type:** Shader, **Mode:** **Spatial** by default (entries: Spatial, Canvas Item, Particles, Sky, Fog, Texture Blit), **Template:** Default, **Built-in Shader:** off, **Path:** `res://scenes/e1_sprite.gdshader` (the scene's folder and name), two lines "Shader path/name is valid." and "Will create a new shader file.", buttons **Cancel** and **Create**. **A Sprite2D's shader needs Mode set to Canvas Item, or the file starts with `shader_type spatial;`.** The film does not say this.
6. **Create** writes the file, puts it in the Shader slot (`dial.g...` at the default width) and **the Shader Editor opens by itself** in the bottom panel (`E1-4`). The film's last clause is true.

Suggested wording for B10 (the film's, not mine to edit): "Open the node's Material slot, choose ShaderMaterial under New, click it, and in its Shader slot choose New Shader. Set the mode to Canvas Item, give it a name, and Godot opens the shader editor."

### 2.2 Godot Shaders row 38 (B27): "under Shader Parameters, there is a control named red"

The group header reads **Shader Parameters** (true). The control's on-screen label is **Red**, capitalised (the property is `shader_parameter/red`). The group is folded (`E2-0`) while every value is at its default; frames `E2-1` to `E2-4` are taken after the driver unfolded it (its `unfold()`, what a click on the header does). It opens by itself, when the Inspector is rebuilt, once a value differs from its default.

### 2.3 Godot Shaders row 39 (B29): "A range hint makes a slider; a source color hint makes a color picker"

- `uniform float red : hint_range(0.0, 1.0)` is a number box (`0.2`) with a thin slider bar under it; dragging it changes the value. It is one widget, not a separate slider. A revert arrow appears left of the box when the value differs from the default (`E2-2`, `E2-4`; absent at 0.5 in `E2-1`).
- `uniform vec4 tint : source_color` is a colour swatch button labelled **Tint** (`E3-1`). Clicking it opens the colour picker (`E3-2`): a colour wheel, a brightness bar, tabs **RGB**, **HSV**, **Linear**, sliders **R**, **G**, **B**, **I**, **A**, a **Hex** field, **Swatches**, **Recent Colors**. So "a color picker" is a swatch that opens a picker.

### 2.4 Drawing Shapes row 69 (B44): "six uniforms appear as six sliders in the real Inspector"

True. Under **Shader Parameters**: **Dot Size**, **Ring Distance**, **Ring Width**, **Arm Gap**, **Arm Length**, **Arm Width**, each a number box with a slider bar under it. The ShaderMaterial's preview thumbnail at the top shows the crosshair and changes with the values. At the default dock width "Ring Distance" is cut to "Ring Distanc" while its revert arrow is showing (`drawing-shapes_E1-3_ring_distance-0.2-default-width.png`); the wide variant reads it in full. The earlier planning frame `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-drawing-shapes-with-math/evidence/planning-checks/png/editor-inspector-check-2d.png` agrees with these labels.

### 2.5 Local, World and Screen Space row 23 (B11): "the editor's Inspector shows that relative value as Transform, Position"

True. Category **Node2D** > group **Transform** > **Position**, two fields labelled **x** and **y** with a `px` suffix (`50.0 px`, `0.0 px` for the Child; `500.0 px`, `300.0 px` for the Parent), then **Rotation** (degrees), **Scale** (x, y and a link toggle), **Skew**. The Transform group is folded by default and open when its values differ from the defaults, which both nodes' do. The Scene dock shows the tree **Scene** > **Parent** > **Child** (clean scene). If the root itself is the transformed Node2D (the plan's exact scene), the editor puts a warning triangle on it: "The root node of a scene is recommended to not be transformed, since instances of the scene will usually override this."

### 2.6 Drawing Shapes row B32 and Local, World B14 (optional E2 rows)

The shader editor shows the failing line highlighted in red and one line of text under the code. Drawing Shapes: **Error at line 3: Unknown identifier in expression: 'UV'.** Local, World: **Error at line 4: Unknown identifier in expression: 'MODEL_MATRIX'.** Same wording and line numbers as the engine log the films already quote.

### 2.7 Textures and Color row 52 (B18): "The Inspector's menu says New NoiseTexture2D and New FastNoiseLite"

Not as worded. On the **Noise Tex** slot (`E1-1b`): a **Search** box, a heading **New**, then bare class names (19 of them: ViewportTexture, CanvasTexture, CompressedTexture2D, PortableCompressedTexture2D, ImageTexture, AtlasTexture, MeshTexture, CurveTexture, CurveXYZTexture, GradientTexture1D, GradientTexture2D, CameraTexture, ExternalTexture, DrawableTexture2D, PlaceholderTexture2D, DPITexture, AnimatedTexture, Texture2DRD, **NoiseTexture2D**), a divider, **Quick Load...**, **Load...**. Inside the NoiseTexture2D (`E1-2c`), the **Noise** slot's menu is **New** > **FastNoiseLite**, then **Quick Load...**, **Load...**. No entry starts with the word "New"; "New" is the heading.

And the plan's frame (3), "the preview shows the grey clouds, with width and height visible", is **two Inspector views, not one**: the NoiseTexture2D view has **Width 512 px** and **Height 512 px** (and Generate Mipmaps, Noise, Color Ramp, Seamless, Invert, In 3D Space, As Normal Map, Normalize) but **no preview** (`E1-3a`); the grey clouds appear one click deeper, when the Inspector shows the **FastNoiseLite** itself (click its slot; `E1-3b`): a preview image with a **3D** button, **Noise Type** Simplex Smooth, **Seed** 0, **Frequency** 0.01, **Offset** x y z, groups **Fractal** and **Domain Warp**.

### 2.8 Textures and Color row 94 (B34): "a color picker for the hinted uniform and four number boxes for the plain one"

True (`textures-and-color_E2_picked-swatch-and-typed-four-boxes.png`): **Picked** is a colour swatch button, **Typed** is four number boxes labelled **x**, **y**, **z**, **w** (0.2, 0.4, 0.6, 1.0).

### 2.9 Textures and Color rows 106 and 107 (B40)

Row 107 is true: the menu lists **Forward+** (selected, radio), **Mobile**, **Compatibility** (`E3-2`). Row 106 ("the renderer's name sits in the upper right corner") is **only true when an editor setting is on**: in 4.7.2 the renderer selector is hidden by default (`interface/editor/appearance/show_renderer_selector` is `false` in a fresh editor's settings, and none of the other 38 frames shows it). With it on, the title bar's right end reads **Forward+** with a small arrow (`E3-1`). The setting is in Editor Settings under Interface, Editor, Appearance ("Show Renderer Selector" by the dialog's usual capitalisation; I did not open that dialog).

## 3. Answer to the coordinator's question: the two Textures and Color popup menus

**Both can be opened and recorded by script. Neither needs a human click.** One condition applies to all popups.

- **(a) The resource-picker menus** ("New NoiseTexture2D" / "New FastNoiseLite", three states): the driver presses the picker's own dropdown arrow, so the editor builds and shows its real menu; `pick_menu_item` then fires the real menu's `id_pressed`, exactly what a click on an entry does. All three states are recorded (`E1-1b`, `E1-2c` have the menu open; `E1-2a` and `E1-3a` hold the result). The menu stays open for about ten frames in these runs; the plan's "hold two seconds" is a still held in the cut, or add a `wait_frames` before the `mark` and re-run. See 2.7 for what the menu really says.
- **(b) The renderer menu** in the upper right: `open_option_button` calls `show_popup()` on the real renderer OptionButton. Recorded in `E3-2`, with **Mobile** highlighted. This button exists only when the editor setting `interface/editor/appearance/show_renderer_selector` is on (it is off by default, see 2.9). `settings/editor_settings-single-window-renderer-selector.tres` has it on.
- **The one condition:** popups are recorded only when the editor setting `interface/editor/display/single_window_mode` is `true` ("Single Window Mode"). With it off (the factory default) every dropdown and dialog is its own OS window, `PopupMenu.is_embedded()` is false, and Movie Maker records only the main window, so the frame shows no menu (probe: `logs/probes/probe1/named/P1-04-material-dropdown-open.png`, and the factory-settings comparison in `logs/compare/compare-results.txt`). With it on, the same menus are drawn inside the window and appear in the frames. Nothing else in the editor changes: frames without a popup are pixel-identical in both modes (section 6).
- Pushing a mouse event into the window at a control's rectangle also works (`click_control` and `click_at` use `Viewport.push_input`): it is how the colour swatch is clicked in `E3-2`. It was not needed for the two menus above. `Input.parse_input_event` was not tried.

## 4. The true on-screen labels (from the frames and the live Inspector)

| Question | Answer, with the frame |
|---|---|
| Group name above a ShaderMaterial's uniforms | **Shader Parameters** (`E2-2`, `E3-1`) |
| Widget for a `hint_range` float | a number box with a slider bar under it (`EditorPropertyFloat` with the slider), label **Red** (`E2-2`) |
| Widget for a `source_color` vec4 | a colour swatch button (`EditorPropertyColor`), label **Tint**; click opens the picker (`E3-1`, `E3-2`) |
| A plain vec4 | four number boxes **x y z w** (`textures-and-color_E2`) |
| Node2D position | **Node2D** > **Transform** > **Position** with **x** and **y**, `px` suffix (`local-world_E1-1`) |
| Material path on a Sprite2D | Inspector > **CanvasItem** > **Material** (group, folded by default) > **Material** (row; plus **Use Parent Material**) (`E1-1`) |
| Does the shader editor open as a bottom panel? | **Yes.** Bottom strip tabs: **Output**, **Debugger**, **Audio**, **Animation**, **Shader Editor** (and `4.7.2.stable` at the right end). Panel: a file list on the left (`dial.gdshader`), menus **File**, **Edit**, **Search**, **Go To**, **Online Docs** at the right, the code with line numbers, then `100 %`, `1 : 1`, `Tabs`; a compile error shows as one red line above that row (`E1-4`, `drawing-shapes_E2`) |
| Reading the Screen's prior-art labels | the same ColorRect Inspector lists **Anchors Preset** and, in the **Mouse** group, **Filter** (dump `colorrect-inspector` in `logs/probes/probe8a/states.json`), consistent with that film's `evidence/planning-checks/editor-labels` run |

Other exact strings: the editor's own title bar shows **2D**, **3D**, **Script**, **Game**, **Asset Store**; the Inspector dock tabs **Inspector**, **Signals** (and **Groups** when the dock is wide).

## 5. How it works

**Pieces** (all in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/`):

- `proj/addons/driver/plugin.gd`, `plugin.cfg`: the driver. It reads `res://state_script.json`, runs one step per editor frame (or after `wait_frames`), logs every step and every `mark` to `states.json`, and quits the editor when the script ends. Before any step it flashes the whole editor magenta for two frames (so the helper can find where the recording starts).
- `capture_editor_states.sh <project> <scene|-> <state_script.json> <out_dir> [--size WxH] [--settings FILE] [--renderer R] ...`: takes `/private/tmp/claude-501/shaderlab.lock` with `mkdir` (waits up to 30 minutes), touches it every 30 seconds from a background loop that dies with the script, releases it with `rmdir` in a trap; resets the project's `.godot/editor` and the editor settings each run; runs `godot --editor --path ... --write-movie <out>/frames/f.png --fixed-fps 30` with an isolated `HOME`; prints where the frames and the log are.
- `extract_marks.py <states.json> <frames_dir> <out_dir>`: copies the frame of each mark to `<MARKNAME>.png`, checks it is settled (identical to the next frame), writes `marks.json`, and with `--crop-dock` also the whole right dock.
- `make_state_scripts.py` writes `state-scripts/final/*.json`; `run_all.sh <WxH> <out_root> [names]` runs them all; `run_compare.sh` is the settings and renderer comparison; `compare_frames.py` compares two sets of PNGs.
- `proj/`: the scratch project (a teal test sprite made like the Lab's, 8 small scenes, 7 shaders: the films' own files byte-identical, listed with their sha256 in `SHADERS.sha256`, plus `e3-dial-and-tint.gdshader`, mine, with a `hint_range` float `red` and a `source_color` vec4 `tint`). The project's window override sets the movie size.
- `settings/`: the editor-settings variants (`...factory-after-first-run`, `...single-window`, `...single-window-renderer-selector`, `...100pct`). All differ from the factory file by exactly one line.

**State script steps** (any step may carry `"settle": N` to wait N frames after it; `mark` always ends its frame, so nothing can change the marked picture):

| Step | What it does | Kind |
|---|---|---|
| `open_scene`, `select_node`, `select_nodes`, `set_main_screen`, `hide_bottom_panel` | `EditorInterface.open_scene_from_path`, `EditorSelection.clear/add_node`, `set_main_screen_editor`, `EditorPlugin.hide_bottom_panel` | script |
| `inspect_object`, `edit_resource`, `edit_resource_file` | `EditorInterface.inspect_object(obj, for_property, inspector_only)`, `edit_resource`; the last two open the Shader Editor | script |
| `set_property` | `Object.set` on the node or resource, value read back and logged, Inspector rows refreshed; this is how `red` and the crosshair uniforms are set | script |
| `menu_item` | the real `View` menu entry (Frame Selection) via the menu's `id_pressed` | real handler |
| `unfold_group` | calls the Inspector section's own `unfold()` (scrolls nothing) | real handler |
| `unfold_resource` | the picker's `resource_selected(resource, true)`: what a click on a resource thumbnail does; waits until the Inspector really shows it (11 to 61 frames) | real handler |
| `open_picker_menu` / `focus_menu_item` / `pick_menu_item` | presses the picker's dropdown arrow; highlights an entry (`PopupMenu.set_focused_item`); fires the real menu's `id_pressed` | real handler |
| `select_option`, `set_text`, `press_ok` | the Create Shader dialog's Mode `OptionButton`, Path `LineEdit` (+ `text_changed`), OK button | real handler |
| `open_option_button` | `OptionButton.show_popup()` (renderer menu) | real handler |
| `click_control`, `click_at` | a scripted left click pushed through `Viewport.push_input` | **scripted input** (only the colour swatch in the final scripts) |
| `dock_split` | sets `DockHSplitMain.split_offsets` to widen the Inspector dock | layout, by script |
| `dump_inspector`, `dump_popup`, `dump_windows`, `dump_tree`, `dump_object`, `dump_scene_tree`, `probe_window`, `log` | write what the editor says (labels, menu items, window facts) into `states.json`; used for every label in this README | read only |

A step whose target is not on screen yet (a row, a popup, a dialog) runs again two frames later, up to 40 times, then logs an error. Final runs: 0 driver errors in all 20.

**What the log gives you:** `states.json` maps each mark to `process_frame` (the movie file number) and `frame` (`Engine.get_frames_drawn()`, not usable, see section 8), plus the edited object, the Inspector scroll, the selected nodes and the rectangles of the Inspector and the right dock.

## 6. Capture facts

**Frame size.** The movie size is the project's `window_width_override` x `window_height_override`, written by the launcher's `--size`. The driver first sets the editor window to **3456x1944** (16:9; this Mac's usable screen is 3456x2068). Movie Maker resamples that window to the movie size: **1920x1080** frames (UI looks about 111 %, text about 15 px high, legible) and **3456x1944** native (editor scale 200 %, crisp; cropped Inspector dock 560 px wide). All 40 native frames match their 1920x1080 twin (mean absolute difference 0.36 to 0.60 of 255, median 0.46, after resampling). A third option, a true 1920x1080 window with the editor's display scale at 100 %, also works (`png/true-1080p-at-100pct-scale/`, 14 frames, UI text about 13 px).

**Capture duration.** Per run, 1920x1080: 17 to 31 s wall (100 to 381 frames, 3 to 13 s of movie, 12 to 40 % of real time); 3456x1944: 25 to 56 s. The ten final scripts take about 4 minutes at 1920x1080 and 6 minutes at 3456x1944. The lock was held for exactly the run (longest hold 56 s; most acquisitions waited 0 s, the longest 36 s). About 70 editor runs in all, every one under the lock.

**Compatibility vs Forward+ (tested).** Same state scripts, `--rendering-method gl_compatibility` (OpenGL 4.1 on Metal): the editor looks the same. Every frame differs by at most 1 level of 255 (rounding), except the **Material slot's sphere preview thumbnail**, a 60x60 px box that renders differently (up to 49 levels; `logs/compare/compare-results.txt`). Colours inside the 2D viewport (the ColorRect) are identical (`E2-*`: no pixel differs by more than 1).

**Factory settings vs Single Window Mode (tested).** Frames without a popup: pixel-identical (all five `E2` frames and `E1-1`, `E1-2b`, `E1-3a`, `E1-3e`; the only difference anywhere is a 2x19 px text caret in `E1-4`). The frames with a popup differ only inside the popup's box, where the factory frames show nothing.

**Not tested:** a GPU or machine other than this one, another display scale than 200 % and 100 %, the Mobile renderer, 4.7.1 or earlier, a non-English editor.

## 7. Re-running it

```bash
# copy the folder to a scratch place first (a run writes .godot, home/ and frames next to it)
R=/private/tmp/claude-501/godot-shaders-editor-capture-rerun
mkdir -p $R && rsync -a --exclude png --exclude logs /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/ $R/
cd $R && python3 make_state_scripts.py
./run_all.sh 1920x1080 $R/out pilot-E2          # one script; omit the name for all ten; use 3456x1944 for native
# frames: $R/out/pilot-E2/named/*.png   log: $R/out/pilot-E2/states.json
```

Use `GODOT_CAPTURE_HOME=<dir>` (or `--home`) for the isolated editor HOME. A new state script is a JSON list of the steps in section 5; copy `state-scripts/final/pilot-E2.json` and change the scene, the `unfold_*` and `set_property` lines and the `mark` names. Label dumps alone do not need a window: the Reading the Screen film read its labels from a headless editor with its own small plugin (no window, no lock). I did not test this driver headless.

## 8. Traps met, and the failed attempts I kept

Logs of every attempt are in `logs/`; none was deleted.

1. **`Engine.get_frames_drawn()` is not the movie frame number.** The editor skips drawing while idle, so that counter falls behind. The movie writer writes one file per main-loop iteration, so the file number is `Engine.get_process_frames()` (the magenta flash confirms it: expected offset 0, found 0 in every final run). My first full batch indexed by `frames_drawn` and cut the wrong frame for 10 of its 40 marks (three scripts: pilot E1, pilot E2, Local, World plan-exact). Kept: `logs/failed-attempts/attempt1-frames_drawn-indexing-WRONG/` (its PNGs are the wrong frames; do not use).
2. **`open_picker_menu` was flaky:** the Inspector rebuilds its rows while previews arrive, freeing the picker and its menu. The pilot E1 run lost its Shader menu once (`logs/failed-attempts/attempt2-open_picker_menu-flaky-E1-failed/`). Fixed by looking the picker up again every frame and pressing again every 6 frames, plus the generic retry (section 5).
3. **The `View` menu was the 3D editor's** when the scene had not switched the main screen to 2D yet (`logs/failed-attempts/attempt3-local-world-*`). Fixed with `set_main_screen 2D` and a retry.
4. **Menus and dialogs are not recorded unless Single Window Mode is on** (section 3). The same scripts run without errors in both modes; only the frames differ.
5. **The window size matters.** A maximized editor (3456x2068 here) with a 1920x1080 movie is a centre crop: the title bar and the bottom panel strip are cut off (probe 1 frames, `logs/probes/probe1/named/`). That is what the 2026-10-09 recipe produces. `window_set_size(3840, 2160)` is clamped to 3840x2068 by the screen's height (`logs/probes/probe2`). A real 1920x1080 window at the automatic (200 %) display scale overflows (`logs/probes/probe2/named/P2-B-window-1920x1080.png`); use the 3456x1944 window, or set the display scale to 100 %.
6. **The Inspector takes 11 to 61 frames to switch** to a resource after its thumbnail is clicked (ShaderMaterial 11 to 13, NoiseTexture2D 21, FastNoiseLite 61). `unfold_resource` waits for it.
7. **Folding is automatic:** a group whose values all equal the defaults is folded; one holding a changed value is open when the Inspector is built. The editor stores fold state and the open shader file in the project's `.godot/editor`, which carried one run's state into the next until the launcher started deleting it.
8. **Frames inside `res://` are imported as assets** and slow the editor to 13 % of real time; the launcher refuses an out_dir inside the project.
9. **The Create Shader dialog's list reads "Canvas Item"** (with a space); my first script typed `CanvasItem`, the step failed and the file was created as Spatial (`logs/probes/probe7`).
10. **After the driver quits, Movie Maker keeps writing about 80 idle frames** while the editor shuts down; harmless, the marks are earlier.
11. **A film file changed under me.** The Drawing Shapes session reordered two lines of `make_arms` in `17-crosshair.gdshader` at 15:43 (the six uniform declarations are unchanged). I re-copied the file and re-recorded both Drawing Shapes scripts; the earlier runs are kept in `logs/superseded-runs-with-an-older-shader-copy/`.

Probe runs (what each taught): `logs/probes/probe1` first run, the API works and popups are not recorded; `probe2` window sizes and the real menu pick; `probe3` and `probe4` the click path; `probe5` and `probe6` embedded popups and the Create Shader dialog; `probe7` the renderer menu and the dialog end to end; `probe8a` the ColorRect Inspector, `red` slider, colour picker; `probe8b` to `probe8d` the noise menus and the FastNoiseLite preview. The headless API listing is `logs/launcher/api-introspect-1.txt` (the 4.7.2 methods of EditorInterface, EditorInspector, EditorPlugin, EditorProperty, EditorResourcePicker, EditorSelection, EditorSettings; `introspect.gd` made it).

## 9. If a film wants a visible mouse pointer (optional human take)

Nothing above needs it. Movie Maker draws the window but not the pointer, so a viewer never sees a cursor move. If a film wants that, record these takes by hand (screen recording of the Godot window, the `screen-clean` skill first), starting from the scratch project at `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/proj/` copied to a scratch folder (never record in the original):

1. Open `scenes/e1_sprite.tscn`, select **Sprite2D**. Click the **Material** group header under **CanvasItem**. Hold 2 s.
2. Click the Material slot's arrow. Hover **ShaderMaterial** (hold 2 s), click it. Click the new ShaderMaterial thumbnail. Hold 2 s.
3. Click the Shader slot's arrow, hover **New Shader...** (hold 2 s), click it. In **Create Shader** set **Mode** to **Canvas Item**, type a name in **Path**, click **Create**. Hold 3 s on the open Shader Editor.
4. Open `scenes/e2_dial.tscn`, select the **ColorRect**, click its Material thumbnail, open **Shader Parameters**, drag **Red** to 0.2, 0.5, 0.9, holding 2 s each.
5. For `E3`: click the **Tint** swatch, hold 3 s, press Escape.

The scripted frames and a human take then cut together without a visible seam (same project, same editor look).

## 10. Folder map

- `README.md`, `SHADERS.sha256`
- `capture_editor_states.sh`, `extract_marks.py`, `compare_frames.py`, `make_state_scripts.py`, `run_all.sh`, `run_compare.sh`, `assemble_deliverable.sh`, `introspect.gd`
- `proj/` the scratch project and the driver (`proj/addons/driver/`)
- `settings/` four editor-settings files; `state-scripts/final/` the scripts of this run (plus two `true-1080p-at-100pct` variants), `state-scripts/probes/` the exploratory ones
- `png/1920x1080/<film>/`, `png/3456x1944/<film>/` (each state, and `.dock.png`), `png/true-1080p-at-100pct-scale/`
- `logs/final-1080/<script>/` and `logs/final-3456/<script>/`: `states.json`, `run.log`, `run-info.txt`, `marks.json` of every final run; `logs/compare/` (factory vs single-window, Compatibility, true 1080p, `compare-results.txt`); `logs/probes/`; `logs/failed-attempts/`; `logs/superseded-runs-with-an-older-shader-copy/`; `logs/launcher/` (the batch logs)

---

## 11. Follow-up (2026-10-13): the true renderer path a student follows

**What this is.** A second recording session with the same driver, to answer one question from the Textures and Color film (B40) and the Shaders in 3D film (B43): both say "the renderer's name sits in the upper right corner of the editor, click it to switch". Section 2.9 had shown that is true only with an editor setting on. This section records the path a student really follows, with every label read from the live UI (the driver dumps them; none is typed from convention): the Project Settings dialog, the Editor Settings dialog found by searching "renderer", the title bar with that setting off and on, the Project Manager's Create New Project dialog, and the NoiseTexture2D "Seamless" row. Same scratch project, the shared Lab lock around every run, 1920x1080 and native 3456x1944, no human click, no film file touched. Nothing was created in any project: the Project Manager ran in an empty isolated HOME and every dialog was cancelled or closed.

**Why.** A student who follows the films' sentence on a fresh install finds no renderer name in the corner and nothing to click.

**Found.**
- **The title-bar renderer name is hidden by default in 4.7.2, and that is the engine's own default, not an artefact of my settings file.** Three independent proofs (11.4): the running editor reports `false` as the setting's default (`property_get_revert`); a brand-new empty HOME made the editor write its own settings file with `show_renderer_selector = false`; and the title bar of that factory-default editor has no renderer name (`R5-A`). The films' sentence is true only after the student turns on **Show Renderer Selector** (Editor > Editor Settings... > Interface > Editor > Appearance). It is an *advanced* setting: it is not listed until **Advanced Settings** is on, and searching "renderer" turns that on by itself.
- **There are three real places to choose a renderer, and they do not spell it alike.** Project Settings shows the raw identifiers **forward_plus**, **mobile**, **gl_compatibility** (not "Forward+"); the title-bar selector, its restart prompt and the Create New Project dialog show **Forward+**, **Mobile**, **Compatibility**. The title bar is not a shortcut: choosing another renderer there opens a dialog **Please Confirm...** and needs **Save & Restart**; so does a change in Project Settings (a banner with a warning icon says so).
- **The Project Manager's Create New Project dialog does show the choice**: a **Renderer:** group of three radio buttons, **Forward+** preselected, and five bullet lines per renderer (quoted in 11.2). The preselection comes from Editor Settings > Project Manager > **Default Renderer** (tested).
- **The NoiseTexture2D view has a row labelled exactly "Seamless"**, a checkbox (its box is labelled **On**), unticked by default (11.5).
- **All new stills are DONE, 22 frames at each size**, 0 driver errors, nothing not recordable; what is not recorded is listed in 11.7. The extended driver also re-recorded all 40 phase-1 frames pixel-identically (11.6).

### 11.1 Verdict for each item

Folders (every file name below starts with `renderer-path_`; the same names exist at both sizes):

- `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/renderer-path/`
- `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/3456x1944/renderer-path/`

Next to each full frame `<name>.png` there may be crops cut from that same frame, never redrawn: `<name>.dialog.png` (the dialog with its title bar), `<name>.title-strip.png` (the editor's top 50 px, 90 px native), and for the three Create dialogs `<name>.renderer-block.png` (the Renderer group only, which also leaves out the Project Path field). `stills.json` in each folder lists every file, its source frame and whether it was settled.

| Item asked | Verdict | Stills (after `renderer-path_`) |
|---|---|---|
| **1** Project Settings, Rendering > Renderer, closed and open | **DONE** | `R1-A_Project-menu-open` (the menu with Project Settings...); `R1-B_Project-Settings-dialog-opens`; `R1-C_Project-Settings_Rendering-Renderer_menu-closed`; `R1-D_Project-Settings_Rendering-Method_menu-open`; `R1-E_Project-Settings_restart-note` |
| **2** Editor Settings, found by searching "renderer" | **DONE** | `R2-A_Editor-menu-open`; `R2-B_Editor-Settings-dialog-opens` (Appearance without the row); `R2-C_Editor-Settings_Advanced-on_Interface-Editor-Appearance` (the row, found by scrolling); **`R2-D_Editor-Settings_search-renderer_Show-Renderer-Selector`** (the answer); `R2-E_Editor-Settings_search-renderer_Project-Manager-Default-Renderer`; `R2-F_Editor-Settings_Show-Renderer-Selector_ticked` |
| **3** Title bar, setting off (default) and on | **DONE** | **`R3-A_title-bar_selector-OFF-default`**, **`R3-B_title-bar_selector-ON`** (full frames; their `.title-strip.png` are the bars alone); composites of those two real frames: **`R3_title-bar_OFF-vs-ON_side-by-side`** (right 36 % of each bar, off left, on right) and `R3_title-bar_OFF-over-ON_stacked`; and `R3-C_title-bar_selector-menu-open`, `R3-D_title-bar_selector-restart-prompt`, `R3-E_after-Cancel`. A factory-default editor, for the truly default look: `R5-A_fresh-home_title-bar-factory-default` |
| **4** Project Manager, Create New Project dialog | **DONE**, nothing touched | `R4-A_Project-Manager-empty`; `R4-B_Create-New-Project_Forward-selected`; `R4-C_Create-New-Project_Mobile-selected`; `R4-D_Create-New-Project_Compatibility-selected`; `R4-E_after-Cancel-nothing-created` |
| **5** NoiseTexture2D has a row "Seamless" | **CONFIRMED from real frames** | no new recording needed, see 11.5 |
| Is "hidden by default" just this Mac's first run? | **No** | 11.4 |

### 11.2 The true path, with the exact labels

**A. Change the project's renderer (needs no setting).**

1. Menu **Project** > **Project Settings...** (`R1-A`). The dialog is titled **Project Settings (project.godot)**, has tabs **General**, **Input Map**, **Localization**, **Globals**, **Plugins**, **GDExtension**, **Import Defaults**, and opens on **General**, page **Application** > **Config** (`R1-B`).
2. In the left tree open the group **Rendering** and click the page **Renderer** (`R1-C`). Trap: the tree has a second page called **Rendering**, under **Internationalization**; that is not it.
3. The page has three rows: **Rendering Method** (dropdown, reads `forward_plus`), **Rendering Method.web** (`gl_compatibility`, and that is its only choice) and **Rendering Method.mobile** (`mobile`); the last two are per-platform overrides, drawn dimmer. The Rendering Method dropdown lists three radio entries: **forward_plus**, **mobile**, **gl_compatibility** (`R1-D`). The setting's key is `rendering/renderer/rendering_method`.
4. Choose another one: the row gets a revert arrow and a banner appears at the bottom of the dialog: warning icon, **Changed settings will be applied to the editor after restarting.**, buttons **Save & Restart** and a small **X** (`R1-E`). The two override rows do not change. The banner stays even after the value is put back (`fu-probe-D`, dump `after-revert-texts`). I never pressed Save & Restart; I put the value back and closed the dialog (the scratch project's `project.godot` ended identical to where it started, apart from the movie-size lines the launcher writes).

**B. Show the renderer name in the title bar (needs one editor setting), then use it.**

1. Menu **Editor** > **Editor Settings...** (the menu shows the shortcut **Command+Comma** on this Mac) (`R2-A`). The dialog is titled **Editor Settings**, tabs **General** and **Shortcuts**, a **Filter Settings** box and a switch **Advanced Settings**, and opens on **Interface** > **Editor** (`R2-B`). Its section **Appearance** lists four rows (**Display Scale**, **Custom Display Scale**, **Use Embedded Menu**, **Expand to Title**); **Show Renderer Selector** is not among them.
2. Two ways to find it. *Searching:* type `renderer` in **Filter Settings**. The switch **Advanced Settings** turns itself on and greys out; its tooltip, read from the UI, is **Advanced settings are always shown when searching.** *Scrolling:* turn **Advanced Settings** on; **Appearance** then lists eleven rows and the last one is **Show Renderer Selector** (`R2-C`).
3. The search result (`R2-D`): the left tree shrinks to **Interface** > **Editor** (selected) and **Project Manager**; the right pane shows the section header **Appearance** and one row, **Show Renderer Selector**, a checkbox whose label is **On**, unticked. So the **exact label is "Show Renderer Selector"**; its **category path in the dialog is Interface > Editor, section Appearance**; its tooltip key is `interface/editor/appearance/show_renderer_selector`. The other hit (`R2-E`) is the tree entry **Project Manager** (a top-level entry, not under Interface), row **Default Renderer**, key `project_manager/default_renderer`, dropdown `forward_plus` (its entries read `forward_plus`, `mobile`, `gl_compatibility`).
4. Tick **On** (`R2-F`; a revert arrow appears) and close the dialog. The title bar's right end now reads **Forward+** with a small arrow, in green (`R3-B`). No restart is needed for that.
5. Click the name: a menu lists **Forward+** (selected, radio), **Mobile**, **Compatibility** (`R3-C`). Choose another: a dialog titled **Please Confirm...** says "Changing the renderer requires restarting the editor." then "Choosing Save & Restart will change the renderer to:" and three lines, "- Desktop platforms: Compatibility", "- Mobile platforms: Compatibility", "- Web platform: Compatibility" (after choosing Compatibility), buttons **Cancel** and **Save & Restart** (`R3-D`). I pressed **Cancel**; the selector still reads Forward+ (`R3-E`). So "click it to switch" means: click, choose, confirm Save & Restart, and the editor restarts. The editor after the restart is not recorded.

**C. Choose it when creating the project.** In the Project Manager the toolbar button **Create** opens a dialog titled **Create New Project** (`R4-B`; the empty-list screen also has a **Create New Project** button, which I did not press): **Project Name:**, **Project Path:** with a **Create Folder** switch and **Browse**, then **Renderer:** with three radio buttons **Forward+** (preselected), **Mobile**, **Compatibility**, a link **More information** under them (not opened), and to the right five bullet lines that follow the selected button; below, the sentence **The renderer can be changed later, but scenes may need to be adjusted.**, then **Version Control Metadata:** (Git), **Edit Now**, **Cancel**, **Create**. The bullets, read from the UI:

| Selected | Bullets |
|---|---|
| **Forward+** (`R4-B`) | Supports desktop platforms only. / Advanced 3D graphics available. / Can scale to large complex scenes. / Uses RenderingDevice backend. / Slower rendering of simple scenes. |
| **Mobile** (`R4-C`) | Supports desktop + mobile platforms. / Less advanced 3D graphics. / Less scalable for complex scenes. / Uses RenderingDevice backend. / Fast rendering of simple scenes. |
| **Compatibility** (`R4-D`) | Supports desktop, mobile + web platforms. / Least advanced 3D graphics. / Intended for low-end/older devices. / Uses OpenGL 3 backend (OpenGL 3.3/ES 3.0/WebGL2). / Fastest rendering of simple scenes. |

The Forward+ preselection comes from Editor Settings > Project Manager > **Default Renderer**: with that setting set to `gl_compatibility` the same dialog opens on Compatibility (tested, `logs/followup/probes/pm-probe4`). In the stills the **Project Path** field shows this run's scratch folder (`/private/tmp/claude-501/godot-shaders-editor-capture/hom...`) and the footer says "Offline mode, update checks disabled."; use the `.renderer-block.png` crops, or crop those out.

**How the three spellings split:**

| Where | The three renderers read |
|---|---|
| Project Settings > Rendering > Renderer > Rendering Method (and its `.web`, `.mobile` rows) | `forward_plus`, `mobile`, `gl_compatibility` |
| Editor Settings > Project Manager > Default Renderer | `forward_plus`, `mobile`, `gl_compatibility` |
| Title-bar selector and its **Please Confirm...** dialog | Forward+, Mobile, Compatibility |
| Create New Project dialog | Forward+, Mobile, Compatibility |

**Wording that is true for 4.7.2** (for the two films to adopt; I did not edit any film file): "The project's renderer lives in Project > Project Settings, Rendering, Renderer, Rendering Method (forward_plus, mobile or gl_compatibility); change it, then Save & Restart. A new project picks it in the Create New Project dialog under Renderer. The renderer's name appears in the editor's upper right corner only after you turn on Editor > Editor Settings > Interface > Editor > Appearance > Show Renderer Selector (search 'renderer'); then the name opens a menu, and choosing another renderer asks you to Save & Restart."

### 11.3 The title bar, off and on

`R3-A` and `R3-B` come from one session; the only thing that changed between them is the setting, ticked in `R2-F` through the dialog (a scripted click on its checkbox). Off: the bar's right end holds only the run controls (play, pause, stop and three more icons). On: the run controls move left and **Forward+** with an arrow sits at the very right (`R3_title-bar_OFF-vs-ON_side-by-side.png`, 1396x50 at 1920x1080, 2511x90 native).

**One difference from a stock Mac.** In `R3-A` to `R3-E` and in every dialog frame the editor draws its own menu bar (**Scene Project Debug Editor Help**) inside the window, because the editor setting **Use Embedded Menu** is on for these runs (it shows with a revert arrow in the Editor Settings frames). The macOS default is off: the menus are then in the system menu bar at the top of the screen, which Movie Maker cannot record. `R5-A` is the stock look on this Mac (brand-new HOME, native menu): the window's title bar shows the file and project at the left (`e1_sprite.tscn - godot-shaders-editor-capture`), **2D 3D Script Game Asset Store** in the middle, the run buttons at the right, and **no renderer name**. The right end is the same in both looks. Dialogs are also drawn inside the window here (**Single Window Mode** on, section 3), where stock they are separate OS windows; so call these "scripted editor session" clips, as before.

### 11.4 Is "hidden by default" only this Mac's first run? No.

1. The running editor reports the setting's own default: `EditorSettings.property_get_revert("interface/editor/appearance/show_renderer_selector")` is `false` (`logs/followup/final-1080/editor/states.json`, dump `settings-at-start`; the same in the fresh run). It stays `false` after the box is ticked (value `true`, default `false`, dump `setting-after-tick`), so it is the engine's registered default, not the file's value.
2. A brand-new, empty HOME (the folder was deleted and re-created empty for the run, so no settings file at all): the editor wrote its own `editor_settings-4.7.tres` on first start, and line 43 reads `interface/editor/appearance/show_renderer_selector = false` (also `use_embedded_menu = false`, `single_window_mode = false`, `project_manager/default_renderer = "forward_plus"`). Kept: `settings/editor_settings-fresh-home-written-by-the-editor-4.7.2.tres`.
3. That file differs from `settings/editor_settings-factory-after-first-run.tres`, the "factory" file of sections 2 to 10, only in three lines that hold this HOME's folder name; so the factory file was an editor-written first-run file too, never hand-made.
4. `R5-A`: the title bar of that factory-default editor shows no renderer name.

I can speak only for 4.7.2.stable.official (`ed1daf0bf`); I did not test another version.

### 11.5 "Seamless" in the NoiseTexture2D view

Yes. The NoiseTexture2D Inspector lists, top to bottom: **Width**, **Height**, **Generate Mipmaps**, **Noise**, **Color Ramp**, **Seamless**, **Invert**, **In 3D Space**, **As Normal Map**, **Normalize**. **Seamless** is a checkbox (an `EditorPropertyCheck`, property `seamless`; the box carries the word **On**), **unticked by default**. It is visible in both of these real frames (phase-1 recordings, looked at again at both sizes for this answer):

- `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/textures-and-color/textures-and-color_E1-3a_NoiseTexture2D-width-height-noise-FastNoiseLite.png` (with its `.dock.png` crop of the Inspector), Noise = FastNoiseLite
- `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/png/1920x1080/textures-and-color/textures-and-color_E1-2b_inside-NoiseTexture2D-noise-empty.png` (and `.dock.png`), Noise empty
- native: the same names under `.../png/3456x1944/textures-and-color/`.

The row's label comes from the live dump, not from the frame alone: `logs/final-1080/tc-E1/states.json`, dump `noisetexture2d-with-fastnoiselite`, row `{"label": "Seamless", "class": "EditorPropertyCheck", "property": "seamless"}`.

### 11.6 How these stills were made

Same method as section 5. New driver steps (all in `proj/addons/driver/plugin.gd`; the Project Manager has its own small driver, `pm_driver.gd`):

| Step | What it does | Kind |
|---|---|---|
| `menubar_open` | scripted click on the menu's title in the embedded menu bar (title rectangle computed from the bar's font and style, because `MenuBar` has no rectangle accessor in 4.7.2) | **scripted input** |
| `menubar_pick` | `id_pressed` of the real menu item, then hides the menu | real handler |
| `select_tree_item` | `TreeItem.select` on a path such as Rendering > Renderer (what a click does) | real handler |
| `set_text`, `set_toggle`, `select_option`, `open_option_button`, `press_cancel`, `close_dialog` | the filter box, the **Advanced Settings** switch, the dropdowns (`item_selected`, `show_popup()`), Cancel, hide | real handler |
| `toggle_check` | a scripted click at the centre of a row's checkbox (the row listens to `pressed`, not `toggled`, see 11.8) | **scripted input** |
| `click` (Project Manager) | scripted click at the centre of a radio button, so the dialog's own handler runs as it does for a student | **scripted input** |
| `dump_texts`, `dump_rows`, `dump_menubar`, `dump_windows`, `editor_setting_info` | write every visible string, the Inspector-style rows, menu items, dialog texts and buttons, and each setting's value and default into `states.json` | read only |

Every `mark` now also logs the visible windows (class, title, rectangle, decoration height), which `make_followup_stills.py` uses for the dialog crops. The Project Manager is the real one: `godot --project-manager --script pm_driver.gd` makes Godot build the real Project Manager inside the script's main loop; it ignores Single Window Mode, so the script sets `root.gui_embed_subwindows = true`. It renders with `gl_compatibility` (the log says so); the editor session used `forward_plus`.

**Results.** Final runs, 1920x1080 / native: editor session 578 / 577 frames, 40 s / 72 s wall, 16 marks; Project Manager 140 / 140 frames, 9 s / 19 s, 5 marks; fresh HOME 77 / 77 frames, 14 s / 20 s, 1 mark. 0 driver errors, 0 retried steps in the editor sessions, every mark's frame identical to the next (settled). I looked at every new frame at both sizes (for some dialogs the crop cut from the frame instead of the whole frame). The lock was taken and released around every run (`/private/tmp/claude-501/shaderlab.lock` was gone after each batch); in the runs whose output I printed the wait was 0 s. 27 recorded runs in all (11 probes, 6 final, 10 regression), logs in `logs/followup/`.

**Regression.** The extended driver re-recorded all ten phase-1 state scripts at 1920x1080: 40 marks, 0 errors, and **all 40 stills pixel-identical to the stored phase-1 frames** (largest per-channel difference 0, `logs/followup/regression-1080/regression-compare.txt`). So sections 1 to 10 are untouched by the change, and the recordings are reproducible bit for bit on this machine. The phase-1 driver is kept in `tools-history/plugin-v1-for-readme-sections-1-to-10.gd`.

### 11.7 Not recorded, and caveats

- The macOS system menu bar (outside the window) and the separate OS windows of a stock editor; see 11.3. The film should show the in-window versions only as "scripted editor session".
- **Save & Restart was never pressed**: what the editor looks like after switching renderer, and how long the restart takes, are not recorded. Nor is the project's `project.godot` after a real switch.
- The dropdown entries are chosen through the dropdown's own handler (`item_selected`), not by a pointer click on the entry, as in the earlier sections. No pointer is ever visible.
- Not opened: the **More information** link in the Create dialog (it opens a web page), the Project Manager's own Settings, the project list with an existing project (so whether a listed project shows its renderer is not recorded), the Mobile or Compatibility editor look (section 6 covers Compatibility), Windows and Linux, other display scales, any version other than 4.7.2.
- The Project Settings and Editor Settings frames show this machine's scratch values: project name **godot-shaders-editor-capture**, and, in the Editor Settings, **Use Embedded Menu** and **Single Window Mode** switched on (revert arrows). Crop with the `.dialog.png` files or avoid those rows.

### 11.8 Traps met in this follow-up (failed attempts kept in `logs/followup/probes/`)

1. **`menubar_open` first clicked "Debug" instead of "Editor"**: `MenuBar` has no public rectangle accessor in 4.7.2 and my first guess at the title positions was wrong (`fu-probe-A`, frame `FU-A1`). Fixed by laying the titles out as the bar draws them.
2. **Setting `button_pressed` on a checkbox changes the box but not the setting**: the row listens to `pressed`. Probe `fu-probe-E` ticked the box and `editor_setting_info` still read `false`; the later steps then had no title-bar selector to open. Fixed with a scripted click (`fu-probe-E2`).
3. **Controls inside an embedded dialog report positions relative to the dialog**, so a click needs the dialog's own position added.
4. **`close_popups` did not close an OptionButton's menu** (its popup is an internal child): in `fu-probe-F` the renderer menu stayed open behind the restart prompt. Fixed.
5. **A dialog's message text and its buttons are internal children**, invisible to `dump_texts`; `dump_windows` now logs `dialog_text`, `ok_text`, `cancel_text`. The Create dialog's Cancel is pressed through `ConfirmationDialog.get_cancel_button()`.
6. **The editor starts on the 3D screen** when only the scene is opened; `select_node` on the Sprite2D switches to 2D (`fu-probe-C` versus the final frames).
7. **The Project Manager ignores Single Window Mode**: in `pm-probe1` the log says the Create dialog was open as a separate window (`embedded: false`) and its frame `PM1-B-after-pressing-Create.png` shows no dialog at all. Fixed in `pm_driver.gd` (11.6); `pm-probe2` has the first good frame.

### 11.9 Re-running, and the folder map

```bash
R=/private/tmp/claude-501/godot-shaders-editor-capture-rerun
mkdir -p $R && rsync -a --exclude png --exclude logs /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture/ $R/
cd $R && ./run_followup.sh 1920x1080 $R/out/followup-1080     # or 3456x1944; three sessions, each under the lock
python3 make_followup_stills.py $R/out/followup-1080 $R/out/followup-1080/png
```

`run_followup.sh` makes the three state scripts (`make_followup_scripts.py`), clones `proj/` to `proj-settings/` first (so a Project Settings edit can never reach the master project), records the editor, Project Manager and fresh-HOME sessions, and extracts the stills. A fresh HOME needs no setup: the script makes it. Tested: this exact recipe, run from a copy of this folder at 1920x1080, wrote 57 PNGs that are all pixel-identical to the ones delivered (the fresh-HOME settings file differs only in the three lines that hold the HOME's path).

New in the folder (everything else is as in section 10):

- tools: `pm_driver.gd`, `pmproj/` (the near-empty project that gives the Project Manager recording its size), `run_pm.sh`, `with_lab_lock.sh` (holds the lock around any command), `probe.sh` (one exploratory run on a fresh clone), `run_followup.sh`, `make_followup_scripts.py`, `make_followup_stills.py`, `assemble_followup.sh`; `tools-history/` (the phase-1 driver)
- `settings/`: `editor_settings-single-window-embedded-menu.tres` (single-window on, embedded menu on), `editor_settings-fresh-home-written-by-the-editor-4.7.2.tres`, `editor_settings-pm-default-renderer-gl_compatibility.tres` (the factory file with one line changed, for the preselection test)
- `state-scripts/followup/` (`rp-editor.json`, `rp-pm.json`, `rp-fresh.json`) and `state-scripts/probes/followup/`
- `png/1920x1080/renderer-path/`, `png/3456x1944/renderer-path/` (58 files each: 22 full frames, 13 dialog crops, 17 title strips, 3 renderer blocks, 2 composites, `stills.json`)
- `logs/followup/final-1080/`, `final-3456/` (`editor`, `pm`, `fresh`: `states.json`, `run.log`, `run-info.txt`, `marks.json`), `logs/followup/probes/` (the eleven exploratory runs with their stills), `logs/followup/regression-1080/`
