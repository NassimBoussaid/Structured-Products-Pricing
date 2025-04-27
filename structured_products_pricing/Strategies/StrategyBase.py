from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Market import Market
from datetime import timedelta
from typing import List, Any
from copy import copy
from abc import ABC
import numpy as np

from structured_products_pricing.Rate.RateFlat import RateFlat
from structured_products_pricing.Volatility.FlatVolatility import FlatVolatility


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

    def price(self) -> float:
        """
        Computes the total price of the strategy by summing the price of each product multiplied by its quantity.

        Returns:
        - float. Total strategy price.
        """
        price = 0
        for product, quantity in zip(self.products_params, self.quantities):
            price += product.compute_price() * quantity
        return price

    def delta(self) -> float:
        """
        Computes the delta of the strategy using finite differences.

        Returns:
        - float. Strategy Delta.
        """
        shift: float = self.Market.und_price * 0.01
        originalMarket: Market = copy(self.Market)
        # Compute price after positive shift
        self.Market.und_price = originalMarket.und_price + shift
        priceUp: float = self.price()
        # Compute price after negative shift
        self.Market.und_price = originalMarket.und_price - shift
        priceDown: float = self.price()
        # Restore original spot
        self.Market.und_price = originalMarket.und_price

        return (priceUp - priceDown) / (2 * shift)

    def gamma(self) -> float:
        """
        Computes the gamma of the strategy using finite differences.

        Returns:
        - float. Strategy Gamma.
        """
        shift: float = self.Market.und_price * 0.01
        originalMarket: Market = copy(self.Market)
        # Compute base price
        price: float = self.price()
        # Compute price after positive shift
        self.Market.und_price = originalMarket.und_price + shift
        priceUp: float = self.price()
        # Compute price after negative shift
        self.Market.und_price = originalMarket.und_price - shift
        priceDown: float = self.price()
        # Restore original spot
        self.Market.und_price = originalMarket.und_price

        return (priceUp - 2 * price + priceDown) / (shift**2)

    def vega(self) -> float:
        """
        Computes the vega of the strategy using finite differences.

        Returns:
        - float. Strategy Vega.
        """
        shift: float = 0.01

        originalMarket: Market = copy(self.Market)
        # Compute price after positive shift
        self.Market.vol = originalMarket.vol + shift
        priceUp: float = self.price()
        # Compute price after negative shift
        self.Market.vol = originalMarket.vol - shift
        priceDown: float = self.price()
        # Restore original volatility
        self.Market.vol = originalMarket.vol

        return (priceUp - priceDown) / (2 * shift) / 100

    def theta(self) -> float:
        """
        Computes the theta of the strategy using finite differences.

        Returns:
        - float. Strategy Theta.
        """
        shift: float = 1
        originalPricer: PricerBase = copy(self.Pricer)
        # Compute price after positive shift
        self.Pricer.pricing_date = originalPricer.pricing_date - timedelta(days=shift)
        priceUp: float = self.price()
        # Compute price after negative shift
        self.Pricer.pricing_date = originalPricer.pricing_date + timedelta(days=shift)
        priceDown: float = self.price()
        # Restore original pricing date
        self.Pricer.pricing_date = originalPricer.pricing_date

        return -(1 / 252) * (priceUp - priceDown) / (2 * shift / 365)

    def rho(self) -> float:
        """
        Computes the rho of the strategy using finite differences.

        Returns:
        - float. Strategy Rho.
        """
        shift: float = 0.01
        originalMarket: Market = copy(self.Market)
        # Compute price after positive shift
        self.Market.rates = RateFlat(rate=originalMarket.int_rate + shift)
        priceUp: float = self.price()
        # Compute price after negative shift
        self.Market.rates = RateFlat(rate=originalMarket.int_rate - shift)
        priceDown: float = self.price()
        self.Market.rates = RateFlat(rate=originalMarket.int_rate)

        return (priceUp - priceDown) / (2 * shift) / 100

    def greeks(self) -> np.array:
        """
        Computes all standard Greeks and returns them as a numpy array.

        Returns:
        - np.array. [Delta, Gamma, Vega, Theta, Rho]
        """
        if self.Pricer.pricer_name == "MC" or self.Pricer.pricer_name == "Tree":
            return np.array([self.delta(), self.gamma(), self.vega(), self.theta(), self.rho()])
        elif self.Pricer.pricer_name == "BS":
            return self.products_params[0].compute_bs_greeks()

    def greeks_over_spot_range(self, is_option: bool = False):
        """
        Computes price and Greeks over a range of underlying spot prices.

        Parameters:
        - is_option: bool. If True, also computes the theoretical payoff profile.

        Returns:
        - dict. Dictionary containing spot, payoff, price, and Greeks arrays.
        """
        # Define the range of spot values (from 10% to 200% of spot)
        step_percentages = np.linspace(0.1, 2.0, 20)
        spot_values = self.Market.und_price * step_percentages
        payoff_list, price_list, delta_list, gamma_list, vega_list, theta_list, rho_list = [], [], [], [], [], [], []
        if is_option:
            # Compute payoff for each spot if applicable
            product_payoff = np.zeros_like(spot_values)
            for product, quantity in zip(self.products_params, self.quantities):
                product_payoff += product.Option.payoff(np.array(spot_values)) * quantity
            payoff_list = product_payoff

        for spot in spot_values:
            self.Market.und_price = spot
            price_list.append(self.price())
            greeks = self.greeks()
            delta_list.append(greeks[0])
            gamma_list.append(greeks[1])
            vega_list.append(greeks[2])
            theta_list.append(greeks[3])
            rho_list.append(greeks[4])

        greeks = {"Spot": np.array(spot_values), "Payoff": np.array(payoff_list),
                  "Price": np.array(price_list), "Delta": np.array(delta_list),
                  "Gamma": np.array(gamma_list), "Vega": np.array(vega_list),
                  "Theta": np.array(theta_list), "Rho": np.array(rho_list)}

        return greeks

    def display_strategy(self):
        """
        Displays a summary of the strategy: number of products and details for each product.
        """
        print(f"Strategy with {len(self.products_params)} products.")
        for i, product in enumerate(self.products_params):
            print(f"Product {i + 1}: {product.__class__.__name__} with quantity {self.quantities[i]}")