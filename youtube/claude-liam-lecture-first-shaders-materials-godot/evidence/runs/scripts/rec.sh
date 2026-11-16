#!/usr/bin/env bash
# rec.sh <name> <command...>  (run from SCRATCH). Appends command, exit code, elapsed to journal.tsv
name="$1"; shift
J=/private/tmp/claude-501/a5-evidence/journal.tsv
start=$(python3 -c 'import time;print(time.time())')
"$@"
rc=$?
end=$(python3 -c 'import time;print(time.time())')
printf '%s\t%s\texit=%s\telapsed=%.1fs\t%s\n' "$(date +%H:%M:%S)" "$name" "$rc" "$(python3 -c "print($end-$start)")" "$*" >> $J
echo "[rec] $name exit=$rc"
exit $rc
