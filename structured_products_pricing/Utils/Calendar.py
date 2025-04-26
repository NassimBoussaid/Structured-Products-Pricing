from datetime import datetime
from typing import List
import pandas as pd

class Calendar:
    """
    Class to manage a trading calendar.
    """

    # Mapping of custom frequency labels to pandas date_range aliases
    FREQUENCY_MAPPING = {
        'monthly': 'ME',
        'quarterly': 'QE',
        'yearly': 'YE',
    }

    def __init__(self, start_date: datetime, end_date: datetime, frequency=None):
        """
        Initializes a Calendar.

        Parameters:
        - start_date: datetime. Start date of the calendar.
        - end_date: datetime. End date of the calendar.
        - frequency: str, optional. Rebalancing frequency ("monthly", "quarterly", "yearly").

        Raises:
        - ValueError: If dates cannot be parsed or if start_date is after end_date.
        """
        try:
            self.start_date = pd.to_datetime(start_date)
            self.end_date = pd.to_datetime(end_date)
        except Exception as e:
            raise ValueError(f"Error parsing dates: {e}")

        if self.start_date > self.end_date:
            raise ValueError("start_date must be earlier than end_date.")

        self.frequency = frequency
        if self.frequency is not None:
            self.observation_dates = self._generate_observation_dates()
            self.all_dates = self._generate_all_trading_dates()

    def _generate_observation_dates(self) -> set[datetime]:
        """
        Generates observation dates based on frequency and date range.

        Returns:
        - List[datetime]. List of rebalancing dates.
        """
        # Get pandas frequency alias from mapping
        freq_alias = self.FREQUENCY_MAPPING[self.frequency]
        # Generate observation dates with given frequency
        observation_dates = pd.date_range(start=self.start_date, end=self.end_date, freq=freq_alias).to_pydatetime()
        # Force last observation date to match exact end_date
        observation_dates[-1] = self.end_date.to_pydatetime()

        return observation_dates

    def _generate_all_trading_dates(self) -> List[datetime]:
        """
        Generates all trading dates (business days only) in the given date range.

        Returns:
        - List[datetime]. List of trading dates excluding weekends.
        """
        all_business_days = pd.bdate_range(start=self.start_date, end=self.end_date, freq='C').tolist()
        return all_business_days

    @staticmethod
    def year_fraction(start: datetime, end: datetime, convention: str) -> float:
        """
        Computes the year fraction between two dates based on a day count convention.

        Parameters:
        - start: datetime. Start date.
        - end: datetime. End date.
        - convention: str. Day-count convention ("30/360", "act/360", "act/365").

        Returns:
        - float. Year fraction according to the specified convention.
        """
        days = (end - start).days
        conv = convention.lower()
        if conv == "30/360":
            d1, d2 = min(start.day, 30), min(end.day, 30)
            return ((end.year - start.year) * 360 + (end.month - start.month) * 30 + (d2 - d1)) / 360
        elif conv == "act/360":
            return days / 360
        elif conv == "act/365":
            return days/365
        return days / 365.25
