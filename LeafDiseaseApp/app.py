"""Streamlit web app for plant leaf disease detection."""

from __future__ import annotations

import json
import os
from importlib import import_module
from io import BytesIO
from pathlib import Path
from typing import Any

import httpx
import streamlit as st
from dotenv import load_dotenv
from openai import APIConnectionError, OpenAI
from PIL import Image, ImageOps, UnidentifiedImageError

try:
    register_heif_opener = import_module("pillow_heif").register_heif_opener
    register_heif_opener()
except Exception:
    pass

from predict import PredictionError, load_class_names, predict_disease


BASE_DIR = Path(__file__).resolve().parent
DISEASE_INFO_PATH = BASE_DIR / "disease_info.json"
ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "bmp",
    "gif",
    "tif",
    "tiff",
    "heic",
    "heif",
}

load_dotenv()
CHAT_MODEL = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning")
CHAT_TEMPERATURE = float(os.getenv("NVIDIA_TEMPERATURE", "0.6"))
CHAT_TOP_P = float(os.getenv("NVIDIA_TOP_P", "0.95"))
CHAT_MAX_TOKENS = int(os.getenv("NVIDIA_MAX_TOKENS", "1200"))
CHAT_REASONING_BUDGET = int(os.getenv("NVIDIA_REASONING_BUDGET", "1024"))


def readable_name(class_name: str) -> str:
    """Convert model class labels into user-facing text."""
    return class_name.replace("___", " - ").replace("_", " ").strip()


def normalize_display_text(text: str) -> str:
    """Convert stored guidance text into clean markdown-friendly output."""
    return (
        text.replace("<br />", "\n")
        .replace("<br/>", "\n")
        .replace("<br>", "\n")
        .strip()
    )


def split_class_name(class_name: str) -> tuple[str, str]:
    """Split a PlantVillage-style class into crop and condition names."""
    parts = class_name.split("___", maxsplit=1)
    crop = parts[0].replace("_", " ").replace(",", ", ")
    condition = parts[1].replace("_", " ") if len(parts) > 1 else class_name.replace("_", " ")
    return crop.strip(), condition.strip()


def build_default_disease_info(class_name: str) -> dict[str, str]:
    """Create practical disease guidance for a class when a JSON entry is missing."""
    crop, condition = split_class_name(class_name)
    disease_name = readable_name(class_name)

    if condition.lower() == "healthy":
        return {
            "disease_name": disease_name,
            "symptoms": f"The {crop} leaf appears generally healthy, with even color, normal shape, and no clear disease lesions.",
            "causes": "Healthy results are usually associated with balanced nutrition, suitable watering, good sunlight, and low pest or pathogen pressure.",
            "treatment": "No disease treatment is required. Continue routine crop monitoring and avoid unnecessary pesticide use.",
            "prevention": "Maintain sanitation, rotate crops where appropriate, water at the base of plants, inspect leaves weekly, and remove stressed plant debris.",
        }

    lower_condition = condition.lower()
    if "rust" in lower_condition:
        symptoms = f"{crop} leaves may show orange, brown, or reddish pustules that can spread across the leaf surface."
        causes = "Rust fungi thrive in humid weather, dense canopies, and situations where leaves stay wet for long periods."
        treatment = "Remove heavily infected leaves, improve airflow, and use a crop-approved fungicide early when local guidance recommends it."
    elif "blight" in lower_condition:
        symptoms = f"{crop} leaves may develop dark, expanding spots, scorched margins, yellowing tissue, and rapid leaf decline."
        causes = "Blight is favored by wet foliage, plant stress, infected debris, and warm or cool humid periods depending on the pathogen."
        treatment = "Remove infected debris, avoid overhead irrigation, improve spacing, and apply recommended protective fungicides when disease pressure is high."
    elif "mildew" in lower_condition:
        symptoms = f"{crop} leaves may show white or gray powdery growth, curling, yellowing, and reduced vigor."
        causes = "Powdery mildew is encouraged by crowded plants, shade, moderate humidity, and poor airflow."
        treatment = "Prune crowded growth, remove badly affected leaves, and use sulfur, potassium bicarbonate, or another locally approved fungicide if needed."
    elif "bacterial" in lower_condition:
        symptoms = f"{crop} leaves may show small water-soaked spots that turn brown or black, often with yellow halos."
        causes = "Bacteria spread through splashing water, contaminated tools, infected seed or transplants, and handling wet plants."
        treatment = "Remove infected leaves, disinfect tools, avoid working wet plants, and use copper-based products only where they are locally recommended."
    elif "virus" in lower_condition or "mosaic" in lower_condition or "curl" in lower_condition:
        symptoms = f"{crop} leaves may show mottling, mosaic patterns, curling, distortion, yellowing, and stunted plant growth."
        causes = "Plant viruses are commonly spread by insect vectors, infected transplants, weeds, and contaminated tools."
        treatment = "There is no curative spray for viral infection. Remove severely infected plants and manage insect vectors promptly."
    elif "mite" in lower_condition:
        symptoms = f"{crop} leaves may show stippling, bronzing, fine webbing, curling, and premature leaf drop."
        causes = "Spider mites increase quickly in hot, dry conditions and on water-stressed plants."
        treatment = "Rinse leaf undersides, reduce plant stress, encourage beneficial insects, and use insecticidal soap or miticide when appropriate."
    elif "scab" in lower_condition:
        symptoms = f"{crop} leaves and fruit may develop olive-brown, velvety, scabby lesions and distorted young leaves."
        causes = "Scab fungi survive on infected leaves and spread during cool, wet spring weather."
        treatment = "Remove fallen infected leaves, prune for airflow, and apply preventive fungicides according to local extension advice."
    elif "rot" in lower_condition:
        symptoms = f"{crop} leaves may show dark circular spots, browning tissue, and fruit or stem lesions depending on infection stage."
        causes = "Rot pathogens survive in infected plant material and spread during wet, humid conditions."
        treatment = "Remove infected material, improve sanitation and drainage, and use labeled fungicides as part of an integrated plan."
    else:
        symptoms = f"{crop} leaves may show discoloration, spots, curling, blighting, or other abnormal patterns linked with {condition}."
        causes = "Disease development is often associated with susceptible varieties, infected debris, humid weather, pest vectors, and plant stress."
        treatment = "Remove severely affected leaves, improve airflow and watering practices, and follow local agricultural guidance for approved treatments."

    return {
        "disease_name": disease_name,
        "symptoms": symptoms,
        "causes": causes,
        "treatment": treatment,
        "prevention": "Use clean planting material, rotate crops where possible, remove infected debris, avoid overhead watering, keep tools clean, and monitor plants regularly.",
    }


