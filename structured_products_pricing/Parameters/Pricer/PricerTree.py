from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from datetime import datetime

class PricerTree(PricerBase):
    """
    Class to handle pricer parameters for tree-based methods, extending from PricerBase.
    """
    def __init__(self, pricing_date: datetime, nb_steps: int, pruning_mode: str, pruning_limit: float):
        """
        Initializes a Tree pricer.

        Parameters:
        - pricing_date: datetime. The date at which pricing is performed.
        - nb_steps: int. Number of steps in the tree.
        - pruning_mode: str. "True" if pruning is active, otherwise "False".
        - pruning_limit: float. Threshold limit for pruning branches (only used if pruning is active).
        """
        super().__init__(pricing_date)
        self.pricer_name: str = "Tree"
        self.nb_steps: int = nb_steps
        self.pruning_mode: bool = str(pruning_mode) == "True"
        if self.pruning_mode:
            self.pruning_limit: float = pruning_limit
        else:
            self.pruning_limit: float = -1