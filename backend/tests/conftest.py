import io
import os
import tempfile
import pytest

from app import create_app
from db import db

@pytest.fixture()
def client():
    # Use a temporary SQLite DB for tests
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    try:
        app = create_app()
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        )
        with app.app_context():
            db.create_all()
        with app.test_client() as client:
            yield client
    finally:
        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass
