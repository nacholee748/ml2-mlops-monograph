import mlflow
from abc import ABC, abstractmethod


class Model(ABC):
    """
    An abstract base class for machine learning models.
    """

    @abstractmethod
    def fit(self, x_train, y_train):
        """
        Train the model on the training data.

        Parameters
        ----------
        X_train : array-like of shape (n_samples, n_features)
            The training feature data.
        y_train : array-like of shape (n_samples,)
            The training target data.
        """

    @abstractmethod
    def predict(self, x_train):
        """
        Make predictions on the test data.

        Parameters
        ----------
        X_test : array-like of shape (n_samples, n_features)
            The test feature data.

        Returns
        -------
        array-like of shape (n_samples,)
            The predicted target data.
        """

    def evaluate(self, x_test, y_test, run_name):
        """
        Evaluate the model on the test data and log the results to MLflow.

        Parameters
        ----------
        x_test : array-like of shape (n_samples, n_features)
            The test feature data.
        y_test : array-like of shape (n_samples,)
            The test target data.
        run_name : str
            The name of the MLflow run.
        """
        y_pred = self.predict(x_test)

        from metrics.metrics import mean_squared_error, mean_absolute_error, r2_score
        mean_squared_error = mean_squared_error(y_test, y_pred)
        mean_absolute_error = mean_absolute_error(y_test, y_pred)
        r2_score = r2_score(y_test, y_pred)

        with mlflow.start_run(run_name=run_name):
            mlflow.log_metric("mean_squared_error", mean_squared_error)
            mlflow.log_metric("mean_absolute_error", mean_absolute_error)
            mlflow.log_metric("r2_score", r2_score)
