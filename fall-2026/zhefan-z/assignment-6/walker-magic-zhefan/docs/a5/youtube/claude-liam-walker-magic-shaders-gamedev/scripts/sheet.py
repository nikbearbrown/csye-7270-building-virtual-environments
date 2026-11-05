"""Phase 1: write beat_sheet.json from SCRIPT.md.

Adapted from the Assignment 3 film's sheet.py. Narration is taken verbatim from SCRIPT.md (plus the
Your Turn sign-off the skill requires, SIGN_OFF). Measured narration already in the sheet is kept
when the text is unchanged, so re-running this never silently invalidates generated audio.
"""
from common import REEL, SLUG, TITLE, BUILD, load_json, save_json, script_narration

SIGN_OFF = ' Liam, in for Bear.'   # godot-gamedev SKILL.md: "Liam signs off in Your Turn."

COMPOSER = {'topic': 'CSYE 7270 · reconstructed prompt, not a saved chat', 'greeting': 'Hello, Liam',
            'runningText': '', 'folderLabel': 'walker-magic', 'modelLabel': 'Claude Code',
            'effortLabel': '', 'placeholder': ''}

# id, heading, visual kind, extra
BEATS = [
    ('B00', 'Walker opening', 'remotion', {'pattern': 'ClaudeComposerAsk', 'props': {
        **COMPOSER,
        'command': 'Please use Walker to convert my game design document\nabout a fire mage in a cold cave into two shaders:\n'
                   'a red hurt tint while she is invulnerable after a hit,\nand a frosted rock whose textures decide where the\n'
                   'frost goes — each predicted first, then tested\nheadlessly and captured in the engine.',
        'output': ['hurt_tint.gdshader · canvas_item · driven by Player.invulnerable',
                   'rock_frost.gdshader · spatial · two materials, one shader',
                   'test_hurt_tint.gd · 17 checks / 0 failures at 30, 60 and 144 fps',
                   'test_materials.gd · 32 checks / 0 failures'],
        'segment': TITLE}}),
    ('B01', 'What got built', 'remotion', {'pattern': 'BrutalistHesitantWriter', 'props': {
        'text': 'One shader turns\nthe mage red;\none frosts a rock.\nTextures are\npictures.',
        'triggerWords': 'pictures', 'replacementWords': 'information',
        'fontSize': 172, 'lineSpacing': 1.1, 'mistakeRate': 0, 'hesitateWithin': 0, 'hesitateBetween': 0, 'charMs': 50, 'jitter': 0,
        'seed': SLUG, 'face': 'serif', 'align': 'center'}, 'lead_silence_s': 0.8}),
    ('B02', 'The game, the state, the object', 'still', {}),
    ('B03', 'The colour line, specified first', 'still', {}),
    ('B04', 'The shader (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B05', 'Controlled values (result)', 'still', {}),
    ('B06', 'The driver (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B07', 'The driver in the game loop (result)', 'still', {}),
    ('B08', 'A value from code, past the slider', 'still', {}),
    ('B09', 'Two materials, one shader (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B10', 'The two rocks (result)', 'still', {}),
    ('B11', 'Change a material, then the shader', 'still', {}),
    ('B12', 'The hint experiment (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B13', 'Same bytes, two meanings (result)', 'still', {}),
    ('B14', 'Three samplers (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B15', 'Data, checked as data (result)', 'still', {}),
    ('B16', 'Where the frost goes (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B17', 'Frost amount, swept (result)', 'still', {}),
    ('B18', 'The interface (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B19', 'The interface, swept (result)', 'still', {}),
    ('B20', 'The language (code)', 'remotion', {'pattern': 'GodotDevWorkbench'}),
    ('B21', 'Two pipelines (result)', 'still', {}),
    ('B22', 'The shader Godot writes', 'still', {}),
    ('B23', 'What the tests proved', 'still', {}),
    ('B24', 'Broken on purpose, and the limit', 'still', {}),
    ('B25', 'What the agent got wrong', 'still', {}),
    ('B26', 'Still uncertain, and one next step', 'still', {}),
    ('B27', 'Who did what', 'still', {}),
    ('B28', 'Verdict', 'remotion', {'pattern': 'ClaudeVerdictArtifact', 'props': {
        'artifactTitle': 'Verdict', 'artifactHeading': 'Built · measured · judged · unknown'}}),   # lines: media.py
    ('B29', 'Your Turn', 'remotion', {'pattern': 'ClaudeComposerAsk', 'props': {
        **COMPOSER, 'topic': 'CSYE 7270 · suggested prompt, not a saved chat', 'greeting': 'Your turn.',
        'runningText': 'paste this into Claude…', 'output': [],
        'command': 'Please use Walker to turn the ice roughness in my frosted\nrock shader into a uniform with a range, set in both\n'
                   'materials. Before changing anything, predict which of my\ncaptures will change and which will not, then add a\n'
                   'check to my material test that fails if either material\nleaves it unset.',
        'segment': 'Your Turn'}}),
    ('B30', 'Regular outro', 'outro', {'pattern': 'ClaudeTitleOutro', 'props': {'title': TITLE, 'slug': SLUG}}),
]

SHOT_TYPE = {'remotion': 'REMOTION', 'outro': 'REMOTION', 'still': 'STILL'}


def main():
    spoken = script_narration()
    old = {}
    path = REEL / 'beat_sheet.json'
    if path.exists():
        old = {b['beat_id']: b for b in load_json(path)['beats']}
    beats = []
    for bid, heading, kind, extra in BEATS:
        text = spoken[bid] + (SIGN_OFF if bid == 'B29' else '')
        if kind == 'outro':
            assert text == '', f'{bid} must be unnarrated'
        else:
            assert text, f'{bid} has no narration in SCRIPT.md'
        shot = {'type': SHOT_TYPE[kind], 'source': 'own', 'classification': 'SHOW',
                'visual_intent': heading, 'show': [{'at': 'beat', 'event': heading}]}
        if kind in ('remotion', 'outro'):
            shot['remotion'] = {'pattern': extra['pattern'], 'props': dict(extra.get('props', {}))}
        if kind == 'still':
            shot['motion'] = 'hold'
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
        'capture_source': f'captures/ at {BUILD}: in-engine PNG captures from the F9-F12 capture scenes '
                          '(tests/capture/, f4123db), 640x360 viewport, scripted values; no new capture for this film',
        'human_review_approved': False,
        'authorization': 'Author requested the CSYE 7270 Assignment 5 film (prompt-6-film.txt). Local 4K master for the '
                         'author to review; no upload, publication or commit.'},
        'beats': beats}
    save_json(path, sheet)
    print(f'wrote {path.name}: {len(beats)} beats; narrated {sum(1 for b in beats if b["narration_text"])}')


if __name__ == '__main__':
    main()
