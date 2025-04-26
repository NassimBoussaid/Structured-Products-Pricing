import math


class RateFlat:
    """
    Class for constant rate
    """
    def __init__(self, rate: float):
        """
        Initializes Rate.

        Parameters:
        - rate: float. Constant interest rate applied for all maturities.
        """
        self.rate = rate

    def discount_factor(self, t: float) -> float:
        """
        Computes the discount factor for a given maturity using the flat rate.

        Parameters:
        - t: float. Time to maturity.

        Returns:
        - float. Discount factor exp(-r * t).
        """
        return math.exp(-self.rate * t)

    def get_yield(self, t: float) -> float:
        """
        Retrieves the flat yield for a given maturity.

        Parameters:
        - t: float. Time to maturity.

        Returns:
        - float. Constant interest rate (flat yield).
        """
        return self.rate

    @classmethod
    def flat(cls, rate: float) -> 'RateFlat':
        """
        Class method to instantiate a flat rate curve.

        Parameters:
        - rate: float. Constant interest rate.

        Returns:
        - RateFlat. Instance of RateFlat with the given rate.
        """
        return cls(rate)
