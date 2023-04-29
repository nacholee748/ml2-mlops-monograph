from fastapi import FastAPI, File, UploadFile
import numpy as np
from inference import Inference

inferenceApi = FastAPI()

@inferenceApi.get("/")
def read_root():
    return {"Message": "API - Monograph - Testing"}

# Realiza la inferencia
@inferenceApi.post("/inference/")
async def inference(version: str,data_test: dict):
    inference = Inference(version= version,data_test = data_test)
    result = inference.test()
    return result

