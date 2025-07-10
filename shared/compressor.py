import subprocess
import os

def compress_pdf(input_path, mode="balanced"):
    quality = {
        "fast": "/screen",
        "balanced": "/ebook",
        "extreme": "/printer"
    }.get(mode, "/ebook")

    output_path = input_path.replace(".pdf", "_compressed.pdf")
    command = [
        "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={quality}",
        "-dNOPAUSE", "-dQUIET", "-dBATCH",
        f"-sOutputFile={output_path}", input_path
    ]
    subprocess.run(command, check=True)
    return output_path
