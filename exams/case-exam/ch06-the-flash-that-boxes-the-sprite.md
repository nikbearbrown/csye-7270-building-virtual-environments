# Case 6: The failure flash that draws a box

Chapter 6, Shader foundations. Seeded flaw: a `canvas_item` fragment shader overwrites the alpha channel (RGBA) with 1.0, so the transparent area around a sprite becomes a solid rectangle; the agent claimed success because the shader compiled. Key terms: fragment shader, RGBA / alpha channel, mix, discard, compile vs looks right.

---

# STUDENT PAGE

## Scenario
Anjali is the art director of a 2D platformer. When the hero fails a run she wants the sprite to tint toward dark ink and then fade back before the retry. The sprite is a cutout character: only the character is opaque and the rest of the rectangle is transparent. She asks the agent to add the flash.

## The instruction given to the agent
"Add a failure flash shader to the hero sprite: tint toward the ink colour when a run fails, then fade back before the retry. Tell me when it is done."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Added flash.gdshader (shader_type canvas_item):
  uniform vec4 ink : source_color = vec4(0.11, 0.09, 0.07, 1.0);
  uniform float flash : hint_range(0.0, 1.0) = 0.0;
  void fragment() {
      vec4 tex = texture(TEXTURE, UV);
      COLOR = mix(tex, ink, flash);
  }
hero.gd sets `material.set_shader_parameter("flash", f)` and tweens f 1 -> 0.
Checks: godot --headless --quit loaded the shader with no compile errors.
Tween test: flash parameter reaches 1.0 then 0.0. PASS.
Done: the failure flash works.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "the failure flash works" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Anjali what she will see on screen when the hero fails.

---

# TA RUBRIC PAGE (not for students)

## The fixed rubric
| Row | Pts | Awarded for |
|---|---|---|
| Catches the flaw | 3 | Q1 |
| Exact term | 2 | Q1 |
| Asks for evidence | 2 | Q2 |
| Fix or next step | 2 | Q3 |
| Scope and plain language | 1 | Q4 |

## The flaw in one sentence
`mix(tex, ink, flash)` mixes all four RGBA channels, so as `flash` rises the alpha of the transparent area rises to the ink's alpha of 1.0 and a dark rectangle appears around the sprite; the checks (compiles, parameter reaches 1.0) cannot see this, so "done" has no visual evidence.

## Terms
- **Full credit (2):** alpha channel / RGBA overwritten (alpha should be kept from the texture: mix only `.rgb`, keep `tex.a`); compile error vs visual bug.
- **Half credit (1):** "the transparency is lost", "the shader tints the whole sprite sheet", "should use modulate" with no mention of alpha.
- **No credit:** "wrong shader type", "uniform should be a varying", "TIME is not used".

## Acceptable evidence requests
1. "Render one frame with flash = 1.0 over a bright background and show a screenshot; the area outside the character must still show the background."
2. "Test the fragment output at a transparent pixel: with flash = 1.0, alpha at that pixel must still be 0."

**Unacceptable:** "Check it compiled again", "check the parameter reaches 1.0" (already checked), "run the game and tell me if it looks fine" (no pass/fail).

## Traps
- Students may say the tint is not strong enough or that the ink is wrong colour: not the flaw.
- A student who names "compiled is not the same as looks right" without finding the alpha issue gets Catches 1/3, Term 1.
- A student who suggests the Modulate property of the sprite as an alternative may be correct as a fix (credit Fix 2 if alpha handling is named).

**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

*Check with a game developer before first use: the shader reading in this key.*

## Scored sample answers
**Strong (9/10).** Q1: "`mix` runs on all four channels, so alpha is mixed toward the ink's alpha of 1. The transparent background turns opaque and shows as a dark box. Alpha should be kept from the texture. The checks only proved it compiles and the number moves." Q2: "Render one frame at flash = 1.0 over a bright background and check the area outside the sprite still shows the background." Q3: "Mix only the rgb and set COLOR.a to the texture's alpha, then show the screenshot." Q4: "She will see a dark square around the hero instead of just the hero turning dark." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 describes the bug, as asked, but does not say what will be seen after the fix.*

**Typical (6/10).** Q1: "The shader does not keep the transparent part. The background will show." Q2: "Take a screenshot." Q3: "Make sure the transparent part stays transparent." Q4: "A box will show around the hero." *Catches 3; Term 1 (transparency, no alpha/RGBA); Evidence 0 (screenshot with no pass/fail condition); Fix 1 (right goal, no mechanism); Scope 1.* Total 6. *Reason: right observation in plain words.*

**Fluent but wrong (3/10).** Q1: "The flash should be done in the vertex shader, because per-vertex colour interpolation is cheaper and TIME should drive it, not a tween." Q2: "Profile GPU time with the flash active." Q3: "Move the tint into vertex() and use TIME." Q4: "The effect is in the wrong part of the shader." *Catches 0; Term 0 (stage names used but not tied to the problem); Evidence 1 (a measurement, wrong target); Fix 1 (specific, wrong); Scope 1.* Total 3. *Reason: real shader vocabulary, wrong problem.*
