-- Optional sample rows for demonstrating the schema in a fresh SQLite database.
-- Runtime app uploads and conversion history are stored by db/database.py.
INSERT INTO images (filename, uploaded_at, width, height, file_format)
VALUES ('sample_demo.png', '2026-01-01T10:00:00', 2, 2, 'PNG');

INSERT INTO colour_spaces (image_id, source_space, target_space, matrix_name, created_at)
VALUES (last_insert_rowid(), 'RGB', 'YIQ', 'RGB_TO_YIQ_3x3', '2026-01-01T10:00:01');

INSERT INTO conversions (image_id, operation, mae, rmse, status, created_at)
VALUES (1, 'RGB to YIQ to RGB', 0.0, 0.0, 'success', '2026-01-01T10:00:02');
