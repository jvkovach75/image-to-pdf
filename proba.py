import os
import tempfile

import streamlit as st
from PIL import Image, ImageOps

st.markdown(
    '<meta name="google-site-verification" content="ba80sENhom1" />',
    unsafe_allow_html=True
)

st.set_page_config(page_title="Image to PDF", layout="centered")

st.title("Image to PDF")
st.markdown("### Free Image to PDF Converter")
st.write("Convert one or multiple JPG, JPEG and PNG images into a single PDF.")

files = st.file_uploader(
    "Upload image(s)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if files:
    st.markdown("### Preview")
    for i, file in enumerate(files, start=1):
        st.image(file, caption=f"Image {i}", use_container_width=True)

    try:
        processed_images = []

        for file in files:
            image = Image.open(file)
            image = ImageOps.exif_transpose(image)

            if image.mode in ("RGBA", "P"):
                background = Image.new("RGB", image.size, (255, 255, 255))
                if image.mode == "RGBA":
                    background.paste(image, mask=image.split()[3])
                else:
                    background.paste(image)
                image = background
            else:
                image = image.convert("RGB")

            processed_images.append(image)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            pdf_path = temp_pdf.name

        if len(processed_images) == 1:
            processed_images[0].save(pdf_path, "PDF", resolution=100.0)
        else:
            processed_images[0].save(
                pdf_path,
                "PDF",
                resolution=100.0,
                save_all=True,
                append_images=processed_images[1:]
            )

        st.success("Your PDF is ready!")

        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF",
                data=f,
                file_name="images.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        try:
            if "pdf_path" in locals() and os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception:
            pass

st.markdown("---")
st.markdown("**Keywords:** image to pdf, jpg to pdf, png to pdf, multiple images to pdf, convert images to pdf online")
