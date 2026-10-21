# Beat sheet: Build the Planet Express Ship in Blender, from Images

Skill: `blender-build` (brutalist.art a187fab). Narrator: the Liam voice. 19 beats, about 5.5 min estimated from word count; the real clock is the measured narration once Professor Bear renders it.

No subtitles, no captions, no .srt. The film is rendered by Professor Bear with his own tools; this folder is the film source only.

## B00 · opening · brutalist_opening · ~20.2 s

**On screen:** Brutalist opening over the hero render

**Images:** `../../renders/web/front34.jpg`
**Evidence:** observed

> This is Liam. This is the Planet Express ship, as Grok Bot finished it in Blender. This film is not the story of how it was made. It is one possible way you could build something like it yourself, starting from nothing but these pictures and a coding agent.

## B01 · read the images · body · ~18.6 s

**On screen:** Side, top and front renders side by side, axes drawn outside the ship

**Images:** `../../renders/web/side.jpg`, `../../renders/web/top.jpg`, `../../renders/web/front.jpg`
**Evidence:** observed

> Start by reading the images, not by opening Blender. Use the side view for length and height, the top view for width, and the front view for the cross-section. The quarter view looks the best and tells you the least, because perspective hides the errors.

## B02 · read the images · body · ~20.2 s

**On screen:** Side view with a 12-unit ruler; front view with width and height brackets

**Images:** `../../renders/web/side.jpg`, `../../renders/web/front.jpg`
**Evidence:** proposed

> Pick a working scale and say it out loud. Call the hull about twelve units long. From the side and front views, it's roughly a quarter as wide and a quarter as tall as it is long. That's an assumption you can check, not a fact from the original.

## B03 · block out · body · ~19.4 s

**On screen:** PROMPTS.md checkpoint 1 excerpt beside the side render

**Images:** `../../renders/web/side.jpg`
**Evidence:** proposed

> Checkpoint one: the hull blockout. One UV sphere, low resolution, scaled long along Y. Nothing else yet. Here's the prompt you give your agent: change only the hull, match its length, width and height to the side and front views, then render those two views for comparison.

## B04 · block out · body · ~17.4 s

**On screen:** Target side view with the hull top line and belly line traced

**Images:** `../../renders/web/side.jpg`
**Evidence:** observed

> Your check: lay your side render over the target side view. The top line should rise to the turret and fall to the engine, and the belly should be fuller than the back. If only the quarter view matches, you're not done.

## B05 · shape · body · ~22.2 s

**On screen:** Front three-quarter crop on the nose and red lip

**Images:** `../../renders/web/front34.jpg`
**Evidence:** proposed

> Checkpoint two: the nose. In the front quarter view, the nose narrows to a rounded point and a red rubber lip wraps it. Use loop cuts and proportional editing to taper it, or ask the agent to loft the hull from cross-sections. Then make the lip a separate object that follows the hull's edge.

## B06 · shape · body · ~17.8 s

**On screen:** Cockpit close-up, then front view

**Images:** `../../renders/web/detail_cockpit.jpg`, `../../renders/web/front.jpg`
**Evidence:** proposed

> Checkpoint three: the cockpit visor. It's a low, flat dark-teal frame with glass panes, sitting on the hull rather than floating above it. Model one frame, inset the panes, and check from the front that it isn't sunk too deep or sticking out.

## B07 · secondary forms · body · ~20.6 s

**On screen:** Top view, then turret close-up, then rear three-quarter

**Images:** `../../renders/web/top.jpg`, `../../renders/web/detail_turret.jpg`, `../../renders/web/rear34.jpg`
**Evidence:** proposed

> Checkpoint four: the fin, wings and turret. Each is its own named object. The fin is a plane outline given thickness with a Solidify modifier. Mirror the wings across the center. The turret is a simple revolved dome with a barrel. Check the roots in the top and rear views.

## B08 · repeated detail · body · ~20.6 s

**On screen:** Side view crop along the porthole row

**Images:** `../../renders/web/side.jpg`
**Evidence:** proposed

