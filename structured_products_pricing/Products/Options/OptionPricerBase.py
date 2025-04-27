from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.ModelParams import ModelParams
from structured_products_pricing.Parameters.Market import Market
from abc import ABC, abstractmethod
import numpy as np

from structured_products_pricing.Rate.RateFormat import generate_rates_paths
from structured_products_pricing.Rate.RateStochastic import RateStochastic


class OptionPricerBase(ABC):
    """
    Abstract base class to handle the structure of option pricers.
    """

    def __init__(self, model_params: ModelParams):
        """
        Initializes the base setup for any option pricer.

        This class stores the aggregated market, option, and pricer parameters,
        and precomputes additional objects needed for pricing models.

        Parameters:
            model_params (ModelParams): Object aggregating:Market (Market), Option (OptionBase), Pricer (PricerBase)


        Attributes Initialized:
            self.Market (Market): Market data object.
            self.Option (OptionBase): Option or rate product object.
            self.Pricer (PricerBase): Pricer settings object.
            self.dt (float): Time increment (time_to_maturity divided by number of steps), only for MC or Tree.
            self.rates (np.ndarray or None): Discrete spot rates at each time step (for deterministic pricers).
            self.rates_path (np.ndarray or None): Broadcasted spot rate paths across simulations.
            self.df (np.ndarray or None): Discount factors associated to each time step and path.
        """
        self.Market: Market = model_params.Market
        self.Option: OptionBase = model_params.Option
        self.Pricer: PricerBase = model_params.Pricer
        if self.Pricer.pricer_name == "MC" or self.Pricer.pricer_name == "Tree":
            self.dt = self.Option.time_to_maturity / self.Pricer.nb_steps

            self.rates, self.rates_path, self.df = generate_rates_paths(interest_rate=self.Market.int_rate,
                                                                        mode=self.Market.rate_mode,
                                                                        time_to_maturity=self.Option.time_to_maturity,
                                                                        pricer=self.Pricer)


@abstractmethod
def compute_price(self) -> float:
    """
    Abstract method to compute the option price.

    Returns:
    - float. The computed option price.
    """
    pass
