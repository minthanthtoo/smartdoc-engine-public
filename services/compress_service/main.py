from fastapi import APIRouter, File, UploadFile
from shared.compressor import compress_pdf
from fastapi.responses import FileResponse
import tempfile

router = APIRouter()

@router.post("/")
async def compress_file(file: UploadFile = File(...), mode: str = "balanced"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        temp_input.write(await file.read())
        temp_input.flush()

        output_path = compress_pdf(temp_input.name, mode)

    return FileResponse(output_path, media_type="application/pdf", filename="compressed.pdf")
