import pdfWrite
from typing import Union
from fastapi import FastAPI
import os
WIDTH = 0
HEIGHT = 0
 
app = FastAPI()
 
@app.get("/")
def read_root():
    os.system("pdfWrite.py")
    return {"PDF": "Written"}