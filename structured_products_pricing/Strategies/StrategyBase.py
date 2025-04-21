from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from abc import ABC
from typing import List, Any

class StrategyBase(ABC):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase):
        self.strategy_name: str = None
        self.Market: Market = MarketObject
        self.Pricer: PricerBase = PricerObject
        self.products_params: List[Any] = None
        self.quantities: List[int] = None

    def price(self):
        price = 0
        for i, product in enumerate(self.products_params):
            price += product.compute_price() * self.quantities[i]
        return price

    def display_strategy(self):
        print(f"Strategy with {len(self.products_params)} products.")
        for i, product in enumerate(self.products_params):
            print(f"Product {i + 1}: {product.__class__.__name__} with quantity {self.quantities[i]}")