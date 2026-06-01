"""Frontend UI components and layout for the Leaf Disease App."""

from io import BytesIO

import streamlit as st
from PIL import Image, UnidentifiedImageError

# Import core logic and helpers from the main application file
from app import (
    ALLOWED_EXTENSIONS,
    PredictionError,
    build_default_disease_info,
    handle_chat_message,
    image_to_preview_bytes,
    normalize_display_text,
    predict_disease,
    validate_uploaded_image,
)


def inject_custom_css() -> None:
    """Apply Bootstrap 5 and custom CSS for floating elements and styling."""
    css = """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root {
        --bg: #f4f7f4;
        --panel: #ffffff;
        --text: #1a231e;
        --primary: #1e824c;
        --muted: #6c757d;
        --line: rgba(128, 128, 128, 0.2);
        --soft: rgba(46, 204, 113, 0.1);
        --radius: 12px;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --bg: #0e1117;
            --panel: #262730;
            --text: #fafafa;
            --primary: #2ecc71;
            --muted: #a3a8b8;
            --line: rgba(255, 255, 255, 0.1);
        }
    }
    html, body, [data-testid="stAppViewContainer"] {
        font-family: Inter, system-ui, -apple-system, sans-serif;
        background: var(--bg);
        color: var(--text);
    }
    /* Prevents Bootstrap from overwriting Streamlit text colors globally */
    p, h1, h2, h3, h4, h5, h6, span, div { color: inherit; }
    /* Override Bootstrap specific classes to respect Dark Mode */
    .card { background-color: var(--panel) !important; border-color: var(--line) !important; color: var(--text) !important; }
    .bg-white, .bg-light { background-color: var(--panel) !important; }
    .text-dark { color: var(--text) !important; }
    .text-muted { color: var(--muted) !important; }
    .border { border-color: var(--line) !important; }
    .shadow-sm { box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; }
    /* Floating Chat Launcher Button */
    div[data-testid="stVerticalBlock"]:has(#chat-launcher) {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1050;
        width: auto !important;
    }
    div[data-testid="stVerticalBlock"]:has(#chat-launcher) button {
        border-radius: 50px;
        padding: 14px 28px;
        font-size: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
        font-weight: bold;
        transition: transform 0.2s ease;
    }
    div[data-testid="stVerticalBlock"]:has(#chat-launcher) button:hover {
        transform: translateY(-2px) scale(1.02);
    }
    /* Floating Chat Window */
    div[data-testid="stVerticalBlock"]:has(#chat-window) {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 400px;
        max-width: 90vw;
        background-color: var(--panel);
        border-radius: 16px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.3) !important;
        z-index: 1050;
        padding: 20px;
        border: 1px solid var(--line);
    }
    /* Fix Streamlit form styling inside the chat widget */
    div[data-testid="stVerticalBlock"]:has(#chat-window) [data-testid="stForm"] {
        border: none;
        padding: 0;
        margin-bottom: 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_page_header() -> None:
    """Render the application header with Bootstrap components."""
    st.markdown(
        """
        <div class="card shadow-sm mb-4 border-0" style="background: linear-gradient(135deg, var(--soft) 0%, var(--bg) 100%); border-radius: var(--radius);">
            <div class="card-body d-flex flex-wrap justify-content-between align-items-center p-4">
                <div class="d-flex align-items-center gap-3">
                    <div class="d-flex justify-content-center align-items-center rounded shadow-sm text-white" style="width:64px; height:64px; font-size:32px; background-color: var(--primary);">
                        <i class="fa-solid fa-leaf"></i>
                    </div>
                    <div>
                        <span class="text-uppercase fw-bold" style="color: var(--primary); font-size: 12px; letter-spacing: 1px;">Plant health workspace</span>
                        <h2 class="mb-1 fw-bolder text-dark" style="font-size: 26px;">Leaf Disease Detection</h2>
                        <p class="text-muted mb-0" style="font-size: 15px;">Upload a clear leaf photo, review the prediction, and get practical plant-care guidance.</p>
                    </div>
                </div>
                <div class="d-flex gap-2 mt-3 mt-md-0">
                    <div class="text-center px-3 py-2 rounded shadow-sm border bg-white d-flex align-items-center justify-content-center" style="border-color: var(--primary) !important; font-size: 20px; min-width: 54px;" title="Current Theme">
                        <i class="fa-solid fa-sun theme-icon-light text-warning"></i>
                        <i class="fa-solid fa-moon theme-icon-dark text-info"></i>
                    </div>
                    <div class="text-center px-4 py-2 rounded shadow-sm border bg-white" style="border-color: var(--primary) !important;">
                        <small class="d-block text-muted fw-semibold">Status</small>
                        <strong style="color: var(--primary);">Ready</strong>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_panel_header(title: str, subtitle: str | None = None) -> None:
    """Render a consistent section header using Bootstrap."""
    subtitle_html = f"<p class='text-muted mb-0' style='font-size: 14px;'>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="mb-3 mt-4">
            <h5 class="mb-1 fw-bold text-dark">{title}</h5>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_results(prediction: dict, disease_info: dict) -> None:
    """Display model prediction and disease guidance using Bootstrap cards."""
    render_panel_header("Prediction Result", "Most likely class and confidence ranking.")

    leaf_validation = prediction.get("leaf_validation")
    if leaf_validation:
        st.markdown(
            f"""
            <div class="card shadow-sm mb-3 border-0 bg-light">
                <div class="card-body border-start border-4 rounded d-flex justify-content-between align-items-center py-3" style="border-color: var(--primary) !important;">
                    <strong class="text-dark"><i class="fa-solid fa-circle-check" style="color: var(--primary);"></i> Leaf validation passed</strong>
                    <span class="badge" style="background-color: var(--primary);">{leaf_validation['leaf_confidence']:.2f}% leaf confidence</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Predicted Disease:**\n### {prediction['disease']}")
    with col2:
        st.success(f"**Confidence Score:**\n### {prediction['confidence']:.2f}%")

    with st.expander("View Top Predictions (Details)"):
        for top_pred in prediction["top_predictions"]:
            st.markdown(
                f"""
                <div class="d-flex justify-content-between align-items-center p-2 mb-2 border rounded bg-white shadow-sm">
                    <strong class="text-dark">{top_pred['disease']}</strong>
                    <span class="text-muted">{top_pred['confidence']:.2f}%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    info = disease_info.get(prediction["class_name"], build_default_disease_info(prediction["class_name"]))
    render_panel_header("Disease Guidance", "Symptoms, causes, treatment, and prevention.")

    for title, key in [("Symptoms", "symptoms"), ("Causes", "causes"), ("Treatment", "treatment"), ("Prevention", "prevention")]:
        with st.expander(title, expanded=title in {"Symptoms", "Treatment"}):
            st.markdown(f"<div class='p-2'>{normalize_display_text(info[key])}</div>", unsafe_allow_html=True)


def render_upload_section(disease_info: dict) -> None:
    """Render the upload and prediction workflow."""
    render_panel_header("Leaf Image", "Use a clear photo with the leaf filling most of the frame.")

    col_input, col_preview = st.columns([1.2, 1], gap="large")

    image = None
    with col_input:
        default_source = 1 if st.query_params.get("source") == "camera" else 0
        source_choice = st.radio("Image source", ["Upload from device", "Take a photo"], index=default_source, horizontal=True)
        if source_choice == "Upload from device":
            source_file = st.file_uploader("Choose a leaf image", type=sorted(ALLOWED_EXTENSIONS))
        else:
            st.info("Keep the leaf close, steady, and well lit. Avoid shadows and busy backgrounds.")
            source_file = st.camera_input("Take a leaf photo")

        if source_file:
            try:
                image = validate_uploaded_image(source_file)
                st.session_state.selected_image_bytes = image_to_preview_bytes(image)
                st.session_state.selected_image_name = getattr(source_file, "name", "Captured image")
            except ValueError as exc:
                image, st.session_state.selected_image_bytes = None, None
                st.error(str(exc))

    with col_preview:
        if st.session_state.selected_image_bytes:
            try:
                image = Image.open(BytesIO(st.session_state.selected_image_bytes)).convert("RGB")
                st.image(image, caption="Selected image", use_column_width=True)
            except (UnidentifiedImageError, OSError):
                image, st.session_state.selected_image_bytes = None, None
                st.warning("Preview expired. Please upload again.")

        st.write("")
        predict_clicked = st.button("Analyze Leaf", disabled=image is None or not st.session_state.selected_image_bytes, type="primary", use_container_width=True)

    if predict_clicked and image is not None and st.session_state.selected_image_bytes:
        st.markdown("<hr>", unsafe_allow_html=True)
        try:
            with st.status("Analyzing leaf image...", expanded=True) as status:
                st.write("Validating image format...")
                st.write("Running AI disease prediction model...")
                st.session_state.prediction = predict_disease(BytesIO(st.session_state.selected_image_bytes))
                status.update(label="Analysis complete!", state="complete", expanded=False)
        except PredictionError as exc:
            st.session_state.prediction = None
            st.error(str(exc))
        except Exception:
            st.session_state.prediction = None
            st.error("Something went wrong while analyzing the image.")

    if st.session_state.prediction:
        st.markdown("<hr>", unsafe_allow_html=True)
        render_prediction_results(st.session_state.prediction, disease_info)


def render_chatbot() -> None:
    """Render the professional floating agriculture chatbot widget."""
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    if not st.session_state.chat_open:
        # Render the floating launcher button
        with st.container():
            st.markdown('<div id="chat-launcher"></div>', unsafe_allow_html=True)
            if st.button("Chat with AI", key="open_chat", type="primary"):
                st.session_state.chat_open = True
                st.rerun()
    else:
        # Render the open chat window
        with st.container():
            st.markdown('<div id="chat-window"></div>', unsafe_allow_html=True)

            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.markdown("<h5 class='fw-bold mb-0 mt-2' style='color: var(--primary);'><i class='fa-solid fa-message'></i> AI Plant Care</h5>", unsafe_allow_html=True)
            with col2:
                if st.button("Close", key="close_chat"):
                    st.session_state.chat_open = False
                    st.rerun()

            st.markdown("<hr class='mt-2 mb-3'>", unsafe_allow_html=True)

            # Chat History (Scrollable Area)
            chat_history = st.container(height=350)
            with chat_history:
                for message in st.session_state.chat_messages:
                    with st.chat_message(message["role"]):
                        st.markdown(normalize_display_text(message["content"]))

            # Input Area
            st.caption("Ask a plant care question:")
            with st.form("chat_form", clear_on_submit=True):
                user_message = st.text_input(
                    "Message",
                    placeholder="e.g. How do I treat leaf rust?",
                    label_visibility="collapsed"
                )
                submitted = st.form_submit_button("Send", use_container_width=True, type="primary")

            if submitted and user_message.strip():
                with st.spinner("Thinking..."):
                    handle_chat_message(user_message.strip())
                st.rerun()