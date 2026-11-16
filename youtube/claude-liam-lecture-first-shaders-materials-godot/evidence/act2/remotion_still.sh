#!/usr/bin/env bash
# usage: [SCALE=2] remotion_still.sh <Pattern> <props.json> <out_prefix> <frame> [frame...]
# `npx remotion still` hangs at 'Getting composition' on this Mac with Remotion's bundled Chrome (see CLAUDE.md, Remotion version law): this passes Playwright's headless shell.
# B09's props: python3 -c "import json;L=json.load(open('lanes/act2.json'));p=dict(L['B09']['props']);p['durationSeconds']=9.06;json.dump(p,open('/private/tmp/claude-501/b09_props.json','w'),ensure_ascii=False)"
PAT="$1"; PROPS="$2"; OUT="$3"; shift 3
CH=$(ls ~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell | tail -1)
cd /Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion || exit 1
for F in "$@"; do
  npx remotion still src/index.ts "$PAT" "${OUT}_${F}.png" --frame="$F" --props="$PROPS" --scale=${SCALE:-1} --browser-executable="$CH" 2>&1 | tail -2
done
echo DONE
