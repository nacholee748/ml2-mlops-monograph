from data_layer.data_layer import GetDataFeautureStore
from models.model_factory import ModelFactory
import mlflow
from config import MODELS_ARTIFACTS_PATH
from joblib import dump,load

# def evaluate(model,x_test, y_test, run_name):
#         """
#         Evaluate the model on the test data and log the results to MLflow.

#         Parameters
#         ----------
#         x_test : array-like of shape (n_samples, n_features)
#             The test feature data.
#         y_test : array-like of shape (n_samples,)
#             The test target data.
#         run_name : str
#             The name of the MLflow run.
#         """

#         y_pred = model.predict(x_test)

#         from metrics.metrics import mean_squared_error, mean_absolute_error, r2_score
#         mean_squared_error = mean_squared_error(y_test, y_pred)
#         mean_absolute_error = mean_absolute_error(y_test, y_pred)
#         r2_score = r2_score(y_test, y_pred)

#         with mlflow.start_run(run_name=run_name):
#             mlflow.log_metric("mean_squared_error", mean_squared_error)
#             mlflow.log_metric("mean_absolute_error", mean_absolute_error)
#             mlflow.log_metric("r2_score", r2_score)

#         with mlflow.start_run():
#         self.model.fit(x_train, y_train)
#         y_pred = self.model.predict(x_test)

#         accuracy = Metrics.accuracy(y_test, y_pred)
#         f1_score = Metrics.f1_score(y_test, y_pred)

#         mlflow.log_param("model_name", self.model.name)
#         mlflow.log_param("model_params", self.model.get_params())
#         mlflow.log_metric("accuracy", accuracy)
#         mlflow.log_metric("f1_score", f1_score)

#         mlflow.sklearn.log_model(self.model, "model")

#         mlflow.search_experiments()
#         mlflow.log_figure()

if __name__ == "__main__":

    get_data = GetDataFeautureStore(type_source="local_path")
    x_train, x_test, y_train, y_test = get_data.split_data(target_col='Permeabilidad',test_size=0.25)

    linearRegression = ModelFactory().create_model(model_name='LinearRegression')
    linearRegression.fit(x_test,y_test)
    dump(linearRegression, "model.joblib")

    RandomForestRegressor = ModelFactory().create_model('RandomForestRegressor')



    svr = ModelFactory().create_model('SVR')