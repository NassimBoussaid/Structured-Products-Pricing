import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import fmin
from structured_products_pricing.Utils.Data import Data

def nelson_siegel(maturities, beta0, beta1, beta2, lambda1):
    """Apply the Nelson-Siegel formula to maturities."""
    with np.errstate(divide='ignore', invalid='ignore'):
        factor1 = (1 - np.exp(-maturities / lambda1)) / (maturities / lambda1)
        factor2 = factor1 - np.exp(-maturities / lambda1)
        ns_curve = beta0 + beta1 * factor1 + beta2 * factor2
    return ns_curve


class RateCurve:
    def __init__(self, beta0, beta1, beta2, lambda1):
        self.initial_params = [beta0, beta1, beta2, lambda1]
        self.yield_curve = None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(current_dir, "yields_data.xlsx")
        self.rates_data = Data().import_data_excel(excel_path, "yields")

    def get_yield(self, t):
        """Return the yield for the specified maturity and interpolate the curve"""

        if self.yield_curve is None:
            raise ValueError("Yield curve has not been computed yet. Call compute_yield_curve() first.")

        maturities = self.yield_curve['Maturity'].values
        yields = self.yield_curve['NS'].values

        interpolator = interp1d(maturities, yields, kind='linear', fill_value='extrapolate')
        return float(interpolator(t))

    def compute_yield_curve(self):
        """Calibrate and compute the Nelson-Siegel yield curve."""
        best_params = fmin(self._calibration_error, self.initial_params, disp=False)
        maturities = self.rates_data['Maturity'].values
        ns_yields = nelson_siegel(maturities, *best_params)
        self.yield_curve = pd.DataFrame({
            'Maturity': maturities,
            'NS': ns_yields
        })

    def _calibration_error(self, params):
        """Objective function for calibration."""
        maturities = self.rates_data['Maturity'].values
        actual_yields = self.rates_data['Yields'].values
        model_yields = nelson_siegel(maturities, *params)
        return np.sum((actual_yields - model_yields) ** 2)

    def plot_yield_curve(self):
        """Plot the Nelson-Siegel yield curve after calibration."""
        if self.yield_curve is None:
            raise ValueError("Yield curve has not been computed yet. Call compute_yield_curve() first.")

        plt.figure(figsize=(10, 6))
        plt.plot(self.yield_curve['Maturity'], self.yield_curve['NS'], marker='o', linestyle='-', color='royalblue')
        plt.title("Nelson-Siegel Yield Curve", fontsize=14)
        plt.xlabel("Maturity", fontsize=12)
        plt.ylabel("Yield (%)", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()
