"""ACT III · What the AI Must Not Do  (B08-B13, all Manim)

The material is Walker's own rules, quoted verbatim (<= 15 words, ellipsis where a cut is made) with the file and line they come from,
and one tag for where each rule lives: "installed" (publish.sh copies it into every game), "doc" (a framework document, NOT installed),
"game file" (the game's own hand-written file). Sources: EVID/research/walker-brief.md section 2 (rule numbers in factcheck/act3.md),
checked against the files themselves: walker/prompts/zelda-gdd.md, prompts/runtime.md, README.md, asset-gen/SKILL.md (line numbers are the
working tree of 2026-10-09, which is what the research brief cites); walker-jumpman-clawd/AGENTS.md, design/DESIGN-STATUS.json.
Real game frames in B11 are Godot's own output of the walker-claude project (EVID/godot-captures/walker-claude, scripted input recorded
2026-10-09), shown as frames of that recording.

One cast for the act: THE AGENT (a terracotta dot), THE LOOP (an outlined track), a BARRIER (a short ink bar the dot stops at), and the
rule SLIP (outlined card: verbatim quote, source in Menlo, where-it-lives tag). Pacing: every cue is set from the REAL word times of the
narration audio (evidence/act3/word_times.json, faster-whisper) through a3_at().
"""
import glob as _glob

A3_X0 = -6.2                    # left text margin (serif labels)
A3_LP = 0.5                     # line pitch of a size-34 serif quote
A3_TAG = {"I": "installed", "D": "doc", "G": "game file"}
A3_CACHE = {}


def a3_at(self, t):
    """Wait until absolute beat time t (seconds of the narration audio)."""
    gap = t - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a3_tb(s, size, color):
    """EB Garamond with hidden bars at both ends (every label shares one ascender/descender box); returns (text, width of the two bars)."""
    t = T("|" + s + "|", size, color)
    t[0].set_opacity(0)
    t[-1].set_opacity(0)
    bw = T("|a|", size, color).width - T("a", size, color).width
    return t, bw


def a3_tl(s, x, y, size=36, color=INK):
    """Serif label whose LEFT edge (of the visible text) sits at x: the hidden left bar hangs ~0.0025*size outside it (measured in
    Pango: |a| minus a is ~0.005 units per point of size; a constant, so Gate A's stub, which cannot measure text, sees sane coordinates)."""
    t, bw = a3_tb(s, size, color)
    return t.move_to([x - 0.0025 * size, y, 0], aligned_edge=LEFT)


def a3_tc(s, cx, y, size=36, color=INK):
    """Serif label CENTRED on cx (the two hidden bars are symmetric, so the text's centre is the visible centre)."""
    t, bw = a3_tb(s, size, color)
    return t.move_to([cx, y, 0])


def a3_tr(s, x, y, size=36, color=INK):
    t, bw = a3_tb(s, size, color)
    return t.move_to([x + 0.0025 * size, y, 0], aligned_edge=RIGHT)


def a3_tw(s, size=34):
    """Visible width of a serif string (cached)."""
    k = (s, size)
    if k not in A3_CACHE:
        t, bw = a3_tb(s, size, INK)
        A3_CACHE[k] = t.width - bw
    return A3_CACHE[k]


def a3_m(s, x, y, size=32, color=INK):
    """Menlo text whose first character cell starts at x (0.25 units per character at size 32)."""
    t = M("|" + s + "|", size, color)
    t[0].set_opacity(0)
    t[-1].set_opacity(0)
    return t.move_to([x - 0.243 * size / 32, y, 0], aligned_edge=LEFT)


def a3_cx(x, nch, size=32):
    """x of the END of a Menlo run of nch characters that starts at x."""
    return x + nch * 0.25 * size / 32


def a3_pill(word, x, y, size=32):
    """Outlined tag, left edge at x. Returns (VGroup, right edge x)."""
    w = a3_tw(word, size) + 0.5
    ring = RoundedRectangle(width=w, height=0.54, corner_radius=0.31, fill_opacity=0, stroke_color=DIM,
                            stroke_width=4).move_to([x + w / 2, y, 0])
    lab = a3_tl(word, x + 0.25, y, size)
    return VGroup(ring, lab), x + w


