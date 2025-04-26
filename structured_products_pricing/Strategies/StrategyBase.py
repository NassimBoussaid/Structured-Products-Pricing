from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Market import Market
from typing import List, Any
from abc import ABC

class StrategyBase(ABC):
    """
    Abstract base class to handle structured strategies composed of multiple products.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase):
        """
        Initializes a StrategyBase.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        """
        self.strategy_name: str = None
        self.Market: Market = MarketObject
        self.Pricer: PricerBase = PricerObject
        self.products_params: List[Any] = None
        self.quantities: List[int] = None

    def price(self):
        """
        Computes the total price of the strategy by summing the price of each product multiplied by its quantity.

        Returns:
        - float. Total strategy price.
        """
        price = 0
        for product, quantity in zip(self.products_params, self.quantities):
            price += product.compute_price() * quantity
        return price

    def display_strategy(self):
        """
        Displays a summary of the strategy: number of products and details for each product.
        """
        print(f"Strategy with {len(self.products_params)} products.")
        for i, product in enumerate(self.products_params):
            print(f"Product {i + 1}: {product.__class__.__name__} with quantity {self.quantities[i]}")