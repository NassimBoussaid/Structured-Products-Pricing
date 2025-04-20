from Parameters.Market import Market
from Parameters.Option.OptionBase import OptionBase
from Parameters.Pricer.PricerBase import PricerBase

class ModelParams:
    """
    A class to handle parameters (market, option, pricer).
    """
    def __init__(self, MarketObject: Market, OptionObject: OptionBase, PricerObject: PricerBase):
        self.Market: Market = MarketObject
        self.Option: OptionBase = OptionObject
        self.Pricer: PricerBase = PricerObject
        self.Option.time_to_maturity = (self.Option.maturity_date - self.Pricer.pricing_date).days / 365
        self.Option.time_to_div = (self.Market.div_date - self.Pricer.pricing_date).days / 365