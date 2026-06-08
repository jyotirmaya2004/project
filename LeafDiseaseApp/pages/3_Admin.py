import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from frontend.components import page_header
from frontend.styles import load_css
from frontend.chatbot import chatbot_ui

st.set_page_config(
    page_title="Admin - Database Viewer",
    page_icon=":shield:",
    layout="wide",
)

load_css()
page_header(
    "Admin - Database Viewer",
    "View and download the SQLite database directly from the deployed app.",
    "fa-shield-halved",
)

load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

if not st.session_state.get("admin_authenticated", False):
    st.warning("This page is restricted. Please enter the admin password to continue.")
    pwd = st.text_input("Admin Password", type="password")
    if st.button("Login"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    # Render chatbot and stop execution so the database remains hidden
    chatbot_ui()
    st.stop()

if st.button("Logout", icon="🔒"):
    st.session_state.admin_authenticated = False
    st.rerun()

try:
    from supabase import create_client
    supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
    supabase_key = os.getenv("SUPABASE_KEY")
    if not supabase_key:
        st.error("SUPABASE_KEY not found in .env file.")
        st.stop()

    supabase = create_client(supabase_url, supabase_key)
    response = supabase.table("user_history").select("*").execute()
    df = pd.DataFrame(response.data)
    if df.empty:
        df = pd.DataFrame(columns=["id", "username", "timestamp", "disease", "confidence", "image_url"])

    st.write(f"### Total Records: {len(df)}")
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "image_url": st.column_config.ImageColumn("Uploaded Image")
        }
    )

    if not df.empty:
        st.write("#### Manage Records")
        col_sel, col_btn_del, col_btn_all = st.columns([2, 1, 1])
        with col_sel:
            row_id = st.selectbox("Select Record ID to delete", df["id"].tolist(), label_visibility="collapsed")
        with col_btn_del:
            if st.button("Delete Row", use_container_width=True):
                supabase.table("user_history").delete().eq("id", row_id).execute()
                st.rerun()
        with col_btn_all:
            confirm_delete = st.checkbox("Confirm wipe", help="Check this box to enable the delete button")
            if st.button("Delete ALL", type="primary", use_container_width=True, disabled=not confirm_delete):
                supabase.table("user_history").delete().neq("id", -1).execute() # .neq is a wildcard to delete all rows
                st.rerun()
        st.html("<br>")

except Exception as e:
    st.error(f"Could not load database: {e}")

# Render floating chatbot globally
chatbot_ui()