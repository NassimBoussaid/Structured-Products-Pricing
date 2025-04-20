import numpy as np

class RegressionModel:
    """
    Class to compute polynomial regression using different basis functions.
    """
    def __init__(self, choice: str, degree: int):
        """
        Initializes RegressionModel.

        Parameters:
        - choice: str. Type of regression polynomials.
        - degree: int. Degree of the specified regression polynomials.
        """
        self.choice = choice
        self.coefficients = None
        self.degree = degree

    def classic_basis(self, X: np.array) -> np.array:
        """
        Generates the classic polynomial design matrix.

        Parameters:
        - X: np.array. Input data array.

        Returns:
        - X_matrix: np.array. The design matrix using classic polynomials up to the specified degree.
        """
        X_matrix = np.ones((len(X), self.degree + 1))
        for i in range(1, self.degree + 1):
            X_matrix[:, self.degree - i] = X ** i
        return X_matrix

    def laguerre_basis(self, X: np.array) -> np.array:
        """
        Generates the Laguerre polynomial design matrix.

        Parameters:
        - X: np.array. Input data array.

        Returns:
        - X_matrix: np.array. The design matrix using Laguerre polynomials up to the specified degree.
        """
        X_matrix = np.ones((len(X), self.degree + 1))

        if self.degree >= 1:
            X_matrix[:, self.degree - 1] = -X + 1
        if self.degree >= 2:
            X_matrix[:, self.degree - 2] = 0.5 * (X ** 2 - 4 * X + 2)
        if self.degree >= 3:
            X_matrix[:, self.degree - 3] = 1 / 6 * (-X ** 3 + 9 * X ** 2 - 18 * X + 6)
        if self.degree >= 4:
            X_matrix[:, self.degree - 4] = 1 / 24 * (X ** 4 - 16 * X ** 3 + 72 * X ** 2 - 96 * X + 24)
        if self.degree >= 5:
            X_matrix[:, self.degree - 5] = 1 / 120 * (-X ** 5 + 25 * X ** 4 - 200 * X ** 3 + 600 * X ** 2
                                                      - 600 * X + 120)
        if self.degree >= 6:
            X_matrix[:, self.degree - 6] = 1 / 720 * (X ** 6 - 36 * X ** 5 + 450 * X ** 4 - 2400 * X ** 3
                                                      + 5400 * X ** 2 - 4320 * X + 720)

        return X_matrix

    def hermite_basis(self, X: np.array) -> np.array:
        """
        Generates the Hermite polynomial design matrix.

        Parameters:
        - X: np.array. Input data array.

        Returns:
        - X_matrix: np.array. The design matrix using Hermite polynomials up to the specified degree.
        """
        X_matrix = np.ones((len(X), self.degree + 1))

        if self.degree >= 1:
            X_matrix[:, self.degree - 1] = X
        if self.degree >= 2:
            X_matrix[:, self.degree - 2] = X ** 2 - 1
        if self.degree >= 3:
            X_matrix[:, self.degree - 3] = X ** 3 - 3 * X
        if self.degree >= 4:
            X_matrix[:, self.degree - 4] = X ** 4 - 6 * X ** 2 + 3
        if self.degree >= 5:
            X_matrix[:, self.degree - 5] = X ** 5 - 10 * X ** 3 + 15 * X
        if self.degree >= 6:
            X_matrix[:, self.degree - 6] = X ** 6 - 15 * X ** 4 + 45 * X ** 2 - 15

        return X_matrix

    def legendre_basis(self, X: np.array) -> np.array:
        """
        Generates the Legendre polynomial design matrix.

        Parameters:
        - X: np.array. Input data array.

        Returns:
        - X_matrix: np.array. The design matrix using Legendre polynomials up to the specified degree.
        """
        X_matrix = np.ones((len(X), self.degree + 1))

        if self.degree >= 1:
            X_matrix[:, self.degree - 1] = X
        if self.degree >= 2:
            X_matrix[:, self.degree - 2] = 0.5 * (3 * X ** 2 - 1)
        if self.degree >= 3:
            X_matrix[:, self.degree - 3] = 0.5 * (5 * X ** 3 - 3 * X)
        if self.degree >= 4:
            X_matrix[:, self.degree - 4] = 1 / 8 * (35 * X ** 4 - 30 * X ** 2 + 3)
        if self.degree >= 5:
            X_matrix[:, self.degree - 5] = 1 / 8 * (63 * X ** 5 - 70 * X ** 3 + 15 * X)
        if self.degree >= 6:
            X_matrix[:, self.degree - 6] = 1 / 16 * (231 * X ** 6 - 315 * X ** 4 + 105 * X ** 2 - 5)

        return X_matrix

    def tchebychev_basis(self, X: np.array) -> np.array:
        """
        Generates the Tchebychev polynomial design matrix.

        Parameters:
        - X: np.array. Input data array.

        Returns:
        - X_matrix: np.array. The design matrix using Tchebychev polynomials up to the specified degree.
        """
        X_matrix = np.ones((len(X), self.degree + 1))

        if self.degree >= 1:
            X_matrix[:, self.degree - 1] = X
        if self.degree >= 2:
            X_matrix[:, self.degree - 2] = 2 * X ** 2 - 1
        if self.degree >= 3:
            X_matrix[:, self.degree - 3] = 4 * X ** 3 - 3 * X
        if self.degree >= 4:
            X_matrix[:, self.degree - 4] = 8 * X ** 4 - 8 * X ** 2 + 1
        if self.degree >= 5:
            X_matrix[:, self.degree - 5] = 16 * X ** 5 - 20 * X ** 3 + 5 * X
        if self.degree >= 6:
            X_matrix[:, self.degree - 6] = 32 * X ** 6 - 48 * X ** 4 + 18 * X ** 2 - 1

        return X_matrix

    def fit(self, X: np.array, y: np.array) -> np.array:
        """
        Fits the regression model to the input data using the specified regression polynomials and degree.

        Parameters:
        - X: np.array. Input data array.
        - y: np.array. Target data array.

        Returns:
        - self.coefficients: np.array. Least square solution to a linear matrix equation.
        """
        if self.choice == "Classic":
            X_matrix = self.classic_basis(X)
        elif self.choice == "Laguerre":
            X_matrix = self.laguerre_basis(X)
        elif self.choice == "Hermite":
            X_matrix = self.hermite_basis(X)
        elif self.choice == "Legendre":
            X_matrix = self.legendre_basis(X)
        elif self.choice == "Tchebychev":
            X_matrix = self.tchebychev_basis(X)

        self.coefficients = np.linalg.lstsq(X_matrix, y, rcond=None)[0]
        return self.coefficients

    def predict(self, X: np.array) -> np.array:
        """
        Computes the output for the input data using the previously fitted regression model.

        Parameters:
        - X: np.array. Input data array.

        Returns:
        - np.array. Predicted output values.
        """
        if self.choice == "Classic":
            X_matrix = self.classic_basis(X)
        elif self.choice == "Laguerre":
            X_matrix = self.laguerre_basis(X)
        elif self.choice == "Hermite":
            X_matrix = self.hermite_basis(X)
        elif self.choice == "Legendre":
            X_matrix = self.legendre_basis(X)
        elif self.choice == "Tchebychev":
            X_matrix = self.tchebychev_basis(X)

        return X_matrix @ self.coefficients