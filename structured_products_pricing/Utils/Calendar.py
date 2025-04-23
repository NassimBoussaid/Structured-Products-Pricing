from datetime import datetime
import pandas as pd

class Calendar:
    """
    Classe de gestion du calendrier de trading :
    Gestion des jours de trading et des dates de rebalancement en fonction des fréquences spécifiées,
    en tenant compte des jours fériés fédéraux aux États-Unis.
    """

    FREQUENCY_MAPPING = {
        'monthly': 'ME',
        'quarterly': 'QE',
        'yearly': 'YE',
    }

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
        self.observation_dates = self._generate_observation_dates()

    def _generate_observation_dates(self) -> set[datetime]:
        """
        Génération des dates de rebalancement en fonction de la fréquence et de la plage de dates.

        :return: Ensemble des dates de rebalancement.
        """
        freq_alias = self.FREQUENCY_MAPPING[self.frequency]
        observation_dates = pd.date_range(start=self.start_date, end=self.end_date, freq=freq_alias).to_pydatetime()
        observation_dates[-1] = self.end_date.to_pydatetime()
        return observation_dates