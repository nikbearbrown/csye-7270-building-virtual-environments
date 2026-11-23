"""Phase 1: write beat_sheet.json from the plan below (narration and visual plan), then, after Kokoro, pad the beats
whose picture needs more time than their words.

    python sheet.py            # (re)write beat_sheet.json from PLAN, keeping measured durations already in it
    python sheet.py --pad      # after generate_audio_kokoro.py: add each beat's lead/tail silence to its mp3
                               # (G11's track is built by audio.py instead: narration, then the game's own sounds)

Written by Claude Code for the Assignment 8 pitch film; rebuilt 2026-11-22 for the updated assignment (prompt-2-gdd.txt):
the film follows the spec's order -- title card with the GDD's metadata, the game in brief, the GDD's sixteen beats,
the seven questions (only what the GDD beats have not already said), the appendix, the silent outro. The narration is
the author's GDD.md and PROJECT-BRIEF.md put into spoken sentences, in the author's first person (Liam's voice speaks
as Zhefan Zhang). Every number in it is in those two files or in a committed log; FACTCHECK.md maps each one.

Labels: each beat names what its picture is -- real (captured play or the game's own files, with the revision),
generated (the Gemini concept art), constructed (drawn for this film), or figure (drawn from committed logs).
"""
import sys

from common import REEL, SLUG, TITLE, AUTHOR, FPS, W, H, REV_A7, load_json, save_json, run

