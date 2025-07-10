# tests/benchmark/run.py
from test_ocr_accuracy import test_ocr_accuracy
from test_compression_quality import test_pdf_compression

def run_all():
    print("🧪 Running Benchmarks...")
    test_pdf_compression()
    test_ocr_accuracy()

if __name__ == "__main__":
    run_all()
