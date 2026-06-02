import pandas as pd
import streamlit as st

from frontend.components import page_header, section_title
from frontend.styles import load_css


st.set_page_config(
    page_title="Prediction History",
    page_icon=":clipboard:",
    layout="wide",
)

load_css()
page_header(
    "Prediction History",
    "Review previous analyses from this session and export them as a CSV file.",
    "fa-clock-rotate-left",
)

history = st.session_state.setdefault("prediction_history", [])

section_title("Session Records", "fa-table")
if not history:
    st.info("No predictions available yet. Analyze a leaf from the Home page first.")
else:
    df = pd.DataFrame(history)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download History",
        df.to_csv(index=False),
        file_name="prediction_history.csv",
        mime="text/csv",
        use_container_width=True,
    )
