from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.ModelParams import ModelParams
from structured_products_pricing.Parameters.Market import Market
from abc import ABC, abstractmethod
import numpy as np

from structured_products_pricing.Rate.RateStochastic import RateStochastic


class OptionPricerBase(ABC):
    """
    Abstract base class to handle the structure of option pricers.
    """

    def __init__(self, model_params: ModelParams):
        """
        Initializes an OptionPricerBase.

        Parameters:
        - model_params: ModelParams. Aggregated market, option, and pricer parameters.
        """
        self.Market: Market = model_params.Market
        self.Option: OptionBase = model_params.Option
        self.Pricer: PricerBase = model_params.Pricer
        if self.Pricer.pricer_name == "MC" or self.Pricer.pricer_name == "Tree":
            self.dt = self.Option.time_to_maturity / self.Pricer.nb_steps
            t_grid = np.arange(0, self.Pricer.nb_steps + 1) * self.dt

            self.vol_curve = np.array([self.Market.vol.get_volatility(self.Option.strike, t) for t in t_grid])

            self.rates_path = None
            if self.Market.rate_mode == "stochastic rate":
                sto_rates = RateStochastic(self.Market.int_rate, 0.5, 0.03, 0.07, self.Option.time_to_maturity)
                sto_rates.compute_stochastic_rates(self.Pricer.nb_steps, self.Pricer.nb_draws)
                self.rates_path = sto_rates.rates
                self.df = np.exp(- self.rates_path[:, 1:] * self.dt)

            else:
                self.rates = np.array([self.Market.rates.get_yield(t) for t in t_grid])

                self.rates_path: np.array = np.broadcast_to(self.rates[np.newaxis, :],
                                                            (self.Pricer.nb_draws, self.rates.size))
                cum_rates = np.cumsum(self.rates_path * self.dt, axis=1)
                self.df = np.exp(-cum_rates[:, :])

    @abstractmethod
    def compute_price(self) -> float:
        """
        Abstract method to compute the option price.

        Returns:
        - float. The computed option price.
        """
        pass
