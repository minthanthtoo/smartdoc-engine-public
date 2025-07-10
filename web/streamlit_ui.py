import streamlit as st
from PIL import Image
import pytesseract
import json
import tempfile
import os
from shared.compressor import compress_pdf
from shared.converter import convert_doc

st.set_page_config(page_title="📂 SmartDoc Engine", layout="centered")

st.title("📂 SmartDoc Engine")
tabs = st.tabs(["🧠 OCR", "📦 Compress PDF", "🔁 Convert File"])

# ========================
# TAB 1: OCR
# ========================
with tabs[0]:
    st.header("🧠 OCR: Image to Text/JSON")
    ocr_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"], key="ocr")
    lang = st.selectbox("Language", ["eng", "mya", "jpn", "chi_sim"], index=0)
    fmt = st.radio("Output Format", ["text", "json"], horizontal=True)

    if ocr_file and st.button("🚀 Run OCR"):
        image = Image.open(ocr_file)
        st.image(image, caption="Preview", use_column_width=True)

        with st.spinner("Extracting..."):
            if fmt == "json":
                data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
                st.success("✅ Done")
                st.json(data)
            else:
                text = pytesseract.image_to_string(image, lang=lang)
                st.success("✅ Done")
                st.text_area("OCR Result", text, height=300)

# ========================
# TAB 2: Compress
# ========================
with tabs[1]:
    st.header("📦 Compress PDF")
    pdf_file = st.file_uploader("Upload PDF to compress", type=["pdf"], key="compress")
    mode = st.selectbox("Compression Mode", ["fast", "balanced", "extreme"])

    if pdf_file and st.button("🚀 Compress PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_file.read())
            tmp.flush()
            input_path = tmp.name

        with st.spinner("Compressing..."):
            try:
                output_path = compress_pdf(input_path, mode)
                st.success("✅ Compression successful")
                with open(output_path, "rb") as f:
                    st.download_button("⬇️ Download Compressed PDF", f, file_name="compressed.pdf")
            except Exception as e:
                st.error(f"❌ Compression failed: {e}")

# ========================
# TAB 3: Convert
# ========================
with tabs[2]:
    st.header("🔁 Convert Files")
    conv_file = st.file_uploader("Upload file to convert", type=["pdf", "docx", "txt"], key="convert")
    to_format = st.selectbox("Convert to format", ["pdf", "docx", "txt"])

    if conv_file and st.button("🚀 Convert File"):
        ext = os.path.splitext(conv_file.name)[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(conv_file.read())
            tmp.flush()
            input_path = tmp.name

        with st.spinner("Converting..."):
            try:
                output_path = convert_doc(input_path, to_format)
                st.success("✅ Conversion successful")
                with open(output_path, "rb") as f:
                    st.download_button("⬇️ Download Converted File", f, file_name=f"converted.{to_format}")
            except Exception as e:
                st.error(f"❌ Conversion failed: {e}")