#!/bin/zsh
# lab-lib.sh: a thin logger around the Shader Lab (../../../_godot-shaders-series/lab/check_shader.sh).
# Source it from a batch script; call:  run <label> <shader> [check_shader options...]
#   <shader> is a file name inside ../../lab-shaders/, or an absolute path (calculators live in ./calc/).
# Every call appends one JSON line to $RES with the label, the exact options, the exit code and the Lab's own output.
HERE="$(cd "$(dirname "${(%):-%x}")" && pwd)"
FILM="$(cd "$HERE/../.." && pwd)"
LAB="$(cd "$FILM/../_godot-shaders-series/lab" && pwd)"
SH="$FILM/lab-shaders"
OUT="$HERE/png"; mkdir -p "$OUT"
RES="${RES:-$HERE/lab-results.jsonl}"
run() {
  local label="$1"; local shader="$2"; shift 2
  local spath="$shader"; [[ "$shader" != /* ]] && spath="$SH/$shader"
  local line code
  line=$("$LAB/check_shader.sh" "$spath" "$@" --png "$OUT/$label.png" 2>&1)
  code=$?
  python3 - "$label" "$shader" "$code" "$line" "$*" >>"$RES" <<'PY'
import json, sys, datetime
label, shader, code, out, args = sys.argv[1:6]
print(json.dumps({"check": label, "shader": shader, "args": args, "exit": int(code), "output": out.strip(),
                  "when": datetime.datetime.now().isoformat(timespec="seconds")}))
PY
  echo "[$code] $label"
}
