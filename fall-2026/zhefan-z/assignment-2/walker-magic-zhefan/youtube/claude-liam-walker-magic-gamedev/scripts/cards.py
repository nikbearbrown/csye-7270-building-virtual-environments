"""Native 3840x2160 cards and footage labels, drawn with Pillow in the Claude palette.

Used where no library composition fits (long verbatim prompts, a Python source
view, file previews, recorded output, credits). Every text on a card is either
verbatim from a named file or a plain label of what the viewer is looking at.
"""
from PIL import Image, ImageDraw, ImageFont

from common import W, H, PAGE, CARD, BORDER, INK, INK_SOFT, SPARK, font_path

SAFE_L, SAFE_T, SAFE_R, SAFE_B = 192, 108, 3648, 2052
_fonts = {}


def F(name, size):
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(str(font_path(name)), size)
    return _fonts[key]


def wrap(d, text, font, width):
    out = []
    for para in text.split('\n'):
        if not para.strip():
            out.append('')
            continue
        lead = para[:len(para) - len(para.lstrip(' '))]
        line = ''
        for word in para.strip(' ').split(' '):
            trial = f'{line} {word}' if line else lead + word
            if d.textlength(trial, font=font) <= width:
                line = trial
                continue
            if line:
                out.append(line)
            while d.textlength(lead + word, font=font) > width:
                k = len(word)
                while k > 1 and d.textlength(lead + word[:k], font=font) > width:
                    k -= 1
                out.append(lead + word[:k])
                word = word[k:]
            line = lead + word
        out.append(line)
    return out


def base(title, chip=None, chip_fill=INK):
    im = Image.new('RGB', (W, H), PAGE)
    d = ImageDraw.Draw(im)
    d.text((SAFE_L, 150), title, font=F('serif', 120), fill=INK)
    y = 330
    if chip:
        f = F('sans', 46)
        tw = d.textlength(chip, font=f)
        d.rounded_rectangle([SAFE_L, y, SAFE_L + tw + 72, y + 86], radius=43, fill=chip_fill)
        d.text((SAFE_L + 36, y + 16), chip, font=f, fill=PAGE)
        y += 140
    return im, d, y


def footer(d, text):
    d.text((SAFE_L, 1968), text, font=F('sans', 40), fill=INK_SOFT)


def panel(d, box, fill=CARD):
    d.rounded_rectangle(box, radius=28, fill=fill, outline=BORDER, width=4)


