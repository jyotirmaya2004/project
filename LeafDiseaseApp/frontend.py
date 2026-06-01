"""Premium Streamlit frontend for the Leaf Disease App."""

from __future__ import annotations

from io import BytesIO
from textwrap import dedent

import streamlit as st
from PIL import Image, UnidentifiedImageError

from app import (
    ALLOWED_EXTENSIONS,
    PredictionError,
    ask_nvidia_assistant,
    build_default_disease_info,
    image_to_preview_bytes,
    normalize_display_text,
    predict_disease,
    validate_uploaded_image,
)


def initialize_session_state() -> None:
    """Prepare Streamlit session variables used by the frontend."""
    st.session_state.setdefault("upload_mode", "gallery")
    st.session_state.setdefault("selected_image_bytes", None)
    st.session_state.setdefault("selected_image_name", None)
    st.session_state.setdefault("prediction", None)
    st.session_state.setdefault("chat_open", False)
    st.session_state.setdefault("chat_messages", [])


def inject_custom_css() -> None:
    """Apply the premium dark botanical theme and responsive layout."""
    st.markdown(
        dedent(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            :root {
                --bg: #121814;
                --panel: rgba(17, 24, 20, 0.86);
                --panel-solid: #18211c;
                --text: #eef6f1;
                --muted: #a7b6ad;
                --line: rgba(167, 243, 208, 0.14);
                --line-strong: rgba(167, 243, 208, 0.26);
                --primary: #10b981;
                --primary-2: #34d399;
                --warning: #f59e0b;
                --radius: 18px;
                --shadow: 0 18px 50px rgba(0, 0, 0, 0.28);
            }

            html, body, [data-testid="stAppViewContainer"] {
                font-family: Inter, system-ui, -apple-system, "Segoe UI", sans-serif;
                background:
                    radial-gradient(circle at top, rgba(16, 185, 129, 0.12), transparent 35%),
                    linear-gradient(180deg, #0e1411 0%, #121814 100%);
                color: var(--text);
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            [data-testid="stToolbar"] {
                visibility: hidden;
                height: 0;
            }

            [data-testid="collapsedControl"],
            [data-testid="stSidebar"],
            [data-testid="stSidebarContent"] {
                display: none !important;
            }

            .main .block-container {
                max-width: 1160px;
                padding: 84px 20px 36px;
            }

            .topbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 16px;
                margin-bottom: 18px;
            }

            .brand {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .brand-badge {
                width: 46px;
                height: 46px;
                border-radius: 14px;
                display: grid;
                place-items: center;
                background: linear-gradient(135deg, var(--primary), var(--primary-2));
                color: #04110c;
                font-size: 22px;
                box-shadow: 0 12px 30px rgba(16, 185, 129, 0.28);
            }

            .brand h1 {
                margin: 0;
                font-size: 1.35rem;
                line-height: 1;
                color: var(--text);
            }

            .brand p {
                margin: 4px 0 0;
                font-size: 0.88rem;
                color: var(--muted);
            }

            .status-pill {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 10px 14px;
                border-radius: 999px;
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.25);
                color: #c9f7e5;
                font-weight: 700;
                box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.04), 0 0 24px rgba(16, 185, 129, 0.08);
            }

            .glass-card {
                position: relative;
                border-radius: var(--radius);
                background: linear-gradient(180deg, rgba(24, 33, 28, 0.92), rgba(18, 24, 20, 0.88));
                border: 1px solid rgba(167, 243, 208, 0.14);
                box-shadow: var(--shadow);
                overflow: hidden;
            }

            .glass-card::before {
                content: "";
                position: absolute;
                inset: 0;
                padding: 1px;
                border-radius: inherit;
                background: linear-gradient(135deg, rgba(16,185,129,0.8), rgba(167,243,208,0.05), rgba(245,158,11,0.25));
                mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
                mask-composite: exclude;
                pointer-events: none;
            }

            .upload-panel {
                padding: 22px;
            }

            .upload-title {
                margin: 0 0 6px;
                font-size: 1.08rem;
                color: var(--text);
                font-weight: 800;
            }

            .upload-subtitle {
                margin: 0 0 16px;
                color: var(--muted);
                font-size: 0.95rem;
            }

            .upload-hero {
                display: grid;
                place-items: center;
                min-height: 220px;
                border-radius: 16px;
                border: 1.5px dashed rgba(167, 243, 208, 0.26);
                background:
                    radial-gradient(circle at center, rgba(16, 185, 129, 0.08), transparent 58%),
                    rgba(255, 255, 255, 0.02);
                text-align: center;
                padding: 18px;
            }

            .upload-hero .icon {
                font-size: 52px;
                line-height: 1;
                margin-bottom: 10px;
            }

            .upload-hero strong {
                display: block;
                font-size: 1.05rem;
                color: var(--text);
                margin-bottom: 6px;
            }

            .upload-hero span {
                color: var(--muted);
                font-size: 0.92rem;
                max-width: 420px;
            }

            .mode-row {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 12px;
                margin-top: 14px;
            }

            .mode-row .stButton > button {
                width: 100%;
                border-radius: 14px;
                min-height: 52px;
                font-weight: 800;
                border: 1px solid rgba(167, 243, 208, 0.16);
                background: rgba(255, 255, 255, 0.03);
                color: var(--text);
            }

            .mode-row .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, var(--primary), var(--primary-2));
                color: #04110c;
                box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.16), 0 12px 28px rgba(16, 185, 129, 0.22);
            }

            [data-testid="stFileUploader"] {
                border: none;
                padding: 0;
                background: transparent;
            }

            [data-testid="stFileUploader"] section {
                border-radius: 14px;
                border: 1px solid rgba(167, 243, 208, 0.18) !important;
                background: rgba(255, 255, 255, 0.03) !important;
            }

            [data-testid="stCameraInput"] {
                border-radius: 14px;
                border: 1px solid rgba(167, 243, 208, 0.18);
                background: rgba(255, 255, 255, 0.03);
                padding: 12px;
            }

            [data-testid="stFileUploader"] label,
            [data-testid="stCameraInput"] label,
            [data-testid="stFileUploader"] p,
            [data-testid="stCameraInput"] p,
            [data-testid="stFileUploader"] small,
            [data-testid="stCameraInput"] small {
                color: var(--text) !important;
                opacity: 1 !important;
                font-weight: 600;
            }

            .preview-label {
                margin: 18px 0 8px;
                color: var(--muted);
                font-size: 0.8rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }

            [data-testid="stImage"] img {
                border-radius: 16px;
                border: 1px solid rgba(167, 243, 208, 0.18);
                object-fit: cover;
                max-height: 440px;
            }

            .cta-bar {
                margin-top: 16px;
                position: sticky;
                bottom: 14px;
                z-index: 20;
            }

            .cta-bar .stButton > button {
                width: 100%;
                min-height: 58px;
                border-radius: 16px;
                font-size: 1rem;
                font-weight: 900;
                color: #04110c;
                background: linear-gradient(90deg, #10b981, #34d399, #10b981);
                background-size: 200% 100%;
                border: none;
                box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
                animation: pulseGlow 2.6s ease-in-out infinite;
            }

            .cta-bar .stButton > button:hover {
                transform: translateY(-1px);
            }

            @keyframes pulseGlow {
                0% { box-shadow: 0 0 0 rgba(16,185,129,0.0), 0 10px 28px rgba(16,185,129,0.22); background-position: 0% 50%; }
                50% { box-shadow: 0 0 22px rgba(16,185,129,0.25), 0 12px 34px rgba(16,185,129,0.28); background-position: 100% 50%; }
                100% { box-shadow: 0 0 0 rgba(16,185,129,0.0), 0 10px 28px rgba(16,185,129,0.22); background-position: 0% 50%; }
            }

            .panel-title {
                margin: 0 0 6px;
                font-size: 1.08rem;
                font-weight: 800;
                color: var(--text);
            }

            .panel-subtitle {
                margin: 0 0 16px;
                color: var(--muted);
                font-size: 0.94rem;
            }

            .result-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 12px;
            }

            .result-card {
                padding: 14px;
                border-radius: 16px;
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(167, 243, 208, 0.14);
            }

            .result-card .label {
                display: block;
                margin-bottom: 6px;
                color: var(--muted);
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.04em;
                font-weight: 800;
            }

            .result-card .value {
                color: var(--text);
                font-size: 1.1rem;
                font-weight: 800;
                line-height: 1.25;
            }

            .top-list {
                display: grid;
                gap: 10px;
                margin-top: 14px;
            }

            .top-row {
                display: flex;
                justify-content: space-between;
                gap: 12px;
                align-items: center;
                padding: 12px 14px;
                border-radius: 14px;
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(167, 243, 208, 0.12);
            }

            .top-row strong {
                color: var(--text);
            }

            .top-row span {
                color: var(--muted);
                font-weight: 700;
            }

            .info-card {
                padding: 14px;
                border-radius: 16px;
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(167, 243, 208, 0.14);
                line-height: 1.65;
                color: var(--text);
            }

            .fab-chat {
                position: fixed;
                right: 18px;
                bottom: 18px;
                width: 58px;
                height: 58px;
                border-radius: 50%;
                display: grid;
                place-items: center;
                z-index: 999;
                background: linear-gradient(135deg, #10b981, #34d399);
                color: #06110c;
                box-shadow: 0 18px 40px rgba(16, 185, 129, 0.34);
                border: 1px solid rgba(255, 255, 255, 0.14);
            }

            .fab-chat button {
                width: 58px !important;
                height: 58px !important;
                border-radius: 50% !important;
                padding: 0 !important;
                font-size: 1.2rem !important;
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
            }

            .chat-panel {
                position: fixed;
                right: 18px;
                bottom: 88px;
                width: 380px;
                max-width: calc(100vw - 36px);
                z-index: 998;
                border-radius: 18px;
                background: rgba(17, 24, 20, 0.98);
                border: 1px solid rgba(167, 243, 208, 0.14);
                box-shadow: var(--shadow);
                padding: 16px;
            }

            .chat-panel h3 {
                margin: 0 0 8px;
                color: var(--text);
            }

            .chat-panel .stCaption,
            .chat-panel label,
            .chat-panel p {
                color: var(--muted);
            }

            .chat-context {
                margin: 0 0 12px;
                padding: 10px 12px;
                border-radius: 14px;
                background: rgba(16, 185, 129, 0.08);
                border: 1px solid rgba(16, 185, 129, 0.16);
                color: var(--text);
            }

            .chat-panel [data-testid="stChatMessage"] {
                border-radius: 14px;
                border: 1px solid rgba(167, 243, 208, 0.12);
                background: rgba(255, 255, 255, 0.03);
                color: var(--text);
            }

            .chat-panel [data-testid="stTextInput"] input {
                border-radius: 14px;
                border: 1px solid rgba(167, 243, 208, 0.14);
                background: rgba(255, 255, 255, 0.04);
                color: var(--text);
            }

            .chat-panel .stButton > button[kind="primary"] {
                border-radius: 14px;
                min-height: 50px;
                font-weight: 800;
                background: linear-gradient(135deg, var(--primary), var(--primary-2));
                color: #04110c;
            }

            .streamlit-expanderHeader {
                color: var(--text) !important;
                font-weight: 800;
            }

            @media (max-width: 900px) {
                .main .block-container {
                    padding: 64px 14px 28px;
                }

                .topbar {
                    align-items: flex-start;
                }

                .result-grid {
                    grid-template-columns: 1fr;
                }

                .upload-hero {
                    min-height: 180px;
                }

                .chat-panel {
                    width: calc(100vw - 24px);
                    right: 12px;
                    bottom: 80px;
                }
            }

            @media (max-width: 520px) {
                .main .block-container {
                    padding-top: 72px;
                }

                .brand h1 {
                    font-size: 1.12rem;
                }

                .mode-row {
                    grid-template-columns: 1fr;
                }

                .brand-badge {
                    width: 42px;
                    height: 42px;
                    font-size: 18px;
                }

                .fab-chat {
                    right: 12px;
                    bottom: 12px;
                    width: 54px;
                    height: 54px;
                }
            }
            </style>
            """
        ),
        unsafe_allow_html=True,
    )


def render_topbar() -> None:
    """Render the premium header and status pill."""
    st.markdown(
        """
        <div class="topbar">
            <div class="brand">
                <div class="brand-badge">🌿</div>
                <div>
                    <h1>LeafShield AI</h1>
                    <p>Leaf disease detection for field and garden use</p>
                </div>
            </div>
            <div class="status-pill">● System Active & Ready</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_upload_card() -> Image.Image | None:
    """Render the upload area and return a validated image if available."""
    st.markdown(
        """
        <div class="glass-card upload-panel">
            <div class="upload-title">Scan a leaf image</div>
            <div class="upload-subtitle">Take a photo or upload one from your gallery.</div>
            <div class="upload-hero">
                <div>
                    <div class="icon">🍃</div>
                    <strong>Drag and drop or tap to upload</strong>
                    <span>Best results come from a clear, well-lit leaf filling most of the frame.</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mode_left, mode_right = st.columns(2, gap="small")
    with mode_left:
        if st.button("📷 Take a Photo", use_container_width=True, type="primary"):
            st.session_state.upload_mode = "camera"
    with mode_right:
        if st.button("📁 Upload from Gallery", use_container_width=True):
            st.session_state.upload_mode = "gallery"

    image = None
    source_file = None

    if st.session_state.upload_mode == "camera":
        source_file = st.camera_input("Take a leaf photo")
    else:
        source_file = st.file_uploader(
            "Upload a leaf image",
            type=sorted(ALLOWED_EXTENSIONS),
            accept_multiple_files=False,
            label_visibility="visible",
        )

    if source_file:
        try:
            image = validate_uploaded_image(source_file)
            st.session_state.selected_image_bytes = image_to_preview_bytes(image)
            st.session_state.selected_image_name = getattr(source_file, "name", "Captured image")
        except ValueError as exc:
            st.session_state.selected_image_bytes = None
            st.session_state.selected_image_name = None
            st.session_state.prediction = None
            st.error(str(exc))

    if st.session_state.selected_image_bytes:
        try:
            image = Image.open(BytesIO(st.session_state.selected_image_bytes)).convert("RGB")
            st.markdown('<div class="preview-label">Selected image preview</div>', unsafe_allow_html=True)
            st.image(image, caption=st.session_state.selected_image_name or "Selected image", use_column_width=True)
        except (UnidentifiedImageError, OSError):
            image = None
            st.session_state.selected_image_bytes = None
            st.session_state.selected_image_name = None
            st.warning("The selected image preview expired. Please upload or capture it again.")

    return image


def render_analyze_cta(image: Image.Image | None) -> bool:
    """Render the sticky analyze CTA and return whether it was clicked."""
    if image is None or not st.session_state.selected_image_bytes:
        return False

    with st.container():
        st.markdown('<div id="analyze-cta"></div>', unsafe_allow_html=True)
        return st.button("Analyze Leaf Image", use_container_width=True, type="primary")


def render_prediction_results(prediction: dict[str, object], disease_info: dict[str, dict[str, str]]) -> None:
    """Display the model result and disease guidance cards."""
    st.markdown(
        """
        <div class="glass-card upload-panel">
            <div class="panel-title">Prediction Result</div>
            <div class="panel-subtitle">Most likely class and confidence ranking.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="result-grid" style="margin-top: 14px;">
            <div class="result-card">
                <span class="label">Predicted Disease</span>
                <div class="value">{prediction['disease']}</div>
            </div>
            <div class="result-card">
                <span class="label">Confidence Score</span>
                <div class="value">{prediction['confidence']:.2f}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    leaf_validation = prediction.get("leaf_validation")
    if leaf_validation:
        st.markdown(
            f"""
            <div class="chat-context" style="margin-top: 14px;">
                <strong>Leaf validation passed</strong><br />
                {leaf_validation['leaf_confidence']:.2f}% leaf confidence
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='top-list'>", unsafe_allow_html=True)
    for top_prediction in prediction["top_predictions"]:
        st.markdown(
            f"""
            <div class="top-row">
                <strong>{top_prediction['disease']}</strong>
                <span>{top_prediction['confidence']:.2f}%</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    info = disease_info.get(prediction["class_name"], build_default_disease_info(prediction["class_name"]))

    st.markdown(
        """
        <div class="glass-card upload-panel" style="margin-top: 18px;">
            <div class="panel-title">Disease Guidance</div>
            <div class="panel-subtitle">Symptoms, causes, treatment, and prevention.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for title, key in [
        ("Symptoms", "symptoms"),
        ("Causes", "causes"),
        ("Treatment", "treatment"),
        ("Prevention", "prevention"),
    ]:
        with st.expander(title, expanded=title in {"Symptoms", "Treatment"}):
            st.markdown(f"<div class='info-card'>{normalize_display_text(info[key])}</div>", unsafe_allow_html=True)


def handle_chat_message(message: str) -> None:
    """Append a chat message and generate the assistant reply."""
    st.session_state.chat_messages.append({"role": "user", "content": message})
    with st.chat_message("user"):
        st.markdown(normalize_display_text(message))

    with st.chat_message("assistant"):
        with st.spinner("Thinking through the crop-care details..."):
            reply = normalize_display_text(ask_nvidia_assistant(message, st.session_state.prediction))
            st.markdown(reply)

    st.session_state.chat_messages.append({"role": "assistant", "content": reply})


def render_chat_fab() -> None:
    """Render the floating chat assistant launcher."""
    with st.container():
        st.markdown('<div id="chat-fab-anchor"></div>', unsafe_allow_html=True)
        if st.button("💬", key="chat_fab_button", help="Open AI assistant"):
            st.session_state.chat_open = not st.session_state.chat_open
            st.rerun()


def render_chat_panel() -> None:
    """Render the floating AI assistant panel."""
    if not st.session_state.chat_open:
        return

    with st.container():
        st.markdown('<div id="chat-panel-anchor"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="chat-panel">
                <h3>AI Plant Care</h3>
                <div class="panel-subtitle">Ask about treatment, prevention, fertilizer, pests, and crop care.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Close", key="close_chat", use_container_width=True):
            st.session_state.chat_open = False
            st.rerun()

        prediction = st.session_state.prediction
        if prediction:
            st.markdown(
                f"""
                <div class="chat-context">
                    <strong>Current context</strong><br />
                    {prediction['disease']} · {prediction['confidence']:.2f}% confidence
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.container(height=320):
            for message in st.session_state.chat_messages[-12:]:
                with st.chat_message(message["role"]):
                    st.markdown(normalize_display_text(message["content"]))

        with st.form("chat_form", clear_on_submit=True):
            user_message = st.text_input(
                "Message",
                placeholder="e.g. How do I treat leaf rust?",
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button("Send", use_container_width=True, type="primary")

        if submitted and user_message.strip():
            handle_chat_message(user_message.strip())
            st.rerun()


def main() -> None:
    """Run the redesigned Streamlit frontend."""
    st.set_page_config(
        page_title="LeafShield AI",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    initialize_session_state()
    inject_custom_css()
    render_topbar()

    disease_info = {}
    try:
        from app import ensure_disease_info

        disease_info = ensure_disease_info()
    except Exception:
        disease_info = {}

    image = render_upload_card()

    if source_file := st.session_state.get("selected_image_bytes"):
        if len(source_file) > 15 * 1024 * 1024:
            st.warning("Large mobile photos can fail during upload. If that happens, resize the image or retake it.")

    analyze_clicked = render_analyze_cta(image)
    if analyze_clicked and image is not None and st.session_state.selected_image_bytes:
        try:
            with st.spinner("Analyzing leaf image..."):
                st.session_state.prediction = predict_disease(BytesIO(st.session_state.selected_image_bytes))
            st.success("Leaf validation passed. Disease prediction completed.")
        except PredictionError as exc:
            st.session_state.prediction = None
            st.error(str(exc))
        except Exception:
            st.session_state.prediction = None
            st.error("Something went wrong while analyzing the image. Please try a clearer leaf photo.")

    if st.session_state.prediction:
        render_prediction_results(st.session_state.prediction, disease_info)

    render_chat_fab()
    render_chat_panel()


if __name__ == "__main__":
    main()
