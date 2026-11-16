#!/bin/zsh
# build_pool.sh WORKER - take the next unclaimed checked film (READY), build it end to end, retry once from resheet.
# Guard: never start a film when the disk has under 3 GB free. Deck 04 goes last (its voice track may still be recording).
cd "${0:A:h}/.."
for n in 01 02 03 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 04; do
  [ -f extract/$n/READY ] || continue
  mkdir extract/$n/.claim 2>/dev/null || continue
  while pgrep -f "voice_queue.sh" >/dev/null && [ $n = 04 ]; do sleep 60; done
  free_gb=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}')
  if [ "$free_gb" -lt 3 ]; then echo "$n skipped: only ${free_gb} GB free (worker $1)" >> logs/pool.log; rmdir extract/$n/.claim; continue; fi
  python3 tools/build_film.py $n --from sheet --to checks > logs/build-$n.log 2>&1
  echo "$n exit $? (worker $1, $(date +%H:%M))" >> logs/pool.log
  if ! grep -q "stages done: .*checks" logs/build-$n.log; then
    python3 tools/build_film.py $n --from resheet --to checks > logs/build-$n-retry.log 2>&1
    echo "$n retry exit $? (worker $1, $(date +%H:%M))" >> logs/pool.log
  fi
done
echo "worker $1 done $(date +%H:%M)" >> logs/pool.log
