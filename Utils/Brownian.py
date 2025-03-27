import numpy as np
from scipy.stats import norm
from typing import Optional

class Brownian:
    """
    Class to generate Brownian motions.
    """
    def __init__(self, t: float, nb_steps: int, nb_draws: int, seed: Optional[int] = None):
        self.t = t
        self.nb_steps = int(nb_steps)
        self.nb_draws = nb_draws
        self.dt = self.t/self.nb_steps
        if seed is not None:
            self.rng: np.random.Generator = np.random.default_rng(seed)
        else:
            self.rng: np.random.Generator = np.random

    def MotionVector(self) -> np.array:
        first_value = np.zeros((self.nb_draws, 1))
        normal_draws = norm.ppf(self.rng.uniform(size=(self.nb_draws, self.nb_steps))) * np.sqrt(self.dt)
        motion = np.concatenate((first_value, np.cumsum(normal_draws, axis=1)), axis=1)

        return motion