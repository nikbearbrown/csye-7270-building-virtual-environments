"""films.py - the twenty-five films of the playlist "Building Virtual Environments, Exam Prep".

One film per terminology deck in glossary/decks/. Films are never numbered for the viewer;
the two-digit key is the deck's file prefix and is used only for paths.

Adapted 2026-11-13 from info-7375-computational-skepticism-for-ai/youtube/exam-prep-deck-films/tools/films.py.
"""
from pathlib import Path

COURSE = Path(__file__).resolve().parents[3]
BOOKS = COURSE.parent
TOOLKIT = BOOKS / "brutalist.art"
HERE = COURSE / "youtube" / "exam-prep-deck-films"
PLAYLIST = "Building Virtual Environments, Exam Prep"
COURSE_NAME = "CSYE 7270 Building Virtual Environments"
COURSE_TAGS = ["Building Virtual Environments", "CSYE 7270", "Game development", "Godot"]

CH = "chapters/"
NOTES = "glossary/notes/"
GLOSS = "midterm/jargon-midterm/GLOSSARY-jargon-midterm.md"

# nn: (deck file, topic as spoken and shown, card title lines, reference files (first = main), cited on the exam cheat sheet?)
# "On the exam cheat sheet" = glossary/EXAM-CHEAT-SHEET.md links at least one slide of the deck (checked 2026-11-13).
_F = {
    "01": ("01 Game design A.html", "What a Game Is", ["Key Terms:", "What a Game Is"],
           [NOTES + "GAME-DESIGN-TERMS-source-crashcourse.md", NOTES + "RIOT-SERIES-TERMS.md", CH + "05-the-gdd-and-virtual-worlds.md", GLOSS], True),
    "02": ("02 Game design B.html", "Choices and Challenge", ["Key Terms:", "Choices and", "Challenge"],
           [NOTES + "GAME-DESIGN-TERMS-source-crashcourse.md", NOTES + "RIOT-SERIES-TERMS.md"], False),
    "03": ("03 Game design C.html", "Pacing and Guidance", ["Key Terms:", "Pacing and", "Guidance"],
           [NOTES + "GAME-DESIGN-TERMS-source-crashcourse.md", NOTES + "RIOT-SERIES-TERMS.md", GLOSS], True),
    "04": ("04 Walker and the toolchain.html", "Walker and the Toolchain", ["Key Terms:", "Walker and", "the Toolchain"],
           [CH + "00-the-toolchain.md", CH + "01-walker-and-godot.md", GLOSS], True),
    "05": ("05 Godot editor and scenes.html", "The Godot Editor and Scenes", ["Key Terms:", "The Godot Editor", "and Scenes"],
           [CH + "01-walker-and-godot.md", CH + "04-scenes-collision-and-physics.md", CH + "15-final-projects-brief-to-export.md", GLOSS], True),
    "06": ("06 2D art and sound assets.html", "2D Art and Sound Assets", ["Key Terms:", "2D Art and", "Sound Assets"],
           [CH + "02-prompting-game-art.md", CH + "12-audio-and-triggers.md", NOTES + "RIOT-SERIES-TERMS.md", GLOSS], True),
    "07": ("07 Art principles and concept art.html", "Concept Art and Character Art", ["Key Terms:", "Concept Art and", "Character Art"],
           [NOTES + "RIOT-SERIES-TERMS.md", CH + "02-prompting-game-art.md", GLOSS], True),
    "08": ("08 Blender interface and modeling.html", "The Blender Interface and Modeling", ["Key Terms:", "The Blender Interface", "and Modeling"],
           [CH + "03-blender-mcp-to-godot.md", GLOSS], True),
    "09": ("09 Blender to Godot.html", "Blender to Godot", ["Key Terms:", "Blender to Godot"],
           [CH + "03-blender-mcp-to-godot.md", NOTES + "RIOT-SERIES-TERMS.md", GLOSS], True),
    "10": ("10 Game design document.html", "The Game Design Document", ["Key Terms:", "The Game Design", "Document"],
           [CH + "05-the-gdd-and-virtual-worlds.md", GLOSS], True),
    "11": ("11 Shader foundations.html", "Shader Foundations", ["Key Terms:", "Shader Foundations"],
           [CH + "06-shader-foundations.md", GLOSS], True),
    "12": ("12 Materials and textures.html", "Materials and Textures", ["Key Terms:", "Materials and", "Textures"],
           [CH + "07-materials-and-textures.md", CH + "06-shader-foundations.md", CH + "02-prompting-game-art.md", GLOSS], True),
    "13": ("13 Shader verification.html", "Shader Verification", ["Key Terms:", "Shader Verification"],
           [CH + "08-shader-verification.md", CH + "00-the-toolchain.md", GLOSS], False),
    "14": ("14 Particles and VFX.html", "Particles and VFX", ["Key Terms:", "Particles and VFX"],
           [CH + "09-particle-effects.md", NOTES + "RIOT-SERIES-TERMS.md", GLOSS], False),
    "15": ("15 Animation principles.html", "Animation Principles", ["Key Terms:", "Animation Principles"],
           [CH + "10-animation-foundations.md", CH + "11-animation-and-interaction.md", NOTES + "RIOT-SERIES-TERMS.md", GLOSS], True),
    "16": ("16 Animation foundations.html", "Animation Foundations", ["Key Terms:", "Animation", "Foundations"],
           [CH + "10-animation-foundations.md", GLOSS], True),
    "17": ("17 Animation and interaction.html", "Animation and Interaction", ["Key Terms:", "Animation and", "Interaction"],
           [CH + "11-animation-and-interaction.md", CH + "10-animation-foundations.md", GLOSS], False),
    "18": ("18 Camera.html", "Camera", ["Key Terms:", "Camera"], [GLOSS], False),
    "19": ("19 Game AI perception and pathfinding.html", "Game AI, Perception and Pathfinding", ["Key Terms:", "Game AI, Perception", "and Pathfinding"],
           [CH + "14-game-ai-and-systems.md", CH + "01-walker-and-godot.md", GLOSS], False),
    "20": ("20 Game AI decisions and systems.html", "Game AI, Decisions and Systems", ["Key Terms:", "Game AI, Decisions", "and Systems"],
           [CH + "14-game-ai-and-systems.md", CH + "06-shader-foundations.md", GLOSS], False),
    "21": ("21 Walkthrough film.html", "The Walkthrough Film", ["Key Terms:", "The Walkthrough", "Film"],
           [GLOSS, "assignments"], False),
    "22": ("22 Game trailer.html", "The Game Trailer", ["Key Terms:", "The Game Trailer"],
           [CH + "00-the-toolchain.md", GLOSS], False),
    "23": ("23 Godot Unity Unreal comparison.html", "Godot, Unity and Unreal", ["Key Terms:", "Godot, Unity", "and Unreal"],
           [CH + "00-the-toolchain.md", CH + "01-walker-and-godot.md", CH + "04-scenes-collision-and-physics.md", GLOSS], True),
    "24": ("24 Unity editor interface.html", "The Unity Editor", ["Key Terms:", "The Unity Editor"],
           [CH + "15-final-projects-brief-to-export.md", GLOSS], False),
    "25": ("25 Unreal editor interface.html", "The Unreal Editor", ["Key Terms:", "The Unreal Editor"],
           [CH + "10-animation-foundations.md", GLOSS], False),
}


