# Planet Express ship: build notes

Built by Grok Bot in Blender 4.2.3 (headless, Cycles CPU with denoising), entirely from a Python script (`scripts/build_pe.py` + `scripts/params.json`). It was judged over 15 rounds against Professor Bear's 12 reference photos of a toy model, using 12 cameras matched by eye to the photos. Each round was rendered side by side with the photos (`compare/`).

## Scores

| Round | Grok Bot (overall) | Side | Front | Rear | Top | Professor Bear |
|---|---|---|---|---|---|---|
| r12 | 4/10 | 5 | 3 | 3 | 5 | **"pretty good, maybe 6/10, could use another round"** |
| r13 | 5/10 | 5 | 4.5 | 4 | 5 | — |
| r14 | 5.5/10 | 6 | 5 | 4.5 | 5 | — |
| r15 | 5.5/10 | 6 | 5 | 4 | 5.5 | pending |

Grok Bot's scores are deliberately harsh and judge look and feel against the photos, not a checklist.

## Round history

- **r1–r2:** a lofted superellipse hull from profile tables traced off the side and top photos; lip tube, portholes, turret, fin, wings, engine bell; 12 matched cameras. Camera framing fixes.
- **r3:** fin reshaped, portholes placed by height, recessed glass, deeper teal.
- **r4:** superseded.
- **r5:** narrower hull and a rounder dome; larger turret skirt. The front view now reads as a dome.
- **r6:** narrower under-hull, sharper nose in plan, fatter lip.
- **r7:** smaller nozzle, wider and shallower cockpit.
- **r8:** blunt tail: the hull now ends just ahead of the engine bell. This is when the rear three-quarter view first read as the ship.
- **r9–r10:** lip end shortened, turret rescaled, oblique top cameras re-solved.
- **r11:** fin re-traced as a slender blade, logo mirrored on one side like the toy, blunter upper nose, larger cockpit.
- **r12:** fin raised, darker fin teal. Professor Bear: "pretty good, maybe 6/10, could use another round."
- **r13 (targeted fixes; working parts kept):** cockpit rebuilt as a wide, low visor projected onto the nose; centre beak on the lip; engine rebuilt as a dense lug cluster in a thick cream rim; vent slots sunk and given a raised border; hatch dial and ladder slats; less wing droop; slightly moodier lighting.
- **r14 (chunkier hull, Professor Bear's first priority):** fuller, more vertical upper sides, a deeper rounder belly, a heavier nose. Checked with silhouette overlays against the side and front photos (a first ×1.20 height overshot and was backed off to ×1.08). All details refit flush, the far-side lip end sunk into the hull, and the vent given depth.
- **r15 (STL refit):** Professor Bear supplied 26 STL files: a 3D-printable kit of the ship laid out on a print bed (separate nose and rear hull sections, lip ring, engine bell, exhaust lugs, turret, dome, fin, wings, cockpit frame, logo layers, vents and a stand).
  - The two hull sections were rotated into one frame and measured slice by slice. The true hull is 178.6 mm from tip to tail cut (plus a ~25 mm bell), 49.4 mm wide and 48.3 mm high (22.5 mm above and 25.8 mm below the lip groove), and the lip groove is straight.
  - The parametric hull was refit to that envelope at 0.066 model units per mm. The result is narrower than r14, nearly round in section, with a pointed nose over a long shallow chin. The turret, portholes and engine bell were placed from the kit.
  - Building directly from the STL meshes was rejected: the hull is split for printing, and refitting the parametric hull keeps every detail flush and the glossy toy look.

## STL data

The STL kit is **Professor Bear's data**. No licence or source was stated, so the STL files are **not included** in this folder. They were used only as measurement reference. `scripts/stl/` holds the scripts used to render, assemble and measure them, and `scripts/stl/parts.md` lists the parts and the assembly transforms.

## What is still off (r15)

- The upper hull reads lower and lighter than in the side photos, partly because of the photos' close, wide-angle cameras, which are matched only by eye.
- The engine bell sticks out too far and looks too big in the rear views.
- The cockpit visor reads slightly too large from the front.
- The details (vent, hatch, wing rings, lugs) are clean primitives, not the toy's sculpted parts. Only the hull and bell sizes were taken from the kit; the wings were placed by eye.
- The lighting and materials are even and computer-clean rather than soft, saturated toy plastic. There are no panel lines.
- The logo is an original drawn approximation.

## Reproduce

`blender -b -P scripts/build_pe.py -- r15` (each script sets the project folder at the top, `HERE` or `H`; point it at a folder holding `params.json`, `logo.png` and `logo_m.png`). `scripts/final.py` renders the gallery and exports the GLB.
