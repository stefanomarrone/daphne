import uvicorn
from fastapi import APIRouter, UploadFile, File


router = APIRouter()
@router.post("/matforpat")
def postrepomodel(configuration_name: str):
    #todo: complete the method
    pass
    return {"success": True}

uvicorn.run(router,port=1812)