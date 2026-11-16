# Voice check (faster-whisper small)

**What this is.** Automatic transcription of each beat's Kokoro audio against `narration.py`; a rough ear, not a replacement for Bear's.

**Found.** 46 beats; 5 below 0.85 similarity (listed with transcripts). Pronunciation dictionary untouched.

| beat | similarity |
|---|---|
| BOPEN | 0.99 |
| BIDEA | 0.99 |
| BDEFS | 0.65 |
| B01 | 1.00 |
| B02 | 1.00 |
| B03 | 0.91 |
| B04 | 0.99 |
| B05 | 0.87 |
| B06 | 0.99 |
| B07 | 0.99 |
| B08 | 0.21 |
| B09 | 1.00 |
| B10 | 0.82 |
| B11 | 0.95 |
| B12 | 0.93 |
| B13 | 0.91 |
| B14 | 0.96 |
| B15 | 1.00 |
| B16 | 1.00 |
| B17 | 1.00 |
| B18 | 0.93 |
| B19 | 0.88 |
| B20 | 1.00 |
| B21 | 1.00 |
| B22 | 1.00 |
| B23 | 1.00 |
| B24 | 0.98 |
| B25 | 0.99 |
| B26 | 1.00 |
| B27 | 1.00 |
| B28 | 1.00 |
| B29 | 1.00 |
| B30 | 0.97 |
| B31 | 1.00 |
| B32 | 1.00 |
| B33 | 1.00 |
| B34 | 1.00 |
| B35 | 1.00 |
| B36 | 1.00 |
| B37 | 0.79 |
| B38 | 0.98 |
| B39 | 0.89 |
| B40 | 0.97 |
| BVDT | 1.00 |
| BHTF | 0.62 |
| BOUT | 0.99 |

## Low beats (read the transcript, then LISTEN)

### BDEFS (0.65)
- spoken text: Five terms. An angle is an amount of turn. A radian is an angle measured so that a full turn is about six point two eight. The hypotenuse is the longest side of a right triangle. A vec two is a bundle of two numbers. And U V is a pixel's address, zero to one across and down.
- heard: Five terms, an angle is an amount of turn. A radian is an angle measured so that a full turn is about 6.28. The hypotenuse is the longest side of a right triangle. A VEC-2 is a bundle of two numbers. And UV is a pixel's address, zero to one across and down.

### B08 (0.21)
- spoken text: Godot's own manual says the same. Vector two has a function, from angle, that builds a point from an angle. The manual calls it equivalent to cosine of the angle, sine of the angle. The engine knows the recipe.
- heard: Godot's own manual says the same. Vector 2 has a function from angle that builds a point from an angle. The manual calls it equivalent to cosine of the angle, sine of the angle. The engine knows the recipe.

### B10 (0.82)
- spoken text: Try one by hand. Radius point six, angle thirty degrees. The first number is point six times cosine, about point five two. The second is point six times sine, exactly point three. Hold on to those two numbers.
- heard: Try one by hand, radius 0.6, angle 30 degrees. The first number is 0.6 times cosine about 0.52. The second is 0.6 times sine exactly 0.3. Hold on to those two numbers.

### B37 (0.79)
- spoken text: Work one pixel. Up and to the left, at minus point three, minus point three. Arc tangent says minus three quarters of pi. Divide by tau: minus point three seven five. Add one half: point one two five. One eighth.
- heard: Work one pixel up into the left at minus 0.3 minus 0.3. Arc tangent says minus three quarters of pi divide by tau minus 0.375. Add one half 0.125 one eighth.

### BHTF (0.62)
- spoken text: Your turn. Paste this into Claude: Write a Godot canvas item shader for a square Color Rect: a teal planet in the middle and a smaller moon that circles it once every four seconds. Place the moon with cosine and sine of an angle in radians, and point me to the line that sets the speed. Then check two things yourself. Does the moon finish a lap in about four seconds? And does it turn clockwise, so that negating the angle reverses it?
- heard: Your turn, paste this into Claude, write a Godot canvas item shader for a square color rect, a teal planet in the middle and a smaller moon that circles it once every 4 seconds. Place the moon with cosine and sine of an angle and radians and point me to the line that sets the speed. Then check two things yourself. Does the moon finish a lap in about 4 seconds? And does it turn clockwise so that negating the angle reverses it?