def a3_slip(lines, src, tag, x, ytop, w, size=34, stack=False):
    """The rule slip: outlined card with the verbatim quote (lines are wrapped BY HAND: Gate A's stub cannot measure text), the source
    (Menlo) and the where-it-lives pill. Returns (group, bottom y)."""
    pad = 0.25
    h = 2 * pad + len(lines) * A3_LP + (1.27 if stack else 0.72)
    card = RoundedRectangle(width=w, height=h, corner_radius=0.15, fill_opacity=0, stroke_color=DIM,
                            stroke_width=4).move_to([x + w / 2, ytop - h / 2, 0])
    g = VGroup(card)
    for i, ln in enumerate(lines):
        g.add(a3_tl(ln, x + pad, ytop - pad - (i + 0.5) * A3_LP, size))
    ys = ytop - pad - len(lines) * A3_LP - 0.37
    g.add(a3_m(src, x + pad, ys))
    if stack:    # narrow slip: the tag goes on its own row under the source
        pill, _ = a3_pill(A3_TAG[tag], x + pad, ys - 0.55)
    else:
        pill, _ = a3_pill(A3_TAG[tag], a3_cx(x + pad, len(src)) + 0.35, ys)
    g.add(pill)
    return g, ytop - h


def a3_bar(x, y, h=0.5):
    """A barrier: a short ink bar across a path."""
    return Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=INK, stroke_width=9)


def a3_check(x, y, s=0.2):
    return check(x, y, s, INK, 7)


def a3_cross(x, y, r=0.17, sw=7):
    return VGroup(Line([x - r, y + r, 0], [x + r, y - r, 0], color=INK, stroke_width=sw),
                  Line([x - r, y - r, 0], [x + r, y + r, 0], color=INK, stroke_width=sw))


def a3_bump(self, dot, bar, x_in, x_back, y):
    """The agent walks into the barrier, is stopped, and comes back."""
    self.play(dot.animate.move_to([x_in, y, 0]), run_time=0.24)
    self.play(Indicate(bar, scale_factor=1.5, color=INK), run_time=0.22)
    self.play(dot.animate.move_to([x_back, y, 0]), run_time=0.2)


# ── B08 · scope (ACT TITLE) ─────────────────────────────────────────────────────────────────────────────────────────────
# zelda-gdd.md:13 (engines) and :40 (just to keep a loop running); the agent walks the loop and is stopped at each exit.
A3_STUBS = [("switch engine", 1.7), ("cut requirements", 1.05), ("extend schedule", 0.4), ("spend money", -0.25), ("publish", -0.9)]


