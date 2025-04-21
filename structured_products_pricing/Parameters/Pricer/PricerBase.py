from datetime import datetime
from abc import ABC, abstractmethod


class PricerBase(ABC):
    """
    A class to handle pricer parameters for Monte Carlo.
    """

    def __init__(self, pricing_date: datetime):
        self.pricer_name: str = None
        self.pricing_date: datetime = pricing_date
