"""Act I (B02, B08, B09, B11; the rest of the act is captures and Remotion). Manim only, kit objects, real Godot 4.7.2 renders through lab_window.
Cast: the stage palette, the sand/rock/buoy/water set, one terracotta dot or ring per picture (never text). Numbers are the measured ones from the lane visual_intent
(B08: 25,115,178 / 184,157,110 / 108,129,162, predicted 108,129,161, screen 108,129,162; B09: red 108 and 71, ticks 73 and 108). B11 is a drawing and says so."""

a1_BLUE = "#6E9BC7"; a1_WATER = "#1973B2"; a1_SAND = "#B89D6E"; a1_RESULT = "#6C81A2"; a1_ROCK = "#8E877B"; a1_SANDDK = "#8F7A52"


def a1_left(mob, x, y):
    """Put a mob's LEFT edge at x, centred on y."""
    mob.move_to([x + mob.width / 2.0, y, 0])
    return mob


def a1_right(mob, x, y):
    """Put a mob's RIGHT edge at x, centred on y."""
    mob.move_to([x - mob.width / 2.0, y, 0])
    return mob


def a1_tdot(p, r=0.17):
    return Dot(np.array([p[0], p[1], 0.0], dtype=float), radius=r, color=TERRA).set_stroke(DIM, width=3)


def a1_pring(p, r=0.3):
    """A terracotta ring on a point, over a wider grey backing (never accent text). No fill: the pixel inside stays visible."""
    c = np.array([p[0], p[1], 0.0])
    back = Circle(radius=r + 0.04, stroke_color=DIM, stroke_width=13, stroke_opacity=0.6).move_to(c)
    rr = Circle(radius=r, stroke_color=TERRA, stroke_width=7).move_to(c)
    return VGroup(back, rr)


def a1_pulse(r, k=1.15):
    """Pulse a ring (grey backing + terracotta) without Indicate's default yellow: each part keeps its own colour."""
    return [Indicate(r[0], scale_factor=k, color=DIM), Indicate(r[1], scale_factor=k, color=TERRA)]


def a1_tile(cx, cy, w=2.2, h=1.1, th=0.15):
    """A flat isometric plane tile: a diamond top, a thin slab edge, two grid lines."""
    L, R, Tp, B = [cx - w / 2, cy, 0], [cx + w / 2, cy, 0], [cx, cy + h / 2, 0], [cx, cy - h / 2, 0]
    side_l = Polygon(L, B, [cx, cy - h / 2 - th, 0], [cx - w / 2, cy - th, 0], stroke_color=INK, stroke_width=3, fill_color=GHOST, fill_opacity=1)
    side_r = Polygon(B, R, [cx + w / 2, cy - th, 0], [cx, cy - h / 2 - th, 0], stroke_color=INK, stroke_width=3, fill_color=LAB_STAGE, fill_opacity=1)
    top = Polygon(L, Tp, R, B, stroke_color=INK, stroke_width=4, fill_color=CARD, fill_opacity=1)
    g1 = Line([cx - w / 4, cy + h / 4, 0], [cx + w / 4, cy - h / 4, 0], color=DIM, stroke_width=3)
    g2 = Line([cx + w / 4, cy + h / 4, 0], [cx - w / 4, cy - h / 4, 0], color=DIM, stroke_width=3)
    return VGroup(side_l, side_r, top, g1, g2)


def a1_ball(cx, cy, r=0.5):
    """A round material preview tile: a pale water-blue ball with a cream glint."""
    b = Circle(radius=r, stroke_color=INK, stroke_width=4, fill_color=a1_BLUE, fill_opacity=0.65).move_to([cx, cy, 0])
    gl = Circle(radius=r * 0.2, stroke_width=0, fill_color=CARD, fill_opacity=0.95).move_to([cx - r * 0.35, cy + r * 0.35, 0])
    return VGroup(b, gl)


