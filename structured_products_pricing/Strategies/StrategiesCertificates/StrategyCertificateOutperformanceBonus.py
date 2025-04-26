from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Option.OptionBarrier import OptionBarrier
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyCertificateOutperformanceBonus(StrategyCertificateBase):
    """
    Class to define an Outperformance Bonus Certificate strategy, extending from StrategyCertificateBase.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, bonus_level: float, barrier_level: float,
                 upside_participation: float, maturity_date: datetime):
        """
        Initializes an Outperformance Bonus Certificate strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - bonus_level: float. Strike price for the bonus payout.
        - barrier_level: float. Barrier level protecting the bonus.
        - upside_participation: float. Participation rate above the bonus level (e.g., 1.2 for 120% participation).
        - maturity_date: datetime. Common maturity date for the product.
        """
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Outperformance Bonus"
        # Define the barrier put option to provide downside protection
        option_1 = OptionBarrier("Put", bonus_level, maturity_date, "out", "down", barrier_level, "American")
        # Define the call option for enhanced upside participation
        option_2 = OptionEuropean("Call", bonus_level, maturity_date)
        # Wrap each option with its pricer manager
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        self.products_params += [option_1_params, option_2_params]
        self.quantities += [1, (upside_participation - 1)]