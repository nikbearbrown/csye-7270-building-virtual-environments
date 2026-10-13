"""ACT II · What the AI Does, What You Do  (B06-B15, all Manim)

One cast for the act:
  THE CHANNEL AND THE GATE (B06-B08): kraft crates (game parts) stream out of a grey maker block along a channel and meet a
    wall with ONE person-sized slot. The channel widens, the slot does not (the make/check asymmetry, drawn like water and a sluice).
  YOU = one Professor Bear portrait (pantry/a2_bear_*.png, 1x1 #71, the same one in every beat that needs "you").
  REAL EVIDENCE, shown as itself: a real check receipt (S/evidence/mechanics-*.json), real code and scene lines of walker-claude,
    real captures of the Claude Walker game (frames from walker-claude-jumpman-gameplay.mp4 stepped in time), the project's own
    brief and signature-slot file. Drawn pictures of an idea are labelled "example".
Pacing: a2_at() waits for the real spoken time of a word (faster-whisper times, evidence/act2/word_times.json).
GATE T notes: grey (BAR1/BAR2/DIM) for big blocks, never ink fills; terracotta only as dots; no ring around capture pixels.
"""

A2P = "pantry/"
A2_BEAR = A2P + "a2_bear_head.png"
A2_CRATE_F, A2_CRATE_T = "#DCC9AA", "#F3E9D8"


