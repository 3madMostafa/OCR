import streamlit as st
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import platform
import tempfile

# Detect OS and set Tesseract path
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
elif platform.system() == "Darwin":  # macOS
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
# On Linux, Tesseract is typically installed in /usr/bin/tesseract

# Function to extract text from images
def extract_text_from_image(image, lang="ara+eng"):
    return pytesseract.image_to_string(image, lang=lang)

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path, lang="ara+eng"):
    poppler_path = None
    if platform.system() == "Windows":
        poppler_path = r"C:\poppler\bin"  # Adjust if necessary
    
    # لا نمرر poppler_path على Linux لأن poppler-utils مثبت من `packages.txt`
    images = convert_from_path(pdf_path, poppler_path=poppler_path if poppler_path else None)
    text = "\n".join([pytesseract.image_to_string(img, lang=lang) for img in images])
    return text

# Streamlit UI
st.title("📄 OCR Text Extractor (Image & PDF)")
st.write("Upload an image or a PDF to extract text.")

uploaded_file = st.file_uploader("Upload Image/PDF", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    file_type = uploaded_file.type

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_type.split("/")[-1]) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    if file_type.startswith("image"):
        image = Image.open(temp_path)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        extracted_text = extract_text_from_image(image)
    elif file_type == "application/pdf":
        extracted_text = extract_text_from_pdf(temp_path)
    
    os.remove(temp_path)

    if extracted_text:
        st.subheader("📝 Extracted Text:")
        st.text_area("", extracted_text, height=300)
