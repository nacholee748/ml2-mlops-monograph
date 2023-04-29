import numpy as np
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, r2_score


class Metrics:
    """
    A class for calculating evaluation metrics for machine learning models.
    """

    @staticmethod
    def accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate the accuracy score.

        Parameters
        ----------
        y_true : np.ndarray
            The true labels.
        y_pred : np.ndarray
            The predicted labels.

        Returns
        -------
        float
            The accuracy score.
        """
        return accuracy_score(y_true, y_pred)

    @staticmethod
    def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate the mean squared error.

        Parameters
        ----------
        y_true : np.ndarray
            The true labels.
        y_pred : np.ndarray
            The predicted labels.

        Returns
        -------
        float
            The mean squared error.
        """
        return mean_squared_error(y_true, y_pred)

    @staticmethod
    def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate the mean absolute error.

        Parameters
        ----------
        y_true : np.ndarray
            The true labels.
        y_pred : np.ndarray
            The predicted labels.

        Returns
        -------
        float
            The mean absolute error.
        """
        return mean_absolute_error(y_true, y_pred)

    @staticmethod
    def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate the R-squared score.

        Parameters
        ----------
        y_true : np.ndarray
            The true labels.
        y_pred : np.ndarray
            The predicted labels.

        Returns
        -------
        float
            The R-squared score.
        """
        return r2_score(y_true, y_pred)
