# shared/converter.py
import subprocess
import os
import shutil

def convert_doc(input_path, to_format):
    ext = os.path.splitext(input_path)[-1].lower()
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(os.path.dirname(input_path), f"{base_name}.{to_format}")

    print(f"Converting '{input_path}' to '{output_path}' using format '{to_format}'")

    # Prefer libreoffice
    if shutil.which("libreoffice"):
        cmd = [
            "libreoffice", "--headless", "--convert-to", to_format,
            "--outdir", os.path.dirname(input_path), input_path
        ]
        subprocess.run(cmd, check=True)
        return output_path

    elif shutil.which("soffice"):
        cmd = [
            "soffice", "--headless", "--convert-to", to_format,
            "--outdir", os.path.dirname(input_path), input_path
        ]
        subprocess.run(cmd, check=True)
        return output_path

    # Fallback to docx2pdf if converting .docx -> .pdf
    elif ext == ".docx" and to_format == "pdf":
        try:
            from docx2pdf import convert
            convert(input_path, output_path)
            return output_path
        except ImportError:
            raise RuntimeError("Missing docx2pdf. Install via: pip install docx2pdf")

    # Fallback to pandoc for basic conversions
    elif shutil.which("pandoc"):
        cmd = ["pandoc", input_path, "-o", output_path]
        subprocess.run(cmd, check=True)
        return output_path

    else:
        raise RuntimeError("❌ No valid conversion tool found (libreoffice, docx2pdf, or pandoc)")