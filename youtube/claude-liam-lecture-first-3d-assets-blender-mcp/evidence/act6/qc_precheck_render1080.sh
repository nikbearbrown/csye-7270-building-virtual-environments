#!/bin/zsh
# Renders act VI scenes at 1920x1080, 15 fps into a private scratch (one at a time) for the GATE T / Gate V pre-checks:
#   evidence/act6/qc_precheck_render1080.sh B50_ExportGLB ... ; python3 evidence/act6/qc_precheck_gateT.py /private/tmp/claude-501/a6_hd/media/videos/scenes/1080p15/*.mp4
#   (for the 4K-scale GATE T path render with -r 2880,1620 instead; the x2 line in gateT is an upscale estimate only)
R=/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-3d-assets-blender-mcp
S=/private/tmp/claude-501/a6_hd
mkdir -p $S
python3 $R/assemble_scenes.py --out $S --acts 6 >/dev/null
cp $R/beat_sheet.json $S/; ln -sfn $R/pantry $S/pantry
cd $S
for C in "$@"; do
  manim -r 1920,1080 --fps 15 --media_dir $S/media scenes.py $C 2>&1 | grep -E "\[pace\]|Error|Traceback" | sed 's/.*\[pace\]/[pace]/'
done
