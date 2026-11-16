"""Native 3840x2160 cards and footage labels, drawn with Pillow in the Claude palette.

Adapted from the Assignment 2 film's cards.py. Used where no library composition fits (the
author's screenshots with enlarged details, Blender Python source views, recorded output,
look renders). Every text on a card is either verbatim from a named file or a plain label of
what the viewer is looking at.
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


def badge(d, x, y, text, fill=SPARK):
    f = F('sans', 40)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 56, y + 70], radius=35, fill=fill)
    d.text((x + 28, y + 12), text, font=f, fill=PAGE)


def fit(img, box_w, box_h, nearest=False):
    r = min(box_w / img.width, box_h / img.height)
    size = (max(1, round(img.width * r)), max(1, round(img.height * r)))
    return img.resize(size, Image.NEAREST if nearest else Image.LANCZOS), r


def brief_card(title, chip, left_head, left_rows, right_head, right_rows, src):
    """Two panels of short rows: (label, detail)."""
    im, d, y = base(title, chip)
    gap = 60
    cw = (SAFE_R - SAFE_L - gap) // 2
    for i, (head, rows) in enumerate(((left_head, left_rows), (right_head, right_rows))):
        x0 = SAFE_L + i * (cw + gap)
        panel(d, [x0, y + 10, x0 + cw, 1910])
        d.text((x0 + 60, y + 60), head, font=F('serif_med', 70), fill=SPARK)
        ty = y + 190
        for label, detail in rows:
            for line in wrap(d, label, F('serif_med', 80), cw - 120):
                d.text((x0 + 60, ty), line, font=F('serif_med', 80), fill=INK)
                ty += 100
            for line in wrap(d, detail, F('sans', 56), cw - 120):
                d.text((x0 + 60, ty), line, font=F('sans', 56), fill=INK_SOFT)
                ty += 76
            ty += 64
        assert ty < 1910, f'{head}: panel overflows'
    footer(d, src)
    return im


def gallery(title, chip, items, src, top_h=None):
    """Side-by-side images. item: {'img', 'badge', 'caption', 'insets': [(crop_box, label, nearest)]}."""
    im, d, y = base(title, chip)
    n = len(items)
    gap = 60
    cw = (SAFE_R - SAFE_L - gap * (n - 1)) // n
    has_insets = any(it.get('insets') for it in items)
    img_h = top_h or (900 if has_insets else 1250)
    for i, it in enumerate(items):
        x0 = SAFE_L + i * (cw + gap)
        pic, _ = fit(it['img'], cw, img_h)
        py = y + 10
        px = x0 + (cw - pic.width) // 2
        im.paste(pic, (px, py))
        d.rectangle([px, py, px + pic.width, py + pic.height], outline=BORDER, width=4)
        badge(d, px + 24, py + 24, it['badge'])
        ty = py + pic.height + 30
        for line in wrap(d, it['caption'], F('sans', 44), cw):
            d.text((x0, ty), line, font=F('sans', 44), fill=INK)
            ty += 58
        ty += 20
        for crop, label, nearest in it.get('insets', []):
            part = it['img'].crop(crop)
            avail = 1930 - ty - 70
            ins, r = fit(part, cw, min(avail, 420), nearest)
            im.paste(ins, (x0, ty))
            d.rectangle([x0, ty, x0 + ins.width, ty + ins.height], outline=SPARK, width=6)
            k = 0
            for k, line in enumerate(wrap(d, f'{label} · enlarged ×{r:.1f} from the same screenshot', F('sans', 40), cw)):
                d.text((x0, ty + ins.height + 14 + k * 54), line, font=F('sans', 40), fill=INK_SOFT)
            ty += ins.height + 14 + (k + 1) * 54 + 30
        assert ty < 1960, f'gallery column {i} overflows ({ty})'
    footer(d, src)
    return im


def shot_with_insets(title, chip, img, img_badge, caption, insets, src):
    """One screenshot (left) with enlarged details from it stacked on the right."""
    im, d, y = base(title, chip)
    split = 2300
    pic, _ = fit(img, split - SAFE_L - 60, 1300)
    px, py = SAFE_L, y + 10
    im.paste(pic, (px, py))
    d.rectangle([px, py, px + pic.width, py + pic.height], outline=BORDER, width=4)
    badge(d, px + 24, py + 24, img_badge)
    cy = py + pic.height + 30
    for line in wrap(d, caption, F('sans', 46), split - SAFE_L - 60):
        d.text((px, cy), line, font=F('sans', 46), fill=INK)
        cy += 60
    ty = y + 10
    for crop, label, nearest in insets:
        part = img.crop(crop)
        ins, r = fit(part, SAFE_R - split, 560, nearest)
        im.paste(ins, (split, ty))
        d.rectangle([split, ty, split + ins.width, ty + ins.height], outline=SPARK, width=6)
        for k, line in enumerate(wrap(d, f'{label} · enlarged ×{r:.1f} from the same screenshot', F('sans', 40), SAFE_R - split)):
            d.text((split, ty + ins.height + 14 + k * 52), line, font=F('sans', 40), fill=INK_SOFT)
        ty += ins.height + 180
    assert ty < 1990 and cy < 1950, 'insets overflow'
    footer(d, src)
    return im


def main_and_side(title, chip, main, side, src):
    """main / side items: {'img', 'badge', 'caption'}. Main large on the left, two stacked on the right."""
    im, d, y = base(title, chip)
    split = 2380
    pic, _ = fit(main['img'], split - SAFE_L - 60, 1250)
    px, py = SAFE_L, y + 10
    im.paste(pic, (px, py))
    d.rectangle([px, py, px + pic.width, py + pic.height], outline=BORDER, width=4)
    badge(d, px + 24, py + 24, main['badge'])
    cy = py + pic.height + 30
    for line in wrap(d, main['caption'], F('sans', 54), split - SAFE_L - 60):
        d.text((px, cy), line, font=F('sans', 54), fill=INK)
        cy += 72
    ty = y + 10
    for it in side:
        s_pic, _ = fit(it['img'], SAFE_R - split, 600)
        im.paste(s_pic, (split, ty))
        d.rectangle([split, ty, split + s_pic.width, ty + s_pic.height], outline=BORDER, width=4)
        badge(d, split + 20, ty + 20, it['badge'])
        k = 0
        for k, line in enumerate(wrap(d, it['caption'], F('sans', 46), SAFE_R - split)):
            d.text((split, ty + s_pic.height + 18 + k * 60), line, font=F('sans', 46), fill=INK)
        ty += s_pic.height + 18 + (k + 1) * 60 + 50
    assert ty < 1960 and cy < 1950, f'main_and_side overflows ({ty}, {cy})'
    footer(d, src)
    return im


def prompt_and_shot(title, chip, prompt_head, prompt_lines, prompt_src, shot, shot_badge, shot_caption, src):
    """Verbatim prompt lines (left) beside a screenshot (right)."""
    im, d, y = base(title, chip)
    split = 1880
    panel(d, [SAFE_L, y + 10, split - 40, 1910])
    d.text((SAFE_L + 60, y + 60), prompt_head, font=F('serif_med', 64), fill=SPARK)
    ty = y + 180
    for para in prompt_lines:
        for line in wrap(d, para, F('mono', 62), split - SAFE_L - 200):
            d.text((SAFE_L + 90, ty), line, font=F('mono', 62), fill=INK)
            ty += 88
        ty += 60
    d.rectangle([SAFE_L + 60, y + 180, SAFE_L + 68, ty - 40], fill=SPARK)
    for line in wrap(d, prompt_src, F('sans', 40), split - SAFE_L - 160):
        d.text((SAFE_L + 60, ty + 10), line, font=F('sans', 40), fill=INK_SOFT)
        ty += 54
    assert ty < 1900, 'prompt panel overflows'
    badge(d, split, y + 10, shot_badge)
    pic, _ = fit(shot, SAFE_R - split, 1000)
    px, py = split, y + 110
    im.paste(pic, (px, py))
    d.rectangle([px, py, px + pic.width, py + pic.height], outline=BORDER, width=4)
    cy = py + pic.height + 30
    for line in wrap(d, shot_caption, F('sans', 56), SAFE_R - split):
        d.text((px, cy), line, font=F('sans', 56), fill=INK)
        cy += 74
    footer(d, src)
    return im


def source_view(title, chip, path, start, text, highlight, note):
    """Dark editor-style source panel (light text), line numbers, wrapped long lines."""
    im, d, y = base(title, chip)
    top = y + 10
    d.rounded_rectangle([SAFE_L, top, SAFE_R, 1935], radius=28, fill='#202531')
    raw = text.split('\n')
    for size in (52, 48, 46, 43, 40, 37, 34):
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


def image_facts(title, chip, img, img_badge, facts, src):
    """One image (left) with label/value facts (right)."""
    im, d, y = base(title, chip)
    split = 2350
    pic, r = fit(img, split - SAFE_L - 60, 1910 - y - 10)
    px, py = SAFE_L, y + 10
    im.paste(pic, (px, py))
    d.rectangle([px, py, px + pic.width, py + pic.height], outline=BORDER, width=4)
    badge(d, px + 24, py + 24, img_badge)
    fy = y + 20
    for label, value in facts:
        d.text((split, fy), label, font=F('sans', 42), fill=INK_SOFT)
        fy += 62
        for line in wrap(d, value, F('serif', 62), SAFE_R - split):
            d.text((split, fy), line, font=F('serif', 62), fill=INK)
            fy += 78
        fy += 36
    assert fy < 1940, 'facts overflow'
    footer(d, src)
    return im


def terminal(title, chip, command, lines, highlight, note, src, size=46):
    im, d, y = base(title, chip)
    top = y + 10
    d.rounded_rectangle([SAFE_L, top, SAFE_R, 1790], radius=28, fill='#202531')
    f = F('mono', size)
    lh = int(size * 1.39)
    ty = top + 50
    for part in wrap(d, '$ ' + command, f, SAFE_R - SAFE_L - 140):
        d.text((SAFE_L + 70, ty), part, font=f, fill='#8BC7F3')
        ty += lh
    ty += 24
    for i, line in enumerate(lines):
        parts = wrap(d, line, f, SAFE_R - SAFE_L - 160)
        if i in highlight:
            d.rectangle([SAFE_L + 30, ty - 8, SAFE_L + 42, ty + lh * len(parts) - 14], fill=SPARK)
        colour = '#EDF1F7' if i in highlight else '#BEC8D7'
        for part in parts:
            d.text((SAFE_L + 70, ty), part, font=f, fill=colour)
            ty += lh
    assert ty < 1790, f'terminal overflows ({ty})'
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
            for line in wrap(d, value, F('serif', 62), cw - 112):
                d.text((x0 + 56, ty), line, font=F('serif', 62), fill=INK)
                ty += 78
            ty += 44
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
