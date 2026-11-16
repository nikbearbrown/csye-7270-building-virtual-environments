# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-shaders-in-3d`  |  Checked: 2026-10-14T16:59  |  Overall: PASS  |  Beats checked: 50  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.97) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 46px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 48px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B06 | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B07 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B08 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B10 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B11 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B12 | remotion | light | no-wordy-card §8.5: pull-quote (8 words ≤ 12) | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 253px >= floor 41px | PASS | — |
| B14 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B15 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B16 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B17 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B18 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B19 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B20 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B21 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B22 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B23 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B24 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B25 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B26 | remotion | light | no-wordy-card §8.5: pull-quote (12 words ≤ 12) | PASS | — |
| B27 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B28 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B29 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B30 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B31 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B32 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B33 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B34 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B35 | manim | light | min-size §8.1: min text-run height 48px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B36 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B37 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B38 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B39 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B41 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B42 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B43 | editor | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B44 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | light | min-size §8.1: min text-run height 44px >= floor 41px (individual-char fallback at 2×) | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 31 | 0 |
| min-size §8.1 | 50 | 0 |
| overflow §8.2 | 50 | 0 |
| contrast §8.3 | 50 | 0 |
| contrast-local §8.3b | 50 | 0 |
| bbox-overlap §8.6b | 50 | 0 |
| card-clip §8.13 | 50 | 0 |
| kerning §8.4 | 14 | 0 |
| redundancy §8.10 (advisory) | 2 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
