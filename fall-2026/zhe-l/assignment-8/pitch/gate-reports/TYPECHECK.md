# TYPECHECK.md — GATE T

Reel: `walker-survival-shooting-pitch`  |  Checked: 2026-11-26T00:56  |  Overall: PASS  |  Beats checked: 19  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | media | — | no video | SKIP | — |
| B01 | manim | light | min-size §8.1: min text-run height 765px >= floor 41px | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 65px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 432px >= floor 41px | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 81px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 81px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 504px >= floor 41px | PASS | — |
| B07 | media | — | no video | SKIP | — |
| B08 | media | — | no video | SKIP | — |
| B09 | media | — | no video | SKIP | — |
| B10 | media | — | no video | SKIP | — |
| B11 | media | — | no video | SKIP | — |
| B12 | media | — | no video | SKIP | — |
| B13 | media | — | no video | SKIP | — |
| B14 | manim | light | min-size §8.1: min text-run height 192px >= floor 41px | PASS | — |
| B15 | manim | light | min-size §8.1: min text-run height 81px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B16 | manim | light | min-size §8.1: min text-run height 81px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B17 | manim | light | min-size §8.1: min text-run height 87px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BOUT | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 1 | 0 |
| min-size §8.1 | 11 | 0 |
| overflow §8.2 | 11 | 0 |
| contrast §8.3 | 11 | 0 |
| contrast-local §8.3b | 11 | 0 |
| bbox-overlap §8.6b | 11 | 0 |
| card-clip §8.13 | 11 | 0 |
| kerning §8.4 | 10 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
