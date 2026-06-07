import streamlit as st

from frontend.components import page_header, section_title
from frontend.styles import load_css
from frontend.chatbot import chatbot_ui


st.set_page_config(
    page_title="About Project",
    page_icon=":information_source:",
    layout="wide",
)

load_css()
page_header(
    "About LeafGuard AI",
    "An AI-powered plant leaf disease detection system with practical crop-care guidance.",
    "fa-circle-info",
)

section_title("Project Overview", "fa-leaf")
st.html(
    """
    <div class="leaf-panel">
        <p>
            LeafGuard AI uses a two-stage deep learning workflow. It first checks
            whether the uploaded image looks like a plant leaf, then predicts the
            most likely disease and shows symptoms, causes, treatment, and prevention
            guidance from the disease knowledge base.
        </p>
    </div>
    """,
)

col_frontend, col_backend, col_model = st.columns(3)
with col_frontend:
    st.html(
        """
        <div class="leaf-panel">
            <h3>Frontend</h3>
            <ul>
                <li>Streamlit</li>
                <li>HTML components</li>
                <li>Shared CSS</li>
            </ul>
        </div>
        """,
    )

with col_backend:
    st.html(
        """
        <div class="leaf-panel">
            <h3>Backend</h3>
            <ul>
                <li>Python</li>
                <li>TensorFlow</li>
                <li>NumPy</li>
            </ul>
        </div>
        """,
    )

with col_model:
    st.html(
        """
        <div class="leaf-panel">
            <h3>Models</h3>
            <ul>
                <li>MobileNetV2 classifier</li>
                <li>Leaf validation model</li>
                <li>224 x 224 input size</li>
            </ul>
        </div>
        """,
    )

section_title("Project Features", "fa-list-check")
st.html(
    """
    <div class="leaf-panel">
        <ul>
            <li>Leaf detection before disease classification</li>
            <li>Top 3 predictions with confidence scores</li>
            <li>Disease symptoms, causes, treatment, and prevention</li>
            <li>AI agriculture assistant</li>
            <li>Session prediction history</li>
        </ul>
    </div>
    """,
)

section_title("Academic Details", "fa-graduation-cap")

st.html(
    """
    <div class="leaf-panel">
        <h4>Project Team Members</h4>
        <ul>
            <li>Jyotirmaya Behera (3146/24)</li>
            <li>Diptesh Ranjan Pradhan (3141/24)</li>
            <li>Bibekananda Sahoo (3136/24)</li>
            <li>Pritam Kumar Behera (3159/24)</li>
            <li>Laxman Kumar Sahoo (3148/24)</li>
        </ul>

        <h4>Academic Information</h4>
        <p><strong>Academic Year:</strong> 2025 - 2026</p>
    </div>
    """
)

# Render floating chatbot globally
chatbot_ui()
