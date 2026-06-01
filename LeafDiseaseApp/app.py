import streamlit as st
from textwrap import dedent
from frontend.ui import main

st.set_page_config(
    page_title="LeafGuard AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def mobile_navbar(active_tab: str):
    all_active = "active" if active_tab in {"all", "home"} else ""
    history_active = "active" if active_tab == "history" else ""
    tips_active = "active" if active_tab == "tips" else ""
    chat_active = "active" if active_tab == "chat" else ""

    nav_html = (
        dedent("""
    <style>
    html{
        scroll-behavior:smooth;
    }
    .main .block-container{
        padding-bottom:105px;
    }
    .mobile-nav{
        display:flex;
        position:fixed;
        bottom:12px;
        left:50%;
        transform:translateX(-50%);
        width:92%;
        max-width:500px;
            height:72px;
            background:rgba(15,23,42,0.95);
            backdrop-filter:blur(12px);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:40px;
            justify-content:space-around;
            align-items:center;
            z-index:99999;
            box-shadow:0 8px 30px rgba(0,0,0,.35);
        }

        .mobile-nav a{
            text-decoration:none;
            color:inherit;
            display:flex;
            align-items:center;
            justify-content:center;
        }

        .nav-item{
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            color:#9ca3af;
            font-size:11px;
            font-weight:600;
            gap:3px;
        }

        .nav-item.active{
            color:#52b788;
        }

        .nav-icon{
            font-size:22px;
        }

        .center-button{
            width:72px;
            height:72px;
            border-radius:50%;
            background:linear-gradient(135deg,#52b788,#40916c);
            display:flex;
            justify-content:center;
            align-items:center;
            color:white;
            font-size:34px;
            margin-top:-35px;
            box-shadow:0 0 25px rgba(82,183,136,.55);
        }

        .center-button a{
            display:flex;
            justify-content:center;
            align-items:center;
            width:100%;
            height:100%;
            color:white;
            text-decoration:none;
        }

    </style>
    <div class="mobile-nav">
        <a href="/" target="_self">
            <div class="nav-item {{all_active}}">
                <div class="nav-icon">🏠</div>
                Home
            </div>
        </a>
        <a href="/history" target="_self">
            <div class="nav-item {{history_active}}">
                <div class="nav-icon">📊</div>
                History
            </div>
        </a>
        <div class="center-button">
            <a href="/" target="_self" aria-label="Go to home page">🌿</a>
        </div>
        <a href="/tips" target="_self">
            <div class="nav-item {{tips_active}}">
                <div class="nav-icon">💡</div>
                Tips
            </div>
        </a>
        <a href="/chat" target="_self">
            <div class="nav-item {{chat_active}}">
                <div class="nav-icon">🤖</div>
                Chat
            </div>
        </a>
    </div>
    """)
        .replace("{{all_active}}", all_active)
        .replace("{{history_active}}", history_active)
        .replace("{{tips_active}}", tips_active)
        .replace("{{chat_active}}", chat_active)
    )

    st.markdown(nav_html, unsafe_allow_html=True)

# Main App UI
active_tab = st.query_params.get("tab", "all")
main(active_tab=active_tab)

# Mobile navbar at bottom
mobile_navbar(active_tab)