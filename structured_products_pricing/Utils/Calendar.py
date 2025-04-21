from datetime import datetime, timedelta
import pandas as pd
from typing import List
from workalendar.usa import UnitedStates


class Calendar:
    """
    Classe de gestion du calendrier de trading :
    Gestion des jours de trading et des dates de rebalancement en fonction des fréquences spécifiées,
    en tenant compte des jours fériés fédéraux aux États-Unis.
    """

    FREQUENCY_MAPPING = {
        'daily': 'D',
        'weekly': 'W',
        'monthly': 'ME',
        'quarterly': 'Q',
        'yearly': 'YE',
    }

    CALENDAR = UnitedStates()

    def __init__(self, frequency: str, start_date: str, end_date: str):
        """
        Initialisation de la classe Calendar.

        :param frequency: Fréquence des rebalancements ('daily', 'monthly', 'quarterly', etc.).
        :param start_date: Date de début au format 'YYYY-MM-DD'.
        :param end_date: Date de fin au format 'YYYY-MM-DD'.
        :raises ValueError: Fréquence non supportée ou format de date incorrect.
        """
        frequency = frequency.lower()
        if frequency not in self.FREQUENCY_MAPPING:
            raise ValueError(
                f"Unsupported frequency '{frequency}'. Supported frequencies are: {list(self.FREQUENCY_MAPPING.keys())}"
            )

        try:
            self.start_date = pd.to_datetime(start_date)
            self.end_date = pd.to_datetime(end_date)
        except Exception as e:
            raise ValueError(f"Error parsing dates: {e}")

        if self.start_date > self.end_date:
            raise ValueError("start_date must be earlier than end_date.")

        self.frequency = frequency
        self.holidays = set(self.get_holidays_in_range(self.start_date, self.end_date))

        self.all_dates = self._generate_all_trading_dates()
        self.observation_dates = self._generate_observation_dates()

    def _is_trading_day(self, date: datetime) -> bool:
        """
        Identification d'un jour de trading (pas un week-end ou un jour férié fédéral).

        :param date: Date à vérifier.
        :return: True si c'est un jour de trading, False sinon.
        """
        return date.weekday() < 5 and date.date() not in self.holidays

    @classmethod
    def get_holidays_in_range(cls, start_date: datetime, end_date: datetime) -> List[datetime.date]:
        """
        Extraction des jours fériés fédéraux dans une plage de dates.

        :param start_date: Date de début.
        :param end_date: Date de fin.
        :return: Liste des jours fériés.
        """
        holidays = []
        start_year = start_date.year
        end_year = end_date.year

        for year in range(start_year, end_year + 1):
            yearly_holidays = cls.CALENDAR.holidays(year)
            for date, _ in yearly_holidays:
                if start_date.date() <= date <= end_date.date():
                    holidays.append(date)

        return holidays

    def _generate_all_trading_dates(self) -> List[datetime]:
        """
        Génération des jours de trading dans la plage définie, hors week-ends et jours fériés.

        :return: Liste des jours de trading.
        """
        all_business_days = pd.bdate_range(start=self.start_date, end=self.end_date, freq='C',
                                           holidays=self.holidays).tolist()
        return all_business_days

    def _adjust_to_next_trading_day(self, date: datetime) -> datetime:
        """
        Ajustement d'une date au prochain jour de trading disponible si nécessaire.

        :param date: Date à ajuster.
        :return: Jour de trading ajusté.
        """
        adjusted_date = date
        while not self._is_trading_day(adjusted_date):
            adjusted_date += timedelta(days=1)
            if adjusted_date > self.end_date:
                raise ValueError("Adjusted date exceeds the end_date range.")
        return adjusted_date

    def _generate_observation_dates(self) -> set[datetime]:
        """
        Génération des dates de rebalancement en fonction de la fréquence et de la plage de dates.

        :return: Ensemble des dates de rebalancement.
        """
        freq_alias = self.FREQUENCY_MAPPING[self.frequency]
        scheduled_dates = pd.date_range(start=self.start_date, end=self.end_date, freq=freq_alias)
        observation_dates = sorted(
            self._adjust_to_next_trading_day(date.to_pydatetime())
            for date in scheduled_dates
        )
        return set(observation_dates)

    @staticmethod
    def year_fraction(start: datetime, end: datetime, convention: str) -> float:
        """
        Calcule la fraction d'année entre deux dates selon :
         - '30/360'  30/360
         - 'act/360' Actual/360
         - 'act/365.25' Actual/365.25 (année bisextile)
        """
        days = (end - start).days
        conv = convention.lower()
        if conv == '30/360':
            d1, d2 = min(start.day, 30), min(end.day, 30)
            m1, m2 = start.month, end.month
            y1, y2 = start.year, end.year
            return (360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)) / 360.0
        if conv == 'act/360':
            return days / 360.0
        return days / 365.25  # act/365.25 par défaut
