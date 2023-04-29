from pickle import load
from config import MODEL_CURRENT_VERSION

class Inference:
    """
    Inference Class
    """

    def __init__(self,version: str,data_test: dict) -> None:
        self.version = version
        self.data_test = data_test

    def test(self):
        # Cargar el modelo desde la ruta
        model = load(MODEL_CURRENT_VERSION)
        predicted = model.predict(self.data_test)

        return predicted