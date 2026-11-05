"""Phase 2: build every non-Remotion slot and fill Remotion props, using measured narration.

Adapted from the Assignment 2 film's media.py. Footage rule: the B16 clip is cut from the Movie
Maker take at normal speed, every second 60 fps source frame for 30 fps output, to exactly the
frame count the compiler gives the beat, so compile.py never retimes, slows or center-cuts it.
The surplus after the 12 s take is a final-frame hold labelled "Held frame" on screen.
"""
import json
from pathlib import Path

from PIL import Image

import cards
from common import (REEL, GAME, A3, BUILD, FPS, SRC_FPS, W, H, SNAPSHOT, load_json, save_json, render_frames,
                    run, probe_frames, source_lines, sha256)

CAP = REEL / 'capture'
MEDIA = REEL / 'media'
WORK = MEDIA / '_work'
EV = REEL / 'evidence'
ENC = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-an']
SRC = SNAPSHOT or GAME

MINE = 'My screenshot'
LOOK = 'Blender MCP look render — captured by Claude Code'
PYVIEW = 'Source view · Blender Python, run through the MCP — not Godot'
DISCLOSE = 'Godot Movie Maker capture · scripted camera · run-01 · build 8d8895c · capture copy · viewport set to 3840×2160'


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


def still(bid, img, prov, **extra):
    img.save(MEDIA / f'{bid}.png')
    BEATS[bid]['shot'].update({'type': 'STILL', 'motion': 'hold'})
    BEATS[bid]['shot'].pop('remotion', None)
    BEATS[bid].update(extra)
    PROV[bid] = prov


def shot(path):
    return Image.open(path).convert('RGB')


def pyview(bid, title, rel, start, end, first, hi, note):
    code = excerpt(rel, start, end, first)
    still(bid, cards.source_view(title, PYVIEW, f'{rel} · lines {start}–{end}', start, code, hi,
                                 f'{note} · exact source at {BUILD}'),
          {'card': f'media/{bid}.png', 'source': f'{rel}:{start}-{end}'},
          source_view={'path': rel, 'start_line': start, 'end_line': end})


def workbench(bid, title, rel, start, end, first, notes, cues, font=30):
    code = excerpt(rel, start, end, first)
    remotion(bid, mode='code', title=title, project='walker-magic', path=rel,
             source=f'Exact source at {BUILD} · lines {start}–{end} · next: the visible result',
             code=code, startLine=start, codeFontSize=font,
             notes=[{'label': k, 'value': v} for k, v in notes],
             output=[f'Godot editor reconstruction · {rel} lines {start}–{end} · build {BUILD}'],
             cues=[{'at': at(bid, p) if isinstance(p, str) else p, 'line': line, 'label': lab} for p, line, lab in cues])
    BEATS[bid]['excerpt'] = {'path': rel, 'start_line': start, 'end_line': end}


def footage_with_hold(take, out, total, overlays_png, held_png):
    """The whole take at normal speed (every 2nd 60 fps frame), then its final frame held."""
    src_n = probe_frames(CAP / f'{take}.avi')[0]
    live = src_n // 2
    hold = total - live
    assert hold >= 0, f'{take}: beat shorter than the take'
    graph = (f"[0:v]select='not(mod(n\\,2))',setpts=N/{FPS}/TB,tpad=stop_mode=clone:stop={hold}[v0];"
             f"[v0][1:v]overlay=0:0[v1];"
             f"[v1][2:v]overlay=0:0:enable='gte(n\\,{live})'[v2];"
             f"[v2]scale=in_range=full:out_range=tv,format=yuv420p[vout]")
    run(['ffmpeg', '-y', '-v', 'error', '-i', CAP / f'{take}.avi', '-loop', '1', '-i', overlays_png,
         '-loop', '1', '-i', held_png,
         '-filter_complex', graph, '-map', '[vout]', '-frames:v', str(total)] + ENC + [out])
    got = probe_frames(out)[0]
    assert got == total, f'{out}: {got} frames, expected {total}'
    return {'take': take, 'src_frames': src_n, 'src_frame_start': 0, 'src_frame_end': src_n,
            'take_start_s': 0.0, 'take_end_s': src_n / SRC_FPS, 'live_frames': live, 'held_frames': hold,
            'sha256_take': sha256(CAP / f'{take}.avi')}


