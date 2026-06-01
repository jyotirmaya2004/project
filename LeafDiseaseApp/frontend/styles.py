import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* Main App */
    .stApp{
        background: linear-gradient(
            135deg,
            #081c15,
            #0b2b1f,
            #1b4332
        );
        color:white;
    }

    /* Remove Streamlit Menu */
    #MainMenu{
        visibility:hidden;
    }

    footer{
        visibility:hidden;
    }

    header{
        visibility:hidden;
    }

    /* Cards */
    .glass-card{
        background:rgba(255,255,255,0.05);
        backdrop-filter:blur(15px);
        border:1px solid rgba(255,255,255,0.1);
        border-radius:20px;
        padding:20px;
        margin-bottom:20px;
    }

    /* Titles */
    h1,h2,h3{
        color:white;
    }

    /* File Uploader */
    section[data-testid="stFileUploader"]{
        border-radius:15px;
        border:2px dashed #52b788;
        background:rgba(255,255,255,0.03);
    }

    /* Buttons */
    .stButton button{

        width:100%;
        height:55px;

        border:none;
        border-radius:15px;

        background:linear-gradient(
            135deg,
            #52b788,
            #2d6a4f
        );

        color:white;
        font-size:18px;
        font-weight:bold;

        transition:0.3s;
    }

    .stButton button:hover{

        transform:translateY(-2px);

        box-shadow:
        0px 5px 20px rgba(82,183,136,0.4);
    }

    /* Metrics */
    div[data-testid="metric-container"]{

        background:rgba(255,255,255,0.05);

        border-radius:15px;

        padding:15px;

        border:1px solid rgba(255,255,255,0.08);
    }

    /* Sidebar */
    section[data-testid="stSidebar"]{
        background:#081c15;
    }

    /* Scrollbar */
    ::-webkit-scrollbar{
        width:8px;
    }

    ::-webkit-scrollbar-thumb{
        background:#52b788;
        border-radius:10px;
    }

    </style>
    """,
    unsafe_allow_html=True)