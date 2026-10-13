#!/bin/zsh
# B39A/B39B evidence: Blender's own description of the four flags the script-route command uses (read-only: prints help and exits).
cd "${0:A:h}"
B=/Applications/Blender.app/Contents/MacOS/Blender
{ echo "\$ $B --version"; "$B" --version 2>&1 | head -3; echo "\$ $B --help   (the four flags, with the lines that follow each)"; "$B" --help 2>&1 | grep -A3 -E "^(-b or --background|--factory-startup|-P or --python <|--python-exit-code)"; } > blender_help.log
cat blender_help.log
