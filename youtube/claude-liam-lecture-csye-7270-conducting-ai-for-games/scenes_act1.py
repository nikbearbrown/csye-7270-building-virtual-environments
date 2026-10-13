"""ACT I · The Empty Podium  (B01-B05, all Manim)

One cast for the act (ACTS.md "cast per act"):
  THE ORCHESTRA  - an isometric stage: a kraft podium (empty) and two arcs of player seats, each seat a kraft block with an instrument
                   standing on it (B03 builds it, B04 reuses the same drawing as the parts of a game, B05 keeps only the podium);
  THE BATON      - a thin ink line with ONE terracotta dot at its tip (B02 draws it, B03/B05 show where it is missing);
  THE GAME       - real frames of the real Walker Jumpman project with Clawd (EVID/godot-captures/walker-claude, Godot 4.7.2,
                   scripted input recorded 2026-10-09), stepped in time from pantry/a1_g_###.png (frames 3-70 of the 12 fps extract);
  THE RECORDED RUN - the four real tool calls of the recorded Godot run (EVID/godot-evidence/part2): Read, Edit, Write, godot --headless.
Pacing: a1_at() lands each motion on the real spoken word (faster-whisper times, evidence/act1/word_times.json).
GATE T: the real game window is a capture with dark navy ground and small HUD type; it is checked at real 4K (evidence/act1/gates_act1.py).
"""

A1P = "pantry/"
A1_KR = "#A38A60"                      # mid kraft: outline for the many SMALL objects (a lighter outline than the kit's #917A55, which GATE T counts as text ink)


def a1_at(self, t):
    """Wait until the clip clock reaches t seconds (a real spoken time of a word, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a1_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a1_no(x, y, r=0.5, sw=8):
    """A prohibition mark (ink ring + bar)."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring, bar)


# ───────────── the real game, stepped frame by frame from pantry/ ─────────────
A1_FR = {}


def a1_frame(i):
    if i not in A1_FR:
        from PIL import Image
        A1_FR[i] = np.array(Image.open(f"{A1P}a1_g_{i:03d}.png").convert("RGBA"))
    return A1_FR[i]


def a1_game(self, w, x, y, f0=3, f1=70, fps=12.0):
    """The Walker Jumpman capture as an ImageMobject; call a1_game_play(...) to start stepping it with the clip clock."""
    im = ImageMobject(f"{A1P}a1_g_{f0:03d}.png")
    im.set_width(w)
    im.move_to(np.array([x, y, 0.0]))
    return im


def a1_game_play(self, im, f0=3, f1=70, fps=12.0):
    st = {"i": f0, "t0": _elapsed(self)}

    def upd(m):
        i = min(f1, f0 + int(max(0.0, _elapsed(self) - st["t0"]) * fps))
        if i != st["i"]:
            st["i"] = i
            m.pixel_array = a1_frame(i)
    im.add_updater(upd)


def a1_win(w, h, x, y, color=DIM):
    """The thin grey frame around a real capture (grey, never ink: ink touching capture pixels fails GATE T)."""
    return Rectangle(width=w + 0.12, height=h + 0.12, stroke_color=color, stroke_width=4, fill_opacity=0).move_to([x, y, 0])


# ───────────── the orchestra (isometric) ─────────────
A1_ROWS = [(2.8, [-48, -24, 0, 24, 48]), (4.2, [-48, -32, -16, 0, 16, 32, 48])]
A1_SW, A1_SD, A1_SH = 0.62, 0.62, 0.30         # a seat block: width, depth, height
A1_IW = 0.17                                   # an instrument's footprint
A1_H0, A1_H1 = 0.32, 0.78                      # instrument height before / after it improves


def a1_xy(r, phi):
    a = np.radians(45 + phi)
    return r * np.cos(a), r * np.sin(a)


def a1_box(iso, x0, y0, z0, w, d, h, top, left, right, stroke=INK, sw=4):
    x1, y1, z1 = x0 + w, y0 + d, z0 + h
    return VGroup(
        iso.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, stroke=stroke, sw=sw),
        iso.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, stroke=stroke, sw=sw),
        iso.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, stroke=stroke, sw=sw))


