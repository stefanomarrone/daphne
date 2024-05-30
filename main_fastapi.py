from typing import List
from fastapi import FastAPI, requests
import requests
from pydantic import BaseModel
import uvicorn

from src.core import grab


# Definisci il modello dei dati JSON
class Item(BaseModel):
    name: str
    content: str


class Configurations(BaseModel):
    configurations: List[Item]

app = FastAPI()

#Endpoint che legge Json
@app.post("/execute/") #router.get
def create_item(item: Configurations):

    #todo: estrarre il contenuto delle configurazioni dal json
    for configuration in configurationnames:
        grab(configuration)
    return {"item": item}



uvicorn.run(app,port=4416)



