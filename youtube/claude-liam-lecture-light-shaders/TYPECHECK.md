# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-light-shaders`  |  Checked: 2026-10-14T13:25  |  Overall: PASS  |  Beats checked: 46  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.97) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 46px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 57px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B03 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B05 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B06 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B09 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B13 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B14 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B15 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B16 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B17 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B18 | remotion | light | no-wordy-card §8.5: pull-quote (12 words ≤ 12) | PASS | — |
| B19 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B20 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B21 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B22 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B23 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B24 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B25 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B26 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B27 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B28 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B29 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B30 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B31 | manim | light | min-size §8.1: min text-run height 48px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B32 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B33 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B34 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B35 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B36 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B37 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B38 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B39 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | remotion | light | no-wordy-card §8.5: pull-quote (11 words ≤ 12) | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | dark | min-size §8.1: min text-run height 224px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 29 | 0 |
| min-size §8.1 | 46 | 0 |
| overflow §8.2 | 46 | 0 |
| contrast §8.3 | 46 | 0 |
| contrast-local §8.3b | 46 | 0 |
| bbox-overlap §8.6b | 46 | 0 |
| card-clip §8.13 | 46 | 0 |
| kerning §8.4 | 12 | 0 |
| redundancy §8.10 (advisory) | 1 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
