from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.extraction_service import extract_text_from_image

router = APIRouter()

@router.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    return await extract_text_from_image(file)  