from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from shared.compressor import compress_pdf
import tempfile
import os
import magic  # pip install python-magic

router = APIRouter()

SUPPORTED_MIME = {"application/pdf"}
SUPPORTED_EXT = {".pdf"}

@router.post("/compress")
async def compress_file(file: UploadFile = File(...), mode: str = "balanced"):
    filename = file.filename.lower()
    ext = os.path.splitext(filename)[-1]

    if ext not in SUPPORTED_EXT:
        return JSONResponse(
            status_code=400,
            content={
                "error": "❌ Unsupported file type.",
                "supported_types": list(SUPPORTED_EXT),
                "filename": file.filename
            }
        )

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_input:
        content = await file.read()
        temp_input.write(content)
        temp_input.flush()

        # Check MIME type using python-magic
        mime = magic.from_file(temp_input.name, mime=True)
        if mime not in SUPPORTED_MIME:
            os.unlink(temp_input.name)
            return JSONResponse(
                status_code=400,
                content={
                    "error": "❌ Invalid file content.",
                    "detected_mime": mime,
                    "expected": list(SUPPORTED_MIME)
                }
            )

        # Run compression and catch failure
        try:
            output_path = compress_pdf(temp_input.name, mode)
        except Exception as e:
            os.unlink(temp_input.name)
            return JSONResponse(
                status_code=500,
                content={
                    "error": f"❌ Compression failed.",
                    "details": str(e),
                    "tip": "Ensure the PDF is not encrypted or corrupted."
                }
            )

    return FileResponse(output_path, media_type="application/pdf", filename="compressed.pdf")