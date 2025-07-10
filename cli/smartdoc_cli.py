# smartdoc_cli.py
import typer
from pathlib import Path
from shared.compressor import compress_pdf
from shared.ocr_engine import extract_text
from shared.converter import convert_doc

app = typer.Typer()

@app.command()
def compress(
    input: Path = typer.Argument(..., exists=True, help="Input PDF file"),
    mode: str = typer.Option("balanced", "--mode", "-m", help="Compression mode: fast, balanced, extreme")
):
    try:
        output = compress_pdf(str(input), mode)
        typer.echo(f"✅ Compressed file saved to: {output}")
    except Exception as e:
        typer.echo(f"❌ Compression failed: {e}", err=True)

@app.command()
def ocr(
    input: Path = typer.Argument(..., exists=True, help="Image file for OCR"),
    lang: str = typer.Option("eng", "--lang", "-l", help="OCR language (e.g. eng, mya)"),
    format: str = typer.Option("text", "--format", "-f", help="Output format: text or json")
):
    try:
        result = extract_text(str(input), lang=lang, output_format=format)
        typer.echo(result if isinstance(result, str) else result.get("text", ""))
    except Exception as e:
        typer.echo(f"❌ OCR failed: {e}", err=True)

@app.command()
def convert(
    input: Path = typer.Argument(..., exists=True, help="Input file"),
    to: str = typer.Option("pdf", "--to", "-t", help="Output format: pdf, docx, txt")
):
    try:
        output = convert_doc(str(input), to)
        typer.echo(f"🔁 Converted file saved to: {output}")
    except Exception as e:
        typer.echo(f"❌ Conversion failed: {e}", err=True)

if __name__ == "__main__":
    app()
