import streamlit as st


def load_css():
    st.html(
        """
        <link rel="stylesheet"
              href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
        <style>
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
        }

        .stApp{
            background:
                radial-gradient(circle at 18% 0%, rgba(82,183,136,0.22), transparent 30%),
                linear-gradient(135deg, #06140f 0%, #0b2b1f 48%, #1b4332 100%);
            color:var(--leaf-text);
        }

        /* #MainMenu, footer, header{
            visibility:hidden;
        } */

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

        .chat-bubble{
            padding:10px 12px;
            border-radius:14px;
            margin-bottom:8px;
            font-size:14px;
            line-height:1.45;
            border:1px solid rgba(255,255,255,0.08);
        word-break: break-word;
        overflow-wrap: break-word;
        }

    .chat-bubble p {
        margin-bottom: 8px;
    }

    .chat-bubble p:last-child {
        margin-bottom: 0;
    }

    .chat-bubble pre {
        background: rgba(0, 0, 0, 0.25);
        padding: 10px;
        border-radius: 8px;
        overflow-x: auto;
        white-space: pre-wrap; /* Only apply pre-wrap to actual code blocks */
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .chat-bubble table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .chat-bubble th, .chat-bubble td {
        border: 1px solid var(--leaf-border);
        padding: 8px;
        text-align: left;
    }

    .chat-bubble th {
        background: rgba(255, 255, 255, 0.05);
    }

        .chat-bubble.assistant{
            background:rgba(255,255,255,0.07);
            color:white;
        }

        .chat-bubble.user{
            background:rgba(82,183,136,0.22);
            color:white;
            margin-left:34px;
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
