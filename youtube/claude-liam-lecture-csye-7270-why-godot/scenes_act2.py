"""ACT II · A Scene Is a Text File  (B06–B14, all Manim)

One cast for the act: THE REAL TEXT of the real runs, shown as recorded text in plain outlined windows on the cream stage
(never as a live screen, never mocked): the real pong.tscn (EVID/godot-evidence/part2/pong.tscn.before), the real `file` output
(evidence/act2/file-check.txt, run 2026-10-09 on this Mac), the real tool calls of the recorded run
(part2/04-tool-calls-and-results.txt), the real independent checks (part2/independent-checks.txt), the real diff (part2/pong.tscn.diff)
and Godot's own re-saved copy (part2/pong.resaved-by-godot.tscn). Real game: the Walker Pong capture (godot-captures/walker-pong,
scripted input, recorded 2026-10-09), frames in pantry/a2_pong_NN.png (8 fps, game area only: crop 1728x1080 of the 1920x1080 clip).
Every line is verbatim; where a line is shortened the cut is shown with a visible ellipsis (Menlo 32 is 0.25 units per character,
so a 69-character node line cannot fit beside anything else). Pacing: cues are the real spoken word times (faster-whisper,
evidence/act2/word_times.json) through a2_at().
GATE T: the dark Pong window is small and sits clear of text; the terracotta Dot is only ever a dot (never text, never a stroke).
"""
from PIL import Image as _A2Img

A2P = "pantry/"