class B08_Scope(Scene):
    def construct(self):
        title = a3_tl("What the AI Must Not Do", A3_X0, 3.0, 40)
        self.add(title)
        loop_pts = [[0.9, 2.3, 0], [1.9, 2.3, 0], [1.9, -1.25, 0], [0.9, -1.25, 0], [0.9, 2.3, 0]]
        track = VMobject(stroke_color=DIM, stroke_width=5).set_points_as_corners(loop_pts)
        dot = Dot([1.9, 2.3, 0], radius=0.15, color=TERRA)
        agent = a3_tl("the agent", 2.3, 2.3, 32)
        loopl = a3_tc("loop", 1.4, 0.6, 32)
        self.play(Create(track), run_time=0.7)
        self.play(FadeIn(dot), FadeIn(agent), FadeIn(loopl), run_time=0.4)
        a3_at(self, 2.5)
        scope = a3_tl("scope", 0.9, 3.0, 36)
        self.play(FadeIn(scope), run_time=0.3)
        # the where-it-lives legend (the first tag the viewer sees)
        a3_at(self, 3.2)
        leg = VGroup()
        for i, (k, gloss) in enumerate((("I", "in every game"), ("D", "framework only"), ("G", "that game's own"))):
            pill, _ = a3_pill(A3_TAG[k], 0.9, -1.85 - 0.57 * i)
            leg.add(pill, a3_tl(gloss, 3.25, -1.85 - 0.57 * i, 32, INK))
        s1, b1 = a3_slip(["“Do not silently use Unity,", "Bevy, Babylon.js, or a hosted", "game generator.”"],
                         "zelda-gdd.md:13", "D", -6.1, 2.5, 6.5)
        self.play(FadeIn(s1), FadeIn(leg), run_time=0.45)
        # stub 1 (engines) and the agent stopped at it
        stubs = [Line([1.9, y, 0], [2.9, y, 0], color=DIM, stroke_width=4) for lab, y in A3_STUBS]
        bars = [a3_bar(2.9, y) for lab, y in A3_STUBS]
        labs = [a3_tl(lab, 3.2, y, 32) for lab, y in A3_STUBS]
        a3_at(self, 3.85)
        self.play(Create(stubs[0]), Create(bars[0]), FadeIn(labs[0]), run_time=0.3)
        self.play(dot.animate.move_to([1.9, 1.7, 0]), run_time=0.15)
        a3_bump(self, dot, bars[0], 2.62, 1.9, 1.7)
        # the cut-requirements rule, then the other four exits drawn before the midpoint
        a3_at(self, 4.75)
        s2, b2 = a3_slip(["“Do not cut requirements,", "extend schedules, spend, publish", "… just to keep a loop running.”"],
                         "zelda-gdd.md:40", "D", -6.1, b1 - 0.15, 6.5)
        self.play(FadeIn(s2), Create(VGroup(*stubs[1:])), Create(VGroup(*bars[1:])), FadeIn(VGroup(*labs[1:])), run_time=0.7)
        for i, t in ((1, 6.36), (2, 7.52), (3, 8.4), (4, 9.08)):
            lab, y = A3_STUBS[i]
            a3_at(self, t - 0.62)
            self.play(dot.animate.move_to([1.9, y, 0]), run_time=0.16)
            a3_bump(self, dot, bars[i], 2.62, 1.9, y)
        # "just to keep the loop running": the agent runs the whole loop
        a3_at(self, 9.72)
        run = VMobject().set_points_as_corners([[1.9, -0.9, 0], [1.9, -1.25, 0], [0.9, -1.25, 0], [0.9, 2.3, 0], [1.9, 2.3, 0]])
        self.play(MoveAlongPath(dot, run), run_time=1.5)
        done(self)