def requirements(rows, note, src):
    im, d, y = base('What the film has to show', 'From the author’s Assignment 2 film brief')
    cols, gap = 3, 48
    cw = (SAFE_R - SAFE_L - gap * (cols - 1)) // cols
    ch = 520
    for i, (label, detail) in enumerate(rows):
        x0 = SAFE_L + (i % cols) * (cw + gap)
        y0 = y + 20 + (i // cols) * (ch + gap)
        panel(d, [x0, y0, x0 + cw, y0 + ch])
        d.text((x0 + 56, y0 + 50), str(i + 1), font=F('serif', 110), fill=SPARK)
        ly = y0 + 200
        for line in wrap(d, label, F('serif_med', 70), cw - 112):
            d.text((x0 + 56, ly), line, font=F('serif_med', 70), fill=INK)
            ly += 86
        ly += 18
        for line in wrap(d, detail, F('sans', 46), cw - 112):
            d.text((x0 + 56, ly), line, font=F('sans', 46), fill=INK_SOFT)
            ly += 62
    d.text((SAFE_L, 1860), note, font=F('sans', 52), fill=INK)
    footer(d, src)
    return im


def prompt(step, name, text, uploaded, src):
    im, d, y = base('The prompt, word for word',
                    'Prompt drafted by Claude, sent by the author in the Gemini app · Gemini 3.8 Flash')
    d.text((SAFE_L, y + 10), f'{step} of 3 · {name}', font=F('serif_med', 76), fill=SPARK)
    top = y + 130
    panel(d, [SAFE_L, top, SAFE_R, 1900])
    for size in (84, 76, 68, 62, 58, 54, 50, 46, 42):
        f = F('sans', size)
        lines = wrap(d, text, f, SAFE_R - SAFE_L - 160)
        lh = int(size * 1.42)
        if top + 70 + len(lines) * lh <= 1840:
            break
    ty = top + 70
    for line in lines:
        d.text((SAFE_L + 80, ty), line, font=f, fill=INK)
        ty += lh
    footer(d, f'{uploaded} · {src}')
    return im


def source_view(title, chip, path, start, text, highlight, note):
    """Dark editor-style source panel (light text), line numbers, wrapped long lines."""
    im, d, y = base(title, chip)
    top = y + 10
    d.rounded_rectangle([SAFE_L, top, SAFE_R, 1935], radius=28, fill='#202531')
    raw = text.split('\n')
    for size in (46, 43, 40, 37, 34):
        f = F('mono', size)
        lh = int(size * 1.36)
        rows = [(start + i, part, j == 0) for i, line in enumerate(raw)
                for j, part in enumerate(wrap(d, line.replace('\t', '    ') or ' ', f, SAFE_R - SAFE_L - 330))]
        if top + 120 + len(rows) * lh <= 1915:
            break
    d.text((SAFE_L + 60, top + 30), path, font=F('mono', 40), fill='#8BC7F3')
    ty = top + 110
    for num, part, first in rows:
        if num in highlight:
            d.rectangle([SAFE_L + 4, ty - 6, SAFE_R - 4, ty + lh - 6], fill='#3A4A5E')
            d.rectangle([SAFE_L + 4, ty - 6, SAFE_L + 14, ty + lh - 6], fill=SPARK)
        if first:
            d.text((SAFE_L + 60, ty), f'{num:>4}', font=f, fill='#8D97A8')
        colour = '#AEB9B0' if part.strip().startswith('#') else '#EDF1F7'
        d.text((SAFE_L + 250, ty), part, font=f, fill=colour)
        ty += lh
    footer(d, note)
    return im


def design_card(title, chip, section, excerpt, image, image_label, swatches, notes, src):
    """Document excerpt (left) beside a labelled design image, palette swatches and notes (right)."""
    im, d, y = base(title, chip)
    top = y + 10
    split = 1640
    panel(d, [SAFE_L, top, split, 1900])
    d.text((SAFE_L + 60, top + 50), 'DOCUMENT EXCERPT', font=F('sans', 40), fill=INK_SOFT)
    d.text((SAFE_L + 60, top + 120), section, font=F('serif_med', 64), fill=INK)
    ty = top + 240
    for para in excerpt:
        for line in wrap(d, para, F('sans', 52), split - SAFE_L - 150):
            d.text((SAFE_L + 90, ty), line, font=F('sans', 52), fill=INK)
            ty += 72
        ty += 34
    d.rectangle([SAFE_L + 60, top + 240, SAFE_L + 68, ty - 34], fill=SPARK)
    x0 = split + 60
    d.text((x0, top + 10), image_label, font=F('sans', 40), fill=INK_SOFT)
    box = [x0, top + 70, SAFE_R, top + 70 + 420]
    r = min((box[2] - box[0]) / image.width, (box[3] - box[1]) / image.height)
    pic = image.resize((round(image.width * r), round(image.height * r)), Image.LANCZOS)
    im.paste(pic, (box[0] + (box[2] - box[0] - pic.width) // 2, box[1] + (box[3] - box[1] - pic.height) // 2))
    sy = box[3] + 70
    d.text((x0, sy), 'Palette: six key colours + outline', font=F('serif_med', 58), fill=INK)
    sy += 100
    cw = (SAFE_R - x0) // 4
    for i, (name, hexv) in enumerate(swatches):
        sx, yy = x0 + (i % 4) * cw, sy + (i // 4) * 210
        d.rounded_rectangle([sx, yy, sx + 110, yy + 110], radius=14, fill=hexv, outline=BORDER, width=3)
        d.text((sx + 135, yy + 6), name, font=F('sans', 40), fill=INK)
        d.text((sx + 135, yy + 58), hexv, font=F('mono', 38), fill=INK_SOFT)
    ny = sy + 450
    for label, value in notes:
        d.text((x0, ny), label, font=F('sans', 42), fill=INK_SOFT)
        d.text((x0, ny + 58), value, font=F('serif', 62), fill=INK)
        ny += 160
    assert ny < 1960, 'design card overflows'
    footer(d, src)
    return im


def image_card(title, chip, img, facts, src, img_box, facts_x, checker=False, scale_nearest=None):
    im, d, y = base(title, chip)
    x0, y0, x1, y1 = img_box
    if checker:
        step = 40
        for yy in range(y0, y1, step):
            for xx in range(x0, x1, step):
                if ((xx - x0) // step + (yy - y0) // step) % 2:
                    d.rectangle([xx, yy, min(xx + step, x1) - 1, min(yy + step, y1) - 1], fill='#D9D6CC')
                else:
                    d.rectangle([xx, yy, min(xx + step, x1) - 1, min(yy + step, y1) - 1], fill='#EFECE3')
    if scale_nearest:
        pic = img.resize((img.width * scale_nearest, img.height * scale_nearest), Image.NEAREST)
    else:
        r = min((x1 - x0) / img.width, (y1 - y0) / img.height)
        pic = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    px, py = x0 + (x1 - x0 - pic.width) // 2, y0 + (y1 - y0 - pic.height) // 2
    if pic.mode == 'RGBA':
        im.paste(pic, (px, py), pic)
    else:
        im.paste(pic, (px, py))
    d.rectangle([x0, y0, x1, y1], outline=BORDER, width=4)
    fy = y + 30
    fw = (x0 - 100 - facts_x) if facts_x < x0 else (SAFE_R - facts_x)
    for label, value in facts:
        d.text((facts_x, fy), label, font=F('sans', 42), fill=INK_SOFT)
        fy += 62
        for line in wrap(d, value, F('serif', 64), fw):
            d.text((facts_x, fy), line, font=F('serif', 64), fill=INK)
            fy += 80
        fy += 40
    footer(d, src)
    return im


def terminal(title, chip, command, lines, highlight, note, src):
    im, d, y = base(title, chip)
    top = y + 10
    d.rounded_rectangle([SAFE_L, top, SAFE_R, 1790], radius=28, fill='#202531')
    f = F('mono', 46)
    lh = 64
    ty = top + 50
    for part in wrap(d, '$ ' + command, f, SAFE_R - SAFE_L - 140):
        d.text((SAFE_L + 70, ty), part, font=f, fill='#8BC7F3')
        ty += lh
    ty += 24
    for i, line in enumerate(lines):
        parts = wrap(d, line, f, SAFE_R - SAFE_L - 160)
        if i in highlight:
            d.rectangle([SAFE_L + 30, ty - 8, SAFE_L + 42, ty + lh * len(parts) - 14], fill=SPARK)
        colour = '#EDF1F7' if i in highlight or line.startswith('WALKER') else '#BEC8D7'
        for part in parts:
            d.text((SAFE_L + 70, ty), part, font=f, fill=colour)
            ty += lh
    for k, line in enumerate(wrap(d, note, F('sans', 50), SAFE_R - SAFE_L)):
        d.text((SAFE_L, 1825 + k * 66), line, font=F('sans', 50), fill=INK)
    footer(d, src)
    return im


def columns(title, chip, cols, src):
    im, d, y = base(title, chip)
    gap = 48
    cw = (SAFE_R - SAFE_L - gap * (len(cols) - 1)) // len(cols)
    for i, (head, items) in enumerate(cols):
        x0 = SAFE_L + i * (cw + gap)
        panel(d, [x0, y + 10, x0 + cw, 1900])
        d.text((x0 + 56, y + 60), head, font=F('serif_med', 66), fill=SPARK)
        ty = y + 180
        for label, value in items:
            if label:
                for line in wrap(d, label, F('sans', 46), cw - 112):
                    d.text((x0 + 56, ty), line, font=F('sans', 46), fill=INK_SOFT)
                    ty += 62
            for line in wrap(d, value, F('serif', 64), cw - 112):
                d.text((x0 + 56, ty), line, font=F('serif', 64), fill=INK)
                ty += 80
            ty += 46
        assert ty < 1900, f'{head}: column overflows'
    footer(d, src)
    return im


def labels(items):
    """Transparent 3840x2160 overlay. items: (text, 'tl'|'tr'|'tc2', style). Returns (image, boxes)."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    boxes = []
    for text, pos, style in items:
        f = F('sans', 58 if style == 'disclosure' else 64)
        tw = d.textlength(text, font=f)
        bw, bh = tw + 80, 104
        if pos == 'tl':
            x, y = 220, 132
        elif pos == 'tr':
            x, y = SAFE_R - 28 - bw, 132
        else:                                   # second row, centred
            x, y = (W - bw) / 2, 290
        fill = (61, 57, 41, 236) if style == 'disclosure' else (217, 119, 87, 245)
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=52, fill=fill)
        d.text((x + 40, y + 18), text, font=f, fill=(250, 249, 245, 255))
        boxes.append([x, y, x + bw, y + bh])
    return im, boxes
