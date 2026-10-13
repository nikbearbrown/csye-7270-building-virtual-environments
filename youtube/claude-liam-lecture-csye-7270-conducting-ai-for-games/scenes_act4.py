"""ACT IV · Why You Check the World  (B23-B29, all Manim)

Cast for the act: THE RECEIPT (a saved record, shown as the REAL text of the file, trimmed only by dropping whole lines), THE COUNT
(one bar of frames: filled = saved, dashed = still missing), and THE TWO PANES (what was said / what changed). Every line of file text is
quoted from a real file of walker-jumpman-clawd (see factcheck/act4.md): gallery-two-receipt.json, gallery-two-v2-receipt.json,
inspector-v2-process.json, evidence/clawd/build-manifest.json, CLAWD-STATUS.json, design/decisions.md, and `git diff --stat` / `--numstat`
(re-run by evidence/act4/b26_check.py). B29's moving picture is 12 REAL frames of the Godot capture walker-claude-jumpman-gameplay.mp4
(scripted input, recorded 2026-10-09), cropped by evidence/act4/make_a4_pantry.py.
Pacing: a4_at(t) lands each motion on the real spoken time of a word (faster-whisper, evidence/act4/word_times.json).
"""

A4P = "pantry/"


def a4_at(self, t, lead=0.12):
    """Wait until the clip clock reaches t - lead seconds (t = the real spoken start time of a word)."""
    gap = t - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a4_left(mob, x, y):
    """Place a text left-aligned at x (explicit coordinates; never read back a text's edge)."""
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def a4_card(cx, cy, w, h, dashed=False, color=DIM):
    """An outline-only card (no fill behind text)."""
    r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=4, fill_opacity=0).move_to([cx, cy, 0])
    return DashedVMobject(r, num_dashes=44, dashed_ratio=0.55) if dashed else r


def a4_cross(x, y, s=0.22, w=8):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


def a4_bar(x0, y, w, h, color=BAR1):
    """A filled grey bar whose left end sits at x0 (the count of frames saved)."""
    return Rectangle(width=w, height=h, fill_color=color, fill_opacity=1, stroke_width=0).move_to([x0 + w / 2.0, y, 0])


def a4_gap(x0, y, w, h):
    """The part of the count that is missing: an outline-only dashed box."""
    return a4_card(x0 + w / 2.0, y, w, h, dashed=True)


def a4_lines(rows, x, y0, dy=0.5, size=32):
    """Real file text, one Menlo line per row, left-aligned at x."""
    return VGroup(*[a4_left(M(s, size), x, y0 - i * dy) for i, s in enumerate(rows)])


# ── B23 · ACT TITLE · a receipt that said PASS held 343 of the 540 frames the plan needed ───────────────────────────
class B23_ReceiptSaidPass(Scene):
    def construct(self):
        title = a4_left(T("Why You Check the World", 40), -6.1, 3.0)
        self.add(title)
        card = a4_card(-3.1, 1.05, 6.0, 2.0)
        rows = a4_lines(['"take": "gallery-two",', '"frames": 343,', '"status": "PASS",'], -5.85, 1.5, 0.5)
        lab = a4_left(T("the receipt, as saved", 36), 0.35, 1.6)
        lab2 = a4_left(T("a gallery take, not gameplay", 32), 0.35, 1.05)
        a4_at(self, 4.0)                                                   # "One recording of the game came with a receipt"
        self.play(FadeIn(card), FadeIn(rows), FadeIn(lab), FadeIn(lab2), run_time=0.6)
        a4_at(self, 6.14)                                                  # "that said pass"
        ok = check(0.55, 0.4, s=0.28)
        self.play(Create(ok), run_time=0.35)
        a4_at(self, 7.3)                                                   # "It held 343 frames"
        saved = a4_bar(-6.0, -1.3, 343 / 540.0 * 12.0, 0.8)
        n343 = T("343", 72).move_to([-2.2, -2.5, 0])
        s343 = a4_left(T("saved", 36), -1.2, -2.5)
        self.play(GrowFromEdge(saved, LEFT), FadeIn(n343), FadeIn(s343), run_time=0.8)
        a4_at(self, 9.5)                                                   # "The plan needed 540"
        gap = a4_gap(-6.0 + 343 / 540.0 * 12.0, -1.3, 12.0 * 197 / 540.0, 0.8)
        n540 = T("540", 72).move_to([2.9, -2.5, 0])
        s540 = a4_left(T("needed", 36), 3.7, -2.5)
        self.play(Create(gap), FadeIn(n540), FadeIn(s540), run_time=0.7)
        done(self)