# ── B09 · drafting is not permission (zelda-gdd.md:44 and :21) ──────────────────────────────────────────────────────────
class B09_DraftNotPermission(Scene):
    def construct(self):
        spine = Line([-5.6, 1.5, 0], [-5.6, -2.2, 0], color=DIM, stroke_width=4)
        p_draft = Line([-5.6, 1.5, 0], [-4.85, 1.5, 0], color=DIM, stroke_width=4)
        p_appr = Line([-5.6, -0.55, 0], [-4.2, -0.55, 0], color=DIM, stroke_width=4)
        p_run = Line([-5.6, -2.2, 0], [-4.2, -2.2, 0], color=DIM, stroke_width=4)
        bar_appr, bar_run = a3_bar(-4.2, -0.55, 0.8), a3_bar(-4.2, -2.2, 0.8)
        page = RoundedRectangle(width=2.2, height=2.0, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                stroke_width=5).move_to([-3.7, 1.5, 0])
        slot = DashedVMobject(RoundedRectangle(width=2.4, height=1.0, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                               stroke_width=4).move_to([-2.75, -0.55, 0]), num_dashes=28)
        runbox = RoundedRectangle(width=1.9, height=1.0, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                  stroke_width=4).move_to([-2.95, -2.2, 0])
        draft_l = a3_tl("draft", -4.8, 2.85, 36)
        appr_l = a3_tl("approval", -3.55, -0.55, 32)
        run_l = a3_tl("run", -3.7, -2.2, 32)
        dot = Dot([-5.6, 1.5, 0], radius=0.15, color=TERRA)
        self.add(draft_l, page, appr_l, run_l)
        self.play(Create(VGroup(spine, p_draft, p_appr, p_run)), Create(VGroup(bar_appr, bar_run)), Create(slot), Create(runbox),
                  FadeIn(dot), run_time=0.7)
        # the draft is written line by line
        ends = [-2.95, -3.15, -2.9, -3.35, -3.05]
        ys = [2.15, 1.8, 1.45, 1.1, 0.75]
        lns = [Line([-4.5, y, 0], [e, y, 0], color=DIM, stroke_width=5) for y, e in zip(ys, ends)]
        a3_at(self, 0.35)
        s1, b1 = a3_slip(["\u201cDrafting tasks is not", "authorization to", "execute them.\u201d"], "zelda-gdd.md:44", "D", 0.2, 2.0, 5.95)
        self.play(LaggedStart(*[Create(l) for l in lns[:3]], lag_ratio=0.35), FadeIn(s1), run_time=0.9)
        # "not permission to run it": the agent goes to the run exit and is stopped
        a3_at(self, 1.25)
        self.play(dot.animate.move_to([-5.6, -2.2, 0]), run_time=0.3)
        a3_bump(self, dot, bar_run, -4.55, -5.6, -2.2)
        self.play(dot.animate.move_to([-5.6, 1.5, 0]), run_time=0.3)
        # "A direct request for a complete draft allows the draft": the quote changes, the page fills
        a3_at(self, 2.55)
        s2, b2 = a3_slip(["\u201c\u2026 authorizes drafting with", "named assumptions; it does", "not authorize inventing", "approvals \u2026\u201d"],
                         "zelda-gdd.md:21", "D", 0.2, 2.0, 5.95)
        self.play(FadeOut(s1), FadeIn(s2), run_time=0.4)
        a3_at(self, 3.7)
        self.play(LaggedStart(*[Create(l) for l in lns[3:]], lag_ratio=0.5), run_time=0.7)
        a3_at(self, 4.3)
        self.play(dot.animate.move_to([-4.95, 1.5, 0]), run_time=0.3)
        # "with its assumptions named"
        a3_at(self, 5.75)
        asm = VGroup(a3_tl("assumptions", -2.3, 2.15, 36))
        for y in (1.55, 1.1, 0.65):
            asm.add(Dot([-2.15, y, 0], radius=0.06, color=DIM), Line([-1.9, y, 0], [-0.5, y, 0], color=DIM, stroke_width=5))
        self.play(FadeIn(asm), run_time=0.5)
        # "does not allow inventing approvals": the agent goes to the approval slot and is stopped; the slot stays empty
        a3_at(self, 7.05)
        self.play(dot.animate.move_to([-5.6, 1.5, 0]), run_time=0.2)
        self.play(dot.animate.move_to([-5.6, -0.55, 0]), run_time=0.3)
        a3_bump(self, dot, bar_appr, -4.55, -5.6, -0.55)
        done(self)


# ── B10 · four gates, signed by humans only (C/design/DESIGN-STATUS.json:10-13 and :19) ────────────────────────────────
A3_GATES = [("vision", -3.9, "  "), ("systems", -1.4, " "), ("world", 1.1, "   "), ("scope", 3.6, "   ")]


class B10_FourGates(Scene):
    def construct(self):
        path = Line([-6.0, 2.5, 0], [6.0, 2.5, 0], color=DIM, stroke_width=4)
        dot = Dot([-5.8, 2.5, 0], radius=0.15, color=TERRA)
        self.add(path)
        self.play(FadeIn(dot), run_time=0.4)
        bars, labs = [], []
        for (name, gx, _), t in zip(A3_GATES, (0.92, 1.34, 2.2, 2.62)):
            a3_at(self, t)
            b = a3_bar(gx, 2.5, 0.9)
            lb = a3_tc(name, gx, 1.8, 36)
            bars.append(b)
            labs.append(lb)
            self.play(Create(b), FadeIn(lb), run_time=0.3)
        # the real status file: every gate unsigned
        a3_at(self, 2.95)
        head = a3_m("DESIGN-STATUS.json:10-13, 19", -6.0, 1.0)
        pill, _ = a3_pill(A3_TAG["G"], a3_cx(-6.0, 28) + 0.35, 1.0)
        rows, nulls = VGroup(), []
        for i, (name, gx, pad) in enumerate(A3_GATES):
            y = 0.3 - 0.7 * i
            pre = f'  "{name}":{pad}{{"signed_by": '
            rows.add(a3_m(pre + "null, …},", -6.0, y))
            nulls.append(rows[-1])
        notes = a3_m('"notes": "… Gates are signed by humans only."', -6.0, -2.7)
        self.play(FadeIn(head), FadeIn(pill), FadeIn(rows), FadeIn(notes), run_time=0.5)
        # "The agent never signs a gate": it walks to the first gate and is stopped; every signed_by is still null
        a3_at(self, 4.75)
        self.play(dot.animate.move_to([-4.3, 2.5, 0]), run_time=0.6)
        self.play(Indicate(bars[0], scale_factor=1.5, color=INK), run_time=0.25)
        self.play(LaggedStart(*[Indicate(n, scale_factor=1.06, color=INK) for n in nulls], lag_ratio=0.3), run_time=1.1)
        done(self)


