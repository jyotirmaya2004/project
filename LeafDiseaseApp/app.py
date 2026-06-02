import streamlit as st

from frontend.ui import main


st.set_page_config(
    page_title="LeafGuard AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)


active_tab = st.query_params.get("tab", "all")
main(active_tab=active_tab)
