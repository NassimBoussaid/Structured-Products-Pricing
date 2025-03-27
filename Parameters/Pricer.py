from datetime import datetime

class Pricer:
    """
    A class to handle pricer parameters for Monte Carlo.
    """
    def __init__(self, pricing_date: datetime, nb_steps: int, nb_draws: int, seed: int):
        self.pricing_date: datetime = pricing_date
        self.nb_steps: int = nb_steps
        self.nb_draws: int = nb_draws
        if seed is not None:
            self.seed = seed
        else:
            self.seed = None