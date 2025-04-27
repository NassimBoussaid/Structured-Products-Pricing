import math


class RateFlat:
    """
    Flat Rate Curve class.
    Represents a constant yield curve where the interest rate is independent of maturity.

    Parameters:
        rate (float): Constant interest rate applied for all maturities.

    Methods:
        get_yield(t: float) -> float:
            Returns the same flat rate regardless of the input maturity t.
    """

    def __init__(self, rate: float):
        self.rate = rate

    def get_yield(self, t: float) -> float:
        return self.rate
