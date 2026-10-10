"""Work-around for a diffusers/torchsde bug hit by Stable Audio Open's default sampler (found 2026-09-29).

CosineDPMSolverMultistepScheduler builds a Brownian tree over [sigma_min, sigma_max] = [0.3, 500], but its final
step asks for noise between sigma = 0.3 and sigma_next = 0.0, outside the tree, and torchsde recurses until
RecursionError (reproduced on CPU and MPS without the model). In that step the noise term is multiplied by
sigma_next = 0, so returning zero noise there is exact; every other step is untouched.
"""
import torch
import diffusers.schedulers.scheduling_cosine_dpmsolver_multistep as _cosine
import diffusers.schedulers.scheduling_dpmsolver_sde as _sde


class SafeBrownianTreeNoiseSampler(_sde.BrownianTreeNoiseSampler):
    def __init__(self, x, sigma_min, sigma_max, seed=None, transform=lambda x: x):
        super().__init__(x, sigma_min, sigma_max, seed, transform)
        self._lo = float(sigma_min)
        self._zeros = torch.zeros_like(x)

    def __call__(self, sigma, sigma_next):
        if min(float(sigma), float(sigma_next)) < self._lo - 1e-6:
            return self._zeros.clone()
        return super().__call__(sigma, sigma_next)


def apply() -> str:
    _cosine.BrownianTreeNoiseSampler = SafeBrownianTreeNoiseSampler
    return "final-step noise below sigma_min returned as zeros (gen/sfx_sampler_fix.py)"
