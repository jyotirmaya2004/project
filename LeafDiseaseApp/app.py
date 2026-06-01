import streamlit as st
from frontend.ui import main

st.set_page_config(
    page_title="LeafGuard AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

main()