from logger import setup_logger
from config import RAW_DATA_PATH, FEAUTURE_DATA_PATH
from etl.extraction.local_paths_extract import LocalPathsExtract
from etl.transform.permeability_transform import PermeabilityTransoform
from etl.load.local_paths_save import LocalPathsLoad
import pandas as pd

logger = setup_logger()

def etl_permeability_feauture_store()->None:
    logger.info('Starting ETL permeability Process')
    source_path = RAW_DATA_PATH
    file_name = 'Permeabilidad.xlsx'

    extract = LocalPathsExtract()
    raw_data = extract.local_path_read_file(path=source_path,file_name=file_name)
    logger.info('Extract Data Sucessfull')

    transform = PermeabilityTransoform(df_raw=raw_data)
    data_transformed = transform.clean_permability()

    load = LocalPathsLoad()
    restult = load.local_path_save_file(df=data_transformed,path=FEAUTURE_DATA_PATH,file_name="data_processed.csv")


    print(restult)

    # output_path = 'transformed_data.csv'
    # transformed_data = transform_data(raw_data)
    # load_data(transformed_data, output_path)


if __name__ == '__main__':
    etl_permeability_feauture_store()

#     logger.info('Starting ETL process...')
#     raw_data = extract_data(RAW_DATA_PATH)
#     transformed_data = transform_data(raw_data)
#     load_data(transformed_data, TRANSFORMED_DATA_PATH)
#     logger.info('ETL process completed successfully.')
