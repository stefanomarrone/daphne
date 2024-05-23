#   QUESTA PARTE DEVE ANDARE NEL MAIN PRINCIPALE AL POSTO DEL IF __NAME__== MAIN

from fastapi import APIRouter, FastAPI
import uvicorn
from conf import conf
import json

router = APIRouter()

@router.get("/write_json")
def write_json ():
    result = conf() #in result ci sarà il nome del file json da leggere

    data = json.load(open(result)) #in data apriamo il file json e lo leggiamo

    return str(data) #stampiamo in web il file json


app = FastAPI()
app.include_router(router)
uvicorn.run(app, port = 4415)