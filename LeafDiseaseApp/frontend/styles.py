import streamlit as st


def load_css():
    st.html(
        """
        <style>
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css');

        :root{
            --leaf-bg:#081c15;
            --leaf-panel:rgba(255,255,255,0.07);
            --leaf-panel-strong:rgba(255,255,255,0.12);
            --leaf-border:rgba(255,255,255,0.14);
            --leaf-primary:#52b788;
            --leaf-primary-dark:#2d6a4f;
            --leaf-accent:#ffd166;
            --leaf-text:#f8fafc;
            --leaf-muted:#cbd5e1;
            --leaf-shadow: 0 22px 65px rgba(0,0,0,0.45);
        }


        .stApp{
            background:
                radial-gradient(circle at 18% 0%, rgba(82,183,136,0.22), transparent 30%),
                linear-gradient(135deg, #06140f 0%, #0b2b1f 48%, #1b4332 100%);
            color:var(--leaf-text);
        }

        h1,h2,h3{
            color:var(--leaf-text);
            letter-spacing:0;
        }

        .leaf-hero{
            border:1px solid var(--leaf-border);
            background:linear-gradient(135deg, rgba(82,183,136,0.20), rgba(255,255,255,0.06));
            padding:24px;
            border-radius:18px;
            margin-bottom:22px;
            box-shadow:0 18px 45px rgba(0,0,0,0.22);
        }

        .leaf-hero h1{
            margin:0;
            font-size:40px;
            line-height:1.1;
        }

        .leaf-hero p{
            color:var(--leaf-muted);
            margin:8px 0 0;
            font-size:16px;
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
            border-radius:16px;
            padding:18px;
            margin-bottom:16px;
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

        div[data-testid="stDataFrame"]{
            border:1px solid var(--leaf-border);
            border-radius:14px;
            overflow:hidden;
        }

        section[data-testid="stFileUploader"],
        div[data-testid="stCameraInput"]{
            border-radius:16px;
            border:2px dashed var(--leaf-primary);
            background:rgba(255,255,255,0.04);
            padding:8px;
        }

        .stButton button{
            border:none;
            border-radius:14px;
            background:linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark));
            color:white;
            font-weight:700;
            min-height:46px;
            transition:transform 0.18s ease, box-shadow 0.18s ease;
        }

        .stButton button:hover{
            transform:translateY(-1px);
            box-shadow:0 10px 24px rgba(82,183,136,0.28);
        }

        div[data-testid="metric-container"]{
            background:var(--leaf-panel);
            border-radius:14px;
            padding:14px;
            border:1px solid var(--leaf-border);
        }

        div[data-testid="stExpander"]{
            background:rgba(255,255,255,0.04);
            border:1px solid var(--leaf-border);
            border-radius:14px;
        }

        .chat-shell{
        width: 100%;
            background:rgba(8,28,21,0.97);
            border:1px solid rgba(82,183,136,0.35);
            border-radius:18px;
            box-shadow:0 22px 65px rgba(0,0,0,0.45);
            padding:14px;
        box-sizing: border-box;
        }

        /* --- Floating chatbot UI --- */
        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-fab-marker) {
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

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-fab-marker) button {
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

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-fab-marker) button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 24px rgba(82,183,136,0.4) !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-fab-marker) button p {
            display: none !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-fab-marker) button::after {
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

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) {
            position: fixed;
            right: 18px;
            bottom: 86px;
            width: min(420px, calc(100vw - 36px));
            max-height: 80vh;
            overflow-y: auto;
            z-index: 10000;
            background: rgba(8,28,21,0.98);
            border: 1px solid rgba(82,183,136,0.35);
            border-radius: 18px;
            box-shadow: var(--leaf-shadow);
            padding: 16px;
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stForm"] {
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
        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button svg {
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
        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) .stTextInput {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) .stTextInput input {
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

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessage"] {
            border-radius: 16px;
            padding: 8px 12px;
            margin-bottom: 12px;
            border: 1px solid transparent;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            max-width: 88%;
            width: fit-content;
            overflow-wrap: break-word;
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.user-msg-marker) {
            background-color: rgba(82, 183, 136, 0.15) !important;
            border-color: rgba(82, 183, 136, 0.35) !important;
            margin-left: auto !important;
            flex-direction: row-reverse !important;
            border-bottom-right-radius: 4px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.assistant-msg-marker) {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-color: rgba(255, 255, 255, 0.12) !important;
            margin-right: auto !important;
            border-bottom-left-radius: 4px !important;
        }

        /* --- FontAwesome Chat Avatars --- */
        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessageAvatar"] {
            background-color: rgba(255,255,255,0.05) !important;
            color: transparent !important; /* Hide original emoji */
            position: relative !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border-radius: 50% !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessageAvatar"] svg {
            display: none !important; /* Hide Streamlit native SVG if present */
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.user-msg-marker) div[data-testid="stChatMessageAvatar"]::after {
            content: "\\f007"; /* fa-user */
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            color: white;
            font-size: 16px;
            position: absolute;
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.assistant-msg-marker) div[data-testid="stChatMessageAvatar"]::after {
            content: "\\f544"; /* fa-robot */
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            color: var(--leaf-primary);
            font-size: 16px;
            position: absolute;
        }

        /* --- Chat Table Formatting & Overflow Fix --- */
        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessage"] table {
            display: block !important;
            overflow-x: auto !important;
            border-collapse: collapse !important;
            margin: 10px 0 !important;
            font-size: 13.5px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessage"] th,
        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessage"] td {
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            padding: 6px 12px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div.element-container .chat-floating-panel-marker) div[data-testid="stChatMessage"] th {
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

        ::-webkit-scrollbar{
            width:8px;
        }

        ::-webkit-scrollbar-thumb{
            background:var(--leaf-primary);
            border-radius:10px;
        }
        </style>
        """,

    )
