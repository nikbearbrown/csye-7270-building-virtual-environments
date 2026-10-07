# TYPECHECK.md — GATE T

Reel: `claude-liam-walker-rudy-gamedev`  |  Checked: 2026-10-04T23:16  |  Overall: PASS  |  Beats checked: 43  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B01 | ? | light | min-size §8.1: min text-run height 89px >= floor 41px | PASS | — |
| B02 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03 | ? | — | no video | SKIP | — |
| B04 | ? | light | no-wordy-card §8.5: 2 element(s), 14 words — within budget. Detail: 2 output lines (14 wor… | PASS | — |
| B05 | ? | light | no-wordy-card §8.5: pull-quote (12 words ≤ 12) | PASS | — |
| B06 | ? | light | no-wordy-card §8.5: pull-quote (8 words ≤ 12) | PASS | — |
| B07 | ? | — | no video | SKIP | — |
| B08 | ? | light | no-wordy-card §8.5: pull-quote (5 words ≤ 12) | PASS | — |
| B09 | ? | — | no video | SKIP | — |
| B10 | ? | light | no-wordy-card §8.5: pull-quote (11 words ≤ 12) | PASS | — |
| B11 | ? | — | no video | SKIP | — |
| B12 | ? | light | no-wordy-card §8.5: pull-quote (12 words ≤ 12) | PASS | — |
| B13 | ? | — | no video | SKIP | — |
| B14 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B15 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B16 | ? | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B16R | ? | — | no video | SKIP | — |
| B17 | ? | — | no video | SKIP | — |
| B18 | ? | light | no-wordy-card §8.5: pull-quote (11 words ≤ 12) | PASS | — |
| B19 | ? | — | no video | SKIP | — |
| B20 | ? | light | no-wordy-card §8.5: pull-quote (8 words ≤ 12) | PASS | — |
| B21 | ? | — | no video | SKIP | — |
| B22 | ? | light | no-wordy-card §8.5: pull-quote (5 words ≤ 12) | PASS | — |
| B23 | ? | — | no video | SKIP | — |
| B24 | ? | light | no-wordy-card §8.5: pull-quote (10 words ≤ 12) | PASS | — |
| B25 | ? | — | no video | SKIP | — |
| B26 | ? | light | no-wordy-card §8.5: pull-quote (9 words ≤ 12) | PASS | — |
| B27 | ? | — | no video | SKIP | — |
| B28 | ? | light | no-wordy-card §8.5: pull-quote (4 words ≤ 12) | PASS | — |
| B29 | ? | — | no video | SKIP | — |
| B30 | ? | light | no-wordy-card §8.5: pull-quote (11 words ≤ 12) | PASS | — |
| B31 | ? | — | no video | SKIP | — |
| B32 | ? | light | no-wordy-card §8.5: pull-quote (10 words ≤ 12) | PASS | — |
| B33 | ? | — | no video | SKIP | — |
| B34 | ? | light | no-wordy-card §8.5: pull-quote (3 words ≤ 12) | PASS | — |
| B35 | ? | — | no video | SKIP | — |
| B36 | ? | light | no-wordy-card §8.5: pull-quote (8 words ≤ 12) | PASS | — |
| B37 | ? | — | no video | SKIP | — |
| BVD1 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BVD2 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | ? | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 20 | 0 |
| min-size §8.1 | 26 | 0 |
| overflow §8.2 | 26 | 0 |
| contrast §8.3 | 26 | 0 |
| contrast-local §8.3b | 26 | 0 |
| bbox-overlap §8.6b | 26 | 0 |
| card-clip §8.13 | 26 | 0 |
| kerning §8.4 | 0 | 0 |
| redundancy §8.10 (advisory) | 2 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
