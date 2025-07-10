import pytesseract
from pytesseract import TesseractNotFoundError
from PIL import Image

def extract_text(image_path, lang="eng", output_format="text"):
    try:
        image = Image.open(image_path)
        if output_format == "json":
            data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
            return json.loads(json.dumps(data))
        else:
            text = pytesseract.image_to_string(image, lang=lang)
            return {"text": text}
    except TesseractNotFoundError:
        raise