# ── B11 · proof (runtime.md:10, README.md:28, AGENTS.md:13, zelda-gdd.md:52) ───────────────────────────────────────────
# The picture is the REAL running game (frames of walker-claude-jumpman-gameplay.mp4, scripted input recorded 2026-10-09, every 3rd
# frame = 10 fps in pantry/a3_run_001..072.jpg). The rule slips swap in the right column; four small cards light up in turn.
A3_RUN = "pantry/a3_run_%03d.jpg"
A3_RUN_N = 72


def a3_run_window(self, cx, cy, w, t0, speed=1.0):
    """The recorded run as an ImageMobject whose pixels follow scene time (an updater): frame k shows from t0 + k*0.1/speed;
    it loops (the run is 7.2 s). Returns the image."""
    img = ImageMobject(A3_RUN % 1).scale_to_fit_width(w).move_to([cx, cy, 0])
    st = {"t": -t0, "i": 0}

    def up(m, dt):
        st["t"] += dt
        i = int(st["t"] * speed / 0.1) % A3_RUN_N
        if i != st["i"]:
            st["i"] = i
            try:
                from PIL import Image as _PI
                m.pixel_array = np.array(_PI.open(A3_RUN % (i + 1)).convert("RGBA"))
            except Exception:
                pass
    img.add_updater(up)
    return img


