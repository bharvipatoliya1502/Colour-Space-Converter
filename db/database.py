"""SQLite persistence; canonical schema is maintained in schema.sql."""
import json, sqlite3
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime
DB_PATH = Path(__file__).resolve().parent / "project_data.db"
VALID_STATUSES = {"queued", "processing", "success", "failed"}

@contextmanager
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn=sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys=ON")
        yield conn; conn.commit()
    except Exception:
        conn.rollback(); raise
    finally: conn.close()

def initialize_database():
    with get_connection() as conn:
        conn.executescript((Path(__file__).parent / "schema.sql").read_text(encoding="utf-8"))
        cols={r[1] for r in conn.execute("PRAGMA table_info(colour_spaces)")}
        for name, kind in (("matrix_values","TEXT"),("determinant","REAL"),("matrix_rank","INTEGER")):
            if name not in cols: conn.execute(f"ALTER TABLE colour_spaces ADD COLUMN {name} {kind}")

def save_image_record(filename,width,height,file_format):
    with get_connection() as c:
        cur=c.execute("INSERT INTO images(filename,uploaded_at,width,height,file_format) VALUES(?,?,?,?,?)",
          (filename,datetime.now().isoformat(timespec="seconds"),width,height,str(file_format or "Unknown")))
        return cur.lastrowid

def update_image_dimensions(image_id,width,height):
    with get_connection() as c: c.execute("UPDATE images SET width=?,height=? WHERE image_id=?",(width,height,image_id))

def save_colour_space_record(image_id,source_space="RGB",target_space="YIQ"):
    from math_engine.converter import RGB_TO_YIQ
    from math_engine.matrix import determinant,matrix_rank
    with get_connection() as c:
        c.execute("""INSERT INTO colour_spaces(image_id,source_space,target_space,matrix_name,created_at,matrix_values,determinant,matrix_rank)
        VALUES(?,?,?,?,?,?,?,?)""",(image_id,source_space,target_space,"RGB_TO_YIQ_3x3",
        datetime.now().isoformat(timespec="seconds"),json.dumps(RGB_TO_YIQ),determinant(RGB_TO_YIQ),matrix_rank(RGB_TO_YIQ)))

def save_conversion_record(image_id,operation,mae=None,rmse=None,status="success"):
    if status not in VALID_STATUSES: raise ValueError("Invalid conversion status.")
    with get_connection() as c:
        cur=c.execute("INSERT INTO conversions(image_id,operation,mae,rmse,status,created_at) VALUES(?,?,?,?,?,?)",
        (image_id,operation,mae,rmse,status,datetime.now().isoformat(timespec="seconds")))
        return cur.lastrowid

def update_conversion_status(conversion_id,status,mae=None,rmse=None):
    if status not in VALID_STATUSES: raise ValueError("Invalid conversion status.")
    with get_connection() as c:
        c.execute("UPDATE conversions SET status=?,mae=COALESCE(?,mae),rmse=COALESCE(?,rmse) WHERE conversion_id=?",
                  (status,mae,rmse,conversion_id))

def get_recent_history(limit=20):
    with get_connection() as c:
        return c.execute("""SELECT c.conversion_id,i.filename,c.operation,c.mae,c.rmse,c.status,c.created_at
        FROM conversions c JOIN images i ON i.image_id=c.image_id ORDER BY c.conversion_id DESC LIMIT ?""",(int(limit),)).fetchall()

def get_table_counts():
    with get_connection() as c:
        return {t:c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("images","colour_spaces","conversions")}