def a2_at(self, t):
    """Wait until the clip clock reaches t seconds (the real spoken time of a word, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a2_lab(s, x, y, size=36, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a2_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A2P + name)
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a2_x(x, y, s=0.17, color=INK, w=7):
    """An ink cross."""
    return VGroup(Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w),
                  Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w))


def a2_crate(x, y, s=0.8):
    """A kraft crate (a game part): front face + a slanted top face. (x, y) = centre of the front face."""
    k = s * 0.22
    front = Square(side_length=s, fill_color=A2_CRATE_F, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    top = Polygon([x - s / 2, y + s / 2, 0], [x + s / 2, y + s / 2, 0], [x + s / 2 + k, y + s / 2 + k * 0.8, 0],
                  [x - s / 2 + k, y + s / 2 + k * 0.8, 0], fill_color=A2_CRATE_T, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(front, top)


def a2_portrait(x, y, h=1.5, ring=True):
    """Professor Bear = 'you' (the PROFESSOR BEAR LAW): the same circular portrait in every beat of the act."""
    im = ImageMobject(A2_BEAR)
    im.set_height(h)
    im.move_to([x, y, 0])
    return im


def a2_portrait_ring(x, y, h=1.5):
    return Circle(radius=h / 2, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x, y, 0])


# ── real game footage: frames of walker-claude-jumpman-gameplay.mp4 (12 fps, 1280x720), stepped in time ─────────────────
_A2_FR = {}


def a2_frames():
    if not _A2_FR:
        import glob
        from PIL import Image as _Im
        for f in sorted(glob.glob(A2P + "a2_gp/f*.jpg")):
            _A2_FR[len(_A2_FR)] = np.array(_Im.open(f).convert("RGBA"))
    return _A2_FR


def a2_clip(h, at, start=0.0, fps=12.0):
    """The real gameplay capture as a stepped image: shows source time `start + (scene time since creation)`; holds the last frame."""
    fr = a2_frames()
    n = len(fr)
    if n == 0:                                   # (Gate A's folder holds only scenes.py: no frames there)
        im = ImageMobject(np.zeros((72, 128, 4), dtype=np.uint8))
        im.set_height(h)
        im.move_to([at[0], at[1], 0])
        return im
    im = ImageMobject(fr[min(n - 1, int(start * fps))])
    im.set_height(h)
    im.move_to([at[0], at[1], 0])
    im._a2 = dict(t=0.0, last=-1)

    def tick(m, dt):
        m._a2["t"] += dt
        i = min(n - 1, int((start + m._a2["t"]) * fps))
        if i != m._a2["last"]:
            m._a2["last"] = i
            m.pixel_array = fr[i]
    im.add_updater(tick)
    return im


def a2_window(cx, cy, w, h, color=DIM):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=5, fill_opacity=0).move_to([cx, cy, 0])


# ── the channel and the gate (B06-B08) ──────────────────────────────────────────────────────────────────────────
A2_FLOOR = -0.9            # channel floor (crate bottoms)
A2_GATE_X = 3.0            # the wall


def a2_gate(slot_top=0.1):
    """The wall with ONE person-sized slot (1.0 high) and its (unlit) lamp. Returns (wall, lamp)."""
    wx = A2_GATE_X
    low = Rectangle(width=0.34, height=0.6, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([wx, A2_FLOOR - 0.3, 0])
    up = Rectangle(width=0.34, height=1.9, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([wx, slot_top + 0.95, 0])
    lamp = Circle(radius=0.13, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([wx, slot_top + 0.4, 0])
    return VGroup(low, up), lamp


def a2_maker(h=1.9, cy=-0.2):
    """The grey maker block with its mouth facing the channel."""
    body = Rectangle(width=1.5, height=h, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-5.45, cy, 0])
    mouth = Rectangle(width=0.5, height=0.8, fill_color=STAGE, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-4.95, A2_FLOOR + 0.4, 0])
    return VGroup(body, mouth)


def a2_channel_lines(h=0.9, x0=-4.7, x1=A2_GATE_X - 0.17):
    """Floor and roof of the channel (roof at floor + h + 0.1)."""
    fl = Line([x0, A2_FLOOR, 0], [x1, A2_FLOOR, 0], color=INK, stroke_width=5)
    rf = Line([x0, A2_FLOOR + h + 0.1, 0], [x1, A2_FLOOR + h + 0.1, 0], color=INK, stroke_width=5)
    return fl, rf


# ── B06 · two jobs: making is cheap, checking is not ───────────────────────────────────────────────────────────────
class B06_TwoJobs(Scene):
    def construct(self):
        title = T("What the AI Does, What You Do", 40).move_to([-3.1, 2.95, 0])
        title.set_x(-6.2 + title.width / 2)
        maker = a2_maker()
        wall, lamp = a2_gate()
        fl, rf = a2_channel_lines()
        self.add(title, maker, wall, lamp, fl)
        # the pass tray after the gate
        tray = Line([3.55, A2_FLOOR, 0], [6.0, A2_FLOOR, 0], color=INK, stroke_width=5)
        self.add(tray)
        a2_at(self, 1.2)                                       # "making an answer"
        mk_l = a2_lab("make", -5.45, -2.05, 36)
        c1 = a2_crate(-4.95, A2_FLOOR + 0.4)
        self.play(FadeIn(mk_l), FadeIn(c1, shift=RIGHT * 0.3), run_time=0.4)
        self.play(c1.animate.shift(RIGHT * 6.9), run_time=1.0)       # rolls to the gate (x = 1.95)
        a2_at(self, 2.2)                                       # "checking an answer"
        ck_l = a2_lab("check", A2_GATE_X, -2.05, 36)
        self.play(FadeIn(ck_l), run_time=0.3)
        lit = Dot(lamp.get_center(), radius=0.13, color=TERRA)
        self.play(FadeIn(lit), run_time=0.2)
        self.play(c1.animate.shift(RIGHT * 3.35), run_time=0.9)      # slowly through the slot -> x = 5.3
        self.play(FadeOut(lit), run_time=0.15)
        tick = check(5.3, 0.45, s=0.24, color=INK, w=8)
        self.play(Create(tick), run_time=0.35)
        # (midpoint 4.35: one crate made, checked, in the tray; labels in place)
        a2_at(self, 4.55)                                      # "The A.I. made the first one cheap"
        crates = [a2_crate(-4.95, A2_FLOOR + 0.4) for _ in range(5)]
        self.add(*crates)
        dest = [1.95 - 0.88 * k for k in range(5)]
        self.play(LaggedStart(*[c.animate.shift(RIGHT * (d + 4.95)) for c, d in zip(crates, dest)], lag_ratio=0.28), run_time=1.5)
        ok = check(-5.95, -2.8, s=0.2, color=INK, w=7)
        ch_l = a2_lab("cheap", -5.0, -2.8, 36)
        self.play(Create(ok), FadeIn(ch_l), run_time=0.35)
        a2_at(self, 6.3)                                       # "It did not make the second one cheap"
        lit2 = Dot(lamp.get_center(), radius=0.13, color=TERRA)
        self.play(FadeIn(lit2), run_time=0.15)
        self.play(crates[0].animate.shift(RIGHT * 2.4), run_time=1.3)
        nx = a2_x(A2_GATE_X - 1.25, -2.8)
        nc_l = a2_lab("not cheap", A2_GATE_X + 0.35, -2.8, 36)
        self.play(Create(nx), FadeIn(nc_l), run_time=0.35)
        done(self)


# ── B07 · the channel widens, the gate stays person-sized ───────────────────────────────────────────────────────────
class B07_WiderChannel(Scene):
    def construct(self):
        maker = a2_maker()
        wall, lamp = a2_gate()
        fl, rf = a2_channel_lines()
        mk_l = a2_lab("make", -5.45, -2.05, 36)
        ck_l = a2_lab("check", A2_GATE_X, -2.05, 36)
        tray = Line([3.55, A2_FLOOR, 0], [6.0, A2_FLOOR, 0], color=INK, stroke_width=5)
        q = [a2_crate(1.95 - 0.88 * k, A2_FLOOR + 0.4) for k in range(3)]
        self.add(maker, wall, lamp, fl, tray, mk_l, ck_l, *q)
        a2_at(self, 0.3)                                       # "it gets harder, not easier"
        lit = Dot(lamp.get_center(), radius=0.13, color=TERRA)
        self.play(FadeIn(lit), run_time=0.2)
        a2_at(self, 1.7)                                       # "The faster the A.I. makes things"
        more = [a2_crate(-4.95, A2_FLOOR + 0.4) for _ in range(4)]
        self.add(*more)
        dest = [1.95 - 0.88 * (k + 3) for k in range(4)]
        self.play(LaggedStart(*[c.animate.shift(RIGHT * (d + 4.95)) for c, d in zip(more, dest)], lag_ratio=0.2), run_time=1.9)
        # the queue is now 8 deep, backed up to the maker (the midpoint frame is a still)
        a2_at(self, 4.9)                                       # "The channel for making gets wider"
        up_h = 2.7
        rf2 = Line([-4.7, A2_FLOOR + up_h + 0.1, 0], [A2_GATE_X - 0.17, A2_FLOOR + up_h + 0.1, 0], color=INK, stroke_width=5)
        w_arr = dim_arrow([-4.2, A2_FLOOR + 0.0, 0], [-4.2, A2_FLOOR + up_h + 0.1, 0], color=INK, w=5)
        wide_l = a2_lab("wider", -3.2, 1.35, 36)
        rows = VGroup(*[a2_crate(1.95 - 0.88 * k, A2_FLOOR + 0.4 + 0.9 * r) for r in (1, 2) for k in range(3)])
        self.play(Create(rf2), GrowArrow(w_arr), FadeIn(wide_l), run_time=0.7)
        self.play(FadeIn(rows, shift=RIGHT * 0.3), run_time=0.5)
        a2_at(self, 6.6)                                       # "the gate for checking stays person-sized"
        g_arr = dim_arrow([3.62, A2_FLOOR, 0], [3.62, A2_FLOOR + 1.0, 0], color=INK, w=5)
        who = a2_portrait(5.05, 1.2, 1.5)
        who_l = a2_lab("person-sized", 5.05, 0.15, 32)
        self.play(GrowArrow(g_arr), FadeIn(who, scale=0.85), run_time=0.5)
        self.play(FadeIn(who_l), run_time=0.3)
        done(self)


# ── B08 · the claim has limits: a tool measures, but a person chose the check and decides what was meant ────────────────
class B08_ClaimWithLimits(Scene):
    def construct(self):
        # an argument, not a law: the person-sized gate drawn dashed
        g1 = DashedVMobject(Rectangle(width=0.4, height=0.5).move_to([-5.6, 1.65, 0]), num_dashes=48).set_stroke(DIM, 5)
        g2 = DashedVMobject(Rectangle(width=0.4, height=0.8).move_to([-5.6, 2.85, 0]), num_dashes=64).set_stroke(DIM, 5)
        g_l = a2_lab("argument, not law", -3.35, 2.15, 36)
        a2_at(self, 1.4)                                        # "an argument with limits"
        self.play(Create(g1), Create(g2), FadeIn(g_l), run_time=0.7)
        # the real receipt pane
        pane = RoundedRectangle(width=8.95, height=3.55, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([1.85, -0.35, 0])
        cap = a2_lab("recorded receipt", 1.85, -2.55, 34)
        X0 = -2.35
        lines = [M('"id": "fixed-jump-and-no-double",', 32), M("…", 32), M('"rise_px": 56.07470703125', 32), M("…", 32), M('"status": "PASS"', 32)]
        ys = [0.95, 0.4, -0.15, -0.7, -1.25]
        for ln, y in zip(lines, ys):
            ln.move_to([X0 + ln.width / 2, y, 0])
        a2_at(self, 3.45)                                       # "A tool that runs your game and measures it"
        self.play(Create(pane), FadeIn(cap), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.25), run_time=1.4)
        a2_at(self, 5.35)                                       # "does check something"
        tick = check(5.3, -1.25, s=0.22, color=INK, w=8)
        self.play(Create(tick), run_time=0.3)
        # (midpoint 5.95: the real receipt, ticked)
        a2_at(self, 6.75)                                       # "a person chose that check"
        who = a2_portrait(-4.35, -0.2, 1.4)
        arr = Arrow([-3.55, -0.2, 0], [-2.55, 0.8, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        dot = Dot([X0 - 0.2, 0.95, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(who, scale=0.85), run_time=0.3)
        self.play(GrowArrow(arr), FadeIn(dot), run_time=0.4)
        a2_at(self, 8.3)                                        # "a person decides whether the result is what was meant"
        arr2 = Arrow([-3.55, -0.2, 0], [-2.55, -0.15, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        lead = Line([4.2, -0.15, 0], [4.5, -0.15, 0], color=DIM, stroke_width=3)
        q_l = T("meant?", 36).move_to([5.3, -0.15, 0])
        self.play(FadeOut(arr), FadeOut(dot), run_time=0.2)
        self.play(GrowArrow(arr2), Create(lead), FadeIn(q_l), run_time=0.5)
        done(self)


# ── B09 · the split: the A.I. does the typing (five real kinds of file from the Claude Walker game) ───────────────────────
class B09_TheTyping(Scene):
    def construct(self):
        a2_at(self, 2.0)                                        # "The A.I. does the typing"
        hd = T("the A.I. types", 38).move_to([-4.6, 2.9, 0])
        hd.set_x(-5.9 + hd.width / 2)
        hdot = Dot([-6.15, 2.9, 0], radius=0.09, color=TERRA)
        self.play(FadeIn(hd), FadeIn(hdot), run_time=0.3)
        YS = [1.9, 0.85, -0.2, -1.15, -2.1]
        X_ART = -2.2

        def row_label(s, y):
            t = T(s, 36).move_to([0, y, 0])
            t.set_x(-5.9 + t.width / 2)
            return t

        def mono(s, y):
            m = M(s, 32)
            m.move_to([X_ART + m.width / 2, y, 0])
            return m
        # 1 scenes: a real scene file
        a2_at(self, 3.5)                                        # "scenes"
        l1 = row_label("scenes", YS[0])
        a1 = VGroup(mono('[node name="ClawdGallery" …]', YS[0] + 0.25), mono('script = ExtResource("1")', YS[0] - 0.25))
        self.play(FadeIn(l1), FadeIn(a1, shift=RIGHT * 0.2), run_time=0.3)
        # 2 scripts: real GDScript
        a2_at(self, 4.15)                                       # "scripts"
        l2 = row_label("scripts", YS[1])
        a2 = VGroup(mono("extends CharacterBody2D", YS[1] + 0.25), mono("var tuning = Tuning.new()", YS[1] - 0.25))
        self.play(FadeIn(l2), FadeIn(a2, shift=RIGHT * 0.2), run_time=0.3)
        # (midpoint 4.48: scene and script rows in place)
        a2_at(self, 4.62)                                       # "placeholder art"
        l3 = row_label("placeholder art", YS[2])
        a3 = a2_img("a2_clawd_idle.png", h=0.9, at=(X_ART + 0.7, YS[2]))
        self.play(FadeIn(l3), FadeIn(a3, scale=0.9), run_time=0.3)
        # 4 repeated variants: real gallery frames
        a2_at(self, 5.55)                                       # "repeated variants"
        l4 = row_label("repeated variants", YS[3])
        a4 = Group(*[a2_img(f"a2_clawd_{n}.png", h=0.9, at=(X_ART + 0.7 + 1.5 * i, YS[3])) for i, n in enumerate(("bounce", "wave", "run"))])
        self.play(FadeIn(l4), LaggedStart(*[FadeIn(im, scale=0.9) for im in a4], lag_ratio=0.3), run_time=0.9)
        # 5 tests: a real receipt line
        a2_at(self, 6.5)                                        # "tests"
        l5 = row_label("tests", YS[4])
        a5 = VGroup(mono('"failures": 0', YS[4] + 0.25), mono('"status": "PASS"', YS[4] - 0.25))
        self.play(FadeIn(l5), FadeIn(a5, shift=RIGHT * 0.2), run_time=0.3)
        a2_at(self, 7.4)                                        # "from a clear description"
        src = a2_lab("real files, Claude Walker game", 3.2, -3.0, 32)
        self.play(FadeIn(src), run_time=0.4)
        done(self)


# ── B10 · you decide what the game is for and who for; the A.I. builds any version flawlessly, the wrong one too ────────────
class B10_YouDecide(Scene):
    def construct(self):
        a2_at(self, 0.9)                                        # "You decide what the game is for"
        who = a2_portrait(-5.3, 2.2, 1.5)
        pg = RoundedRectangle(width=9.9, height=2.75, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([0.95, 1.85, 0])
        hd = M("GAME-BRIEF.md", 32)
        hd.move_to([-3.8 + hd.width / 2, 2.95, 0])

        def tl(s, y):
            t = T(s, 34)
            t.move_to([-3.8 + t.width / 2, y, 0])
            return t
        q1 = VGroup(tl("Clawd, a coding agent, goes through an", 2.4), tl("agentic loop on every level: …", 1.95))
        self.play(FadeIn(who, scale=0.85), Create(pg), FadeIn(hd), run_time=0.5)
        self.play(FadeIn(q1, shift=RIGHT * 0.2), run_time=0.4)
        a2_at(self, 2.3)                                        # "and who it is for"
        q2 = VGroup(tl("keyboard players who know what", 1.35), tl("a coding agent is, …", 0.9))
        self.play(FadeIn(q2, shift=RIGHT * 0.2), run_time=0.4)
        # (midpoint 4.27: the brief's two real lines, you at the left; rows start landing after)
        a2_at(self, 3.7)                                        # "an A.I. will build any version you hand it"
        rows = VGroup()
        labs = ["(a) undo most recent task, station re-reachable", "(b) undo becomes a 2 s freeze", "(c) malware is a plain hazard, no undo"]
        ys = [-0.4, -1.25, -2.1]
        checks = []
        for lab, y in zip(labs, ys):
            r = RoundedRectangle(width=10.5, height=0.8, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([0.95, y, 0])
            t = T(lab, 34)
            t.move_to([-4.1 + t.width / 2, y, 0])
            rows.add(VGroup(r, t))
        self.play(FadeIn(rows[0], shift=UP * 0.2), run_time=0.35)
        a2_at(self, 4.5)
        self.play(FadeIn(rows[1], shift=UP * 0.2), run_time=0.3)
        a2_at(self, 5.0)
        self.play(FadeIn(rows[2], shift=UP * 0.2), run_time=0.3)
        a2_at(self, 5.95)                                       # "flawlessly": each version builds, each is checked off
        cks = [check(5.6, y, s=0.2, color=INK, w=7) for y in ys]
        self.play(LaggedStart(*[Create(c) for c in cks], lag_ratio=0.35), run_time=0.9)
        a2_at(self, 7.1)                                        # "including the wrong one"
        q = a2_lab("which is wrong?", 0.95, -3.0, 34)
        dot = Dot([-5.0, ys[0], 0], radius=0.1, color=TERRA)
        self.play(FadeIn(q), FadeIn(dot), run_time=0.3)
        self.play(dot.animate.move_to([-5.0, ys[1], 0]), run_time=0.3)
        self.play(dot.animate.move_to([-5.0, ys[2], 0]), run_time=0.3)
        done(self)


# ── B11 · you hear that something is wrong before any check says so: three drawn examples ──────────────────────────────────
def a2_clawd_sprite(x, y, h=0.55):
    """A drawn player (grey body, ink outline): a stand-in for the game's hero, so a drawn example never wears the real art."""
    w = h * 1.0
    body = Rectangle(width=w * 0.7, height=h * 0.6, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + h * 0.1, 0])
    arms = Rectangle(width=w, height=h * 0.2, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + h * 0.05, 0])
    legs = VGroup(*[Line([x + dx, y - h * 0.2, 0], [x + dx, y - h * 0.5, 0], color=INK, stroke_width=6) for dx in (-0.2 * w, -0.07 * w, 0.07 * w, 0.2 * w)])
    return VGroup(arms, body, legs)


