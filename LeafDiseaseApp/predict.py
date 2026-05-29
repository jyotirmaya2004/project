"""Prediction utilities for the Plant Leaf Disease Detection app."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, BinaryIO

import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "leaf_disease_model.keras"
CLASS_NAMES_PATH = BASE_DIR / "model" / "class_names.json"
IMAGE_SIZE = (224, 224)
ALLOWED_FORMATS = {"JPEG", "PNG"}


class PredictionError(Exception):
    """Raised when an image cannot be processed or predicted safely."""


@lru_cache(maxsize=1)
def load_model() -> tf.keras.Model:
    """Load the TensorFlow model once per Python process."""
    if not MODEL_PATH.exists():
        raise PredictionError(f"Model file was not found at {MODEL_PATH}.")

    try:
        return tf.keras.models.load_model(MODEL_PATH, compile=False)
    except Exception as exc:  # pragma: no cover - TensorFlow emits many exception types.
        raise PredictionError("Unable to load the trained disease model.") from exc


@lru_cache(maxsize=1)
def load_class_names() -> list[str]:
    """Load class names from JSON once per Python process."""
    if not CLASS_NAMES_PATH.exists():
        raise PredictionError(f"Class names file was not found at {CLASS_NAMES_PATH}.")

    try:
        with CLASS_NAMES_PATH.open("r", encoding="utf-8") as file:
            raw_class_names = json.load(file)
    except json.JSONDecodeError as exc:
        raise PredictionError("class_names.json is not valid JSON.") from exc

    if isinstance(raw_class_names, dict):
        class_names = [raw_class_names[key] for key in sorted(raw_class_names, key=lambda item: int(item))]
    elif isinstance(raw_class_names, list):
        class_names = raw_class_names
    else:
        raise PredictionError("class_names.json must contain a list or an index-to-name dictionary.")

    if not class_names or not all(isinstance(name, str) and name.strip() for name in class_names):
        raise PredictionError("class_names.json does not contain valid class names.")

    return class_names


def format_class_name(class_name: str) -> str:
    """Convert PlantVillage-style class labels into readable names."""
    return class_name.replace("___", " - ").replace("_", " ").strip()


def _open_image(image_source: str | Path | bytes | BinaryIO | Image.Image) -> Image.Image:
    """Open and validate an image from a path, bytes, file-like object, or PIL image."""
    try:
        if isinstance(image_source, Image.Image):
            image = image_source.copy()
        else:
            image = Image.open(image_source)

        image.load()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise PredictionError("Please upload a valid JPG, JPEG, or PNG image.") from exc

    if image.format and image.format.upper() not in ALLOWED_FORMATS:
        raise PredictionError("Unsupported image format. Please use JPG, JPEG, or PNG.")

    return image.convert("RGB")


def preprocess_image(image_source: str | Path | bytes | BinaryIO | Image.Image) -> np.ndarray:
    """Resize an image into the 0-255 RGB batch expected by the saved model."""
    image = _open_image(image_source)
    image = image.resize(IMAGE_SIZE)
    image_array = tf.keras.utils.img_to_array(image)
    return np.expand_dims(image_array, axis=0)


def predict_disease(image_source: str | Path | bytes | BinaryIO | Image.Image, top_k: int = 3) -> dict[str, Any]:
    """Predict the disease class for a leaf image.

    Args:
        image_source: Path, bytes, uploaded file object, or PIL image.
        top_k: Number of highest-confidence predictions to return.

    Returns:
        A dictionary with the predicted disease, confidence percentage, and top predictions.
    """
    model = load_model()
    class_names = load_class_names()
    processed_image = preprocess_image(image_source)

    try:
        probabilities = model.predict(processed_image, verbose=0)[0]
    except Exception as exc:  # pragma: no cover - TensorFlow emits many exception types.
        raise PredictionError("The model could not make a prediction for this image.") from exc

    if len(probabilities) != len(class_names):
        raise PredictionError(
            "The model output size does not match class_names.json. Please verify the model artifacts."
        )

    top_k = max(1, min(top_k, len(class_names)))
    top_indices = np.argsort(probabilities)[::-1][:top_k]
    top_predictions = [
        {
            "class_name": class_names[index],
            "disease": format_class_name(class_names[index]),
            "confidence": round(float(probabilities[index]) * 100, 2),
        }
        for index in top_indices
    ]

    best_prediction = top_predictions[0]
    return {
        "class_name": best_prediction["class_name"],
        "disease": best_prediction["disease"],
        "confidence": best_prediction["confidence"],
        "top_predictions": top_predictions,
    }
