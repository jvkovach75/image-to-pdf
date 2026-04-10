import os
import tempfile
import streamlit as st
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="Image to PDF", layout="centered")

st.title("Image to PDF")
st.write("Convert JPG, JPEG and PNG images to PDF instantly.")
st.caption("Free online image to PDF converter")

file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

if file:
    try:
        image = Image.open(file)

        # Ispravi rotaciju sa telefona (EXIF)
        image = ImageOps.exif_transpose(image)

        # PNG / transparent background -> RGB
        if image.mode in ("RGBA", "P"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode == "RGBA":
                background.paste(image, mask=image.split()[3])
            else:
                background.paste(image)
            image = background
        else:
            image = image.convert("RGB")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
            temp_img_path = temp_img.name
            image.save(temp_img_path, format="JPEG", quality=95)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            pdf_path = temp_pdf.name

        c = canvas.Canvas(pdf_path, pagesize=A4)
        page_width, page_height = A4

        img_width, img_height = image.size

        margin = 20
        max_width = page_width - 2 * margin
        max_height = page_height - 2 * margin

        scale = min(max_width / img_width, max_height / img_height)
        new_width = img_width * scale
        new_height = img_height * scale

        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2

        c.drawImage(temp_img_path, x, y, width=new_width, height=new_height)
        c.showPage()
        c.save()

        st.success("Image converted successfully!")

        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF",
                data=f,
                file_name="converted.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        try:
            if "temp_img_path" in locals() and os.path.exists(temp_img_path):
                os.remove(temp_img_path)
            if "pdf_path" in locals() and os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception:
            pass
