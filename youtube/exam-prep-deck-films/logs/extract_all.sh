#!/bin/zsh
# extract every deck (words per step + stills). Deck 11 uses the film copy in decks/ (the newer version with the extra step).
cd "${0:A:h}/.."
G=../../glossary/decks
one() {
  f="$1"; nn="${${f:t}[1,2]}"
  src="$f"; [ -f "decks/${f:t}" ] && src="decks/${f:t}"
  python3 tools/deck_extract.py "$src" extract/$nn > logs/extract-$nn.log 2>&1
  echo "$nn exit $? $(tail -1 logs/extract-$nn.log)" >> logs/extract.log
}
: > logs/extract.log
i=0
for f in $G/*.html; do
  one "$f" &
  i=$((i+1)); [ $((i % 5)) -eq 0 ] && wait
done
wait
echo ALL-DONE >> logs/extract.log
