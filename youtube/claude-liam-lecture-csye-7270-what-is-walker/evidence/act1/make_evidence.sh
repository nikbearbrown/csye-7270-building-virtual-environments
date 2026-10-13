#!/usr/bin/env bash
# make_evidence.sh — regenerates the Act I evidence files from the Walker repo (read-only commands).
# W = the Walker framework repo; HEAD = its committed (public) version 10fedb8.
set -eu
W=/Users/bear/Documents/CoWork/bear-textbooks/books/walker
OUT="$(cd "$(dirname "$0")" && pwd)"
{
  echo "# git ls-tree -r --name-only HEAD legacy   (walker HEAD $(git -C "$W" rev-parse --short HEAD), run $(date '+%Y-%m-%d'))"
  git -C "$W" ls-tree -r --name-only HEAD legacy
  echo "# count by extension"
  git -C "$W" ls-tree -r --name-only HEAD legacy | sed 's/.*\.//' | sort | uniq -c
  echo "# working-tree changes under legacy/ (empty = none)"
  git -C "$W" status --short -- legacy
} > "$OUT/legacy-tree.txt"
{
  echo "# the quoted lines, with their real line numbers"
  grep -n "AI made" "$W/legacy/README.md"
  grep -n "Doctrine and tooling" "$W/legacy/README.md"
  grep -n "tooling does not exist" "$W/legacy/AGENTS.md" | cut -c1-40
  grep -n "Text layer\|Asset / engine" "$W/legacy/AGENTS.md" | cut -c1-110
  echo "# LICENSE.md head (HEAD and working tree)"
  git -C "$W" show HEAD:LICENSE.md | head -3
  echo "# CHANGELOG.md: HEAD top vs working tree top"
  git -C "$W" show HEAD:CHANGELOG.md | sed -n 1,3p | cut -c1-60
  sed -n 1,4p "$W/CHANGELOG.md" | cut -c1-90
  grep -n "Initial Godogen release" "$W/CHANGELOG.md" | cut -c1-70
  echo "# publish.sh usage line 5 at HEAD"
  git -C "$W" show HEAD:publish.sh | sed -n 5p
  echo "# is gdd/ tracked at HEAD? (empty = no)"
  git -C "$W" ls-tree HEAD gdd/
  git -C "$W" status --short gdd | head -2
} > "$OUT/quotes.txt"
cat "$OUT/legacy-tree.txt" "$OUT/quotes.txt" | head -80
