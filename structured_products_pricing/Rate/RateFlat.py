import math

class RateFlat:
    def __init__(self, rate: float):
        self.rate = rate

    def discount_factor(self, t: float) -> float:
        return math.exp(-self.rate * t)

    def get_yield(self, t: float) -> float:
        return self.rate

    @classmethod
    def flat(cls, rate: float) -> 'RateFlat':
        return cls(rate)