from datetime import datetime
from abc import ABC

class PricerBase(ABC):
    """
    Abstract base class to handle pricer parameters.
    """
    def __init__(self, pricing_date: datetime):
        """
        Initializes the base pricer attributes.

        Parameters:
        - pricing_date: datetime. The date at which pricing is performed.
        """
        self.pricer_name: str = None
        self.pricing_date: datetime = pricing_date