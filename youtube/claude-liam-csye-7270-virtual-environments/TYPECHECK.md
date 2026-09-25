# TYPECHECK.md — GATE T

Reel: `claude-liam-csye-7270-virtual-environments`  |  Checked: 2026-09-10T22:53  |  Overall: PASS  |  Beats checked: 35  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | REMOTION | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B01 | REMOTION | light | min-size §8.1: min text-run height 86px >= floor 41px | PASS | — |
| B02 | MANIM | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| B03 | VOX | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B04 | REMOTION | light | no-wordy-card §8.5: pull-quote (7 words ≤ 12) | PASS | — |
| B05 | MANIM | light | min-size §8.1: min text-run height 42px >= floor 41px | PASS | — |
| B06 | REMOTION | light | no-wordy-card §8.5: pull-quote (4 words ≤ 12) | PASS | — |
| B07 | MANIM | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B08 | REMOTION | light | no-wordy-card §8.5: pull-quote (7 words ≤ 12) | PASS | — |
| B09 | MANIM | light | min-size §8.1: min text-run height 82px >= floor 41px | PASS | — |
| B10 | VOX | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B11 | MANIM | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B12 | REMOTION | light | no-wordy-card §8.5: pull-quote (7 words ≤ 12) | PASS | — |
| B13 | REMOTION | light | no-wordy-card §8.5: pull-quote (4 words ≤ 12) | PASS | — |
| B14 | VOX | light | no-wordy-card §8.5: pull-quote (7 words ≤ 12) | PASS | — |
| B15 | MANIM | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B16 | REMOTION | light | no-wordy-card §8.5: pull-quote (7 words ≤ 12) | PASS | — |
| B17 | VOX | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B18 | MANIM | light | min-size §8.1: min text-run height 62px >= floor 41px | PASS | — |
| B19 | REMOTION | light | no-wordy-card §8.5: pull-quote (8 words ≤ 12) | PASS | — |
| B20 | MANIM | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B21 | REMOTION | light | no-wordy-card §8.5: pull-quote (7 words ≤ 12) | PASS | — |
| B22 | MANIM | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B23 | REMOTION | light | no-wordy-card §8.5: pull-quote (4 words ≤ 12) | PASS | — |
| B24 | MANIM | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B25 | REMOTION | light | no-wordy-card §8.5: pull-quote (5 words ≤ 12) | PASS | — |
| B26 | REMOTION | light | no-wordy-card §8.5: pull-quote (8 words ≤ 12) | PASS | — |
| B27 | VOX | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B28 | MANIM | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B29 | REMOTION | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B30 | VOX | light | no-wordy-card §8.5: pull-quote (6 words ≤ 12) | PASS | — |
| B31 | MANIM | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B32 | REMOTION | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B33 | REMOTION | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B34 | REMOTION | dark | min-size §8.1: min text-run height 44px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 18 | 0 |
| min-size §8.1 | 35 | 0 |
| overflow §8.2 | 35 | 0 |
| contrast §8.3 | 35 | 0 |
| contrast-local §8.3b | 35 | 0 |
| bbox-overlap §8.6b | 35 | 0 |
| card-clip §8.13 | 35 | 0 |
| kerning §8.4 | 12 | 0 |
| redundancy §8.10 (advisory) | 1 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*

## Reel-local scope

All 35 designed overlays are pixel-checked. Six archival picture insets are masked only in the checker copy: their unchanged game UI is visually inspected in the unmasked contact sheets, not treated as newly authored Brutalist labels. All thresholds remain unchanged. Terracotta in the registered mechanism scenes denotes structural borders/fills, never text. See scripts/type-gate.py.
