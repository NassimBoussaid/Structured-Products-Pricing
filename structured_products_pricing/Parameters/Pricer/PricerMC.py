from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from datetime import datetime

class PricerMC(PricerBase):
    """
    Class to handle pricer parameters for Monte Carlo simulations, extending from PricerBase.
    """
    def __init__(self, pricing_date: datetime, nb_steps: int, nb_draws: int, seed: int):
        """
        Initializes a Monte Carlo pricer.

        Parameters:
        - pricing_date: datetime. The date at which pricing is performed.
        - nb_steps: int. Number of time steps in the simulation.
        - nb_draws: int. Number of Monte Carlo paths.
        - seed: int. Random seed for reproducibility (optional).
        """
        super().__init__(pricing_date)
        self.pricer_name: str = "MC"
        self.nb_steps: int = nb_steps
        self.nb_draws: int = nb_draws
        if seed is not None:
            self.seed = seed
        else:
            self.seed = None
