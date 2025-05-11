import streamlit as st
from pathlib import Path
import fitz  # PyMuPDF
import os
import json
import networkx as nx
from datetime import datetime
from streamlit_pdf_viewer import pdf_viewer
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import uuid
import numpy as np
from io import BytesIO
from mentalmap import ConceptualMap
import html
import requests
from multi_tool_agent.splitting_agent import split_text
from multi_tool_agent.agent import suggest_addition, feedback
import asyncio
from pdf import pdf_to_text

# --- CONFIGURATION ---
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)                              # :contentReference[oaicite:1]{index=1}
GRAPH_DIR = Path(".")
GRAPH_DIR.mkdir(exist_ok=True)

def from_custom_to_netowrkx_format(input_json):
    """
    Transform a graph JSON from the first format to the NetworkX-compatible format.
    
    Args:
        input_json (dict): Input JSON in the first format
        
    Returns:
        dict: Transformed JSON in the NetworkX-compatible format
    """
    if type(input_json) is str:
        try:
            input_json = json.loads(input_json)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string provided.")
    
    # Create the base structure for the output
    output_json = {
        "directed": False,
        "multigraph": False,
        "graph": {},
        "nodes": [],
        "links": []
    }
    
    # Create a mapping from node IDs to node text
    # This will be used for the links
    node_id_to_text = {}
    
    # Process nodes
    for node in input_json.get("nodes", []):
        # Add node to output
        output_json["nodes"].append({
            "id": node["text"]  # Using the text as the node ID in the output
        })
        
        # Store the mapping
        node_id_to_text[node["id"]] = node["text"]
    
    # Process edges
    for edge in input_json.get("edges", []):
        # Get the source and target text using the mapping
        source_text = node_id_to_text[edge["sourceId"]]
        target_text = node_id_to_text[edge["targetId"]]
        
        # Add link to output
        output_json["links"].append({
            "label": edge["text"],
            "source": source_text,
            "target": target_text
        })
    
    return output_json

def from_networkx_to_custom_format(input_json):
    """
    Transform a graph JSON from NetworkX-compatible format back to the original format.
    
    Args:
        input_json (dict): Input JSON in NetworkX-compatible format
        
    Returns:
        dict: Transformed JSON in the original format
    """
    # Create the base structure for the output
    output_json = {
        "nodes": [],
        "edges": []
    }
    
    # Process nodes
    for i, node in enumerate(input_json.get("nodes", [])):
        x = 0  
        y = 0  
        
        # Add node to output with default coordinates
        output_json["nodes"].append({
            "id": f"node-{i+1}",  # Generate a new ID like "node-1", "node-2", etc.
            "x": x,
            "y": y,
            "text": node["id"]  # The "id" from input becomes the "text" in output
        })
    
    # Create a mapping from node text to node ID
    text_to_node_id = {node["text"]: node["id"] for node in output_json["nodes"]}
    
    # Process links
    for i, link in enumerate(input_json.get("links", [])):
        # Find the source and target node IDs using the mapping
        source_id = text_to_node_id[link["source"]]
        target_id = text_to_node_id[link["target"]]
        
        # Add edge to output
        output_json["edges"].append({
            "id": f"edge-{i+1}",  # Generate a new ID like "edge-1", "edge-2", etc.
            "sourceId": source_id,
            "targetId": target_id,
            "text": link["label"]
        })
    
    return output_json

def export_graph(graph_json: str, filename):
    with open(filename, 'w') as file:
        file.write(graph_json)
    
def import_graph(filename):
    with open(filename, 'r') as file:
        graph_json = file.read()
        graph_json = json.loads(graph_json)
        
    return graph_json

def get_clean_text(pdf_file_path: Path) -> str:
    raw_text = pdf_to_text(pdf_file_path)
    try:
        clean_text = asyncio.run(split_text(raw_text))
        print("Clean text:", clean_text)
    except Exception as e:
        print(f"Error during text splitting: {e}")
        clean_text = raw_text
    return clean_text

def get_feedback_graph(reference_text:str, g0: str, g1: str):
    g0_json = from_custom_to_netowrkx_format(g0)
    g1_json = from_custom_to_netowrkx_format(g1)
    try:
        feedback_response = asyncio.run(feedback(text=reference_text, g0=g0_json, g1=g1_json))
    except Exception as e:
        print(f"Error during feedback generation: {e}")
        feedback_response = "Error generating feedback"
    return feedback_response

