from data_layer.data_layer import GetDataFeautureStore
from models.model_factory import ModelFactory
import numpy as np

if __name__ == "__main__":

    get_data = GetDataFeautureStore(type_source="local_path")
    x_train, x_test, y_train, y_test = get_data.split_data(target_col='Permeabilidad',test_size=0.25)

    linearRegression = ModelFactory().create_model(model_name='LinearRegression')
    linearRegression.fit(x_test,y_test)
    x_test.replace(np.nan,0,inplace=True)
    
    y_test.replace(to_replace='NaN.',value=0)
    x_test = x_test.where(x_test != np.nan)
    x_test = y_test.where(y_test != np.nan)

    RandomForestRegressor = ModelFactory().create_model('RandomForestRegressor')
    svr = ModelFactory().create_model('SVR')