def a3_glyph(k, cx, cy):
    """The four small proof glyphs (B11 cards)."""
    if k == 0:       # a running game: a screen with a play triangle
        return VGroup(RoundedRectangle(width=0.95, height=0.6, corner_radius=0.08, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([cx, cy, 0]),
                      Polygon([cx - 0.12, cy - 0.16, 0], [cx - 0.12, cy + 0.16, 0], [cx + 0.18, cy, 0], fill_color=INK, fill_opacity=1,
                              stroke_width=0))
    if k == 1:       # build passed  !=  a human played it
        return VGroup(RoundedRectangle(width=0.5, height=0.5, corner_radius=0.06, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([cx - 0.62, cy, 0]),
                      a3_check(cx - 0.62, cy, 0.14),
                      Line([cx - 0.2, cy + 0.09, 0], [cx + 0.2, cy + 0.09, 0], color=INK, stroke_width=6),
                      Line([cx - 0.2, cy - 0.09, 0], [cx + 0.2, cy - 0.09, 0], color=INK, stroke_width=6),
                      Line([cx - 0.12, cy - 0.26, 0], [cx + 0.12, cy + 0.26, 0], color=INK, stroke_width=6),
                      DashedVMobject(RoundedRectangle(width=0.5, height=0.5, corner_radius=0.06, fill_opacity=0, stroke_color=DIM,
                                                      stroke_width=4).move_to([cx + 0.62, cy, 0]), num_dashes=16))
    if k == 2:       # an invented pass: an empty (dashed) result, crossed
        return VGroup(DashedVMobject(RoundedRectangle(width=0.95, height=0.6, corner_radius=0.08, fill_opacity=0, stroke_color=DIM,
                                                      stroke_width=4).move_to([cx, cy, 0]), num_dashes=24),
                      a3_cross(cx, cy, 0.17, 7))
    # k == 3: a weakened test: the pass line is pushed down
    return VGroup(Line([cx - 0.55, cy + 0.24, 0], [cx + 0.2, cy + 0.24, 0], color=DIM, stroke_width=5),
                  Arrow([cx - 0.3, cy + 0.2, 0], [cx - 0.3, cy - 0.28, 0], buff=0, color=INK, stroke_width=6, tip_length=0.16),
                  a3_cross(cx + 0.45, cy - 0.02, 0.15, 7))


A3_B11_CARDS = [("running game", -4.675), ("not a play-test", -1.555), ("invented passes", 1.565), ("weakened test", 4.685)]


class B11_Proof(Scene):
    def construct(self):
        cx, cy, w = -3.15, 1.14, 5.9
        h = w * 9 / 16
        frame = RoundedRectangle(width=w + 0.2, height=h + 0.2, corner_radius=0.1, fill_opacity=0, stroke_color=DIM,
                                 stroke_width=4).move_to([cx, cy, 0])
        win = a3_run_window(self, cx, cy, w, -0.55)
        cap1 = a3_tl("recorded run, looping", cx - w / 2, -0.95, 36)
        cap2 = a3_tl("scripted input, 2026-10-09", cx - w / 2, -1.4, 32, DIM)
        cap2b = a3_tl("scripted input: not a play-test", cx - w / 2, -1.4, 32, DIM)
        self.add(win, frame, cap1, cap2)
        # While the voice says "build is not a play-test" the real run steps aside (a real game frame is read by GATE T as text and
        # terracotta, so the 50% frame must not hold one) and the same idea is drawn large; the run returns after the midpoint.
        bx, by = -5.3, 1.3
        big = VGroup(RoundedRectangle(width=1.8, height=1.8, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([bx, by, 0]),
                     check(bx, by, 0.5, INK, 10),
                     a3_tc("build", bx, 0.0, 36),
                     Line([-3.9, by + 0.22, 0], [-3.1, by + 0.22, 0], color=INK, stroke_width=9),
                     Line([-3.9, by - 0.22, 0], [-3.1, by - 0.22, 0], color=INK, stroke_width=9),
                     Line([-3.65, by - 0.65, 0], [-3.35, by + 0.65, 0], color=INK, stroke_width=9),
                     DashedVMobject(RoundedRectangle(width=1.8, height=1.8, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                                     stroke_width=5).move_to([-1.7, by, 0]), num_dashes=36),
                     a3_tc("human play-test", -1.7, 0.0, 36))
        slips = [
            (["“Judge progress from the", "running game, never from a", "clean build …”"], "runtime.md:10", "I"),
            (["“A successful build is not", "evidence of a successful", "human playtest.”"], "README.md:28", "D"),
            (["“Never invent human", "playtests, … approvals or", "test passes.”"], "AGENTS.md:13", "G"),
            (["“… instead of weakening", "the test to make it pass.”"], "zelda-gdd.md:52", "D")]
        cur = None
        times = [0.3, 3.45, 6.85, 11.3]
        for k, (lines, src, tag) in enumerate(slips):
            a3_at(self, times[k])
            sl, _ = a3_slip(lines, src, tag, 0.3, 2.8, 5.85)
            pill = sl[-1]
            if k == 2:      # the "game file" pill lands on "The game's own file adds" (7.4 s); the quote is already up before the midpoint
                sl.remove(pill)
            # the card for this rule, lit as the rule is spoken
            lab, ccx = A3_B11_CARDS[k]
            card = RoundedRectangle(width=2.85, height=1.3, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                    stroke_width=4).move_to([ccx, -2.45, 0])
            glyph = a3_glyph(k, ccx, -2.2)
            label = a3_tc(lab, ccx, -2.82, 32)
            if cur is None:
                self.play(FadeIn(sl), FadeIn(card), Create(glyph), FadeIn(label), run_time=0.45)
            else:
                self.play(FadeOut(cur), FadeIn(sl), FadeIn(card), Create(glyph), FadeIn(label), run_time=0.45)
            cur = sl
            if k == 1:      # the run steps aside while the build/play-test idea is drawn large
                a3_at(self, 5.6)
                self.play(FadeOut(win), FadeOut(frame), FadeOut(cap1), FadeOut(cap2), Create(big), run_time=0.45)
            if k == 2:      # pill on the words, then the run returns after the midpoint, captioned as what it is: scripted input
                a3_at(self, 7.6)
                sl.add(pill)
                self.play(FadeIn(pill), FadeOut(big), FadeIn(win), FadeIn(frame), FadeIn(cap1), FadeIn(cap2b), run_time=0.45)
        done(self)


# ── B12 · money and safety (runtime.md:4, asset-gen SKILL.md:92, README.md:71 and :63, zelda-gdd.md:56) ──────────────────
# Three zones, side by side (money | credentials | publishing). The headers are on screen from the first frame; each zone draws on its cue.
# The prices are asset-gen's own quick-reference line (asset-gen/SKILL.md:92), quoted as written, not checked against today's price lists.
class B12_MoneySafety(Scene):
    def construct(self):
        ax, bx, cx = -6.1, -1.4, 2.35
        hA, hB, hC = a3_tl("money", ax, 3.0, 36), a3_tl("credentials", bx, 3.0, 36), a3_tl("publishing", cx, 3.0, 36)
        self.add(hA, hB, hC)
        # zone A: what a call costs (hero number), then the agent stopped at "confirm" before the first paid call
        src_l = a3_m("SKILL.md:92", -4.4, 2.2)
        path = Line([-5.9, 0.85, 0], [-4.5, 0.85, 0], color=DIM, stroke_width=4)
        bar = a3_bar(-4.5, 0.85, 0.7)
        box = DashedVMobject(RoundedRectangle(width=1.5, height=0.7, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                              stroke_width=4).move_to([-3.45, 0.85, 0]), num_dashes=22)
        boxl = a3_tc("call", -3.45, 0.85, 32)
        conf = a3_tl("confirm", -2.55, 0.85, 32)
        dot = Dot([-5.8, 0.85, 0], radius=0.15, color=TERRA)
        a3_at(self, 1.5)
        self.play(FadeIn(src_l), Create(path), Create(bar), Create(box), FadeIn(boxl), FadeIn(dot), run_time=0.5)
        cur = None
        for (num, lab), t in zip((("2¢", "asset-gen: sprite"), ("37¢", "asset-gen: 3D asset"), ("≈92¢", "asset-gen: rigged character")), (2.1, 3.1, 4.0)):
            a3_at(self, t)
            pair = VGroup(a3_tl(num, ax, 2.2, 56), a3_tl(lab, ax, 1.6, 32))
            self.play(*([FadeOut(cur)] if cur is not None else []), FadeIn(pair), run_time=0.3)
            cur = pair
        a3_at(self, 4.85)
        sA, _ = a3_slip(["“Confirm the spend …", "before the first paid", "generation.”"], "runtime.md:4", "I", ax, 0.0, 4.5, 32, stack=True)
        self.play(FadeIn(sA), run_time=0.4)
        a3_at(self, 5.45)
        self.play(dot.animate.move_to([-4.85, 0.85, 0]), FadeIn(conf), run_time=0.35)
        self.play(Indicate(bar, scale_factor=1.5, color=INK), run_time=0.25)
        self.play(dot.animate.move_to([-5.8, 0.85, 0]), run_time=0.25)
        # the other two zones' containers are laid out before the midpoint; their rules arrive on their own cues
        a3_at(self, 6.15)
        bbar = a3_bar(0.55, 1.9, 0.9)
        bbox = RoundedRectangle(width=1.4, height=0.95, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([1.5, 1.9, 0])
        bboxl = a3_tc("commit", 1.5, 1.9, 32)
        comp = RoundedRectangle(width=1.35, height=1.0, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.5, 1.9, 0])
        compl = a3_tc("computer", 3.5, 1.2, 32)
        gh = RoundedRectangle(width=1.2, height=1.0, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([5.5, 1.9, 0])
        ghl = a3_tc("GitHub", 5.5, 1.2, 32)
        self.play(Create(bbar), Create(bbox), FadeIn(bboxl), Create(comp), FadeIn(compl), Create(gh), FadeIn(ghl), run_time=0.6)
        # zone B: a key goes toward the commit and is stopped
        a3_at(self, 7.3)
        ring = Circle(radius=0.22, color=INK, stroke_width=6).move_to([-1.0, 1.9, 0])
        shaft = Line([-0.78, 1.9, 0], [-0.05, 1.9, 0], color=INK, stroke_width=6)
        teeth = VGroup(Line([-0.3, 1.9, 0], [-0.3, 1.68, 0], color=INK, stroke_width=6), Line([-0.05, 1.9, 0], [-0.05, 1.68, 0], color=INK, stroke_width=6))
        key = VGroup(ring, shaft, teeth)
        sB, _ = a3_slip(["“Never commit", "credentials.”"], "README.md:71", "D", bx, 0.0, 3.55, 32, stack=True)
        self.play(FadeIn(key), FadeIn(sB), run_time=0.5)
        a3_at(self, 7.95)
        self.play(key.animate.shift(RIGHT * 0.55), run_time=0.3)
        self.play(Indicate(bbar, scale_factor=1.5, color=INK), run_time=0.25)
        self.play(key.animate.shift(LEFT * 0.55), run_time=0.25)
        # zone C: files written on the computer are not an upload to GitHub
        a3_at(self, 8.85)
        sC, _ = a3_slip(["“… write runtime", "files locally, not", "upload to GitHub.”"], "README.md:63", "D", cx, 0.0, 3.8, 32, stack=True)
        self.play(FadeIn(sC), run_time=0.5)
        a3_at(self, 9.3)
        page = RoundedRectangle(width=0.4, height=0.55, corner_radius=0.05, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([3.5, 1.9, 0])
        pl = VGroup(*[Line([3.37, 1.9 + dy, 0], [3.63, 1.9 + dy, 0], color=DIM, stroke_width=4) for dy in (0.1, -0.02, -0.14)])
        self.play(Create(page), Create(pl), run_time=0.4)
        a3_at(self, 10.9)
        arr = Line([4.18, 1.9, 0], [4.9, 1.9, 0], color=DIM, stroke_width=4)
        cbar = a3_bar(4.5, 1.9, 0.7)
        self.play(Create(arr), Create(cbar), run_time=0.35)
        a3_at(self, 12.3)
        sep = a3_tc("separate action", 4.5, 0.6, 32)
        self.play(FadeIn(sep), Indicate(cbar, scale_factor=1.5, color=INK), run_time=0.5)
        done(self)


# ── B13 · size: one reviewable change, and the failure predicted first (C/AGENTS.md:11) ─────────────────────────────────
# The grid is a DRAWING of an idea (a game as a few cells), not a game capture; "one change" is one cell, "predicted failure" is a note
# written before the cell is built.
class B13_OneChange(Scene):
    def construct(self):
        gx0, gy0, cw, ch = 0.7, 2.6, 1.35, 1.15
        hdr = a3_tl("the game", gx0, 2.95, 36)
        self.add(hdr)
        cells = VGroup(*[Rectangle(width=cw, height=ch, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to(
            [gx0 + cw * (c + 0.5), gy0 - ch * (r + 0.5), 0]) for r in range(3) for c in range(4)])
        self.play(Create(cells), run_time=0.7)
        a3_at(self, 0.45)
        sl, _ = a3_slip(["“Make one reviewable change.", "Predict a failure, preserve", "unrelated behavior …”"], "AGENTS.md:11", "G", -6.1, 1.3, 6.4)
        self.play(FadeIn(sl), run_time=0.4)
        # "Make one reviewable change": ONE cell is marked
        a3_at(self, 0.9)
        tx, ty = gx0 + cw * 2.5, gy0 - ch * 2.5
        one = Rectangle(width=cw, height=ch, stroke_color=INK, stroke_width=9, fill_opacity=0).move_to([tx, ty, 0])
        one_l = a3_tr("one change", gx0 + cw * 4, 2.95, 36)
        pt = Dot([tx, ty + ch / 2 + 0.28, 0], radius=0.0)
        self.play(Create(one), FadeIn(one_l), run_time=0.5)
        # "Predict how it could fail": the note is written first, pointing at the cell
        a3_at(self, 2.9)
        note = RoundedRectangle(width=3.4, height=0.8, corner_radius=0.14, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([tx, -1.85, 0])
        note_l = a3_tc("predicted failure", tx, -1.85, 32)
        arr = Arrow([tx, -1.45, 0], [tx, -0.98, 0], buff=0, color=INK, stroke_width=6, tip_length=0.18)
        self.play(FadeIn(note), FadeIn(note_l), Create(arr), run_time=0.5)
        # "before you build it": only then is the cell built (the agent's dot lands in it)
        a3_at(self, 4.3)
        built = Dot([tx, ty, 0], radius=0.17, color=TERRA)
        self.play(GrowFromCenter(built), run_time=0.4)
        done(self)
