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

    .mobile-nav{
        display:none;
    }

    @media (max-width:768px){

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

    }

    </style>

    <div class="mobile-nav">

        <div class="nav-item active">
            <div class="nav-icon">🏠</div>
            Home
        </div>

        <div class="nav-item">
            <div class="nav-icon">📊</div>
            History
        </div>

        <div class="center-button">
            🌿
        </div>

        <div class="nav-item">
            <div class="nav-icon">💡</div>
            Tips
        </div>

        <div class="nav-item">
            <div class="nav-icon">👤</div>
            Profile
        </div>

    </div>
    """, unsafe_allow_html=True)

# Main App UI
main()

# Mobile navbar at bottom
mobile_navbar()