from typing import Tuple
import mlflow
import mlflow.sklearn
from training.model import Model
from data_layer.data_layer import Dataset
from metrics.metrics import Metrics


class Trainer:
    """
    A class for training and evaluating machine learning models.
    """

    def __init__(self, dataset: Dataset, model: Model):
        """
        Initialize the Trainer class.

        Parameters
        ----------
        dataset : Dataset
            The preprocessed dataset to use for training and testing.
        model : Model
            The machine learning model to train and test.
        """
        self.dataset = dataset
        self.model = model

    def train(self) -> Tuple[float, float]:
        """
        Train the machine learning model and evaluate its performance.

        Returns
        -------
        Tuple[float, float]
            The accuracy and F1 score of the trained model.
        """
        x_train, x_test, y_train, y_test = self.dataset.split_data()

        with mlflow.start_run():
            self.model.fit(x_train, y_train)
            y_pred = self.model.predict(x_test)

            accuracy = Metrics.accuracy(y_test, y_pred)
            f1_score = Metrics.f1_score(y_test, y_pred)

            mlflow.log_param("model_name", self.model.name)
            mlflow.log_param("model_params", self.model.get_params())
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("f1_score", f1_score)

            mlflow.sklearn.log_model(self.model, "model")

       
