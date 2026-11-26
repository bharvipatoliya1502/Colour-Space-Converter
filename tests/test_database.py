"""Database persistence tests, including failed batch job recording."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from db import database


class TestDatabasePersistence(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_project.db"
        self.path_patcher = patch.object(database, "DB_PATH", self.db_path)
        self.path_patcher.start()
        database.initialize_database()

    def tearDown(self):
        self.path_patcher.stop()
        self.temp_dir.cleanup()

    def test_successful_conversion_is_readable_from_database(self):
        image_id = database.save_image_record("sample.png", 2, 3, "PNG")
        database.save_colour_space_record(image_id)
        database.save_conversion_record(image_id, "RGB to YIQ", 0.0, 0.0, "success")
        history = database.get_recent_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][5], "success")
        self.assertEqual(database.get_table_counts(), {"images": 1, "colour_spaces": 1, "conversions": 1})

    def test_failed_batch_job_is_persisted(self):
        # Dimensions are unknown when a corrupt uploaded image is first recorded.
        image_id = database.save_image_record("broken.png", None, None, "image/png")
        database.save_conversion_record(image_id, "Batch RGB to YIQ to RGB", status="failed")
        history = database.get_recent_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][1], "broken.png")
        self.assertEqual(history[0][5], "failed")
        self.assertEqual(database.get_table_counts()["conversions"], 1)

    def test_image_dimensions_can_be_updated_after_decode(self):
        image_id = database.save_image_record("sample.png", None, None, "PNG")
        database.update_image_dimensions(image_id, 12, 8)
        with database.get_connection() as conn:
            row = conn.execute("SELECT width, height FROM images WHERE image_id=?", (image_id,)).fetchone()
        self.assertEqual(row, (12, 8))


if __name__ == "__main__":
    unittest.main()
