from structured_products_pricing.Utils.Data import Data
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from scipy.optimize import fmin
import pandas as pd
import numpy as np
import os

def nelson_siegel(maturities, beta0, beta1, beta2, lambda1):
    """
    Apply the Nelson-Siegel formula to a set of maturities.

    Parameters:
    - maturities: np.array. Array of maturities.
    - beta0, beta1, beta2: float. Nelson-Siegel model coefficients.
    - lambda1: float. Decay factor.

    Returns:
    - np.array. Computed yields for each maturity.
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        factor1 = (1 - np.exp(-maturities / lambda1)) / (maturities / lambda1)
        factor2 = factor1 - np.exp(-maturities / lambda1)
        ns_curve = beta0 + beta1 * factor1 + beta2 * factor2
    return ns_curve


class RateCurve:
    """
    Class to represent and calibrate a yield curve using the Nelson-Siegel model.
    """
    def __init__(self, beta0, beta1, beta2, lambda1):
        """
        Initializes curve parameters

        Parameters:
        - beta0, beta1, beta2: float. Initial guesses for model coefficients.
        - lambda1: float. Initial guess for decay parameter.
        """
        self.initial_params = [beta0, beta1, beta2, lambda1]
        self.yield_curve = None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(current_dir, "yields_data.xlsx")
        self.rates_data = Data().import_data_excel(excel_path, "yields")

    def get_yield(self, t):
        """
        Return the interpolated yield for a specified maturity.

        Parameters:
        - t: float. Maturity.

        Returns:
        - float. Interpolated yield.
        """

        if self.yield_curve is None:
            raise ValueError("Yield curve has not been computed yet. Call compute_yield_curve() first.")

        maturities = self.yield_curve['Maturity'].values
        yields = self.yield_curve['NS'].values

        interpolator = interp1d(maturities, yields, kind='linear', fill_value='extrapolate')
        return float(interpolator(t))

    def compute_yield_curve(self):
        """
        Calibrate the Nelson-Siegel model and compute the yield curve.
        """
        best_params = fmin(self._calibration_error, self.initial_params, disp=False)
        maturities = self.rates_data['Maturity'].values
        ns_yields = nelson_siegel(maturities, *best_params)
        self.yield_curve = pd.DataFrame({
            'Maturity': maturities,
            'NS': ns_yields
        })

    def _calibration_error(self, params):
        """
        Objective function for Nelson-Siegel calibration (sum of squared errors).

        Parameters:
        - params: list. Model parameters [beta0, beta1, beta2, lambda1].

        Returns:
        - float. Calibration error.
        """
        maturities = self.rates_data['Maturity'].values
        actual_yields = self.rates_data['Yields'].values
        model_yields = nelson_siegel(maturities, *params)
        return np.sum((actual_yields - model_yields) ** 2)

    def plot_yield_curve(self):
        """
        Plot the calibrated Nelson-Siegel yield curve.
        """
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
