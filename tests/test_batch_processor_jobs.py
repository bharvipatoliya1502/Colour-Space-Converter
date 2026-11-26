import io, tempfile
from PIL import Image
from unittest.mock import patch
from app import batch_processor as bp

class Upload(io.BytesIO):
    name="batch.png"
    type="image/png"

def test_enqueue_creates_queued_job_and_run_success():
    stream=io.BytesIO()
    Image.new("RGB",(2,2),(20,40,60)).save(stream,format="PNG")
    upload=Upload(stream.getvalue())
    with tempfile.TemporaryDirectory() as td, patch("db.database.DB_PATH",__import__("pathlib").Path(td)/"t.db"):
        from db.database import initialize_database, get_recent_history
        initialize_database()
        job=bp.enqueue_batch_file(upload)
        assert get_recent_history()[0][5]=="queued"
        result=bp.run_batch_job(job)
        assert result["status"]=="success"
        assert get_recent_history()[0][5]=="success"

def test_corrupt_batch_job_is_failed():
    upload=Upload(b"not an image")
    with tempfile.TemporaryDirectory() as td, patch("db.database.DB_PATH",__import__("pathlib").Path(td)/"t.db"):
        from db.database import initialize_database, get_recent_history
        initialize_database()
        job=bp.enqueue_batch_file(upload)
        result=bp.run_batch_job(job)
        assert result["status"]=="failed"
        assert get_recent_history()[0][5]=="failed"
