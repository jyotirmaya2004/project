import io
import json
import os
import re
from datetime import datetime

import streamlit as st
from PIL import Image as PILImage

from backend.disease_info import get_disease_details
from backend.predict_two_stage import PredictionError, predict_two_stage
from frontend.chatbot import chatbot_ui
from frontend.components import (
    causes_card,
    page_header,
    prediction_card,
    prevention_card,
    section_title,
    symptoms_card,
    top_predictions_card,
    treatment_card,
)
from frontend.styles import load_css

HISTORY_FILE = "user_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def render_header():
    page_header(
        "AgroVision AI",
        "Upload or capture a leaf image and get instant disease analysis.",
        "fa-leaf",
    )


def render_upload_section():
    section_title("Leaf Image", "fa-camera")

    default_source = 1 if st.query_params.get("source") == "camera" else 0
    source_choice = st.radio(
        "Image source",
        ["Upload from device", "Use camera"],
        index=default_source,
        horizontal=True,
    )

    if source_choice == "Use camera":
        image_file = st.camera_input("Take a clear leaf photo")
    else:
        image_file = st.file_uploader(
            "Choose a leaf image",
            type=["jpg", "jpeg", "png", "webp", "bmp", "gif", "tiff", "heic", "heif"],
        )

    if image_file:
        st.image(image_file, caption="Selected leaf image", use_container_width=True)

    return image_file


