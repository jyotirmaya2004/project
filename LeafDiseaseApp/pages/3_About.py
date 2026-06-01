import streamlit as st

st.set_page_config(
    page_title="About Project",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About LeafGuard AI")

st.markdown("""
## 🌿 Project Overview

LeafGuard AI is an AI-powered plant disease detection system.

The application uses Deep Learning to identify diseases from leaf images and provide:

- Disease Detection
- Confidence Score
- Symptoms
- Causes
- Treatment
- Prevention Tips
- AI Agriculture Assistant

---

## 🧠 Technologies Used

### Frontend

- Streamlit
- HTML
- CSS

### Backend

- Python
- TensorFlow
- NumPy

### AI Models

- MobileNetV2
- Leaf Validation Model

---

## 📂 Dataset

PlantVillage Dataset

Supported Plants:

- Apple
- Tomato
- Potato
- Corn
- Grape
- Strawberry
- Peach
- Pepper
- Orange

Total Classes: 38+

---

## 📊 Model Information

Input Size:

224 × 224

Model Type:

Transfer Learning

Framework:

TensorFlow / Keras

---

## 🎯 Project Features

✅ Leaf Detection

✅ Disease Classification

✅ Top 3 Predictions

✅ Disease Knowledge Base

✅ AI Chatbot

✅ Prediction History

---

## 👨‍💻 Team Members

Add your team members here.

1. Your Name
2. Team Member 2
3. Team Member 3

---

## 🏫 College Information

Add your college information here.

---

## 📅 Academic Year

2025 - 2026
""")