from functools import lru_cache
import logging
import os
from pathlib import Path
import shutil

import numpy as np
from PIL import Image


IMG_SIZE = (256, 256)
MODEL_PATH = Path("models/plant_leaf_disease_detector")
CLASS_NAMES_PATH = MODEL_PATH.parent / f"{MODEL_PATH.name}.classes.txt"
PREPROCESSING_PATH = MODEL_PATH.parent / f"{MODEL_PATH.name}.preprocessing.txt"

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(os.getenv("PREDICTION_LOG_LEVEL", "INFO").upper())
LOGGER.propagate = False
if not LOGGER.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
    LOGGER.addHandler(handler)


def _load_text_lines(path):
    if not path.exists():
        return []

    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _load_model_preprocessing():
    return os.getenv(
        "MODEL_PREPROCESSING",
        PREPROCESSING_PATH.read_text(encoding="utf-8").strip() if PREPROCESSING_PATH.exists() else "rescale_1_255",
    ).lower()


DEFAULT_CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

CLASS_NAMES = _load_text_lines(CLASS_NAMES_PATH) or DEFAULT_CLASS_NAMES
MODEL_PREPROCESSING = _load_model_preprocessing()

if CLASS_NAMES != sorted(CLASS_NAMES):
    LOGGER.warning(
        "Class names are not in sorted Keras directory order. Verify %s matches the training generator.",
        CLASS_NAMES_PATH,
    )

TREATMENT_RECOMMENDATIONS = {
    "healthy": [
        "No disease detected. Continue regular field scouting every 5-7 days.",
        "Use balanced irrigation and avoid wetting leaves late in the evening.",
        "Keep the crop residue-free and follow locally recommended nutrition schedules.",
    ],
    "Apple_scab": [
        "Remove and destroy fallen infected leaves to reduce spores.",
        "Improve pruning and airflow in the canopy.",
        "Use a locally approved protective fungicide before wet weather.",
    ],
    "Black_rot": [
        "Prune infected twigs, mummified fruit, and cankers.",
        "Destroy crop residue away from the field.",
        "Apply a recommended fungicide early in the season if the disease is spreading.",
    ],
    "Cedar_apple_rust": [
        "Remove nearby alternate juniper hosts where practical.",
        "Prune infected leaves and improve orchard ventilation.",
        "Use a preventive fungicide during early leaf emergence in high-risk areas.",
    ],
    "Powdery_mildew": [
        "Remove heavily infected leaves and avoid dense planting.",
        "Improve sunlight and airflow around plants.",
        "Use sulphur or another locally approved fungicide when symptoms start.",
    ],
    "Cercospora_leaf_spot Gray_leaf_spot": [
        "Rotate maize with non-host crops and remove infected residue.",
        "Avoid overhead irrigation when possible.",
        "Use a recommended foliar fungicide if lesions spread before grain filling.",
    ],
    "Common_rust_": [
        "Plant resistant maize hybrids in future seasons.",
        "Monitor lower leaves and remove severely infected plants in small plots.",
        "Apply fungicide only when infection appears early and weather remains humid.",
    ],
    "Northern_Leaf_Blight": [
        "Use resistant maize varieties and rotate with legumes or other non-host crops.",
        "Bury or remove infected residue after harvest.",
        "Consider fungicide if long cigar-shaped lesions appear before tasseling.",
    ],
    "Esca_(Black_Measles)": [
        "Prune infected grapevine wood during dry weather.",
        "Disinfect pruning tools between vines.",
        "Avoid water stress and remove severely affected vines where recovery is unlikely.",
    ],
    "Leaf_blight_(Isariopsis_Leaf_Spot)": [
        "Remove infected grape leaves and old vineyard debris.",
        "Improve airflow with balanced pruning and spacing.",
        "Use locally recommended protective fungicides during humid periods.",
    ],
    "Haunglongbing_(Citrus_greening)": [
        "Remove and destroy confirmed infected citrus trees.",
        "Control psyllid vectors with recommended integrated pest management.",
        "Use disease-free nursery plants for replanting.",
    ],
    "Bacterial_spot": [
        "Avoid overhead irrigation and handling plants when leaves are wet.",
        "Remove infected leaves and crop debris.",
        "Use certified seed or seedlings and copper-based sprays only as locally advised.",
    ],
    "Early_blight": [
        "Remove lower infected leaves and stake plants to reduce soil splash.",
        "Rotate with non-solanaceous crops for 2-3 seasons.",
        "Use a recommended fungicide if spots spread during warm, humid weather.",
    ],
    "Late_blight": [
        "Remove infected plants quickly and do not compost diseased material.",
        "Avoid wet foliage by using drip irrigation where possible.",
        "Apply locally approved late-blight fungicide immediately during cool, wet outbreaks.",
    ],
    "Leaf_scorch": [
        "Remove infected strawberry leaves after harvest.",
        "Improve spacing and avoid excess nitrogen.",
        "Use disease-free planting material and recommended fungicide in severe cases.",
    ],
    "Leaf_Mold": [
        "Ventilate protected cultivation and reduce humidity.",
        "Remove infected tomato leaves carefully.",
        "Use resistant varieties and approved fungicides where disease pressure is high.",
    ],
    "Septoria_leaf_spot": [
        "Remove lower infected tomato leaves and mulch to prevent soil splash.",
        "Rotate crops and destroy crop residue after harvest.",
        "Apply a recommended fungicide early if small circular spots spread quickly.",
    ],
    "Spider_mites Two-spotted_spider_mite": [
        "Spray leaves with water to reduce dust and mite buildup.",
        "Release or conserve natural enemies where available.",
        "Use a recommended miticide only when mite numbers cross local thresholds.",
    ],
    "Target_Spot": [
        "Remove infected tomato foliage and improve spacing.",
        "Avoid prolonged leaf wetness.",
        "Use crop rotation and locally recommended fungicides during humid weather.",
    ],
    "Tomato_mosaic_virus": [
        "Remove infected plants and disinfect hands, stakes, and tools.",
        "Do not use seed from infected plants.",
        "Control weeds and avoid tobacco handling before working in tomato plots.",
    ],
    "Tomato_Yellow_Leaf_Curl_Virus": [
        "Remove infected tomato plants early to reduce spread.",
        "Control whiteflies with yellow sticky traps, netting, and approved sprays.",
        "Use tolerant tomato varieties and virus-free seedlings.",
    ],
}


