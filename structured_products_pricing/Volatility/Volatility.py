import os
from abc import ABC
from structured_products_pricing.Utils.Data import Data

class Volatility(ABC):
    def __init__(self):
        """
        Initialize the Volatility class, setting up the file path for options data.

        Attributes:
        - options_data: DataFrame. Holds the options data once imported.
        - path_file: str. Path to the Excel file containing options data.
        """
        self.options_data = None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.path_file = os.path.join(current_dir, "TSLA_BBG_DATA.xlsx")

    def import_data(self):
        """
        Imports options data from an Excel file into the options_data attribute.
        This method uses the Data class to read the 'CallPut' sheet from the specified Excel file.

        Returns:
        - None. The data is directly stored in the options_data attribute.
        """
        data_import = Data()
        self.options_data = data_import.import_data_excel(self.path_file, "CallPut")