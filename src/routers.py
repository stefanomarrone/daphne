import glob
from src.configuration import folderextraction
from src.core import grab
from src.mongodb import MongoWriter
from src.models import *
from fastapi import APIRouter


router = APIRouter()
@router.post("/execute")
async def create_item(item: Experiments):
    for configurations in item.configurations:
        name = configurations.name
        content = configurations.content
        folder = folderextraction(content)
        writer = MongoWriter(router.mongodb_address, router.mongodb_port)
        grab(content)
        #todo: improve the feedback to the user
        for file in glob.glob(folder + "/*"):
            result = writer.write(name, file)
    return {"item": item}


