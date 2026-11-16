#!/bin/zsh
# clean_passed.sh - Bear, 2026-11-13: "Yes, delete those". Once a Key Terms film's build log says every stage through
# checks passed AND its 4K master exists, delete its regenerable build files: clips/, mp4/ and the slate cut.
# The master (exports/), media/, mp3/, captions and paperwork stay. Loops until both build workers are done.
cd "${0:A:h}/.."
Y=../
clean() {
  local slug=${1:?}
  local reel="$Y${slug:?}"
  [ -f "$reel/exports/landscape/${slug:?}.mp4" ] || return
  [ -d "$reel/clips" ] || [ -d "$reel/mp4" ] || [ -f "$reel/${slug:?}-slate.mp4" ] || return
  rm -rf "${reel:?}/clips" "${reel:?}/mp4"; rm -f "${reel:?}/${slug:?}-slate.mp4"
  echo "$(date +%H:%M) cleaned $slug, free $(df -h /System/Volumes/Data | tail -1 | awk '{print $4}')" >> logs/clean.log
}
while true; do
  for f in logs/build-*.log logs/pilot-05-build.log; do
    [ -f "$f" ] || continue
    tail -40 "$f" | grep -q "stages done: .*checks" || continue
    slug=$(grep -o "claude-liam-lecture-key-terms-[a-z0-9-]*" "$f" | head -1)
    [ -n "$slug" ] && clean "$slug"
  done
  [ $(grep -c "worker .* done" logs/pool.log 2>/dev/null) -ge 2 ] && ! pgrep -f build_film.py >/dev/null && break
  sleep 120
done
echo "$(date +%H:%M) cleaner done" >> logs/clean.log
