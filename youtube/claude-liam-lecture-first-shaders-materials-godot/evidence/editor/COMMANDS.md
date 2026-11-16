# COMMANDS: how the real Godot 4.7.2 editor frames were recorded

What this is: the exact commands that produced the PNGs in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/captures/editor/`. Read `EDITOR-NOTES.md` first for what each frame shows.

Nothing here touched Bear's project. `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/godot/` was read once by `rsync` (without its `.godot` cache) and never opened in Godot.

## 1. Scratch set-up (copy, never the originals)

```bash
DRIVER=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/editor-capture
SRC=/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude
R=/private/tmp/claude-501/a5-editor-capture

mkdir -p $R && rsync -a --exclude png --exclude logs $DRIVER/ $R/            # the driver tools (launcher, extract_marks.py, settings/)
rsync -a --exclude .godot $SRC/godot/ $R/a5proj/                              # Bear's project, copied WITHOUT its .godot cache
mkdir -p $R/a5proj/addons/driver
cp $DRIVER/proj/addons/driver/plugin.gd $DRIVER/proj/addons/driver/plugin.cfg $R/a5proj/addons/driver/
printf '\n[editor_plugins]\n\nenabled=PackedStringArray("res://addons/driver/plugin.cfg")\n' >> $R/a5proj/project.godot
cp $R/a5proj/addons/driver/plugin.gd $R/plugin.gd.orig                         # to make the diff
# then plugin.gd was extended in the SCRATCH copy only: see plugin.gd.diff (and the full file plugin.gd) next to this file
```

The first launcher run does a headless `--import` of the copy (about 90 s).

## 2. One recording (always through the launcher, which takes the Lab lock)

```bash
cd $R
./capture_editor_states.sh a5proj - ss/<script>.json out/<script> \
    --size 3456x1944 \
    --settings $R/settings/editor_settings-single-window.tres \
    --home $R/home
python3 extract_marks.py out/<script>/states.json out/<script>/frames out/<script>/named
rm -rf out/<script>/frames          # a native recording is about 400 MB to 1.2 GB of frames: delete after extracting
```

- `capture_editor_states.sh` takes `/private/tmp/claude-501/shaderlab.lock` (`mkdir`), refreshes it every 30 s, releases it on exit. Every run waited 0 s.
- `--size 3456x1944` writes the movie size into the scratch `project.godot`; the driver sets the editor window to 3456x1944 and the frames are the window 1:1 (editor scale 200 %).
- `editor_settings-single-window.tres`: Single Window Mode on (popups and menus are drawn inside the window, so the recorder sees them).
- The project's own renderer was used: `gl_compatibility` (Bear's `project.godot`). One extra run used `--renderer forward_plus` (see section 4).
- Each mark was taken twice (`NAME`, then `NAME__chk` 25 to 70 frames later) and the two PNGs compared pixel by pixel; a frame is only used if they are identical (`run_one.sh` in the scratch folder did this and printed `TWIN <name> IDENTICAL`).

## 3. The state scripts (this folder's `state-scripts/`)

| Script | Frames | Notes |
|---|---|---|
| `f1.json` | F1a, F1b | standard_generated.gdshader in the Shader Editor; bottom panel expanded by a scripted click on its expand button at (2770, 1896); files panel hidden with the editor's own "Toggle Files Panel" button; `goto_line` with `no_blink` |
| `f2.json` | F2 | signal.gdshader; bottom panel raised by a scripted drag of the split bar (1700,1241 to 1700,900); cursor to line 10 |
| `f35final.json` | F3a, F3b, F5a to F5e | matte.tres, coated.tres, standard-source.tres, then the MeshInstance3D Material Override picker menu; right dock widened to 900 px with `dock_split` |
| `f4final.json` | F4a to F4f, F4x | Import dock; left dock widened to 760 px; tall variants by a scripted drag of the left dock's split bar; F4x is the extra |
| `f4tree.json` | F4a, F4b (the delivered ones) | the same two default-height Import dock frames with the FileSystem tree scrolled (`scroll_tree`) so the driver's `addons` row is out of view; replaces the F4a/F4b of `f4final.json` |
| `f3fp.json` | extra | matte and coated again with `--renderer forward_plus` (run as `./run_one_fp.sh f3fp`, the same glue plus `--renderer forward_plus`) |
| `f3.json`, `f4.json`, `f5.json`, `probe1.json`, `probe2.json` | none used | earlier attempts, kept (see `failed/` and EDITOR-NOTES, "Traps") |

Run from the scratch folder, for example:

```bash
./run_one.sh f35final     # = capture_editor_states.sh + extract_marks.py + the twin check + delete frames
```

(`run_one.sh` and `assemble.py` live in `/private/tmp/claude-501/a5-editor-capture/`; they are four lines of glue and are described here, not needed to understand the frames.)

## 4. New driver steps (all in the scratch `plugin.gd`; see `plugin.gd.diff`)

| Step | What it does |
|---|---|
| `unfold_sections {property, object}` | unfolds EVERY Inspector section that contains the row (the old `unfold_group` only did the innermost one); used for the `Surface` and `Pattern` groups and for Albedo, Roughness, Normal Map |
| `goto_line {line, column, first_visible, focus, no_blink, center, select_line}` | CodeEdit APIs on the visible code editor: caret, first visible line, steady caret |
| `dump_codeedit` | writes the visible lines, caret and scroll of the code editor into the log |
| `select_file {path}` | `EditorInterface.select_file` plus `FileSystemDock.navigate_to_path` |
| `drag {x1,y1,x2,y2,steps}` | a scripted left-button drag (one motion event per frame) through `Viewport.push_input`: used on the two split bars |
| `scroll_in {within, to|y}` | scrolls the first EditorInspector inside a node (the Import dock) |
| `scroll_tree {within, text, margin}` | moves a Tree's internal vertical scroll bar so the item with that text is at the top (the FileSystem dock) |
| `key`, `call_editor`, `click_at` (old) | exploration helpers (`key` was not needed for any final frame) |
| `_resolve` targets `edited`, `file` | the object the Inspector is editing / a resource loaded from a path |
| `value_resource` in `set_property` | assigns a resource loaded from a `res://` path (used to put standard-source.tres into the scratch scene's Sample node) |
| `dump_inspector` now logs `value` | the model value behind each row |
| `internal: true` on `dump_tree`, `dump_texts`, `press`, `click_control` | also walks internal children (the bottom panel's tab bar and buttons) |

Existing steps used as documented in the driver's README: `open_scene`, `set_main_screen`, `edit_resource_file`, `select_node`, `set_property`, `unfold_group`, `open_picker_menu`, `focus_menu_item`, `select_tab`, `select_option`, `dock_split`, `scroll_inspector`, `dump_inspector`, `dump_texts`, `dump_tree`, `dump_popup`, `wait_frames`, `mark`.

## 5. Logs

`logs/<script>/states.json` (every step, every mark, every dump: this is where the labels in EDITOR-NOTES.md were read), `run-info.txt`, `run.log`.
