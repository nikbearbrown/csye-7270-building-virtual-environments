# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-what-is-pbr`  |  Checked: 2026-11-13T17:03  |  Overall: PASS  |  Beats checked: 16  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.94) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 62px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01 | body | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B02 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B05 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B06 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B07 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B08 | body | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B09 | remotion | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | body | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | light | min-size §8.1: min text-run height 103px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 8 | 0 |
| min-size §8.1 | 16 | 0 |
| overflow §8.2 | 16 | 0 |
| contrast §8.3 | 16 | 0 |
| contrast-local §8.3b | 16 | 0 |
| bbox-overlap §8.6b | 16 | 0 |
| card-clip §8.13 | 16 | 0 |
| kerning §8.4 | 3 | 0 |
| redundancy §8.10 (advisory) | 1 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
