from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.ModelParams import ModelParams
from structured_products_pricing.Products.Options.OptionPricerBS import OptionPricerBS
from structured_products_pricing.Products.Options.OptionPricerMC import OptionPricerMC
from structured_products_pricing.Products.Options.OptionPricerTree import OptionPricerTree

class OptionPricerManager:
    def __init__(self, MarketObject: Market, OptionObject: OptionBase, PricerObject: PricerBase):
        self.Market: Market = MarketObject
        self.Option: OptionBase = OptionObject
        self.Pricer: PricerBase = PricerObject
        self.Models_Params = ModelParams(MarketObject, OptionObject, PricerObject)

    def compute_price(self):
        if self.Pricer.pricer_name == "MC":
            return OptionPricerMC(self.Models_Params).compute_price()
        elif self.Pricer.pricer_name == "Tree":
            return OptionPricerTree(self.Models_Params).compute_price()
        elif self.Pricer.pricer_name == "BS":
            return OptionPricerBS(self.Models_Params).compute_price()