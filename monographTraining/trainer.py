from data_layer.data_layer import GetDataFeautureStore
from models.model_factory import ModelFactory
from config import MODELS_ARTIFACTS_PATH
from joblib import dump,load
import os

class Trainer:
    """
    A class for training and evaluating machine learning models.
    """

    def __init__(self, model: str,version: str,test_size: float):
        """
        Initialize the Trainer class.

        Parameters
        ----------
        version : str
            The preprocessed dataset to use for training and testing.
        model : str
            The machine learning model to train and test.
        """
        self.version = version
        self.model = model
        self.test_size = test_size

    def train(self) -> dict:
        """
        Train the machine learning model and evaluate its performance.

        Returns
        -------
        Tuple[float, float]
            The accuracy and F1 score of the trained model.
        """

        get_data = GetDataFeautureStore(type_source="local_path")
        x_train, x_test, y_train, y_test = get_data.split_data(target_col='Permeabilidad',test_size=self.test_size)
        
        training_model = ModelFactory().create_model(model_name=self.model)
        training_model.fit(x_test,y_test)

        model_path = f"{MODELS_ARTIFACTS_PATH}\\{self.version}\\model.joblib"
        if not os.path.exists(os.path.dirname(model_path)):
            os.makedirs(os.path.dirname(model_path))
        dump(training_model,model_path )

        restult = {"StatusCode":200, "Message": f"Model {self.model} trained with in the version: {self.version}"}
        
        return restult