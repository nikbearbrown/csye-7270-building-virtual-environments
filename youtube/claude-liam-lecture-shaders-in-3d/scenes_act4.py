"""ACT IV · Read a Real One  (B35 only here, Manim; the kit is pasted above by assemble_scenes.py)

The pad shader's fragment function (lines 6 to 10 of lab-shaders/12-signal-pad.gdshader) as the one filled slot of the skeleton from Act I, with the
two empty slots (vertex, light) as dashed boxes above and below, all three on one width and one alignment. Two lines of the real file are wrapped
at an operator (marked in the report) because at the type floor (32) they are wider than the frame; the tokens themselves are untouched.
"""

A4_CW = 0.24962


def a4_toks(line, left, ybase, size=32):
    """Words of one code line on a shared baseline at exact monospace columns (see act 1's a1_toks)."""
    out = []
    col = 0
    for w in line.split(" "):
        if w:
            t = Text("H" + w + "H", font=MONO, color=INK, font_size=size)
            if len(t.submobjects) >= len(w) + 2:
                h0 = t.submobjects[0]
                t.shift([left + (col - 0.5) * A4_CW - h0.get_center()[0], ybase - h0.get_bottom()[1], 0])
                out.append(VGroup(*t.submobjects[1:-1]))
            else:
                out.append(M(w, size).move_to([left + (col + len(w) / 2.0) * A4_CW, ybase + 0.16, 0]))
        col += len(w) + 1
    return out


class B35_MissingSlots(Scene):
    """Two dashed slots draw in around the one filled function; then the filled one is outlined solid."""

    def construct(self):
        W = 12.3
        xc = 0.0
        src = ["void fragment() {",
               "  float stripe = step(0.5, fract(UV.x * 8.0));",
               "  vec3 base = quiet_color.rgb *",
               "      mix(0.65, 1.0, stripe);",
               "  ALBEDO = mix(base, active_color.rgb,",
               "      activation);",
               "}"]
        lh = 0.5
        H = len(src) * lh + 0.3
        cy = 0.0
        frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4).set_fill(PALEBOX, opacity=1).move_to([xc, cy, 0])
        left = xc - W / 2 + 0.45
        toks = []
        for i, ln in enumerate(src):
            y = cy + H / 2 - 0.15 - lh * (i + 0.5)
            toks += a4_toks(ln, left, y - 0.16)
        fn = VGroup(frame, *toks)
        top_y = cy + H / 2 + 0.3 + 0.4
        bot_y = cy - H / 2 - 0.3 - 0.4

        def slot(y):
            r = RoundedRectangle(width=W, height=0.8, corner_radius=0.14, stroke_color=DIM, stroke_width=5).move_to([xc, y, 0])
            return DashedVMobject(r, num_dashes=60, dashed_ratio=0.55)
        s_top = slot(top_y)
        s_bot = slot(bot_y)
        l_top = T("vertex(): Godot's default", 32).move_to([xc, top_y, 0])
        l_bot = T("light(): skipped by unshaded", 32).move_to([xc, bot_y, 0])
        self.add(fn)
        until(self, "no vertex function")
        self.play(Create(s_top), run_time=0.9)
        self.play(FadeIn(l_top), run_time=0.3)
        until(self, "no light function")
        self.play(Create(s_bot), run_time=0.9)
        self.play(FadeIn(l_bot), run_time=0.3)
        until(self, "The pad needs only fragment", lead=0.5)
        self.play(Indicate(s_top, scale_factor=1.03, color=DIM), Indicate(s_bot, scale_factor=1.03, color=DIM), run_time=0.8)
        self.play(frame.animate.set_stroke(INK, width=7), run_time=0.5)
        done(self)
