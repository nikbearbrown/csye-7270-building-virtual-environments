"""Native 3840x2160 cards, drawn with Pillow in the Claude palette.

Adapted from the Assignment 3 film's cards.py. Used where no library composition fits: the author's
in-engine captures (640x360) enlarged with nearest-neighbour scaling, document and source views,
and tables of recorded results. Every text on a card is either verbatim or a figure from a named
source file, or a plain label of what the viewer is looking at.
"""
from PIL import Image, ImageDraw, ImageFont

from common import W, H, PAGE, CARD, BORDER, INK, INK_SOFT, SPARK, font_path

SAFE_L, SAFE_T, SAFE_R, SAFE_B = 192, 108, 3648, 2052
DARK, DARK_TEXT, DARK_MUTED, DARK_HI = '#202531', '#EDF1F7', '#8D97A8', '#3A4A5E'
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


def text_block(d, x, y, text, font, width, fill, lh):
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


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


def badge(d, x, y, text, fill=SPARK, size=40):
    f = F('sans', size)
    tw = d.textlength(text, font=f)
    h = int(size * 1.75)
    d.rounded_rectangle([x, y, x + tw + 56, y + h], radius=h // 2, fill=fill)
    d.text((x + 28, y + int(size * 0.3)), text, font=f, fill=PAGE)
    return x + tw + 56


def enlarge(img, crop, box_w, box_h):
    """Crop a capture and enlarge it by the largest whole factor that fits (nearest neighbour)."""
    part = img.crop(crop)
    k = max(1, min(box_w // part.width, box_h // part.height))
    return part.resize((part.width * k, part.height * k), Image.NEAREST), k


def rows_of_crops(title, chip, items, crop, header, widths, note, src, img_w=1300, img_h=400, size=46):
    """One row per capture: an enlarged crop on the left, table cells on the right.
    items: [{'img', 'cells'}]; header/widths describe the cells only."""
    im, d, y = base(title, chip)
    x_cells = SAFE_L + img_w + 70
    cx = x_cells
    hy = y
    for w, h in zip(widths, header):
        hy = max(hy, text_block(d, cx, y, h, F('sans', 40), w - 30, INK_SOFT, 52))
        cx += w
    ty = hy + 24
    k = 1
    fr = F('sans', size)
    for it in items:
        pic, k = enlarge(it['img'], crop, img_w, img_h)
        paste_framed(im, d, pic, SAFE_L, ty)
        cx = x_cells
        for i, (w, cell) in enumerate(zip(widths, it['cells'])):
            text_block(d, cx, ty + 10, str(cell), F('mono', size) if i == 0 else fr, w - 30, INK, int(size * 1.32))
            cx += w
        ty += max(pic.height, img_h // 2) + 34
        d.line([SAFE_L, ty - 17, SAFE_R, ty - 17], fill=BORDER, width=2)
    if note:
        ty = text_block(d, SAFE_L, ty + 4, note + f' · crops enlarged ×{k}, nearest neighbour', F('sans', 42),
                        SAFE_R - SAFE_L, INK_SOFT, 56)
    assert ty < 1960, f'rows_of_crops overflows ({ty})'
    footer(d, src)
    return im


def fit(img, box_w, box_h):
    r = min(box_w / img.width, box_h / img.height)
    return img.resize((max(1, round(img.width * r)), max(1, round(img.height * r))), Image.LANCZOS), r


def paste_framed(im, d, pic, x, y):
    im.paste(pic, (x, y))
    d.rectangle([x, y, x + pic.width, y + pic.height], outline=BORDER, width=4)


def mark(d, crop, k, ox, oy, px, label, below=False):
    """Outline one capture pixel inside an enlarged crop, with a small label."""
    x = ox + (px[0] - crop[0]) * k
    y = oy + (px[1] - crop[1]) * k
    d.rectangle([x - 6, y - 6, x + k + 6, y + k + 6], outline=SPARK, width=6)
    if label:
        f = F('sans', 36)
        tw = d.textlength(label, font=f)
        lx = x + k + 18
        ly = y + k + 14 if below else y - 52
        d.rounded_rectangle([lx, ly, lx + tw + 32, ly + 56], radius=28, fill=(61, 57, 41))
        d.text((lx + 16, ly + 8), label, font=f, fill=PAGE)


def table(d, x, y, widths, header, rows, size=48, head_size=40, row_h=None, hi_cols=(), wrap_w=True):
    """Simple grid: header in soft ink, rows in ink; columns in hi_cols drawn in the accent."""
    fh = F('sans', head_size)
    fr = F('sans', size)
    lh = int(size * 1.32)
    cx = x
    head_lines = max(len(wrap(d, h, fh, w - 30)) for w, h in zip(widths, header))
    for w, h in zip(widths, header):
        text_block(d, cx, y, h, fh, w - 30, INK_SOFT, int(head_size * 1.3))
        cx += w
    y += head_lines * int(head_size * 1.3) + 18
    d.line([x, y, x + sum(widths), y], fill=BORDER, width=4)
    y += 22
    for row in rows:
        cx = x
        n = 1
        for i, (w, cell) in enumerate(zip(widths, row)):
            fill = SPARK if i in hi_cols else INK
            lines = wrap(d, str(cell), fr, w - 30)
            n = max(n, len(lines))
            for j, line in enumerate(lines):
                d.text((cx, y + j * lh), line, font=fr, fill=fill)
            cx += w
        y += max(n * lh, row_h or 0) + 26
        d.line([x, y - 14, x + sum(widths), y - 14], fill=BORDER, width=2)
    return y


# ---------------------------------------------------------------- layouts
def identity(title, chip, left, right, src):
    """Two captures side by side, each with a caption and fact rows. left/right: {img, badge, caption, rows}."""
    im, d, y = base(title, chip)
    gap = 80
    cw = (SAFE_R - SAFE_L - gap) // 2
    for i, it in enumerate((left, right)):
        x0 = SAFE_L + i * (cw + gap)
        pic, k = enlarge(it['img'], it.get('crop', (0, 0, 640, 360)), cw, 900)
        paste_framed(im, d, pic, x0, y + 10)
        badge(d, x0 + 24, y + 34, it['badge'])
        ty = y + 10 + pic.height + 26
        ty = text_block(d, x0, ty, it['caption'] + f' · enlarged ×{k}, nearest neighbour', F('sans', 40), cw, INK_SOFT, 54)
        ty += 24
        for label, value in it['rows']:
            ty = text_block(d, x0, ty, label, F('serif_med', 76), cw, SPARK, 92)
            ty = text_block(d, x0, ty, value, F('sans', 56), cw, INK, 76) + 26
        assert ty < 1950, f'identity column {i} overflows ({ty})'
    footer(d, src)
    return im


def source_view(title, chip, path, start, text, highlight, note, max_size=56):
    """Dark editor-style source panel (light text), line numbers, wrapped long lines."""
    im, d, y = base(title, chip)
    top = y + 10
    d.rounded_rectangle([SAFE_L, top, SAFE_R, 1935], radius=28, fill=DARK)
    raw = text.split('\n')
    for size in (max_size, 52, 48, 46, 43, 40, 37, 34):
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
            d.rectangle([SAFE_L + 4, ty - 6, SAFE_R - 4, ty + lh - 6], fill=DARK_HI)
            d.rectangle([SAFE_L + 4, ty - 6, SAFE_L + 14, ty + lh - 6], fill=SPARK)
        if first:
            d.text((SAFE_L + 60, ty), f'{num:>4}', font=f, fill=DARK_MUTED)
        d.text((SAFE_L + 250, ty), part, font=f, fill=DARK_TEXT)
        ty += lh
    footer(d, note)
    return im


def crops_and_table(title, chip, img_items, crop, marks, header, rows, widths, src, box_h=640, size=48, hi_cols=()):
    """Several enlarged crops of captures in a row (each with a caption), a results table below.
    img_items: [{'img', 'caption'}]; marks: [(capture_px, label)] drawn on every crop."""
    im, d, y = base(title, chip)
    n = len(img_items)
    gap = 60
    cw = (SAFE_R - SAFE_L - gap * (n - 1)) // n
    bottom = y
    for i, it in enumerate(img_items):
        x0 = SAFE_L + i * (cw + gap)
        pic, k = enlarge(it['img'], crop, cw, box_h)
        px = x0 + (cw - pic.width) // 2
        paste_framed(im, d, pic, px, y + 10)
        for j, (p, label) in enumerate(marks):
            mark(d, crop, k, px, y + 10, p, label if i == 0 else '', below=j % 2 == 1)
        ty = text_block(d, x0, y + 10 + pic.height + 22, it['caption'], F('sans', 44), cw, INK, 58)
        bottom = max(bottom, ty)
    d.text((SAFE_L, bottom + 4), f'Each image: the same crop of a 640×360 capture, enlarged ×{k}, nearest neighbour; '
                                 'outlined squares are the sampled pixels.', font=F('sans', 36), fill=INK_SOFT)
    ty = table(d, SAFE_L, bottom + 90, widths, header, rows, size=size, hi_cols=hi_cols)
    assert ty < 1960, f'crops_and_table overflows ({ty})'
    footer(d, src)
    return im


def crop_beside_table(title, chip, img, crop, marks, img_caption, header, rows, widths, notes, src, size=50, hi_cols=(),
                      img_w=1440, img_h=1380):
    """One enlarged crop (left) with a table and notes (right)."""
    im, d, y = base(title, chip)
    split = SAFE_L + img_w + 60
    pic, k = enlarge(img, crop, img_w, img_h)
    paste_framed(im, d, pic, SAFE_L, y + 10)
    for j, (p, label) in enumerate(marks):
        mark(d, crop, k, SAFE_L, y + 10, p, label, below=j % 2 == 1)
    text_block(d, SAFE_L, y + 10 + pic.height + 22, img_caption + f' · enlarged ×{k}, nearest neighbour',
               F('sans', 40), img_w, INK_SOFT, 54)
    ty = table(d, split + 60, y + 20, widths, header, rows, size=size, hi_cols=hi_cols)
    ty += 30
    for label, value in notes:
        ty = text_block(d, split + 60, ty, label, F('sans', 40), SAFE_R - split - 60, INK_SOFT, 54)
        ty = text_block(d, split + 60, ty, value, F('serif', 60), SAFE_R - split - 60, INK, 74) + 30
    assert ty < 1960, f'crop_beside_table overflows ({ty})'
    footer(d, src)
    return im


def big_capture(title, chip, img, crop, labels, caption, src):
    """One capture region enlarged across the frame. labels: [(capture_xy, text)] placed under that point."""
    im, d, y = base(title, chip)
    pic, k = enlarge(img, crop, SAFE_R - SAFE_L, 1300)
    px = SAFE_L + (SAFE_R - SAFE_L - pic.width) // 2
    paste_framed(im, d, pic, px, y + 10)
    for (cx, cy), text in labels:
        f = F('sans', 50)
        tw = d.textlength(text, font=f)
        x = px + (cx - crop[0]) * k - tw / 2 - 30
        yy = y + 10 + (cy - crop[1]) * k
        d.rounded_rectangle([x, yy, x + tw + 60, yy + 84], radius=42, fill=(61, 57, 41))
        d.text((x + 30, yy + 14), text, font=f, fill=PAGE)
    text_block(d, SAFE_L, y + 10 + pic.height + 26, caption + f' · enlarged ×{k}, nearest neighbour',
               F('sans', 44), SAFE_R - SAFE_L, INK, 58)
    footer(d, src)
    return im


def sweep_grid(title, chip, rows, crop, src):
    """rows: [(uniform, values_label, [min_img, default_img, max_img], (min_obs, max_obs))]."""
    im, d, y = base(title, chip)
    label_w, obs_w, gap = 470, 1010, 28
    img_w = (SAFE_R - SAFE_L - label_w - obs_w - gap * 4) // 3
    heads = ['minimum', 'default (the material’s value)', 'maximum']
    hx = SAFE_L + label_w + gap
    for i, h in enumerate(heads):
        d.text((hx + i * (img_w + gap), y), h, font=F('sans', 38), fill=INK_SOFT)
    d.text((SAFE_R - obs_w, y), 'What the author saw (TEST-REPORT.md)', font=F('sans', 38), fill=INK_SOFT)
    ty = y + 60
    k = None
    for uniform, values, imgs, (lo, hi) in rows:
        row_top = ty
        d.text((SAFE_L, ty), uniform, font=F('mono', 50), fill=INK)
        text_block(d, SAFE_L, ty + 70, values, F('sans', 38), label_w - 20, INK_SOFT, 50)
        for i, img in enumerate(imgs):
            pic, k = fit(img.crop(crop), img_w, 305)
            paste_framed(im, d, pic, hx + i * (img_w + gap), ty)
        oy = text_block(d, SAFE_R - obs_w, ty, 'Min: ' + lo, F('sans', 38), obs_w, INK, 49)
        oy = text_block(d, SAFE_R - obs_w, oy + 6, 'Max: ' + hi, F('sans', 38), obs_w, INK, 49)
        ty = max(row_top + pic.height, oy) + 24
    assert ty < 1950, f'sweep grid overflows ({ty})'
    footer(d, src + f' · crops of the frosted rock enlarged ×{k:.1f}')
    return im


def code_pairs(title, chip, pairs, note, src):
    """pairs: [(left_path, left_line, left_text, right_path, right_line, right_text, annotation)]."""
    im, d, y = base(title, chip)
    gap = 60
    cw = (SAFE_R - SAFE_L - gap) // 2
    fm = F('mono', 58)
    ty = y + 10
    for lp, ll, lt, rp, rl, rt, ann in pairs:
        heights = []
        for i, (path, line, text) in enumerate(((lp, ll, lt), (rp, rl, rt))):
            x0 = SAFE_L + i * (cw + gap)
            parts = wrap(d, text.replace('\t', '    '), fm, cw - 230)
            h = 100 + len(parts) * 80 + 30
            heights.append(h)
            d.rounded_rectangle([x0, ty, x0 + cw, ty + h], radius=24, fill=DARK)
            d.text((x0 + 40, ty + 22), path, font=F('mono', 36), fill='#8BC7F3')
            d.text((x0 + 40, ty + 100), f'{line:>3}', font=fm, fill=DARK_MUTED)
            for j, part in enumerate(parts):
                d.text((x0 + 190, ty + 100 + j * 80), part, font=fm, fill=DARK_TEXT)
        hmax = max(heights)
        ty += hmax + 24
        d.rectangle([SAFE_L, ty, SAFE_L + 10, ty + 2 * 76], fill=SPARK)
        ty = text_block(d, SAFE_L + 40, ty, ann, F('sans', 54), SAFE_R - SAFE_L - 40, INK, 74) + 60
    ty = text_block(d, SAFE_L, ty, note, F('sans', 40), SAFE_R - SAFE_L, INK_SOFT, 54)
    assert ty < 1960, f'code_pairs overflows ({ty})'
    footer(d, src)
    return im


def table_card(title, chip, header, rows, widths, note, src, size=46):
    im, d, y = base(title, chip)
    ty = table(d, SAFE_L, y + 10, widths, header, rows, size=size)
    if note:
        ty = text_block(d, SAFE_L, ty + 20, note, F('sans', 46), SAFE_R - SAFE_L, INK, 62)
    assert ty < 1960, f'table_card overflows ({ty})'
    footer(d, src)
    return im


def columns(title, chip, cols, src, value_size=56, label_size=42):
    """cols: [(head, [(label, value)])]."""
    im, d, y = base(title, chip)
    gap = 48
    cw = (SAFE_R - SAFE_L - gap * (len(cols) - 1)) // len(cols)
    for i, (head, items) in enumerate(cols):
        x0 = SAFE_L + i * (cw + gap)
        panel(d, [x0, y + 10, x0 + cw, 1920])
        ty = text_block(d, x0 + 56, y + 50, head, F('serif_med', 64), cw - 112, SPARK, 76) + 30
        for label, value in items:
            if label:
                ty = text_block(d, x0 + 56, ty, label, F('sans', label_size), cw - 112, INK_SOFT, int(label_size * 1.35))
            ty = text_block(d, x0 + 56, ty, value, F('serif', value_size), cw - 112, INK, int(value_size * 1.26)) + 40
        assert ty < 1920, f'{head}: column overflows ({ty})'
    footer(d, src)
    return im