class B11_HearWrong(Scene):
    def construct(self):
        a2_at(self, 0.2)                                        # "You hear that something is wrong"
        who = a2_portrait(-5.45, 2.45, 1.3)
        arcs = [Arc(radius=r, start_angle=-PI / 4, angle=PI / 2, color=DIM, stroke_width=5, arc_center=[-4.6, 2.45, 0]) for r in (0.4, 0.8, 1.2)]
        self.play(FadeIn(who, scale=0.85), run_time=0.3)
        for a in arcs:
            self.play(Create(a), run_time=0.22)
        a2_at(self, 1.5)                                        # "before any check says so": the check lamp stays unlit
        lamp = Circle(radius=0.24, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([-1.9, 2.45, 0])
        lamp_l = a2_lab("check: not yet", 0.2, 2.45, 34)
        self.play(Create(lamp), FadeIn(lamp_l), run_time=0.4)
        # panels
        PW, PH, PY = 3.8, 3.2, -0.45
        cx = [-4.2, 0.0, 4.2]
        pans = [Rectangle(width=PW, height=PH, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, PY, 0]) for x in cx]
        ex_l = a2_lab("drawn examples", 0.0, -2.85, 32)
        # 1 · a jump that cannot clear the gap
        a2_at(self, 2.75)                                       # "a jump that cannot clear the gap"
        gx = cx[0]
        ground_l = Line([gx - 1.8, -1.0, 0], [gx - 0.55, -1.0, 0], color=INK, stroke_width=6)
        ground_r = Line([gx + 0.95, -1.0, 0], [gx + 1.8, -1.0, 0], color=INK, stroke_width=6)
        clawd = a2_clawd_sprite(gx - 1.2, -0.65, 0.55)
        self.play(Create(pans[0]), Create(ground_l), Create(ground_r), FadeIn(clawd), FadeIn(ex_l), run_time=0.5)
        arc = ArcBetweenPoints(np.array([gx - 0.95, -0.5, 0.0]), np.array([gx + 0.05, -1.15, 0.0]), angle=-PI / 1.9)
        arc.set_stroke(INK, 5)
        self.play(Create(arc), run_time=0.7)
        land = Dot([gx + 0.05, -1.15, 0], radius=0.11, color=TERRA)
        cap1 = a2_lab("gap too wide", gx, -1.7, 34)
        self.play(FadeIn(land), FadeIn(cap1), run_time=0.3)
        # (midpoint 4.3: the short jump, its landing in the gap, the caption)
        # 2 · an enemy that cannot be dodged
        a2_at(self, 4.75)                                       # "an enemy that cannot be dodged"
        ex = cx[1]
        floor = Line([ex - 1.8, -1.0, 0], [ex + 1.8, -1.0, 0], color=INK, stroke_width=6)
        roof = Line([ex - 1.8, 0.75, 0], [ex + 1.8, 0.75, 0], color=INK, stroke_width=6)
        clawd2 = a2_clawd_sprite(ex - 1.2, -0.65, 0.55)
        self.play(Create(pans[1]), Create(floor), Create(roof), FadeIn(clawd2), run_time=0.4)
        spikes = VGroup(*[Polygon([ex + 0.5, y, 0], [ex + 0.5, y + 0.35, 0], [ex + 0.05, y + 0.175, 0], fill_color=BAR2, fill_opacity=1,
                                  stroke_color=INK, stroke_width=4) for y in (-1.0, -0.65, -0.3, 0.05, 0.4)])
        self.play(LaggedStart(*[GrowFromCenter(sp) for sp in spikes], lag_ratio=0.15), run_time=0.7)
        cap2 = a2_lab("no way past", ex, -1.7, 34)
        self.play(FadeIn(cap2), run_time=0.25)
        # 3 · a number that is too perfect
        a2_at(self, 6.4)                                        # "a number that is too perfect"
        nx = cx[2]
        self.play(Create(pans[2]), run_time=0.3)
        big = T("100%", 90).move_to([nx, -0.15, 0])
        cap3 = a2_lab("too perfect", nx, -1.7, 34)
        self.play(FadeIn(big, scale=0.9), run_time=0.4)
        self.play(FadeIn(cap3), run_time=0.25)
        done(self)


