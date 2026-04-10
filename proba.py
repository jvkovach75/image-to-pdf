import streamlit as st
from PIL import Image
import tempfile

st.set_page_config(page_title="Image to PDF", layout="centered")

st.title("Convert Image to PDF")

file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

if file:
    image = Image.open(file)

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        pdf_path = temp_file.name

    image.save(pdf_path, "PDF")

    st.success("Image converted successfully!")

    with open(pdf_path, "rb") as f:
        st.download_button(
            "Download PDF",
            data=f,
            file_name="converted.pdf",
            mime="application/pdf"
        )