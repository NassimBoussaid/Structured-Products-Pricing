from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionBarrier import OptionBarrier
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyCertificateBonus(StrategyCertificateBase):
    """
    Class to define a Bonus Certificate strategy, extending from StrategyCertificateBase.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, bonus_level: float, barrier_level: float,
                 maturity_date: datetime):
        """
        Initializes a Bonus Certificate strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - bonus_level: float. Level of the bonus payoff (strike of the put).
        - barrier_level: float. Barrier level below which protection is lost.
        - maturity_date: datetime. Common maturity date for the product.
        """
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Bonus"
        # Define the barrier put option representing the protection feature
        option = OptionBarrier("Put", bonus_level, maturity_date, "out", "down", barrier_level, "American")
        # Wrap the barrier option with its pricer manager
        option_params = OptionPricerManager(self.Market, option, self.Pricer)
        self.products_params += [option_params]
        self.quantities += [1]