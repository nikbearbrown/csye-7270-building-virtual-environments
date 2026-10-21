# Prompts: build a Planet Express-style ship from images

For a fresh coding-agent chat. Attach these published images (download from the gallery listed in SOURCES.md): `side.jpg` (right side), `top.jpg` (top, nose toward the bottom), `front.jpg` (front), `front34.jpg` (front three-quarter), `rear34.jpg` (rear three-quarter), plus the close-ups `detail_cockpit.jpg`, `detail_engine.jpg`, `detail_turret.jpg`, `detail_fin_logo.jpg`, `detail_vent_wing.jpg`. Your agent needs either Blender control or the ability to write a script you paste into Blender's Scripting workspace.

## Starter

> Help me learn Blender by building a stylized delivery spaceship from the attached images: side.jpg (right side), top.jpg (top view, nose at the bottom), front.jpg (front), front34.jpg and rear34.jpg. These images are all I have; do not assume any original model, STL kit, blueprints or scripts. First describe the visible major forms and any uncertainty caused by perspective. Propose a short sequence of modeling checkpoints and the Blender concept behind each. Use X for width, Y for length, Z for height. Use a working scale of about 12 units for hull length and label it an assumption. Start with only the hull blockout. If you can control Blender, work in a new scene and save `ship_c1.blend`; otherwise give me a script for the Scripting workspace and a manual alternative. Render front, side and quarter views. Tell me what you actually executed and what is still a proposal.

## C1: hull

> Change only the hull. Match its length, its height profile (rising to the turret, falling to the engine, fuller belly) to side.jpg, and its width and height to front.jpg. Render side and front views from fixed cameras and tell me the remaining disagreement. Success: my side render overlays the target's top line and belly within a small margin.

## C2: nose and lip

> Keep the hull length. Taper the nose to the rounded point in front34.jpg using loop cuts and proportional editing (or by editing the cross-sections), and add the red lip as a separate object that follows the hull edge. Render front and front three-quarter. Success: the nose is rounded, not needle-pointed, in front.jpg's view.

## C3: visor

> Add the cockpit visor from detail_cockpit.jpg as a separate named object: a low flat dark-teal frame with inset glass panes, seated on the hull surface. Explain where you put its origin. Success: in the front view it neither floats nor sinks.

## C4: fin, wings, turret

> Add the fin (plane outline + Solidify), the two wings (one wing + Mirror) and the turret (revolved dome, barrel, antenna) as separate named objects, matching top.jpg, rear34.jpg and detail_turret.jpg. Show top and rear views before adding trim. Success: roots and tips line up with the references; no guessed mechanisms.

## C5: one porthole, then many

> Make one porthole (cream ring, dark pane) and explain its local axes and depth. Wait for me to check it. Then repeat it at the spacing in side.jpg. Success: no floating or buried portholes.

## C6: engine

> Build the visible engine from detail_engine.jpg and rear34.jpg: a cream bell and a cluster of dark nozzles made from one nozzle with radial duplication around an explicit center. Exterior only; say which depths are estimated. Success: bell diameter relative to the hull matches side.jpg.

## C7: materials

> Under neutral lights, add materials: glossy teal, dark teal, cream, red and the round fin logo as an image texture (I will supply or draw the logo). Explain your surface-detail choices without claiming they were the original method. Success: colour boundaries match the close-ups.

## C8: correction

> Show target and current front, side and rear views. The front view shows the nose too narrow and pointed and the engine bell too big. Keep the length, the fin and the wings. Widen the front of the hull and scale the bell down, save a new checkpoint, then render the same views. Do not move the cameras. Tell me which values changed and why.

## C9: export

> Save a numbered .blend, apply scale, and export a glTF 2.0 (.glb). Re-import it into a new scene and confirm its size and colours. List what the export did not keep.

These prompts have not been run by a learner or tested for this lesson.
