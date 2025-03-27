from Parameters.Market import Market
from Parameters.Option import Option
from Parameters.Pricer import Pricer

class ModelParams:
    """
    A class to handle parameters (market, option, pricer).
    """
    def __init__(self, MarketObject: Market, OptionObject: Option, PricerObject: Pricer):
        self.Market: Market = MarketObject
        self.Option: Option = OptionObject
        self.Pricer: Pricer = PricerObject
        self.Option.time_to_maturity = (self.Option.maturity_date - self.Pricer.pricing_date).days / 365