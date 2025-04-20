from Parameters.Market import Market
from Parameters.Pricer.PricerBase import PricerBase
from Strategies.StrategyBase import StrategyBase
from Products.Options.OptionPricerManager import OptionPricerManager
from Parameters.Option.OptionEuropean import OptionEuropean
from datetime import datetime

class StrategyCertificateBase(StrategyBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, maturity_date: datetime):
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = None
        zero_strike_call = OptionEuropean("Call", 0, maturity_date)
        zero_strike_call_params = OptionPricerManager(self.Market, zero_strike_call, self.Pricer)
        self.products_params = [zero_strike_call_params]
        self.quantities = [1]