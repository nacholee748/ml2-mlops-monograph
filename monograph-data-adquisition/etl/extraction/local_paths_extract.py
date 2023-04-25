import pandas as pd
from logger import setup_logger

class LocalPathsExtract:
    logger = setup_logger()

    def __init__(self) -> None:
        self.param1=None
    
    def local_path_read_file(self,path: str, file_name: str) -> pd.DataFrame:
        """
        Reads a file from a local path and returns its content as a pandas DataFrame.

        Args:
            path (str): The path of the directory where the file is located.
            file_name (str): The name of the file to read.

        Returns:
            pd.DataFrame: A pandas DataFrame with the content of the file.
        """
        file_path = f"{path}\{file_name}"
        self.logger.info(f'Start read File - {file_path}')
        try:
            df = pd.read_excel(file_path)
            self.logger.info('File readed corretly')
            return df
        except FileNotFoundError:
            self.logger.error(f"File {file_name} not found in path {path}")
            return None
        except Exception as e:
            self.logger.error(f"An error occurred while reading file {file_name}: {e}")
            return None
