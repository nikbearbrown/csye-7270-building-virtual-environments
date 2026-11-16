# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-shader-math-toolkit`  |  Checked: 2026-10-14T17:21  |  Overall: PASS  |  Beats checked: 47  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.88) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 46px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B03 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 174px >= floor 41px | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B08 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B12 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B13 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B15 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B16 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B17 | manim | light | min-size §8.1: min text-run height 188px >= floor 41px | PASS | — |
| B18 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B19 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B20 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B21 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B22 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B23 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B24 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B25 | remotion | light | no-wordy-card §8.5: pull-quote (12 words ≤ 12) | PASS | — |
| B26 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B27 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B28 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B29 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B30 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B31 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B32 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B33 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B34 | manim | light | min-size §8.1: min text-run height 711px >= floor 41px | PASS | — |
| B35 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B36 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B37 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B38 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B39 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B41 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | dark | min-size §8.1: min text-run height 102px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 19 | 0 |
| min-size §8.1 | 47 | 0 |
| overflow §8.2 | 47 | 0 |
| contrast §8.3 | 47 | 0 |
| contrast-local §8.3b | 47 | 0 |
| bbox-overlap §8.6b | 47 | 0 |
| card-clip §8.13 | 47 | 0 |
| kerning §8.4 | 23 | 0 |
| redundancy §8.10 (advisory) | 1 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
