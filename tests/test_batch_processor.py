"""End-to-end tests for batch processing and persisted job statuses."""
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from db import database
from app.batch_processor import process_batch_file


class UploadedBytes(io.BytesIO):
    def __init__(self, data, name, content_type="image/png"):
        super().__init__(data)
        self.name = name
        self.type = content_type


class TestBatchProcessor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path_patcher = patch.object(database, "DB_PATH", Path(self.temp_dir.name) / "batch.db")
        self.path_patcher.start()
        database.initialize_database()

    def tearDown(self):
        self.path_patcher.stop()
        self.temp_dir.cleanup()

    def test_valid_image_is_processed_and_saved_as_success(self):
        buffer = io.BytesIO()
        Image.new("RGB", (2, 2), (25, 80, 200)).save(buffer, format="PNG")
        result = process_batch_file(UploadedBytes(buffer.getvalue(), "valid.png"))
        self.assertEqual(result["status"], "success")
        self.assertIsNotNone(result["mae"])
        self.assertEqual(database.get_recent_history()[0][5], "success")

    def test_corrupt_image_is_saved_as_failed(self):
        result = process_batch_file(UploadedBytes(b"not an image", "broken.png"))
        self.assertEqual(result["status"], "failed")
        history = database.get_recent_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][1], "broken.png")
        self.assertEqual(history[0][5], "failed")


if __name__ == "__main__":
    unittest.main()
