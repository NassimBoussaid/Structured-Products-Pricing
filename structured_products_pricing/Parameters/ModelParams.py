from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase

class ModelParams:
    """
    Class to handle model parameters, combining Market, Option, and Pricer information.
    """
    def __init__(self, MarketObject: Market, OptionObject: OptionBase, PricerObject: PricerBase):
        """
        Initializes model parameters.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - OptionObject: OptionBase. Object describing the option to be priced.
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        """
        self.Market: Market = MarketObject
        self.Option: OptionBase = OptionObject
        self.Pricer: PricerBase = PricerObject
        self.Option.time_to_maturity = (self.Option.maturity_date - self.Pricer.pricing_date).days / 365
        self.Market.time_to_div = (self.Market.div_date - self.Pricer.pricing_date).days / 365