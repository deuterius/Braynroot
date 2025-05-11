import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json

# Initialize session state
if "nodes" not in st.session_state:
    st.session_state.nodes = []
if "edges" not in st.session_state:
    st.session_state.edges = []
if "selected_node" not in st.session_state:
    st.session_state.selected_node = None

# Utility functions
def find_node_at_position(x, y):
    for node in st.session_state.nodes:
        if (node["x"] <= x <= node["x"] + 200) and (node["y"] <= y <= node["y"] + 100):
            return node
    return None

def create_node_svg(node):
    return {
        "type": "rect",
        "left": node["x"],
        "top": node["y"],
        "width": 200,
        "height": 100,
        "fill": "#d3d3d3" if node["id"] != st.session_state.selected_node else "#a0d3f0",
        "stroke": "#000000",
        "strokeWidth": 2,
        "id": str(node["id"]),
        "metadata": {"title": node["title"], "content": node["content"]}
    }

# Sidebar controls
with st.sidebar:
    st.header("Node Editor")
    title = st.text_input("Title", key="title_input")
    content = st.text_area("Content", key="content_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Node"):
            new_node = {
                "id": len(st.session_state.nodes),
                "title": title,
                "content": content,
                "x": 50,
                "y": 50
            }
            st.session_state.nodes.append(new_node)
    with col2:
        if st.button("Update Node") and st.session_state.selected_node is not None:
            st.session_state.nodes[st.session_state.selected_node]["title"] = title
            st.session_state.nodes[st.session_state.selected_node]["content"] = content

# Main canvas area
st.header("Concept Map Canvas")

canvas = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#ffffff",
    height=800,
    width=1200,
    drawing_mode="freedraw",
    initial_drawing={
        "objects": [create_node_svg(node) for node in st.session_state.nodes] +
                   [{"type": "line", 
                     "x1": edge["start"][0], "y1": edge["start"][1],
                     "x2": edge["end"][0], "y2": edge["end"][1],
                     "strokeWidth": 2} for edge in st.session_state.edges]
    },
    key="canvas",
)

# Handle canvas events
if canvas.json_data is not None:
    objects = canvas.json_data.get("objects", [])
    events = canvas.json_data.get("events", [])
    
    # Handle node selection
    for event in events:
        if event.get("type") == "mouseup":
            x = event.get("x")
            y = event.get("y")
            if x is not None and y is not None:
                clicked_node = find_node_at_position(x, y)
                if clicked_node:
                    st.session_state.selected_node = clicked_node["id"]
                    st.session_state.title = clicked_node["title"]
                    st.session_state.content = clicked_node["content"]
    
    # Handle edge creation
    for obj in objects:
        if obj.get("type") == "line" and "custom" not in obj:
            x1, y1 = obj.get("x1"), obj.get("y1")
            x2, y2 = obj.get("x2"), obj.get("y2")
            if all(v is not None for v in [x1, y1, x2, y2]):
                start_node = find_node_at_position(x1-100, y1-50)
                end_node = find_node_at_position(x2-100, y2-50)
                if start_node and end_node and start_node != end_node:
                    edge_exists = any(e["start"] == start_node["id"] and e["end"] == end_node["id"]
                                    for e in st.session_state.edges)
                    if not edge_exists:
                        st.session_state.edges.append({
                            "start": start_node["id"],
                            "end": end_node["id"],
                            "start_pos": (x1, y1),
                            "end_pos": (x2, y2)
                        })
                        obj["custom"] = True  # Mark as processed

# Debug information
with st.expander("Debug Information"):
    st.write("Nodes:", st.session_state.nodes)
    st.write("Edges:", st.session_state.edges)
    st.write("Selected Node:", st.session_state.selected_node)