def a2_at(self, t):
    """Wait until the clip clock reaches t seconds (the real spoken time of a word, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a2_l(s, x, y, size=34, color=INK):
    """Serif label whose LEFT edge is at x."""
    return T(s, size, color).move_to([x, y, 0], aligned_edge=LEFT)


def a2_c(s, x, y, size=34, color=INK):
    """Serif label centred on x."""
    return T(s, size, color).move_to([x, y, 0])


def a2_m(s, x, y, size=32, color=INK):
    """Menlo text whose first character CELL starts at x (0.25 units per character at size 32), on a common baseline
    (hidden bars at both ends give every row the same ascender/descender box)."""
    t = M("|" + s + "|", size, color)
    t[0].set_opacity(0)
    t[-1].set_opacity(0)
    return t.move_to([x - 0.243 * size / 32 + t.width / 2, y, 0])


def a2_win(x0, x1, y0, y1, color=DIM, sw=4):
    """Outline-only window (no fill behind text)."""
    return RoundedRectangle(width=x1 - x0, height=y1 - y0, corner_radius=0.12, stroke_color=color, stroke_width=sw,
                            fill_opacity=0).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def a2_x(cx, cy, s=0.3, color=INK, sw=8):
    return VGroup(Line([cx - s, cy + s, 0], [cx + s, cy - s, 0], color=color, stroke_width=sw),
                  Line([cx - s, cy - s, 0], [cx + s, cy + s, 0], color=color, stroke_width=sw))


def a2_page(cx, cy, w=1.0, h=1.3):
    """A file page: card outline, three ghost text lines."""
    pg = RoundedRectangle(width=w, height=h, corner_radius=0.06, fill_color=CARD, fill_opacity=1, stroke_color=INK,
                          stroke_width=4).move_to([cx, cy, 0])
    ls = VGroup(*[Line([cx - w * 0.3, cy + h * f, 0], [cx + w * 0.3, cy + h * f, 0], color=GHOST, stroke_width=6)
                  for f in (0.25, 0.05, -0.15)])
    return VGroup(pg, ls)


def a2_clip(prefix, n, fps, cx, cy, w):
    """The real capture as stepped frames (pantry/<prefix>NN.png), advancing in scene time through an updater
    (frames are read lazily; a missing file just leaves the first frame, so Gate A's pantry-less copy still builds)."""
    im = ImageMobject(f"{A2P}{prefix}01.png")
    im.set_width(w)
    im.move_to([cx, cy, 0])
    im.a2 = [0.0, {}]

    def upd(m, dt):
        m.a2[0] += dt
        i = int(m.a2[0] * fps) % n + 1
        try:
            if i not in m.a2[1]:
                m.a2[1][i] = np.array(_A2Img.open(f"{A2P}{prefix}{i:02d}.png").convert("RGBA"))
            m.pixel_array = m.a2[1][i]
        except Exception:
            pass
    im.add_updater(upd)
    return im


def a2_pong_clip(cx, cy, w):
    return a2_clip("a2_pong_", 64, 8.0, cx, cy, w)


# ── B06 · a scene is a text file: the real pong.tscn beside the real game ──────────────────────────────────────────────
class B06_RealScene(Scene):
    def construct(self):
        title = T("A Scene Is a Text File", 40).move_to([-6.1, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        a2_at(self, 3.0)                                        # "A Godot scene is a text file"
        win = a2_win(-6.1, 3.46, -2.7, 1.5)
        f_l = a2_l("pong.tscn: 103 lines, excerpt", -6.1, 1.95, 34)
        self.play(Create(win), FadeIn(f_l), run_time=0.45)
        rows = [('[node name="Left" type="Area2D"…', 1.08), ('modulate = Color(0, 1, 1, 1)', 0.62),
                ('position = Vector2(67.6285, 192.594)', 0.16), ('script = ExtResource("1")', -0.30),
                ('[node name="Ball" type="Area2D"…', -1.22), ('position = Vector2(320.5, 191.124)', -1.68),
                ('script = ExtResource("4")', -2.14)]
        R = [a2_m(s, -5.8, y) for s, y in rows]
        a2_at(self, 3.45)
        self.play(LaggedStart(*[FadeIn(r) for r in R[:4]], lag_ratio=0.35), run_time=1.0)
        a2_at(self, 5.0)                                        # "This is a real one, from a Pong game"
        pong = a2_pong_clip(5.0, -1.55, 2.3)
        p_l = a2_c("Pong game", 5.0, -2.65, 34)
        p_s = a2_c("scripted play", 5.0, -3.1, 32, DIM)
        self.play(FadeIn(pong), FadeIn(p_l), FadeIn(p_s), LaggedStart(*[FadeIn(r) for r in R[4:]], lag_ratio=0.3), run_time=0.7)
        # (midpoint: the real file excerpt, the running game, both labelled: a still)
        a2_at(self, 7.2)                                        # "Every object in the game is a few plain lines"
        b1 = Line([3.75, 1.3, 0], [3.75, 0.86, 0], color=DIM, stroke_width=6)
        b2 = Line([3.75, 0.5, 0], [3.75, -0.5, 0], color=DIM, stroke_width=6)
        self.play(Create(b1), Create(b2), run_time=0.5)
        a2_at(self, 9.55)                                       # "its name, its type"
        n_l = a2_l("name, type", 4.0, 1.08, 34)
        self.play(FadeIn(n_l), run_time=0.3)
        a2_at(self, 10.65)                                      # "its settings"
        s_l = a2_l("settings", 4.0, 0.0, 34)
        self.play(FadeIn(s_l), run_time=0.3)
        done(self)


# ── B07 · scripts, settings, scenes: all plain text, as the file command reports ─────────────────────────────────────────
class B07_FileCommand(Scene):
    def construct(self):
        xs = (-5.0, -2.6, -0.2)
        pg = [a2_page(x, 1.85) for x in xs]
        names = ["scripts", "settings", "scenes"]
        labs = [a2_c(n, x, 0.88, 34) for n, x in zip(names, xs)]
        ticks = [check(x, 1.78, s=0.2, color=INK, w=7) for x in xs]
        self.add(pg[0], labs[0])
        a2_at(self, 0.2)                                        # "The scripts are text"
        self.play(Create(ticks[0]), run_time=0.3)
        a2_at(self, 1.1)                                        # "the project's settings are text"
        self.play(FadeIn(pg[1]), FadeIn(labs[1]), run_time=0.3)
        self.play(Create(ticks[1]), run_time=0.25)
        a2_at(self, 2.0)                                        # "text"
        self.play(FadeIn(pg[2]), FadeIn(labs[2]), run_time=0.3)
        self.play(Create(ticks[2]), run_time=0.25)
        a2_at(self, 2.6)                                        # "On this Mac, the file command"
        win = a2_win(-6.1, 6.1, -2.7, 0.3)
        rec = a2_c("recorded on this Mac, 2026-10-09", 0.0, -3.0, 32, DIM)
        self.play(Create(win), FadeIn(rec), run_time=0.4)
        cmd = a2_m("$ file game/main.tscn ui/hud.gd project.godot", -5.8, -0.2)
        self.play(FadeIn(cmd), run_time=0.25)
        out = [a2_m("game/main.tscn: ASCII text", -5.8, -0.8), a2_m("ui/hud.gd:      ASCII text", -5.8, -1.4),
               a2_m("project.godot:  ASCII text", -5.8, -2.0)]
        self.play(LaggedStart(*[FadeIn(o) for o in out], lag_ratio=0.5), run_time=0.7)
        # (midpoint: the three file kinds ticked, the command and its three real lines: a still)
        a2_at(self, 4.95)                                       # "every script and scene file"
        hero = T("13 of 13", 72).move_to([4.1, 2.1, 0])
        c1, c2 = a2_c("script and scene files", 4.1, 1.4, 32), a2_c("read as ASCII text", 4.1, 0.9, 32)
        cks = [check(1.3, y, s=0.18, color=INK, w=7) for y in (-0.8, -1.4, -2.0)]
        self.play(FadeIn(hero), FadeIn(c1), FadeIn(c2), LaggedStart(*[Create(c) for c in cks], lag_ratio=0.3), run_time=0.8)
        done(self)


# ── B08 · no bridge: the agent reads a file, edits a file, and the diff shows what changed ─────────────────────────────
class B08_NoBridge(Scene):
    def construct(self):
        ai_box = RoundedRectangle(width=2.8, height=1.3, corner_radius=0.14, stroke_color=INK, stroke_width=5,
                                  fill_opacity=0).move_to([-4.6, 1.3, 0])
        ai_t = T("A. I.", 44).move_to([-4.6, 1.3, 0])
        page = a2_page(0.6, 1.3, 1.8, 2.4)
        pg_l = a2_c("pong.tscn", 0.6, 2.85, 36)
        self.add(ai_box, ai_t, page, pg_l)
        a2_at(self, 1.0)                                        # "no special bridge"
        br = DashedVMobject(RoundedRectangle(width=1.9, height=1.1, corner_radius=0.1).move_to([-1.75, 1.3, 0]),
                            num_dashes=24).set_stroke(DIM, 5)
        ring = Circle(radius=0.78, stroke_color=INK, stroke_width=7).move_to([-1.75, 1.3, 0])
        bar = Line([-2.30, 1.85, 0], [-1.20, 0.75, 0], color=INK, stroke_width=7)
        b_l = a2_c("bridge", -1.75, 2.55, 36)
        self.play(Create(br), Create(ring), Create(bar), FadeIn(b_l), run_time=0.6)
        a2_at(self, 2.85)                                       # "to read your game": the bridge goes
        self.play(FadeOut(br), FadeOut(ring), FadeOut(bar), FadeOut(b_l), run_time=0.3)
        a2_at(self, 3.2)                                        # "It reads a file"
        rd = Arrow([-0.5, 1.7, 0], [-3.0, 1.7, 0], buff=0, color=INK, stroke_width=7, tip_length=0.28)
        rd_l = a2_c("read", -1.75, 2.3, 40)
        self.play(GrowArrow(rd), FadeIn(rd_l), run_time=0.4)
        a2_at(self, 4.6)                                        # "It edits a file"
        ed = Arrow([-3.0, 0.9, 0], [-0.5, 0.9, 0], buff=0, color=INK, stroke_width=7, tip_length=0.28)
        ed_l = a2_c("edit", -1.75, 0.3, 40)
        self.play(GrowArrow(ed), FadeIn(ed_l), run_time=0.3)
        # (midpoint: the agent and the file with its read and edit arrows: a still)
        a2_at(self, 6.95)                                       # "And your version history"
        dn = Arrow([0.6, 0.05, 0], [0.6, -0.7, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        dn_l = a2_l("version history", 0.95, -0.3, 34)
        win = a2_win(-6.1, 4.5, -3.1, -0.9)
        dif_l = a2_l("diff", 4.8, -2.0, 34)
        self.play(GrowArrow(dn), FadeIn(dn_l), Create(win), FadeIn(dif_l), run_time=0.5)
        rows = [("@@ -95,6 +95,9 @@", -1.3, DIM), (" offset = Vector2(320, 200)", -1.75, DIM),
                ('+[node name="HelloLabel" type="Label"…', -2.2, INK), ('+text = "Hello from a text file"', -2.65, INK)]
        R = [a2_m(s, -5.5, y, 32, c) for s, y, c in rows]
        a2_at(self, 7.5)
        self.play(LaggedStart(*[FadeIn(r) for r in R], lag_ratio=0.3), run_time=1.0)
        a2_at(self, 8.9)                                        # "exactly what changed"
        d1 = Dot([-5.9, -2.2, 0], radius=0.09, color=TERRA)
        d2 = Dot([-5.9, -2.65, 0], radius=0.09, color=TERRA)
        self.play(FadeIn(d1), FadeIn(d2), run_time=0.3)
        done(self)


# ── B09 · the recorded run: one job, four tools, nothing else ──────────────────────────────────────────────────────────
class B09_TheJob(Scene):
    def construct(self):
        hdr = a2_l("recorded run: a Claude Code subagent", -6.1, 2.9, 34)
        self.add(hdr)
        a2_at(self, 1.2)                                        # "A fresh Claude Code agent"
        win = a2_win(-6.1, 3.1, -2.4, 1.9)
        w_l = a2_l("the job, from the real prompt (excerpt)", -6.1, 2.3, 34)
        self.play(Create(win), FadeIn(w_l), run_time=0.45)
        a2_at(self, 2.85)                                       # "a small Pong project"
        pong = a2_pong_clip(4.95, 1.55, 2.3)
        p_l = a2_c("Pong", 4.95, 2.75, 34)
        p_s = a2_c("scripted play", 4.95, 0.45, 32, DIM)
        self.play(FadeIn(pong), FadeIn(p_l), FadeIn(p_s), run_time=0.4)
        rows = [("Task: add a new Label node named", 1.35), ("HelloLabel as a child of the root", 0.7),
                ("node in …/pong.tscn, with its text", 0.05), ('set to "Hello from a text file", by', -0.6),
                ("editing the .tscn text directly.", -1.25)]
        R = [a2_m(s, -5.8, y) for s, y in rows]
        a2_at(self, 4.5)                                        # "one job"
        self.play(FadeIn(R[0]), run_time=0.3)
        a2_at(self, 5.2)
        self.play(FadeIn(R[1]), run_time=0.25)
        a2_at(self, 5.55)
        self.play(FadeIn(R[2]), run_time=0.25)
        # (midpoint: the card with its first three prompt lines and the running Pong: a still)
        a2_at(self, 6.2)
        self.play(FadeIn(R[3]), run_time=0.3)
        a2_at(self, 6.7)
        self.play(FadeIn(R[4]), run_time=0.3)
        a2_at(self, 7.7)                                        # "It could read, edit, write a file, and run Godot"
        names = [("Read", -0.3), ("Edit", -1.1), ("Write", -1.9), ("godot", -2.7)]
        chips = []
        cues = [7.95, 8.5, 8.85, 9.65]
        for (n, y), c in zip(names, cues):
            pill_ = RoundedRectangle(width=2.4, height=0.7, corner_radius=0.35, stroke_color=INK, stroke_width=4,
                                     fill_opacity=0).move_to([4.95, y, 0])
            txt = a2_m(n, 4.95 - len(n) * 0.249 / 2, y)
            dot = Dot([3.9, y, 0], radius=0.09, color=TERRA)
            chips.append((pill_, txt, dot))
        for (pill_, txt, dot), c in zip(chips, cues):
            a2_at(self, c)
            self.play(Create(pill_), FadeIn(txt), FadeIn(dot), run_time=0.25)
        done(self)


# ── B10 · the four real tool calls on a time axis: 23.4 seconds from request to report ───────────────────────────────────
class B10_Timeline(Scene):
    def construct(self):
        hdr = a2_l("recorded run", -6.1, 2.9, 34)
        K = 10.8 / 23.4
        X = lambda s: -5.4 + s * K
        axis = Line([-5.4, -0.4, 0], [5.4, -0.4, 0], color=DIM, stroke_width=5)
        cap = a2_c("seconds since the request, to scale", 0.0, -2.75, 34, DIM)
        d0 = Dot([X(0), -0.4, 0], radius=0.12, color=INK)
        r_l = a2_c("request", -5.0, -0.95, 34)
        self.add(hdr, axis, d0, r_l, cap)
        tool = Dot([X(0), -0.4, 0], radius=0.14, color=TERRA)
        self.add(tool)
        ev = [("Read", 1.7, 0.15, "the scene", 0.75), ("Edit", 4.4, -0.95, "+3 lines", -1.55),
              ("Write", 7.1, 0.15, "check script", 0.75), ("godot", 10.5, -0.95, "no window", -1.55)]
        cues = [0.12, 0.95, 2.3, 3.75]
        for (n, s, y, sub, sy), c in zip(ev, cues):
            a2_at(self, c)
            x = X(s)
            dt = Dot([x, -0.4, 0], radius=0.12, color=INK)
            nm = a2_m(n, x - len(n) * 0.249 / 2, y)
            sb = a2_c(sub, x, sy, 34, DIM)
            self.play(tool.animate.move_to([x, -0.4, 0]), FadeIn(dt), FadeIn(nm), FadeIn(sb), run_time=0.35)
        # (midpoint: four ticks placed, the clock dot at the godot call: a still)
        a2_at(self, 5.9)                                        # "Twenty-three seconds"
        x_end = X(23.4)
        end_d = Dot([x_end, -0.4, 0], radius=0.12, color=INK)
        e_l = a2_c("report", x_end - 0.2, 0.15, 34)
        hero = T("23.4 s", 80).move_to([3.4, 1.9, 0])
        self.play(tool.animate.move_to([x_end, -0.4, 0]), FadeIn(end_d), FadeIn(e_l), FadeIn(hero), run_time=0.9)
        done(self)


# ── B11 · two checks: the agent's own (little), and one written outside the project ────────────────────────────────────
class B11_TwoChecks(Scene):
    def construct(self):
        a_l = a2_l("its own check: the agent wrote it", -6.1, 2.65, 34)
        winA = a2_win(-6.1, 4.3, 1.0, 2.25)
        a1 = a2_m("HelloLabel text: Hello from a text file", -5.8, 1.85)
        a2 = a2_m("PASS", -5.8, 1.35)
        self.add(a_l, winA, a1, a2)
        a2_at(self, 0.75)                                       # "printed pass"
        ckA = check(5.2, 1.7, s=0.2, color=DIM, w=7)
        self.play(Create(ckA), run_time=0.3)
        a2_at(self, 3.7)                                        # "So a second check"
        b_l = a2_l("a second check, written outside the project", -6.1, 0.55, 34)
        winB = a2_win(-6.1, 4.3, -2.95, 0.15)
        self.play(FadeIn(b_l), Create(winB), run_time=0.4)
        rows = [("Original nodes present: 21/21", -0.25), ("Label found: path=HelloLabel…", -0.85),
                ("script on Left: res://logic/paddle.gd", -1.45), ("INDEPENDENT RESULT: PASS", -2.05)]
        R = [a2_m(s, -5.4, y) for s, y in rows]
        a2_at(self, 4.7)
        self.play(LaggedStart(*[FadeIn(r) for r in R], lag_ratio=0.3), run_time=1.0)
        # (midpoint: the agent's own PASS above, the second check's four real lines below: a still)
        a2_at(self, 6.7)                                        # "All twenty-one original nodes still there"
        dot = Dot([-5.75, -0.25, 0], radius=0.09, color=TERRA)
        self.play(FadeIn(dot), run_time=0.2)
        a2_at(self, 8.8)                                        # "Scripts still attached"
        self.play(dot.animate.move_to([-5.75, -1.45, 0]), run_time=0.3)
        a2_at(self, 10.25)                                      # "exactly one new label"
        self.play(dot.animate.move_to([-5.75, -0.85, 0]), run_time=0.3)
        a2_at(self, 11.2)
        ckB = check(5.2, -2.05, s=0.2, color=INK, w=7)
        self.play(Create(ckB), run_time=0.3)
        done(self)


# ── B12 · the control: the same check on the scene before the edit fails ───────────────────────────────────────────────
class B12_Control(Scene):
    def construct(self):
        a_l = a2_l("the same check, on the edited scene", -6.1, 2.65, 34)
        winA = a2_win(-6.1, 3.6, 1.0, 2.25)
        a1 = a2_m("INDEPENDENT RESULT: PASS", -5.8, 1.85)
        a2 = a2_m("exit=0", -5.8, 1.35)
        ckA = check(5.0, 1.65, s=0.2, color=INK, w=7)
        self.add(a_l, winA, a1, a2, ckA)
        a2_at(self, 0.15)                                       # "a control"
        b_l = a2_l("the same check, on the scene before the edit", -6.1, 0.4, 34)
        winB = a2_win(-6.1, 3.6, -2.35, 0.0)
        self.play(FadeIn(b_l), Create(winB), run_time=0.4)
        rows = [("Original nodes present: 21/21", -0.4), ("Expected exactly 1 Label, found 0", -0.95),
                ("INDEPENDENT RESULT: FAIL (1)", -1.5), ("exit=1", -2.0)]
        R = [a2_m(s, -5.8, y) for s, y in rows]
        a2_at(self, 1.4)
        self.play(LaggedStart(*[FadeIn(r) for r in R[:2]], lag_ratio=0.4), run_time=0.7)
        a2_at(self, 2.55)                                       # "fails"
        self.play(FadeIn(R[2]), FadeIn(R[3]), run_time=0.25)
        # (midpoint: the PASS above, the control's lines and its FAIL below: a still)
        cx = a2_x(5.0, -1.15, s=0.3)
        a2_at(self, 3.4)
        self.play(Create(cx), run_time=0.3)
        a2_at(self, 4.0)                                        # "A check that cannot fail proves nothing"
        cap = T("a check that cannot fail proves nothing", 40).move_to([0.0, -2.9, 0])
        self.play(FadeIn(cap), run_time=0.4)
        done(self)


# ── B13 · the one difference: the unique_id the agent left out, and Godot's own save adds ──────────────────────────────
class B13_UniqueId(Scene):
    def construct(self):
        hdr = a2_l("the end of a node's first line, from the real scene files", -6.1, 2.85, 34)
        X0 = -2.3
        o_l = a2_l("another node", -6.1, 1.6, 34)
        o_t = a2_m('…parent="." unique_id=957432765]', X0, 1.6)
        self.add(hdr, o_l, o_t)
        a2_at(self, 0.8)                                        # "the agent left out an identifier"
        g_l = a2_l("the agent's node", -6.1, 0.2, 34)
        g_t = a2_m('…parent="."]', X0, 0.2)
        miss = DashedVMobject(RoundedRectangle(width=4.5, height=0.7, corner_radius=0.08).move_to([3.45, 0.2, 0]),
                              num_dashes=34).set_stroke(DIM, 5)
        m_l = a2_c("missing", 3.45, 0.2, 34, DIM)
        self.play(FadeIn(g_l), FadeIn(g_t), run_time=0.4)
        self.play(Create(miss), FadeIn(m_l), run_time=0.5)
        a2_at(self, 4.8)                                        # "Godot loaded the file anyway"
        ok_l = a2_l("Godot loads it: no warning", X0, -0.55, 34)
        self.play(FadeIn(ok_l), run_time=0.4)
        # (midpoint: another node with its id, the agent's node with the id missing, the loads-it note: a still)
        a2_at(self, 7.0)                                        # "When Godot saved the scene itself"
        s_l = a2_l("re-saved by Godot", -6.1, -1.4, 34)
        s_t = a2_m('…parent="." unique_id=1828201969]', X0, -1.4)
        self.play(FadeIn(s_l), FadeIn(s_t), run_time=0.5)
        s_n = a2_l("a Godot script saved a copy", X0, -2.0, 34, DIM)
        self.play(FadeIn(s_n), run_time=0.3)
        a2_at(self, 8.7)                                        # "it added one"
        d = Dot([3.9, -0.98, 0], radius=0.1, color=TERRA)
        self.play(FadeOut(miss), FadeOut(m_l), FadeIn(d), run_time=0.4)
        a2_at(self, 9.8)                                        # "So the text was valid, but not what the editor would have written"
        cap = T("valid text, not what Godot saves", 40).move_to([0.0, -2.85, 0])
        self.play(FadeIn(cap), run_time=0.4)
        done(self)


# ── B14 · the limits of one run, four rows ────────────────────────────────────────────────────────────────────────────
class B14_Limits(Scene):
    def construct(self):
        hdr = T("The limits", 40).move_to([-6.1, 2.95, 0], aligned_edge=LEFT)
        self.add(hdr)
        ys = [1.7, 0.45, -0.8, -2.05]

        def ring(y):
            return DashedVMobject(Circle(radius=0.2).move_to([-5.85, y, 0]), num_dashes=10).set_stroke(DIM, 6)

        a2_at(self, 0.7)                                        # "One run"
        r1, t1 = ring(ys[0]), a2_l("one run", -5.3, ys[0], 38)
        self.play(Create(r1), FadeIn(t1), run_time=0.35)
        a2_at(self, 1.35)                                       # "A tiny change"
        r2, t2 = ring(ys[1]), a2_l("a tiny change", -5.3, ys[1], 38)
        self.play(Create(r2), FadeIn(t2), run_time=0.35)
        a2_at(self, 2.3)                                        # "one node, no resources, no signals"
        s2 = a2_l("one node, no resources, no signals", -5.3, ys[1] - 0.55, 34, DIM)
        self.play(FadeIn(s2), run_time=0.4)
        a2_at(self, 4.7)                                        # "Nothing was drawn on screen"
        r3, t3 = ring(ys[2]), a2_l("nothing drawn on screen", -5.3, ys[2], 38)
        self.play(Create(r3), FadeIn(t3), run_time=0.35)
        a2_at(self, 5.9)                                        # "so this does not show it looks right"
        s3 = a2_l("so it does not show that it looks right", -5.3, ys[2] - 0.55, 34, DIM)
        self.play(FadeIn(s3), run_time=0.3)
        # (midpoint: three limits so far, each with its open ring: a still)
        a2_at(self, 8.3)                                        # "the agent's tool limits were written in its prompt"
        r4, t4 = ring(ys[3]), a2_l("tool limits only in the prompt", -5.3, ys[3], 38)
        self.play(Create(r4), FadeIn(t4), run_time=0.35)
        a2_at(self, 10.5)                                       # "not enforced"
        s4 = a2_m("Not logged in · Please run /login", -5.3, ys[3] - 0.6, 32, DIM)
        self.play(FadeIn(s4), run_time=0.4)
        done(self)
