"""Act III (B26, B27): the normal map. Manim only, kit objects, real Godot 4.7.2 images through lab_window.
B26: the real normal map with two grey-backed rings, two swatches in real pixel colours with arrows, a colour legend, the steepest lean 13 degrees.
B27: two real 2 x 2 tilings (seam off / seam on), the two switch chips, the measured edge jump (53 times a normal step / about 1).
Numbers are the measured ones from the lane visual_intent (FACTCHECK facts2); nothing is recomputed on screen."""

A3_RED = "#C94A45"; A3_GREEN = "#4E9B5C"; A3_BLUE = "#4A6FD6"


def a3_at(mob, x, y, left=False):
    """Place a mob by its left edge (left=True) or centred."""
    if left:
        mob.move_to([x + mob.width / 2.0, y, 0])
    else:
        mob.move_to([x, y, 0])
    return mob


def a3_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def a3_pix_ring(p, r=0.2):
    """A terracotta ring over a wider grey backing, centred on a point: the point itself stays uncovered (the ring sits just outside it)."""
    back = Circle(radius=r, stroke_color=DIM, stroke_width=12, stroke_opacity=0.55).move_to(np.array(p, dtype=float))
    rg = Circle(radius=r, stroke_color=TERRA, stroke_width=6).move_to(np.array(p, dtype=float))
    return VGroup(back, rg)


def a3_chip(text, x, y):
    """An outlined switch chip: a toggle circle and the switch name. Unlit = grey outline and hollow circle."""
    t = T(text, 32)
    w = t.width + 0.95
    rect = RoundedRectangle(width=w, height=0.66, corner_radius=0.33, stroke_color=DIM, stroke_width=4).move_to([x, y, 0])
    dot = Circle(radius=0.12, stroke_color=DIM, stroke_width=4).move_to([x - w / 2 + 0.38, y, 0])
    t.move_to([x - w / 2 + 0.7 + t.width / 2, y, 0])
    g = VGroup(rect, dot, t)
    g.rect = rect; g.dot = dot; g.w = w
    return g


def a3_light(chip):
    """Animations that light a chip: teal outline, filled toggle."""
    return [chip.rect.animate.set_stroke(TEAL, width=6), chip.dot.animate.set_fill(TEAL, opacity=1).set_stroke(TEAL, width=4)]


