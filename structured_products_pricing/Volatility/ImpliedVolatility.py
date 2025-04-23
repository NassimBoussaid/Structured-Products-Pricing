import math
from datetime import datetime
from typing import Dict
import copy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d, griddata
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Products.Options.OptionPricerBS import OptionPricerBS
from structured_products_pricing.Parameters.ModelParams import ModelParams
from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
#from Interpolation import Interpolation
from structured_products_pricing.Volatility.Volatility import Volatility


class ImpliedVolatility(Volatility):

    def __init__(self):
        super().__init__()
        self.convergence_limit = 0.01
        self.iteration_limit = 100
        self.first_guess = 0.65
        self.second_guess = 0.45
        self.volatility_surface = None


    def initialize_surface(self,market: Market, option: OptionEuropean, pricer: PricerBase):
        self.volatility_surface = self.compute_implied_volatility(market, option, pricer)

    def compute_implied_volatility(self, mkt: Market, opt: OptionEuropean, pricer: PricerBase):
        self.import_data()
        df = self.options_data.copy()

        # Calcul du temps jusqu'à maturité
        df['time_to_maturity'] = df['Maturity'].apply(lambda d: (d - pricer.pricing_date).days / 365)

        def compute_row_iv(row):
            opt_copy = OptionEuropean(
                option_type=row["Type"].lower(),
                strike=row["Strike"],
                maturity_date=row["Maturity"]
            )
            mkt_copy = copy.copy(mkt)
            mkt_copy.vol = self.first_guess
            mkt_copy.int_rate = row["Rate"]

            return self.newton_raphson(row["Mid Price"], mkt_copy, opt_copy, pricer)

        df['implied_vol'] = df.apply(compute_row_iv, axis=1)
        df['time_to_maturity'] *= 365

        surface = (
            df[['time_to_maturity', 'Strike', 'implied_vol']]
            .pivot_table(columns="time_to_maturity", index="Strike", values="implied_vol")
            .dropna()
        )
        return surface

    def newton_raphson(self, market_price, mkt: Market, opt: OptionEuropean, pricer: PricerBase):

        implied_vol = mkt.vol

        for i in range(self.iteration_limit):
            params = ModelParams(mkt, opt, pricer)
            bs = OptionPricerBS(params)
            theoretical_price = bs.compute_price()
            vega = bs.vega() * 100
            gap = theoretical_price - market_price
            implied_vol = mkt.vol - gap / vega

            if abs(gap) < self.convergence_limit or abs(mkt.vol - implied_vol) < self.convergence_limit:
                implied_vol = mkt.vol
                break

            if vega == 0:
                implied_vol = self.second_guess

            mkt.vol = implied_vol

        return implied_vol

    def get_volatility(self, strike: float, time_to_maturity: float) -> float:
        surface = self.volatility_surface

        if time_to_maturity in surface.columns and strike in surface.index:
            return surface.at[strike, time_to_maturity]

        X, Y = np.meshgrid(surface.columns.values, surface.index.values)
        Z = surface.values

        try:
            vol = griddata(
                points=(X.flatten(), Y.flatten()),
                values=Z.flatten(),
                xi=(time_to_maturity, strike),
                method='linear'
            )
            if not np.isnan(vol):
                return float(vol)
        except Exception:
            pass

        try:
            nearest_maturity = min(surface.columns, key=lambda x: abs(x - time_to_maturity))
            vol_slice = surface[nearest_maturity].dropna()
            f_interp = interp1d(vol_slice.index, vol_slice.values, kind='linear', fill_value='extrapolate')
            return float(f_interp(strike))
        except Exception:
            pass

        try:
            nearest_strike = min(surface.index, key=lambda x: abs(x - strike))
            vol_slice = surface.loc[nearest_strike].dropna()
            f_interp = interp1d(vol_slice.index, vol_slice.values, kind='linear', fill_value='extrapolate')
            return float(f_interp(time_to_maturity))
        except Exception:
            pass

        raise ValueError("Impossible d'interpoler la volatilité pour les valeurs fournies.")
    def plot_volatility_surface(self):
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        x = self.volatility_surface.columns.values  # Strikes
        y = self.volatility_surface.index.values  # Time to maturity
        z = self.volatility_surface.values  # Implied vol

        X, Y = np.meshgrid(x, y)

        surf = ax.plot_surface(X, Y, z, cmap='viridis', edgecolor='none')

        ax.set_title("Volatility Surface")
        ax.set_xlabel("Time to Maturity (days)")
        ax.set_ylabel("Strike")
        ax.set_zlabel("Implied Volatility")

        fig.colorbar(surf, shrink=0.5, aspect=10)
        plt.tight_layout()
        plt.show()


