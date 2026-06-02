from PIL import Image
import numpy as np


IMAGE_SIZE = (224, 224)


class ImageProcessingError(Exception):
    pass


def load_image(image_file):
    """
    Load image from uploaded file.
    """

    try:
        if hasattr(image_file, "seek"):
            image_file.seek(0)

        image = Image.open(image_file)

        if image.mode != "RGB":
            image = image.convert("RGB")

        return image

    except Exception as e:
        raise ImageProcessingError(
            f"Unable to load image: {e}"
        )


def resize_image(image):

    try:
        return image.resize(IMAGE_SIZE)

    except Exception as e:
        raise ImageProcessingError(
            f"Unable to resize image: {e}"
        )


def image_to_array(image):

    try:

        img_array = np.array(image)

        img_array = img_array.astype("float32")

        img_array = img_array / 255.0

        img_array = np.expand_dims(
            img_array,
            axis=0
        )

        return img_array

    except Exception as e:

        raise ImageProcessingError(
            f"Unable to convert image: {e}"
        )


def preprocess_image(image_file):
    """
    Complete preprocessing pipeline.
    """

    image = load_image(image_file)

    image = resize_image(image)

    image_array = image_to_array(image)

    return image, image_array
