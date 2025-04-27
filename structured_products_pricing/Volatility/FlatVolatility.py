class FlatVolatility:

    def __init__(self, volatility: float, is_shifted: bool = False, shift: float = 0):
        self.volatility = volatility
        self.is_shifted = is_shifted
        self.shift = shift

    def get_volatility(self, strike: float, time_to_maturity: float) -> float:
        if self.is_shifted:
            return self.volatility + self.shift
        else:
            return self.volatility
