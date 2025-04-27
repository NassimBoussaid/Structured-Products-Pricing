from structured_products_pricing.Parameters import Pricer
from structured_products_pricing.Rate.RateCurve import RateCurve
from structured_products_pricing.Rate.RateFlat import RateFlat
from structured_products_pricing.Rate.RateStochastic import RateStochastic
import numpy as np


def get_stochastic_rates(interest_rate: float, time_to_maturity: float, nb_steps: int, nb_draws: int):
    """
    Generate stochastic interest rate paths and their associated discount factors.

    Parameters:
        interest_rate (float): Initial interest rate at time t=0.
        time_to_maturity (float): Total time horizon (in years).
        nb_steps (int): Number of time steps.
        nb_draws (int): Number of Monte Carlo simulation paths.

    Returns:
        rates_path (np.ndarray): Simulated interest rate paths, shape (nb_draws, nb_steps+1).
        df_path (np.ndarray): Corresponding discount factors between steps, shape (nb_draws, nb_steps).

    Notes:
        - rates_path[:, 0] corresponds to time 0.
        - df_path[:, i] discounts cashflows from t_i to t_{i+1}.
    """
    dt = time_to_maturity / nb_steps

    sto_rates = RateStochastic(interest_rate, 0.5, 0.03, 0.07, time_to_maturity)
    sto_rates.compute_stochastic_rates(nb_steps, nb_draws)

    rates_path = sto_rates.rates.T

    df_path = np.exp(-rates_path[:, :] * dt)

    return rates_path, df_path


def get_deterministic_rates(interest_rate: float,
                            rate_mode: str,
                            time_to_maturity: float,
                            pricer: Pricer):
    """
    Generate deterministic interest rate paths and cumulative discount factors.

    Depending on the pricer type ('Tree' vs others), either returns:
    - Only rates for tree-based models,
    - Or full broadcasted rates paths and discount factors for Monte Carlo / deterministic simulations.

    Parameters:
        interest_rate (float): Initial constant rate if 'constant' rate_mode is selected.
        rate_mode (str): Either 'constant', 'rate curve' or 'stochastic rate'
        time_to_maturity (float): Total time horizon (in years).
        pricer (Pricer): Pricer object containing pricer_name, nb_steps, and nb_draws attributes.

    Returns:
        rates (np.ndarray): Zero-coupon rates
        rates_path (np.ndarray or None): Broadcasted rates across all paths (only for non-tree pricers).
        df (np.ndarray or None): Cumulative discount factors across paths (only for non-tree pricers).
    """
    if rate_mode.lower() == 'constant':
        rate_curve = RateFlat(rate=interest_rate)

    else:
        rate_curve = RateCurve(0.01, 0.01, 0.01, 1)
        rate_curve.compute_yield_curve()

    dt = time_to_maturity / pricer.nb_steps

    # Time grid: t_0, t_1, ..., t_nb_steps
    t_grid = np.arange(0, pricer.nb_steps + 1) * dt

    # Spot rates at each time step
    rates = np.array([rate_curve.get_yield(t) for t in t_grid])

    # Broadcast the rates to all paths
    if pricer.pricer_name == "Tree":
        rates_path = None
        df = None
    else:
        rates_path = np.broadcast_to(rates[np.newaxis, :], (pricer.nb_draws, rates.size))

        # Cumulative sum of rates * dt
        cum_rates = np.cumsum(rates_path * dt, axis=1)
        # Discount factors = exp(-int_0^t r(s) ds)
        df = np.exp(-cum_rates)

    return rates, rates_path, df


def generate_rates_paths(mode: str,
                         time_to_maturity: float,
                         pricer: Pricer,
                         interest_rate: float = None):
    """
    Dispatch function to generate rates, rates_path, and discount factors depending on the mode.

    Depending on the mode ('stochastic rate' or deterministic), the function:
    - Calls stochastic rate generation using CIR model if mode is 'stochastic rate'.
    - Calls deterministic generation from a flat or fitted yield curve otherwise.

    Parameters:
        mode (str): 'stochastic rate' or 'curve rate' or 'constant' mode.
        time_to_maturity (float): Total time horizon (in years).
        pricer (Pricer): Pricer object containing nb_steps, nb_draws, and pricer_name attributes.
        interest_rate (float, optional): Initial interest rate. Mandatory if mode is 'stochastic rate'.

    Returns:
        rates (np.ndarray or None): Zero-coupon rates (for deterministic mode) or None (for stochastic mode).
        rates_path (np.ndarray): Simulated or broadcasted rates across all paths.
        df (np.ndarray): Corresponding cumulative discount factors across time steps and paths.
    """
    mode = mode.lower()

    if mode == "stochastic rate":
        if interest_rate is None:
            raise ValueError("interest_rate must be provided for stochastic rate generation.")
        rates_path, df = get_stochastic_rates(
            interest_rate=interest_rate,
            time_to_maturity=time_to_maturity,
            nb_steps=pricer.nb_steps,
            nb_draws=pricer.nb_draws
        )
        rates = None  # not used in stochastic mode

    else:
        rates, rates_path, df = get_deterministic_rates(
            interest_rate=interest_rate,
            rate_mode=mode,
            time_to_maturity=time_to_maturity,
            pricer=pricer)

    return rates, rates_path, df
