import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Prediction History")


if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []


history = st.session_state.prediction_history


if len(history) == 0:

    st.info(
        "No predictions available yet."
    )

else:

    df = pd.DataFrame(history)

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        "⬇ Download History",
        csv,
        file_name="prediction_history.csv",
        mime="text/csv"
    )