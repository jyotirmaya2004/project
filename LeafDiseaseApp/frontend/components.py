import streamlit as st


def prediction_card(disease, confidence):
    confidence = float(confidence)

    st.subheader("Predicted Disease")
    st.metric(
        label=str(disease),
        value=f"{confidence:.2f}% confidence",
    )

    st.progress(max(0.0, min(confidence / 100, 1.0)))

    if confidence >= 90:
        st.success("High Confidence Prediction")
    elif confidence >= 70:
        st.warning("Moderate Confidence Prediction")
    else:
        st.error("Low Confidence Prediction")


def top_predictions_card(predictions):
    st.subheader("Top Predictions")

    for disease, score in predictions:
        left, right = st.columns([3, 1])
        left.write(str(disease))
        right.write(f"{float(score):.2f}%")


def symptoms_card(text):
    with st.expander("Symptoms", expanded=True):
        st.write(text)


def causes_card(text):
    with st.expander("Causes"):
        st.write(text)


def treatment_card(text):
    with st.expander("Treatment"):
        st.write(text)


def prevention_card(text):
    with st.expander("Prevention"):
        st.write(text)
