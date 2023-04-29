from fastapi import FastAPI, File, UploadFile
import numpy as np
from inference import Inference

test_api = FastAPI()


@test_api.get("/")
def read_root():
    return {"Message": "API - Monograph - Testing"}

# Realiza la inferencia
@test_api.post("/test/")
async def train(version: str,data_test: dict):
    inference = Inference(version= version,data_test = data_test)
    result = inference.test()
    return result

