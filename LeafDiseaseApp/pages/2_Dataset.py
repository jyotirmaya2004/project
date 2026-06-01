import streamlit as st

st.set_page_config(
    page_title="Dataset Information",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Dataset Information")

st.markdown("""
## PlantVillage Dataset

This project uses the PlantVillage dataset.

### Total Classes

38+

### Image Size

224 × 224

### Supported Crops

- Apple
- Corn
- Grape
- Peach
- Pepper
- Potato
- Strawberry
- Tomato

### Disease Categories

- Healthy
- Bacterial Spot
- Early Blight
- Late Blight
- Leaf Mold
- Rust
- Powdery Mildew
- Scab
- Leaf Scorch

and many more.

### Dataset Purpose

The dataset is used to train the deep learning model for plant disease identification.
""")