import pandas as pd

class AWSExtract:
    def __init__(self) -> None:
        self.param1=None
    
    def s3_extract(self) -> pd.DataFrame:
        raise NotImplementedError


    