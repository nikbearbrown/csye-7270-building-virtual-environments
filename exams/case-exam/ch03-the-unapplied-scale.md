# Case 3: The checkpoint post that was "2 metres"

Chapter 3, 3D assets and the Blender pipeline. Seeded flaw: size reported from the object's scale-adjusted view in Blender while a non-uniform scale was left on the object instead of being applied, so the exported model's real mesh size, and its collision hull, are wrong in Godot. Key terms: apply transforms, node scale vs mesh size, unit, collision shape vs visual mesh.

---

# STUDENT PAGE

## Scenario
Wei is the level designer of a 3D platformer. He needs a checkpoint post that is 2 metres tall so the player can see it from one jump away. A modeller made it in Blender, and the coding agent exported it to Godot. In the test level the post looks the right height but the player stops about a metre short of touching it and sometimes bounces off the air beside it.

## The instruction given to the agent
"Export the checkpoint post from Blender to Godot at 2 metres tall with a collision hull around it. Confirm the size."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Blender check (units: metres, scale 1.0 on the unit system):
  post object dimensions: 0.4 x 0.4 x 2.0 m     -> height 2.0 m, confirmed.
  object scale: (1.0, 1.0, 4.0)   (mesh drawn 0.5 m tall, stretched on Z)
  collision hull object "post-col": scale (1,1,1), size 0.4 x 0.4 x 0.5 m
Exported checkpoint.glb. Placed at the pad; Godot shows a 2 m tall post.
Collision: hull imported from "post-col".
Conclusion: size confirmed at 2 m; collision matches the post.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "collision matches the post" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Wei why the player stops short of the post.

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
The post's 2 m height comes from an object scale of 4 stretched over a 0.5 m mesh (the transform was not applied), while the collision hull has scale 1 and is only 0.5 m tall, so the visual mesh and the collider disagree and "confirmed" rested on the wrong number.

## Terms
- **Full credit (2):** apply transforms / scale left on the object (node scale) vs real mesh size; collision shape not matching the visual mesh.
- **Half credit (1):** "units are wrong", "scale problem", "axis problem", "collider too small" with no link to the unapplied transform.
- **No credit:** "poly count", "wrong file format", "export setting".

## Acceptable evidence requests
1. "Apply all transforms in Blender, re-export, and report the mesh bounding box and the collision shape size in Godot from a headless script; both must be 0.4 x 0.4 x 2.0 m with node scale (1,1,1)."
2. "Print the node scale and the collision-shape extents for the post and hull in Godot; show they match within 1 cm."

**Unacceptable:** "Open it in Godot and look", "confirm in Blender again", "check the polygon count".

## Traps
- The Blender "dimensions" number includes the object scale; students who say "the dimensions were right so the size is fine" have missed it.
- Students may blame Z-up/Y-up axes. Credit the catch only if they notice the hull vs mesh mismatch or the unapplied scale.
- A student who spots the mismatched hull but not the scale gets Catches 2/3 and Term 1.

**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

## Scored sample answers
**Strong (9/10).** Q1: "The scale of 4 on Z was left on the object instead of applying transforms, so the mesh is really 0.5 m tall and the 2 m comes only from stretching. The hull is a true 0.5 m with scale 1, so the collider does not match the visual mesh." Q2: "Print the node scale and mesh/collider extents in Godot; they should both be 2 m with scale 1." Q3: "In Blender, apply transforms to both objects, re-export, then show the post and hull extents in Godot." Q4: "The post looks tall but the invisible wall around it is only a quarter as tall and in the wrong place, so the player meets the wall, not the post." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 misstates where the hull is ("wrong place").*

**Typical (6/10).** Q1: "The scale is 4 but the mesh is 0.5. The scale should be applied." Q2: "Check the size in Godot." Q3: "Apply the scale and export again." Q4: "The invisible box is smaller than the post." *Catches 3; Term 1 (says apply, no node-scale vs mesh-size or collider mismatch); Evidence 0 ("check the size" has no number); Fix 1 (applies the object but does not mention the hull or re-measure); Scope 1.* Total 6. *Reason: right catch, thin on terms and evidence.*

**Fluent but wrong (3/10).** Q1: "Blender is Z-up and glTF is Y-up, so the export has the axis conversion applied twice and the collision hull is rotated; the post should be exported with -Y forward." Q2: "Check the glTF axis settings in the exporter." Q3: "Re-export with +Y up unchecked." Q4: "The post is the wrong way up for the game." *Catches 0 (a real concept from the chapter, but not what is wrong here: the post stands upright); Term 0; Evidence 1 (checks a setting, not size); Fix 1 (concrete but wrong); Scope 1.* Total 3. *Reason: plausible chapter jargon, misapplied.*