def plot_images(gen, nrows=2, ncols=4, figsize=(16, 8)):
    import matplotlib.pyplot as plt
    plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    class_name_lookup = {index: name for name, index in gen.class_indices.items()}
    data = gen[0]

    for i in range(nrows * ncols):
        plt.subplot(nrows, ncols, i + 1)
        plt.axis(False)
        plt.grid(False)
        plt.imshow(data[0][i])
        plt.title(class_name_lookup[data[1][i].argmax()])
    plt.show()


def split_class_name(class_name):
    crop, disease = class_name.split("___", maxsplit=1)
    return crop.replace("_", " "), disease.replace("_", " ")


def get_recommendations(class_name):
    _, disease = split_class_name(class_name)
    if disease.lower() == "healthy":
        return TREATMENT_RECOMMENDATIONS["healthy"]

    key = next((item for item in TREATMENT_RECOMMENDATIONS if item in class_name), None)
    return TREATMENT_RECOMMENDATIONS.get(
        key,
        [
            "Isolate visibly infected plants or leaves where practical.",
            "Avoid overhead irrigation and remove infected crop residue.",
            "Consult the nearest Krishi Vigyan Kendra or agriculture officer before spraying.",
        ],
    )


@lru_cache(maxsize=1)
def load_trained_model(model_path=MODEL_PATH):
    import tensorflow as tf

    tf.get_logger().setLevel("ERROR")
    model_path = Path(model_path)

    if model_path.is_dir():
        return _load_saved_model_for_inference(tf, model_path)

    return tf.keras.models.load_model(model_path, compile=False)


def _load_saved_model_for_inference(tf, model_path):
    if _saved_model_has_optimizer_slots(model_path):
        return _wrap_saved_model(tf, _repair_saved_model_optimizer_slots(model_path))

    try:
        return _wrap_saved_model(tf, model_path)
    except AttributeError as exc:
        if "add_slot" not in str(exc):
            raise

        repaired_path = _repair_saved_model_optimizer_slots(model_path)
        return _wrap_saved_model(tf, repaired_path)


def _wrap_saved_model(tf, model_path):
    LOGGER.info("Loading TensorFlow SavedModel from %s", model_path)
    inputs = tf.keras.Input(shape=IMG_SIZE + (3,), name="Input")
    outputs = tf.keras.layers.TFSMLayer(
        str(model_path),
        call_endpoint="serving_default",
    )(inputs)

    if isinstance(outputs, dict):
        outputs = outputs["Output"] if "Output" in outputs else next(iter(outputs.values()))

    return tf.keras.Model(inputs=inputs, outputs=outputs)


