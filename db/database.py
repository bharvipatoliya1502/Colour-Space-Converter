"""SQLite persistence for image uploads and conversion history."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "project_data.db"


@contextmanager
def get_connection():
    """Yield a SQLite connection and always commit/rollback and close it."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS images (
                image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                uploaded_at TEXT NOT NULL,
                width INTEGER,
                height INTEGER,
                file_format TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS colour_spaces (
                colour_space_id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id INTEGER NOT NULL,
                source_space TEXT NOT NULL,
                target_space TEXT NOT NULL,
                matrix_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(image_id) REFERENCES images(image_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversions (
                conversion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id INTEGER NOT NULL,
                operation TEXT NOT NULL,
                mae REAL,
                rmse REAL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(image_id) REFERENCES images(image_id)
            )
        """)


def save_image_record(filename, width, height, file_format):
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO images(filename, uploaded_at, width, height, file_format)
               VALUES (?, ?, ?, ?, ?)""",
            (filename, datetime.now().isoformat(timespec="seconds"),
             int(width) if width is not None else None,
             int(height) if height is not None else None,
             str(file_format or "Unknown"))
        )
        return cursor.lastrowid


def update_image_dimensions(image_id, width, height):
    """Update dimensions after an uploaded image has been decoded successfully."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE images SET width = ?, height = ? WHERE image_id = ?",
            (int(width), int(height), int(image_id)),
        )


def save_colour_space_record(image_id, source_space="RGB", target_space="YIQ"):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO colour_spaces
               (image_id, source_space, target_space, matrix_name, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (image_id, source_space, target_space, "RGB_TO_YIQ_3x3",
             datetime.now().isoformat(timespec="seconds"))
        )


def save_conversion_record(image_id, operation, mae=None, rmse=None, status="success"):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO conversions
               (image_id, operation, mae, rmse, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (image_id, operation, mae, rmse, status,
             datetime.now().isoformat(timespec="seconds"))
        )


def get_recent_history(limit=20):
    with get_connection() as conn:
        return conn.execute("""
            SELECT c.conversion_id, i.filename, c.operation, c.mae, c.rmse,
                   c.status, c.created_at
            FROM conversions c
            JOIN images i ON i.image_id = c.image_id
            ORDER BY c.conversion_id DESC
            LIMIT ?
        """, (int(limit),)).fetchall()


def get_table_counts():
    with get_connection() as conn:
        return {
            table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in ("images", "colour_spaces", "conversions")
        }
