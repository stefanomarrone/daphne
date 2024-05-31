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
    for configurations in item.configurations:
        content = configurations.content
        grab(content)
    return {"item": item}



uvicorn.run(app,port=4416)



