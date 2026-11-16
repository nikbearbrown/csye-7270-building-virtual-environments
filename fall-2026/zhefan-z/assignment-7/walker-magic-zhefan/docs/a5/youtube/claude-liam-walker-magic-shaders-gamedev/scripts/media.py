"""Phase 2: build every non-Remotion slot and fill Remotion props, using measured narration.

Adapted from the Assignment 3 film's media.py. No footage and no new capture: every image is one of
the author's in-engine captures in captures/ (PNG, 640x360), shown enlarged. Figures on cards come
from the named source documents; code comes verbatim from the snapshot of the build shown.
"""
from pathlib import Path

from PIL import Image

import cards
from common import (REEL, GAME, A5, CAPS, BUILD, FPS, SNAPSHOT, load_json, save_json, render_frames,
                    source_lines, sha256)

MEDIA = REEL / 'media'
EV = REEL / 'evidence'
SRC = SNAPSHOT or GAME

SCRIPTED = 'In-engine capture · scripted'
TESTS = 'Headless test results, as recorded in TEST-REPORT.md — not a render'
DOC = 'Document view — reconstruction of the text, not a screenshot'
SRCVIEW = 'Source view — reconstruction, not a screenshot'

MAGE = (16, 250, 100, 332)          # the mage at the level start (sprite x 29..91, y 260..327)
ROCKS = (120, 95, 520, 245)         # both rocks in material_compare.tscn
ROCKS_TIGHT = (135, 104, 505, 230)  # the same, cropped close for rows of three
FROSTED = (338, 100, 505, 232)      # the frosted rock only (the sweep changes mat_rock_frosted)
QUADS = (180, 110, 460, 250)        # both hint quads
HAIR, HAT = (56, 278), (53, 267)    # captures/hurt_tint_pixels.json "pixel"


# ---------------------------------------------------------------- helpers
def nframes(bid):
    return render_frames(BEATS[bid]['actual_duration_s'])


def at(bid, phrase):
    """Seconds into the beat where a narration phrase starts (character-proportional estimate)."""
    text = BEATS[bid]['narration_text']
    return round(text.index(phrase) / len(text) * nframes(bid) / FPS, 2)


def remotion(bid, **props):
    rem = BEATS[bid]['shot']['remotion']
    rem['props'].update(props)
    rem['props']['durationSeconds'] = nframes(bid) / FPS


def excerpt(rel, start, end, first):
    text = source_lines(SRC, rel, start, end)
    assert text.split('\n')[0].strip().startswith(first), f'{rel}:{start} does not start with {first!r}'
    if SNAPSHOT:
        assert text == source_lines(GAME, rel, start, end), f'{rel}:{start}-{end} differs from the working tree'
    return text


def still(bid, img, prov, evidence=False):
    img.save(MEDIA / f'{bid}.png')
    BEATS[bid]['shot'].update({'type': 'STILL', 'motion': 'hold'})
    BEATS[bid]['shot'].pop('remotion', None)
    if evidence:
        BEATS[bid]['shot']['evidence_media'] = f'media/{bid}.png'
    PROV[bid] = prov


def cap(name):
    return Image.open(CAPS / name).convert('RGB')


def workbench(bid, title, rel, start, end, first, notes, cues, font=34):
    code = excerpt(rel, start, end, first)
    remotion(bid, mode='code', title=title, project='walker-magic', path=rel,
             source=f'Exact source at {BUILD} · lines {start}–{end} · next: the visible result',
             code=code, startLine=start, codeFontSize=font,
             notes=[{'label': k, 'value': v} for k, v in notes],
             output=[f'Godot editor reconstruction · {rel} lines {start}–{end} · build {BUILD}'],
             cues=[{'at': at(bid, p) if isinstance(p, str) else p, 'line': line, 'label': lab} for p, line, lab in cues])
    BEATS[bid]['excerpt'] = {'path': rel, 'start_line': start, 'end_line': end}


def caps_prov(*names):
    return {'images': [f'captures/{n}' for n in names], 'sha256': {n: sha256(CAPS / n) for n in names}}


