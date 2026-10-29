# TYPECHECK.md — GATE T

Reel: `claude-liam-walker-rudy-shaders`  |  Checked: 2026-10-28T22:07  |  Overall: PASS  |  Beats checked: 28  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B01 | ? | light | min-size §8.1: min text-run height 95px >= floor 41px | PASS | — |
| B02 | ? | — | no video | SKIP | — |
| B03 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B05 | ? | light | no-wordy-card §8.5: pull-quote (7 words ≤ 12) | PASS | — |
| B06 | ? | — | no video | SKIP | — |
| B07 | ? | light | no-wordy-card §8.5: pull-quote (12 words ≤ 12) | PASS | — |
| B08 | ? | — | no video | SKIP | — |
| B09 | ? | — | no video | SKIP | — |
| B10 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B11 | ? | light | no-wordy-card §8.5: pull-quote (11 words ≤ 12) | PASS | — |
| B12 | ? | — | no video | SKIP | — |
| B13 | ? | light | no-wordy-card §8.5: pull-quote (11 words ≤ 12) | PASS | — |
| B14 | ? | — | no video | SKIP | — |
| B15 | ? | light | no-wordy-card §8.5: pull-quote (12 words ≤ 12) | PASS | — |
| B16 | ? | — | no video | SKIP | — |
| B17 | ? | light | no-wordy-card §8.5: pull-quote (11 words ≤ 12) | PASS | — |
| B18 | ? | — | no video | SKIP | — |
| B19 | ? | — | no video | SKIP | — |
| B20 | ? | light | no-wordy-card §8.5: pull-quote (8 words ≤ 12) | PASS | — |
| B21 | ? | — | no video | SKIP | — |
| B22 | ? | — | no video | SKIP | — |
| B23 | ? | — | no video | SKIP | — |
| BVD1 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BVD2 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | ? | dark | min-size §8.1: min text-run height 45px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 10 | 0 |
| min-size §8.1 | 16 | 0 |
| overflow §8.2 | 16 | 0 |
| contrast §8.3 | 16 | 0 |
| contrast-local §8.3b | 16 | 0 |
| bbox-overlap §8.6b | 16 | 0 |
| card-clip §8.13 | 16 | 0 |
| kerning §8.4 | 0 | 0 |
| redundancy §8.10 (advisory) | 2 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
