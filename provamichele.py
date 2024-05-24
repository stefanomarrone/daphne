from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Definisci il modello dei dati JSON
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

#Endpoint che legge Json
@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}




uvicorn.run(app,port=4416)