def get_suggest_addition(reference_text:str, g0: str, g1: str):
    g0_json = from_custom_to_netowrkx_format(g0)
    g1_json = from_custom_to_netowrkx_format(g1)
    try:
        g2_json, explanation = asyncio.run(suggest_addition(text=reference_text, g0=g0_json, g1=g1_json))
    except Exception as e:
        print(f"Error during suggestion generation: {e}")
        explanation = "Error generating suggestion"
        g2_json = g1_json
    
    return explanation, from_networkx_to_custom_format(g2_json)

st.set_page_config(page_title="PDF Manager", layout="wide")

# --- CSS (Your existing CSS for sidebar buttons, etc.) ---
st.markdown("""
<style>
.pdf-name-sidebar {
    font-weight: bold; margin-top: 5px; margin-bottom: 8px; font-size: 20px !important; word-wrap: break-word;
}
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stButton"] > button {
    background-color: #DC3545 !important; color: white !important; border: 1px solid #DC3545 !important;
}
/* ... other button states from your original CSS ... */
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stButton"] > button:hover {
    background-color: #C82333 !important; border-color: #BD2130 !important;
}
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stButton"] > button:active {
    background-color: #B21E2B !important; border-color: #A51C29 !important;
}
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stButton"] > button:focus {
    box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.5) !important;
}
</style>
""", unsafe_allow_html=True)

# --- Helper Function ---
def get_display_name_from_path(file_path: Path) -> str:
    full_stem = file_path.stem
    if len(full_stem) > 15 and full_stem[-15] == '_':
        timestamp_candidate = full_stem[-14:]
        try:
            datetime.strptime(timestamp_candidate, "%Y%m%d%H%M%S")
            return full_stem[:-15]
        except ValueError:
            return full_stem
    else:
        return full_stem

# --- Session State Initialization ---
if 'show_rename_modal' not in st.session_state: st.session_state.show_rename_modal = False
if 'pending_upload_file' not in st.session_state: st.session_state.pending_upload_file = None
if 'selected_pdf_display_path' not in st.session_state: st.session_state.selected_pdf_display_path = None
if 'uploader_key' not in st.session_state: st.session_state.uploader_key = 0

# --- UPLOAD HANDLING ---
uploaded_file_obj = st.sidebar.file_uploader(
    "Upload a PDF", type="pdf", key=f"pdf_file_uploader_{st.session_state.uploader_key}"
)

if uploaded_file_obj is not None:
    if not st.session_state.show_rename_modal and st.session_state.pending_upload_file is None:
        st.session_state.pending_upload_file = uploaded_file_obj
        st.session_state.show_rename_modal = True
        st.rerun()

# --- MODAL DIALOG FOR RENAMING ---
if st.session_state.show_rename_modal and st.session_state.pending_upload_file:
    @st.dialog("Rename & Save PDF", width="small")
    def rename_and_save_dialog_fn():
        pending_file_data = st.session_state.pending_upload_file
        original_uploaded_name = pending_file_data.name
        default_stem = Path(original_uploaded_name).stem
        user_defined_name = st.text_input(
            "Enter desired filename (e.g., 'My Report'):",
            value=default_stem,
            key="rename_dialog_text_input_v4" # Ensure unique key
        )
        if st.button("Save PDF", key="rename_dialog_save_button_v4"): # Ensure unique key
            if not user_defined_name.strip():
                st.error("Filename cannot be empty."); return
            clean_stem = user_defined_name.strip()
            if clean_stem.lower().endswith(".pdf"): clean_stem = clean_stem[:-4]
            if not clean_stem: st.error("Filename (after removing .pdf suffix if any) cannot be empty."); return
            timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
            final_filename = f"{clean_stem}_{timestamp_str}.pdf"
            save_path = UPLOAD_DIR / final_filename
            try:
                with open(save_path, "wb") as f: f.write(pending_file_data.getbuffer())
                st.toast(f"Saved: {clean_stem}", icon="✅")
                st.session_state.pending_upload_file = None
                st.session_state.show_rename_modal = False
                st.session_state.uploader_key += 1
                st.rerun()
            except Exception as e: st.error(f"Error saving file: {e}")
    rename_and_save_dialog_fn()

