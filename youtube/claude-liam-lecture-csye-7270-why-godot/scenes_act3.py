"""ACT III · A Complete Command Line  (B15-B18, all Manim)

HONESTY RULE for the act: every option name, command and output line on screen is verbatim from the real runs of 2026-10-09 on one Mac
(Godot 4.7.2.stable.official.ed1daf0bf): _conducting-series-evidence/godot-evidence/part1/godot-help-full.txt (the option names),
part1/walker-claude-copy-import-quit.txt (B16, B18), part2/independent-checks.txt section 4 (B17). Scratch paths are shown as <copy> /
<project> (the real paths are private scratch folders); line-broken or trimmed text carries a visible label. The game frames in B17 are
frames of a SEPARATE windowed recording (Movie Maker, scripted input), not of the headless run, and are labelled so: a headless run draws
no window. The 60 tick marks in B17 are an idea drawing of the sixty iterations the command asked for.
Menlo 32 is 0.25 scene units per character (measured 0.2497), so rows are placed by column from an explicit left edge.
"""

A3_CW = 0.25                  # Menlo 32: width of one character in scene units
A3P = "pantry/"

# the long option names of `godot --headless --help` (4.7.2), in the help's own order (the "--, ++" separator row omitted)
A3_FLAGS = ["--help", "--version", "--verbose", "--quiet", "--no-header", "--editor", "--project-manager", "--recovery-mode",
            "--debug-server", "--dap-port", "--lsp-port", "--quit", "--quit-after", "--language", "--path", "--scene", "--main-pack",
            "--render-thread", "--remote-fs", "--remote-fs-password", "--audio-driver", "--display-driver", "--audio-output-latency",
            "--rendering-method", "--rendering-driver", "--gpu-index", "--text-driver", "--tablet-driver", "--headless", "--log-file",
            "--write-movie", "--fullscreen", "--maximized", "--windowed", "--always-on-top", "--resolution", "--position", "--screen",
            "--single-window", "--xr-mode", "--wid", "--accessibility", "--accessibility-driver", "--debug", "--breakpoints",
            "--ignore-error-breaks", "--profiling", "--gpu-profile", "--gpu-validation", "--gpu-abort", "--generate-spirv-debug-info",
            "--extra-gpu-memory-tracking", "--accurate-breadcrumbs", "--remote-debug", "--single-threaded-scene", "--debug-collisions",
            "--debug-paths", "--debug-navigation", "--debug-avoidance", "--debug-stringnames", "--debug-canvas-item-redraw",
            "--max-fps", "--frame-delay", "--time-scale", "--disable-vsync", "--disable-render-loop", "--disable-crash-handler",
            "--fixed-fps", "--delta-smoothing", "--print-fps", "--editor-pseudolocalization", "--script", "--main-loop", "--check-only",
            "--import", "--export-release", "--export-debug", "--export-pack", "--export-patch", "--patches",
            "--install-android-build-template", "--convert-3to4", "--validate-conversion-3to4", "--doctool", "--no-docbase",
            "--gdextension-docs", "--gdscript-docs", "--build-solutions", "--dump-gdextension-interface",
            "--dump-gdextension-interface-json", "--dump-extension-api", "--dump-extension-api-with-docs", "--validate-extension-api",
            "--benchmark", "--benchmark-file"]


def a3_m(s, size=32, color=INK):
    """Menlo text with ligatures off, so '--' stays two hyphens (the real text), not one long dash."""
    return Text(s, font=MONO, color=color, font_size=size, disable_ligatures=True)


def a3_row(s, x_left, y, size=32, color=INK):
    """One Menlo row whose first character starts at x_left (explicit coordinates; no get_left()). No leading spaces."""
    cw = A3_CW * size / 32.0
    return a3_m(s, size, color).move_to([x_left + len(s) * cw / 2.0, y, 0])


