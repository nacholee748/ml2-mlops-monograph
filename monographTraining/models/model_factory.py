from typing import Dict
from models.model import Model

class ModelFactory:
    """
    A factory class for creating machine learning models.
    """

    def create_model(self, model_name: str, model_params: Dict = {}) -> Model:
        """
        Create a new machine learning model.

        Parameters
        ----------
        model_name : str [LinearRegression |  ]
            The name of the machine learning model to create.
        model_params : dict
            A dictionary of parameters to pass to the machine learning model.

        Returns
        -------
        Model
            The created machine learning model.
        """
        if model_name == "LinearRegression":
            from sklearn.linear_model import LinearRegression
            return LinearRegression(**model_params)
        elif model_name == "RandomForestRegressor":
            from sklearn.ensemble import RandomForestRegressor
            return RandomForestRegressor(**model_params)
        elif model_name == "SVR":
            from sklearn.svm import SVR
            return SVR(**model_params)
        else:
            raise ValueError(f"Unknown model name '{model_name}'.")
