# Pre-crops of the real Codex template stills so the picture never crosses the title-safe edge (Gate V edge-bleed fix).
# preview px = 1/3.24 of the stored PNG for a6_codex_ask (1600 x 900 preview); tool stills are 1600 x ~287 preview px (scale 4954/1600).
from PIL import Image
P = "pantry/"
ask = Image.open(P + "a6_codex_ask.png"); s = ask.size[0] / 1600.0
def crop(im, s, u0, v0, w, h, out):
    im.crop((int(u0 * s), int(v0 * s), int((u0 + w) * s), int((v0 + h) * s))).save(P + out); print(out, (u0, v0, w, h))
crop(ask, s, 440, 115, 900, 450, "a6_codex_ask_cropA.png")      # asks 1-3 (and the first paragraph)
crop(ask, s, 440, 425, 900, 450, "a6_codex_ask_cropB.png")      # asks 4-5
for n in ("a", "b"):
    t = Image.open(P + f"a6_codex_tool_{n}.png"); st = t.size[0] / 1600.0; h = t.size[1] / st
    crop(t, st, 60 if n == "a" else 560, 0, 1000, h, f"a6_codex_tool_{n}_crop.png")