# ── B12 · you choose the checks, and you look at the real running game, not the report ────────────────────────────────────
class B12_RealGame(Scene):
    def construct(self):
        who = a2_portrait(-5.3, 0.6, 1.5)
        ids = ["launch-grounded", "speed-cap", "coyote-5", "respawn"]
        rows = VGroup(*[M(s, 32) for s in ids])
        for i, r in enumerate(rows):
            r.move_to([-3.4 + r.width / 2, 1.5 - 0.75 * i, 0])
        self.add(who)
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=0.7)
        a2_at(self, 0.75)                                       # "which checks matter"
        t1 = check(-3.7, 0.0, s=0.18, color=INK, w=7)
        t2 = check(-3.7, -0.75, s=0.18, color=INK, w=7)
        self.play(Create(t1), Create(t2), run_time=0.4)
        # (midpoint 2.57: the chosen checks, you; the real game lands just after, so no real pixels are in the GATE T frame)
        a2_at(self, 2.65)                                       # "the real running game"
        win = a2_window(0.7, 0.2, 6.5, 3.66)
        clip = a2_clip(3.66, (0.7, 0.2), start=0.5)
        self.play(FadeOut(rows), FadeOut(t1), FadeOut(t2), FadeIn(clip), Create(win), run_time=0.3)
        real_l = a2_lab("real running game", 0.7, -2.15, 34)
        look = Arrow([-4.45, 0.5, 0], [-2.9, 0.3, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        self.play(GrowArrow(look), FadeIn(real_l), run_time=0.3)
        a2_at(self, 3.55)                                       # "not the report about it"
        pg = RoundedRectangle(width=1.5, height=2.3, corner_radius=0.08, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([5.45, 0.3, 0])
        pl = VGroup(*[Line([4.9, y, 0], [6.0, y, 0], color=GHOST, stroke_width=7) for y in (0.9, 0.5, 0.1, -0.3)])
        rp_l = a2_lab("report", 5.45, -1.2, 34)
        cross = a2_x(5.45, 1.8, s=0.22, w=8)
        self.play(Create(pg), FadeIn(pl), FadeIn(rp_l), Create(cross), run_time=0.5)
        done(self)


# ── B13 · you judge fun, fairness and meaning: the real game plays, the questions stay open ───────────────────────────────
class B13_TasteIsYours(Scene):
    def construct(self):
        qs = ["fun?", "fair?", "what I meant?"]
        ys = [1.9, 1.05, 0.2]
        who = a2_portrait(-3.95, -1.75, 1.7)
        rings = [DashedVMobject(Circle(radius=0.2).move_to([-5.6, y, 0]), num_dashes=12).set_stroke(DIM, 5) for y in ys]
        words = []
        for s_, y in zip(qs, ys):
            t = T(s_, 40)
            t.move_to([-5.1 + t.width / 2, y, 0])
            words.append(t)
        a2_at(self, 0.75)                                       # "fun"
        self.play(Create(rings[0]), FadeIn(words[0]), run_time=0.3)
        a2_at(self, 1.75)                                       # "fair"
        self.play(Create(rings[1]), FadeIn(words[1]), run_time=0.3)
        a2_at(self, 2.55)                                       # "means what you intended"
        self.play(Create(rings[2]), FadeIn(words[2]), FadeIn(who, scale=0.85), run_time=0.4)
        # (midpoint 3.33: three open questions and you; the real game lands just after, so no real pixels are in the GATE T frame)
        a2_at(self, 3.45)
        win = a2_window(2.3, 0.45, 6.5, 3.66)
        clip = a2_clip(3.66, (2.3, 0.45), start=3.6)
        self.play(FadeIn(clip), Create(win), run_time=0.3)
        a2_at(self, 4.35)                                       # "Taste and intent are yours"
        ar = Arrow([-5.2, -0.5, 0], [-4.45, -1.2, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        mine = a2_lab("yours", -2.3, -1.75, 40)
        self.play(GrowArrow(ar), FadeIn(mine), run_time=0.4)
        dot = Dot([-5.6, ys[0], 0], radius=0.1, color=TERRA)
        self.play(FadeIn(dot), run_time=0.2)
        self.play(dot.animate.move_to([-5.6, ys[1], 0]), run_time=0.25)
        self.play(dot.animate.move_to([-5.6, ys[2], 0]), run_time=0.25)
        done(self)


# ── B14 · you sign what ships; the A.I. faces no consequence (real status file: every signature slot is empty) ───────────
class B14_YouSign(Scene):
    def construct(self):
        a2_at(self, 0.05)                                       # "And you sign what ships"
        pg = RoundedRectangle(width=9.0, height=3.5, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-1.55, 0.45, 0])
        hd = M("DESIGN-STATUS.json", 32)
        hd.move_to([-5.8 + hd.width / 2, 1.85, 0])
        src = ['"vision":  {"signed_by": null, …}', '"systems": {"signed_by": null, …}', '"world":   {"signed_by": null, …}', '"scope":   {"signed_by": null, …}']
        rows = VGroup(*[M(t, 32) for t in src])
        ys = [1.1, 0.5, -0.1, -0.7]
        for r, y in zip(rows, ys):
            r.move_to([-5.8 + r.width / 2, y, 0])
        self.play(Create(pg), FadeIn(hd), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=0.9)
        note = T("“… Gates are signed by humans only.”", 34).move_to([-1.55, -2.0, 0])
        a2_at(self, 1.2)                                        # "The A.I. faces no consequence"
        dot = Dot([-6.15, ys[0], 0], radius=0.1, color=TERRA)
        self.play(FadeIn(dot), FadeIn(note), run_time=0.3)
        for y in ys[1:]:
            self.play(dot.animate.move_to([-6.15, y, 0]), run_time=0.35)
        # (the slots stay empty: nobody has signed)
        a2_at(self, 3.0)                                        # "You do"
        who = a2_portrait(4.75, 1.6, 1.5)
        line = Line([3.4, -0.5, 0], [6.1, -0.5, 0], color=INK, stroke_width=5)
        sig = ParametricFunction(lambda t: np.array([3.55 + 2.4 * t, 0.0 + 0.22 * np.sin(9 * t) * (1 - 0.4 * t) + 0.08 * np.sin(23 * t), 0]),
                                 t_range=[0.0, 1.0], color=INK, stroke_width=6)
        sg_l = a2_lab("sign", 4.75, -1.05, 36)
        self.play(FadeIn(who, scale=0.85), Create(line), FadeIn(sg_l), run_time=0.35)
        self.play(Create(sig), run_time=0.6)
        done(self)


# ── B15 · an honest note: medicine, law and software come from teaching people to supervise AI; games are our own extension ──
def a2_icon(name, x, y, h=1.3):
    ic = SVGMobject(A2P + f"a2_icon_{name}.svg")
    ic.set_stroke(INK, width=6).set_fill(opacity=0)
    ic.set_height(h)
    ic.move_to([x, y, 0])
    return ic


class B15_HonestNote(Scene):
    def construct(self):
        a2_at(self, 0.1)                                        # "One honest note"
        note = T("one honest note", 40)
        note.move_to([-5.9 + note.width / 2, 3.0, 0])
        card = RoundedRectangle(width=12.0, height=3.5, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([0, 0.85, 0])
        self.play(FadeIn(note), Create(card), run_time=0.5)
        xs = [-4.1, -1.35, 1.4]
        names = [("stethoscope", "medicine"), ("gavel", "law"), ("terminal", "software")]
        icons, labs = [], []
        for (ic, lab), x, t in zip(names, xs, (3.9, 4.75, 5.15)):
            a2_at(self, t - 0.2 if t > 4 else t)                # medicine, law, software
            i = a2_icon(ic, x, 1.35, 1.2)
            l = a2_lab(lab, x, 0.25, 36)
            self.play(FadeIn(i, scale=0.8), FadeIn(l), run_time=0.3)
            icons.append(i)
        # (midpoint 5.73: three icons, three words)
        a2_at(self, 6.35)                                       # "Games are where this course applies them"
        g = a2_icon("gamepad-2", 4.15, 1.35, 1.2)
        g_l = a2_lab("games", 4.15, 0.25, 36)
        fence = DashedVMobject(RoundedRectangle(width=2.3, height=2.4, corner_radius=0.2).move_to([4.15, 0.85, 0]), num_dashes=40).set_stroke(DIM, 5)
        self.play(FadeIn(g, scale=0.8), FadeIn(g_l), Create(fence), run_time=0.5)
        a2_at(self, 8.8)                                        # "That application is ours"
        ours = a2_lab("ours", 4.15, -1.7, 38)
        od = Dot([3.45, -1.7, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(ours), FadeIn(od), run_time=0.3)
        a2_at(self, 9.8)                                        # "you will be testing it"
        who = a2_portrait(-1.2, -2.15, 1.2)
        arr = Arrow([-0.45, -2.0, 0], [3.0, -1.72, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        t_l = a2_lab("to be tested", 1.45, -2.85, 34)
        self.play(FadeIn(who, scale=0.85), GrowArrow(arr), FadeIn(t_l), run_time=0.5)
        done(self)
