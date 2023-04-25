import pandas as pd

class GCPExtract:
    def __init__(self) -> None:
        self.param1=None
    
    def cloud_storage_extract(self) -> pd.DataFrame:
        raise NotImplementedError

