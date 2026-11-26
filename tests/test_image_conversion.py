"""Normal, edge and independent-library checks for image conversions."""
import unittest
import numpy as np
from PIL import Image

from math_engine.converter import (
    RGB_TO_YIQ,
    change_of_basis_demo,
    convert_image_to_yiq,
    convert_yiq_array_to_rgb,
    convert_image_to_grayscale,
    image_difference,
    rgb_pixel_to_yiq,
    yiq_pixel_to_rgb,
)


class TestImageConversionValidation(unittest.TestCase):
    def test_rgb_to_yiq_image_normal(self):
        image = Image.new("RGB", (2, 1))
        image.putdata([(255, 120, 60), (10, 20, 30)])
        yiq, original = convert_image_to_yiq(image)
        self.assertEqual(yiq.shape, (1, 2, 3))
        self.assertEqual(original.size, (2, 1))
        np.testing.assert_allclose(yiq[0, 0], [153.525, 99.78, 9.765], atol=1e-9)

    def test_rgb_to_yiq_image_edge_single_pixel_black_and_white(self):
        for colour in [(0, 0, 0), (255, 255, 255)]:
            image = Image.new("RGB", (1, 1), colour)
            yiq, _ = convert_image_to_yiq(image)
            self.assertEqual(yiq.shape, (1, 1, 3))
            np.testing.assert_allclose(yiq[0, 0], np.array(RGB_TO_YIQ) @ np.array(colour), atol=1e-9)

    def test_rgb_to_yiq_image_matches_numpy_library(self):
        pixels = np.array([[[12, 34, 56], [200, 150, 90]], [[0, 255, 128], [255, 0, 255]]], dtype=np.uint8)
        yiq, _ = convert_image_to_yiq(Image.fromarray(pixels, mode="RGB"))
        expected = pixels.astype(np.float64) @ np.asarray(RGB_TO_YIQ, dtype=np.float64).T
        np.testing.assert_allclose(yiq, expected, atol=1e-9)

    def test_inverse_image_normal_round_trip(self):
        pixels = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [20, 40, 60]]], dtype=np.uint8)
        yiq, original = convert_image_to_yiq(Image.fromarray(pixels, mode="RGB"))
        restored = convert_yiq_array_to_rgb(yiq)
        mae, rmse, _ = image_difference(original, restored)
        self.assertLessEqual(mae, 1.0)
        self.assertLessEqual(rmse, 1.0)

    def test_inverse_image_edge_rejects_wrong_shape(self):
        with self.assertRaises(ValueError):
            convert_yiq_array_to_rgb(np.zeros((2, 2)))

    def test_inverse_image_matches_independent_numpy_calculation(self):
        pixels = np.array([[[40, 80, 120], [255, 200, 10]]], dtype=np.uint8)
        yiq, _ = convert_image_to_yiq(Image.fromarray(pixels, mode="RGB"))
        restored = np.asarray(convert_yiq_array_to_rgb(yiq), dtype=np.int16)
        np.testing.assert_allclose(restored, pixels.astype(np.int16), atol=1)

    def test_grayscale_normal(self):
        image = Image.new("RGB", (1, 1), (255, 0, 0))
        gray = convert_image_to_grayscale(image)
        self.assertEqual(gray.mode, "L")
        self.assertEqual(gray.getpixel((0, 0)), 76)

    def test_grayscale_edge_black_and_white(self):
        self.assertEqual(convert_image_to_grayscale(Image.new("RGB", (1, 1), (0, 0, 0))).getpixel((0, 0)), 0)
        self.assertEqual(convert_image_to_grayscale(Image.new("RGB", (1, 1), (255, 255, 255))).getpixel((0, 0)), 255)

    def test_grayscale_matches_numpy_reference(self):
        pixels = np.array([[[10, 20, 30], [200, 100, 50]]], dtype=np.uint8)
        gray = np.asarray(convert_image_to_grayscale(Image.fromarray(pixels, mode="RGB")))
        expected = np.rint(pixels[:, :, 0] * .299 + pixels[:, :, 1] * .587 + pixels[:, :, 2] * .114).astype(np.uint8)
        np.testing.assert_array_equal(gray, expected)

    def test_image_difference_edge_identical_images(self):
        image = Image.new("RGB", (1, 1), (5, 10, 15))
        mae, rmse, heat = image_difference(image, image.copy())
        self.assertEqual((mae, rmse), (0.0, 0.0))
        self.assertEqual(heat.getpixel((0, 0)), 0)

    def test_image_difference_rejects_mismatched_dimensions(self):
        with self.assertRaises(ValueError):
            image_difference(Image.new("RGB", (1, 1)), Image.new("RGB", (2, 1)))

    def test_change_of_basis_round_trip(self):
        demo = change_of_basis_demo((255, 120, 60))
        np.testing.assert_allclose(demo["yiq"], [153.525, 99.78, 9.765], atol=1e-9)
        np.testing.assert_allclose(demo["reconstructed_rgb"], [255, 120, 60], atol=1e-8)


    def test_yiq_to_rgb_pixel_normal(self):
        rgb = yiq_pixel_to_rgb(rgb_pixel_to_yiq((25, 80, 200)))
        np.testing.assert_allclose(rgb, [25, 80, 200], atol=1e-8)

    def test_yiq_to_rgb_pixel_edge_white(self):
        rgb = yiq_pixel_to_rgb(rgb_pixel_to_yiq((255, 255, 255)))
        np.testing.assert_allclose(rgb, [255, 255, 255], atol=1e-8)

    def test_yiq_to_rgb_pixel_matches_numpy(self):
        source = (25, 80, 200)
        yiq = np.asarray(rgb_pixel_to_yiq(source))
        expected = np.linalg.inv(np.asarray(RGB_TO_YIQ)) @ yiq
        actual = np.asarray(yiq_pixel_to_rgb(yiq))
        np.testing.assert_allclose(actual, expected, atol=1e-9)

    def test_image_difference_matches_numpy_reference(self):
        a = np.array([[[0, 10, 20], [30, 40, 50]]], dtype=np.uint8)
        b = np.array([[[1, 12, 23], [35, 40, 45]]], dtype=np.uint8)
        mae, rmse, _ = image_difference(Image.fromarray(a, "RGB"), Image.fromarray(b, "RGB"))
        delta = a.astype(np.float64) - b.astype(np.float64)
        self.assertAlmostEqual(mae, float(np.abs(delta).mean()))
        self.assertAlmostEqual(rmse, float(np.sqrt(np.mean(delta ** 2))))

    def test_change_of_basis_matches_numpy_reference(self):
        rgb = np.array([255.0, 120.0, 60.0])
        demo = change_of_basis_demo(tuple(rgb))
        expected_yiq = np.asarray(RGB_TO_YIQ) @ rgb
        expected_rgb = np.linalg.inv(np.asarray(RGB_TO_YIQ)) @ expected_yiq
        np.testing.assert_allclose(demo["yiq"], expected_yiq, atol=1e-9)
        np.testing.assert_allclose(demo["reconstructed_rgb"], expected_rgb, atol=1e-8)

    def test_change_of_basis_rejects_invalid_vector(self):
        with self.assertRaises(ValueError):
            change_of_basis_demo((10, 20))


if __name__ == "__main__":
    unittest.main()
