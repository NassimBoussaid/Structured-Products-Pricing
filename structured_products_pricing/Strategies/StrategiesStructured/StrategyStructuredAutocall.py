from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.ModelParams import ModelParams
from structured_products_pricing.Parameters.Option.OptionBarrier import OptionBarrier
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Products.Options.OptionPricerMC import OptionPricerMC
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Strategies.StrategiesOption.StrategyDigitalReplication import StrategyDigitalReplication
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredBase import StrategyStructuredBase
from structured_products_pricing.Utils.Calendar import Calendar
from datetime import datetime

class StrategyStructuredAutocall(StrategyStructuredBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike: float, barrier_level: float, coupon_level: float,
                 observation_frequency: str, maturity_date: datetime):
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Autocall"
        calendar = Calendar(observation_frequency, self.Pricer.pricing_date, maturity_date)
        observation_dates = calendar.observation_dates
        a = ModelParams(self.Market, OptionEuropean("Call", 100, datetime(2025, 1, 2)), self.Pricer)
        MC = OptionPricerMC(a)
        test = MC.compute_maturity_probabilities()
        print(test)

        coupon_gearing = coupon_level * 100
        for observation, probability in zip(observation_dates, test):
            digital = StrategyDigitalReplication(self.Market, self.Pricer, "Call", strike, 0.05, observation, coupon_gearing)
            self.products_params += digital.products_params
            self.quantities += digital.quantities
        pdi = OptionBarrier("Put", strike, maturity_date, "in", "down", barrier_level, "American")
        pdi_params = OptionPricerManager(self.Market, pdi, self.Pricer)
        zc = StrategyDigitalReplication(self.Market, self.Pricer, "Call", 0, 0.05, maturity_date, 100)
        self.products_params += [pdi_params] + zc.products_params
        self.quantities += [-1] + zc.quantities