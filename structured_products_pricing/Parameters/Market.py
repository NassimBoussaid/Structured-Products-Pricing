from datetime import datetime

from structured_products_pricing.Rate.RateFlat import RateFlat


class Market:
    """
    A class to handle market parameters.
    """

    def __init__(self, underlying_price: float, volatility: float, interest_rate: float, div_mode: str,
                 dividend_rate: float, dividend_discrete: float, dividend_date: datetime):
        self.und_price: float = underlying_price
        self.vol: float = volatility
        self.int_rate: float = interest_rate
        self.discount_curve = RateFlat.flat(self.int_rate)

        self.div_date: datetime = dividend_date
        if div_mode.lower() == "continuous":
            self.div_rate: float = dividend_rate
            self.div_discrete: float = 0
        elif div_mode.lower() == "discrete":
            self.div_discrete: float = dividend_discrete
            self.div_rate: float = 0
            self.time_to_div: float = None
