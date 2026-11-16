#!/bin/zsh
# voice_queue.sh NN... - for each film whose script is checked (READY), build the sheet, voice it, pad it and run Whisper. No video.
cd "${0:A:h}/.."
for n in "$@"; do
  [ -f extract/$n/READY ] || { echo "$n not ready" >> logs/voice.log; continue; }
  python3 tools/build_film.py $n --from sheet --to whisper > logs/voice-$n.log 2>&1
  echo "$n exit $? $(grep -E '^- whisper' logs/voice-$n.log | tail -1)" >> logs/voice.log
done