> Checkpoint five: one repeated detail, done properly. Make one porthole, a cream ring with a dark pane. Set its origin and local axes so it sits flush on the hull. Only then repeat it at the spacing you see along the side. Floating or buried portholes are the classic failure.

## B09 · repeated detail · body · ~17.4 s

**On screen:** Engine close-up

**Images:** `../../renders/web/detail_engine.jpg`
**Evidence:** proposed

> Checkpoint six: the engine. From the rear, a cream bell holds a cluster of dark nozzles. Build one nozzle, then use radial duplication around a center you set on purpose. Build only what you can see. Nobody is claiming a working engine.

## B10 · materials · body · ~14.2 s

**On screen:** Fin logo close-up and vent close-up

**Images:** `../../renders/web/detail_fin_logo.jpg`, `../../renders/web/detail_vent_wing.jpg`
**Evidence:** proposed

> Checkpoint seven: materials, only after the shape holds. Glossy teal, darker teal, cream and red, plus the logo as an image texture on the fin. Use neutral lights so you judge colour, not mood.

## B11 · compare and correct · body · ~20.6 s

**On screen:** Round 15 front render beside the front-on toy reference

**Images:** `../../compare/web/r15_ref06.jpg`
**Evidence:** observed (published comparison sheet)

> Checkpoint eight: compare and correct. Set fixed cameras and render the same front, side and rear views every time. Here's a real lesson from this model. Against the toy photo from the front, Grok Bot's round 15 nose is too narrow and pointed, and the engine bell is too big.

## B12 · compare and correct · body · ~20.2 s

**On screen:** Correction prompt excerpt from PROMPTS.md

**Images:** `../../compare/web/r15_ref06.jpg`, `../../renders/web/rear34.jpg`
**Evidence:** proposed (not demonstrated)

> So your correction prompt is narrow: keep the length and the fin, widen the front of the hull, shrink the engine bell, then render the same views again, without moving the cameras. Fix the biggest mismatch first, and only accept a change that holds in more than one view.

## B13 · rounds · body · ~22.2 s

**On screen:** Before and after, round 12 to round 15

**Images:** `../../compare/web/before_after_r12_to_r15.jpg`
**Evidence:** reported (README and review history)

> Expect rounds. This model took fifteen. At round 12, Grok Bot scored itself four out of ten, and Professor Bear said, pretty good, maybe a six out of ten, but it could use another round. Round 13 skipped the chunkier hull because of Grok Bot's own instruction. Round 15 scored five and a half.

## B14 · export · body · ~15.4 s

**On screen:** Front three-quarter render, export checklist

**Images:** `../../renders/web/front34.jpg`
**Evidence:** proposed

> Checkpoint nine: save and export. Save a numbered .blend at every checkpoint, then export a glTF. Check that the scale and the materials survived. A glTF keeps simple materials but not everything a Blender shader can do.

## B15 · recap · recap · ~17.0 s

**On screen:** Recap card over the side render

**Images:** `../../renders/web/side.jpg`
**Evidence:** recap

> Recap. Read the side, top and front views. Block out one hull. Shape the nose and visor. Add the fin, wings and turret as separate parts. Make one porthole before many. Add colour last, then compare the same views every round.

## B16 · your turn · your_turn · ~15.0 s

**On screen:** Your Turn card with the front view

**Images:** `../../renders/web/front.jpg`
**Evidence:** practice task

> Your turn. Take the round 15 front view and fix just one thing: widen the nose. Then check two things. Does the front view match the toy photo better, and does the side view still match?

## B17 · credit · credit_card · ~3.8 s

**On screen:** Credit card: 'Built by Grok Bot' / 'Narration: the Liam voice'
**Evidence:** credit

> Built by Grok Bot. Narration: the Liam voice.

## B18 · outro · outro_voice · ~6.8 s

**On screen:** Outro card per OUTRO-LOCK: exact title 'Build the Planet Express Ship in Blender, from Images', handle @NikBearBrown, one seeded mascot; spoken, no music, 1.0 s silent tail
**Evidence:** locked outro

> Build the Planet Express Ship in Blender, from Images. At Nik Bear Brown.
