# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-blender-to-godot`  |  Checked: 2026-10-06T14:50  |  Overall: PASS  |  Beats checked: 80  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.6 GOLDEN STRINGS:**

> - B67B: headline 89 chars — adversarial overflow risk (golden LONGEST test fails at this length)

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.95) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BIDEA | bookend | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B07 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B11 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B15 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B16 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B17 | manim | light | min-size §8.1: min text-run height 252px >= floor 41px | PASS | — |
| B18 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B19 | manim | light | min-size §8.1: min text-run height 70px >= floor 41px | PASS | — |
| B20 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B21 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B22 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B23 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B24 | manim | light | min-size §8.1: min text-run height 596px >= floor 41px | PASS | — |
| B25 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B26 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B27 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B28 | manim | light | min-size §8.1: min text-run height 96px >= floor 41px | PASS | — |
| B29 | manim | light | min-size §8.1: min text-run height 645px >= floor 41px | PASS | — |
| B30 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B31 | manim | light | min-size §8.1: min text-run height 56px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B32 | manim | light | min-size §8.1: min text-run height 56px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B33A | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B33B | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B34 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B35 | manim | light | min-size §8.1: min text-run height 280px >= floor 41px | PASS | — |
| B36 | manim | light | min-size §8.1: min text-run height 44px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B37 | manim | light | min-size §8.1: min text-run height 266px >= floor 41px | PASS | — |
| B38 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B39 | manim | light | min-size §8.1: min text-run height 58px >= floor 41px | PASS | — |
| B40 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B41 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B42 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B43 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B44 | manim | light | min-size §8.1: min text-run height 287px >= floor 41px | PASS | — |
| B45 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B46 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B47A | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B47B | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B48 | remotion | dark | min-size §8.1: hand-drawn pattern (CCSession) — §8.1 hachure/crossbar fragments are false … | PASS | — |
| B49 | remotion | dark | min-size §8.1: hand-drawn pattern (CCSession) — §8.1 hachure/crossbar fragments are false … | PASS | — |
| B50 | remotion | dark | min-size §8.1: hand-drawn pattern (CCSession) — §8.1 hachure/crossbar fragments are false … | PASS | — |
| B51 | remotion | dark | min-size §8.1: hand-drawn pattern (CCSession) — §8.1 hachure/crossbar fragments are false … | PASS | — |
| B52 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B53 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px | PASS | — |
| B54 | remotion | dark | min-size §8.1: hand-drawn pattern (CCSession) — §8.1 hachure/crossbar fragments are false … | PASS | — |
| B55 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B56 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B57 | manim | light | min-size §8.1: min text-run height 231px >= floor 41px | PASS | — |
| B58 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B59 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B60 | manim | light | min-size §8.1: min text-run height 59px >= floor 41px | PASS | — |
| B61 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B62 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B63 | manim | light | min-size §8.1: min text-run height 66px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B64 | manim | light | min-size §8.1: min text-run height 41px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B65 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B66 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B67A | manim | light | min-size §8.1: min text-run height 51px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B67B | remotion | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B68 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B69 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B70 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B71A | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B71B | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | light | min-size §8.1: min text-run height 98px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 5 | 0 |
| min-size §8.1 | 80 | 0 |
| overflow §8.2 | 80 | 0 |
| contrast §8.3 | 80 | 0 |
| contrast-local §8.3b | 80 | 0 |
| bbox-overlap §8.6b | 80 | 0 |
| card-clip §8.13 | 80 | 0 |
| kerning §8.4 | 66 | 0 |
| redundancy §8.10 (advisory) | 3 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
