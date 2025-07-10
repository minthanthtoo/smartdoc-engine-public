from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from shared.ocr_engine import extract_text
import tempfile
import os
from pytesseract import TesseractNotFoundError

router = APIRouter()

@router.post("/ocr")
async def ocr_file(file: UploadFile = File(...), lang: str = "eng", format: str = "text"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(await file.read())
        temp_file.flush()
        temp_file_path = temp_file.name

    try:
        result = extract_text(temp_file_path, lang=lang, output_format=format)
    except TesseractNotFoundError:
        raise HTTPException(status_code=500, detail="Tesseract is not installed on the server.")
    finally:
        os.unlink(temp_file_path)  # delete temp file after processing

    if format.lower() == "text":
        return PlainTextResponse(content=result)
    else:
        return JSONResponse(content={"result": result})