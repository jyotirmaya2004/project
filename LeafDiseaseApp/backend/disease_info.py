import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DISEASE_INFO_PATH = (
    BASE_DIR / "disease_info.json"
)


class DiseaseInfoError(Exception):
    pass


def load_disease_info():

    try:

        with open(
            DISEASE_INFO_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except Exception as e:

        raise DiseaseInfoError(
            f"Unable to load disease info: {e}"
        )


def get_disease_details(class_name):

    disease_data = load_disease_info()

    if class_name in disease_data:

        return disease_data[class_name]

    return {
        "disease_name": class_name,
        "symptoms": "Not available",
        "causes": "Not available",
        "treatment": "Not available",
        "prevention": "Not available"
    }


def get_symptoms(class_name):

    return get_disease_details(
        class_name
    )["symptoms"]


def get_causes(class_name):

    return get_disease_details(
        class_name
    )["causes"]


def get_treatment(class_name):

    return get_disease_details(
        class_name
    )["treatment"]


def get_prevention(class_name):

    return get_disease_details(
        class_name
    )["prevention"]