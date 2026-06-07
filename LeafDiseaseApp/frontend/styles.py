import streamlit as st


def load_css():
    st.html(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
        <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css');
        :root{
            --leaf-bg: #0f172a;
            --leaf-panel: rgba(30, 41, 59, 0.65);
            --leaf-panel-strong: rgba(30, 41, 59, 0.95);
            --leaf-border: rgba(16, 185, 129, 0.25);
            --leaf-primary: #10b981;
            --leaf-primary-dark: #059669;
            --leaf-accent: #fbbf24;
            --leaf-text: #f8fafc;
            --leaf-muted: #94a3b8;
            --leaf-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }


        /* Animated Background */
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stApp {
            background: linear-gradient(135deg, #020617, #0f172a, #064e3b, #022c22);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            color: var(--leaf-text);
            font-family: 'Inter', sans-serif;
        }

        /* Overlay fixed radial gradients so they don't shift, or animate them differently */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: radial-gradient(circle at 15% 15%, rgba(16,185,129,0.12), transparent 45%),
                        radial-gradient(circle at 85% 85%, rgba(5,150,105,0.15), transparent 45%);
            z-index: 0;
            pointer-events: none;
        }

        @keyframes contentFadeIn {
            from { opacity: 0; top: 12px; }
            to { opacity: 1; top: 0px; }
        }

        .block-container {
            position: relative;
            z-index: 1;
            animation: contentFadeIn 0.4s ease-out forwards;
        }

        h1,h2,h3{
            color:var(--leaf-text);
            letter-spacing:0;
        }

        /* --- Text Selection Styling --- */
        ::selection {
            background-color: rgba(16, 185, 129, 0.4);
            color: var(--leaf-text);
        }
        ::-moz-selection {
            background-color: rgba(16, 185, 129, 0.4);
            color: var(--leaf-text);
        }

        /* Placeholder styling */
        .empty-placeholder {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            background: var(--leaf-panel);
            border: 2px dashed var(--leaf-border);
            border-radius: 16px;
            text-align: center;
            color: var(--leaf-muted);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            margin-top: 10px;
        }
        .empty-placeholder i {
            font-size: 48px;
            color: var(--leaf-primary);
            margin-bottom: 16px;
            opacity: 0.8;
        }
        .empty-placeholder h4 {
            color: var(--leaf-text);
            margin-bottom: 8px;
            margin-top: 0;
        }
        .empty-placeholder p {
            margin: 0;
            font-size: 15px;
        }

        /* --- Image Preview Styling --- */
        div[data-testid="stImage"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--leaf-border);
            background: rgba(255, 255, 255, 0.02);
            padding: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        div[data-testid="stImage"] img {
            max-height: 350px !important;
            object-fit: contain !important;
            border-radius: 8px;
        }

        div[data-testid="stImageCaption"] {
            color: var(--leaf-accent);
            font-weight: 600;
            margin-top: 8px;
            font-size: 14px;
        }

        .leaf-hero{
            border:1px solid var(--leaf-border);
            background:linear-gradient(135deg, rgba(30,41,59,0.5), rgba(15,23,42,0.8));
            padding:48px 24px;
            border-radius:24px;
            margin-bottom:32px;
            box-shadow:var(--leaf-shadow);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            text-align: center;
        }

        .leaf-hero h1{
            margin:0;
            font-size:46px;
            line-height:1.2;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, var(--leaf-primary), var(--leaf-accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .leaf-hero p{
            color:var(--leaf-muted);
            margin:12px 0 0;
            font-size:18px;
        }

        .section-title{
            display:flex;
            align-items:center;
            gap:10px;
            color:var(--leaf-text);
            margin:8px 0 14px;
        }

        .section-title i{
            color:var(--leaf-primary);
        }

        .leaf-panel{
            background:var(--leaf-panel);
            border:1px solid var(--leaf-border);
            border-top: 3px solid var(--leaf-primary);
            border-radius:18px;
            padding:18px;
            margin-bottom:16px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }

        .leaf-panel h2,
        .leaf-panel h3,
        .leaf-panel p,
        .leaf-panel li{
            color:var(--leaf-text);
        }

        .leaf-panel p,
        .leaf-panel li{
            color:var(--leaf-muted);
            font-size:15px;
            line-height:1.55;
        }

        .leaf-panel ul{
            margin-bottom:0;
        }

        /* --- Features Grid Animation --- */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 24px;
            margin-top: 10px;
        }

        .feature-card {
            background: linear-gradient(135deg, rgba(30,41,59,0.5), rgba(15,23,42,0.8));
            border: 1px solid var(--leaf-border);
            border-top: 3px solid var(--leaf-primary);
            border-radius: 18px;
            padding: 28px 16px;
            text-align: center;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: var(--leaf-shadow);
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .feature-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 20px 40px -10px rgba(16, 185, 129, 0.3);
            border-color: var(--leaf-primary);
        }

        .feature-icon {
            width: 64px;
            height: 64px;
            margin: 0 auto 16px;
            background: rgba(16, 185, 129, 0.15);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            color: var(--leaf-primary);
            transition: all 0.4s ease;
        }

        .feature-card:hover .feature-icon {
            background: var(--leaf-primary);
            color: white;
            transform: scale(1.1) rotate(5deg);
        }

        .feature-value {
            font-size: 42px;
            font-weight: 800;
            color: var(--leaf-text);
            margin-bottom: 6px;
            line-height: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Inter', sans-serif;
        }

        .feature-value-prefix, .feature-value-suffix {
            font-size: 24px;
            color: var(--leaf-accent);
            font-weight: 700;
            margin: 0 4px;
        }

        .feature-label {
            color: var(--leaf-muted);
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        @media (max-width: 992px) {
            .features-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 480px) {
            .features-grid {
                grid-template-columns: repeat(1, 1fr);
            }
        }

        div[data-testid="stDataFrame"]{
            border:1px solid var(--leaf-border);
            border-radius:14px;
            overflow:hidden;
        }

        /* File Uploader and Camera Input Styling */
        div[data-testid="stCameraInput"]{
            border-radius:16px;
            border:2px dashed var(--leaf-primary);
            background:rgba(255,255,255,0.04);
            padding:8px;
        }

        section[data-testid="stFileUploader"] {
            background: transparent;
            border: none;
            padding: 0;
        }

        /* Style the internal dropzone to look like a modern upload panel */
        div[data-testid="stFileUploaderDropzone"] {
            border-radius: 16px;
            border: 2px dashed var(--leaf-primary);
            background: rgba(255, 255, 255, 0.04);
            padding: 32px 16px;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        div[data-testid="stFileUploaderDropzone"]:hover {
            background: rgba(82, 183, 136, 0.1);
            border-color: var(--leaf-accent);
        }

        /* Hide Streamlit's default cloud SVG and drag-and-drop text */
        div[data-testid="stFileUploaderDropzone"] svg,
        div[data-testid="stFileUploaderDropzoneInstructions"] {
            display: none;
        }

        /* Inject a custom FontAwesome cloud icon */
        div[data-testid="stFileUploaderDropzone"]::before {
            content: "\\f0ee"; /* fa-cloud-arrow-up */
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 42px;
            color: var(--leaf-primary);
            margin-bottom: 16px;
        }

        /* Make the 'Browse files' button match standard app buttons */
        div[data-testid="stFileUploaderDropzone"] button {
            border: none;
            border-radius: 30px;
            background: linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark), var(--leaf-primary));
            background-size: 200% auto;
            color: white;
            font-weight: 700;
            padding: 8px 24px;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        div[data-testid="stFileUploaderDropzone"] button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(82, 183, 136, 0.3);
            background-position: right center;
        }

        div[data-testid="stFileUploaderDropzone"] button:active {
            transform: translateY(1px);
            box-shadow: 0 4px 10px rgba(82, 183, 136, 0.2);
        }

        .stButton button,
        div[data-testid="stDownloadButton"] button {
            border:none;
            border-radius:30px;
            background:linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark), var(--leaf-primary));
            background-size: 200% auto;
            color:white;
            font-weight:700;
            min-height: 48px;
            padding: 12px 24px;
            font-size: 16px;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .stButton button:hover,
        div[data-testid="stDownloadButton"] button:hover {
            transform:translateY(-2px);
            box-shadow:0 12px 28px rgba(16, 185, 129, 0.4);
            background-position: right center;
        }

        .stButton button:active,
        div[data-testid="stDownloadButton"] button:active {
            transform:translateY(1px);
            box-shadow:0 4px 12px rgba(82,183,136,0.2);
        }

        /* --- Primary 'Analyze' Button Customization --- */
        .analyze-btn-spacer {
            height: 16px;
        }

        div[data-testid="stButton"] button[kind="primary"] {
            max-width: 320px;
            margin: 0 auto;
            background: linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark), var(--leaf-primary));
            background-size: 200% auto;
            color: white !important;
            font-size: 18px;
            font-weight: 800;
            padding: 14px 32px;
            min-height: 56px;
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
        }

        div[data-testid="stButton"] button[kind="primary"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(16, 185, 129, 0.45);
            background-position: right center;
        }

        div[data-testid="stButton"] button[kind="primary"]::before {
            content: "\\f610"; /* fa-microscope */
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            margin-right: 12px;
            font-size: 20px;
        }

        /* Strip margins from internal p-tags Streamlit adds to prevent uncentering */
        .stButton button p,
        div[data-testid="stDownloadButton"] button p {
            margin: 0;
        }

        /* Add FontAwesome icon to standard download buttons */
        div[data-testid="stDownloadButton"] button::before {
            content: "\\f019";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            margin-right: 8px;
        }

        /* --- Animated Progress Bar Styling (File Uploads & Predictions) --- */
        @keyframes progressFlow {
            0% { background-position: 200% center; }
            100% { background-position: -200% center; }
        }

        div[data-testid="stProgressBar"] > div {
            background-color: rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
        }

        div[data-testid="stProgressBar"] > div > div {
            background: linear-gradient(90deg, var(--leaf-primary-dark), var(--leaf-primary), var(--leaf-accent), var(--leaf-primary), var(--leaf-primary-dark)) !important;
            background-size: 200% auto !important;
            animation: progressFlow 2s linear infinite !important;
            border-radius: 8px !important;
        }

        /* Mobile Responsive adjustments for buttons */
        @media (max-width: 768px) {
            .stButton button,
            div[data-testid="stDownloadButton"] button {
                font-size: 15px;
                padding: 10px 18px;
                min-height: 44px;
            }
        }

        div[data-testid="metric-container"]{
            background:var(--leaf-panel);
            border-radius:14px;
            padding:14px;
            border:1px solid var(--leaf-border);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        div[data-testid="stExpander"]{
            background:rgba(255,255,255,0.04);
            border:1px solid var(--leaf-border);
            border-radius:14px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        .chat-shell{
            width: 100%;
            background:rgba(8,28,21,0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border:1px solid rgba(82,183,136,0.35);
            border-radius:18px;
            box-shadow:0 22px 65px rgba(0,0,0,0.45);
            padding:14px;
            box-sizing: border-box;
        }

        /* --- Floating chatbot UI --- */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-fab-marker) {
            position: fixed;
            right: 18px;
            bottom: 18px;
            z-index: 9999;
            width: 56px;
            height: 56px;
            gap: 0 !important;
        }

        .chat-fab-marker {
            display: none;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-fab-marker) button {
            width: 56px !important;
            height: 56px !important;
            min-height: 56px !important;
            border-radius: 999px !important;
            border: 1px solid rgba(82,183,136,0.55) !important;
            background: linear-gradient(135deg, rgba(82,183,136,0.95), rgba(45,106,79,0.95)) !important;
            box-shadow: var(--leaf-shadow) !important;
            color: white !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            position: relative !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-fab-marker) button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 24px rgba(82,183,136,0.4) !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-fab-marker) button p {
            display: none !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-fab-marker) button::after {
            content: "\\f544";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 24px;
            color: white;
            position: absolute !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) {
            position: fixed;
            right: 18px;
            bottom: 86px;
            width: min(420px, calc(100vw - 36px));
            max-height: 80vh;
            overflow-y: auto;
            z-index: 10000;
            background: rgba(8,28,21,0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(82,183,136,0.35);
            border-radius: 18px;
            box-shadow: var(--leaf-shadow);
            padding: 16px;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stForm"] {
            border: none;
            padding: 0;
        }

        /* --- Chat Panel Action Buttons --- */
        .chat-btn-download-marker, .chat-btn-clear-marker, .chat-btn-close-marker {
            display: none;
        }

    div[data-testid="stElementContainer"]:has(.chat-btn-download-marker),
    div[data-testid="stElementContainer"]:has(.chat-btn-clear-marker),
    div[data-testid="stElementContainer"]:has(.chat-btn-close-marker) {
        display: none !important;
    }

        /* Prevent header columns from stacking on mobile */
        div[data-testid="stHorizontalBlock"]:has(.chat-btn-clear-marker) {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-btn-clear-marker) > div {
            width: auto !important;
            min-width: 0 !important;
            flex: 0 0 auto !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-btn-clear-marker) > div:nth-child(1) {
            flex: 1 1 auto !important;
            width: 100% !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button,
        div[data-testid="stColumn"]:has(.chat-btn-clear-marker) button,
        div[data-testid="stColumn"]:has(.chat-btn-close-marker) button {
            width: 36px !important;
            height: 36px !important;
            min-height: 36px !important;
            position: relative !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 10px !important;
            color: white !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button:hover,
        div[data-testid="stColumn"]:has(.chat-btn-clear-marker) button:hover,
        div[data-testid="stColumn"]:has(.chat-btn-close-marker) button:hover {
            border-color: rgba(82,183,136,0.5) !important;
            background: rgba(82,183,136,0.1) !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button p,
        div[data-testid="stColumn"]:has(.chat-btn-clear-marker) button p,
        div[data-testid="stColumn"]:has(.chat-btn-close-marker) button p,
        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button svg,
        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button::before {
            display: none !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button::after {
            content: "\\f019";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 16px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        div[data-testid="stColumn"]:has(.chat-btn-clear-marker) button::after {
            content: "\\f1f8";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 16px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        div[data-testid="stColumn"]:has(.chat-btn-close-marker) button::after {
            content: "\\f00d";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 18px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        /* --- Instant Send Button (Paper Plane) --- */
        .chat-btn-send-marker {
            display: none;
        }

    div[data-testid="stElementContainer"]:has(.chat-btn-send-marker) {
        display: none !important;
    }

        div[data-testid="stHorizontalBlock"]:has(.chat-btn-send-marker) {
            align-items: center !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 8px !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-btn-send-marker) > div {
            width: auto !important;
            min-width: 0 !important;
            flex: 0 0 auto !important;
            padding-bottom: 0 !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-btn-send-marker) > div:nth-child(1) {
            flex: 1 1 auto !important;
            width: 100% !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-send-marker) button {
            width: 42px !important;
            height: 42px !important;
            min-height: 42px !important;
            padding: 0 !important;
            margin: 0 !important;
        display: block !important;
        position: relative !important;
            background: linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark)) !important;
            border-radius: 8px !important;
            border: none !important;
        }

    div[data-testid="stColumn"]:has(.chat-btn-send-marker) button * {
            display: none !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-send-marker) button::after {
            content: "\\f1d8";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            color: white;
            font-size: 16px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        }

        /* Hide Streamlit default form spacing inside panel for nicer look */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) .stTextInput {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) .stTextInput input {
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(82,183,136,0.35) !important;
            color: var(--leaf-text) !important;
            height: 42px !important;
            box-sizing: border-box !important;
            border-radius: 8px !important;
        }


        .chat-card{
            margin-bottom:8px;
        }

        .chat-header{
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:12px;
            margin-bottom:10px;
        }

        .chat-title{
            display:flex;
            align-items:center;
            gap:10px;
            font-weight:800;
            color:white;
        }

        .chat-title i{
            color:var(--leaf-accent);
        }

        .chat-launch-copy{
            margin:0 0 10px;
            color:var(--leaf-muted);
            font-size:13px;
        }

        .chat-log{
            max-height:320px;
            overflow-y:auto;
            padding-right:4px;
            margin-bottom:10px;
        }

        /* --- Native Streamlit Chat Message Bubbles --- */
        .user-msg-marker, .assistant-msg-marker {
            display: none;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"] {
            border-radius: 16px;
            padding: 8px 12px;
            margin-bottom: 12px;
            border: 1px solid transparent;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            max-width: 88%;
            width: fit-content;
            overflow-wrap: break-word;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.user-msg-marker) {
            background-color: rgba(82, 183, 136, 0.15) !important;
            border-color: rgba(82, 183, 136, 0.35) !important;
            margin-left: auto !important;
            flex-direction: row-reverse !important;
            border-bottom-right-radius: 4px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.assistant-msg-marker) {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-color: rgba(255, 255, 255, 0.12) !important;
            margin-right: auto !important;
            border-bottom-left-radius: 4px !important;
        }

        /* --- FontAwesome Chat Avatars --- */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessageAvatar"] {
            background-color: rgba(255,255,255,0.05) !important;
            color: transparent !important; /* Hide original emoji */
            position: relative !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border-radius: 50% !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessageAvatar"] svg {
            display: none !important; /* Hide Streamlit native SVG if present */
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.user-msg-marker) div[data-testid="stChatMessageAvatar"]::after {
            content: "\\f007"; /* fa-user */
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            color: white;
            font-size: 16px;
            position: absolute;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.assistant-msg-marker) div[data-testid="stChatMessageAvatar"]::after {
            content: "\\f544"; /* fa-robot */
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            color: var(--leaf-primary);
            font-size: 16px;
            position: absolute;
        }

        /* --- Chat Table Formatting & Overflow Fix --- */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"] table {
            display: block !important;
            overflow-x: auto !important;
            border-collapse: collapse !important;
            margin: 10px 0 !important;
            font-size: 13.5px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"] th,
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"] td {
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            padding: 6px 12px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"] th {
            background: rgba(255, 255, 255, 0.08) !important;
            font-weight: 600 !important;
        }

        .chat-thinking {
            color: var(--leaf-primary);
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 4px 0;
        }

        /* --- Chat Follow-up Suggestions --- */
        .chat-followup-marker { display: none; }

        div[data-testid="stHorizontalBlock"]:has(.chat-followup-marker) {
            gap: 6px !important;
            margin-top: 4px !important;
            margin-bottom: 8px !important;
            flex-wrap: wrap !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-followup-marker) > div[data-testid="stColumn"] {
            width: auto !important;
            min-width: 0 !important;
            flex: 1 1 auto !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-followup-marker) button {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            color: var(--leaf-muted) !important;
            font-size: 13px !important;
            padding: 6px 12px !important;
            min-height: 0 !important;
            height: auto !important;
            border-radius: 16px !important;
            line-height: 1.3 !important;
            white-space: normal !important;
            text-align: center !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-followup-marker) button:hover {
            border-color: var(--leaf-primary) !important;
            color: var(--leaf-text) !important;
            background: rgba(82,183,136,0.15) !important;
        }

        /* --- Global Scrollbar Styling --- */
        ::-webkit-scrollbar {
            width: 14px;
            height: 14px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background-color: var(--leaf-primary-dark);
            border-radius: 10px;
            border: 4px solid transparent;
            background-clip: padding-box;
        }

        ::-webkit-scrollbar-thumb:hover {
            background-color: var(--leaf-primary);
        }

        ::-webkit-scrollbar-corner {
            background: transparent;
        }

        /* Firefox cross-browser support */
        * {
            scrollbar-width: thin;
            scrollbar-color: var(--leaf-primary-dark) rgba(255, 255, 255, 0.02);
        }

        /* --- Attractive Sidebar Styling --- */
        section[data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid var(--leaf-border);
        }

        /* Sidebar Header (App Name/Logo area) */
        div[data-testid="stSidebarNav"]::before {
            content: "\\f4d8  AgroVision AI";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            display: block;
            color: var(--leaf-primary);
            font-size: 22px;
            padding: 32px 24px 16px;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--leaf-border);
            text-align: center;
            letter-spacing: 0.5px;
        }

        /* Link Container */
        div[data-testid="stSidebarNav"] ul {
            padding-top: 8px;
        }

        /* Individual Links */
        a[data-testid="stSidebarNavLink"] {
            border-radius: 12px;
            margin: 4px 16px;
            padding: 12px 16px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            color: var(--leaf-text) !important;
            display: flex;
            align-items: center;
            font-weight: 600;
            background: transparent;
            text-decoration: none !important;
        }

        /* Hover State */
        a[data-testid="stSidebarNavLink"]:hover {
            background: rgba(16, 185, 129, 0.15);
            transform: translateX(4px);
        }

        /* Active State */
        a[data-testid="stSidebarNavLink"][aria-current="page"] {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(5, 150, 105, 0.25));
            border-left: 4px solid var(--leaf-primary);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* Hide Native Icons (Emojis or SVGs) */
        span[data-testid="stSidebarNavLinkIcon"] { display: none !important; }
        a[data-testid="stSidebarNavLink"] svg { display: none !important; }

        /* FontAwesome Icon Base */
        a[data-testid="stSidebarNavLink"]::before {
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            margin-right: 14px;
            font-size: 18px;
            color: var(--leaf-primary);
            width: 24px;
            text-align: center;
            display: inline-block;
        }

        /* Specific Icons based on order (1: Home, 2: History, 3: Dataset, 4: About) */
        div[data-testid="stSidebarNav"] ul li:nth-child(1) a::before { content: "\\f015"; } /* fa-home */
        div[data-testid="stSidebarNav"] ul li:nth-child(2) a::before { content: "\\f1da"; } /* fa-clock-rotate-left */
        div[data-testid="stSidebarNav"] ul li:nth-child(3) a::before { content: "\\f1c0"; } /* fa-database */
        div[data-testid="stSidebarNav"] ul li:nth-child(4) a::before { content: "\\f05a"; } /* fa-circle-info */

        </style>
        """,

    )
