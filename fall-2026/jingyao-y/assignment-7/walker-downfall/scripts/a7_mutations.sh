#!/usr/bin/env bash
# scripts/a7_mutations.sh [m1|m2|m3|m4 ...]
# A7 Step 6 mutations (agent, 2026-11-22). Each mutation runs in its own git
# worktree of the course repository at HEAD, sparse-checked-out to this
# assignment's folder, so the working tree is never left broken. The worktree
# starts with no .godot cache, so each one imports from scratch first. The
# mutation is applied with a literal text edit, the named read-back runs
# through that worktree's scripts/run-test.sh, the exit code is recorded, and
# the worktree is removed.
#   m1  rename one track's property in the wave_release clip only
#       (ArmFront:rotation -> ArmFront:rotaton); test_wave_rig_readback must exit 1
#   m2  npc_idle loop_mode LOOP_LINEAR -> LOOP_NONE; test_npc_idle_readback must exit 1
#   m3  one npc_idle frame key set to hframes*vframes (3 -> 4); test_npc_idle_readback must exit 1
#   m4  no mutation: an empty import cache, then both read-backs (the rig is a
#       keyed cutout, not imported, so nothing is expected to be lost)
# Results: logs/a7_mutations/<m>.log and logs/a7_mutations/summary.txt
set -u
HERE="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"          # csye-7270-course
SUB="fall-2026/jingyao-y/assignment-7/walker-downfall"
GODOT="$(cd "$REPO/.." && pwd)/Godot_v4.7.2-stable_win64_console.exe"
OUT="$HERE/logs/a7_mutations"; mkdir -p "$OUT"
REV="$(git -C "$REPO" rev-parse --short HEAD)"

run_one() {
	m="$1"; wt="$(cd "$REPO/.." && pwd)/a7-mutate-$m"; log="$OUT/$m.log"
	{
	echo "== $m at $REV, worktree $wt"
	git -C "$REPO" worktree add --no-checkout "$wt" HEAD >/dev/null 2>&1 || { echo "worktree add failed"; return; }
	git -C "$wt" sparse-checkout set --no-cone "/$SUB/" >/dev/null 2>&1
	git -C "$wt" checkout -q HEAD
	cd "$wt/$SUB" || return
	echo "-- .godot present before import: $([ -d .godot ] && echo yes || echo no)"
	timeout 1500 "$GODOT" --headless --path . --import > "$OUT/$m.import.log" 2>&1
	echo "-- import exit $?"
	case "$m" in
	m1) python - <<'EOF'
p='animations/lappland_wave_rig.tscn'; s=open(p,encoding='utf-8').read()
a='NodePath("ArmFront:rotation")'; i=s.rfind(a)
s=s[:i]+'NodePath("ArmFront:rotaton")'+s[i+len(a):]
open(p,'w',encoding='utf-8',newline='\n').write(s)
EOF
		tests="test_wave_rig_readback.gd";;
	m2) sed -i 's/^loop_mode = 1$/loop_mode = 0/' animations/npc_idle.tscn; tests="test_npc_idle_readback.gd";;
	m3) sed -i 's/"values": \[0, 1, 2, 3\]/"values": [0, 1, 2, 4]/' animations/npc_idle.tscn; tests="test_npc_idle_readback.gd";;
	m4) tests="test_wave_rig_readback.gd test_npc_idle_readback.gd";;
	esac
	echo "-- mutation diff:"; git diff --stat; git diff | grep -E "^[-+][^-+]" | head -6
	for t in $tests; do
		./scripts/run-test.sh "$t" 60 > "$OUT/$m.${t%.gd}.log" 2>&1
		code=$?
		echo "-- $t exit $code; $(grep -cE '^FAIL' "$OUT/$m.${t%.gd}.log") FAIL lines"
		grep -E '^FAIL' "$OUT/$m.${t%.gd}.log" | head -5
		echo "RESULT $m $t exit=$code" >> "$OUT/summary.txt"
	done
	cd "$REPO"
	git -C "$REPO" worktree remove --force "$wt" && echo "-- worktree removed"
	} > "$log" 2>&1
}

: > "$OUT/summary.txt"
set -- ${@:-m1 m2 m3 m4}
for m in "$@"; do run_one "$m" & done
wait
cat "$OUT/summary.txt"
