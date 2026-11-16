"""Phase 1: write beat_sheet.json from SCRIPT.md.

Adapted from the Assignment 5 film's sheet.py. Narration is taken verbatim from SCRIPT.md (the Your Turn beat
already ends with Liam's sign-off). Measured narration already in the sheet is kept when the text is unchanged,
so re-running this never silently invalidates generated audio.
"""
from common import REEL, SLUG, TITLE, BUILD, load_json, save_json, script_narration

COMPOSER = {'topic': 'CSYE 7270 · reconstructed prompt, not a saved chat', 'greeting': 'Merhaba, Liam',
            'runningText': '', 'folderLabel': 'walker-magic', 'modelLabel': 'Claude Code',
            'effortLabel': '', 'placeholder': ''}

WB = {'pattern': 'GodotDevWorkbench'}
# id, heading, visual kind, extra
BEATS = [
    ('B00', 'Walker opening', 'remotion', {'pattern': 'ClaudeComposerAsk', 'props': {
        **COMPOSER,
        'command': 'Please use Walker to convert my game design document\nabout a fire mage\'s fireball into two particle effects:\n'
                   'an impact burst of sparks and smoke wherever it lands,\nand a flame trail while it flies — each specified\n'
                   'first, tested headlessly, tuned from frame strips\nand priced on the GPU.',
        'output': ['effects/fireball_impact.tscn · Sparks + Smoke · on Fireball.explode()',
                   'effects/fireball_trail.tscn · turbulence · sphere emission · while the fireball exists',
                   'test_fireball_impact.gd · 14 checks / 0 failures at 30, 60 and 144 fps',
                   'test_fireball_trail.gd · 20 checks / 0 failures at 30, 60 and 144 fps'],
        'segment': TITLE}}),
    ('B01', 'What got built', 'remotion', {'pattern': 'BrutalistHesitantWriter', 'props': {
        'text': 'Two effects for\none fireball:\na burst, a trail.\nEach is a\npicture.',
        'triggerWords': 'picture', 'replacementWords': 'program',
        'fontSize': 180, 'lineSpacing': 1.02, 'mistakeRate': 0, 'hesitateWithin': 0, 'hesitateBetween': 0, 'charMs': 30,
        'jitter': 0, 'seed': SLUG, 'face': 'serif', 'align': 'center'}, 'lead_silence_s': 0.8}),
    ('B02', 'The game, the jobs, the event and the condition', 'still', {}),
    ('B03', 'Where both effects hook in (code)', 'remotion', WB),
    ('B04', 'One cast, in the running game (result)', 'capture', {}),
    ('B05', 'Emission, process, draw', 'still', {}),
    ('B06', 'Why the headless price is near zero', 'still', {}),
    ('B07', 'Effect A, the intent', 'still', {}),
    ('B08', "The sparks' process settings (code)", 'remotion', WB),
    ('B09', 'The first strip (result)', 'still', {}),
    ('B10', 'Tuning step r0b: the preview, not the effect', 'still', {}),
    ('B11', "Tuning step r1: the smoke's colour ramp (code)", 'remotion', WB),
    ('B12', 'r0 against r1, Effect A (result)', 'still', {}),
    ('B13', 'Effect A in play, with rapid repeats (result)', 'capture', {}),
    ('B14', "Effect B, the intent and the feature A doesn't use", 'still', {}),
    ('B15', "The trail's process settings (code)", 'remotion', WB),
    ('B16', "The trail's first strip (result)", 'still', {}),
    ('B17', 'Tuning step r1: the scale curve (code)', 'remotion', WB),
    ('B18', 'r0 against r1, Effect B (result)', 'still', {}),
    ('B19', 'Effect B in play: start, stop, pause (result)', 'capture', {}),
    ('B20', 'The process shader Godot writes', 'still', {}),
    ('B21', 'What the tests proved', 'still', {}),
    ('B22', 'Broken on purpose', 'still', {}),
    ('B23', 'The headless price, with its control', 'still', {}),
    ('B24', 'The GPU price, against the budget', 'still', {}),
    ('B25', 'What no headless run shows', 'still', {}),
    ('B26', 'What the agent got wrong', 'still', {}),
    ('B27', 'Overruled, uncertain, and one next step', 'still', {}),
    ('B28', 'Who did what', 'still', {}),
    ('B29', 'Verdict', 'remotion', {'pattern': 'ClaudeVerdictArtifact', 'props': {
        'artifactTitle': 'Verdict', 'artifactHeading': 'Built · measured · judged · unknown'}}),   # lines: media.py
    ('B30', 'Your Turn', 'remotion', {'pattern': 'ClaudeComposerAsk', 'props': {
        **COMPOSER, 'topic': 'CSYE 7270 · suggested prompt, not a saved chat', 'greeting': 'Your turn.',
        'runningText': 'paste this into Claude…', 'output': [],
        'command': 'Please use Walker to add a test to my fireball state test\nthat makes one fireball touch two bodies in the same\n'
                   'physics frame — a wall corner and the ground — and checks\nthat explode() spawns exactly one impact and detaches\n'
                   'exactly one trail. Predict first which of my rules fails\nif the _spent guard is removed, then remove it on a\n'
                   'copy and show the test fail.',
        'segment': 'Your Turn'}}),
    ('B31', 'Regular outro', 'outro', {'pattern': 'ClaudeTitleOutro', 'props': {'title': TITLE, 'slug': SLUG}}),
]

