import streamlit as st
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# تحديد مسار Tesseract (غيره حسب نظامك)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\youss\Downloads\tesseract-ocr-w64-setup-5.5.0.20241111.exe"  # للويندوز

# دالة لاستخراج النص من الصورة
def extract_text_from_image(image, lang="ara+eng"):
    text = pytesseract.image_to_string(image, lang=lang)
    return text

# دالة لاستخراج النص من PDF
def extract_text_from_pdf(pdf_path, lang="ara+eng"):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang=lang) + "\n"
    return text

# واجهة Streamlit
st.title("📄 OCR Text Extractor (Image & PDF)")
st.write("Upload an image or a PDF to extract text.")

uploaded_file = st.file_uploader("Upload Image/PDF", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    file_type = uploaded_file.type
    if file_type in ["image/png", "image/jpeg", "image/jpg"]:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        extracted_text = extract_text_from_image(image)
    elif file_type == "application/pdf":
        pdf_path = f"temp_{uploaded_file.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())
        extracted_text = extract_text_from_pdf(pdf_path)
        os.remove(pdf_path)
    else:
        st.error("Unsupported file format!")
        extracted_text = None

    if extracted_text:
        st.subheader("📝 Extracted Text:")
        st.text_area("", extracted_text, height=300)