def ensure_disease_info() -> dict[str, dict[str, str]]:
    """Create or repair disease_info.json so every model class has knowledge-base content."""
    try:
        class_names = load_class_names()
    except PredictionError:
        class_names = []

    disease_info: dict[str, dict[str, str]] = {}
    if DISEASE_INFO_PATH.exists():
        try:
            with DISEASE_INFO_PATH.open("r", encoding="utf-8") as file:
                loaded = json.load(file)
                if isinstance(loaded, dict):
                    disease_info = loaded
        except (json.JSONDecodeError, OSError):
            disease_info = {}

    changed = False
    for class_name in class_names:
        required_keys = {"disease_name", "symptoms", "causes", "treatment", "prevention"}
        existing = disease_info.get(class_name)
        if not isinstance(existing, dict) or not required_keys.issubset(existing):
            disease_info[class_name] = build_default_disease_info(class_name)
            changed = True

    if changed or not DISEASE_INFO_PATH.exists():
        with DISEASE_INFO_PATH.open("w", encoding="utf-8") as file:
            json.dump(disease_info, file, indent=2, ensure_ascii=False)

    return disease_info


def is_allowed_file(file_name: str) -> bool:
    """Validate uploaded file extension."""
    suffix = Path(file_name).suffix.lower().lstrip(".")
    return suffix in ALLOWED_EXTENSIONS


def validate_uploaded_image(uploaded_file: Any) -> Image.Image:
    """Validate and return a displayable image from Streamlit's uploader."""
    if uploaded_file is None:
        raise ValueError("Please upload a leaf image first.")

    if not is_allowed_file(uploaded_file.name):
        raise ValueError("Please upload a common image file such as JPG, PNG, WEBP, BMP, GIF, or TIFF.")

    try:
        raw_bytes = uploaded_file.getvalue()
        image = Image.open(BytesIO(raw_bytes))
        image = ImageOps.exif_transpose(image)
        if getattr(image, "is_animated", False):
            image.seek(0)
        image.verify()

        image = Image.open(BytesIO(raw_bytes))
        image = ImageOps.exif_transpose(image)
        if getattr(image, "is_animated", False):
            image.seek(0)
        return image.convert("RGB")
    except (UnidentifiedImageError, OSError, AttributeError) as exc:
        raise ValueError(
            "The uploaded file does not appear to be a valid image. If you are on a phone, try the camera option "
            "or convert HEIC photos to JPG/PNG if your browser does not support them."
        ) from exc


def image_to_preview_bytes(image: Image.Image) -> bytes:
    """Create a stable image copy independent of Streamlit temp media files."""
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=92, optimize=True)
    return buffer.getvalue()


