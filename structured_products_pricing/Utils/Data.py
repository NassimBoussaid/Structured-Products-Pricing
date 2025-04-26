import pandas as pd

class Data:
    def import_data_excel(self, path_file, sheet_name):
        """
        Imports data from an Excel file.

        Parameters:
        - path_file: str. Path to the Excel file.
        - sheet_name: str. Name of the sheet to import data from.

        Returns:
        - pd.DataFrame. Dataframe containing the data from the specified sheet.
        """
        return pd.read_excel(path_file, sheet_name=sheet_name)