# id, part, heading, kind, label, narration, (lead_s, tail_s) silence added around the measured voice
#   kind: still (a held PNG), capture (gameplay video), audio (G11: a video timed to the game's own sounds)
PLAN = [
    # ---- title + the game in brief (about 15 s)
    ('T00', 'title', 'Title: The Little Flame Witch, GDD 2.0', 'still', 'constructed',
     "I'm Zhefan Zhang, and this pitch is built from my game design document, version 2.0.", (0.3, 0.5)),
    ('P01', 'brief', 'The game in brief', 'still', 'mixed',
     "The Little Flame Witch is an HD-2D cave action game: aim fireballs with the mouse, fight through a cold cave, "
     "and defeat the great wolf at the bottom.", (0.2, 0.4)),
    # ---- the GDD, sections 1-16 (about 1:50)
    ('G01', 'GDD 1', 'GDD 1 · Design pillars', 'still', 'constructed',
     "Four pillars: your fire is the only warmth, every failure is fair, readable even muted, small witch, big threat.",
     (0.2, 0.3)),
    ('G02', 'GDD 2', 'GDD 2 · Core gameplay loop', 'still', 'constructed',
     "The loop: move, jump, aim, fire and read each growl; the slice will chain short levels to the great wolf.",
     (0.2, 0.3)),
    ('G03', 'GDD 3', 'GDD 3 · Player experience goals', 'still', 'constructed',
     "She should feel small but capable when an early shot cancels a lunge, and relieved when the cave falls quiet.",
     (0.2, 0.3)),
    ('G04', 'GDD 4', 'GDD 4 · Core mechanics', 'capture', 'real',
     "Built today: run, jump with coyote time, aim and cast; a pit or zero HP shows the reason and restarts.",
     (0.2, 0.3)),
    ('G05', 'GDD 5', 'GDD 5 · Systems: the wolf and health', 'capture', 'real',
     "Each wolf runs a phase table, growl, lunge, recover, and a hit during the growl cancels the lunge.", (0.2, 0.3)),
    ('G06', 'GDD 6', 'GDD 6 · Progression', 'still', 'constructed',
     "No levelling: she'll gain one heal spell from the first chest, and each level will add harder threats.",
     (0.2, 0.3)),
    ('G07', 'GDD 7', 'GDD 7 · World and environment', 'still', 'constructed',
     "One cold cave in two to three short levels, where warmth comes only from fire.", (0.2, 0.3)),
    ('G08', 'GDD 8', 'GDD 8 · Narrative', 'still', 'constructed',
     "Four short, skippable scenes with portraits will tell a simple story, from the cave mouth to the great wolf.",
     (0.2, 0.3)),
    ('G09', 'GDD 9', 'GDD 9 · Characters', 'still', 'mixed',
     "The witch and the cave wolves exist as sprites; the great wolf exists only as concept art.", (0.2, 0.3)),
    ('G10', 'GDD 10', 'GDD 10 · Art direction', 'still', 'mixed',
     "On the left, the art that exists; on the right, the planned HD-2D look.", (0.2, 0.3)),
    ('G11', 'GDD 11', 'GDD 11 · Sound and music', 'audio', 'real',
     "Music and effects, from Assignment 2:", (0.2, 0.2)),
    ('G12', 'GDD 12', 'GDD 12 · Feature list', 'still', 'constructed',
     "Must, should and could; the smallest playable version is one 3D room, one wolf, and my pin passing.",
     (0.2, 0.3)),
    ('G13', 'GDD 13', 'GDD 13 · Out of scope', 'still', 'constructed',
     "Out of scope: multiplayer, saves, levelling and shops, and a web export.", (0.2, 0.3)),
    ('G14', 'GDD 14', 'GDD 14 · Technical requirements', 'still', 'constructed',
     "Godot 4.7.2, Forward+, a Windows build, aiming for 60 frames per second at 1080p, to be measured.", (0.2, 0.3)),
    ('G15', 'GDD 15', 'GDD 15 · Risks', 'still', 'constructed',
     "The main risk: 2D into 3D could break what works, so one room comes first, judged by my Assignment 7 pin.",
     (0.2, 0.3)),
    ('G16', 'GDD 16', 'GDD 16 · Open questions', 'still', 'constructed',
     "Open questions: a 2D layer or 3D bodies, two levels or three, and pixel sprites under depth of field.",
     (0.2, 0.3)),
    # ---- the seven questions (about 1:10); question 6 is GDD 15
    ('Q01', 'Question 1', 'Question 1 · What it is', 'still', 'constructed',
     "Question one: the artifact will be a Windows exe in a zip, a vertical slice from title to end screen.",
     (0.3, 0.3)),
    ('Q02', 'Question 2', 'Question 2 · Why anyone would care', 'still', 'constructed',
     "Why care? It will put Octopath Traveler's HD-2D look together with Metal Slug-style shooting and a mouse-aimed "
     "fireball; Octopath is turn-based, Metal Slug fires in fixed directions, Hollow Knight is a big cave with "
     "progression, and I've played all three.", (0.2, 0.3)),
    ('Q03', 'Question 3', 'Question 3 · Who opens it, and the first sixty seconds', 'still', 'constructed',
     "For a gameplay programmer role, the reader, a hiring manager or lead, will unzip, double-click, and be playing "
     "within a minute.", (0.2, 0.3)),
    ('Q04', 'Question 4', 'Question 4 · What it proves', 'still', 'figure',
     "It will prove I build and verify gameplay systems: I pinned the wolf before the growl cancel, and thirty-eight "
     "headless runs passed in a fresh clone.", (0.2, 0.3)),
    ('Q05', 'Question 5', 'Question 5 · What comes first, and how anyone would know it ran', 'still', 'constructed',
     "First comes one 3D cave room; it ran if my behaviour pin passes there and a labelled capture shows it.",
     (0.2, 0.3)),
    ('Q07', 'Question 7', 'Question 7 · Why this project: what is new', 'still', 'constructed',
     "Why this project? Half learning, half showing: new to me is a whole 3D level with sprites that run and fight in "
     "it.", (0.2, 0.3)),
    ('Q07X', 'Question 7', 'Question 7 · Already have, by revision', 'capture', 'real',
     "Already mine: the hurt tint, the particles, measured at about 0.02 and 0.10 milliseconds of GPU time on an RTX "
     "5060 Laptop GPU, and the run cycle.", (0.2, 0.3)),
    # ---- the appendix (about 30 s)
    ('A01', 'Appendix', 'Appendix · Exists today', 'capture', 'real',
     "Appendix. Today the 2D game exists, with its animation, effects and tests, my Assignment 3 props, and the "
     "concept portraits.", (0.3, 0.3)),
    ('A02', 'Appendix', 'Appendix · Started, not finished', 'still', 'constructed',
     "Started: this GDD and brief, and the portraits for the story scenes; nothing of the 3D cave yet.", (0.2, 0.3)),
    ('A03', 'Appendix', 'Appendix · Not started (will exist)', 'still', 'constructed',
     "Not started: the 3D levels, the look, the boss, hazards, rest point, screens and the Windows export.",
     (0.2, 0.3)),
    ('A04', 'Appendix', 'Appendix · Can one person finish it?', 'still', 'constructed',
     "One person can finish it at two levels; I'd cut the third level, then the extras, then the scenes.",
     (0.2, 0.3)),
    ('A05', 'Appendix', 'Appendix · Where every asset comes from', 'still', 'mixed',
     "Every asset is mine or generated, with its licence; nothing is bought.", (0.2, 0.3)),
    ('OUT', 'outro', 'Outro', 'still', 'constructed', '', (0.0, 0.0)),
]
OUTRO_S = 5.0
# Pictures that need more time than their words: the shortfall is silence (held frames or a held card), never retiming.
MIN_S = {'G04': 7.0, 'G05': 7.0, 'Q07X': 10.0, 'A01': 7.0, 'A05': 6.0}

