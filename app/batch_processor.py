"""Testable batch-job execution and database status persistence."""
from PIL import Image

from db.database import (
    save_image_record,
    update_image_dimensions,
    save_colour_space_record,
    save_conversion_record,
)
from math_engine.converter import (
    convert_image_to_yiq,
    convert_yiq_array_to_rgb,
    image_difference,
)


def process_batch_file(uploaded_file):
    """Process one uploaded image and persist success or failure in SQLite."""
    image_id = save_image_record(
        uploaded_file.name, None, None, getattr(uploaded_file, "type", "Unknown")
    )
    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        image = Image.open(uploaded_file).convert("RGB")
        image.thumbnail((400, 400))
        update_image_dimensions(image_id, image.width, image.height)
        yiq, original = convert_image_to_yiq(image)
        restored = convert_yiq_array_to_rgb(yiq)
        mae, rmse, _ = image_difference(original, restored)
        save_colour_space_record(image_id)
        save_conversion_record(
            image_id, "Batch RGB to YIQ to RGB", mae, rmse, status="success"
        )
        return {"status": "success", "mae": mae, "rmse": rmse, "error": None}
    except Exception as error:
        save_conversion_record(
            image_id, "Batch RGB to YIQ to RGB", status="failed"
        )
        return {"status": "failed", "mae": None, "rmse": None, "error": str(error)}
