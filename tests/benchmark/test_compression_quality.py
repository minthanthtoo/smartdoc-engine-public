import os
import time
from shared.compressor import compress_pdf
from tests.utils.metrics import calculate_ssim, file_size

def test_pdf_compression():
    input_pdf = "datasets/pdfs/sample.pdf"
    original_size = file_size(input_pdf)

    start = time.time()
    output_pdf = compress_pdf(input_pdf, mode="balanced")
    duration = time.time() - start

    compressed_size = file_size(output_pdf)
    ratio = (original_size - compressed_size) / original_size * 100

    print(f"✅ Size reduced by {ratio:.2f}% in {duration:.2f}s")

    ssim_score = calculate_ssim(input_pdf, output_pdf)
    print(f"🧠 SSIM (Visual Fidelity): {ssim_score:.3f}")

    assert ratio > 20  # expect >20% reduction
    assert ssim_score > 0.85

