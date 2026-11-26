"""RGB/YIQ image conversion routines."""

from PIL import Image
from .matrix import matrix_multiply, matrix_inverse, determinant, matrix_rank

RGB_TO_YIQ = [
    [0.299, 0.587, 0.114],
    [0.596, -0.274, -0.322],
    [0.211, -0.523, 0.312],
]

YIQ_TO_RGB = matrix_inverse(RGB_TO_YIQ)

GRAYSCALE_MATRIX = [[0.299, 0.587, 0.114]]

# The columns of YIQ_BASIS_IN_RGB are the Y, I and Q basis vectors
# expressed in the standard RGB coordinate system.  If x_RGB is a colour
# vector in standard coordinates and c_YIQ its coordinates in the YIQ basis,
# then x_RGB = B_YIQ c_YIQ and c_YIQ = B_YIQ^{-1} x_RGB.
YIQ_BASIS_IN_RGB = YIQ_TO_RGB


def rgb_pixel_to_yiq(pixel):
    """Convert one (R,G,B) pixel to floating-point (Y,I,Q)."""
    if len(pixel) != 3:
        raise ValueError("An RGB pixel must contain exactly three values.")
    vector = [[float(pixel[0])], [float(pixel[1])], [float(pixel[2])]]
    converted = matrix_multiply(RGB_TO_YIQ, vector)
    return tuple(converted[i][0] for i in range(3))


def yiq_pixel_to_rgb(pixel):
    """Convert one (Y,I,Q) pixel back to RGB floating-point values."""
    if len(pixel) != 3:
        raise ValueError("A YIQ pixel must contain exactly three values.")
    vector = [[float(pixel[0])], [float(pixel[1])], [float(pixel[2])]]
    converted = matrix_multiply(YIQ_TO_RGB, vector)
    return tuple(converted[i][0] for i in range(3))


def _as_rgb_image(image):
    if not isinstance(image, Image.Image):
        raise TypeError("Expected a PIL Image.")
    return image.convert("RGB")


def convert_image_to_yiq(image):
    """Convert every pixel. Returns (YIQ float array, original RGB image)."""
    import numpy as np
    rgb_image = _as_rgb_image(image)
    pixels = np.asarray(rgb_image, dtype=np.float64)
    height, width, _ = pixels.shape
    yiq = np.empty((height, width, 3), dtype=np.float64)
    # Apply the from-scratch 3×3 matrix multiplication to every pixel.
    for row in range(height):
        for col in range(width):
            yiq[row, col] = rgb_pixel_to_yiq(pixels[row, col])
    return yiq, rgb_image


def convert_yiq_array_to_rgb(yiq):
    """Convert a YIQ array back to an RGB PIL image, clipping display values."""
    import numpy as np
    array = np.asarray(yiq, dtype=np.float64)
    if array.ndim != 3 or array.shape[2] != 3:
        raise ValueError("YIQ data must have shape (height, width, 3).")
    height, width, _ = array.shape
    rgb = np.empty((height, width, 3), dtype=np.float64)
    for row in range(height):
        for col in range(width):
            rgb[row, col] = yiq_pixel_to_rgb(array[row, col])
    rgb = np.clip(np.rint(rgb), 0, 255).astype("uint8")
    return Image.fromarray(rgb, mode="RGB")


def channel_preview(channel, channel_name):
    """Create a grayscale preview of a Y, I or Q channel."""
    import numpy as np
    values = np.asarray(channel, dtype=np.float64)
    if channel_name.upper() == "Y":
        display = np.clip(values, 0, 255)
    else:
        low, high = float(values.min()), float(values.max())
        if abs(high - low) < 1e-12:
            display = np.full(values.shape, 127.5)
        else:
            display = (values - low) * (255.0 / (high - low))
    return Image.fromarray(np.rint(display).astype("uint8"), mode="L")


def convert_image_to_grayscale(image):
    """Map RGB to one luminance channel; colour information is discarded."""
    import numpy as np
    rgb = np.asarray(_as_rgb_image(image), dtype=np.float64)
    gray = (rgb[:, :, 0] * 0.299 +
            rgb[:, :, 1] * 0.587 +
            rgb[:, :, 2] * 0.114)
    return Image.fromarray(np.clip(np.rint(gray), 0, 255).astype("uint8"), mode="L")


def image_difference(original, restored):
    """Return MAE, RMSE and a difference heatmap image."""
    import numpy as np
    a = np.asarray(_as_rgb_image(original), dtype=np.float64)
    b = np.asarray(_as_rgb_image(restored), dtype=np.float64)
    if a.shape != b.shape:
        raise ValueError("Images must have the same dimensions.")
    diff = np.abs(a - b)
    mae = float(diff.mean())
    rmse = float(np.sqrt(np.mean((a - b) ** 2)))
    heat = np.clip(diff.mean(axis=2) * 4.0, 0, 255).astype("uint8")
    return mae, rmse, Image.fromarray(heat, mode="L")


def change_of_basis_demo(rgb=(255.0, 120.0, 60.0)):
    """Return a concrete RGB <-> YIQ change-of-basis demonstration.

    RGB_TO_YIQ converts standard RGB coordinates into YIQ coordinates.
    YIQ_BASIS_IN_RGB contains the new basis vectors expressed in RGB
    coordinates, so RGB = YIQ_BASIS_IN_RGB @ YIQ.
    """
    if len(rgb) != 3:
        raise ValueError("An RGB colour must contain exactly three values.")
    rgb_column = [[float(value)] for value in rgb]
    yiq_column = matrix_multiply(RGB_TO_YIQ, rgb_column)
    reconstructed_rgb = matrix_multiply(YIQ_BASIS_IN_RGB, yiq_column)
    return {
        "rgb": tuple(float(value) for value in rgb),
        "yiq": tuple(row[0] for row in yiq_column),
        "yiq_basis_in_rgb": YIQ_BASIS_IN_RGB,
        "reconstructed_rgb": tuple(row[0] for row in reconstructed_rgb),
    }


def mathematical_summary():
    return {
        "yiq_basis_in_rgb": YIQ_BASIS_IN_RGB,
        "determinant": determinant(RGB_TO_YIQ),
        "rank_rgb_to_yiq": matrix_rank(RGB_TO_YIQ),
        "rank_grayscale": matrix_rank(GRAYSCALE_MATRIX),
        "inverse": YIQ_TO_RGB,
    }