# --- FILE LISTING (SIDEBAR) ---
st.sidebar.markdown("---")
st.sidebar.info("Your PDFs", icon="📁")
pdf_files_on_disk = sorted(UPLOAD_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
if not pdf_files_on_disk: st.sidebar.info("No PDFs uploaded yet.")
for pdf_path_obj in pdf_files_on_disk:
    display_name_for_list_item = get_display_name_from_path(pdf_path_obj)
    with st.sidebar.container():
        st.markdown(f"<p class='pdf-name-sidebar'>{html.escape(display_name_for_list_item)}</p>", unsafe_allow_html=True)
        try:
            doc = fitz.open(str(pdf_path_obj))
            if len(doc) > 0:
                page = doc.load_page(0)
                pix = page.get_pixmap(matrix=fitz.Matrix(0.7, 0.7))
                thumb_bytes = pix.tobytes("png")
                st.image(thumb_bytes, use_container_width=True, caption="")
            doc.close()
        except Exception: st.caption(f"No thumbnail for {display_name_for_list_item[:20]}...")
        col_btn_view, col_btn_delete = st.columns(2)
        with col_btn_view:
            if st.button("View", key=f"view_{pdf_path_obj.name}", use_container_width=True):
                st.session_state.selected_pdf_display_path = str(pdf_path_obj); st.rerun()
        with col_btn_delete:
            if st.button("Delete", key=f"del_{pdf_path_obj.name}", use_container_width=True):
                try:
                    pdf_path_obj.unlink()
                    if st.session_state.selected_pdf_display_path == str(pdf_path_obj):
                        st.session_state.selected_pdf_display_path = None
                    st.toast(f"Deleted: {display_name_for_list_item}", icon="🗑️")
                except Exception as e: st.error(f"Error deleting file: {e}")
                st.rerun()
        st.sidebar.markdown("---")

# --- MAIN DISPLAY AREA ---
if st.session_state.selected_pdf_display_path:
    selected_path_object_for_display = Path(st.session_state.selected_pdf_display_path)

    if not selected_path_object_for_display.exists():
        st.warning("The selected PDF file no longer exists. It might have been deleted.")
        st.session_state.selected_pdf_display_path = None
        if 'error_shown_for_missing_file' not in st.session_state:
            st.session_state.error_shown_for_missing_file = True; st.rerun()
    else:
        st.session_state.pop('error_shown_for_missing_file', None)
        main_display_name = get_display_name_from_path(selected_path_object_for_display)
        st.header(f"📄 Working on: {main_display_name}")

        tab1, tab2 = st.tabs(["Conceptual map", "Exercises"])
        with tab1:  
            # Add a slider to control the width ratio
            ratio = st.slider("Adjust column width ratio (Left : Right)", min_value=1, max_value=9, value=5)

            # Normalize the ratio
            total = ratio + (10 - ratio)
            left_width = ratio / total
            right_width = (10 - ratio) / total

            # Create columns with dynamic widths
            col1, col2 = st.columns([left_width, right_width])

            with col1:
                try:
                    with open(selected_path_object_for_display, "rb") as f_pdf:
                        pdf_bytes_content = f_pdf.read()

                    if pdf_bytes_content:
                        # Set a fixed height for the PDF viewer.
                        # The component itself should handle scrolling if the PDF is taller.
                        pdf_viewer(input=pdf_bytes_content, height=700)
                    else:
                        st.error("The selected PDF file appears to be empty or could not be read.")
                except ImportError:
                    st.error("Component `streamlit_pdf_viewer` not found. Please install it: `pip install streamlit-pdf-viewer`")
                    st.info("After installing, you may need to stop and restart the Streamlit app.")
                except Exception as e:
                    st.error(f"Error displaying PDF with streamlit_pdf_viewer: {e}")
                    st.exception(e) # Shows full traceback for easier debugging"

            with col2:
                # Embed the iframe in Streamlit
                iframe_code = f"""
                <iframe 
                    name="conceptualMapIframe" 
                    src="http://127.0.0.1:5000/concept-map" 
                    width="100%" 
                    height="700" 
                    frameborder="0"></iframe>
                """
                st.markdown(iframe_code, unsafe_allow_html=True)

                g0 = """{"edges": [], "nodes": []}"""

                if 'button_clicked' not in st.session_state:
                    st.session_state.button_clicked = False

                feed_b, ori_b, sug_b, sub_b = st.columns(4)
                with feed_b:
                    if st.button("Feedback"):
                        st.session_state.button_clicked = True
                
                if st.session_state.button_clicked:
                    response = requests.get("http://localhost:5000/api/graph")
                    if response.status_code == 200:
                        g1 = response.content.decode('utf-8')
                        print(g1)
                        choice = g1
                        with ori_b:
                            if st.button("Original"):
                                choice = g1

                        with sug_b:
                            if st.button("Suggested"):
                                # Codice di andre
                                choice = g1

                        with sub_b:
                            if st.button("Submit"):
                                g0 = choice
                                st.session_state.button_clicked = False

                        print(choice)
                        response = requests.post(
                            "http://localhost:5000/api/graph",
                            json=choice
                        )
        with tab2:
            pass
else:
    st.info("Upload a PDF or select one from the sidebar to view it.")