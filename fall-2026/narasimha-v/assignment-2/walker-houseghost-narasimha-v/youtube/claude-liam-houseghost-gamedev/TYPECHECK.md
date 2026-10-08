# TYPECHECK.md — GATE T

Reel: `claude-liam-houseghost-gamedev`  |  Checked: 2026-10-07T22:23  |  Overall: **FAIL**  |  Beats checked: 25  |  FAILs: 9

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.7–§8.9 PLACEHOLDER / TRUNCATION — GATE BLOCKED:**
> Every item below must be fixed before `./art run` or `./art final`.
> Labels must be authored short phrases (2–5 words). Subs must add something real
> (≤8 words) or be omitted. 'see narration' and truncated strings must not reach
> a rendered surface.

> - §8.10 [B00/greeting] ClaudeComposerAsk has empty or missing greeting — B00 needs '<world-language hello>, Liam', BHTF needs 'Your turn.', body beats need ≤4 words compressed from the beat narration
> - §8.10 [B22/greeting] ClaudeComposerAsk has empty or missing greeting — B00 needs '<world-language hello>, Liam', BHTF needs 'Your turn.', body beats need ≤4 words compressed from the beat narration

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [B01] narration recites the card (1.00) — discuss it, don't read it
> - §8.10 [B06] narration recites the card (0.84) — discuss it, don't read it
> - §8.10 [B17] narration recites the card (0.91) — discuss it, don't read it
> - §8.10 [B20] narration recites the card (0.92) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B01 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B02 | ? | dark | min-size §8.1: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B03 | ? | dark | min-size §8.1: min text-run height 41px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B04 | ? | — | no-wordy-card §8.5: no prose payload found | PASS | — |
| B05 | ? | dark | contrast §8.3: dark-frame fg/bg contrast 4.00:1 < 4.5:1 WCAG (fg≈(173, 177, 174), bg≈(72, … | **FAIL** | Use INK on cream; add backing plate under accent text |
| B06 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B07 | ? | dark | min-size §8.1: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B08 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B08R | ? | dark | contrast §8.3: dark-frame fg/bg contrast 4.13:1 < 4.5:1 WCAG (fg≈(168, 173, 174), bg≈(68, … | **FAIL** | Use INK on cream; add backing plate under accent text |
| B09 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B11 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B12 | ? | light | contrast §8.3: terracotta accent #D97757 on cream 2.74:1 < 4.5:1 WCAG — accent text must s… | **FAIL** | Use INK on cream; add backing plate under accent text |
| B13 | ? | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B14 | ? | dark | contrast §8.3: dark-frame fg/bg contrast 4.00:1 < 4.5:1 WCAG (fg≈(173, 177, 174), bg≈(72, … | **FAIL** | Use INK on cream; add backing plate under accent text |
| B15 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B16 | ? | dark | contrast §8.3: dark-frame fg/bg contrast 4.00:1 < 4.5:1 WCAG (fg≈(173, 177, 174), bg≈(72, … | **FAIL** | Use INK on cream; add backing plate under accent text |
| B17 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B18 | ? | light | no-wordy-card §8.5: 3 prose elements (15 words) > budget 2 (1 display + 1 label). Detail: … | **FAIL** | De-wordify → Manim diagram or Remotion build-on |
| B19 | ? | light | no-wordy-card §8.5: 5 prose elements (39 words) > budget 2 (1 display + 1 label). Detail: … | **FAIL** | De-wordify → Manim diagram or Remotion build-on |
| B20 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B21 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B22 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B23 | ? | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

### SWEEP GATES §8.7–§8.12b (placeholder / truncation / code-card)

- **§8.10 [B00/greeting] ClaudeComposerAsk has empty or missing greeting — B00 needs '<world-language hello>, Liam', BHTF needs 'Your turn.', body beats need ≤4 words compressed from the beat narration**
- **§8.10 [B22/greeting] ClaudeComposerAsk has empty or missing greeting — B00 needs '<world-language hello>, Liam', BHTF needs 'Your turn.', body beats need ≤4 words compressed from the beat narration**

**Fix:** §8.7–§8.9: rewrite flagged labels/subs to authored words. §8.12: replace prose-comment code beat with FormACard or ClaudeVerdictArtifact. §8.12b: give ClaudeCodeBeat a real filename title (e.g. 'analysis.py').

### B02 (?)
- **min-size §8.1**: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast-local §8.3b**: per-blob contrast 1.99:1 < 3.0:1 — text unreadable on actual local background (blob@(2690,968)–(2770,1003) fg≈(198, 151, 84) bg≈(140, 100, 56)); move label off its background or change text color
- **Fix:** Increase font_size in scenes.py or Remotion component

### B05 (?)
- **contrast §8.3**: dark-frame fg/bg contrast 4.00:1 < 4.5:1 WCAG (fg≈(173, 177, 174), bg≈(72, 76, 78)); check text colors on dark background beat
- **Fix:** Use INK on cream; add backing plate under accent text

### B07 (?)
- **min-size §8.1**: smallest text run 35px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **contrast §8.3**: dark-frame fg/bg contrast 3.93:1 < 4.5:1 WCAG (fg≈(204, 158, 104), bg≈(80, 67, 57)); check text colors on dark background beat
- **contrast-local §8.3b**: per-blob contrast 2.33:1 < 3.0:1 — text unreadable on actual local background (blob@(2649,1190)–(2719,1225) fg≈(190, 141, 90) bg≈(110, 86, 65)); move label off its background or change text color
- **Fix:** Increase font_size in scenes.py or Remotion component

### B08R (?)
- **contrast §8.3**: dark-frame fg/bg contrast 4.13:1 < 4.5:1 WCAG (fg≈(168, 173, 174), bg≈(68, 71, 73)); check text colors on dark background beat
- **Fix:** Use INK on cream; add backing plate under accent text

### B12 (?)
- **contrast §8.3**: terracotta accent #D97757 on cream 2.74:1 < 4.5:1 WCAG — accent text must switch to INK #3D3929 or carry a backing plate
- **contrast-local §8.3b**: per-blob contrast 1.66:1 < 3.0:1 — text unreadable on actual local background (blob@(2994,1100)–(3099,1147) fg≈(90, 58, 32) bg≈(134, 87, 43)); move label off its background or change text color
- **Fix:** Use INK on cream; add backing plate under accent text

### B14 (?)
- **contrast §8.3**: dark-frame fg/bg contrast 4.00:1 < 4.5:1 WCAG (fg≈(173, 177, 174), bg≈(72, 76, 78)); check text colors on dark background beat
- **contrast-local §8.3b**: per-blob contrast 2.58:1 < 3.0:1 — text unreadable on actual local background (blob@(1889,495)–(1935,525) fg≈(136, 141, 151) bg≈(75, 76, 79)); move label off its background or change text color
- **Fix:** Use INK on cream; add backing plate under accent text

### B16 (?)
- **contrast §8.3**: dark-frame fg/bg contrast 4.00:1 < 4.5:1 WCAG (fg≈(173, 177, 174), bg≈(72, 76, 78)); check text colors on dark background beat
- **Fix:** Use INK on cream; add backing plate under accent text

### B18 (?)
- **no-wordy-card §8.5**: 3 prose elements (15 words) > budget 2 (1 display + 1 label). Detail: 3 output lines (15 words). De-wordify: rebuild as Manim process diagram or Remotion build-on; keep on-screen words to labels only.
- **Fix:** De-wordify → Manim diagram or Remotion build-on

### B19 (?)
- **no-wordy-card §8.5**: 5 prose elements (39 words) > budget 2 (1 display + 1 label). Detail: 5 output lines (39 words). De-wordify: rebuild as Manim process diagram or Remotion build-on; keep on-screen words to labels only.
- **Fix:** De-wordify → Manim diagram or Remotion build-on

---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 9 | 2 |
| min-size §8.1 | 24 | 2 |
| overflow §8.2 | 24 | 0 |
| contrast §8.3 | 24 | 6 |
| contrast-local §8.3b | 24 | 4 |
| bbox-overlap §8.6b | 24 | 0 |
| card-clip §8.13 | 24 | 0 |
| kerning §8.4 | 0 | 0 |
| redundancy §8.10 (advisory) | 6 | 4 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
