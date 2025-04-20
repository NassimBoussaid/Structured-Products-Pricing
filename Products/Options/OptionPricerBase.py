from Parameters.Market import Market
from Parameters.Option.OptionBase import OptionBase
from Parameters.Pricer.PricerBase import PricerBase
from Parameters.ModelParams import ModelParams
from abc import ABC, abstractmethod
import numpy as np

class OptionPricerBase(ABC):
    def __init__(self, model_params: ModelParams):
        self.Market: Market = model_params.Market
        self.Option: OptionBase = model_params.Option
        self.Pricer: PricerBase = model_params.Pricer
        if self.Pricer.pricer_name == "MC" or self.Pricer.pricer_name == "Tree":
            self.dt = self.Option.time_to_maturity / self.Pricer.nb_steps
            self.df = np.exp(-self.Market.int_rate * self.dt)

    @abstractmethod
    def compute_price(self):
        pass