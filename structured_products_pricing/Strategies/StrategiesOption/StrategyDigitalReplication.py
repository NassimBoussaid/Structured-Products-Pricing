from structured_products_pricing.Strategies.StrategiesOption.StrategyCallSpread import StrategyCallSpread
from structured_products_pricing.Strategies.StrategiesOption.StrategyPutSpread import StrategyPutSpread
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyDigitalReplication(StrategyBase):
    """
    Class to define a Digital Option Replication strategy, extending from StrategyBase.

    This strategy replicates a digital payoff by combining two vanilla options
    (calls or puts) with close strikes, scaled to match the desired payout.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, option_type: str, strike: float, epsilon: float,
                 maturity_date: datetime, coupon_level: float = 1):
        """
        Initializes a Digital Replication strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - option_type: str. Type of option to replicate ("Call" or "Put").
        - strike: float. Central strike around which replication is performed.
        - epsilon: float. Distance between the two strikes (small number).
        - maturity_date: datetime. Common maturity date for the options.
        - coupon_level: float. Payout amount for the replicated digital (default: 1).
        """
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Digital Replication"
        # Build the replication: either a call spread or a put spread
        if option_type == "Call":
            options = StrategyCallSpread(self.Market, self.Pricer, strike - epsilon, strike, maturity_date)
        elif option_type == "Put":
            options = StrategyPutSpread(self.Market, self.Pricer, strike - epsilon, strike, maturity_date)
        # Retrieve the options and quantities from the spread
        self.products_params = options.products_params
        # Retrieve the options and quantities from the spread
        digital_gearing = coupon_level / epsilon
        self.quantities = [digital_gearing, -digital_gearing]