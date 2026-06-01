import streamlit as st
from frontend.styles import load_css
from frontend.components import (
    prediction_card,
    top_predictions_card,
    symptoms_card,
    causes_card,
    treatment_card,
    prevention_card
)
from frontend.chatbot import chatbot_ui
from frontend.styles import load_css

from frontend.components import (
    prediction_card,
    top_predictions_card,
    symptoms_card,
    causes_card,
    treatment_card,
    prevention_card
)

from frontend.chatbot import chatbot_ui

from backend.predict import (
    predict_disease,
    PredictionError
)

from backend.disease_info import (
    get_disease_details
)

def render_header():
    st.markdown("""
    <div style="
        padding:30px;
        border-radius:20px;
        background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
        color:white;
        text-align:center;
        margin-bottom:20px;
    ">
        <h1>🌿 LeafGuard AI</h1>
        <h3>Smart Leaf Disease Detection System</h3>
        <p>Upload a leaf image and get instant AI-powered disease analysis.</p>
    </div>
    """, unsafe_allow_html=True)


def render_upload_section():
    st.markdown("## 📤 Upload Leaf Image")

    uploaded_file = st.file_uploader(
        "Choose a leaf image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        st.image(
            uploaded_file,
            caption="Uploaded Leaf",
            use_container_width=True
        )

    return uploaded_file


def render_prediction_section(uploaded_file):

    st.markdown("## 📊 Prediction Result")

    if uploaded_file is None:

        st.info(
            "Upload a leaf image to begin."
        )

        return

    if st.button(
        "🔍 Analyze Leaf",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Analyzing image..."
            ):

                result = predict_disease(
                    uploaded_file
                )

            prediction_card(
                result["disease"],
                result["confidence"]
            )

            top_predictions = []

            for pred in result[
                "top_predictions"
            ]:

                top_predictions.append(
                    (
                        pred["disease"],
                        pred["confidence"]
                    )
                )

            top_predictions_card(
                top_predictions
            )

            disease_info = (
                get_disease_details(
                    result["class_name"]
                )
            )

            symptoms_card(
                disease_info["symptoms"]
            )

            causes_card(
                disease_info["causes"]
            )

            treatment_card(
                disease_info["treatment"]
            )

            prevention_card(
                disease_info["prevention"]
            )

        except PredictionError as e:

            st.error(str(e))

        except Exception as e:

            st.error(
                f"Unexpected Error: {e}"
            )

def render_feature_cards():
    st.markdown("## 🚀 Features")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Accuracy", "98%")

    with col2:
        st.metric("Prediction", "<2 sec")

    with col3:
        st.metric("Diseases", "38+")

    with col4:
        st.metric("Plants", "15+")


def render_chatbot_button():

    st.markdown("""
    <style>

    .floating-chat{
        position:fixed;
        bottom:20px;
        right:20px;
        width:65px;
        height:65px;
        border-radius:50%;
        background:#00cc66;
        color:white;
        text-align:center;
        line-height:65px;
        font-size:30px;
        font-weight:bold;
        box-shadow:0px 4px 15px rgba(0,0,0,0.3);
        z-index:999;
    }

    </style>

    <div class="floating-chat">
        🤖
    </div>
    """, unsafe_allow_html=True)


def main():

    load_css()

    render_header()

    left, right = st.columns(
        [1,1]
    )

    with left:

        uploaded_file = (
            render_upload_section()
        )

    with right:

        render_prediction_section(
            uploaded_file
        )

    st.divider()

    render_feature_cards()

    chatbot_ui()