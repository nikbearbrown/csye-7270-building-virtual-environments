# Professor Bear's STL kit - parts list
26 binary STL files (Rhinoceros export, Sep 12 2022, millimetres). Source: Professor Bear (licence not stated). Used as dimensional ground truth for round 15; not redistributed.

They are a 3D-printable kit of the **Planet Express ship**, laid out on a print bed. They are NOT assembled in place: the hull is split into a nose and a rear section, each standing on its cut face (ship length along +Z), and the small parts are scattered. Assembly used for measurement (stl/ortho.py, stl/measure.py): nose X = z+13.3, Y = x, Z = y-39.45; rear X = -(z+13.8), Y = -x, Z = y-49.45 (top = +y: turret socket and cockpit visor recess are on +y, the display-stand socket on -y). The two cut faces match (same 49.4 x 45 section).

Assembled hull: 178.6 mm tip to tail cut (plus ~25 mm engine bell), max width 49.4, height 48.3 (22.5 above / 25.8 below the lip groove). Lip groove is a straight line along the widest section.

| # | id | tris | size mm | identified as |
|---|---|---|---|---|
| 01 | 07527535 | 3418 | 34.0 x 3.9 x 1.9 | rod with collars (antenna or gun barrel blank) |
| 02 | 0b95a644 | 10844 | 24.2 x 9.6 x 8.4 | pair of landing feet / pads |
| 03 | 1883d6a3 | 10332 | 36.2 x 12.9 x 1.7 | logo ring layers (C-shaped) |
| 04 | 29acc3d7 | 99918 | 45.8 x 51.9 x 21.1 | three elongated oval frames (vent / wing-root surrounds) |
| 05 | 2b64b703 | 2980 | 15.8 x 3.2 x 7.3 | three small cones (antenna / gun tips) |
| 06 | 459ef32c | 42028 | 7.1 x 45.7 x 79.5 | swept wing / landing strut, one side |
| 07 | 4beecd40 | 8974 | 45.1 x 22.4 x 3.2 | two discs (logo backing discs) |
| 08 | 4fa743b3 | 22224 | 29.9 x 29.6 x 27.5 | engine bell with rivet ring |
| 09 | 526e8971 | 23638 | 20.7 x 20.5 x 13.3 | turret base (stepped) |
| 10 | 5a3ddc70 | 4054 | 7.6 x 7.6 x 4.7 | turret dome |
| 11 | 6af09c0d | 2208 | 32.6 x 16.4 x 8.4 | gun body / mount |
| 12 | 6c86f54e | 12768 | 29.9 x 22.9 x 25.8 | vent box with louvres |
| 13 | 719bc2ce | 362 | 7.6 x 21.7 x 6.1 | small ribbed strip (vent / rivet strip) |
| 14 | 9e3c2dd1 | 3926 | 31.7 x 18.2 x 1.7 | two rocket shapes (logo rockets) |
| 15 | b060907f | 127868 | 50.7 x 48.1 x 89.8 | HULL rear section (vent recesses, fin slots, engine socket) |
| 16 | b19f28e5 | 42308 | 7.2 x 45.7 x 79.5 | swept wing / landing strut, other side |
| 17 | be74cc1b | 4478 | 27.2 x 5.7 x 25.8 | curved louvre panel (vent cover) |
| 18 | c59f9fc8 | 45866 | 8.4 x 92.1 x 81.2 | tail fin (swept blade with root tab) |
| 19 | c6599bdf | 29678 | 24.8 x 24.8 x 9.2 | engine exhaust lug cluster |
| 20 | c7d391ae | 90728 | 49.4 x 48.2 x 88.7 | HULL nose section (porthole holes, cockpit recess, turret socket) |
| 21 | ce2ee4c4 | 30670 | 51.3 x 181.3 x 3.6 | red lip ring (full length, wraps the nose) |
| 22 | d6445cb6 | 71137 | 69.2 x 37.2 x 9.9 | sprue of small parts (pins, rings, porthole rims) |
| 23 | dd7dff5d | 7062 | 35.7 x 20.3 x 9.1 | cockpit window frame |
| 24 | e7fc5abe | 3938 | 11.2 x 9.3 x 16.0 | hatch / door panel |
| 25 | ea020046 | 12828 | 18.0 x 31.1 x 25.5 | side panel with bracket (hatch or wing mount) |
| 26 | fc3875fe | 23252 | 29.4 x 11.8 x 32.6 | two cup-on-post parts (display stand / landing gear) |

Sheet: parts_sheet.jpg (labelled thumbnails, id, triangle count, bbox). Identifications of small parts are best guesses from shape and size.
