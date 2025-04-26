from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Option.OptionBarrier import OptionBarrier
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyCertificateCappedBonus(StrategyCertificateBase):
    """
    Class to define a Capped Bonus Certificate strategy, extending from StrategyCertificateBase.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, bonus_level: float, barrier_level: float,
                 cap_level: float, maturity_date: datetime):
        """
        Initializes a Capped Bonus Certificate strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - bonus_level: float. Level of the bonus payoff (put strike).
        - barrier_level: float. Barrier level protecting the bonus.
        - cap_level: float. Strike price of the cap (short call).
        - maturity_date: datetime. Common maturity date for all options.
        """
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Capped Bonus"
        # Define the barrier put option for protection
        option_1 = OptionBarrier("Put", bonus_level, maturity_date, "out", "down", barrier_level, "American")
        # Define the European call option to cap the upside
        option_2 = OptionEuropean("Call", cap_level, maturity_date)
        # Wrap each option with its pricer manager
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        self.products_params += [option_1_params, option_2_params]
        self.quantities += [1, -1]