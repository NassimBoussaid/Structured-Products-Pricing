from structured_products_pricing.Utils.Brownian import Brownian
from structured_products_pricing.Parameters.ModelParams import ModelParams
from structured_products_pricing.Utils.Calendar import Calendar
from structured_products_pricing.Utils.RegressionModel import RegressionModel
from structured_products_pricing.Products.Options.OptionPricerBase import OptionPricerBase
import numpy as np

class OptionPricerMC(OptionPricerBase):
    """
    Class to compute option prices using Monte Carlo.
    """
    def __init__(self, model_params: ModelParams):
        """
        Initializes MonteCarlo.

        Parameters:
        - model_params: ModelParams. Market, Option and Pricer parameters.
        """
        super().__init__(model_params)

    def compute_asset_price(self, brownian_paths: np.array, full_paths: bool = False,
                            use_incremental_method: bool = False) -> np.array:
        """
        Computes asset price using Brownian motions in a vectorial way.

        Parameters:
        - brownian_paths: np.array. A 2D numpy array of shape (nb_draws, nb_steps + 1), where each row represents
        an independent Brownian motion.
        - full_paths: bool. Determines whether the function returns only the final asset prices or the entire
        asset price paths.
        - use_incremental_method: bool. Determines which discretization schemes to use. Useful for dividends.

        Returns:
        - S_t: np.array. Asset prices as an array.
        """
        if self.Market.div_discrete > 0:
            # Calculate the step on which the dividend occurs
            step_div = int(self.Market.time_to_div / self.dt) + 1
            # Compute the simulated asset price before the dividend step
            S_pre_div: np.array = (self.Market.und_price
                                   * np.exp(np.cumsum((self.Market.int_rate - 0.5 * self.Market.vol ** 2)
                                                      * self.dt + self.Market.vol
                                                      * (brownian_paths[:, 1: step_div]
                                                         - brownian_paths[:, :step_div - 1]), axis=1)))
            # Compute the simulated asset price after the dividend step
            S_post_div: np.array = ((S_pre_div[:, -1][:, np.newaxis] - self.Market.div_discrete)
                                   * np.exp(np.cumsum((self.Market.int_rate - 0.5 * self.Market.vol ** 2)
                                                      * self.dt + self.Market.vol
                                                      * (brownian_paths[:, step_div:]
                                                         - brownian_paths[:, step_div - 1: -1]), axis=1)))
            # Merge the simulated asset price before and after the dividend step
            S_t = np.hstack((S_pre_div, S_post_div))
        elif use_incremental_method:
            # Compute the simulated asset price at maturity
            S_t: np.array = (self.Market.und_price
                             * np.exp((self.Market.int_rate - self.Market.div_rate - 0.5 * self.Market.vol ** 2)
                                      * (self.dt * np.arange(self.Pricer.nb_steps + 1))[np.newaxis, :]
                                      + self.Market.vol * brownian_paths))
        else:
            # Extract the final Brownian motion values
            final_brownian_values: np.array = brownian_paths[:, -1]
            # Compute the simulated asset price at maturity
            S_T: np.array = (self.Market.und_price
                             * np.exp((self.Market.int_rate - self.Market.div_rate - 0.5 * self.Market.vol ** 2)
                                      * self.Option.time_to_maturity + self.Market.vol * final_brownian_values))
            return S_T

        if full_paths:
            return S_t
        else:
            return S_t[:, -1]

    def calculate_standard_deviation(self, payoff: np.array) -> float:
        """
        Calculates the standard deviation of the option payoff.

        Parameters:
        - payoff: np.array. The simulated payoff values from the Monte Carlo simulation.

        Returns:
        - std: float. The standard deviation of the payoff, adjusted for the number of draws.
        """
        std: float = np.std(payoff) / np.sqrt(self.Pricer.nb_draws)

        return std

    def compute_price(self) -> float:
        """
        Computes European option price using Monte Carlo simulations based on vector Brownian motions.

        Returns:
        - price: np.array. Option price as a float.
        """
        # Initialize the Brownian motion class
        brownian_simulator: Brownian = Brownian(self.Option.time_to_maturity, self.Pricer.nb_steps, self.Pricer.nb_draws,
                                                self.Pricer.seed)
        # Generate independent Brownian motion paths
        brownian_paths: np.array = brownian_simulator.MotionVector()
        # Compute the simulated asset price at maturity
        if (self.Option.option_name == "Barrier" and self.Option.barrier_exercise == "American") or self.Option.option_name == "Asian":
            S_T: np.array = self.compute_asset_price(brownian_paths, full_paths=True, use_incremental_method=True)
        else:
            S_T: np.array = self.compute_asset_price(brownian_paths)
        # Compute the average payoff of the option
        payoff: float = self.Option.payoff(S_T)
        # Compute the standard deviation
        std: float = self.calculate_standard_deviation(payoff)
        # Discount the expected payoff back to present value
        price: float = np.mean(payoff) * np.exp(-self.Market.int_rate * self.Option.time_to_maturity)

        # return np.array((price, std))
        return np.array(price)

    def compute_autocall_probabilities(self, autocall_barrier: float, frequency: str):
        """
        Computes the probabilities of an autocall event at each observation date based on Monte Carlo simulations.

        Parameters:
        - autocall_barrier: float. The barrier level triggering an autocall.
        - frequency: str. Observation frequency ("monthly", "quarterly", etc.).

        Returns:
        - dict. Dictionary containing:
            - "observation_dates": List of observation dates.
            - "autocall_prob": List of autocall probabilities at each observation.
            - "duration": Expected duration of the product (in years).
        """
        # Initialize the Brownian motion class
        brownian_simulator: Brownian = Brownian(self.Option.time_to_maturity, self.Pricer.nb_steps, self.Pricer.nb_draws,
                                                self.Pricer.seed)
        # Generate independent Brownian motion paths
        brownian_paths: np.array = brownian_simulator.MotionVector()
        # Compute the simulated asset price at maturity
        S_t: np.array = self.compute_asset_price(brownian_paths, full_paths=True, use_incremental_method=True)
        # Set up calendar and observations
        calendar = Calendar(self.Pricer.pricing_date, self.Option.maturity_date, frequency)
        time_to_obs = [(observation - self.Pricer.pricing_date).days / 365 for observation in calendar.observation_dates]
        # Map each observation time to the corresponding time step index
        obs_steps = [int(observation / self.dt) + 1 for observation in time_to_obs]
        obs_steps[-1] = self.Pricer.nb_steps
        # Initialize breach tracking: tracks if a path already triggered an autocall
        already_breached = np.array([False] * len(S_t))
        autocall_prob = []
        # Iterate over each observation step
        for step in obs_steps:
            prices = S_t[:, step]
            new_breach = np.logical_and(prices > autocall_barrier, ~already_breached)
            already_breached[new_breach] = True
            autocall_prob.append(float(np.sum(new_breach) / len(S_t)))
        # Adjust the final autocall probability to ensure the total sums to 1
        autocall_prob[-1] = round(1 - sum(autocall_prob), 3)
        # Compute the expected duration as the weighted average of observation times
        duration = np.dot(time_to_obs, autocall_prob)

        return {"observation_dates": calendar.observation_dates, "autocall_prob": autocall_prob, "duration": duration}

    def price_LS(self) -> float:
        """
        Computes American option price using Longstaff-Schwartz algorithm.

        Returns:
        - price: np.array. Option price as a float.
        """
        # Initialize the Brownian motion class
        brownian_simulator: Brownian = Brownian(self.Option.time_to_maturity, self.Pricer.nb_steps, self.Pricer.nb_draws,
                                                self.Pricer.seed)
        # Generate independent Brownian motion paths
        brownian_paths: np.array = brownian_simulator.MotionVector()
        # Generate independent Brownian motion paths & Compute the simulated asset price at maturity
        S_t: np.array = self.compute_asset_price(brownian_paths, use_incremental_method=True, full_paths=True)
        # Initialize the Regression class
        regression = RegressionModel(self.Option.regression_type, self.Option.regression_degree)
        # At maturity, the payoff is the same as a European option
        cashflow = self.Option.payoff(S_t[:, -1])
        # Loop over the number of time steps
        for i in reversed(range(2, self.Pricer.nb_steps + 1)):
            # Discount cashflow from the next period
            cashflow *= self.df
            # Store asset price for the current period
            X = S_t[:, i-1]
            # Compute the payoff
            exercise = self.Option.payoff(X)
            # Keep paths eligible for regression (ITM paths)
            itm = exercise > 0
            # Perform regression on eligible paths
            regression.fit(X[itm], cashflow[itm])
            # Compute continuation value
            continuation = regression.predict(X)
            # Store paths for which exercise decision is optimal
            ex_idx = itm & (exercise > continuation)
            # Set paths for which exercise decision is optimal to the payoff value
            cashflow[ex_idx] = exercise[ex_idx]
        # Perform discounting of the cashflow matrix
        cashflow *= self.df
        # Compute the average discounted value for all paths
        price = np.mean(cashflow)
        # Compute the standard deviation
        std = self.calculate_standard_deviation(cashflow)

        # return np.array((price, std))
        return np.array(price)