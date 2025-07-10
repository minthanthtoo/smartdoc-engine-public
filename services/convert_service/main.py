# api/convert.py
import os
import tempfile
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from shared.converter import convert_doc

router = APIRouter()

@router.post("/")
async def convert_file(file: UploadFile = File(...), to: str = "pdf"):
    # Extract extension (e.g., ".docx")
    extension = os.path.splitext(file.filename)[-1]
    if not extension.startswith("."):
        extension = f".{extension}"
    if not extension:
        extension = ".tmp"

    # Create a secure temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
        temp_file.write(await file.read())
        temp_file.flush()
        temp_file_path = temp_file.name

    # Convert the file
    try:
        output_path = convert_doc(temp_file_path, to)
    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}

    # Return result
    media_type = "application/pdf" if to == "pdf" else "application/octet-stream"
    return FileResponse(
        output_path,
        media_type=media_type,
        filename=f"converted.{to}"
    )