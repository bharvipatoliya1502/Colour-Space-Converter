CREATE TABLE IF NOT EXISTS images (
 image_id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL,
 uploaded_at TEXT NOT NULL, width INTEGER, height INTEGER, file_format TEXT
);
CREATE TABLE IF NOT EXISTS colour_spaces (
 colour_space_id INTEGER PRIMARY KEY AUTOINCREMENT, image_id INTEGER NOT NULL,
 source_space TEXT NOT NULL, target_space TEXT NOT NULL, matrix_name TEXT NOT NULL,
 created_at TEXT NOT NULL, matrix_values TEXT, determinant REAL, matrix_rank INTEGER,
 FOREIGN KEY(image_id) REFERENCES images(image_id)
);
CREATE TABLE IF NOT EXISTS conversions (
 conversion_id INTEGER PRIMARY KEY AUTOINCREMENT, image_id INTEGER NOT NULL,
 operation TEXT NOT NULL, mae REAL, rmse REAL,
 status TEXT NOT NULL CHECK(status IN ('queued','processing','success','failed')),
 created_at TEXT NOT NULL, FOREIGN KEY(image_id) REFERENCES images(image_id)
);
