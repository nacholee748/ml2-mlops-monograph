from fastapi import FastAPI, File, UploadFile
import numpy as np
from trainer import Trainer

train_api = FastAPI()


@train_api.get("/")
def read_root():
    return {"Message": "API - Monograph"}

# Realiza la inferencia
@train_api.post("/train/")
async def train(model: str,version: str,test_size: float):
    trainer = Trainer(model= model,version = version,test_size = test_size)
    result = trainer.train()
    return result

