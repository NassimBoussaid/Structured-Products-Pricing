from structured_products_pricing.Products.Options.OptionPricerTree import OptionPricerTree
from structured_products_pricing.Products.Options.OptionPricerBS import OptionPricerBS
from structured_products_pricing.Products.Options.OptionPricerMC import OptionPricerMC
from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.ModelParams import ModelParams
from structured_products_pricing.Parameters.Market import Market
import numpy as np

class OptionPricerManager:
    """
    Class to manage and dispatch option pricing to the appropriate pricing engine.
    """
    def __init__(self, MarketObject: Market, OptionObject: OptionBase, PricerObject: PricerBase):
        """
        Initializes an OptionPricerManager.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - OptionObject: OptionBase. Object describing the option to be priced.
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        """
        self.Market: Market = MarketObject
        self.Option: OptionBase = OptionObject
        self.Pricer: PricerBase = PricerObject
        self.Models_Params = ModelParams(MarketObject, OptionObject, PricerObject)

    def compute_price(self) -> float:
        """
        Computes the price of the option based on the selected pricer.

        Returns:
        - float. The computed option price.
        """
        if self.Pricer.pricer_name == "MC":
            return OptionPricerMC(self.Models_Params).compute_price()
        elif self.Pricer.pricer_name == "Tree":
            return OptionPricerTree(self.Models_Params).compute_price()
        elif self.Pricer.pricer_name == "BS":
            return OptionPricerBS(self.Models_Params).compute_price()

    def compute_autocall_probabilities(self, autocall_barrier: float, frequency: str) -> np.array:
        """
        Computes autocall probabilities if the selected pricer is Monte Carlo.

        Parameters:
        - autocall_barrier: float. Barrier level triggering autocall.
        - frequency: str. Observation frequency.

        Returns:
        - np.array. Array of autocall probabilities at each observation date.
        """
        if self.Pricer.pricer_name == "MC":
            return OptionPricerMC(self.Models_Params).compute_autocall_probabilities(autocall_barrier, frequency)

    def compute_bs_greeks(self) -> np.array:
        """
        Computes the greeks of for BS pricer.

        Returns:
        - np.array. The computed greeks.
        """
        if self.Pricer.pricer_name == "BS":
            return OptionPricerBS(self.Models_Params).greeks()