# ---------------------------------------------------------------- beats
def build():
    remotion('B00')
    remotion('B29')
    remotion('B01')
    remotion('B28', brandLabel='@NikBearBrown', artifactLines=[
        'Built: hurt_tint.gdshader, driven from Player.invulnerable by hurt_tint_driver.gd; rock_frost.gdshader with a dry '
        'and a frosted material in material_compare.tscn; the hint experiment; tests and capture scenes.',
        'Measured: the controlled pixels as predicted (two .5 channels one step lower, within ±1), 6 of 6 hint values, '
        'hint_range not clamping; 17 / 0 at 30, 60, 144 fps; 32 / 0 materials; 95 / 0 earlier suites.',
        'Judged by the author: the hurt effect in play looked correct; the frost layer showed no blocks; '
        'frost_amount 1.0 hurts readability.',
        'Unknown: why the GPU wrote the .5 channels one step lower; why a pause shifts frame time by more than one '
        'physics step.',
        'Claude Code: driver, tests, materials, scenes, audit, capture tools · claude.ai: planning, checks, drafts · '
        'the author: brief, shaders, computations, answers, human checks · source 40c42f5'])
    BEATS['B30']['shot']['remotion']['props']['durationSeconds'] = nframes('B30') / FPS

    # B02 — the game, the state, the object.
    still('B02', cards.identity('walker-magic: the state and the object',
        f'Game source revision {BUILD} · Godot 4.7.2-stable · Forward+', {
            'img': cap('hurt_tint_i0.0.png'), 'badge': SCRIPTED,
            'caption': 'game/main.tscn at the start of the level, the mage idle (hurt_tint_i0.0.png)',
            'rows': [('The state: post-hit invulnerability', 'Player.invulnerable, seconds left: set to 1.0 when a hit '
                      'lands (player.gd:155), counted down with physics delta (player.gd:80); hits are ignored while it '
                      'is above 0 (player.gd:152).')]}, {
            'img': cap('rock_compare_default.png'), 'badge': SCRIPTED, 'crop': ROCKS,
            'caption': 'showcase3d/material_compare.tscn (rock_compare_default.png)',
            'rows': [('The object: the rock', 'rock.glb from Assignment 3, twice. Surface 0, Rock_Main, carries '
                      'surface_material_override/0; Rock_Top (surface 1) keeps its imported material.')]},
        'CHANGE-BRIEF.md section 1, section 4 and revision 2026-10-27 · captures/ at 40c42f5'),
        caps_prov('hurt_tint_i0.0.png', 'rock_compare_default.png'))

    # B03 — the colour line as specified (a document, outside the Godot project).
    brief = (A5 / 'CHANGE-BRIEF.md').read_text(encoding='utf-8').splitlines()
    assert brief[46] == 'COLOR.rgb = mix(COLOR.rgb, tint_color.rgb, intensity);'
    still('B03', cards.source_view('Question 1 · The colour line, specified first', DOC,
                                   'CHANGE-BRIEF.md · lines 38–52', 38, '\n'.join(brief[37:52]), {47, 52},
                                   'The author’s specification (original version 2026-10-22, CHANGE-BRIEF.md line 3); '
                                   'the shader was typed afterwards', max_size=50),
          {'card': 'media/B03.png', 'source': 'CHANGE-BRIEF.md:38-52'})

    # B04 -> B05
    workbench('B04', 'Question 1 · What a shader does', 'shaders/hurt_tint.gdshader', 1, 7, 'shader_type canvas_item', [
        ('LANGUAGE-NOTES.md, answer 2', 'fragment() runs for every pixel the object covers'),
        ('CHANGE-BRIEF.md section 6', 'COLOR = texture colour × vertex colour')],
        [(0.0, 1, 'shader_type canvas_item: a 2D shader'), ('A shader is', 6, 'fragment(): runs for every covered pixel'),
         ('this line mixes', 7, 'Line 7: mix toward tint_color by intensity; COLOR.a untouched')], font=34)
    rows = [('Hair (27, 18)', '0.0', '(232, 230, 240)', '(232, 230, 240)'),
            ('Hat (24, 7)', '0.0', '(58, 64, 160)', '(58, 64, 160)'),
            ('Hair', '0.5', '(244, 115, 120)', '(243, 115, 120)'),
            ('Hat', '0.5', '(157, 32, 80)', '(156, 32, 80)'),
            ('Hair', '1.0', '(255, 0, 0)', '(255, 0, 0)'),
            ('Hat', '1.0', '(255, 0, 0)', '(255, 0, 0)')]
    still('B05', cards.crops_and_table('Controlled values: predicted, then measured',
        SCRIPTED + ' · HurtTint driver off, intensity set from code, tint_color its default red', [
            {'img': cap('hurt_tint_i0.0.png'), 'caption': 'intensity 0.0 · hurt_tint_i0.0.png'},
            {'img': cap('hurt_tint_i0.5.png'), 'caption': 'intensity 0.5 · hurt_tint_i0.5.png'},
            {'img': cap('hurt_tint_i1.0.png'), 'caption': 'intensity 1.0 · hurt_tint_i1.0.png'}],
        MAGE, [(HAT, 'hat (24, 7)'), (HAIR, 'hair (27, 18)')],
        ['Texture pixel of mage_idle.png', 'intensity', 'Predicted (CHANGE-BRIEF.md)', 'Measured (viewport pixel)'],
        rows, [900, 420, 1060, 1076],
        'TEST-REPORT.md → Controlled values · captures/hurt_tint_pixels.json · the two .5 channels (243.5, 156.5) '
        'were allowed ±1 in the brief', box_h=720, size=44, hi_cols=(3,)),
        {**caps_prov('hurt_tint_i0.0.png', 'hurt_tint_i0.5.png', 'hurt_tint_i1.0.png'), 'json': 'captures/hurt_tint_pixels.json'},
        evidence=True)

    # B06 -> B07
    workbench('B06', 'Question 2 · How a material differs from a shader', 'features/player/hurt_tint_driver.gd', 6, 15,
              '@onready var player', [
        ('CHANGE-BRIEF.md:207', 'default in the shader; current value in the ShaderMaterial'),
        ('player.tscn:9', 'resource_local_to_scene = true')],
        [(0.0, 10, '_process(): runs every frame'), ('Line fifteen', 15, 'set_shader_parameter: one number into the material'),
         ('The shader holds', 7, 'material: the sprite’s ShaderMaterial, not the shader')], font=27)
    still('B07', cards.table_card('The driver, in the real game loop', TESTS, ['Rule', 'Result'], [
        ('Driver at 30 / 60 / 144 fps, real game loop, real key events and real wolf lunges',
         '17 checks / 0 failures at each rate'),
        ('R1 first value', '0.9833 at all three rates (minimum allowed 0.95 / 0.9667 / 0.9764)'),
        ('R4 duration (game time)', '1.0000 s / 0.9833 s / 0.9861 s, within one frame (one physics step at 144)'),
        ('R7 pause', 'value held through 31 paused frames and resumed; 60 / 59 / 59 unpaused physics ticks from first '
                     'tint to zero'),
        ('R8 / F4', 'intensity 0.0 from the frame of an HP-0 fail (with invulnerable frozen at 1.0), a pit fall during '
                    'the state, and a clear during the state'),
        ('R9', 'a reloaded scene starts at 0.0 with a different material object')],
        [1250, 2206], 'Headless: every check reads the value the driver sends to the shader, never a pixel.',
        'TEST-REPORT.md → Machine checks · logs/test_hurt_tint_30fps.log, _60fps, _144fps', size=58),
        {'card': 'media/B07.png', 'source': 'TEST-REPORT.md:19-26'}, evidence=True)

    # B08 — hint_range and a value from code.
    still('B08', cards.crop_beside_table('A value from code, past the slider',
        SCRIPTED + ' · tint_color Color(0.5, 0.5, 0.5, 1.0) and intensity 2.0, both set from code',
        cap('hurt_tint_grey_i2.0.png'), MAGE, [(HAT, 'hat'), (HAIR, 'hair')], 'hurt_tint_grey_i2.0.png',
        ['Pixel', 'If not clamped', 'If clamped', 'Measured'],
        [('Hair', '(23, 25, 15)', '(128, 128, 128)', '(23, 25, 15)'),
         ('Hat', '(197, 191, 95)', '(128, 128, 128)', '(197, 191, 95)')],
        [300, 540, 540, 516],
        [('Prediction if not clamped (TEST-REPORT.md)', '2 × 127.5 − stored'),
         ('hurt_tint.gdshader line 4', 'intensity : hint_range(0.0, 1.0)'),
         ('LANGUAGE-NOTES.md, answer 5', 'No. The limit only exists in the Inspector.')],
        'TEST-REPORT.md → hint_range and a value from code · captures/hurt_tint_pixels.json', size=46, hi_cols=(3,)),
        {**caps_prov('hurt_tint_grey_i2.0.png'), 'json': 'captures/hurt_tint_pixels.json'})

    # B09 -> B10
    workbench('B09', 'Question 2 · Two materials, one shader', 'assets/materials/mat_rock_frosted.tres', 8, 17,
              '[resource]', [
        ('mat_rock_dry.tres:10', 'base_tint = Color(1, 1, 1, 1)'),
        ('mat_rock_dry.tres:14', 'frost_amount = 0.0'),
        ('Both files, line 3', 'rock_frost.gdshader')],
        [(0.0, 9, 'shader: one reference to rock_frost.gdshader'),
         ('base tint white', 10, 'base_tint: the dry material has Color(1, 1, 1, 1)'),
         ('frost amount zero', 14, 'frost_amount: the dry material has 0.0')], font=30)
    still('B10', cards.big_capture('One shader, two materials, two rocks', SCRIPTED + ' · F9 · showcase3d/material_compare.tscn',
        cap('rock_compare_default.png'), ROCKS,
        [((217, 230), 'RockDry · mat_rock_dry.tres'), ((421, 230), 'RockFrosted · mat_rock_frosted.tres')],
        'rock_compare_default.png · both overrides on surface 0, Rock_Main; the small top stones are Rock_Top, '
        'which keeps its imported Assignment 3 material',
        'captures/rock_compare_default.png · CHANGE-BRIEF.md revision 2026-10-27'),
        caps_prov('rock_compare_default.png'), evidence=True)

    # B11 — change a material, then the shader.
    still('B11', cards.rows_of_crops('Change a material, then the shader', SCRIPTED + ' · F9, F11, F12', [
        {'img': cap('rock_compare_default.png'), 'cells': ['rock_compare_default.png', '67.9', '84.0', '—']},
        {'img': cap('rock_one_material_changed.png'),
         'cells': ['rock_one_material_changed.png\nnormal_scale 0 on the dry material only', '66.1', '84.0', '6031 / 0']},
        {'img': cap('rock_compare_after_shader_edit.png'),
         'cells': ['rock_compare_after_shader_edit.png\nthe author’s edit of rock_frost.gdshader:28, * 0.5',
                   '54.7', '73.7', '8225 / 8103']}],
        ROCKS_TIGHT, ['Capture', 'Dry rock (left)', 'Frosted rock (right)', 'Pixels changed, left / right'],
        [1060, 360, 360, 416],
        'Mean brightness of the non-background pixels, and pixels changed against the default capture. The shader '
        'edit was reverted afterwards',
        'TEST-REPORT.md → One shader, two materials', img_w=1140, img_h=400, size=44),
        caps_prov('rock_compare_default.png', 'rock_one_material_changed.png', 'rock_compare_after_shader_edit.png'))

    # B12 -> B13
    workbench('B12', 'Question 3 · Why a texture is information', 'shaders/hint_experiment.gdshader', 1, 14,
              'shader_type spatial', [
        ('greys_3x1.png', 'texels 64, 128, 192; lossless, no mipmaps'),
        ('hint_experiment.tscn:10–14', 'Linear tonemap, exposure 1.0; glow, fog, adjustments off')],
        [(0.0, 1, 'shader_type spatial'), ('Two samplers', 4, 'source_color_tex: source_color, filter_nearest'),
         ('one not', 5, 'raw_data_tex: filter_nearest only'), ('on unshaded quads', 2, 'render_mode unshaded')], font=24)
    hint = load_json(CAPS / 'hint_pixels.json')['samples']
    marks = [(tuple(s['pixel']), str(s['rgb8'][0])) for s in hint]
    still('B13', cards.crop_beside_table('Same bytes, two meanings', SCRIPTED + ' · F9 · showcase3d/hint_experiment.tscn',
        cap('hint_quads.png'), QUADS, marks,
        'hint_quads.png · left quad: source_color_tex; right quad: raw_data_tex · labels: measured value',
        ['Texel', 'With source_color: predicted / measured', 'Without: predicted / measured'],
        [('64', '64 / 64', '137 / 137'), ('128', '128 / 128', '188 / 188'), ('192', '192 / 192', '225 / 225')],
        [200, 590, 586],
        [('Without the hint (CHANGE-BRIEF.md section 3)', 'encode(x) = 1.055·x^(1/2.4) − 0.055, for x = stored / 255'),
         ('TEST-REPORT.md', 'All six as predicted.')],
        'TEST-REPORT.md → Hint experiment · captures/hint_pixels.json', size=48, img_w=1960, img_h=1200),
        {**caps_prov('hint_quads.png'), 'json': 'captures/hint_pixels.json'}, evidence=True)

    # B14 -> B15
    workbench('B14', 'Question 3 · Colour, and data', 'shaders/rock_frost.gdshader', 15, 19, 'group_uniforms textures', [
        ('diff (MATERIALS.md)', 'mode 2 · normal_map 2 · DXT1'),
        ('nor_gl', 'mode 2 · normal_map 1 · RGTC_RG'),
        ('rough', '16-bit source · mode 2 · DXT1')],
        [(0.0, 15, 'group_uniforms textures'), ('Line sixteen', 16, 'albedo: source_color, decoded from sRGB'),
         ('Line seventeen', 17, 'normal map: hint_normal, no source_color: data'),
         ('Line eighteen', 18, 'roughness: data, read as stored')], font=33)
    check = source_lines(SRC, 'tests/normal_map_check.gd', 1, 3)
    still('B15', cards.columns('Data, checked as data', TESTS, [
        ('The curl check on the normal maps', [
            ('rock_01_nor_gl_1k.png · bound to both rock materials', 'OpenGL 0.1444 · DirectX 1.8556'),
            ('rock_01_nor_dx_1k.png · not bound', 'OpenGL 1.8556 · DirectX 0.1444'),
            ('The check’s own legend · tests/normal_map_check.gd lines 1–3', check.replace('# ', '')),
            ('Threshold, from the calibration', 'bound map below 0.5 in OpenGL and above 1.5 in DirectX')]),
        ('Remove the colour hint', [
            ('Mutation: source_color removed from rock_frost.gdshader:16',
             'sampler-hints:...:texture_albedo fails, exit 1; shader restored'),
            ('Imported formats (TEST-REPORT.md)', 'DXT1 (albedo, roughness), RGTC_RG (normals), RGB8 (hint)'),
            ('Godot expects (CHANGE-BRIEF.md section 4)', 'the OpenGL green convention')])],
        'TEST-REPORT.md → Machine checks · logs/calibrate_normal_check_60fps.log · logs/mutation-3-source-color_60fps.log',
        value_size=66, label_size=46),
        {'card': 'media/B15.png', 'source': 'TEST-REPORT.md:29-31'}, evidence=True)

    # B16 -> B17
    workbench('B16', 'Question 3 · Where the frost goes', 'shaders/rock_frost.gdshader', 30, 35, '//', [
        ('Comments, translated for this film', '31: half-band 0.1 (band 0.2)\n32: frost_amount 0 → 1 moves the '
         'threshold −0.1 → 1.1\n34: below the threshold, more frost')],
        [(0.0, 30, 'Step 3: the frost mask'), ('compared with a threshold', 33, 'threshold: frost_amount slides it from −0.1 to 1.1'),
         ('Below it', 35, 'frost_mask: 1 where roughness is below the threshold, with a soft band')], font=30)
    still('B17', cards.rows_of_crops('Frost amount, swept', SCRIPTED + ' · F10 · mat_rock_frosted only', [
        {'img': cap('rock_sweep_frost_amount_min.png'),
         'cells': ['frost_amount_min.png', '0.0', 'frost gone; the right rock matches the bare left rock']},
        {'img': cap('rock_sweep_frost_amount_default.png'),
         'cells': ['frost_amount_default.png', '0.65', 'a frost layer and no blocks, at 640×360']},
        {'img': cap('rock_sweep_frost_amount_max.png'),
         'cells': ['frost_amount_max.png', '1.0', 'the whole rock covered in a white crust; the rock texture is almost '
                                                    'gone and the bright parts are close to blown out']}],
        ROCKS_TIGHT, ['Capture (rock_sweep_)', 'frost_amount', 'What the author saw (translated from Chinese)'],
        [700, 330, 1166],
        '“frost_amount = 1.0 loses almost all rock detail and becomes a near-white block, which hurts readability.”',
        'TEST-REPORT.md → Interface sweep · the DXT1 audit prediction', img_w=1140, img_h=400, size=44),
        caps_prov('rock_sweep_frost_amount_min.png', 'rock_sweep_frost_amount_default.png', 'rock_sweep_frost_amount_max.png'),
        evidence=True)

    # B18 -> B19
    workbench('B18', 'Question 3 · The material’s interface', 'shaders/rock_frost.gdshader', 3, 12, '//', [
        ('Lines 3 and 9, translated', 'surface group · frost group'),
        ('The sweep (TEST-REPORT.md)', 'min, own value, max; colours black and white')],
        [(0.0, 4, 'group_uniforms surface'), ('five values', 5, 'base_tint: source_color colour'),
         ('three numbers', 6, 'hint_range(0.0, 2.0, 0.05)'), ('swept every one', 12, 'frost_amount: hint_range(0.0, 1.0, 0.01)')],
        font=26)
    sweep = []
    for u, values, lo, hi in (
            ('base_tint', 'black · (0.92, 0.95, 1) · white', 'the rock’s base turns black; only the white frost patches '
             'float on a dark base', 'the natural grey-brown rock, brightest'),
            ('normal_scale', '0 · 1.0 · 2', 'surface relief flattened; facets stay sharp but look smooth, like plastic',
             'pits and grain much stronger, harder and deeper shading'),
            ('roughness_scale', '0 · 1.0 · 2', 'very smooth; lit faces show a sharp white highlight',
             'fully matte; the highlight spreads out and flattens'),
            ('frost_color', 'black · (0.85, 0.92, 1) · white', 'frost areas turn dark grey-black, like soot deposits',
             'clean bright white snow, strongest contrast')):
        sweep.append((u, values, [cap(f'rock_sweep_{u}_{w}.png') for w in ('min', 'default', 'max')], (lo, hi)))
    names = [f'rock_sweep_{u}_{w}.png' for u, *_ in sweep for w in ('min', 'default', 'max')]
    still('B19', cards.sweep_grid('The interface, swept', SCRIPTED + ' · F10 · mat_rock_frosted only', sweep, FROSTED,
                                  'TEST-REPORT.md → Interface sweep (translated from Chinese) · captures/rock_sweep_*.png'),
          caps_prov(*names), evidence=True)

    # B20 -> B21
    workbench('B20', 'Question 4 · What the Godot shading language is', 'shaders/hurt_tint.gdshader', 1, 4,
              'shader_type canvas_item', [
        ('rock_frost.gdshader:1', 'shader_type spatial;'),
        ('LANGUAGE-NOTES.md, answer 1', 'picks 2D or 3D, and so the built-ins'),
        ('LANGUAGE-NOTES.md, answer 8', 'hints, group_uniforms: not plain GLSL')],
        [(0.0, 1, 'shader_type canvas_item: the 2D pipeline'), ('Lines three and four', 3, 'source_color: a Godot hint'),
         ('hint range', 4, 'hint_range(0.0, 1.0): a Godot hint')], font=40)
    still('B21', cards.identity('One language, two pipelines', SCRIPTED, {
            'img': cap('hurt_tint_i1.0.png'), 'badge': 'canvas_item', 'crop': (0, 200, 320, 360),
            'caption': 'hurt_tint_i1.0.png · hurt_tint.gdshader line 1',
            'rows': [('2D, unlit', 'the shader mixes COLOR directly (hurt_tint.gdshader line 7)')]}, {
            'img': cap('rock_compare_default.png'), 'badge': 'spatial', 'crop': ROCKS,
            'caption': 'rock_compare_default.png · rock_frost.gdshader line 1',
            'rows': [('3D, with lighting', 'the shader writes ALBEDO, ROUGHNESS, NORMAL_MAP and NORMAL_MAP_DEPTH '
                      '(rock_frost.gdshader lines 38, 43, 46, 47); one DirectionalLight3D, “Sun”')]},
        'LANGUAGE-NOTES.md answers 1 and 3 · MATERIALS.md → Lights and environment'),
        caps_prov('hurt_tint_i1.0.png', 'rock_compare_default.png'), evidence=True)

    # B22 — the generated shader beside the author's (LANGUAGE-NOTES.md, two annotated pairs).
    std, mine = 'shaders/standard_generated.gdshader', 'shaders/rock_frost.gdshader'
    still('B22', cards.code_pairs('The shader Godot writes', SRCVIEW, [
        (std, 7, source_lines(SRC, std, 7, 7), mine, 16, source_lines(SRC, mine, 16, 16),
         'Both mark the albedo as sRGB colour, so it is decoded to linear when sampled. The generated one adds '
         'repeat_enable; mine uses the default repeat.'),
        (std, 19, source_lines(SRC, std, 19, 19), mine, 17, source_lines(SRC, mine, 17, 17),
         'Neither has source_color, so both read the normal map as data. The generated one uses hint_roughness_normal, '
         'which also links the normal map to the roughness texture (std:14, hint_roughness_r); mine uses plain hint_normal.')],
        'Generated by Godot 4.7.2 from a StandardMaterial3D (Convert to ShaderMaterial, then Save As), by the author in '
        'the editor; nothing in the game uses it.',
        'LANGUAGE-NOTES.md → The generated shader (annotations verbatim) · exact source at 40c42f5'),
        {'card': 'media/B22.png', 'source': f'{std}:7,19 · {mine}:16,17'})

    # B23 — what the tests proved.
    still('B23', cards.table_card('What the tests proved', TESTS, ['Check', 'Result'], [
        ('Baseline before', '7 suites at 60 fps: a3_assets 22, audio 13, cast 11, flow 14, player 11, sound_triggers 11, '
                            'wolf 13; 95 checks / 0 failures'),
        ('Baseline after', 'same 95 checks / 0 failures, every check line identical to the baseline'),
        ('Hurt-tint shader parses, names and types', 'tint_color (Color) and intensity (float, range 0–1); defaults read '
                                                     'from the source text'),
        ('Driver at 30 / 60 / 144 fps', '17 checks / 0 failures at each rate'),
        ('Material wiring', 'test_materials.gd: 32 checks / 0 failures'),
        ('Fresh import', 'deleted walker-magic-zhefan/.godot, reimported: 32 / 0, no .import file rewritten')],
        [1200, 2256], 'Every test ran through ./scripts/run-test.sh, which pins --fixed-fps, keeps a log, and fails on '
                      'SHADER ERROR / SCRIPT ERROR.',
        'TEST-REPORT.md → Machine checks (shortened)', size=58),
        {'card': 'media/B23.png', 'source': 'TEST-REPORT.md:6,14-28'})

    # B24 — the three mutations, and what no headless run shows.
    still('B24', cards.columns('Broken on purpose, and the limit', 'From TEST-REPORT.md', [
        ('Three mutations', [
            ('Parse: a semicolon deleted', 'SHADER ERROR: Expected a \';\'. · empty uniform list · exit 1'),
            ('Rename: intensity, in the shader only', 'no SHADER ERROR; uniform-list and source-default checks fail, '
                                                      'the other 15 pass; exit 1'),
            ('source_color removed from rock_frost.gdshader:16', 'sampler-hints:...:texture_albedo fails, exit 1; '
                                                                 'shader restored')]),
        ('What no headless run shows', [
            ('', 'The look of either shader, whether red appears on screen, whether transparent pixels stay transparent, '
                 'how the frost settles, whether the normal map lights the rock correctly, and real (not simulated) '
                 'frame timing.'),
            ('', 'Those are the human checks: the captures and play in this film.')])],
        'TEST-REPORT.md → Machine checks · What no headless run shows · logs/mutation-1, -2, -3', value_size=70, label_size=48),
        {'card': 'media/B24.png', 'source': 'TEST-REPORT.md:17-18,29,111'})

    # B25 — the agent's mistakes, caught (FRICTIONAL.md 4, 6, 8).
    still('B25', cards.columns('What the agent got wrong', 'FRICTIONAL.md entries 4, 6 and 8 · agent = Claude Code', [
        ('4 · The CLAUDE.md draft', [
            ('The agent', 'cited a log that was not committed and is overwritten on every run, and described the blink '
                          'as toggling every tick (it toggles every 0.1 s).'),
            ('The author', 'checked every file reference with sed -n, fixed those two, and added Headless facts '
                           '(d893e68).')]),
        ('6 · R7 failed at 144 fps', [
            ('The agent', 'measured the paused window in frame time (0.9653 s at 144) and offered to widen the '
                          'tolerance or drop the clause.'),
            ('The author', 'rejected both; revised the brief to count unpaused physics ticks (b81bad4): 59 ticks '
                           '(9072f67).')]),
        ('8 · Use External', [
            ('The agent', 'found it would break test_a3_assets.gd:106–107, and recommended letting the test fail.'),
            ('The author', 'rejected that and the prop-room override; scene overrides in a new material_compare.tscn '
                           '(47ce061). Earlier suites: 95 / 0.')])],
        'FRICTIONAL.md → Entries', value_size=64, label_size=48),
        {'card': 'media/B25.png', 'source': 'FRICTIONAL.md:13,17,21'})

    # B26 — uncertain, and one next step.
    still('B26', cards.columns('Still uncertain, and one next step', 'FRICTIONAL.md → Still open · README.md → Known limitations', [
        ('Still open', [
            ('Untested explanation', 'Why the .5 channels round down on the GPU.'),
            ('Untested explanation', 'Why a pause shifts summed frame time by more than one physics step.')]),
        ('Known limitations', [
            ('', 'ice_roughness (0.15) is a constant, not a uniform; roughness_scale does not move where frost settles.'),
            ('', 'The textured shader appears only in the 3D showcase scenes; the 2D level has no rock.'),
            ('', 'The imported roughness map is DXT1 (error up to 13 of 255); no blocking was visible in the captures.')]),
        ('One next step', [
            ('Proposed by this film', 'Test the rounding: more controlled values whose mix lands on .5, captured in '
                                      'the engine and compared with round-half-up.')])],
        'FRICTIONAL.md · README.md', value_size=66, label_size=48),
        {'card': 'media/B26.png', 'source': 'FRICTIONAL.md:39 · README.md:29-32'})

    # B27 — who did what.
    still('B27', cards.columns('Who did what', 'Rock 01 textures: Poly Haven, Rob Tuytel, CC0 · game source revision 40c42f5', [
        ('The author', [
            ('', 'Every decision in CHANGE-BRIEF.md and its revisions; the colour line and all uniform and sampler '
                 'declarations; all hand computations.'),
            ('', 'The three shaders, typed by hand; the language answers; every human check, capture key press, play '
                 'test, and the editor conversion of the generated shader.')]),
        ('Claude Code', [
            ('', 'The CLAUDE.md draft, the driver, test_hurt_tint.gd, the hint PNG writer, the four materials, two '
                 'scenes, the calibration and inspection scripts, the audit (MATERIALS.md, test_materials.gd) and the '
                 'capture scenes.')]),
        ('claude.ai (chat)', [
            ('', 'Planning, commands, checking arithmetic and line references, compiling CHANGE-BRIEF and LANGUAGE-NOTES '
                 'from the author’s answers, and drafting FRICTIONAL and TEST-REPORT.'),
            ('', 'Syntax examples for rock_frost and hint_experiment, and the idea of widening the frost threshold '
                 'beyond 0–1.')])],
        'FRICTIONAL.md → Human and AI contributions · SOURCES.md', value_size=62),
        {'card': 'media/B27.png', 'source': 'FRICTIONAL.md:31-35 · SOURCES.md:13'})


def main():
    global BEATS, PROV
    MEDIA.mkdir(exist_ok=True)
    sheet = load_json(REEL / 'beat_sheet.json')
    BEATS = {b['beat_id']: b for b in sheet['beats']}
    PROV = {}
    build()
    save_json(REEL / 'beat_sheet.json', sheet)
    save_json(EV / 'media-provenance.json', {
        'note': 'How each non-Remotion slot was made. Every image is an in-engine capture from captures/ at 40c42f5 '
                '(640x360), cropped and enlarged on a card; nothing was re-captured for this film.',
        'beats': PROV})
    print('media built:', ', '.join(sorted(PROV)))


if __name__ == '__main__':
    main()
