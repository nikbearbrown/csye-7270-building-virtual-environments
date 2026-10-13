#!/bin/zsh
# The two runs the film shows: the same failing script, without and with --python-exit-code 1. Real stdout/stderr and real exit codes.
cd "${0:A:h}"
B=/Applications/Blender.app/Contents/MacOS/Blender
run() {   # logfile  args...
  local log="$1"; shift
  { echo "\$ $B $*"; "$B" "$@" 2>&1; code=$?; echo "\$ echo \$?"; echo "$code"; } > "$log"
  echo "$log: exit $(tail -1 $log)"
}
run without_flag.log -b --factory-startup --python bad.py
run with_flag.log -b --factory-startup --python-exit-code 1 --python bad.py