# ═════════════════════════ B26 · colour is direction ═════════════════════════
class B26_ColorIsDirection(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        W, wx, wy = 5.4, -3.35, 0.4
        lw = lab_window("pantry/normal_a.png", width=W, x=wx, y=wy, caption="real normal map")

        def px(row, col):
            return np.array([wx - W / 2 + (col + 0.5) / 512.0 * W, wy + W / 2 - (row + 0.5) / 512.0 * W, 0.0])
        ring_l = a3_pix_ring(px(100, 100))           # the 'leans' pixel: normal_a.png (100, 100) = (124, 133, 254)
        ring_s = a3_pix_ring(px(285, 226))           # the steepest pixel of the map (12.8 degrees, quoted as 13)

        sx, tx = 0.95, 1.95                           # swatch centre x, text left edge
        yl, yf = 2.45, -1.2                           # 'leans' row, 'flat' row
        sw_l = Square(side_length=1.2, fill_color=a3_hex(124, 133, 254), fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([sx, yl, 0])
        sw_f = Square(side_length=1.2, fill_color=a3_hex(127, 127, 254), fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([sx, yf, 0])
        t_l = a3_at(T("leans", 36), tx, yl + 0.38, left=True); n_l = a3_at(M("(124, 133, 254)", 32), tx, yl - 0.3, left=True)
        t_f = a3_at(T("flat", 36), tx, yf + 0.38, left=True); n_f = a3_at(M("(127, 127, 254)", 32), tx, yf - 0.3, left=True)
        # the arrows: upright for flat; about 3 degrees off upright for the sample pixel (modest: it is one sample)
        tilt = np.radians(3.0)
        base_l = np.array([sx, yl - 0.45, 0.0]); tip_l = base_l + 1.0 * np.array([-np.sin(tilt), np.cos(tilt), 0.0])
        base_f = np.array([sx, yf - 0.45, 0.0]); tip_f = base_f + np.array([0.0, 1.0, 0.0])
        ar_l = arrow(base_l, tip_l, color=INK, w=6, tip=0.22)
        ref_l = DashedLine(base_l, base_l + np.array([0.0, 1.0, 0.0]), color=CARD, stroke_width=3, dash_length=0.1)
        ar_f = arrow(base_f, tip_f, color=INK, w=6, tip=0.22)
        # legend: three arrow shapes in the channel colours, labelled by what each channel does
        ly = [1.15, 0.6, 0.05]
        lg_r = dim_arrow([sx - 0.6, ly[0], 0], [sx + 0.6, ly[0], 0], color=A3_RED, w=7, tip=0.2)
        lg_g = dim_arrow([sx, ly[1] - 0.26, 0], [sx, ly[1] + 0.26, 0], color=A3_GREEN, w=7, tip=0.2)
        lg_b = arrow([sx, ly[2] - 0.26, 0], [sx, ly[2] + 0.26, 0], color=A3_BLUE, w=7, tip=0.2)
        lb_r = a3_at(T("left or right", 32), tx, ly[0], left=True)
        lb_g = a3_at(T("up or down", 32), tx, ly[1], left=True)
        lb_b = a3_at(T("upright", 32), tx, ly[2], left=True)
        # the steepest lean: an upright reference, a 13 degree arrow, the angle, the number
        B = np.array([sx, -3.05, 0.0]); a13 = np.radians(13.0)
        ref13 = DashedLine(B, B + np.array([0.0, 0.95, 0.0]), color=DIM, stroke_width=3, dash_length=0.1)
        ar13 = arrow(B, B + 0.95 * np.array([np.sin(a13), np.cos(a13), 0.0]), color=INK, w=6, tip=0.2)
        arc13 = Arc(radius=0.62, start_angle=PI / 2 - a13, angle=a13, arc_center=B, color=DIM, stroke_width=4)
        n13 = a3_at(T("13°", 64, bold=True), tx, -2.45, left=True)
        s13 = a3_at(T("steepest", 32), tx + 1.45, -2.45, left=True)

        rg_sw = ring(sw_l, pad=0.1, sw=6)            # pairs the swatch with its pixel ring
        rg_13 = ring(n13, pad=0.1, sw=6)             # pairs the number with the steepest pixel's ring
        self.wait(0.2)
        self.play(FadeIn(lw), run_time=0.7)
        # "Red leans left or right": the sample pixel, its colour and its arrow
        until(self, "Red leans", lead=0.35)
        self.play(FadeIn(ring_l), FadeIn(sw_l), FadeIn(rg_sw), FadeIn(t_l), FadeIn(n_l), run_time=0.5)
        self.play(GrowArrow(ar_l), Create(ref_l), run_time=0.6)
        # the legend, one arrow per channel as the voice names it (all before the midpoint)
        until(self, "left or right", lead=0.3)
        self.play(GrowArrow(lg_r), FadeIn(lb_r), run_time=0.45)
        until(self, "green leans", lead=0.2)
        self.play(GrowArrow(lg_g), FadeIn(lb_g), run_time=0.45)
        until(self, "blue is how", lead=1.1)
        self.play(GrowArrow(lg_b), FadeIn(lb_b), run_time=0.45)
        # "A flat pixel is half, half, one"
        until(self, "A flat pixel", lead=0.3)
        self.play(FadeIn(sw_f), FadeIn(t_f), FadeIn(n_f), run_time=0.45)
        self.play(GrowArrow(ar_f), run_time=0.55)
        # "The steepest pixel here leans thirteen degrees"
        until(self, "steepest pixel", lead=0.2)
        self.play(FadeIn(ring_s), run_time=0.4)
        until(self, "thirteen", lead=0.45)
        self.play(Create(ref13), GrowArrow(ar13), Create(arc13), run_time=0.5)
        self.play(FadeIn(n13), FadeIn(rg_13), FadeIn(s13), run_time=0.4)
        done(self)


# ═════════════════════════ B27 · seamless ═════════════════════════
class B27_Seamless(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        W, lx, rx, iy = 3.8, -3.0, 3.0, 0.4
        lw = lab_window("pantry/tiles-not-seamless.png", width=W, x=lx, y=iy, caption="Seamless off")
        rw = lab_window("pantry/tiles-seamless.png", width=W, x=rx, y=iy, caption="Seamless on")
        top, edge_l, edge_r = iy + W / 2, lx - W / 2, rx + W / 2
        # two thin grey ticks per tiling, just outside the picture, marking where the tile edges cross (the seam pixels stay uncovered)
        ticks = VGroup(
            Line([lx, top + 0.08, 0], [lx, top + 0.26, 0], color=DIM, stroke_width=4), Line([edge_l - 0.1, iy, 0], [edge_l - 0.34, iy, 0], color=DIM, stroke_width=4),
            Line([rx, top + 0.08, 0], [rx, top + 0.26, 0], color=DIM, stroke_width=4), Line([edge_r + 0.1, iy, 0], [edge_r + 0.34, iy, 0], color=DIM, stroke_width=4))
        ca = a3_chip("As Normal Map", -1.48, 2.95)
        cb = a3_chip("Seamless", 2.185, 2.95)
        seam = a3_pix_ring([lx - W / 2 + 0.72 * W, iy, 0.0], r=0.3)
        n_off = T("53 times", 48, bold=True).move_to([lx, -2.55, 0]); u_off = T("a normal step", 32, DIM).move_to([lx, -3.05, 0])
        n_on = T("about 1", 48, bold=True).move_to([rx, -2.55, 0]); u_on = T("a normal step", 32, DIM).move_to([rx, -3.05, 0])

        self.wait(0.2)
        self.play(FadeIn(lw), FadeIn(rw), FadeIn(ca), FadeIn(cb), Create(ticks), run_time=0.9)
        # "switch on As Normal Map": the first chip lights
        until(self, "switch on As Normal Map", lead=0.3)
        self.play(*a3_light(ca), run_time=0.45)
        # "Also switch on Seamless": the second chip lights
        until(self, "Also switch on Seamless", lead=0.3)
        self.play(*a3_light(cb), run_time=0.45)
        # "the tile edges show a jump": the ring on the visible seam in the left tiling
        until(self, "tile edges show", lead=0.2)
        self.play(FadeIn(seam), run_time=0.45)
        # "fifty-three times a normal step": the measured jump under each tiling
        until(self, "fifty-three times", lead=0.3)
        self.play(FadeIn(n_off), FadeIn(u_off), run_time=0.45)
        until(self, "normal step", lead=0.15)
        self.play(FadeIn(n_on), FadeIn(u_on), run_time=0.45)
        done(self)
