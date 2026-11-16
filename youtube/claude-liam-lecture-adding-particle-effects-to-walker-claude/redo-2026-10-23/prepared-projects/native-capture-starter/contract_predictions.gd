extends RefCounted
# EFFECT A: one root-owned milestone burst, initially inactive.
# Gate opening and finish events provide its world position.
# A newer event intentionally replaces the same active emitter.
# EFFECT B: motes indicate an available route while the room is active.
# Condition: gate_open and not won and presentation_enabled and visible.
#
# PREDICTIONS:
# 1. Hiding the player does not hide the root-owned burst.
# 2. Hiding the scene stops new motes.
# 3. Pause stops pausable processing while emitting may remain true.
# 4. Reset during charge cannot produce a delayed gate event.
# 5. A replacement burst occupies the latest position and still finishes.
#
# APPEARANCE: preserve a baseline and a separately motivated revision per effect.
# Native visual comparison is required; state assertions do not approve it.
#
# PROVISIONAL 60 FPS BUDGET: approximately 16.7 ms for the whole frame.
# Burst allocation: 0.5 ms. Motes allocation: 1.0 ms.
# Combined effect envelope: 2.0 ms including drawing, with 0.5 ms contingency.
# Headless CPU evidence alone cannot establish that these limits are met.
# Name the machine, renderer, viewport, mode and timing availability.