def status_inset(img):
    w, h = img.size
    return (int(w * 0.83), int(h * 0.974), int(w * 0.93), h)


# ---------------------------------------------------------------- beats
def build():
    remotion('B00')
    remotion('B21')
    remotion('B01')
    remotion('B20', brandLabel='@NikBearBrown', artifactLines=[
        'Built: rock, crystal and chest through the Blender MCP, their .glb and .import files, a prop room and a headless check.',
        'Measured: size, origin, transforms, triangles and colours — headless, 22 checks / 0 failures; the .glb files read back.',
        'Judged by the author: upright, closed undersides, and that they read as a rock, a crystal and a chest.',
        'Unknown: how the 0.066 m floor gap and the crystal’s glow look in real play, under the cave’s light.',
        'Claude Code: Blender code, exports, scene, check · Claude (chat): sizes, colours, build prompts, documents · the author: choices, approvals, hand edit, looks · source 8d8895c'])
    BEATS['B22']['shot']['remotion']['props']['durationSeconds'] = nframes('B22') / FPS

    # B02 — the assignment and the three props.
    still('B02', cards.brief_card('The assignment, and this game', 'walker-magic-zhefan · a 2D pixel-art fire mage in a cold cave',
        'Assignment 3 asks for', [
            ('Three props from basic shapes', 'At most six shapes and 500 triangles each, a flat-colour material.'),
            ('Built with Claude through the Blender MCP', 'In a running Blender; the code Claude ran kept in tools/blender/.'),
            ('One edit by hand', 'Made in Blender’s own window.'),
            ('A small Godot 3D scene and a headless check', 'Floor, one light, a camera, the props side by side at game scale.')],
        'The three props (CHANGE-BRIEF.md)', [
            ('Rock · 1.0 × 0.8 × 0.7 m', 'A roadblock on the path that the player jumps over.'),
            ('Crystal · 0.35 × 0.35 × 0.6 m', 'Decoration: a cold glow in the cave scenery.'),
            ('Treasure chest · 0.8 × 0.5 × 0.6 m', 'The reward at the exit after a cleared level — warm on purpose.'),
            ('Palette rule', 'The cave is cold; warmth belongs only to fire and to what fire makes safe.')],
        'Summarised from the Assignment 3 text and CHANGE-BRIEF.md (committed before any building, c75176a)'),
        {'card': 'media/B02.png'})

    # B03 — learning the window: the author's three measurements.
    items = []
    for name, cap in (('blender-learn-uv-sphere-960-tris.png', 'Default UV sphere (32 segments, 16 rings): 960 triangles'),
                      ('blender-learn-icosphere-subdiv1-20-tris.png', 'Ico sphere, subdivisions 1: 20 triangles'),
                      ('blender-learn-cone-6-verts-10-tris.png', 'Cone, 6 vertices: 10 triangles')):
        img = shot(A3 / 'evidence' / name)
        items.append({'img': img, 'badge': MINE, 'caption': cap,
                      'insets': [(status_inset(img), 'Status bar: vertices, faces, then the triangle count', False)]})
    still('B03', cards.gallery('Learning the window: measured, not guessed', 'The author’s own Blender 5.2.2 session',
                               items, 'evidence/blender-learn-*.png in assignment-3 · Scene Statistics in the status bar'),
          {'card': 'media/B03.png', 'images': [f'assignment-3/evidence/{n}' for n in (
              'blender-learn-uv-sphere-960-tris.png', 'blender-learn-icosphere-subdiv1-20-tris.png',
              'blender-learn-cone-6-verts-10-tris.png')]})

    # B04 — the Rock prompt (verbatim) and the approval screenshot.
    still('B04', cards.prompt_and_shot('The prompt, and the approval', 'Every asset started with a written prompt and a plan',
        'Excerpt from the Claude Code session · the Rock prompt', [
            'Task: build only this asset: Rock, exactly as the brief specifies (size in metres, origin, materials, '
            'triangle budget). Start from an empty scene with metric units; Blender is Z-up.',
            'Do not export yet, do not save the .blend yet, and do not commit anything. Say what you could not verify.'],
        'Two lines, word for word, from the author’s prompt in the Claude Code session, 2026-10-14 (PROMPTS.md)',
        shot(A3 / 'evidence' / 'claude-code-rock-plan-approval.png'), MINE,
        'Claude Code’s plan question for the Rock, and the button the author pressed: “Yes, build it”.',
        'evidence/claude-code-rock-plan-approval.png in assignment-3'),
        {'card': 'media/B04.png', 'image': 'assignment-3/evidence/claude-code-rock-plan-approval.png'})

    # B05 -> B06
    pyview('B05', 'Rock, Revision 1: size from the vertices', 'tools/blender/build_rock.py', 309, 319,
           '# Bake: lowest face', {310, 311, 312, 316, 317, 318}, 'Call R2 (Rock_A)')
    still('B06', cards.gallery('The rock: before and after the revision', LOOK, [
        {'img': shot(EV / 'look' / 'rock-first-build.png'), 'badge': 'First build',
         'caption': 'Fit X 1.19, Y 1.12: read as three separate stones, “like dice”.'},
        {'img': shot(EV / 'look' / 'rock-revision-1.png'), 'badge': 'Revision 1',
         'caption': 'Fit 1.000, 1.000, 1.000 · 1.0 × 0.8 × 0.7 m · 60 triangles · 0.066 m floor gap accepted.'}],
        'Claude Code’s look tool, six views each (front, right, back, top, three-quarter, low), shown enlarged from 1031×686',
        top_h=1250),
        {'card': 'media/B06.png', 'images': ['evidence/look/rock-first-build.png', 'evidence/look/rock-revision-1.png']})

    # B07 — the hand edit.
    he = shot(A3 / 'evidence' / 'hand-edit-crystal-short-b-rotz20.png')
    still('B07', cards.shot_with_insets('The hand edit: one cone, rotation Z = 20°', 'The author’s own Blender session',
        he, MINE, 'Crystal_Short_B selected; rotation Z typed into the sidebar, then Enter.',
        [((0, 0, 215, 24), 'Title bar · * = an unsaved change', True),
         ((1740, 498, 1995, 572), 'Sidebar · rotation X, Y, Z', True)],
        'evidence/hand-edit-crystal-short-b-rotz20.png in assignment-3 · the fourth attempt; three earlier ones never reached the scene'),
        {'card': 'media/B07.png', 'image': 'assignment-3/evidence/hand-edit-crystal-short-b-rotz20.png'})

    # B08 -> B09
    pyview('B08', 'Crystal: lengthen the cone, keep the rotation', 'tools/blender/build_crystal.py', 472, 478,
           'tip_i = max(range(len(me.vertices))', {475, 476, 477}, 'Call J1 (Crystal_Short_B)')
    still('B09', cards.image_facts('The crystal', LOOK, shot(EV / 'look' / 'crystal.png'), 'Joined crystal', [
        ('Before J1, after the hand edit', '0.3228 × 0.35 × 0.60 m'),
        ('J1', 'Short_B ×1.2125 along its own axis; rotation 9.04°, −31.32°, 20.00° kept'),
        ('After', '0.350 × 0.350 × 0.600 m · fit 1.000 · 30 triangles'),
        ('Material', '#3558C8 with emission 0.5')],
        'Claude Code’s look tool, six views, shown enlarged from 1031×686 · numbers from build_crystal.py calls 12 and J1–J2'),
        {'card': 'media/B09.png', 'image': 'evidence/look/crystal.png'})

    # B10 -> B11
    pyview('B10', 'The chest lid: a flat face up', 'tools/blender/build_chest.py', 107, 113,
           '# Bake: axis along X', {108, 111, 112, 113},
           'Call 4 (Chest_Lid) · line 134: print("true top z:", round(max(wz), 4), "| reaches", TOTAL_HEIGHT, …)')
    still('B11', cards.image_facts('The chest', LOOK, shot(EV / 'look' / 'chest-gold-metallic-1.0.png'), 'Joined chest', [
        ('Lid', 'true top 0.600 m · top face flat (normal 0, 0, 1)'),
        ('Split', 'body 0.376 + lid 0.224 m (brief: 0.35 + 0.25; total unchanged)'),
        ('Size', '0.8 × 0.5 × 0.6 m · fit 1.000 · 76 triangles'),
        ('Shown here', 'gold at metallic 1.0 — lowered to 0.3 after this render')],
        'Claude Code’s look tool, six views, shown enlarged from 1031×686 · numbers from build_chest.py calls 4 and 8'),
        {'card': 'media/B11.png', 'image': 'evidence/look/chest-gold-metallic-1.0.png'})

    # B12 -> B13
    pyview('B12', 'Export: Blender’s own glTF exporter', 'tools/blender/build_chest.py', 377, 390,
           'settings = dict(', {378, 379, 381, 382}, 'Call E1 (chest.glb); the rock and crystal exports use the same settings')
    log = (EV / 'glb-read-8d8895c.log').read_text(encoding='utf-8').splitlines()
    body = [l for l in log if not l.startswith(('$', '#', 'exit'))]
    hi = {i for i, l in enumerate(body) if 'node ' in l or 'bounds' in l or 'max Z' in l}
    still('B13', cards.terminal('Read back outside Blender', 'Recorded command output · reference copy of 8d8895c',
                                'python -I scripts/read_glb.py <reference copy>/assets/models', body, hi,
                                'Y is up in glTF: the brief’s height is the Y range. The chest’s gold lock reaches +Z 0.25; '
                                'the wood stops at 0.21, so its front faces +Z.',
                                'Full log: evidence/glb-read-8d8895c.log', size=36),
          {'card': 'media/B13.png', 'log': 'evidence/glb-read-8d8895c.log'})

    # B14 — the author's look in Godot, before the scene fixes.
    still('B14', cards.main_and_side('The author’s look in Godot, before the fixes', 'The author’s own screenshots of res://showcase3d/prop_room.tscn',
        {'img': shot(A3 / 'evidence' / 'prop-room-f6-before-fixes.png'), 'badge': MINE,
         'caption': 'F6 from the game camera: grey default background, floor edges in view; the gold reads yellow-gold.'}, [
        {'img': shot(A3 / 'evidence' / 'prop-room-editor-above-before-fixes.png'), 'badge': MINE,
         'caption': 'Editor, from above: the mage seen from the side is a thin line.'},
        {'img': shot(A3 / 'evidence' / 'prop-room-editor-below-before-fixes.png'), 'badge': MINE,
         'caption': 'Editor, from below through the floor: closed undersides.'}],
        'evidence/prop-room-*-before-fixes.png in assignment-3 · taken before the background, floor and billboard fixes'),
        {'card': 'media/B14.png', 'images': ['assignment-3/evidence/prop-room-f6-before-fixes.png',
                                              'assignment-3/evidence/prop-room-editor-above-before-fixes.png',
                                              'assignment-3/evidence/prop-room-editor-below-before-fixes.png']})

    # B15 -> B16
    workbench('B15', 'The scene fixes', 'showcase3d/prop_room.tscn', 37, 44, '[node name="Mage"', [
        ('Lines 16–18 · Environment_cave', 'background_mode = 1\nbackground_color = Color(0.0588235, 0.0666667, 0.0980392, 1)'),
        ('Pixel size', '64 visible rows × 0.0226563 m = 1.45 m')],
        [(0.0, 37, 'The mage: a Sprite3D'), ('billboard mode', 40, 'billboard = 2: turns to face the camera'),
         ('Her pixel size', 39, 'pixel_size: 64 px → 1.45 m')], font=34)
    lab, boxes = cards.labels([(DISCLOSE, 'tl', 'disclosure')])
    lab.save(WORK / 'label-B16.png')
    held, _ = cards.labels([('Held frame', 'tc2', 'event')])
    held.save(WORK / 'label-B16-held.png')
    PROV['B16'] = footage_with_hold('run-01', MEDIA / 'B16.mp4', nframes('B16'), WORK / 'label-B16.png',
                                    WORK / 'label-B16-held.png')
    regions = [{'label': 'Disclosure label', 'box': [round((b[0] + 30) / W, 4), round((b[1] + 14) / H, 4),
                                                     round((b[2] - 30) / W, 4), round((b[3] - 14) / H, 4)]} for b in boxes]
    BEATS['B16']['qc'] = {'full_bleed': True, 'full_bleed_reason': 'Native 4K Godot capture fills the frame; not a slide.',
                          'contrast_reason': 'Dark scene: the disclosure label is the stable text.',
                          'contrast_regions': regions}

    # B17 -> B18
    workbench('B17', 'The headless check', 'tests/test_a3_assets.gd', 78, 90, 'func check_asset', [
        ('Brief values (lines 9–16)', 'copied by hand from CHANGE-BRIEF.md: rock 1.0 × 0.7 × 0.8 · crystal 0.35 × 0.6 × 0.35 · '
                                      'chest 0.8 × 0.6 × 0.5 (X × Y × Z), TOL = 0.02'),
        ('Exit code', 'quit(1) on any failure')],
        [(0.0, 81, 'True vertex bounds in world space'), ('compares them', 84, 'Within ±0.02 m of the brief'),
         ('within two centimetres', 89, 'Upright: height on Y, lowest point at 0')], font=26)
    log = (EV / 'test_a3_assets-8d8895c.log').read_text(encoding='utf-8').splitlines()
    shown, hi = [], set()
    for line in log:
        if line.startswith('{"id"'):
            r = json.loads(line)
            if r['id'].endswith(('.size', '.upright')) or r['id'].startswith('scene.'):
                if r['id'].endswith('.size') or r['id'] == 'scene.one_light':
                    hi.add(len(shown))
                o = r['observed']
                keep = {k: o[k] for k in ('size_xyz', 'brief_xyz', 'height_axis', 'lowest_y', 'lights', 'visible_height', 'feet_y') if k in o}
                shown.append(f'{r["id"]:<24} {r["status"]}  {json.dumps(keep)}')
            else:
                shown.append(f'{r["id"]:<24} {r["status"]}')
        elif line.startswith('A3 ASSET CHECK') or line.startswith('exit:'):
            hi.add(len(shown))
            shown.append(line)
    still('B18', cards.terminal('Twenty-two checks, zero failures', 'Headless check output — not a render · reference copy of 8d8895c',
                                'Godot_v4.7.2-stable_win64_console.exe --headless --path . --script res://tests/test_a3_assets.gd',
                                shown, hi,
                                'It can fail: with the rock’s width set to 1.1 in a scratch copy it reported rock.size FAIL, '
                                '1 failure, exit 1. It cannot judge looks, light or glow.',
                                'Exact results, details shortened to the measured values; full log: evidence/test_a3_assets-8d8895c.log',
                                size=34),
          {'card': 'media/B18.png', 'log': 'evidence/test_a3_assets-8d8895c.log'})

    # B19 — what Claude got wrong, and the known limitations.
    still('B19', cards.columns('What Claude got wrong', 'From TEST-REPORT.md and FRICTIONAL.md', [
        ('Caught and corrected', [
            ('The first rock', 'Sized from get_scene_info’s box, which overstates rotated parts: stretched 1.19 wide.'),
            ('The hand edit', 'Blamed a different Blender; the screenshot showed the same one. The rotation was probably cancelled.'),
            ('FRICTIONAL.md', 'Said the file did not exist; it had been created in bac0f4c.'),
            ('Smaller', 'The first test run failed to load (a GDScript typing error); a script header numbered calls wrong.')]),
        ('Known limitations', [
            ('Rock', 'A 0.066 m gap at the floor between its two base stones.'),
            ('Chest', 'The lid is an 8-sided prism with a flat top, not a true curve.'),
            ('Build scripts', 'Recorded in run order; not re-run on their own to rebuild the assets.'),
            ('Glow', 'The crystal’s emission is #243E92 at energy 1.0; how it reads in real cave light is unknown.')])],
        'TEST-REPORT.md → What Claude got wrong · Known limitations (commit 8d8895c)'),
        {'card': 'media/B19.png'})


def main():
    global BEATS, PROV
    MEDIA.mkdir(exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    sheet = load_json(REEL / 'beat_sheet.json')
    BEATS = {b['beat_id']: b for b in sheet['beats']}
    PROV = {}
    build()
    BEATS['B16']['shot']['evidence_media'] = 'media/B16.mp4'
    BEATS['B18']['shot']['evidence_media'] = 'media/B18.png'
    for bid in ('B06', 'B09', 'B11', 'B13'):
        BEATS[bid]['shot']['evidence_media'] = f'media/{bid}.png'
    save_json(REEL / 'beat_sheet.json', sheet)
    save_json(EV / 'media-provenance.json', {
        'note': 'How each non-Remotion slot was made. B16 times are take seconds; frames are 60 fps source frames.',
        'look_renders': {p.name: sha256(p) for p in sorted((EV / 'look').glob('*.png'))},
        'beats': PROV})
    print('media built:', ', '.join(sorted(PROV)))


if __name__ == '__main__':
    main()
