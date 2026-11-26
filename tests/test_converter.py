import unittest
import numpy as np
from PIL import Image

from math_engine.matrix import (
    matrix_multiply, determinant, matrix_inverse, matrix_rank
)
from math_engine.converter import (
    RGB_TO_YIQ, rgb_pixel_to_yiq, yiq_pixel_to_rgb,
    convert_image_to_yiq, convert_yiq_array_to_rgb,
    convert_image_to_grayscale, image_difference, GRAYSCALE_MATRIX
)
from ds.batch_queue import BatchQueue


class TestMatrixAlgorithms(unittest.TestCase):
    def test_matrix_multiply_normal(self):
        self.assertEqual(matrix_multiply([[1, 2], [3, 4]], [[5], [6]]),
                         [[17.0], [39.0]])

    def test_matrix_multiply_dimension_error(self):
        with self.assertRaises(ValueError):
            matrix_multiply([[1, 2]], [[1, 2]])

    def test_matrix_multiply_matches_numpy(self):
        a = [[1, 2, 3], [4, 5, 6]]
        b = [[7, 8], [9, 10], [11, 12]]
        actual = np.array(matrix_multiply(a, b))
        expected = np.array(a) @ np.array(b)
        np.testing.assert_allclose(actual, expected)

    def test_determinant_normal(self):
        self.assertAlmostEqual(determinant([[1, 2], [3, 4]]), -2.0)

    def test_determinant_singular_edge(self):
        self.assertAlmostEqual(determinant([[1, 2], [2, 4]]), 0.0)

    def test_determinant_matches_numpy(self):
        matrix = [[2, 1, 3], [0, 4, 5], [1, 0, 6]]
        self.assertAlmostEqual(determinant(matrix), float(np.linalg.det(matrix)), places=8)

    def test_inverse_normal(self):
        a = [[4, 7], [2, 6]]
        inv = matrix_inverse(a)
        product = matrix_multiply(a, inv)
        np.testing.assert_allclose(product, np.eye(2), atol=1e-9)

    def test_inverse_singular_edge(self):
        with self.assertRaises(ValueError):
            matrix_inverse([[1, 2], [2, 4]])

    def test_inverse_matches_numpy(self):
        a = [[3, 0, 2], [2, 0, -2], [0, 1, 1]]
        np.testing.assert_allclose(matrix_inverse(a), np.linalg.inv(a), atol=1e-9)

    def test_rank_normal(self):
        self.assertEqual(matrix_rank([[1, 2], [2, 4]]), 1)

    def test_rank_zero_edge(self):
        self.assertEqual(matrix_rank([[0, 0], [0, 0]]), 0)

    def test_rank_matches_numpy(self):
        a = [[1, 2, 3], [2, 4, 6], [1, 1, 1]]
        self.assertEqual(matrix_rank(a), int(np.linalg.matrix_rank(a)))


class TestColourConversion(unittest.TestCase):
    def test_known_pixel(self):
        yiq = rgb_pixel_to_yiq((255, 120, 60))
        np.testing.assert_allclose(yiq, [153.525, 99.78, 9.765], atol=1e-9)

    def test_pixel_round_trip_edge_black(self):
        rgb = yiq_pixel_to_rgb(rgb_pixel_to_yiq((0, 0, 0)))
        np.testing.assert_allclose(rgb, [0, 0, 0], atol=1e-8)

    def test_rgb_yiq_matrix_matches_numpy(self):
        pixel = np.array([[25.0], [80.0], [200.0]])
        expected = np.array(RGB_TO_YIQ) @ pixel
        actual = np.array(rgb_pixel_to_yiq((25, 80, 200))).reshape(3, 1)
        np.testing.assert_allclose(actual, expected, atol=1e-9)

    def test_image_round_trip(self):
        image = Image.new("RGB", (2, 2))
        image.putdata([(255, 0, 0), (0, 255, 0), (0, 0, 255), (20, 40, 60)])
        yiq, original = convert_image_to_yiq(image)
        restored = convert_yiq_array_to_rgb(yiq)
        mae, rmse, _ = image_difference(original, restored)
        self.assertLessEqual(mae, 1.0)
        self.assertLessEqual(rmse, 1.0)

    def test_grayscale_shape_and_rank(self):
        image = Image.new("RGB", (2, 2), (100, 50, 25))
        gray = convert_image_to_grayscale(image)
        self.assertEqual(gray.mode, "L")
        self.assertEqual(matrix_rank(GRAYSCALE_MATRIX), 1)


class TestQueue(unittest.TestCase):
    def test_fifo_order(self):
        q = BatchQueue()
        q.enqueue("first")
        q.enqueue("second")
        self.assertEqual(q.dequeue(), "first")
        self.assertEqual(q.dequeue(), "second")

    def test_empty_queue(self):
        q = BatchQueue()
        self.assertTrue(q.is_empty())
        with self.assertRaises(IndexError):
            q.dequeue()


if __name__ == "__main__":
    unittest.main()
