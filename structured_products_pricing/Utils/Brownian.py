from typing import Optional
from scipy.stats import norm
import numpy as np

class Brownian:
    """
    Class to generate Brownian motions.
    """
    def __init__(self, t: float, nb_steps: int, nb_draws: int, seed: Optional[int] = None):
        """
        Initializes Brownian.

        Parameters:
        - t: float. Time to maturity (in years).
        - nb_steps: int. Number of time steps.
        - nb_draws: int. Number of independent Brownian paths.
        - seed: Optional[int]. If provided, used to initialize the random number generator to a fixed state.
        """
        self.t = t
        self.nb_steps = int(nb_steps)
        self.nb_draws = nb_draws
        self.dt = self.t/self.nb_steps
        # Initialize the random number generator
        if seed is not None:
            self.rng: np.random.Generator = np.random.default_rng(seed)
        else:
            self.rng: np.random.Generator = np.random

    def MotionScalar(self) -> np.array:
        """
        Generates multiple Brownian motion paths (2D array) using scalars.

        Returns:
        - motion: np.array. A 2D numpy array of shape (nb_draws, nb_steps + 1), where each row represents an independent
        Brownian motion.
        """
        # Create an empty list for Brownian motion paths
        motion = []
        # Loop over the number of independent Brownian paths
        for i in range(1, self.nb_draws + 1):
            # Create an empty list for one Brownian motion path
            single_motion = [0]
            # Loop over the number of time steps
            for j in range(1, self.nb_steps + 1):
                # Compute Brownian motion increments
                uniform_draw: float = self.rng.random()
                normal_draw: float = norm.ppf(uniform_draw)
                brownian_draw: float = normal_draw * np.sqrt(self.dt)
                single_motion.append(single_motion[j-1] + brownian_draw)
            # Add the independent Brownian motion to the list
            motion.append(single_motion)
        # Turn the motion into an array
        motion = np.array(motion)

        return motion

    def MotionVector(self) -> np.array:
        """
        Generates multiple Brownian motion paths (2D array) using numpy vectors.

        Returns:
        - motion: np.array. A 2D numpy array of shape (nb_draws, nb_steps + 1), where each row represents an independent
        Brownian motion.
        """
        # Generate first value of Brownian motion paths (zeros)
        first_value = np.zeros((self.nb_draws, 1))
        # Generate uniform draws using numpy vectors
        normal_draws = norm.ppf(self.rng.uniform(size=(self.nb_draws, self.nb_steps))) * np.sqrt(self.dt)
        # Compute and concatenate the cumulative sum along the time axis to obtain Brownian motion paths
        motion = np.concatenate((first_value, np.cumsum(normal_draws, axis=1)), axis=1)

        return motion