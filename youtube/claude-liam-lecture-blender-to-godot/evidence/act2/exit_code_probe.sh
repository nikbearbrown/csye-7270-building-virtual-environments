#!/usr/bin/env bash
# Act II, B15 evidence: raise the same Python error in background Blender with and without --python-exit-code 1,
# and record the real stdout/stderr and the real exit status of each run. Output: exit_code_transcript.txt
# (the transcript's `$` lines are the commands exactly as run, `Blender` = /Applications/Blender.app/Contents/MacOS/Blender).
set -u
cd "$(dirname "$0")"
Blender() { /Applications/Blender.app/Contents/MacOS/Blender "$@"; }
{
  echo '$ Blender --version | head -1'; Blender --version | head -1
  echo "\$ Blender -b --python-expr \"raise ValueError('boom')\""
  Blender -b --python-expr "raise ValueError('boom')" 2>&1; rc=$?
  echo '$ echo $?'; echo "$rc"
  echo "\$ Blender -b --python-exit-code 1 --python-expr \"raise ValueError('boom')\""
  Blender -b --python-exit-code 1 --python-expr "raise ValueError('boom')" 2>&1; rc=$?
  echo '$ echo $?'; echo "$rc"
} > exit_code_transcript.txt
cat exit_code_transcript.txt
