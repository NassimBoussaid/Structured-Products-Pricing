import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


class RateStochastic:
    def __init__(self, r0, a, b, sigma, T):
        self.r0 = r0
        self.a = a
        self.b = b
        self.T = T
        self.sigma = sigma
        self.rates = None

    def cir(self, num_steps, num_paths, dt):
        self.rates = np.zeros((num_steps + 1, num_paths))
        self.rates[0] = self.r0
        dW = np.random.normal(0, 1, (num_steps, num_paths))
        for t in range(1, num_steps + 1):
            sqrt_r = np.sqrt(np.maximum(self.rates[t - 1], 0))
            self.rates[t] = self.rates[t - 1] + self.a * (self.b - self.rates[t - 1]) * dt + \
                            self.sigma * sqrt_r * np.sqrt(dt) * dW[t - 1]
            self.rates[t] = np.maximum(self.rates[t], 0)

    def calibrate_LS(self, dt):
        r0 = self.rates[:-1, 0].reshape(-1, 1)
        r1 = self.rates[1:, 0]
        reg = LinearRegression().fit(r0, r1)

        a_LS = (1 - reg.coef_[0]) / dt
        b_LS = reg.intercept_ / (dt * a_LS)

        epsilon = r1 - reg.predict(r0)

        sigma_LS = np.std(epsilon) / (np.sqrt(np.mean(r0)) * np.sqrt(dt))

        self.a = a_LS
        self.b = b_LS
        self.sigma = sigma_LS

    def compute_stochastic_rates(self, num_steps, num_paths):
        dt = self.T / num_steps
        self.cir(num_steps, 1, dt)
        self.calibrate_LS(dt)
        self.cir(num_steps, num_paths, dt)

    def plot_rates(self):
        if self.rates is None:
            print("No rates computed")
            return

        num_steps = self.rates.shape[0] - 1
        num_paths = self.rates.shape[1]
        time_grid = np.linspace(0, self.T, num_steps + 1)

        plt.figure(figsize=(10, 5))
        for i in range(min(10, num_paths)):
            plt.plot(time_grid, self.rates[:, i], lw=1)

        plt.title("Stochastic rates using CIR model")
        plt.xlabel("Time")
        plt.ylabel("Rates")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
