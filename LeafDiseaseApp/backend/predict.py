import json
import numpy as np
from pathlib import Path

from backend.image_utils import preprocess_image
from backend.model_loader import (
    load_disease_model,
    load_leaf_model,
)


BASE_DIR = Path(__file__).resolve().parent.parent

CLASS_NAMES_PATH = (
    BASE_DIR / "model" / "class_names.json"
)


class PredictionError(Exception):
    pass


def load_class_names():
    try:
        with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
            class_names = json.load(file)
        return class_names
    except Exception as e:
        raise PredictionError(f"Unable to load class names: {e}")


def format_disease_name(name):
    return name.replace("___", " - ").replace("_", " ")


def validate_leaf(image_array):
    """Binary leaf validation.

    IMPORTANT: this assumes the leaf model output is a single sigmoid score where
    the value corresponds to NON-leaf probability (so leaf_probability = 1 - p).
    """
    leaf_model = load_leaf_model()

    prediction = leaf_model.predict(image_array, verbose=0)[0][0]

    leaf_confidence = (1 - prediction) * 100

    return {
        "is_leaf": leaf_confidence >= 50,
        "leaf_confidence": round(leaf_confidence, 2),
    }


def predict_disease(image_file):
    """Legacy predictor (kept for backward compatibility).

    New UI uses `backend.predict_two_stage.predict_two_stage`.
    """
    image, image_array = preprocess_image(image_file)

    leaf_result = validate_leaf(image_array)

    if not leaf_result["is_leaf"]:
        raise PredictionError("This image does not appear to be a leaf.")

    model = load_disease_model()
    class_names = load_class_names()

    predictions = model.predict(image_array, verbose=0)[0]
    predicted_index = np.argmax(predictions)

    confidence = predictions[predicted_index] * 100

    disease_name = format_disease_name(class_names[predicted_index])

    top_indices = np.argsort(predictions)[::-1][:3]

    top_predictions = []
    for idx in top_indices:
        top_predictions.append(
            {
                "class_name": class_names[idx],
                "disease": format_disease_name(class_names[idx]),
                "confidence": round(predictions[idx] * 100, 2),
            }
        )

    return {
        "disease": disease_name,
        "class_name": class_names[predicted_index],
        "confidence": round(confidence, 2),
        "leaf_validation": leaf_result,
        "top_predictions": top_predictions,
    }

