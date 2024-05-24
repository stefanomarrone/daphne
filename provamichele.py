import json
import os
from typing import List

from fastapi import FastAPI, requests
import requests
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Definisci il modello dei dati JSON
class Item(BaseModel):
    name: str
    content: str
class Configurations(BaseModel):
    configurations: List[Item]


#Endpoint che legge Json
@app.post("/items/") #router.get
async def create_item(item: Configurations):
    return {"item": item}

uvicorn.run(app,port=4416)



