import tensorflow as tf
from pathlib import Path
from functools import lru_cache


BASE_DIR = Path(__file__).resolve().parent.parent

DISEASE_MODEL_PATH = (
    BASE_DIR / "model" / "leaf_disease_model.keras"
)

LEAF_MODEL_PATH = (
    BASE_DIR / "model" / "leaf_vs_non_leaf_model.keras"
)


class ModelLoadError(Exception):
    pass


@lru_cache(maxsize=1)
def load_disease_model():

    if not DISEASE_MODEL_PATH.exists():

        raise ModelLoadError(
            f"Disease model not found:\n{DISEASE_MODEL_PATH}"
        )

    try:

        model = tf.keras.models.load_model(
            DISEASE_MODEL_PATH,
            compile=False
        )

        return model

    except Exception as e:

        raise ModelLoadError(
            f"Unable to load disease model:\n{e}"
        )


@lru_cache(maxsize=1)
def load_leaf_model():

    if not LEAF_MODEL_PATH.exists():

        raise ModelLoadError(
            f"Leaf validation model not found:\n{LEAF_MODEL_PATH}"
        )

    try:

        model = tf.keras.models.load_model(
            LEAF_MODEL_PATH,
            compile=False
        )

        return model

    except Exception as e:

        raise ModelLoadError(
            f"Unable to load leaf model:\n{e}"
        )


def test_models():

    disease_model = load_disease_model()
    leaf_model = load_leaf_model()

    print("Disease Model Loaded Successfully")
    print("Leaf Validation Model Loaded Successfully")

    print(disease_model.summary())
    print(leaf_model.summary())