# ── B24 · the AI rejected the recording, kept it as evidence, and now requires 600 frames ────────────────────────────
class B24_RejectedKept(Scene):
    def construct(self):
        t1 = a4_left(T("gallery-two", 36), -5.8, 2.2)
        c1 = a4_card(-3.4, 1.0, 4.8, 1.5)
        r1 = a4_lines(['"frames": 343,', '"status": "PASS"'], -5.55, 1.25, 0.5)
        self.add(t1, c1, r1)
        a4_at(self, 1.22)                                                  # "rejected the recording"
        x1 = a4_cross(-5.3, -0.4)
        l1 = a4_left(T("rejected", 36), -4.85, -0.4)
        self.play(Create(x1), FadeIn(l1), run_time=0.4)
        a4_at(self, 2.5)                                                   # "kept it as evidence"
        d1 = Dot([-5.3, -1.2, 0], radius=0.1, color=DIM)
        l2 = a4_left(T("kept as evidence", 36), -4.85, -1.2)
        self.play(GrowFromCenter(d1), FadeIn(l2), run_time=0.4)
        a4_at(self, 3.86)                                                  # "and changed its method"
        arr = Arrow([-0.7, 1.0, 0], [0.8, 1.0, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        t2 = a4_left(T("gallery-two-v2", 36), 1.1, 2.2)
        c2 = a4_card(3.5, 1.0, 4.8, 1.5)
        r2 = a4_lines(['"frames": 600,', '"status": "PASS"'], 1.35, 1.25, 0.5)
        self.play(Create(arr), FadeIn(t2), FadeIn(c2), FadeIn(r2), run_time=0.6)
        a4_at(self, 5.3)                                                   # "to require 600 frames"
        n600 = T("600", 72).move_to([2.4, -0.6, 0])
        s600 = a4_left(T("frames required", 36), 3.3, -0.65)
        self.play(FadeIn(n600, shift=UP * 0.15), FadeIn(s600), run_time=0.5)
        done(self)


# ── B25 · exit code 0, no completion receipt, 416 of 600 frames ──────────────────────────────────────────────────────
class B25_ExitCodeZero(Scene):
    def construct(self):
        a4_at(self, 0.74)                                                  # "ended with exit code 0"
        lab = a4_left(T("process record", 36), -6.0, 2.85)
        card = a4_card(-3.8, 1.9, 4.4, 0.9)
        row = a4_left(M('"exit_code": 0,', 32), -5.75, 1.9)
        self.play(FadeIn(lab), FadeIn(card), FadeIn(row), run_time=0.5)
        a4_at(self, 2.7)                                                   # "the code that means success"
        ok = check(-0.9, 1.9, s=0.28)
        oks = a4_left(T("success", 36), -0.35, 1.9)
        self.play(Create(ok), FadeIn(oks), run_time=0.4)
        a4_at(self, 4.4)                                                   # "no completion receipt"
        page = a4_card(3.6, 1.9, 3.0, 1.4, dashed=True)
        pl = T("no receipt", 36).move_to([3.6, 0.85, 0])
        self.play(Create(page), FadeIn(pl), run_time=0.5)
        a4_at(self, 5.9)                                                   # "only 416 of 600 frames"
        saved = a4_bar(-6.0, -0.35, 416 / 600.0 * 12.0, 0.7)
        n416 = T("416", 72).move_to([-2.6, -1.4, 0])
        s416 = a4_left(T("saved", 36), -1.8, -1.4)
        self.play(GrowFromEdge(saved, LEFT), FadeIn(n416), FadeIn(s416), run_time=0.55)
        a4_at(self, 7.4)
        gap = a4_gap(-6.0 + 416 / 600.0 * 12.0, -0.35, 12.0 * 184 / 600.0, 0.7)
        n600 = T("600", 72).move_to([3.2, -1.4, 0])
        s600 = a4_left(T("required", 36), 4.0, -1.4)
        self.play(Create(gap), FadeIn(n600), FadeIn(s600), run_time=0.6)
        a4_at(self, 10.1)                                                  # "In the record's own words: exit code 0 did not establish success"
        ring = DashedVMobject(Circle(radius=0.3, stroke_color=DIM, stroke_width=6).move_to([-0.9, 1.9, 0]), num_dashes=14, dashed_ratio=0.55)
        q = T("Exit code zero did not establish success.", 40).move_to([0, -2.55, 0])
        qa = T("the project's own record", 32).move_to([0, -3.05, 0])
        self.play(FadeOut(ok), Create(ring), FadeIn(q), FadeIn(qa), run_time=0.7)
        done(self)


# ── B26 · "byte-identical" was true of one function; the same file changed by 33 lines ──────────────────────────────
# player.gd at the Clawd commit is 93 lines. `func _physics_process(` runs from line 44 to 72 (the record's own slice, 29 lines).
# git diff -U0: lines 4-6 added, 73-91 added, 93 added (23 added) and 10 old lines removed (evidence/act4/b26_check.log).
A4_N, A4_TOP, A4_PITCH = 93, 2.5, 5.1 / 93.0
A4_CHANGED = list(range(4, 7)) + list(range(73, 92)) + [93]


def a4_row_y(k):
    return A4_TOP - (k - 0.5) * A4_PITCH


class B26_OneFunction(Scene):
    def construct(self):
        head = a4_left(M("player.gd", 32), -5.3, 3.0)
        frame = Rectangle(width=3.9, height=5.3, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([-3.35, -0.1, 0])
        rows = VGroup(*[Rectangle(width=3.6 * (0.4 + 0.6 * (((k * 37) % 11) / 11.0)), height=0.034, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                        .move_to([-5.15 + 1.8 * (0.4 + 0.6 * (((k * 37) % 11) / 11.0)), a4_row_y(k), 0]) for k in range(1, A4_N + 1)])
        self.add(head, frame, rows)
        a4_at(self, 2.4)                                                   # "the physics function"
        sl = VGroup(*[rows[k - 1] for k in range(44, 73)])
        br = VGroup(Line([-1.3, a4_row_y(44) + 0.03, 0], [-1.3, a4_row_y(72) - 0.03, 0], color=INK, stroke_width=5),
                    Line([-1.3, a4_row_y(44) + 0.03, 0], [-1.45, a4_row_y(44) + 0.03, 0], color=INK, stroke_width=5),
                    Line([-1.3, a4_row_y(72) - 0.03, 0], [-1.45, a4_row_y(72) - 0.03, 0], color=INK, stroke_width=5))
        ld = Line([-1.3, -0.65, 0], [-0.7, -0.65, 0], color=INK, stroke_width=5)
        fn = a4_left(M("_physics_process", 32), -0.25, -0.65)
        self.play(*[r.animate.set_fill(DIM) for r in sl], Create(br), Create(ld), FadeIn(fn), run_time=0.7)
        a4_at(self, 4.12)                                                  # "byte-identical"
        bi = a4_left(T("byte-identical", 40), -0.25, -1.4)
        ok = check(2.9, -1.4, s=0.28)
        self.play(FadeIn(bi), Create(ok), run_time=0.5)
        a4_at(self, 5.9)                                                   # "that check compares one function"
        one = a4_left(T("the check reads this one function", 36), -0.25, -2.15)
        self.play(FadeIn(one), run_time=0.4)
        a4_at(self, 7.7)                                                   # "The same file changed by 33 lines"
        ch = VGroup(*[rows[k - 1] for k in A4_CHANGED])
        dots = VGroup(*[Dot([-5.55, a4_row_y(m), 0], radius=0.09, color=TERRA) for m in (5, 82, 93)])
        n33 = T("33", 120).move_to([1.2, 1.75, 0])
        l33 = a4_left(T("lines changed", 36), 2.3, 1.95)
        l23 = VGroup(a4_left(T("23 added", 36), 2.3, 1.4), a4_left(T("10 removed", 36), 2.3, 0.95))
        self.play(*[r.animate.set_fill(DIM) for r in ch], FadeIn(dots), FadeIn(n33), FadeIn(l33), FadeIn(l23), run_time=0.7)
        done(self)


# ── B27 · two panes: what was said / what changed ────────────────────────────────────────────────────────────────────
class B27_SaidVersusChanged(Scene):
    def construct(self):
        pl = a4_card(-3.15, 0.6, 5.5, 3.0)
        pr = a4_card(3.15, 0.6, 5.5, 3.0)
        a4_at(self, 0.35)
        self.play(Create(pl), Create(pr), run_time=0.5)
        a4_at(self, 2.4)                                                   # "A success statement records what was said"
        hl = T("what was said", 38).move_to([-3.15, 2.6, 0])
        tl = a4_lines(['"physics_function":', '"byte-identical"'], -5.65, 0.95, 0.65)
        self.play(FadeIn(hl), FadeIn(tl), run_time=0.5)
        a4_at(self, 4.7)                                                   # "The state records what actually changed"
        hr = T("what changed", 38).move_to([3.15, 2.6, 0])
        tr = a4_lines(['…/player.gd | 33 +-', '+23  -10'], 0.65, 0.95, 0.65)
        ne = VGroup(Line([-0.2, -1.55, 0], [0.2, -1.55, 0], color=INK, stroke_width=8), Line([-0.2, -1.8, 0], [0.2, -1.8, 0], color=INK, stroke_width=8),
                    Line([-0.12, -1.95, 0], [0.12, -1.4, 0], color=INK, stroke_width=8))
        self.play(FadeIn(hr), FadeIn(tr), Create(ne), run_time=0.5)
        a4_at(self, 6.84)                                                  # "You read the state"
        cur = cursor(0.0, -2.2)
        self.add(cur)
        ok = check(5.0, 2.6, s=0.26)
        self.play(cur.animate.move_to([3.4, 0.25, 0]), Create(ok), run_time=0.7)
        done(self)


# ── B28 · the records are the AI's own, no human finding, play-test pending, eight questions open ───────────────────
class B28_NoHumanFinding(Scene):
    def construct(self):
        a4_at(self, 0.12)                                                  # "these records were written by the AI itself"
        pg = Polygon([-5.9, 2.75, 0], [-5.35, 2.75, 0], [-5.15, 2.55, 0], [-5.15, 1.85, 0], [-5.9, 1.85, 0],
                     fill_opacity=0, stroke_color=INK, stroke_width=4)
        pls = VGroup(*[Line([-5.7, y, 0], [-5.35, y, 0], color=GHOST, stroke_width=4) for y in (2.2, 2.05)])
        w1 = a4_left(T("written by the AI", 38), -4.8, 2.3)
        self.play(Create(pg), Create(pls), FadeIn(w1), run_time=0.5)
        a4_at(self, 3.44)                                                  # "look for the human finding"
        w2 = a4_left(T("human finding", 38), -6.0, 1.05)
        slot = a4_card(-0.4, 1.05, 4.6, 0.9, dashed=True)
        self.play(FadeIn(w2), Create(slot), run_time=0.5)
        a4_at(self, 5.3)                                                   # "There is none"
        none = a4_left(T("none recorded", 38), 2.2, 1.05)
        self.play(FadeIn(none), run_time=0.35)
        a4_at(self, 6.04)                                                  # "The human play-test is still marked pending"
        hp = a4_left(M('"human_playtest": "pending"', 32), -6.0, -0.35)
        self.play(FadeIn(hp, shift=RIGHT * 0.2), run_time=0.45)
        a4_at(self, 8.62)                                                  # "Eight design questions are still open"
        cells = VGroup(*[a4_card(-5.55 + 0.65 + i * 1.4, -1.75, 1.3, 0.8) for i in range(8)])
        qs = VGroup(*[M(f"Q-0{i + 1}", 32).move_to([-5.55 + 0.65 + i * 1.4, -1.75, 0]) for i in range(8)])
        self.play(LaggedStart(*[AnimationGroup(Create(c), FadeIn(q)) for c, q in zip(cells, qs)], lag_ratio=0.25), run_time=1.5)
        a4_at(self, 10.64)                                                 # "each with a person's name on it"
        ow = T("every one: owner Bear, status Open", 36).move_to([0, -2.75, 0])
        self.play(FadeIn(ow), run_time=0.45)
        done(self)


# ── B29 · HINGE · the machine says passed; a person says whether it is fun ──────────────────────────────────────────
class B29_PassedVersusFun(Scene):
    def construct(self):
        # GATE T reads the flat terracotta Clawd (a mascot wider than 1.5x its height) as accent text at the 50% frame, so the real
        # capture window lands AFTER the midpoint (3.9 s of 7.64 s); before it the frame holds the machine's side.
        frames = [ImageMobject(A4P + f"a4_g{i:02d}.png").set_width(5.6).move_to([3.3, 1.0, 0]) for i in range(12)]
        for f in frames:
            f.set_opacity(0.0)
            self.add(f)
        box = Rectangle(width=5.6, height=5.6 * 530 / 1120.0, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([3.3, 1.0, 0])
        cap1 = T("scripted input", 32).move_to([3.3, -0.6, 0])
        cap2 = T("recorded 2026-10-09", 32).move_to([3.3, -1.0, 0])
        mid = Line([0.0, 3.0, 0], [0.0, -3.0, 0], color=GHOST, stroke_width=5)
        live = [False]
        tm = [0.0]

        def upd(_m, dt):
            tm[0] += dt
            i = int(tm[0] * 10) % 12
            for j, f in enumerate(frames):
                f.set_opacity(1.0 if (live[0] and j == i) else 0.0)
        frames[0].add_updater(upd)
        self.play(Create(mid), run_time=0.3)
        a4_at(self, 2.5)                                                   # "The machine can tell you 100 things passed"
        hm = T("the machine", 40).move_to([-3.0, 2.9, 0])
        dots = VGroup(*[Dot([-4.35 + (j % 10) * 0.3, 1.9 - (j // 10) * 0.3, 0], radius=0.07, color=BAR1) for j in range(100)])
        self.play(FadeIn(hm), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.012), run_time=1.1)
        a4_at(self, 3.95)                                                  # "passed" (the real game starts running)
        ps = T("passed", 44).move_to([-3.0, -1.45, 0])
        ok = check(-4.4, -1.45, s=0.3)
        ex = T("an example: 100 checks", 32).move_to([-3.0, -2.05, 0])
        rt = guard(self, 0.5)                                              # keep the capture window off the midpoint frame
        live[0] = True
        self.play(Create(box), FadeIn(cap1), FadeIn(cap2), FadeIn(ps), Create(ok), FadeIn(ex), run_time=rt)
        a4_at(self, 4.9)                                                   # "Only a person can say whether it is fun"
        hp = T("a person", 40).move_to([3.3, 2.9, 0])
        fun = T("fun?", 60).move_to([2.6, -2.2, 0])
        ring = DashedVMobject(Circle(radius=0.55, stroke_color=DIM, stroke_width=6).move_to([4.5, -2.2, 0]), num_dashes=18, dashed_ratio=0.55)
        self.play(FadeIn(hp), FadeIn(fun), Create(ring), run_time=0.7)
        done(self)
