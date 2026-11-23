"""Phase 1: write beat_sheet.json from the plan below (narration and visual plan), then, after Kokoro, pad the beats
whose picture needs more time than their words.

    python sheet.py            # (re)write beat_sheet.json from PLAN, keeping measured durations already in it
    python sheet.py --pad      # after generate_audio_kokoro.py: add each beat's lead/tail silence to its mp3

Written by Claude Code for the Assignment 8 pitch film. The narration is the author's PROJECT-BRIEF.md put into spoken
sentences, in the author's first person (Liam's voice speaks as Zhefan Zhang). Every number in it is in
PROJECT-BRIEF.md or in a committed log; FACTCHECK.md maps each one to its source.

Labels: each beat names what its picture is -- real (captured play of the game), generated (the Gemini concept art),
constructed (drawn for this film), or figure (drawn from committed logs).
"""
import sys

from common import REEL, SLUG, TITLE, AUTHOR, FPS, W, H, REV_A7, load_json, save_json, run

# id, heading, kind, label, narration, (lead_s, tail_s) silence added around the measured voice
PLAN = [
    ('B00', 'Hook: a growl and an early hit', 'capture', 'real',
     "A wolf growls before it lunges. Hit it during the growl, and the lunge is cancelled. "
     "This is my game as it runs today, played by scripted input.", (0.3, 1.6)),
    ('B01', 'What it is', 'still', 'constructed',
     "I'm Zhefan Zhang. My final project is The Little Flame Witch, an HD-2D cave adventure shooter: "
     "a little witch fights through one cave with fireballs and defeats a great wolf. "
     "It will be a playable Windows build of one vertical slice, title screen to end screen.", (0.4, 0.6)),
    ('B02', 'Why anyone would care', 'still', 'constructed',
     "Why care? It will put Octopath Traveler's HD-2D look together with Metal Slug-style side-scrolling, "
     "with a mouse-aimed fireball. Octopath is turn-based, Metal Slug fires in fixed directions, "
     "Hollow Knight is a large cave with progression; I've played all three. This will be a short action run.", (0.3, 0.6)),
    ('B03', 'The look', 'still', 'constructed',
     "The look will come from Godot's own renderer: tilt-shift depth of field, bloom, a cold blue cave where only "
     "fire is warm, light shafts through fog, and the fireball as a moving light, each one visual only, "
     "with my behaviour pin still passing.", (0.3, 0.6)),
    ('B04', 'Story moment: the opening', 'still', 'constructed',
     "Four short, skippable story moments will use portraits. The opening: "
     "The fire in my staff is the only warm thing down here. Let's see where this cave goes.", (0.3, 0.6)),
    ('B05', 'Story moment: before the boss', 'still', 'constructed',
     "Before the boss, the great wolf: Turn back, little flame. This cave is mine. "
     "And the witch: Then I'll light my own way.", (0.3, 0.8)),
    ('B06', 'Story moment: after the boss', 'still', 'constructed',
     "After the fight: Your fire burns brighter than I thought. Go on. We did it! "
     "A campfire line will follow the first fight, and a sad portrait will mark a defeat.", (0.3, 0.8)),
    ('B07', 'Who opens it: the first sixty seconds', 'still', 'constructed',
     "Who opens it? A hiring manager or a lead gameplay programmer; my target role is gameplay programmer. "
     "In the first sixty seconds they'll unzip it, double-click the exe, see the controls on the title screen, "
     "skip the opening line with one key, and be playing within a minute.", (0.3, 0.6)),
    ('B08', 'What it proves: the lunge and its cancel', 'capture', 'real',
     "It will prove I can build and verify gameplay systems. This much already ran in Assignment 7: "
     "the wolf's lunge, and a fireball during the growl cancelling it.", (0.3, 2.0)),
    ('B09', 'What it proves: the pin and the tests', 'still', 'figure',
     "I pinned the behaviour every physics tick before that change; only the two scenarios with a hit during the "
     "growl changed. Thirty-eight headless test runs passed in a fresh clone. "
     "The slice's frame time will be measured on an RTX 5060 Laptop GPU.", (0.3, 0.6)),
    ('B10', 'In, out, first', 'still', 'constructed',
     "In: one cave level from title to end screen, with a heal spell, the great-wolf boss, spikes, a boulder, "
     "a chest, a campfire, the story moments and a Windows build. "
     "Out: multiplayer. First: the core loop in one 3D cave room. It ran if my existing behaviour pin passes there "
     "and a windowed capture shows it, labelled with its revision.", (0.3, 0.6)),
    ('B11', 'The risk, and the pin as its test', 'still', 'constructed',
     "The risk: moving the 2D game into 3D could break movement, collision and state machines that work today. "
     "A 2D gameplay layer in front of a 3D cave, or 3D bodies held to a plane? A one-room spike will decide, "
     "judged by my Assignment 7 pin. If it fails, the 2D layer stays and the 3D is backdrop.", (0.3, 0.6)),
    ('B12', 'Why this project: what is new', 'still', 'constructed',
     "Why this project? Half learning, half showing. New to me: HD-2D itself, a lit 3D cave, its camera, "
     "and 2D sprites placed in it.", (0.3, 0.6)),
    ('B13', 'Already have: the hurt tint (Assignment 5)', 'capture', 'real',
     "Already mine: the hurt-tint shader from Assignment 5,", (0.2, 0.0)),
    ('B14', 'Already have: the particles (Assignment 6)', 'capture', 'real',
     "the fireball particles from Assignment 6, measured at about 0.02 and 0.10 milliseconds of GPU time "
     "on an RTX 5060 Laptop GPU,", (0.1, 0.0)),
    ('B15', 'Already have: the run cycle (Assignment 7)', 'capture', 'real',
     "and the run cycle, state machines and tests from Assignment 7.", (0.1, 0.0)),
    ('B16', 'Exists today, and what will exist', 'still', 'mixed',
     "Today: the 2D game, its animation, shaders, particles and tests, the Assignment 3 props, and concept "
     "portraits not yet in the game. Everything else will exist: the 3D cave and its look, the story in the game, "
     "the heal spell, the boss, hazards, the rest point, title and end screens, the Windows build and its "
     "test report.", (0.3, 1.2)),
    ('B17', 'Outro', 'still', 'constructed', '', (0.0, 0.0)),
]
OUTRO_S = 4.0
# The footage beats need at least this much time on screen; the shortfall becomes held-frame time, never retiming.
MIN_S = {'B13': 6.0, 'B14': 7.0, 'B15': 5.0}