def a1_inst_draw(g):
    """Redraws an instrument (a thin kraft block standing on its seat) at the height held by its tracker."""
    iso, x0, y0, z0, w, h = g.a1["iso"], g.a1["x0"], g.a1["y0"], g.a1["z0"], g.a1["w"], g.a1["h"].get_value()
    x1, y1, z1 = x0 + w, y0 + w, z0 + h
    faces = [[(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],
             [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
             [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    for poly, f in zip(g, faces):
        pts = [iso.p(*q) for q in f]
        poly.set_points_as_corners(pts + [pts[0]])


def a1_orch(iso):
    """Builds the orchestra. Returns dict: floor, pod (podium), seats (back to front; each seat = VGroup(block, instrument)),
    inst (the height trackers), dots (terracotta lights on the seat tops, opacity 0), phi (each seat's angle), gate (the empty baton)."""
    floor = iso.quad([(-0.5, -0.5, 0), (5.0, -0.5, 0), (5.0, 5.0, 0), (-0.5, 5.0, 0)], "#EAE6DA", stroke="#EAE6DA", sw=0)
    pod = a1_box(iso, -0.55, -0.55, 0, 1.1, 1.1, 0.34, BOX_TOP, BOX_L, BOX_R, stroke=INK, sw=4)
    items = []
    for r, phis in A1_ROWS:
        for ph in phis:
            x, y = a1_xy(r, ph)
            items.append((x + y, x, y, ph))
    items.sort(reverse=True)                      # back (large x + y) first
    seats, inst, dots, phis = [], [], [], []
    for _, x, y, ph in items:
        blk = a1_box(iso, x - A1_SW / 2, y - A1_SD / 2, 0, A1_SW, A1_SD, A1_SH, BOX_TOP, BOX_L, BOX_R, stroke=A1_KR, sw=3)
        trk = ValueTracker(A1_H0)
        ins = VGroup(*[Polygon([0, 0, 0], [1, 0, 0], [1, 1, 0], fill_color=c, fill_opacity=1, stroke_color=A1_KR, stroke_width=3)
                       for c in (BOX_L, BOX_R, BOX_TOP)])
        ins.a1 = dict(iso=iso, x0=x - A1_IW / 2 + 0.06, y0=y - A1_IW / 2 + 0.06, z0=A1_SH, w=A1_IW, h=trk)
        a1_inst_draw(ins)
        ins.add_updater(a1_inst_draw)
        dot = Dot(iso.p(x - A1_SW / 2 + 0.16, y - A1_SD / 2 + 0.16, A1_SH), radius=0.085, color=TERRA)
        dot.set_opacity(0)
        seats.append(VGroup(blk, ins))
        inst.append(trk)
        dots.append(dot)
        phis.append(ph)
    gate = DashedVMobject(Line(iso.p(0, 0, 0.34), iso.p(0, 0, 0.34) + np.array([0.85, 1.05, 0]), stroke_width=6), num_dashes=7)
    gate.set_stroke(DIM, 6)
    return dict(floor=floor, pod=pod, seats=seats, inst=inst, dots=dots, phi=phis, gate=gate)


def a1_ellipse(iso, c=(2.55, 2.55), half_along=1.95, half_across=3.7, n=80):
    """A flat ring on the stage floor around all the players (the whole performance), as a dashed grey curve."""
    u, v = np.array([1.0, 1.0]) / np.sqrt(2), np.array([1.0, -1.0]) / np.sqrt(2)
    pts = []
    for k in range(n + 1):
        t = 2 * np.pi * k / n
        q = np.array(c) + half_along * np.cos(t) * u + half_across * np.sin(t) * v
        pts.append(iso.p(q[0], q[1], 0.0))
    ring = VMobject()
    ring.set_points_as_corners(pts)
    return DashedVMobject(ring, num_dashes=70).set_stroke(DIM, 5)


# ── B01 · the AI writes the code: a page of code writes itself, then the real recorded run, then the real game; you do not type it ──
class B01_AIWritesCode(Scene):
    def construct(self):
        title = T("The Empty Podium", 40).move_to([-6.05, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        px, py, pw, ph = -2.95, 0.3, 6.3, 3.9
        panel = RoundedRectangle(width=pw, height=ph, corner_radius=0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0
                                 ).move_to([px, py, 0])
        a1_at(self, 0.1)
        self.play(Create(panel), run_time=0.4)
        # "the A. I. writes the code": lines of code write themselves into the page, a terracotta cursor at the end of each
        lens = [4.2, 3.0, 4.8, 2.2, 3.9, 3.4, 2.6]
        ys = [py + 1.4 - i * 0.46 for i in range(7)]
        x0 = px - 2.7
        cur = Dot([x0, ys[0], 0], radius=0.09, color=TERRA)
        self.add(cur)
        wl = VGroup()
        for y, w in zip(ys, lens):
            ln = Line([x0, y, 0], [x0 + w, y, 0], color=BAR1, stroke_width=9)
            wl.add(ln)
            self.play(Create(ln), cur.animate.move_to([x0 + w + 0.2, y, 0]), run_time=0.2, rate_func=linear)
        a1_at(self, 2.1)                                              # "Claude Code or Codex": the page becomes the tool's own window
        head = a1_lab("Claude Code", px, py + 1.6, 36)
        r_l = a1_lab("recorded run", px, py - ph / 2 - 0.45, 34)
        self.play(FadeOut(wl), FadeOut(cur), FadeIn(head), FadeIn(r_l), run_time=0.5)
        rows_y = [py + 0.8, py + 0.25, py - 0.3, py - 0.85, py - 1.4]
        X0 = px - 2.75

        def row(txt, y):
            t = M(txt, 32).move_to([X0 + 0.3, y, 0], aligned_edge=LEFT)
            d = Dot([X0, y, 0], radius=0.07, color=TERRA)
            return VGroup(d, t)
        r1, r2, r3, r4 = row("Read pong.tscn", rows_y[0]), row("Edit pong.tscn", rows_y[1]), \
            row("Write check_label.gd", rows_y[2]), row("godot --headless …", rows_y[3])
        a1_at(self, 3.62)                                             # "reads your project"
        self.play(FadeIn(r1, shift=RIGHT * 0.15), run_time=0.3)
        # (midpoint 4.25: the tool's window with its first real tool call; the game lands right after, as the project)
        gx, gy, gw = 3.35, 0.4, 5.55
        gh = gw * 9 / 16
        a1_at(self, 4.32)                                             # "your project": the real game it works on
        game = a1_game(self, gw, gx, gy)
        frame = a1_win(gw, gh, gx, gy)
        g_l = a1_lab("Walker Jumpman", gx, gy - gh / 2 - 0.5, 36)
        self.play(FadeIn(game), Create(frame), FadeIn(g_l), run_time=0.4)
        a1_game_play(self, game)
        a1_at(self, 4.72)                                             # "edits it"
        self.play(FadeIn(r2, shift=RIGHT * 0.15), FadeIn(r3, shift=RIGHT * 0.15), run_time=0.3)
        a1_at(self, 5.22)                                             # "runs it"
        self.play(FadeIn(r4, shift=RIGHT * 0.15), run_time=0.25)
        a1_at(self, 5.74)                                             # "and reports back"
        ok = check(X0 + 0.0, rows_y[4] - 0.02, s=0.2, color=INK, w=7)
        pas = M("PASS", 32).move_to([X0 + 0.55, rows_y[4], 0], aligned_edge=LEFT)
        self.play(Create(ok), FadeIn(pas), run_time=0.3)
        a1_at(self, 6.72)                                             # "You do not type the game"
        kx, ky = gx, -2.55
        kb = RoundedRectangle(width=2.9, height=0.9, corner_radius=0.14, stroke_color=DIM, stroke_width=5, fill_opacity=0
                              ).move_to([kx, ky, 0])
        keys = VGroup(*[Line([kx - 1.2, ky + dy, 0], [kx + 1.2, ky + dy, 0], color=GHOST, stroke_width=9) for dy in (0.2, -0.05)],
                      Line([kx - 0.8, ky - 0.28, 0], [kx + 0.8, ky - 0.28, 0], color=GHOST, stroke_width=9))
        self.play(FadeIn(kb), FadeIn(keys), run_time=0.3)
        no = a1_no(kx, ky, 0.52, 8)
        self.play(Create(no), run_time=0.4)
        done(self)


# ── B02 · less work, different work: the typing pile shrinks, a baton rises ─────────────────────────────────────────────────
class B02_DifferentWork(Scene):
    def construct(self):
        lx, ly = -3.5, 0.45
        page = RoundedRectangle(width=3.6, height=3.9, corner_radius=0.12, stroke_color=DIM, stroke_width=5, fill_opacity=0
                                ).move_to([lx, ly, 0])
        lens = [2.5, 1.8, 2.6, 1.4, 2.3, 1.9, 2.4, 1.6]
        lines = VGroup(*[Line([lx - 1.4, ly + 1.55 - i * 0.44, 0], [lx - 1.4 + w, ly + 1.55 - i * 0.44, 0], color=BAR1, stroke_width=10)
                         for i, w in enumerate(lens)])
        pile = VGroup(page, lines)
        t_l = a1_lab("typing", lx, -2.05, 40)
        self.play(FadeIn(pile, shift=UP * 0.15), FadeIn(t_l), run_time=0.45)
        a1_at(self, 0.58)                                             # "less work"
        self.play(pile.animate.scale(0.5, about_point=np.array([lx, ly - 1.95, 0])), run_time=0.75)
        a1_at(self, 1.6)                                              # "different work"
        arr = Arrow([-1.55, 0.0, 0], [0.9, 0.0, 0], buff=0, color=INK, stroke_width=8, tip_length=0.32)
        self.play(GrowArrow(arr), run_time=0.4)
        hx, hy = 2.2, -1.5
        tx, ty = 5.3, 1.9
        L = np.hypot(tx - hx, ty - hy)
        shaft = Line([hx, hy, 0], [tx, ty, 0], color=INK, stroke_width=11)
        grip = Line([hx, hy, 0], [hx + 0.55 * (tx - hx) / L, hy + 0.55 * (ty - hy) / L, 0], color=INK, stroke_width=26)
        tip = Dot([tx, ty, 0], radius=0.14, color=TERRA)
        c_l = a1_lab("conducting", 3.75, -2.05, 40)
        self.play(Create(shaft), FadeIn(grip), FadeIn(tip, scale=0.5), run_time=0.5)
        self.play(FadeIn(c_l), run_time=0.3)
        baton = VGroup(shaft, grip, tip)
        # (midpoint: the shrunken pile, the arrow, the baton and both labels)
        a1_at(self, 2.8)                                              # "the work this course teaches": the baton conducts
        H = np.array([hx, hy, 0.0])
        self.play(Rotate(baton, angle=0.16, about_point=H), run_time=0.4)
        self.play(Rotate(baton, angle=-0.32, about_point=H), run_time=0.55)
        self.play(Rotate(baton, angle=0.16, about_point=H), run_time=0.4)
        done(self)


# ── B03 · the orchestra with an empty podium: every player and instrument better, nobody conducting ──────────────────────────
class B03_EmptyPodium(Scene):
    def construct(self):
        iso = Iso(0.0, -2.55, 1.1)
        o = a1_orch(iso)
        a1_at(self, 0.2)                                              # "Picture an orchestra"
        self.add(o["floor"], o["pod"])
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in o["seats"]], lag_ratio=0.06), run_time=1.3)
        orch_l = a1_lab("orchestra", -4.3, 1.9, 38)
        self.play(FadeIn(orch_l), run_time=0.3)
        a1_at(self, 1.5)                                              # "every player has just got better": each seat lights up
        self.play(LaggedStart(*[d.animate.set_opacity(1) for d in o["dots"]], lag_ratio=0.07), run_time=1.2)
        a1_at(self, 3.0)                                              # "Every instrument improved": the instruments grow
        self.play(LaggedStart(*[t.animate.set_value(A1_H1) for t in o["inst"]], lag_ratio=0.06), run_time=1.1)
        a1_at(self, 4.2)                                              # "and nobody is conducting": the baton is missing
        self.play(Create(o["gate"]), run_time=0.8)
        # (midpoint 5.6: the orchestra, lit and grown, the missing baton drawn dashed over the podium)
        a1_at(self, 5.8)                                              # "Each player is brilliant": a spark visits every seat
        spark = Dot(o["dots"][0].get_center(), radius=0.1, color=TERRA).set_z_index(30)
        self.add(spark)
        order = sorted(range(len(o["dots"])), key=lambda i: (o["phi"][i], -i))
        for i in order:
            self.play(spark.animate.move_to(o["dots"][i].get_center()), run_time=0.085, rate_func=linear)
        a1_at(self, 7.3)                                              # "Nobody is holding the whole performance"
        ring = a1_ellipse(iso)
        self.play(Create(ring), run_time=1.0)
        w_l = a1_lab("whole performance", 4.1, -2.45, 36)
        self.play(FadeIn(w_l), FadeOut(spark), run_time=0.4)
        a1_at(self, 9.35)                                             # "The podium is empty"
        e_l = a1_lab("empty podium", -3.7, -2.65, 38)
        self.play(FadeIn(e_l), *[d.animate.set_opacity(0.25) for d in o["dots"]], run_time=0.6)
        self.play(o["gate"].animate.set_stroke(INK, 8), run_time=0.5)
        done(self)


# ── B04 · the same orchestra is a game: each part polished, the game wrong, because nobody held the whole thing ─────────────────
class B04_NobodyHeldIt(Scene):
    def construct(self):
        iso = Iso(-3.05, -2.3, 0.72)
        o = a1_orch(iso)
        for t in o["inst"]:
            t.set_value(A1_H1)
        for sg in o["seats"]:
            a1_inst_draw(sg[1])
            sg[1].clear_updaters()
        o["gate"].set_stroke(INK, 8)
        stage = VGroup(o["floor"], o["pod"], *o["seats"], o["gate"])
        self.add(stage)
        gp_x, gp_y = 3.6, 0.3                                         # the game: a plain drawn panel (an illustration)
        a1_at(self, 0.35)                                             # "a game built by an A. I.": the game appears beside the players
        panel = RoundedRectangle(width=3.9, height=2.6, corner_radius=0.12, stroke_color=INK, stroke_width=5, fill_color=CARD,
                                 fill_opacity=1).move_to([gp_x, gp_y, 0])
        gl1 = Line([gp_x - 1.7, gp_y - 0.75, 0], [gp_x - 0.35, gp_y - 0.75, 0], color=DIM, stroke_width=7)
        gl2 = Line([gp_x + 0.35, gp_y - 0.75, 0], [gp_x + 1.7, gp_y - 0.75, 0], color=DIM, stroke_width=7)
        gbl = Rectangle(width=0.36, height=0.36, stroke_color=A1_KR, stroke_width=4, fill_color=BOX_L, fill_opacity=1
                        ).move_to([gp_x - 1.1, gp_y - 0.52, 0])
        g_l = a1_lab("game", gp_x, gp_y - 1.8, 40)
        self.play(FadeIn(panel), Create(gl1), Create(gl2), FadeIn(gbl), FadeIn(g_l), run_time=0.6)
        left = VGroup(*[s for s, p in zip(o["seats"], o["phi"]) if p <= -20])
        right = VGroup(*[s for s, p in zip(o["seats"], o["phi"]) if p >= 20])
        mid = VGroup(*[s for s, p in zip(o["seats"], o["phi"]) if -20 < p < 20])
        a1_at(self, 1.9)                                              # "with nobody directing": the empty podium is marked
        self.play(Indicate(o["gate"], color=INK, scale_factor=1.15), run_time=0.7)
        a1_at(self, 3.05)                                             # "Each script can be fluent"
        l1 = a1_lab("script", -4.95, 1.3, 36)
        k1 = check(-4.15, 1.34, s=0.2, color=INK, w=7)
        self.play(FadeIn(l1), Create(k1), run_time=0.45)
        a1_at(self, 4.45)                                             # "each scene can look right"
        l2 = a1_lab("scene", -3.15, 1.3, 36)
        k2 = check(-2.35, 1.34, s=0.2, color=INK, w=7)
        self.play(FadeIn(l2), Create(k2), run_time=0.45)
        l3 = a1_lab("art", -1.4, 1.3, 36)
        k3 = check(-0.85, 1.34, s=0.2, color=INK, w=7)
        self.play(FadeIn(l3), Create(k3), run_time=0.4)
        # (midpoint 4.79: script, scene and art each checked; the game panel waits to the right)
        a1_at(self, 5.8)                                              # "and the game can still be wrong": an ink cross on the game
        x0, y0, s = gp_x, gp_y + 0.2, 0.62
        cross = VGroup(Line([x0 - s, y0 + s, 0], [x0 + s, y0 - s, 0], color=INK, stroke_width=14),
                       Line([x0 - s, y0 - s, 0], [x0 + s, y0 + s, 0], color=INK, stroke_width=14))
        self.play(Create(cross), run_time=0.5)
        a1_at(self, 7.35)                                             # "because nobody held the whole thing": the parts drift apart
        self.play(left.animate.shift(LEFT * 0.3), right.animate.shift(RIGHT * 0.25), mid.animate.shift(UP * 0.2),
                  run_time=0.9)
        done(self)


# ── B05 · the question: "can the AI write the code?" answered (it can); "what is left for you?" is the work ──────────────────
class B05_TheQuestion(Scene):
    def construct(self):
        wx, wy, ww = -3.0, 0.2, 5.9
        wh = ww * 9 / 16
        a1_at(self, 0.35)                                             # "the question": a page of code, as in the first beats
        page = RoundedRectangle(width=ww, height=wh, corner_radius=0.12, stroke_color=DIM, stroke_width=5, fill_opacity=0
                                ).move_to([wx, wy, 0])
        lens = [4.6, 3.2, 5.0, 2.4, 4.2, 3.7, 2.8]
        lines = VGroup(*[Line([wx - 2.6, wy + 1.2 - i * 0.4, 0], [wx - 2.6 + w, wy + 1.2 - i * 0.4, 0], color=BAR1, stroke_width=9)
                         for i, w in enumerate(lens)])
        q1 = a1_lab("write the code?", wx, wy + wh / 2 + 0.55, 40)
        self.play(FadeIn(page), FadeIn(lines), run_time=0.4)
        a1_at(self, 1.75)                                             # "can the A. I. write the code"
        self.play(FadeIn(q1), run_time=0.4)
        # (midpoint 3.74: the question over a page of code; the real answer lands right after)
        a1_at(self, 3.82)                                             # "It can." the real game it wrote
        game = ImageMobject(f"{A1P}a1_g_034.png")
        game.set_width(ww)
        game.move_to([wx, wy, 0])
        frame = a1_win(ww, wh, wx, wy)
        ok = check(wx - 0.95, wy - wh / 2 - 0.62, s=0.24, color=INK, w=8)
        yes = a1_lab("yes", wx - 0.05, wy - wh / 2 - 0.6, 40)
        self.play(FadeOut(page), FadeOut(lines), FadeIn(game), Create(frame), Create(ok), FadeIn(yes), run_time=0.45)
        a1_at(self, 4.3)                                              # "The question is what is left for you"
        iso = Iso(3.95, -1.45, 1.3)
        pod = a1_box(iso, -0.55, -0.55, 0, 1.1, 1.1, 0.34, BOX_TOP, BOX_L, BOX_R, stroke=INK, sw=4)
        gate = DashedVMobject(Line(iso.p(0, 0, 0.34), iso.p(0, 0, 0.34) + np.array([1.05, 1.4, 0]), stroke_width=7), num_dashes=7)
        gate.set_stroke(DIM, 7)
        self.play(FadeIn(pod, shift=DOWN * 0.2), Create(gate), run_time=0.6)
        q2 = a1_lab("what is left?", 3.95, 1.5, 40)
        self.play(FadeIn(q2), run_time=0.35)
        a1_at(self, 6.0)                                              # "and how to do it well"
        h_l = a1_lab("done well", 3.95, -2.7, 38)
        self.play(FadeIn(h_l), gate.animate.set_stroke(INK, 9), run_time=0.5)
        done(self)
