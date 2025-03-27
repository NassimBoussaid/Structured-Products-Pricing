from datetime import datetime

class Option:
    """
    A class to handle option parameters.
    """
    def __init__(self, option_type: str, exercise_type: str, payoff_type: str, strike: float,
                 maturity_date: datetime):
        self.option_type: str = option_type
        self.exercise_type: str = exercise_type
        self.payoff_type: str = payoff_type
        self.strike: float = strike
        self.maturity_date: datetime = maturity_date
        self.time_to_maturity: float = None

    def is_call(self) -> bool:
        return self.option_type.lower() == "Call".lower()

    def is_put(self) -> bool:
        return self.option_type.lower() == "Put".lower()

    def is_european(self) -> bool:
        return self.exercise.lower() == "European".lower()

    def is_american(self) -> bool:
        return self.exercise.lower() == "American".lower()

    def payoff(self, und_price: float) -> float:
        return max(0, (und_price - self.strike) * (1 if self.is_call() else -1))