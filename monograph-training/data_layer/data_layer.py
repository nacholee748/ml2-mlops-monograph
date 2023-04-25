import pandas as pd
from typing import Tuple
from config import FEAUTURE_DATA_PATH

class GetDataFeautureStore:
    """
    A class for loading and handling datasets.

    Attributes
    ----------
    data_path : str
        The path to the data file.
    """

    def __init__(self, type_source: str):
        """
        Parameters
        ----------
        data_path : str
            The path to the data file.
        """
        self.type_source = type_source

    def get_local_path(self) -> pd.DataFrame:
        """
        Load the dataset from disk.

        Returns
        -------
        pd.DataFrame
            The loaded dataset.
        """

        # self.logger.info(f'Start read File - {file_path}')
        try:
            feauture_store_path = FEAUTURE_DATA_PATH
            file_name = 'data_processed.csv'
            file_path = f"{feauture_store_path}\{file_name}"

            return pd.read_csv(file_path)
        except FileNotFoundError as e:
            # self.logger.error(f"File {file_name} not found in path {path}")
            return e
        except Exception as e:
            # self.logger.error(f"An error occurred while reading file {file_name}: {e}")
            return e
                

    def split_data(self, target_col: str, test_size: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split the dataset into training and test sets.

        Parameters
        ----------
        target_col : str
            The name of the target column.
        test_size : float
            The proportion of data to include in the test set.

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame]
            The training and test sets.
        """

        if self.type_source == 'local_path':
            data = self.get_local_path()
        else:
            raise ModuleNotFoundError
        
        target = data[target_col]
        features = data.drop(columns=[target_col])

        from sklearn.model_selection import train_test_split
        return train_test_split(features, target, test_size=test_size, random_state=42)
