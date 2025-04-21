from datetime import datetime
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase

class PricerTree(PricerBase):
    """
    A class to handle pricer parameters for Monte Carlo.
    """
    def __init__(self, pricing_date: datetime, nb_steps: int, pruning_mode: str, pruning_limit: float):
        super().__init__(pricing_date)
        self.pricer_name: str = "Tree"
        self.nb_steps: int = nb_steps
        self.pruning_mode: bool = str(pruning_mode) == "True"
        if self.pruning_mode:
            self.pruning_limit: float = pruning_limit
        else:
            self.pruning_limit: float = -1