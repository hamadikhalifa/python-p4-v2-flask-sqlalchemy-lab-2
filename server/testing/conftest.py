import os
import pytest
from app import app, db

TEST_DB = "test.db"

@pytest.fixture(autouse=True)
def app_context():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{TEST_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture
def client():
    return app.test_client()
