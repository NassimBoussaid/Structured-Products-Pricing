class Market:
    """
    A class to handle market parameters.
    """
    def __init__(self, underlying_price: float, volatility: float, interest_rate: float, dividend_rate: float):
        self.und_price: float = underlying_price
        self.vol: float = volatility
        self.int_rate: float = interest_rate
        self.div_rate: float = dividend_rate