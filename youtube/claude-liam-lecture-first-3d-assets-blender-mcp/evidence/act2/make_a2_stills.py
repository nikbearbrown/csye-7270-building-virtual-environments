"""make_a2_stills.py — the one Act II image made by resizing a real capture (no pixel is drawn or edited):
pantry/a2_b20_screenshot.png = pantry/a2_bl_sidebar_closed.png (the act's window: lantern selected) scaled with Lanczos to the
exact pixel size it is shown at in B20's notes-file slot on the 4K master (3.2 scene units wide = 864 px), so Manim shows it
1:1 instead of point-sampling a 3456-px image down. Run from the reel folder."""
from PIL import Image
src = Image.open("pantry/a2_bl_sidebar_closed.png").convert("RGB")
w = round(3.2 * 3840 / (128 / 9))          # 3.2 units at 270 px per unit
h = round(w * src.height / src.width)
src.resize((w, h), Image.LANCZOS).save("pantry/a2_b20_screenshot.png")
print("pantry/a2_b20_screenshot.png", w, h)
