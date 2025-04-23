import os
from abc import ABC
from structured_products_pricing.Utils.Data import Data

class Volatility(ABC):
    def __init__(self):
        self.options_data = None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.path_file = os.path.join(current_dir, "TSLA_BBG_DATA.xlsx")

    def import_data(self):
        data_import = Data()
        self.options_data = data_import.import_data_excel(self.path_file, "CallPut")