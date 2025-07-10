from shared.ocr_engine import extract_text
from difflib import SequenceMatcher
import os

def test_ocr_accuracy():
    input_img = "datasets/scans/sample_invoice.png"
    ground_truth_path = "datasets/ground_truth/sample_invoice.txt"

    extracted = extract_text(input_img, lang="eng")["text"]
    with open(ground_truth_path, "r") as f:
        expected = f.read()

    accuracy = SequenceMatcher(None, extracted.strip(), expected.strip()).ratio()
    print(f"🧪 OCR Accuracy: {accuracy:.2%}")

    assert accuracy > 0.85
