# Final Work Machine Learning II 

**Presented by:**

  Jorge Ignacio Morales - Laura Isabel Barrera Echeverri
  
  ***Universidad de Antioquia***

Predicción de resultados de permeabilidad en la toma de muestras de un laboratorio

**1.** **Problem Statement**: To predict the permeability of a packaging material in the market.

It seeks to provide value to the laboratory team as there is currently no guide value that allows approving or rejecting this quality characteristic, which implies a potential risk of delivering defective products to customers.

**2.** **Course techniques used**: 

**PCA**

- Why: To reduce dimensionality of model variables that are highly correlated.
- Where in the pipeline: In the Data Acquisition process, in the pre-loading transformation stage of the Feature Store.

**Explained Variance**

- Why: To evaluate the proportion of accumulated explained variance and select the minimum number of components. With just one component, 100% of the variance can be captured

**3.** **Model results:**: R2, MAE, MSE metrics

**4.** **Deployment**: Projects focused on the MLOps structure.


ML2MLOPSMONOGRAPH/

  monographDataAdquisition/

  monographEvalperformance/

  monographInference/

  monographTraining/

  storage/




## MLOps stages:
**monographDataAdquisition/**: batch execution process. Connection to the information source to bring in raw data and store it in the Feature Store. It contains an ETL of extraction, transformation, and loading.

The process is a scheduled task that runs at a defined frequency.

```linux
python .\monographDataAdquisition\main.py
```


**monographEvalperformance/**: batch and on-demand execution process, which could be programmed with N frequencies to observe model behavior and experiment with them.

It is implemented with the MLFlow tool, and its dashboard can be viewed with the following command:

```linux
cd monographEvalperformance
mlflow ui
```

**monographInference/**: an API is being made available on demand, which needs to be tested with the data to identify a record and send it.

To start the service, run the following command:
```linux
cd monographInference
unvicorn api_inference:inferenceApi --reload --port 8001
```

To consume the API, it must be done through the POST method with the following structure:

URL: localhost:8001/inference

METHOD: POST

BODY:

```JSON
{
  "version":"0.1",
  "data_test":{
    "Muestra":1,
    "Grados_C":25.6,
    "Porc_Humedad":23,
    "Estructura" : "BOPP",
    "Calibre1": 16.4,
    "Calibre2": 16.4,
    "Calibre3": 16.4,
    "Calibre4": 16.4,
    "Calibre5": 16.4,
    "CalibreProm": 16.4
  }
}
```

**monographTraining/**: an API is being made available on demand, and the model to be trained, the version, and the size of the data to be tested can be invoked.

```linux
cd monographTraining
unvicorn api_train:train_api --reload --port 8000
```

To consume the API, it must be done through the POST method with the following structure:

URL: localhost:8000/train

METHOD: POST

BODY:

```JSON
{
  "model":"LinearRegression",
  "version": "0.1",
  "test_size":0.25
}
```

It contains a data_layer layer where the training is executed to generate a model.


**storage/**: contains 3 base folders, data, logs, models.

data: Here we will manage all the raw and processed data ready to be consumed by the models stored in the feature store.

logs: Here we will manage the logs of the different projects.

models: In this folder, we will store productive models at the version level.


- **IMPORTANT!!** The "permeability" database is excluded in the ".gitignore" file as it contains confidential client information.

If it is required to execute it, it will be provided to the professor by email.

