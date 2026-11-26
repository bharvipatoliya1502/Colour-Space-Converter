from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest

MAIN_PY = str(Path(__file__).resolve().parents[1] / "main.py")


def test_app_smoke_has_five_tabs_without_exception():
    at = AppTest.from_file(MAIN_PY, default_timeout=60).run()
    assert not at.exception
    assert len(at.tabs) == 5
