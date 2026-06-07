import streamlit as st


def page_header(title: str, subtitle: str, icon: str = "fa-leaf") -> None:
    st.html(
        f"""
        <div class="leaf-hero">
            <h1><i class="fa-solid {icon}"></i> {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
    )


def section_title(title: str, icon: str) -> None:
    st.html(
        f'<h3 class="section-title"><i class="fa-solid {icon}"></i> {title}</h3>',
    )


def empty_placeholder(icon: str, title: str, description: str = "") -> None:
    st.html(
        f"""
        <div class="empty-placeholder">
            <i class="fa-solid {icon}"></i>
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """
    )


def prediction_card(disease, confidence):
    confidence = float(confidence)

    section_title("Predicted Disease", "fa-virus")
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
    section_title("Top Predictions", "fa-ranking-star")

    for disease, score in predictions:
        left, right = st.columns([3, 1])
        left.write(str(disease))
        right.write(f"{float(score):.2f}%")


def symptoms_card(text):
    with st.expander("🩺 Symptoms", expanded=True):
        st.write(text)


def causes_card(text):
    with st.expander("🦠 Causes"):
        st.write(text)


def treatment_card(text):
    with st.expander("💊 Treatment"):
        st.write(text)


def prevention_card(text):
    with st.expander("🛡️ Prevention"):
        st.write(text)