def slugify(s):
    import re
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")


def film(nn):
    deck, topic, lines, refs, on_exam = _F[nn]
    title = f"Key Terms: {topic}"
    slug = f"claude-liam-lecture-key-terms-{slugify(topic)}"
    # A film copy of a deck lives in exam-prep-deck-films/decks/ and wins over the study deck. Deck 11 has one:
    # the newer version from <course>/decks/ with the extra "more than one fragment shader" step.
    film_copy = HERE / "decks" / deck
    deck_path = film_copy if film_copy.exists() else COURSE / "glossary" / "decks" / deck
    ref_paths = [COURSE / r for r in refs]
    return {"nn": nn, "deck_file": deck_path, "study_deck": COURSE / "glossary" / "decks" / deck, "topic": topic, "title": title, "title_lines": lines,
            "chapter": ref_paths[0], "refs": ref_paths, "on_exam": on_exam, "slug": slug, "reel": COURSE / "youtube" / slug,
            "extract": HERE / "extract" / nn}


ALL = sorted(_F)

# Voice-only pronunciations (word or phrase -> IPA) for Kokoro. Only what the voice gets wrong is listed, each
# checked with the toolkit's phonemizer. Narration text and captions keep the normal spelling. Godot is in the
# Liam dictionary already. "A-I" is keyed on the Liam dictionary's respelling of AI.
PRONOUNCE = {}
AI_FIX = {"A-I": "ˈeɪaɪ", "A-I's": "ˈeɪaɪz"}

# What each tag means, where a deck's own opening note gives it a narrower meaning than the default.
# nn -> {tag: (card line, spoken sentence)}
LABEL_OVERRIDE = {
    "21": {"video only": ("from the course's film skills and assignment briefs",
                          "Video only: the term comes from the course's film skills and assignment briefs.")},
}

# The short line printed on the title card under the title (52 characters at most). Filled from each script's
# opening_description by make_film.py when a film has no entry here.
CARD_LINE = {}
