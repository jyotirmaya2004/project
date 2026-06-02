import streamlit as st

from backend.disease_info import get_disease_details
from backend.predict_two_stage import PredictionError, predict_two_stage
from frontend.chatbot import chatbot_ui
from frontend.components import (
    causes_card,
    prediction_card,
    prevention_card,
    symptoms_card,
    top_predictions_card,
    treatment_card,
)
from frontend.styles import load_css


def render_header():
    st.title("LeafGuard AI")
    st.caption("Upload or capture a leaf image and get instant disease analysis.")


def render_upload_section():
    st.subheader("Leaf Image")

    default_source = 1 if st.query_params.get("source") == "camera" else 0
    source_choice = st.radio(
        "Image source",
        ["Upload from device", "Use camera"],
        index=default_source,
        horizontal=True,
    )

    if source_choice == "Use camera":
        image_file = st.camera_input("Take a clear leaf photo")
    else:
        image_file = st.file_uploader(
            "Choose a leaf image",
            type=["jpg", "jpeg", "png", "webp", "bmp", "gif", "tiff", "heic", "heif"],
        )

    if image_file:
        st.image(image_file, caption="Selected leaf image", use_column_width=True)

    return image_file


def render_prediction_section(image_file):
    st.subheader("Prediction Result")

    with st.expander("Debug: leaf vs non-leaf output", expanded=False):
        show_debug = st.checkbox("Show raw leaf validation output", value=False)

    if image_file is None:
        st.info("Upload or capture a leaf image to begin.")
        return

    if st.button("Analyze Leaf", use_container_width=True, type="primary"):
        try:
            with st.spinner("Analyzing image..."):
                result = predict_two_stage(image_file, top_k=3)

            st.session_state.prediction = result
            st.session_state.setdefault("prediction_history", []).append(
                {
                    "Disease": result["disease"],
                    "Confidence": result["confidence"],
                }
            )
        except PredictionError as exc:
            st.session_state.prediction = None
            st.error(str(exc))
        except Exception as exc:
            st.session_state.prediction = None
            st.error(f"Unexpected error: {exc}")

    result = st.session_state.get("prediction")
    if not result:
        return

    prediction_card(result["disease"], result["confidence"])
    top_predictions_card(
        [(pred["disease"], pred["confidence"]) for pred in result["top_predictions"]]
    )

    if show_debug:
        st.json(result["leaf_validation"])

    disease_info = get_disease_details(result["class_name"])
    symptoms_card(disease_info["symptoms"])
    causes_card(disease_info["causes"])
    treatment_card(disease_info["treatment"])
    prevention_card(disease_info["prevention"])


def render_history_section():
    st.subheader("Prediction History")

    history = st.session_state.get("prediction_history", [])
    if not history:
        st.info("No history yet. Analyze a leaf image to see records here.")
        return

    st.dataframe(history, use_container_width=True)


def render_tips_section():
    st.subheader("Quick Care Tips")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Use clear, bright photos with one leaf in focus.")
    with col2:
        st.info("Retake blurry images for better model confidence.")
    with col3:
        st.info("Review treatment and prevention before spraying chemicals.")


def render_feature_cards():
    st.subheader("Features")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", "98%")
    col2.metric("Prediction", "<2 sec")
    col3.metric("Diseases", "38+")
    col4.metric("Plants", "15+")


def main(active_tab: str = "all"):
    load_css()
    render_header()

    if active_tab == "history":
        render_history_section()
        return

    if active_tab == "tips":
        render_tips_section()
        return

    if active_tab == "chat":
        chatbot_ui()
        return

    left, right = st.columns([1, 1])
    with left:
        image_file = render_upload_section()
    with right:
        render_prediction_section(image_file)

    st.divider()
    render_feature_cards()

    st.divider()
    render_history_section()

    st.divider()
    render_tips_section()

    st.divider()
    chatbot_ui()
