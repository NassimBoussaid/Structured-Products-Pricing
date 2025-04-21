from structured_products_pricing.Parameters.ModelParams import ModelParams
import numpy as np
from math import exp, sqrt, log
from scipy.stats import norm
from structured_products_pricing.Products.Options.OptionPricerBase import OptionPricerBase

class OptionPricerBS(OptionPricerBase):
    """
    Class to compute option prices using Black Scholes.
    """
    def __init__(self, model_params: ModelParams):
        """
        Initializes BlackScholes.

        Parameters:
        - model_params: ModelParams. Market, Option and Pricer parameters.
        """
        super().__init__(model_params)
        self.und_price: float = self.Market.und_price
        self.int_rate: float = self.Market.int_rate
        self.vol: float = self.Market.vol
        self.div: float = self.Market.div_rate
        self.strike: float = self.Option.strike
        self.time_to_maturity: float = self.Option.time_to_maturity
        self.d1: float = ((log(self.und_price/self.strike) + (self.int_rate - self.div + self.vol**2/2)
                           * self.time_to_maturity) / (self.vol * sqrt(self.time_to_maturity)))
        self.d2: float = self.d1 - self.vol * sqrt(self.time_to_maturity)

    def compute_price(self) -> float:
        """
        Computes the price of the option using Black Scholes.

        Returns:
        - price: float. Option price.
        """
        # Call option
        if self.Option.is_call():
            price: float = self.und_price * exp(-self.div * self.time_to_maturity) * norm.cdf(self.d1) \
                    - exp(-self.int_rate * self.time_to_maturity) * self.strike * norm.cdf(self.d2)
        # Put option
        elif self.Option.is_put():
            price: float = exp(-self.int_rate * self.time_to_maturity) * self.strike * norm.cdf(-self.d2) \
                    - self.und_price * exp(-self.div * self.time_to_maturity) * norm.cdf(-self.d1)
        return price

    def delta(self) -> float:
        """
        Computes the delta of the option using Black Scholes.

        Returns:
        - delta: float. Option Delta.
        """
        # Call option
        if self.Option.is_call():
            delta: float = exp(-self.div * self.time_to_maturity) * norm.cdf(self.d1)
        # Put option
        elif self.Option.is_put():
            delta: float = -exp(-self.div * self.time_to_maturity) * norm.cdf(-self.d1)
        return delta

    def gamma(self) -> float:
        """
        Computes the gamma of the option using Black Scholes.

        Returns:
        - gamma: float. Option Gamma.
        """
        gamma: float = exp(-self.div * self.time_to_maturity) * norm.pdf(self.d1) \
                / (self.und_price * self.vol * sqrt(self.time_to_maturity))
        return gamma

    def vega(self) -> float:
        """
        Computes the vega of the option using Black Scholes.

        Returns:
        - vega: float. Option Vega.
        """
        vega: float = self.und_price * exp(-self.div * self.time_to_maturity) * norm.pdf(self.d1) * sqrt(self.time_to_maturity)
        return vega/100

    def theta(self) -> float:
        """
        Computes the theta of the option using Black Scholes.

        Returns:
        - theta: float. Option Theta.
        """
        if self.Option.is_call():
            theta: float = (-exp(-self.div * self.time_to_maturity) * self.und_price * norm.pdf(self.d1)
                            * self.vol / (2 * sqrt(self.time_to_maturity))
                            - self.int_rate * self.strike * exp(-self.int_rate * self.time_to_maturity) * norm.cdf(self.d2)
                            + self.div * self.und_price * exp(-self.div * self.time_to_maturity) * norm.cdf(self.d1))
        elif self.Option.is_put():
            theta: float = (-exp(-self.div * self.time_to_maturity) * self.und_price * norm.pdf(self.d1)
                            * self.vol / (2 * sqrt(self.time_to_maturity))
                            + self.int_rate * self.strike * exp(-self.int_rate * self.time_to_maturity) * norm.cdf(-self.d2)
                            - self.div * self.und_price * exp(-self.div * self.time_to_maturity) * norm.cdf(-self.d1))
        return theta/252

    def rho(self) -> float:
        """
        Computes the rho of the option using Black Scholes.

        Returns:
        - rho: float. Option Rho.
        """
        if self.Option.is_call():
            rho: float = self.strike * self.time_to_maturity * exp(-self.int_rate * self.time_to_maturity) * norm.cdf(self.d2)
        elif self.Option.is_put():
            rho: float = -self.strike * self.time_to_maturity * exp(-self.int_rate * self.time_to_maturity) * norm.cdf(-self.d2)
        return rho/100

    def vomma(self) -> float:
        """
        Computes the vomma of the option using Black Scholes.

        Returns:
        - vomma: float. Option Vomma.
        """
        vomma: float = (self.und_price * exp(-self.div * self.time_to_maturity)
                        * norm.pdf(self.d1) * sqrt(self.time_to_maturity) * self.d1 * self.d2 / self.vol)
        return vomma

    # Black & Scholes vanna
    def vanna(self) -> float:
        """
        Computes the vanna of the option using Black Scholes.

        Returns:
        - vanna: float. Option Vanna.
        """
        vanna: float = -exp(-self.div * self.time_to_maturity) * norm.pdf(self.d1) * self.d2 / self.vol
        return vanna

    def greeks(self) -> np.array:
        """
        Computes the greeks of the option using Black Scholes.

        Returns:
        - np.array. Option Greeks.
        """
        return np.array([self.delta(), self.gamma(), self.vega(), self.theta(), self.rho()])