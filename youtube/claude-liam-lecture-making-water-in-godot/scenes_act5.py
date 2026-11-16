"""Act V (B42): the depth texture. A schematic (tagged 'drawing'): a camera, the water surface, the sand, one view ray; the depth texture holds the floor, not the water.
Measured test geometry (E8): camera 6 m above the water, floor 0.5 m below; the gap read 0.500 m, so the depth texture held the floor (6.5 m) and not the water (6.0 m).
The picture is not to scale (the 0.5 m gap is exaggerated so the two hit points can be told apart)."""

A5_WATER = "#6E9BC7"; A5_SAND = "#B89D6E"


def a5_at(mob, x, y, left=False):
    """Place a mob by its left edge (left=True) or centred."""
    if left:
        mob.move_to([x + mob.width / 2.0, y, 0])
    else:
        mob.move_to([x, y, 0])
    return mob


def a5_dot(p, r=0.15):
    return Dot(np.array(p, dtype=float), radius=r, color=TERRA).set_stroke(DIM, width=3)


def a5_wave(x):
    return -0.2 + 0.05 * np.sin(3.0 * x)


# ═════════════════════════ B42 · the depth texture ═════════════════════════
class B42_DepthTexture(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        ttl = T("The Shore", 40)
        ttl.move_to([-6.2 + ttl.width / 2, 3.05, 0])
        self.add(ttl)

        # the cast: camera, surface, sand
        cam_body = RoundedRectangle(width=0.9, height=0.6, corner_radius=0.1, stroke_color=INK, stroke_width=5).move_to([-5.0, 1.2, 0])
        cam_lens = Polygon([-4.55, 1.35, 0], [-4.25, 1.5, 0], [-4.25, 0.9, 0], [-4.55, 1.05, 0], stroke_color=INK, stroke_width=5)
        cam_lab = T("camera", 32).move_to([-5.0, 0.55, 0])
        surface = ParametricFunction(lambda t: np.array([t, a5_wave(t), 0.0]), t_range=[-5.9, 5.9], stroke_color=A5_WATER, stroke_width=7)
        ysand = -1.9
        sand = Line([-5.9, ysand, 0], [5.9, ysand, 0], color=A5_SAND, stroke_width=8)
        rs = np.random.RandomState(4)
        specks = VGroup(*[Dot([float(rs.uniform(-5.7, 5.7)), float(rs.uniform(ysand - 0.28, ysand - 0.1)), 0], radius=0.035, color=A5_SAND) for _ in range(26)])
        drawing = T("drawing", 32, DIM).move_to([5.3, -3.05, 0])

        # the ray: camera -> water point W -> floor point F (W found where the ray meets the wavy surface)
        C = np.array([-4.25, 1.2, 0.0]); F = np.array([-0.4, ysand, 0.0])
        wx = -2.5
        for _ in range(6):
            yw = a5_wave(wx)
            wx = C[0] + (C[1] - yw) / (C[1] - F[1]) * (F[0] - C[0])
        W = np.array([wx, a5_wave(wx), 0.0])
        ray1 = Line(C, W, color=INK, stroke_width=6)
        ray2 = Line(W, F, color=INK, stroke_width=6)
        dw = a5_dot(W); df = a5_dot(F)
        lw = T("water 6.0 m", 32).move_to([-3.95, -0.85, 0])
        lw_lead = Line([W[0] - 0.12, W[1] - 0.12, 0], [W[0] - 0.42, W[1] - 0.45, 0], color=DIM, stroke_width=3)
        lf = T("floor 6.5 m", 32).move_to([F[0], ysand - 0.75, 0])
        lf_lead = Line([F[0], ysand - 0.2, 0], [F[0], ysand - 0.5, 0], color=DIM, stroke_width=3)

        # the depth texture box, holding only the floor value
        bx = box(3.6, 1.95, 3.9, 1.6, color=INK, sw=5)
        bt = T("depth texture", 32).move_to([3.6, 3.15, 0])
        bv = T("6.5 m", 48, bold=True).move_to([3.6, 1.5, 0])
        f_from = F + np.array([0.2, 0.18, 0.0])
        a_floor = arrow(f_from, np.array([2.9, 1.12, 0.0]), color=INK, w=6, tip=0.22)
        flow = a5_dot(f_from, r=0.1)
        # the water's arrow, grey and struck out
        w_from = W + np.array([0.1, 0.12, 0.0]); w_to = np.array([1.52, 1.7, 0.0])
        a_water = arrow(w_from, w_to, color=DIM, w=6, tip=0.22)
        mid = (w_from + w_to) / 2.0
        cross = VGroup(Line(mid + np.array([-0.27, -0.27, 0.0]), mid + np.array([0.27, 0.27, 0.0]), color=INK, stroke_width=7),
                       Line(mid + np.array([-0.27, 0.27, 0.0]), mid + np.array([0.27, -0.27, 0.0]), color=INK, stroke_width=7))
        notin = T("not in it", 32).move_to([mid[0] - 0.55, mid[1] + 0.8, 0])

        self.wait(0.2)
        self.play(FadeIn(VGroup(cam_body, cam_lab)), Create(cam_lens), Create(surface), Create(sand), FadeIn(specks), FadeIn(drawing), run_time=0.9)
        # "To know that, the water must know how deep": the ray draws from the camera, a dot marks each hit
        until(self, "To know that", lead=0.2)
        self.play(Create(ray1), run_time=0.8, rate_func=linear)
        self.play(FadeIn(dw, scale=1.6), FadeIn(lw), Create(lw_lead), run_time=0.35)
        until(self, "the water must", lead=0.2)
        self.play(Create(ray2), run_time=0.5, rate_func=linear)
        self.play(FadeIn(df, scale=1.6), FadeIn(lf), Create(lf_lead), run_time=0.35)
        # "how deep it is" / "A texture with the hint": the box, then only the floor value flows into it (all before the midpoint)
        until(self, "how deep it is", lead=0.3)
        self.play(Create(bx), FadeIn(bt), run_time=0.5)
        until(self, "A texture", lead=0.95)
        self.play(Create(a_floor), FadeIn(flow), run_time=0.35)
        self.play(flow.animate.move_to([2.9, 1.12, 0]), run_time=0.6, rate_func=linear)
        self.play(FadeOut(flow), FadeIn(bv), run_time=0.3)
        # "The water itself is not in it": the water's arrow, grey, struck out
        until(self, "The water itself", lead=0.3)
        self.play(Create(a_water), run_time=0.5)
        self.play(Create(cross), FadeIn(notin), run_time=0.35)
        # "so it can look beneath": the ray runs on through the water to the floor
        until(self, "look beneath", lead=0.3)
        self.play(Indicate(ray2, color=TEAL, scale_factor=1.0), run_time=0.7)
        done(self)
