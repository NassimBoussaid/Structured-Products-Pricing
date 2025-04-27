from datetime import datetime

from structured_products_pricing.Volatility.FlatVolatility import FlatVolatility
from structured_products_pricing.Rate.RateCurve import RateCurve
from structured_products_pricing.Rate.RateFlat import RateFlat


class Market:
    """
    Class to handle market parameters such as spot price, volatility, interest rate, and dividends.
    """

    def __init__(self, underlying_price: float, volatility: float, rate_mode: str, interest_rate: float,
                 div_mode: str,
                 dividend_rate: float, dividend_discrete: float, dividend_date: datetime):
        """
        Initializes market parameters.

        Parameters:
        - underlying_price: float. Current spot price of the underlying asset.
        - volatility: float. Volatility of the underlying asset.
        - rate_mode:str. 'stochastic rate' or 'curve rate' or 'constant' mode.
        - interest_rate: float. Risk-free interest rate.
        - div_mode: str. Dividend mode, either "continuous" or "discrete".
        - dividend_rate: float. Continuous dividend yield (if applicable).
        - dividend_discrete: float. Discrete dividend amount (if applicable).
        - dividend_date: datetime. Date when the discrete dividend is paid.
        """
        self.und_price: float = underlying_price
        self.vol = volatility

        self.rate_mode: str = rate_mode
        self.int_rate = interest_rate

        self.div_mode: str = div_mode
        self.div_date: datetime = dividend_date
        self.time_to_div: float = None
        if self.div_mode.lower() == "continuous":
            self.div_rate: float = dividend_rate
            self.div_discrete: float = 0
        elif self.div_mode.lower() == "discrete":
            self.div_discrete: float = dividend_discrete
            self.div_rate: float = 0