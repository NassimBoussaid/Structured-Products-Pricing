from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from datetime import datetime
import numpy as np

class OptionBarrier(OptionBase):
    """
    Class to handle Barrier option parameters, extending from OptionBase.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime, barrier_type: str,
                 barrier_direction: str, barrier_level: float, barrier_exercise: str):
        """
        Initializes a Barrier option.

        Parameters:
        - option_type: str. "call" or "put".
        - strike: float. Strike price of the option.
        - maturity_date: datetime. Maturity date of the option.
        - barrier_type: str. "in" (knock-in) or "out" (knock-out).
        - barrier_direction: str. "up" (up-and-...) or "down" (down-and-...).
        - barrier_level: float. Barrier trigger level.
        - barrier_exercise: str. "european" (check at maturity) or "american" (check continuously).
        """
        super().__init__(option_type, strike, maturity_date)
        self.option_name: str = "Barrier"
        self.barrier_type: str = barrier_type
        self.barrier_direction: str = barrier_direction
        self.barrier_level: float = barrier_level
        self.barrier_exercise: str = barrier_exercise
        self.active: bool = None

    def is_up(self) -> bool:
        """
        Checks if the barrier direction is "up".

        Returns:
        - bool. True if up barrier, False otherwise.
        """
        return self.barrier_direction.lower() == "up"

    def is_down(self) -> bool:
        """
        Checks if the barrier direction is "down".

        Returns:
        - bool. True if down barrier, False otherwise.
        """
        return self.barrier_direction.lower() == "down"

    def is_in(self):
        """
        Checks if the barrier type is "in" (knock-in).

        Returns:
        - bool. True if knock-in, False otherwise.
        """
        return self.barrier_type.lower() == "in"

    def is_out(self):
        """
        Checks if the barrier type is "out" (knock-out).

        Returns:
        - bool. True if knock-out, False otherwise.
        """
        return self.barrier_type.lower() == "out"

    def is_european_barrier(self):
        """
        Checks if the barrier exercise type is "european" (only checked at maturity).

        Returns:
        - bool. True if European style, False otherwise.
        """
        return self.barrier_exercise.lower() == "european"

    def is_american_barrier(self):
        """
        Checks if the barrier exercise type is "american" (checked continuously over the life).

        Returns:
        - bool. True if American style, False otherwise.
        """
        return self.barrier_exercise.lower() == "american"

    def is_barrier_breached(self, und_price: np.array):
        """
        Updates the barrier breach status based on the underlying path.

        Parameters:
        - und_price: np.array. Array of underlying prices over time.
        """
        # Determine if barrier has been breached at each time step
        self.active = (und_price > self.barrier_level) if self.is_up() else (und_price < self.barrier_level) if self.is_down() else None
        # For American barriers: active if the barrier was ever breached along the path
        if self.is_american_barrier():
            self.active = np.any(self.active, axis=1)

    def is_active(self):
        """
        Returns the activation status of the option, depending on barrier type.

        Returns:
        - np.array. Boolean array indicating if the option is active.
        """
        return self.active if self.is_in() else ~self.active if self.is_out() else None

    def payoff(self, und_price: np.array) -> np.array:
        """
        Computes the payoff of the Barrier option given underlying price paths.

        Parameters:
        - und_price: np.array. A 2D array of underlying prices.

        Returns:
        - np.array. Payoff values.
        """
        # Update barrier status
        self.is_barrier_breached(und_price)
        und_price = (und_price[:, -1]) if self.is_american_barrier() else und_price
        return np.maximum(0, (und_price - self.strike) * (1 if self.is_call() else -1) * np.where(self.is_active(), 1, 0))