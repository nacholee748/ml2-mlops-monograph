from logger import setup_logger
from config import RAW_DATA_PATH, FEAUTURE_DATA_PATH,FILE_NAME_PERMEABILITY
from etl.extraction.local_paths_extract import LocalPathsExtract
from etl.transform.permeability_transform import PermeabilityTransoform
from etl.load.local_paths_save import LocalPathsLoad
import pandas as pd

logger_etl = setup_logger()

def etl_permeability_feauture_store()->None:
    logger_etl.info('Starting ETL permeability Process')

    extract = LocalPathsExtract()
    raw_data = extract.local_path_read_file(path=RAW_DATA_PATH,file_name=FILE_NAME_PERMEABILITY)
    logger_etl.info('Extract Data Sucessfull')

    transform = PermeabilityTransoform(df_raw=raw_data)
    data_transformed = transform.clean_permability()

    load = LocalPathsLoad()
    restult = load.local_path_save_file(df=data_transformed,path=FEAUTURE_DATA_PATH,file_name="data_processed.csv")

    print(restult)


if __name__ == '__main__':
    etl_permeability_feauture_store()
