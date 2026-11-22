#!/usr/bin/env bash
# scripts/run-baseline.sh <label> [jobs]
# Runs every tests/test_*.gd through scripts/run-test.sh at 60 fps (the pinned
# mode for every existing suite, CLAUDE.md), several at once, and writes
# logs/baseline-<label>/summary.txt with one "PASS|FAIL <exit> <test>" line each.
# Slow suites get a 1200 s timeout, the rest 300 s.
cd "$(dirname "$0")/.."
label="$1"; jobs="${2:-10}"
out="logs/baseline-$label"; mkdir -p "$out"
slow=" test_bosses.gd test_elevation.gd test_layout.gd test_run_save.gd test_v1.gd "
run_one() {
	t="$1"; out="$2"; slow="$3"
	limit=300; case "$slow" in *" $t "*) limit=1200;; esac
	./scripts/run-test.sh "$t" 60 "$limit" > "$out/${t%.gd}.log" 2>&1
	code=$?
	if [ $code -eq 0 ]; then echo "PASS $code $t"; else echo "FAIL $code $t"; fi
}
export -f run_one
ls tests | grep -E '^test_.*\.gd$' | xargs -P "$jobs" -I{} bash -c 'run_one "$@"' _ {} "$out" "$slow" | sort -k3 > "$out/summary.txt"
echo "$(grep -c '^PASS' "$out/summary.txt") of $(wc -l < "$out/summary.txt") pass" | tee -a "$out/summary.txt"
