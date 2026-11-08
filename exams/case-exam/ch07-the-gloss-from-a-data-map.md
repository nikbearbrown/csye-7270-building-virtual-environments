# Case 7: The hull that turned to plastic

Chapter 7, Materials and textures. Seeded flaw: a roughness (data) texture imported as an sRGB colour texture, so its values are decoded as colour and the hull looks glossy and wrong. Key terms: data texture vs colour texture, sRGB-to-linear decode, roughness, import settings, ORM.

---

# STUDENT PAGE

## Scenario
Hana is the 3D artist on a pirate-ship game. The wooden hull should look matte and weathered, but after an agent applied the roughness map from the model's texture set, the hull looks like shiny plastic in the lit scene. She asks the agent to confirm the material is correct.

## The instruction given to the agent
"Apply the hull's roughness texture from the Poly Haven set to the hull material and confirm the material setup is correct."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
hull_material (StandardMaterial3D):
  albedo_texture     = hull_diff.png   (import: Compress/Lossless, sRGB on)
  roughness_texture  = hull_rough.png  (import: Compress/Lossless, sRGB on, as imported by default)
  roughness          = 1.0
  roughness_texture_channel = Red
Checks: all 3 texture slots non-null; paths exist; attribution file present.
Result: material is correctly set up; the hull is textured.
The glossy look comes from the scene's lights, not the material.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "correctly set up" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Hana why the hull looks shiny.

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
The roughness map is data, not colour, but it was imported with the sRGB (colour) setting on, so its values are decoded as if they were colours and the roughness the shader reads is wrong (typically too low, so too shiny); the agent's checks only proved that the slots were filled.

## Terms
- **Full credit (2):** data texture vs colour texture; sRGB-to-linear decode / sRGB flag should be off for roughness (linear); import settings.
- **Half credit (1):** "wrong import setting", "texture compression", "texture is not linear" with no data/colour reasoning.
- **No credit:** "needs a normal map", "increase roughness to 1", "polygon count", "lighting is too bright" (this repeats the agent's excuse).

## Acceptable evidence requests
1. "Report the import colour-space setting for each map and show that albedo is sRGB and roughness is linear; then render the hull under a fixed light before and after and show the highlight is broader."
2. "Read back the roughness value at three known pixels of hull_rough.png in the engine and compare to the file; they should match."

**Unacceptable:** "check the slots are filled" (already claimed), "view it in the editor", "try other lights".

## Traps
- The agent blames the lights: the student must not accept that.
- Students may say "use a normal map": that is a different texture type; no credit.
- Do not accept "increase the roughness number" as the correction; roughness is already 1.0 and the map should drive the look.

- Students who agree that the lights cause the gloss have accepted the agent's excuse: Catches 0.
**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

*Check with a game developer before first use: the sRGB reading in this key.*

## Scored sample answers
**Strong (9/10).** Q1: "Roughness is a data texture, but the agent left sRGB on, so its numbers were decoded as colour, giving wrong roughness. It also accepted 'lights' as the cause without evidence." Q2: "Report each map's import setting: albedo sRGB, roughness linear, then render under a fixed light." Q3: "Turn off sRGB on hull_rough.png (import as linear/data), re-import, and show the before and after render." Q4: "The map that says how rough each spot is got read as a picture instead of numbers, so the wood came out too shiny." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 never says what Hana should expect to see after the fix.*

**Typical (6/10).** Q1: "The roughness texture was imported wrong. The sRGB should not be on." Q2: "Look at it in the game with a fixed light." Q3: "Turn off sRGB on the roughness texture." Q4: "The roughness image was read the wrong way, so the wood is shiny." *Catches 3; Term 1 (sRGB named, no data vs colour); Evidence 1 (fixed light render but no pass/fail); Fix 1 (turns off sRGB, no re-import or before/after); Scope 0 (unclear in 'read the wrong way').* Total 6. *Reason: correct, short, no reasoning about data vs colour.*

**Fluent but wrong (3/10).** Q1: "The material needs an ORM channel pack with a metallic channel and a normal map, and the hull needs SSAO so the specular energy is conserved." Q2: "Enable SSAO and inspect the energy conservation in the render." Q3: "Add an ORM texture and enable SSAO." Q4: "The hull needs more detail maps." *Catches 0; Term 0; Evidence 1 (a render check, wrong target); Fix 1; Scope 1.* Total 3. *Reason: material vocabulary that skips the import setting.*
