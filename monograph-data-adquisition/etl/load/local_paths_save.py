import pandas as pd
from logger import setup_logger
import json

class LocalPathsLoad:
    logger = setup_logger()

    def __init__(self) -> None:
        self.param1=None
    
    def local_path_save_file(self,df: pd.DataFrame, path: str, file_name: str) -> json:
        """
        Reads a file from a local path and returns its content as a pandas DataFrame.

        Args:
            path (str): The path of the directory where the file is located.
            file_name (str): The name of the file to read.

        Returns:
            pd.DataFrame: A pandas DataFrame with the content of the file.
        """
        file_path = f"{path}\{file_name}"
        self.logger.info(f'Start save File - {file_path}')
        try:
            df.to_csv(file_path, index=False)
            self.logger.info('File readed corretly')
            return {'StatusCode':200, 'Message':'Data saved Sucessful!!!'}
        except FileNotFoundError:
            self.logger.error(f"File {file_name} is saved in path {path}")
            return  {'StatusCode':501, 'Message':'File {file_name} is saved in path {path}'}
        except Exception as e:
            self.logger.error(f"An error occurred while saving file {file_name}: {e}")
            return  {'StatusCode':501, 'Message':'An error occurred while saving file {file_name}: {e}'}