def a1_card(cx, cy, w=1.3, h=1.5):
    """A small code-card icon: a cream card with four short grey lines (no text on it)."""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=DIM, stroke_width=4, fill_color=PALEBOX, fill_opacity=1).move_to([cx, cy, 0])
    lines = VGroup(*[Line([cx - w / 2 + 0.22, cy + h / 2 - 0.3 - 0.3 * i, 0], [cx - w / 2 + 0.22 + ln, cy + h / 2 - 0.3 - 0.3 * i, 0], color=DIM, stroke_width=6)
                     for i, ln in enumerate((0.8, 0.55, 0.85, 0.45))])
    return VGroup(fr, lines)


# ═════════════════════════ B02 · three links ═════════════════════════
class B02_ThreeLinks(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        bx = box(-1.65, -0.4, 8.0, 4.0, color=INK, sw=5)                        # the MeshInstance3D node: x -5.65..2.35, y -2.4..1.6
        slot = box(0.0, -0.3, 3.5, 2.4, color=DIM, sw=4)                          # the Material Override slot
        title = T("MeshInstance3D", 36).move_to([-1.65, 2.3, 0])
        slot_lab = T("Material  Override", 36).move_to([0.0, -1.95, 0])
        card = a1_card(5.35, 0.3); card_lab = T("shader", 36).move_to([5.35, -0.8, 0])
        plane = a1_tile(-3.3, 0.35); plane_lab = T("PlaneMesh", 36).move_to([-3.3, -0.75, 0])
        ball = a1_ball(0.0, 0.3); ball_lab = T("ShaderMaterial", 36).move_to([0.0, -0.75, 0])
        # a shader alone: the card sits by itself on the empty stage
        self.play(FadeIn(card), FadeIn(card_lab), run_time=0.5)
        # link 1: the mesh (the plane) and the node that holds it
        until(self, "A mesh gives it a shape", lead=0.4)
        self.play(FadeIn(plane, shift=DOWN * 0.3), FadeIn(plane_lab), run_time=0.5)
        self.play(Create(bx), Create(slot), FadeIn(title), FadeIn(slot_lab), run_time=0.8)
        a_1 = arrow([-3.3, 0.95, 0], [-3.3, 2.0, 0], w=6)
        until(self, "here a flat plane", lead=0.3)
        self.play(GrowArrow(a_1), run_time=0.4)
        # link 2: the shader goes into the material
        until(self, "A material holds the shader", lead=0.8)
        self.play(FadeIn(ball, scale=0.6), FadeIn(ball_lab), run_time=0.4)
        a_2 = arrow([4.55, 0.3, 0], [0.62, 0.3, 0], w=6)
        self.play(GrowArrow(a_2), run_time=0.5)
        # link 3: the node holds the material (after the midpoint: the picture before it is a settled still)
        until(self, "the mesh node holds", lead=0.4)
        a_3 = arrow([0.0, 0.88, 0], [0.0, 2.0, 0], w=6)
        self.play(GrowArrow(a_3), run_time=0.5)
        self.play(Indicate(bx, color=TEAL, scale_factor=1.0), run_time=0.7)
        until(self, "Those three links", lead=0.2)
        self.play(*[Indicate(a, color=TEAL, scale_factor=1.0) for a in (a_1, a_2, a_3)], run_time=0.9)
        done(self)


# ═════════════════════════ B08 · the blend, as arithmetic ═════════════════════════
def a1_swatch(x, y, hexcol, s=0.8):
    return Square(side_length=s, stroke_color=INK, stroke_width=3, fill_color=hexcol, fill_opacity=1).move_to([x, y, 0])


def a1_numrow(label, nums, y, x_label=-5.95, x_nums=(-3.6, -2.25, -0.9), size=40):
    """A row 'label  n1, n2, n3' with the three numbers left-aligned in FIXED columns, so two rows sit exactly one under the other."""
    lab = a1_left(T(label, 36), x_label, y)
    ns = [a1_left(T(n, size), x_nums[i], y) for i, n in enumerate(nums)]
    g = VGroup(lab, *ns)
    g.lab = lab; g.ns = ns
    return g


class B08_BlendArithmetic(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        sx = -5.55
        sw_w = a1_swatch(sx, 2.75, a1_WATER); lw_ = a1_left(T("water  (25, 115, 178)", 34), -4.85, 2.75)
        sw_s = a1_swatch(sx, 1.75, a1_SAND); ls_ = a1_left(T("sand  (184, 157, 110)", 34), -4.85, 1.75)
        by = 0.1
        wbar = Rectangle(width=3.5, height=0.4, stroke_width=0, fill_color=a1_WATER, fill_opacity=1).move_to([-4.2, by, 0])
        sbar = Rectangle(width=1.5, height=0.4, stroke_width=0, fill_color=a1_SAND, fill_opacity=1).move_to([-0.8, by, 0])
        plus = VGroup(Line([-2.15, by, 0], [-1.85, by, 0], color=DIM, stroke_width=6), Line([-2.0, by - 0.15, 0], [-2.0, by + 0.15, 0], color=DIM, stroke_width=6))
        p70 = T("70%", 36).move_to([-4.2, by + 0.6, 0]); p30 = T("30%", 36).move_to([-0.8, by + 0.6, 0])
        # the real Forward+ render, shown as itself, probe ringed just outside
        Wd, wx, wy = 5.2, 3.5, 0.5
        win = lab_window("pantry/blend-fp.png", width=Wd, x=wx, y=wy, caption="Forward+")
        probe = [wx - 0.2 * Wd, wy]                      # plate over floor: x 0.30 of the image, y 0.5
        pr = a1_pring(probe, 0.3)
        # rows
        pred = a1_numrow("predicted", ["108,", "129,", "161"], -1.85)
        scr = a1_numrow("screen", ["108,", "129,", "162"], -2.7)
        res_sw = a1_swatch(sx, -0.85, a1_RESULT); res_lab = a1_left(T("result", 36), -4.85, -0.85)

        # the sum: seventy percent water plus thirty percent of what is behind
        until(self, "seventy percent water", lead=0.5)
        self.play(FadeIn(sw_w), FadeIn(lw_), GrowFromEdge(wbar, LEFT), FadeIn(p70), run_time=0.6)
        until(self, "plus thirty percent", lead=0.5)
        self.play(FadeIn(sw_s), FadeIn(ls_), FadeIn(plus), GrowFromEdge(sbar, LEFT), FadeIn(p30), run_time=0.6)
        # one pixel, checked in the real render
        until(self, "We checked one pixel", lead=0.5)
        self.play(FadeIn(win), run_time=0.5)
        until(self, "water over sand", lead=0.7)
        self.play(FadeIn(pr, scale=1.6), run_time=0.5)
        # --- after the midpoint: the bars slide together into the result swatch; the predicted row lands ---
        until(self, "The blend predicts", lead=-1.3)                      # lands after the 45 to 55 percent window
        self.play(sbar.animate.shift(LEFT * 0.9), p30.animate.shift(LEFT * 0.9), FadeOut(plus), FadeIn(pred.lab), FadeIn(pred.ns[0]), run_time=0.5)
        wt = Rectangle(width=0.56, height=0.8, stroke_width=0, fill_color=a1_WATER, fill_opacity=1).move_to([-5.67, -0.85, 0])
        st = Rectangle(width=0.24, height=0.8, stroke_width=0, fill_color=a1_SAND, fill_opacity=1).move_to([-5.27, -0.85, 0])
        self.play(Transform(wbar, wt), Transform(sbar, st), FadeOut(p70), FadeOut(p30), FadeIn(pred.ns[1]), run_time=0.7)
        self.play(FadeIn(res_sw), FadeIn(res_lab), FadeOut(wbar), FadeOut(sbar), run_time=0.4)
        until(self, "one sixty-one", lead=0.1)
        self.play(FadeIn(pred.ns[2]), run_time=0.3)
        # the screen reads
        until(self, "The screen reads", lead=0.1)
        self.play(FadeIn(scr.lab), run_time=0.3)
        until(self, "reads one hundred eight", lead=-0.45)
        self.play(FadeIn(scr.ns[0]), run_time=0.3)
        until(self, "twenty-nine, one sixty-two", lead=-0.2)
        self.play(FadeIn(scr.ns[1]), run_time=0.3)
        until(self, "one sixty-two", lead=0.4)
        self.play(FadeIn(scr.ns[2]), run_time=0.3)
        self.play(Indicate(pred.ns[2], color=TEAL, scale_factor=1.0), Indicate(scr.ns[2], color=TEAL, scale_factor=1.0), *a1_pulse(pr), run_time=0.4)
        done(self)


# ═════════════════════════ B09 · two renderers, one number line ═════════════════════════
def a1_xline(v, x0=-5.6, x1=5.6):
    return x0 + (x1 - x0) * v / 255.0


class B09_TwoRenderers(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        Wd, lx, rx, iy = 5.0, -3.1, 3.1, 1.85
        lw = lab_window("pantry/blend-fp.png", width=Wd, x=lx, y=iy, caption="Forward+")
        rw = lab_window("pantry/blend-compat.png", width=Wd, x=rx, y=iy, caption="Compatibility")
        pl = a1_pring([lx - 0.2 * Wd, iy], 0.26); pr_ = a1_pring([rx - 0.2 * Wd, iy], 0.26)
        # the red channel reads, under each render
        def reading(x, n):
            red = T("red", 32, DIM); num = T(n, 56, bold=True)
            return VGroup(red, num).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to([x, -0.75, 0])
        rd_l = reading(lx, "108"); rd_r = reading(rx, "71")
        # the number line 0 to 255 with two ticks
        ly = -1.95
        line = Line([-5.6, ly, 0], [5.6, ly, 0], color=INK, stroke_width=5)
        e0 = T("0", 32, DIM).move_to([-5.6, -1.45, 0]); e1 = T("255", 32, DIM).move_to([5.6, -1.45, 0])
        x73, x108, x71 = a1_xline(73), a1_xline(108), a1_xline(71)
        tk73 = Line([x73, ly - 0.22, 0], [x73, ly + 0.22, 0], color=INK, stroke_width=7)
        tk108 = Line([x108, ly - 0.22, 0], [x108, ly + 0.22, 0], color=INK, stroke_width=7)
        n73 = a1_right(T("typed-number mix", 36), x73 + 0.45, -2.6); v73 = T("73", 36).move_to([x73, -3.1, 0])
        n108 = a1_left(T("linear-light blend", 36), x108 - 0.45, -2.6); v108 = T("108", 36).move_to([x108, -3.1, 0])
        d108 = a1_tdot([lx, -1.4]); d71 = a1_tdot([rx, -1.4])

        # both real renders, the probe point ringed in each
        self.play(FadeIn(lw), FadeIn(rw), run_time=0.7)
        self.play(FadeIn(pl, scale=1.6), FadeIn(pr_, scale=1.6), run_time=0.5)
        # Forward+ blends in linear light: the line and its linear-light tick
        until(self, "Forward Plus blends in linear light", lead=0.5)
        self.play(Create(line), FadeIn(e0), FadeIn(e1), run_time=0.5)
        self.play(FadeIn(tk108), FadeIn(n108), FadeIn(v108), run_time=0.4)
        until(self, "mixing the typed numbers", lead=0.4)
        self.play(FadeIn(tk73), FadeIn(n73), FadeIn(v73), run_time=0.4)
        until(self, "would predict", lead=0.1)
        self.play(FadeIn(rd_l), FadeIn(rd_r), run_time=0.4)
        # --- after the 45 to 55 percent window: the two readings drop onto the line and snap to their ticks ---
        until(self, "not one hundred eight", lead=-0.2)
        self.play(FadeIn(d108), run_time=0.15)
        self.play(d108.animate.move_to([x108, -1.4, 0]), run_time=0.6, rate_func=smooth)
        self.play(d108.animate.move_to([x108, ly, 0]), run_time=0.25, rate_func=ease_in)
        self.play(Indicate(tk108, scale_factor=1.6, color=TEAL), run_time=0.4)
        until(self, "the typed numbers directly", lead=0.3)
        self.play(*a1_pulse(pr_), run_time=0.5)
        until(self, "so the same water reads", lead=1.0)
        self.play(FadeIn(d71), run_time=0.15)
        self.play(d71.animate.move_to([x71, -1.4, 0]), run_time=0.8, rate_func=smooth)
        self.play(d71.animate.move_to([x71, ly, 0]), run_time=0.25, rate_func=ease_in)
        self.play(Indicate(tk73, scale_factor=1.6, color=TEAL), run_time=0.4)
        done(self)