# The voice reads narration_text; these spoken forms keep Kokoro from guessing at tokens (the toolkit's normaliser only
# maps symbols). PLAN keeps the written script, which FACTCHECK.md quotes and the screen shows.
SAY = [('HD-2D', 'H-D two-D'), ('2D', 'two-D'), ('3D', 'three-D'), ('RTX 5060', 'R-T-X fifty-sixty'),
       ('0.02 and 0.10 milliseconds', 'zero point zero two and zero point one zero milliseconds'),
       ('the exe', 'the E-X-E')]


def spoken(text):
    for a, b in SAY:
        text = text.replace(a, b)
    return text


def plan():
    return {p[0]: p for p in PLAN}


def write():
    path = REEL / 'beat_sheet.json'
    old = {b['beat_id']: b for b in load_json(path)['beats']} if path.exists() else {}
    beats = []
    for bid, heading, kind, label, text, (lead, tail) in PLAN:
        b = {'beat_id': bid, 'heading': heading, 'narration_text': spoken(text), 'script_text': text,
             'engine': 'kokoro', 'voice': 'am_onyx', 'label': label, 'pad_s': [lead, tail],
             'shot': {'type': 'VIDEO' if kind == 'capture' else 'STILL', 'source': 'capture' if kind == 'capture' else 'own',
                      'classification': 'SHOW', 'visual_intent': heading,
                      'show': [{'at': 'beat', 'event': heading}],
                      'motion': 'video' if kind == 'capture' else 'hold'},
             'visual_kind': kind}
        if bid == 'B01':
            # The title card is an edge-to-edge plate: a real captured frame of the cave, darkened, under the title.
            # Its text is checked in its own region instead of against the whole frame's average (final_frame_check).
            b['qc'] = {'full_bleed': True,
                       'contrast_regions': [{'label': 'title and subtitle', 'box': [0.05, 0.27, 0.58, 0.58]}],
                       'contrast_reason': 'Title text over a darkened real capture of the cave; the plate is '
                                          'full-bleed by design, so contrast is measured on the title block.'}
        if bid == 'B17':
            b.update({'act': 'outro', 'audio_policy': 'silence', 'estimated_duration_s': OUTRO_S,
                      'actual_duration_s': OUTRO_S})
        else:
            b['audio_file'] = f'mp3/beat-{bid}.mp3'
            prev = old.get(bid, {})
            if prev.get('narration_text') == spoken(text) and prev.get('actual_duration_s'):
                b['actual_duration_s'] = prev['actual_duration_s']
                for k in ('voice_s', 'padded'):
                    if k in prev:
                        b[k] = prev[k]
        beats.append(b)
    sheet = {'metadata': {
        'slug': SLUG, 'title': TITLE, 'author': AUTHOR, 'persona': 'Liam (Kokoro am_onyx) speaking as the author',
        'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx', 'fps': FPS, 'width': W, 'height': H,
        'aspect_ratio': '16:9', 'fit': 'crop', 'caption_policy': 'No captions (not requested); no burned captions',
        'skill': 'godot-waikthrough', 'modifier': 'walker (capture contract only; see BUILD-PROMPT.md)',
        'game_revision': REV_A7,
        'capture_source': 'capture/run-01.mp4: the real main scene at 840b501, played by capture/driver.gd (scripted '
                          'input), Movie Maker, windowed, 640x360 at 60 fps, archived x6 nearest neighbour; '
                          'capture/a5-run-01.mp4: the Assignment 5 game at 2b68e0a, the same way; the Assignment 6 '
                          "film's capture run-01.mp4 at 3c37fe0, reused unchanged (SHA-256 checked)",
        'authorization': 'Author requested the CSYE 7270 Assignment 8 pitch film (pitch/prompt-1-pitch.txt). Local 4K '
                         'master for the author to review; no upload or publication; records committed, media kept '
                         'out of git.',
        'human_review_approved': False}, 'beats': beats}
    save_json(path, sheet)
    print('beat_sheet.json:', len(beats), 'beats')


