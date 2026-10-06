#!/bin/bash
# usage: run.sh <project-root> <label> <fixed:yes|no>
P=$1; L=$2; F=$3; E=$(dirname $0)/ev-$L; mkdir -p $E
ARGS="--headless --path $P/godot"
[ "$F" = yes ] && ARGS="$ARGS --fixed-fps 60"
start=$(date +%s)
WALKER_EVIDENCE_DIR=$E godot $ARGS --script $P/tests/input_route.gd > $E/out.log 2>&1
code=$?
end=$(date +%s)
python3 - "$E" "$L" "$code" "$((end-start))" <<'PY'
import json,glob,sys
E,L,code,secs=sys.argv[1:]
f=sorted(glob.glob(E+'/route-*.json'))[-1]; d=json.load(open(f))
bad=[k for k,v in d['checks'].items() if not v]
print(f"{L}: exit={code} wall={secs}s counts={d['counts']} max_speed={d['max_speed']:.2f} failed={bad}")
PY
