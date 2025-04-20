import numpy as np
from datetime import datetime
from Parameters.Option.OptionBase import OptionBase

class OptionBarrier(OptionBase):
    """
    Class to handle Barrier option parameters.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime, barrier_type: str,
                 barrier_direction: str, barrier_level: float, barrier_exercise: str):
        super().__init__(option_type, strike, maturity_date)
        self.option_name: str = "Barrier"
        self.barrier_type: str = barrier_type
        self.barrier_direction: str = barrier_direction
        self.barrier_level: float = barrier_level
        self.barrier_exercise: str = barrier_exercise
        self.active: bool = None

    def is_up(self) -> bool:
        return self.barrier_direction.lower() == "up"

    def is_down(self) -> bool:
        return self.barrier_direction.lower() == "down"

    def is_in(self):
        return self.barrier_type.lower() == "in"

    def is_out(self):
        return self.barrier_type.lower() == "out"

    def is_european_barrier(self):
        return self.barrier_exercise.lower() == "european"

    def is_american_barrier(self):
        return self.barrier_exercise.lower() == "american"

    def is_barrier_breached(self, und_price: np.array):
        self.active = (und_price > self.barrier_level) if self.is_up() else (und_price < self.barrier_level) if self.is_down() else None
        if self.is_american_barrier():
            self.active = np.any(self.active, axis=1)

    def is_active(self):
        return self.active if self.is_in() else ~self.active if self.is_out() else None

    def payoff(self, und_price: np.array) -> np.array:
        self.is_barrier_breached(und_price)
        und_price = (und_price[:, -1]) if self.is_american_barrier() else und_price
        return np.maximum(0, (und_price - self.strike) * (1 if self.is_call() else -1) * np.where(self.is_active(), 1, 0))