def pad():
    """Add each beat's lead/tail silence (and any held-frame room a footage beat needs) to its measured mp3."""
    path = REEL / 'beat_sheet.json'
    sheet = load_json(path)
    for b in sheet['beats']:
        if b.get('audio_policy') == 'silence' or b.get('padded'):
            continue
        mp3 = REEL / b['audio_file']
        voice = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp3])
                      .stdout.decode().strip())
        lead, tail = b['pad_s']
        want = max(voice + lead + tail, MIN_S.get(b['beat_id'], 0.0))
        tail = want - voice - lead
        tmp = mp3.with_suffix('.tmp.mp3')
        run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-af', f'adelay={int(lead * 1000)}:all=1,apad=pad_dur={tail:.3f}',
             '-ar', '24000', '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '192k', tmp])
        tmp.replace(mp3)
        dur = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp3])
                    .stdout.decode().strip())
        b['voice_s'] = round(voice, 3)
        b['actual_duration_s'] = round(dur, 2)
        b['padded'] = [lead, round(tail, 3)]
        print(f"{b['beat_id']}: voice {voice:.2f}s -> {dur:.2f}s (lead {lead}, tail {tail:.2f})")
    save_json(path, sheet)


if __name__ == '__main__':
    pad() if '--pad' in sys.argv else write()
