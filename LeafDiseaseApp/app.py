import streamlit as st
from frontend.ui import main

st.set_page_config(
    page_title="LeafGuard AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def mobile_navbar():
    st.markdown("""
    <style>

    html{
        scroll-behavior:smooth;
    }

    .mobile-nav{
        display:none;
    }

    @media (max-width:768px){

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

    }

    </style>

    <div class="mobile-nav">

        <a href="#home-section">
            <div class="nav-item active">
                <div class="nav-icon">🏠</div>
                Home
            </div>
        </a>

        <a href="#history-section">
            <div class="nav-item">
                <div class="nav-icon">📊</div>
                History
            </div>
        </a>

        <div class="center-button">
            <a href="#upload-section" aria-label="Go to upload section">🌿</a>
        </div>

        <a href="#tips-section">
            <div class="nav-item">
                <div class="nav-icon">💡</div>
                Tips
            </div>
        </a>

        <a href="#chat-section">
            <div class="nav-item">
                <div class="nav-icon">🤖</div>
                Chat
            </div>
        </a>

    </div>
    """, unsafe_allow_html=True)

# Main App UI
main()

# Mobile navbar at bottom
mobile_navbar()