def _generate_report_pdf(image_bytes, prediction, disease_info):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
        from reportlab.platypus import Image as RLImage
        from reportlab.lib import colors
        from reportlab.lib.units import inch
    except ImportError:
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=20
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2d6a4f'),
        spaceBefore=12,
        spaceAfter=6
    )

    story = []
    story.append(Paragraph("<b>AgroVision AI - Plant Health Report Card</b>", title_style))
    story.append(Spacer(1, 10))

    if image_bytes:
        try:
            img_io = io.BytesIO(image_bytes)
            pil_img = PILImage.open(img_io)
            # Strip transparency channels for flawless PDF insertion
            if pil_img.mode in ('RGBA', 'LA') or (pil_img.mode == 'P' and 'transparency' in pil_img.info):
                alpha = pil_img.convert('RGBA').split()[-1]
                bg = PILImage.new("RGB", pil_img.size, (255, 255, 255))
                bg.paste(pil_img, mask=alpha)
                pil_img = bg
            else:
                pil_img = pil_img.convert('RGB')

            clean_img_io = io.BytesIO()
            pil_img.save(clean_img_io, format='JPEG')
            clean_img_io.seek(0)

            # Proportionally scale image to fit nicely on the document
            img_width, img_height = pil_img.size
            max_w, max_h = 400.0, 250.0
            ratio = min(max_w / img_width, max_h / img_height)
            new_w, new_h = img_width * ratio, img_height * ratio

            rl_img = RLImage(clean_img_io, width=new_w, height=new_h)

            img_table = Table([[rl_img]], colWidths=[new_w + 10])
            img_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(img_table)
            story.append(Spacer(1, 20))
        except Exception:
            pass

    disease = prediction.get("disease", "Unknown")
    confidence = prediction.get("confidence", 0.0)

    data = [
        [Paragraph("<b>Diagnosed Disease</b>", styles["Normal"]), Paragraph(disease, styles["Normal"])],
        [Paragraph("<b>Model Confidence</b>", styles["Normal"]), Paragraph(f"{confidence}%", styles["Normal"])]
    ]

    top_preds = prediction.get("top_predictions", [])
    if len(top_preds) > 1:
        alts = ", ".join([f"{p['disease']} ({p['confidence']}%)" for p in top_preds[1:]])
        data.append([Paragraph("<b>Other Predictions</b>", styles["Normal"]), Paragraph(alts, styles["Normal"])])

    t = Table(data, colWidths=[1.5*inch, 4.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#eaf4f0')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    if disease_info:
        for section in ["symptoms", "causes", "treatment", "prevention"]:
            if section in disease_info and disease_info[section]:
                story.append(Paragraph(f"{section.title()}", h2_style))
                text = disease_info[section].replace("<", "&lt;").replace(">", "&gt;")
                story.append(Paragraph(text, styles["Normal"]))
                story.append(Spacer(1, 8))

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.dimgrey)
        footer_text = f"AgroVision AI Report Card - Page {doc.page}"
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        date_str = datetime.now().strftime("%B %d, %Y")
        canvas.drawString(0.5 * inch, 0.5 * inch, date_str)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()


def _generate_history_pdf(history_data):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
    except ImportError:
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=20
    )

    story = []
    story.append(Paragraph("<b>AgroVision AI - Prediction History</b>", title_style))
    story.append(Spacer(1, 10))

    if history_data:
        table_data = [[
            Paragraph("<b>Date/Time</b>", styles["Normal"]),
            Paragraph("<b>Disease</b>", styles["Normal"]),
            Paragraph("<b>Confidence</b>", styles["Normal"])
        ]]
        for item in history_data:
            dt = item.get("Timestamp", "N/A")
            disease = item.get("Disease", "Unknown")
            conf = f"{item.get('Confidence', 0)}%"
            table_data.append([
                Paragraph(dt, styles["Normal"]),
                Paragraph(disease, styles["Normal"]),
                Paragraph(conf, styles["Normal"])
            ])

        t = Table(table_data, colWidths=[2.2*inch, 3.5*inch, 1.3*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#eaf4f0')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
    else:
        story.append(Paragraph("No prediction history available.", styles["Normal"]))

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.dimgrey)
        footer_text = f"AgroVision AI History - Page {doc.page}"
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        date_str = datetime.now().strftime("%B %d, %Y")
        canvas.drawString(0.5 * inch, 0.5 * inch, date_str)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()


def render_prediction_section(image_file):
    section_title("Prediction Result", "fa-chart-simple")

    with st.expander("Debug: leaf vs non-leaf output", expanded=False):
        show_debug = st.checkbox("Show raw leaf validation output", value=False)

    if image_file is None:
        st.info("Upload or capture a leaf image to begin.")
        return

    if st.button("Analyze Leaf", use_container_width=True, type="primary"):
        try:
            with st.spinner("Analyzing image..."):
                result = predict_two_stage(image_file, top_k=3)

            st.session_state.prediction = result

            history = load_history()
            history.append(
                {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Disease": result["disease"],
                    "Confidence": result["confidence"],
                }
            )
            save_history(history)
            st.session_state.prediction_history = history
        except PredictionError as exc:
            st.session_state.prediction = None
            st.error(str(exc))
        except Exception as exc:
            st.session_state.prediction = None
            st.error(f"Unexpected error: {exc}")

    result = st.session_state.get("prediction")
    if not result:
        return

    if result.get("validation_warning"):
        st.warning(result["validation_warning"])

    prediction_card(result["disease"], result["confidence"])
    top_predictions_card(
        [(pred["disease"], pred["confidence"]) for pred in result["top_predictions"]]
    )

    if show_debug:
        st.json(result["leaf_validation"])

    disease_info = get_disease_details(result["class_name"])
    symptoms_card(disease_info["symptoms"])
    causes_card(disease_info["causes"])
    treatment_card(disease_info["treatment"])
    prevention_card(disease_info["prevention"])

    st.html("<br>")
    section_title("Diagnosis Report", "fa-file-pdf")
    st.info("Save a detailed PDF report of this diagnosis, including the uploaded image and treatment guidelines.")

    image_bytes = image_file.getvalue() if image_file else None
    pdf_bytes = _generate_report_pdf(image_bytes, result, disease_info)

    if pdf_bytes:
        safe_name = re.sub(r'[^a-zA-Z0-9]+', '_', result['disease']).strip('_').lower()
        st.download_button(
            label="📥 Download Full Report Card",
            data=pdf_bytes,
            file_name=f"agrovision_report_{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.warning("ReportLab is required to generate PDF reports. Please run `pip install reportlab`.")

def render_history_section():
    section_title("Prediction History", "fa-clock-rotate-left")

    history = load_history()
    st.session_state.prediction_history = history

    if not history:
        st.info("No history yet. Analyze a leaf image to see records here.")
        return

    st.dataframe(history, use_container_width=True)

    pdf_bytes = _generate_history_pdf(history)
    if pdf_bytes:
        st.download_button(
            label="📥 Download History PDF",
            data=pdf_bytes,
            file_name="agrovision_ai_history.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


def render_tips_section():
    section_title("Quick Care Tips", "fa-lightbulb")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Use clear, bright photos with one leaf in focus.")
    with col2:
        st.info("Retake blurry images for better model confidence.")
    with col3:
        st.info("Review treatment and prevention before spraying chemicals.")


def render_feature_cards():
    section_title("Features", "fa-seedling")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", "98%")
    col2.metric("Prediction", "<2 sec")
    col3.metric("Diseases", "38+")
    col4.metric("Plants", "15+")


def main(active_tab: str = "all"):
    load_css()
    render_header()

    if active_tab == "history":
        render_history_section()
        return

    if active_tab == "tips":
        render_tips_section()
        return

    if active_tab == "chat":
        chatbot_ui()
        return

    left, right = st.columns([1, 1])
    with left:
        image_file = render_upload_section()
    with right:
        render_prediction_section(image_file)

    st.divider()
    render_feature_cards()

    st.divider()
    render_history_section()

    st.divider()
    render_tips_section()

    st.divider()
    chatbot_ui()
