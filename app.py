import streamlit as st
from pathlib import Path
import fitz  # PyMuPDF                                         # :contentReference[oaicite:0]{index=0}
import os
from datetime import datetime
from streamlit_pdf_viewer import pdf_viewer

# --- CONFIGURATION ---
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)                              # :contentReference[oaicite:1]{index=1}

# --- UPLOAD SECTION IN SIDEBAR ---
st.sidebar.title("📄 Upload a PDF")

uploaded = st.sidebar.file_uploader("Choose a PDF...", type="pdf")  # :contentReference[oaicite:2]{index=2}
if uploaded:
    # Modal form to rename file
    with st.sidebar.form("rename_form", clear_on_submit=True):
        new_name = st.text_input("Filename:", value=uploaded.name)
        submitted = st.form_submit_button("Save")
    if submitted and new_name:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        safe_name = f"{new_name}_{timestamp}.pdf"
        save_path = UPLOAD_DIR / safe_name

        # Write bytes to disk ([turn0search0])
        with open(save_path, "wb") as f:
            f.write(uploaded.getbuffer())
        st.sidebar.success(f"Saved as '{safe_name}'")            # :contentReference[oaicite:3]{index=3}

# --- LIST AND SELECT EXISTING FILES ---
files = sorted(UPLOAD_DIR.glob("*.pdf"), 
               key=lambda p: p.stat().st_mtime, 
               reverse=True)                                  # :contentReference[oaicite:4]{index=4}

st.sidebar.markdown("### Your PDFs")
selected_path = None
for pdf_path in files:
    # Render first page to thumbnail
    doc = fitz.open(str(pdf_path))
    page = doc.load_page(0)
    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))        # low-res thumbnail :contentReference[oaicite:5]{index=5}
    img_bytes = pix.tobytes("png")

    # Display in sidebar with a button to select
    container = st.sidebar.container()
    container.image(img_bytes, use_column_width=True)          # :contentReference[oaicite:6]{index=6}
    if container.button(pdf_path.stem, key=pdf_path.name):     # unique key                                  
        selected_path = pdf_path

# --- MAIN AREA: DISPLAY SELECTED PDF ---
if selected_path:
    st.header(f"📄 Viewing: {selected_path.stem}")
    doc = fitz.open(str(selected_path))
    # Show first page at higher resolution
    page = doc.load_page(0)
    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))         # higher-res :contentReference[oaicite:7]{index=7}
    img = pix.tobytes("png")
    st.image(img, caption="First page preview", use_column_width=True)

    with st.expander("View Full PDF"):
        pdf_viewer(doc['data'])


