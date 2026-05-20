import base64
import io
import os
from collections import defaultdict

from flask import Flask, render_template, request
from PIL import Image, UnidentifiedImageError

from model_utility import CLASS_NAMES, predict_leaf_disease, split_class_name


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def build_support_catalog(class_names):
    catalog = defaultdict(list)

    for class_name in class_names:
        crop, disease = split_class_name(class_name)
        catalog[crop].append(disease)

    return [
        {
            "crop": crop,
            "diseases": sorted(diseases, key=lambda value: (value.lower() != "healthy", value.lower())),
            "class_count": len(diseases),
        }
        for crop, diseases in sorted(catalog.items(), key=lambda item: item[0].lower())
    ]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def image_to_data_uri(image):
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=88)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template(
        "index.html",
        class_count=len(CLASS_NAMES),
        error="The image file is too large. Please upload an image smaller than 8 MB.",
    ), 413


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    preview = None
    top_predictions = []

    if request.method == "POST":
        file = request.files.get("leaf_image")

        if not file or file.filename == "":
            error = "Please upload a clear photo of a plant leaf."
        elif not allowed_file(file.filename):
            error = "Upload a JPG, PNG, JPEG, or WEBP image."
        else:
            try:
                image = Image.open(file.stream).convert("RGB")
                result, top_predictions = predict_leaf_disease(image)
                preview = image_to_data_uri(image)
            except UnidentifiedImageError:
                error = "That file could not be read as an image."
            except Exception as exc:
                error = f"Prediction failed: {exc}"

    return render_template(
        "index.html",
        class_count=len(CLASS_NAMES),
        error=error,
        preview=preview,
        result=result,
        top_predictions=top_predictions,
    )


@app.route("/manual")
def manual():
    support_catalog = build_support_catalog(CLASS_NAMES)

    return render_template(
        "manual.html",
        class_count=len(CLASS_NAMES),
        crop_count=len(support_catalog),
        support_catalog=support_catalog,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG") == "1")