def a3_tok(s, x_left, col, y, size=32, color=INK):
    """One Menlo token at a column of a row (used where a double space must survive)."""
    cw = A3_CW * size / 32.0
    return a3_m(s, size, color).move_to([x_left + (col + len(s) / 2.0) * cw, y, 0])


def a3_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    return t.move_to([x, y, 0], aligned_edge=LEFT) if left else t.move_to([x, y, 0])


def a3_window(cx, cy, w=1.5, h=1.05, color=DIM):
    """A plain app window drawn as an outline: frame + title bar line (Polygon/Line, not Rectangle)."""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    frame = Polygon([x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0], color=color, stroke_width=6)
    bar = Line([x0, y1 - 0.28, 0], [x1, y1 - 0.28, 0], color=color, stroke_width=5)
    dots = VGroup(*[Dot([x0 + 0.17 + 0.17 * i, y1 - 0.14, 0], radius=0.045, color=color) for i in range(3)])
    return VGroup(frame, bar, dots)


def a3_no(x, y, r=0.95, sw=7):
    """A prohibition mark (ring + bar) in INK, drawn around an object (never touching text)."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring, bar)


def a3_plus(x, y, s=0.22, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x + s, y, 0], color=color, stroke_width=w),
                  Line([x, y - s, 0], [x, y + s, 0], color=color, stroke_width=w))


# ── B15 · the second property: a complete command line (ACT TITLE) ──────────────────────────────────────────────────
class B15_CompleteCommandLine(Scene):
    def construct(self):
        title = T("A  Complete  Command  Line", 40).move_to([-2.7, 3.0, 0])
        cmd_a = a3_tok("godot", -3.6, 0, 1.6, 36)
        self.play(FadeIn(title), FadeIn(cmd_a), run_time=0.5)
        until(self, "You can run it with no window", lead=0.15)
        win = a3_window(-5.0, 1.6, 1.3, 0.9)
        no = a3_no(-5.0, 1.6, 0.98)
        cmd_b = a3_tok("--headless", -3.6, 6, 1.6, 36)
        self.play(Create(win), run_time=0.4)
        self.play(Create(no), FadeIn(cmd_b), run_time=0.4)
        wl = a3_lab("no window", 3.6, 1.6, 34)
        self.play(FadeIn(wl), run_time=0.25)
        rows = [("import a project", "--import", 0.15, "tell it to import a project"),
                ("run a script", "--script", -0.7, "run a script"),
                ("check a script for errors", "--check-only", -1.55, "check a script for errors"),
                ("export a build", "--export-release", -2.4, "or export a build")]
        for lab, opt, y, ph in rows:
            until(self, ph, lead=0.2)
            l = a3_lab(lab, -5.5, y, 34, left=True)
            d = Dot([-0.9, y, 0], radius=0.09, color=TERRA)
            o = a3_row(opt, -0.55, y)
            self.play(FadeIn(l), GrowFromCenter(d), FadeIn(o), run_time=0.4)
        cap = a3_lab("option names from the help text, version 4.7.2", 0.0, -3.05, 32, DIM)
        self.play(FadeIn(cap), run_time=0.3)
        done(self)


# ── B16 · the help's options scroll past; then a real import and a real run-and-quit, timed ───────────────────────────
class B16_ImportAndQuit(Scene):
    def construct(self):
        hc = a3_row("godot --headless --help", -6.0, 3.0)
        flags = VGroup(*[a3_row(f, -2.2, 0.0) for f in A3_FLAGS])
        off = ValueTracker(0.0)

        def place(g):
            o = off.get_value()
            for i, m in enumerate(g):
                m.move_to(np.array([-2.2 + (len(A3_FLAGS[i]) * A3_CW / 2.0), o - 2.4 - 0.5 * i, 0.0]))
                y = m.get_center()[1]
                m.set_opacity(0.0 if (y > 2.45 or y < -2.65) else 1.0)
        flags.add_updater(place)
        place(flags)
        self.add(flags)
        self.play(FadeIn(hc), run_time=0.3)
        self.play(off.animate.set_value(48.4), run_time=1.7, rate_func=linear)
        flags.remove_updater(place)
        self.play(FadeOut(flags), FadeOut(hc), run_time=0.3)
        until(self, "Here is a real project", lead=0.1)
        X0 = -6.0
        c1 = a3_row("$ godot --headless --path <copy> --import", X0, 2.9)
        p1 = a3_row("[ DONE ] loading_editor_layout", X0, 2.3)
        self.play(FadeIn(c1), run_time=0.3)
        self.play(FadeIn(p1), run_time=0.25)
        until(self, "exit code zero, in three", lead=0.25)
        e1 = VGroup(a3_tok("exit=0", X0, 0, 1.7), a3_tok("wall=3.03s", X0, 8, 1.7))
        k1 = check(-1.2, 1.7, 0.22)
        bar1 = Line([X0, 1.1, 0], [X0 + 3.03 * 1.4, 1.1, 0], color=BAR1, stroke_width=14)
        self.play(FadeIn(e1), Create(k1), run_time=0.35)
        self.play(Create(bar1), run_time=0.6, rate_func=linear)
        self.play(GrowFromCenter(Dot([X0 + 3.03 * 1.4 + 0.3, 1.1, 0], radius=0.11, color=TERRA)), run_time=0.2)
        until(self, "Then run and quit", lead=0.2)
        c2 = a3_row("$ godot --headless --path <copy> --quit", X0, 0.3)
        self.play(FadeIn(c2), run_time=0.3)
        until(self, "exit code zero, in a quarter", lead=0.25)
        e2 = VGroup(a3_tok("exit=0", X0, 0, -0.3), a3_tok("wall=0.25s", X0, 8, -0.3))
        k2 = check(-1.2, -0.3, 0.22)
        bar2 = Line([X0, -0.9, 0], [X0 + 0.25 * 1.4, -0.9, 0], color=BAR1, stroke_width=14)
        self.play(FadeIn(e2), Create(k2), run_time=0.3)
        self.play(Create(bar2), run_time=0.2, rate_func=linear)
        self.play(GrowFromCenter(Dot([X0 + 0.25 * 1.4 + 0.3, -0.9, 0], radius=0.11, color=TERRA)), run_time=0.2)
        cap = a3_lab("recorded run, on a copy of a real project (27 files)", 0.0, -2.2, 34)
        cap2 = a3_lab("bars drawn to scale: 3.03 s and 0.25 s", 0.0, -2.85, 32, DIM)
        self.play(FadeIn(cap), FadeIn(cap2), run_time=0.3)
        done(self)


# ── B17 · sixty frames with no window: exit code and output; the same game in a window, recorded separately ────────────
class B17_SixtyFrames(Scene):
    def construct(self):
        X0 = -6.0
        c1 = a3_row("$ godot --headless --path <project> \\", X0, 2.9)
        c2 = a3_row("--quit-after 60", X0 + 1.0, 2.35)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        until(self, "for sixty frames", lead=0.2)
        n0 = 60
        x0, x1 = -6.0, -0.4
        ticks = VGroup(*[Line([x0 + (x1 - x0) * i / (n0 - 1), -0.55, 0], [x0 + (x1 - x0) * i / (n0 - 1), -0.15, 0], color=DIM,
                              stroke_width=4) for i in range(n0)])
        tl = a3_lab("60 frames", -3.2, -1.15, 34)
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.02), run_time=1.2, rate_func=linear)
        self.play(FadeIn(tl), run_time=0.25)
        until(self, "without a window", lead=0.2)
        o1 = a3_row("Godot Engine v4.7.2.stable.official.ed1daf0bf", X0, 1.5)
        e1 = VGroup(a3_tok("exit=0", X0, 0, 0.95), a3_tok("wall=0.56s", X0, 8, 0.95))
        k1 = check(-1.2, 0.95, 0.22)
        self.play(FadeIn(o1), run_time=0.3)
        self.play(FadeIn(e1), Create(k1), run_time=0.3)
        cap = a3_lab("recorded run, line broken", -3.2, -2.35, 32, DIM)
        self.play(FadeIn(cap), run_time=0.25)
        until(self, "tell you whether it ran", lead=0.1)
        imgs = [ImageMobject(f"{A3P}a3_pong_{i}.png").set_width(5.4).move_to([3.1, -1.75, 0]) for i in range(1, 6)]
        fl = a3_lab("the same game, in a window", 3.1, 0.2, 34)
        self.add(imgs[0])
        self.play(FadeIn(fl), run_time=0.25)
        for i in range(1, 5):
            self.wait(0.38)
            self.remove(imgs[i - 1])
            self.add(imgs[i])
        until(self, "You can run the same command", lead=0.2)
        d = Dot([-0.85, 2.35, 0], radius=0.1, color=TERRA)
        yl = a3_lab("run it yourself", 1.2, 2.35, 36)
        self.play(GrowFromCenter(d), FadeIn(yl), run_time=0.35)
        done(self)


# ── B18 · the import quietly created one file: the folder before and after, then the two commands that show it ─────────
class B18_QuietNewFile(Scene):
    def construct(self):
        XL, XR = -6.0, 0.5
        hl = a3_lab("before the import", XL + 2.3, 3.0, 34)
        hr = a3_lab("after the import", XR + 2.3, 3.0, 34)
        arr = Arrow([-1.9, 3.0, 0], [0.0, 3.0, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.4)
        Y = [2.3 - 0.52 * i for i in range(7)]
        names_b = ["route_driver.gd.uid", "test_clawd.gd", "test_game.gd", "test_game.gd.uid"]
        lb = [a3_row("tests/ (excerpt)", XL, Y[0])] + [a3_row(n, XL + 0.5, Y[1 + i]) for i, n in enumerate(names_b)]
        lb.append(a3_row("...", XL + 0.5, Y[5]))
        self.play(FadeIn(hl), *[FadeIn(r) for r in lb], run_time=0.5)
        until(self, "That import quietly created one new file", lead=0.25)
        la = [a3_row("tests/ (excerpt)", XR, Y[0]), a3_row("route_driver.gd.uid", XR + 0.5, Y[1]), a3_row("test_clawd.gd", XR + 0.5, Y[2])]
        self.play(FadeIn(hr), Create(arr), *[FadeIn(r) for r in la], run_time=0.45)
        newr = a3_row("test_clawd.gd.uid", XR + 0.5, Y[3])
        pl = a3_plus(XR + 0.22, Y[3], 0.14, INK, 6)
        dot = Dot([XR - 0.25, Y[3], 0], radius=0.11, color=TERRA)
        self.play(FadeIn(newr), Create(pl), GrowFromCenter(dot), run_time=0.45)
        rest = [a3_row("test_game.gd", XR + 0.5, Y[4]), a3_row("test_game.gd.uid", XR + 0.5, Y[5]), a3_row("...", XR + 0.5, Y[6])]
        self.play(*[FadeIn(r) for r in rest], run_time=0.3)
        until(self, "a missing sidecar", lead=0.25)
        uid = a3_row("inside it, this run: uid://ci27qal208t75", XL, -1.45)
        self.play(FadeIn(uid), run_time=0.4)
        until(self, "Even a command that sounds read-only", lead=0.2)
        self.play(Indicate(VGroup(newr, dot), color=INK, scale_factor=1.04), run_time=0.5)
        until(self, "Check the diff", lead=0.35)
        g1 = a3_row("git diff", XL + 0.5, -2.3)
        g2 = a3_row("git status", XL + 0.5, -2.9)
        gl = a3_lab("check what changed", -2.1, -2.6, 34, left=True)
        gd = Dot([XL + 0.15, -2.6, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(gl), GrowFromCenter(gd), run_time=0.4)
        done(self)
