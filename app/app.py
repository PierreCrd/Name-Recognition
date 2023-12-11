import logging
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from utils.rule_based_model import RuleBasedModel
from utils.schemas import OCRData

app = FastAPI()
model = RuleBasedModel()
logging.basicConfig(level=logging.WARNING)

@app.post("/predict")
def predict(ocr_output: OCRData):
    text = ocr_output.get_text()
    output = model.predict(text)
    return output

