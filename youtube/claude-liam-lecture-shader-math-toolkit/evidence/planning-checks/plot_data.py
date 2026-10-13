"""plot_data.py: the curves the Manim plots of this film draw, in numpy, each with the GLSL it stands for.

The build session may import this file (or paste the functions into scenes.py) so every plot is drawn from the SAME formula the shader
computes. run_dense_compare.py proves the match: it renders each GLSL expression in a real Godot 4.7.2 window, reads every pixel of the
middle row, and compares it with the numpy value (8-bit rounding, so a difference of one level counts as a match).

Every entry: name -> (glsl expression using float x, numpy function of x, strip scale note)
`x` is UV.x (0 to 1 across) unless the name says otherwise. Outputs are shown as grey, so they must lie in 0..1 (the scale is part of the expression).
"""
import numpy as np


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def step(edge, x):
    return np.where(x < edge, 0.0, 1.0)


def fract(x):
    return x - np.floor(x)


def mod(x, y):
    return x - y * np.floor(x / y)


CURVES = {
    # name: (glsl, numpy)
    "identity": ("x", lambda x: x),
    "one_minus": ("1.0 - x", lambda x: 1.0 - x),
    "step_half": ("step(0.5, x)", lambda x: step(0.5, x)),
    "clamp_overshoot": ("clamp(x * 2.0 - 0.5, 0.0, 1.0)", lambda x: np.clip(x * 2.0 - 0.5, 0.0, 1.0)),
    "smoothstep_3_7": ("smoothstep(0.3, 0.7, x)", lambda x: smoothstep(0.3, 0.7, x)),
    "smoothstep_0_10_over_0_10": ("smoothstep(0.0, 10.0, x * 10.0)", lambda x: smoothstep(0.0, 10.0, x * 10.0)),
    "linear_0_10_over_0_10": ("clamp(x * 10.0 / 10.0, 0.0, 1.0)", lambda x: np.clip(x * 10.0 / 10.0, 0.0, 1.0)),
    "mix_a_b": ("mix(0.2, 0.9, x)", lambda x: 0.2 * (1.0 - x) + 0.9 * x),
    "abs_centered": ("abs(x * 2.0 - 1.0)", lambda x: np.abs(x * 2.0 - 1.0)),
    "fract_4": ("fract(x * 4.0)", lambda x: fract(x * 4.0)),
    "floor_4_over_3": ("floor(x * 4.0) / 3.0", lambda x: np.floor(x * 4.0) / 3.0),
    "mod_quarter_x4": ("mod(x, 0.25) * 4.0", lambda x: mod(x, 0.25) * 4.0),
    "sine_two_cycles": ("0.5 + 0.5 * sin(x * 12.5663706144)", lambda x: 0.5 + 0.5 * np.sin(x * 4.0 * np.pi)),
    "pow_3": ("pow(x, 3.0)", lambda x: x ** 3.0),
    "pow_half": ("pow(x, 0.5)", lambda x: x ** 0.5),
    "stripes": ("step(0.5, fract(x * 8.0))", lambda x: step(0.5, fract(x * 8.0))),
    # the ring seen from the middle outward: input is the distance d from 0 to 0.7 across the strip
    "ring_profile_hard": ("step(0.3, x * 0.7) - step(0.38, x * 0.7)", lambda x: step(0.3, x * 0.7) - step(0.38, x * 0.7)),
    "ring_profile_soft": ("smoothstep(0.26, 0.30, x * 0.7) - smoothstep(0.38, 0.42, x * 0.7)",
                          lambda x: smoothstep(0.26, 0.30, x * 0.7) - smoothstep(0.38, 0.42, x * 0.7)),
}

# colour blends of two vectors (teal to gold), weight = the named curve. Used by the "any ramp can be the weight" picture.
TEAL = np.array([0.37, 0.64, 0.57])
GOLD = np.array([0.96, 0.80, 0.45])
BLENDS = {
    "blend_plain_ramp": ("mix(vec3(0.37, 0.64, 0.57), vec3(0.96, 0.80, 0.45), x)", lambda x: x),
    "blend_step": ("mix(vec3(0.37, 0.64, 0.57), vec3(0.96, 0.80, 0.45), step(0.5, x))", lambda x: step(0.5, x)),
    "blend_smoothstep": ("mix(vec3(0.37, 0.64, 0.57), vec3(0.96, 0.80, 0.45), smoothstep(0.4, 0.6, x))", lambda x: smoothstep(0.4, 0.6, x)),
}


def blend_rgb(weight):
    w = np.asarray(weight)[..., None]
    return TEAL * (1.0 - w) + GOLD * w
