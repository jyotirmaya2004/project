import streamlit as st

from frontend.components import page_header, section_title
from frontend.styles import load_css


st.set_page_config(
    page_title="Dataset Information",
    page_icon=":books:",
    layout="wide",
)

load_css()
page_header(
    "Dataset Information",
    "Model training data, supported crops, and disease categories.",
    "fa-database",
)

section_title("PlantVillage Dataset", "fa-seedling")

col_summary, col_crops = st.columns([1, 1])
with col_summary:
    st.html(
        """
        <div class="leaf-panel">
            <h3>Dataset Summary</h3>
            <ul>
                <li>Total classes: 38+</li>
                <li>Model image size: 224 x 224</li>
                <li>Purpose: plant disease identification from leaf images</li>
            </ul>
        </div>
        """,
    )

with col_crops:
    st.html(
        """
        <div class="leaf-panel">
            <h3>Supported Crops</h3>
            <ul>
                <li>Apple</li>
                <li>Corn</li>
                <li>Grape</li>
                <li>Peach</li>
                <li>Pepper</li>
                <li>Potato</li>
                <li>Strawberry</li>
                <li>Tomato</li>
            </ul>
        </div>
        """,
    )

st.html(
    """
    <div class="leaf-panel">
        <h3>Disease Categories</h3>
        <p>
            The dataset includes healthy leaves and common disease categories such as
            bacterial spot, early blight, late blight, leaf mold, rust, powdery mildew,
            scab, and leaf scorch.
        </p>
    </div>
    """,
)