def agriculture_question(text: str) -> bool:
    """Basic topic gate before sending a chat message to the NVIDIA endpoint."""
    agricultural_terms = {
        "agriculture", "plant", "leaf", "disease", "crop", "farming", "farm", "soil", "fertilizer",
        "pesticide", "fungicide", "insect", "pest", "irrigation", "harvest", "seed", "fruit",
        "vegetable", "symptom", "cause", "treatment", "prevent", "prevention", "tomato", "potato", "corn",
        "maize", "apple", "grape", "pepper", "orange", "peach", "strawberry", "soybean",
        "squash", "cherry", "blueberry", "raspberry", "mildew", "blight", "rust", "rot",
        "scab", "mosaic", "mite", "watering", "compost", "nutrient", "nitrogen", "organic",
        "spray", "remove", "safe", "first",
    }
    normalized = text.lower()
    return any(term in normalized for term in agricultural_terms)


def contextual_follow_up(text: str, disease_context: dict[str, Any] | None) -> bool:
    """Allow short follow-up questions when a prediction gives the chat enough context."""
    if not disease_context:
        return False

    follow_up_terms = {
        "this", "it", "that", "result", "prediction", "prevent", "prevention", "treat", "treatment",
        "symptom", "cause", "safe", "compost", "first", "next", "fix", "control", "manage",
    }
    normalized = text.lower()
    return any(term in normalized for term in follow_up_terms)


def greeting_message(text: str) -> bool:
    """Detect simple greetings that do not need an API call."""
    normalized = text.strip().lower().strip("!.?, ")
    return normalized in {"hi", "hello", "hey", "namaste", "good morning", "good afternoon", "good evening"}


def get_chat_client() -> OpenAI | None:
    """Create an OpenAI-compatible client for NVIDIA NIM APIs."""
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return None
    http_client = httpx.Client(trust_env=False, timeout=60)
    return OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key, http_client=http_client)


def ask_nvidia_assistant(user_message: str, disease_context: dict[str, Any] | None) -> str:
    """Send an agriculture-scoped chat request to NVIDIA with session memory."""
    if greeting_message(user_message):
        return "Hello! Ask me about a plant disease, crop-care issue, fertilizer, soil, pests, or farming practice."

    if not agriculture_question(user_message) and not contextual_follow_up(user_message, disease_context):
        return "I can help with plant diseases, crop care, fertilizers, soil, pests, and farming practices. Please ask me something in that area."

    client = get_chat_client()
    if client is None:
        return "NVIDIA_API_KEY is not configured. Add it to your environment or .env file, then restart Streamlit."

    context_text = ""
    if disease_context:
        context_text = (
            f"Current model prediction: {disease_context.get('disease')} "
            f"with {disease_context.get('confidence')}% confidence."
        )

    messages = [
        {
            "role": "system",
            "content": (
                "You are an agriculture and plant disease assistant. Only answer questions about plant health, "
                "crop disease symptoms, causes, treatment, prevention, fertilizers, soil, irrigation, pests, "
                "and farming practices. If a question is unrelated, politely refuse and redirect to plant care. "
                "Give practical, safe, locally adaptable guidance and recommend local extension advice for chemical use. "
                "Use plain markdown only. Do not output HTML tags such as <br> or raw HTML tables. "
                f"{context_text}"
            ),
        },
        *st.session_state.chat_messages[-10:],
        {"role": "user", "content": user_message},
    ]

    try:
        response = client.chat.completions.create(
            model=os.getenv("NVIDIA_MODEL", CHAT_MODEL),
            messages=messages,
            temperature=CHAT_TEMPERATURE,
            top_p=CHAT_TOP_P,
            max_tokens=CHAT_MAX_TOKENS,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": True},
                "reasoning_budget": CHAT_REASONING_BUDGET,
            },
        )
        return response.choices[0].message.content or "I could not generate a response. Please try again."
    except APIConnectionError:
        return (
            "The NVIDIA assistant could not connect to the API. Restart Streamlit from your normal terminal, "
            "then check your internet connection, VPN, proxy, or firewall settings if this continues."
        )
    except Exception as exc:
        return f"The NVIDIA assistant is currently unavailable: {exc}"


def initialize_session_state() -> None:
    """Prepare Streamlit session variables."""
    st.session_state.setdefault("prediction", None)
    st.session_state.setdefault("chat_messages", [])
    st.session_state.setdefault("selected_image_bytes", None)
    st.session_state.setdefault("selected_image_name", None)


def handle_chat_message(message: str) -> None:
    """Append a chat message and generate the assistant reply."""
    st.session_state.chat_messages.append({"role": "user", "content": message})
    reply = normalize_display_text(ask_nvidia_assistant(message, st.session_state.prediction))
    st.session_state.chat_messages.append({"role": "assistant", "content": reply})


def main() -> None:
    """Run the Streamlit application."""
    st.set_page_config(
        page_title="Plant Leaf Disease Detection",
        page_icon=":seedling:",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    initialize_session_state()
    disease_info = ensure_disease_info()

    from frontend import inject_custom_css, render_chatbot, render_page_header, render_upload_section

    inject_custom_css()
    render_page_header()
    render_upload_section(disease_info)
    render_chatbot()


if __name__ == "__main__":
    main()
