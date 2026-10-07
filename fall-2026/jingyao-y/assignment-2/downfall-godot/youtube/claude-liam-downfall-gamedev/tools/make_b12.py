"""Build images/B12-asset-trace.png from the real files (run from downfall-godot/).

1 raw gpt-image source (local, not in git), 2 the 72 px runtime icon,
3 the icon cropped 1:1 from the engine screenshot tests/capture_gui.gd wrote.
"""
from PIL import Image, ImageDraw, ImageFont

R = 'youtube/claude-liam-downfall-gamedev'
W, H = 3840, 2160
o = Image.new('RGB', (W, H), '#FAF9F5')
d = ImageDraw.Draw(o)
ui = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 46)
ui2 = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 38)
d.text((210, 110), "Emperor's Favour (皇帝的恩宠): raw → 72 px → engine",
       font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 92), fill='#2f2b26')
raw = Image.open('art/relics/batch_R1_v1/sources/is2_058.png').convert('RGBA')
icon = Image.open('art/relics/runtime/is2_058.png').convert('RGBA')
engine = Image.open('../evidence/gui-relics.png').convert('RGB').crop((14, 76, 90, 152))  # R window, first slot


def card(x, title, sub, note, img):
    y, w, h = 330, 1060, 1450
    d.rectangle([x, y, x + w, y + h], fill='#22262e')
    bg = Image.new('RGB', (w - 80, w - 80), '#1b1b1b')
    im = img
    if im.mode == 'RGBA':
        flat = Image.new('RGB', im.size, '#1b1b1b')
        flat.paste(im, (0, 0), im)
        im = flat
    s = min(bg.width / im.width, bg.height / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.NEAREST if img.width < 300 else Image.LANCZOS)
    bg.paste(im, ((bg.width - im.width) // 2, (bg.height - im.height) // 2))
    o.paste(bg, (x + 40, y + 40))
    d.text((x + 40, y + w), title, font=ui, fill='#edf1f7')
    d.text((x + 40, y + w + 70), sub, font=ui2, fill='#bec8d7')
    d.text((x + 40, y + w + 130), note, font=ui2, fill='#8bc7f3')


card(210, '1  Raw generation', 'gpt-image via Sol · 1254×1254', 'shown downscaled to fit', raw)
card(1390, '2  Game icon', 'reduce_generated.py · 72×72, 23 colours', 'shown 13× nearest-neighbour', icon)
card(2570, '3  In the engine', 'R window, drawn at exactly 1×', 'engine screenshot, enlarged nearest-neighbour', engine)
d.text((210, 1880), 'Real files: art/relics/batch_R1_v1/sources/is2_058.png · art/relics/runtime/is2_058.png · '
       'engine screenshot from tests/capture_gui.gd, 2026-10-07 (same icon file as commit 111bf6e)', font=ui2, fill='#6b6458')
d.text((210, 1950), 'Still images, not motion footage.', font=ui2, fill='#6b6458')
o.save(R + '/images/B12-asset-trace.png')
