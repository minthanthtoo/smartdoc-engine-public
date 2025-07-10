from PIL import Image
from PyPDF2 import PdfReader
import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def file_size(path):
    return os.path.getsize(path)

def pdf_to_image(path):
    from pdf2image import convert_from_path
    images = convert_from_path(path, dpi=100)
    return images[0]  # take first page for quick comparison

def calculate_ssim(pdf1, pdf2):
    img1 = np.array(pdf_to_image(pdf1).convert('L'))
    img2 = np.array(pdf_to_image(pdf2).convert('L'))
    score, _ = ssim(img1, img2, full=True)
    return score
