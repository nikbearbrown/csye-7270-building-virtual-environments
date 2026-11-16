# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-godot-shader-language`  |  Checked: 2026-10-14T17:42  |  Overall: PASS  |  Beats checked: 47  |  FAILs: 0

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
| B02 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B05 | remotion | light | no-wordy-card §8.5: pull-quote (7 words ≤ 12) | PASS | — |
| B06 | terminal | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 221px >= floor 41px | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B11 | terminal | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 66px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B15 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B16 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B17 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B18 | terminal | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B19 | manim | light | min-size §8.1: min text-run height 166px >= floor 41px | PASS | — |
| B20 | manim | light | min-size §8.1: min text-run height 62px >= floor 41px | PASS | — |
| B21 | manim | light | min-size §8.1: min text-run height 485px >= floor 41px | PASS | — |
| B22 | terminal | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B23 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B24 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B25 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B26 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B27 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B28 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B29 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B30 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B31 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B32 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B33 | remotion | light | no-wordy-card §8.5: pull-quote (10 words ≤ 12) | PASS | — |
| B34 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B35 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B36 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B37 | manim | light | min-size §8.1: min text-run height 474px >= floor 41px | PASS | — |
| B38 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B39 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B40 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B41 | terminal | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
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
| no-wordy-card §8.5 | 20 | 0 |
| min-size §8.1 | 47 | 0 |
| overflow §8.2 | 47 | 0 |
| contrast §8.3 | 47 | 0 |
| contrast-local §8.3b | 47 | 0 |
| bbox-overlap §8.6b | 47 | 0 |
| card-clip §8.13 | 47 | 0 |
| kerning §8.4 | 22 | 0 |
| redundancy §8.10 (advisory) | 6 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
