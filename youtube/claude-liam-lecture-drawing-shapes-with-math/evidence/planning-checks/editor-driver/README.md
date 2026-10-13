# Editor driver (a planning check, and a head start for capture E1)

**What this is.** A scratch Godot project (three small files) that opens a ColorRect whose material uses `lab-shaders/17-crosshair.gdshader`, with an `EditorPlugin` that puts the material in the real Inspector so its six uniforms show as sliders.
**Why.** FACTCHECK row 69 (the six uniforms appear as six sliders in the real Inspector) was the film's only open claim, and capture E1 needs exactly this view. It is proven here, so the build session does not have to find the method.
**Found.** It works in one run. The frame in `../png/editor-inspector-check-2d.png` is a real Godot 4.7.2 editor window recorded by Godot's own Movie Maker: Inspector, ShaderMaterial, "Shader Parameters": Dot Size, Ring Distanc(e) (the default dock width cuts the last letter), Ring Width, Arm Gap, Arm Length, Arm Width, each a number with a slider bar under it, plus the Material's own preview thumbnail showing the crosshair. In the 2D viewport the crosshair is the small teal figure at the top left (25 % zoom).

## How to run it (scratch copy only)

```bash
W=/private/tmp/<scratch>/editor-proj; F=/private/tmp/<scratch>/editor-frames
mkdir -p $W/addons/driver $F
cp plugin.gd plugin.cfg  $W/addons/driver/            # from this folder
cp project.godot.txt     $W/project.godot
cp crosshair.tscn.txt    $W/crosshair.tscn
cp ../../../lab-shaders/17-crosshair.gdshader $W/     # the film's own file, unchanged
godot --headless --path $W --import                   # import first, or the editor shows a "(Re)Importing Assets" box over the frame
godot --editor --path $W res://crosshair.tscn --write-movie $F/f.png --fixed-fps 30 --quit-after 150   # about 40 s; take frame 145
```

## What to do differently for the film (E1)

- **Write the frames OUTSIDE the project folder.** Frames inside `res://` are imported as assets: the first attempt (`../run-e1-editor-inspector-check-frames-inside-project-SLOW.log`) ran at 13 % of real time and left an import box on screen.
- **The three states** are three scene files (or one scene edited by a script between runs) with `shader_parameter/...` saved: defaults; `dot_size` = 1.0; `ring_distance` = 0.2. This project's scene already holds dot_size 1.0 and ring_distance 0.2 (the Inspector shows the revert arrows next to those two).
- **Sharp crop.** The film crops the Inspector to the "Shader Parameters" group (no preview thumbnail: it draws the crosshair stretched into an ellipse). **Recommended, not run here** (this check recorded at 1920 by 1080): record at 3840 by 2160 (set `window_width_override` and `window_height_override`) with the editor's display scale at 200 % so the crop is not blurry; never upscale a small frame.
- **The editor theme is dark by default and may fail GATE T.** The Light preset is a global editor setting of Bear's Godot: never change it in place; back the settings file up and restore it, or ask Bear.
- A widening of the dock by script was tried (`DockHSplitMain.split_offset`) and made the left dock narrower instead; it is not needed. If "Ring Distanc" must read in full, widen the Inspector dock by hand once and keep the saved editor layout.