# The voice reads narration_text; these spoken forms keep Kokoro from guessing at tokens (the toolkit's normaliser only
# maps symbols). PLAN keeps the written script, which FACTCHECK.md quotes and the screen shows.
SAY = [('HD-2D', 'H-D two-D'), ('2D', 'two-D'), ('3D', 'three-D'), ('RTX 5060', 'R-T-X fifty-sixty'),
       ('0.02 and 0.10 milliseconds', 'zero point zero two and zero point one zero milliseconds'),
       ('0.08-second', 'zero point zero eight second'), ('Godot 4.7.2', 'Godot four point seven point two'),
       ('1080p', 'ten-eighty p'), ('60 fps', 'sixty frames per second'), ('the exe', 'the E-X-E'),
       ('Windows exe', 'Windows E-X-E'),
       ('version 2.0', 'version two point oh'), ('GDD', 'G-D-D')]


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
    for bid, part, heading, kind, label, text, (lead, tail) in PLAN:
        b = {'beat_id': bid, 'part': part, 'heading': heading, 'narration_text': spoken(text), 'script_text': text,
             'engine': 'kokoro', 'voice': 'am_onyx', 'label': label, 'pad_s': [lead, tail],
             'shot': {'type': 'STILL' if kind == 'still' else 'VIDEO',
                      'source': 'capture' if kind in ('capture', 'audio') else 'own',
                      'classification': 'SHOW', 'visual_intent': heading,
                      'show': [{'at': 'beat', 'event': heading}],
                      'motion': 'hold' if kind == 'still' else 'video'},
             'visual_kind': kind}
        if bid == 'P01':
            b['qc'] = {'contrast_regions': [{'label': 'the game in brief text', 'box': [0.05, 0.75, 0.95, 0.93]}],
                       'contrast_reason': 'A real captured frame and a portrait fill most of the card; the brief '
                                          'text below them is checked in its own region.'}
        if bid == 'OUT':
            b.update({'act': 'outro', 'audio_policy': 'silence', 'estimated_duration_s': OUTRO_S,
                      'actual_duration_s': OUTRO_S})
        else:
            b['audio_file'] = f'mp3/beat-{bid}.mp3'
            prev = old.get(bid, {})
            if prev.get('narration_text') == spoken(text) and prev.get('actual_duration_s'):
                b['actual_duration_s'] = prev['actual_duration_s']
                for k in ('voice_s', 'padded', 'audio_mix'):
                    if k in prev:
                        b[k] = prev[k]
        beats.append(b)
    sheet = {'metadata': {
        'slug': SLUG, 'title': TITLE, 'author': AUTHOR, 'persona': 'Liam (Kokoro am_onyx) speaking as the author',
        'engine': 'kokoro', 'voice': 'am_onyx', 'voice_kokoro': 'am_onyx', 'fps': FPS, 'width': W, 'height': H,
        'aspect_ratio': '16:9', 'fit': 'crop', 'caption_policy': 'No captions (not requested); no burned captions',
        'skill': 'godot-waikthrough', 'modifier': 'walker (capture contract only; see BUILD-PROMPT.md)',
        'game_revision': REV_A7, 'gdd': 'GDD.md version 2.0, 2026-11-21',
        'structure': 'title (GDD metadata) · game in brief · GDD 1-16 · questions 1, 2, 3, 4, 5, 7 (6 is GDD 15) · '
                     'appendix · outro',
        'capture_source': 'capture/run-01.mp4 and capture/run-02.mp4: the real main scene at 840b501, played by '
                          'capture/driver.gd and capture/driver_fail.gd (scripted input), Movie Maker, windowed, '
                          '640x360 at 60 fps, archived x6 nearest neighbour; capture/a5-run-01.mp4: the Assignment 5 '
                          "game at 2b68e0a; the Assignment 6 film's capture run-01.mp4 at 3c37fe0, reused unchanged "
                          '(SHA-256 checked); one render of the Assignment 3 prop scene at 840b501; the Assignment 2 '
                          'music and sound files read at 840b501',
        'authorization': 'Author requested the CSYE 7270 Assignment 8 pitch film (pitch/prompt-1-pitch.txt) and its '
                         'rebuild from the GDD (pitch/prompt-2-gdd.txt). Local 4K master for the author to review; no '
                         'upload or publication; records committed, media kept out of git.',
        'human_review_approved': False}, 'beats': beats}
    save_json(path, sheet)
    print('beat_sheet.json:', len(beats), 'beats')


def pad():
    """Add each beat's lead/tail silence (and any held-frame room a footage beat needs) to its measured mp3."""
    path = REEL / 'beat_sheet.json'
    sheet = load_json(path)
    for b in sheet['beats']:
        if b.get('audio_policy') == 'silence' or b.get('padded') or b['visual_kind'] == 'audio':
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
