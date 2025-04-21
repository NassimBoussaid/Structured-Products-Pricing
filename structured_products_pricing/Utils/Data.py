import pandas as pd


class Data:
    def import_data_excel(self, path_file, sheet_name):
        return pd.read_excel(path_file, sheet_name=sheet_name)