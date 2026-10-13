#!/bin/zsh
# run-editor-labels.sh: opens a scratch copy of this mini project in the REAL Godot 4.7.2 editor (headless: the editor builds its whole UI, nothing is drawn),
# where a plugin (addons/rts_labels/plugin.gd) walks the Inspector and its menus and prints the labels the film names:
#   - the Layout > Anchors Preset dropdown of a ColorRect (it lists "Full Rect")      - Mouse > Filter (Stop, Pass (Propagate Up), Ignore)
#   - a CanvasLayer's Layer group                                                       - a BackBufferCopy's Copy Mode (Disabled, Rect, Viewport)
#   - a ShaderMaterial's "Shader Parameters" group: a hint_range uniform is an EditorPropertyFloat with an EditorSpinSlider, a source_color vec3 is an
#     EditorPropertyColor with a ColorPickerButton, and the hint_screen_texture uniform is not listed at all
# Output: ../editor-labels-run.log   (the editor edits nothing in the project folder you keep; it runs on a scratch copy)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "$HERE/../../.." && pwd)"
W=/private/tmp/claude-501/rts-editor-labels
rm -rf "$W"; mkdir -p "$W/lab-shaders"
rsync -a --exclude run-editor-labels.sh "$HERE/" "$W/"
cp "$FILM/lab-shaders/05-gray.gdshader" "$FILM/lab-shaders/12-pool.gdshader" "$W/lab-shaders/"
{ echo "# $(date '+%Y-%m-%d %H:%M:%S') godot --editor --headless --path <scratch copy of editor-labels> --quit-after 900"; } > "$HERE/../editor-labels-run.log"
timeout 150 godot --editor --headless --path "$W" --quit-after 900 >> "$HERE/../editor-labels-run.log" 2>&1
echo "# exit $?" >> "$HERE/../editor-labels-run.log"
grep -E "^(RESULT|NOTE|GROUPS|WIDGET)|^  (OptionButton|EditorProperty)|EditorPropertyColor|EditorPropertyFloat|ColorPickerButton" "$HERE/../editor-labels-run.log" | cut -c1-300 | head -60
