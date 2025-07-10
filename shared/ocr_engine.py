import pytesseract
from PIL import Image
import json

def extract_text(img_path, lang="eng", output_format="text"):
    image = Image.open(img_path)

    if output_format == "json":
        data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
        return json.loads(json.dumps(data))
    else:
        text = pytesseract.image_to_string(image, lang=lang)
        return {"text": text}
