from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from shared.ocr_engine import extract_text
import tempfile

router = APIRouter()

@router.post("/ocr")
async def ocr_file(file: UploadFile = File(...), lang: str = "eng", format: str = "text"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(await file.read())
        temp_file.flush()

        result = extract_text(temp_file.name, lang=lang, output_format=format)
        return JSONResponse(content=result)