SHOT_TYPE = {'remotion': 'REMOTION', 'outro': 'REMOTION', 'still': 'STILL', 'capture': 'CAPTURE'}


def main():
    spoken = script_narration()
    old = {}
    path = REEL / 'beat_sheet.json'
    if path.exists():
        old = {b['beat_id']: b for b in load_json(path)['beats']}
    beats = []
    for bid, heading, kind, extra in BEATS:
        text = spoken[bid]
        if kind == 'outro':
            assert text == '', f'{bid} must be unnarrated'
        else:
            assert text, f'{bid} has no narration in SCRIPT.md'
        shot = {'type': SHOT_TYPE[kind], 'source': 'capture' if kind == 'capture' else 'own', 'classification': 'SHOW',
                'visual_intent': heading, 'show': [{'at': 'beat', 'event': heading}]}
        if kind in ('remotion', 'outro'):
            shot['remotion'] = {'pattern': extra['pattern'], 'props': dict(extra.get('props', {}))}
        if kind == 'still':
            shot['motion'] = 'hold'
        if kind == 'capture':
            shot['treatment'] = 'none'
        b = {'beat_id': bid, 'heading': heading, 'narration_text': text, 'engine': 'kokoro',
             'voice': 'am_onyx', 'shot': shot, 'visual_kind': kind}
        if 'lead_silence_s' in extra:
            b['lead_silence_s'] = extra['lead_silence_s']
        if kind == 'outro':
            b.update({'act': 'outro', 'audio_policy': 'silence', 'estimated_duration_s': 6.066667,
                      'actual_duration_s': 6.066667})
        prev = old.get(bid)
        if prev and prev.get('narration_text') == text and text:
            for k in ('audio_file', 'actual_duration_s', 'narration_audio'):
                if k in prev:
                    b[k] = prev[k]
        beats.append(b)
    sheet = {'metadata': {
        'slug': SLUG, 'title': TITLE, 'persona': 'Liam', 'brand': 'claude-liam', 'channel': '@NikBearBrown',
        'palette': 'claude', 'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx',
        'fps': 30, 'width': 3840, 'height': 2160, 'aspect_ratio': '16:9', 'fit': 'crop',
        'caption_policy': 'No captions (not requested); no burned captions',
        'skill': 'godot-gamedev', 'modifier': 'walker', 'game_revision': BUILD,
        'capture_source': f'capture/run-01.mp4: the real main scene at {BUILD}, played by capture/driver.gd (scripted '
                          'input through mouse and key events), Movie Maker, windowed, 640x360 at 30 fps, shown x5 '
                          'nearest neighbour; strips: captures/ (fixture captures from the preview scenes)',
        'human_review_approved': False,
        'authorization': 'Author requested the CSYE 7270 Assignment 6 film (prompt-9-film.txt). Local 4K master for the '
                         'author to review; no upload or publication; film records committed, media kept out of git.'},
        'beats': beats}
    save_json(path, sheet)
    print(f'wrote {path.name}: {len(beats)} beats; narrated {sum(1 for b in beats if b["narration_text"])}')


if __name__ == '__main__':
    main()
