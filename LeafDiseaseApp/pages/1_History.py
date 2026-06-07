import pandas as pd
import streamlit as st

from frontend.components import page_header, section_title
from frontend.styles import load_css
from frontend.ui import load_history, _generate_history_pdf
from frontend.chatbot import chatbot_ui


st.set_page_config(
    page_title="Prediction History",
    page_icon=":clipboard:",
    layout="wide",
)

load_css()
page_header(
    "Prediction History",
    "Review previous analyses and export them as a PDF or CSV file.",
    "fa-clock-rotate-left",
)

history = load_history()

section_title("Session Records", "fa-table")
if not history:
    st.info("No predictions available yet. Analyze a leaf from the Home page first.")
else:
    df = pd.DataFrame(history)
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)

    pdf_bytes = _generate_history_pdf(history)
    if pdf_bytes:
        with col1:
            st.download_button(
                label="Download History PDF",
                data=pdf_bytes,
                file_name="agrovision_ai_history.pdf",
                mime="application/pdf",
            )
    with col2:
        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name="prediction_history.csv",
            mime="text/csv",
        )

# Render floating chatbot globally
chatbot_ui()
