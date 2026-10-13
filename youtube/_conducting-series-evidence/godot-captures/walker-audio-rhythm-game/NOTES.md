# walker-audio-rhythm-game: capture notes (VISUAL ONLY)

**What this is.** A real windowed Godot 4.7.2 Movie Maker run of the rhythm game (chart "The Comeback"), recorded 2026-10-09 at a fixed 30 fps from a scratch copy. The source at `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-audio-rhythm-game/godot` was not touched. The copy got only the capture autoload and a 1920x1080 window. **Per the brief, this is visual evidence only: the MP4 has no audio track** (`AUDIO=0`). Movie Maker did record the song to WAV, peaking at -11.9 dB.

**Timing caveat (read before using as rhythm evidence).** The game's conductor blends the audio playback clock with the wall clock (`Time.get_ticks_usec`). Movie Maker runs on simulated, fixed-fps time, so the wall clock does not match the recorded timeline. The project's own CAPTURE-PLAN.md and FRICTIONAL.md warn exactly this. These frames show the real UI, notes and judgments, but they do not certify audio/visual synchronization.

## Scripted input
A "rhythm" controller in the driver reads the game's own NoteManager. Each frame it takes the next note and its delta from `_get_note_delta`. When the note is 0.06 s or less away (one 30 fps frame of input latency), it **presses** `main_key` (InputEventAction) and releases it 2 frames later. It never assigns a score. Every 7th note is deliberately let pass, to show a miss. The run made 19 presses and let 3 notes pass; each one is logged as a RHYTHM line in `raw-log.txt`. The song's first note arrives at about f263 (8.8 s).

## Files (all 1920x1080)
| File | What is on screen |
|---|---|
| `01-start-screen-settings-and-guide.png` | Controls text, settings (smoothing filter on, metronome off, input latency 20 ms, scroll speed 400), the empty guide, chart selector, Perfect/Good/Miss counters at 0, empty error graph. |
| `02-first-notes-approaching-guide.png` | The first notes (white bars) falling toward the guide; counters still 0. |
| `03-after-deliberate-miss-stats.png` | "Miss..." judgment labels either side of the guide. Stats read Perfect 6, Good 0, Miss 1, Avg Error +33.4 ms (Late). The error graph shows dots. |
| `04-perfect-hits-error-graph.png` | A "Good" judgment label by the guide (frame 600). Stats read Perfect 14, Good 2, Miss 2, Avg Error +36.6 ms (Late). The error graph has a row of dots. |
| `walker-audio-rhythm-game-clip.mp4` | 8.0 s, H.264, 30 fps, **no audio**. Movie frames 360–600: notes falling, "Perfect!" and "Good" hits, one deliberate miss, counters climbing (Perfect 6 to 14), error graph filling. |

**Run-to-run variation:** a previous identical take ended at Perfect 13, Good 3 and +40.7 ms. Judgments differ slightly between takes because the conductor reads the wall clock. That is one more reason not to treat these numbers as timing measurements.

**Problems:**
- The roughly +33–40 ms "Late" average comes from the driver's one-frame input latency combined with the clock caveat above. It is not a measurement of the game.
- A harmless engine error appears at startup: `Unrecognized UID "uid://bdd4ws8b7jdqh"`, which is the project icon.