def _saved_model_has_optimizer_slots(model_path):
    from tensorflow.core.protobuf import saved_model_pb2

    saved_model_pb = model_path / "saved_model.pb"
    if not saved_model_pb.exists():
        return False

    saved_model = saved_model_pb2.SavedModel()
    saved_model.ParseFromString(saved_model_pb.read_bytes())

    return any(
        node.slot_variables
        for meta_graph in saved_model.meta_graphs
        for node in meta_graph.object_graph_def.nodes
    )


def _repair_saved_model_optimizer_slots(model_path):
    from tensorflow.core.protobuf import saved_model_pb2

    repaired_path = model_path.with_name(f"{model_path.name}_tf_compat")
    source_pb = model_path / "saved_model.pb"
    repaired_pb = repaired_path / "saved_model.pb"

    if repaired_pb.exists() and repaired_pb.stat().st_mtime >= source_pb.stat().st_mtime:
        return repaired_path

    if repaired_path.exists():
        shutil.rmtree(repaired_path)
    shutil.copytree(model_path, repaired_path)

    saved_model = saved_model_pb2.SavedModel()
    saved_model.ParseFromString(repaired_pb.read_bytes())

    for meta_graph in saved_model.meta_graphs:
        for node in meta_graph.object_graph_def.nodes:
            node.slot_variables.clear()

    repaired_pb.write_bytes(saved_model.SerializeToString())
    return repaired_path


def preprocess_image(image, image_size=IMG_SIZE, preprocessing=MODEL_PREPROCESSING):
    import tensorflow as tf

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    original_mode = image.mode
    original_size = image.size
    image = image.convert("RGB").resize(image_size)
    array = np.asarray(image, dtype=np.float32)

    if preprocessing == "mobilenet_v2":
        array = tf.keras.applications.mobilenet_v2.preprocess_input(array)
        preprocessing_steps = "convert RGB -> resize 256x256 -> MobileNetV2 preprocess_input [-1, 1]"
    elif preprocessing == "rescale_1_255":
        array = array / 255.0
        preprocessing_steps = "convert RGB -> resize 256x256 -> rescale pixels to [0, 1]"
    else:
        raise ValueError(
            f"Unsupported MODEL_PREPROCESSING={preprocessing!r}. "
            "Use 'rescale_1_255' or 'mobilenet_v2'."
        )

    batch = np.expand_dims(array, axis=0)
    LOGGER.info(
        "Image preprocessing: original_size=%s original_mode=%s resized_shape=%s batch_shape=%s steps=%s value_range=(%.4f, %.4f)",
        original_size,
        original_mode,
        array.shape,
        batch.shape,
        preprocessing_steps,
        float(array.min()),
        float(array.max()),
    )
    return batch


def _probabilities_from_model_output(predictions):
    import tensorflow as tf

    predictions = np.asarray(predictions, dtype=np.float32)
    probability_sum = float(np.sum(predictions))
    has_probability_range = np.all(predictions >= 0.0) and np.all(predictions <= 1.0)

    if has_probability_range and np.isclose(probability_sum, 1.0, rtol=1e-3, atol=1e-3):
        LOGGER.info("Model output already appears to be softmax probabilities; sum=%.6f", probability_sum)
        return predictions

    probabilities = tf.nn.softmax(predictions).numpy()
    LOGGER.info(
        "Model output looked like logits; applied softmax. raw_sum=%.6f probability_sum=%.6f",
        probability_sum,
        float(np.sum(probabilities)),
    )
    return probabilities


def _log_prediction_debug(probabilities, predicted_index):
    LOGGER.info("Predicted class index: %d", predicted_index)
    LOGGER.info("Class name mapping: %d -> %s", predicted_index, CLASS_NAMES[predicted_index])
    LOGGER.info("Full probability vector: %s", np.array2string(probabilities, precision=6, suppress_small=False))

    for index, probability in enumerate(probabilities):
        LOGGER.info("Probability[%02d] %-55s %.8f", index, CLASS_NAMES[index], float(probability))


def predict_leaf_disease(image, model=None, top_k=3):
    model = model or load_trained_model()
    raw_predictions = model.predict(preprocess_image(image), verbose=0)[0]
    probabilities = _probabilities_from_model_output(raw_predictions)
    predicted_index = int(np.argmax(probabilities))
    _log_prediction_debug(probabilities, predicted_index)

    top_indices = probabilities.argsort()[-top_k:][::-1]
    top_predictions = [
        {
            "class_name": CLASS_NAMES[index],
            "confidence": float(probabilities[index]),
            "crop": split_class_name(CLASS_NAMES[index])[0],
            "disease": split_class_name(CLASS_NAMES[index])[1],
        }
        for index in top_indices
    ]

    best = top_predictions[0]
    best["recommendations"] = get_recommendations(best["class_name"])
    return best, top_predictions
