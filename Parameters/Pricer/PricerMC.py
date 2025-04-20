from datetime import datetime
from Parameters.Pricer.PricerBase import PricerBase

class PricerMC(PricerBase):
    """
    A class to handle pricer parameters for Monte Carlo.
    """
    def __init__(self, pricing_date: datetime, nb_steps: int, nb_draws: int, seed: int):
        super().__init__(pricing_date)
        self.pricer_name: str = "MC"
        self.nb_steps: int = nb_steps
        self.nb_draws: int = nb_draws
        if seed is not None:
            self.seed = seed
        else:
            self.seed = None