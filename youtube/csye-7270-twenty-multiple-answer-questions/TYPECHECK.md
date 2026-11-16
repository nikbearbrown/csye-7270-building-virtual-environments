# TYPECHECK.md — GATE T

Reel: `csye-7270-twenty-multiple-answer-questions`  |  Checked: 2026-11-15T12:29  |  Overall: PASS  |  Beats checked: 17  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BIDEA | bookend | light | min-size §8.1: min text-run height 59px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B00 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B00A | manim | light | min-size §8.1: min text-run height 45px >= floor 41px | PASS | — |
| B01 | manim | light | min-size §8.1: min text-run height 46px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 169px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 46px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 44px >= floor 41px | PASS | — |
| B16 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B17 | manim | light | min-size §8.1: min text-run height 46px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B18 | manim | light | min-size §8.1: min text-run height 169px >= floor 41px | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | dark | min-size §8.1: min text-run height 66px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 1 | 0 |
| min-size §8.1 | 17 | 0 |
| overflow §8.2 | 17 | 0 |
| contrast §8.3 | 17 | 0 |
| contrast-local §8.3b | 17 | 0 |
| bbox-overlap §8.6b | 17 | 0 |
| card-clip §8.13 | 17 | 0 |
| kerning §8.4 | 13 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
