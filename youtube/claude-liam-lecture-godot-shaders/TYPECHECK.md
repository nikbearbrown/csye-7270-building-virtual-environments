# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-godot-shaders`  |  Checked: 2026-10-14T18:10  |  Overall: PASS  |  Beats checked: 49  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.93) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 46px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 55px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B04 | remotion | light | no-wordy-card §8.5: pull-quote (11 words ≤ 12) | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B06 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B10 | editor | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B11 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B13 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B14 | remotion | light | no-wordy-card §8.5: pull-quote (11 words ≤ 12) | PASS | — |
| B15 | manim | light | min-size §8.1: min text-run height 105px >= floor 41px | PASS | — |
| B16 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B17 | manim | light | min-size §8.1: min text-run height 56px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B18 | manim | light | min-size §8.1: min text-run height 66px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B19 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B20 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B21 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B22 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B23 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B24 | remotion | light | no-wordy-card §8.5: pull-quote (10 words ≤ 12) | PASS | — |
| B25 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B26 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B27 | editor | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B28 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B29 | remotion | light | no-wordy-card §8.5: pull-quote (8 words ≤ 12) | PASS | — |
| B30 | manim | light | min-size §8.1: min text-run height 241px >= floor 41px | PASS | — |
| B31 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B32 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B33 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B34 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B35 | remotion | light | no-wordy-card §8.5: pull-quote (8 words ≤ 12) | PASS | — |
| B36 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B37 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B38 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B39 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B41 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B42 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B43 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
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
| no-wordy-card §8.5 | 26 | 0 |
| min-size §8.1 | 49 | 0 |
| overflow §8.2 | 49 | 0 |
| contrast §8.3 | 49 | 0 |
| contrast-local §8.3b | 49 | 0 |
| bbox-overlap §8.6b | 49 | 0 |
| card-clip §8.13 | 49 | 0 |
| kerning §8.4 | 18 | 0 |
| redundancy §8.10 (advisory) | 1 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
