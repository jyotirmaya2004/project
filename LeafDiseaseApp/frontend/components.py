import streamlit as st


def prediction_card(disease, confidence):

    st.markdown(
        f"""
        <div style="
        background:rgba(255,255,255,0.05);
        padding:25px;
        border-radius:20px;
        border:1px solid rgba(255,255,255,0.1);
        margin-bottom:15px;
        ">
            <h3>🦠 Predicted Disease</h3>

            <h2 style="color:#52b788;">
                {disease}
            </h2>

            <p style="
            font-size:18px;
            font-weight:bold;
            ">
            Confidence: {confidence:.2f}%
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(float(confidence) / 100)

    if confidence >= 90:
        st.success("High Confidence Prediction")
    elif confidence >= 70:
        st.warning("Moderate Confidence Prediction")
    else:
        st.error("Low Confidence Prediction")
def top_predictions_card(predictions):

    st.subheader("📊 Top Predictions")

    for disease, score in predictions:

        st.markdown(
            f"""
            <div style="
            background:rgba(255,255,255,0.04);
            padding:12px;
            border-radius:12px;
            margin-bottom:10px;
            ">
            <b>{disease}</b>
            <span style="float:right;">
            {score:.2f}%
            </span>
            </div>
            """,
            unsafe_allow_html=True
        )


def symptoms_card(text):

    with st.expander("🔍 Symptoms", expanded=True):
        st.write(text)


def causes_card(text):

    with st.expander("⚠ Causes"):
        st.write(text)


def treatment_card(text):

    with st.expander("💊 Treatment"):
        st.write(text)


def prevention_card(text):

    with st.expander("🛡 Prevention"):
        st.write(text)