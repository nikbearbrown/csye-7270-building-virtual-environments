# TYPECHECK.md — GATE T

Reel: `claude-liam-lecture-godot-shading-language`  |  Checked: 2026-10-13T15:06  |  Overall: **FAIL**  |  Beats checked: 58  |  FAILs: 11

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.7–§8.9 PLACEHOLDER / TRUNCATION — GATE BLOCKED:**
> Every item below must be fixed before `./art run` or `./art final`.
> Labels must be authored short phrases (2–5 words). Subs must add something real
> (≤8 words) or be omitted. 'see narration' and truncated strings must not reach
> a rendered surface.

> - §8.12b [B22/title] doubled-title: 'uniform.gdshader (declarations)' has no file extension — ClaudeCodeBeat echoes the full title as the language badge. Use a filename (e.g. 'analysis.py') or fix the content to real code
> - §8.12b [B23/title] doubled-title: 'uniform.gdshader + lab.gd (excerpts)' has no file extension — ClaudeCodeBeat echoes the full title as the language badge. Use a filename (e.g. 'analysis.py') or fix the content to real code
> - §8.12b [B26/title] doubled-title: 'instance.gdshader + lab.gd (excerpts)' has no file extension — ClaudeCodeBeat echoes the full title as the language badge. Use a filename (e.g. 'analysis.py') or fix the content to real code
> - §8.12b [B32/title] doubled-title: 'switch.gdshader (fragment excerpt)' has no file extension — ClaudeCodeBeat echoes the full title as the language badge. Use a filename (e.g. 'analysis.py') or fix the content to real code

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [BVDT] narration recites the card (0.97) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | bookend | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 59px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| BACT1 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B01 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B02 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B02A | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B05 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B06 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B06A | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B07 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| BACT2 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B08 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B09 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B10 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B11 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B12 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B13 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B14 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| BACT3 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B15 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B16 | shell | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B17 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B18 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B19 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B20 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B21 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| BACT4 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B22 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B23 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B24 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B25 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B26 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B27 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B28 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| BACT5 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B29 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B30 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B31 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B32 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B33 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B34 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B35 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| BACT6 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B36 | code | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B37 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B38 | shell | dark | no-wordy-card §8.5: no prose payload found | PASS | — |
| B39 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B40 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B41 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B42 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B43 | capture | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B44 | manim | light | min-size §8.1: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| BVDT | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | dark | min-size §8.1: min text-run height 239px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

### SWEEP GATES §8.7–§8.12b (placeholder / truncation / code-card)

- **§8.12b [B22/title] doubled-title: 'uniform.gdshader (declarations)' has no file extension — ClaudeCodeBeat echoes the full title as the language badge. Use a filename (e.g. 'analysis.py') or fix the content to real code**
- **§8.12b [B23/title] doubled-title: 'uniform.gdshader + lab.gd (excerpts)' has no file extension — ClaudeCodeBeat echoes the full title as the language badge. Use a filename (e.g. 'analysis.py') or fix the content to real code**
- **§8.12b [B26/title] doubled-title: 'instance.gdshader + lab.gd (excerpts)' has no file extension — ClaudeCodeBeat echoes the full title as the language badge. Use a filename (e.g. 'analysis.py') or fix the content to real code**
- **§8.12b [B32/title] doubled-title: 'switch.gdshader (fragment excerpt)' has no file extension — ClaudeCodeBeat echoes the full title as the language badge. Use a filename (e.g. 'analysis.py') or fix the content to real code**

**Fix:** §8.7–§8.9: rewrite flagged labels/subs to authored words. §8.12: replace prose-comment code beat with FormACard or ClaudeVerdictArtifact. §8.12b: give ClaudeCodeBeat a real filename title (e.g. 'analysis.py').

### B01 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B07 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B09 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B11 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B14 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B17 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B19 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B30 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B33 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B35 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B44 (manim)
- **min-size §8.1**: smallest text run 37px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 42 | 0 |
| min-size §8.1 | 58 | 11 |
| overflow §8.2 | 58 | 0 |
| contrast §8.3 | 58 | 0 |
| contrast-local §8.3b | 58 | 0 |
| bbox-overlap §8.6b | 58 | 0 |
| card-clip §8.13 | 58 | 0 |
| kerning §8.4 | 11 | 0 |
| redundancy §8.10 (advisory) | 3 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
