import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ["FLASK_ENV"] = 'testing'

from contextlib import contextmanager

from unittest.mock import MagicMock
import fakeredis

from flask.sessions import SecureCookieSession
from werkzeug.datastructures import ImmutableMultiDict

from tests.utils import create_session_form_data

import pytest

from app.app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    _app = create_app()

    with _app.app_context():
        yield _app


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def test_request_context(app):
    with app.test_request_context() as req:
        yield req


CURRENT_USER_IDNR = "0123456789"


@pytest.fixture(autouse=True)
def testing_current_user(monkeypatch):
    monkeypatch.setattr("app.data_access.storage.session_storage.current_user", MagicMock(idnr_hashed=CURRENT_USER_IDNR))


@pytest.fixture(autouse=True)
def testing_database(monkeypatch):
    fakeredis_connection = fakeredis.FakeStrictRedis()
    monkeypatch.setattr("app.data_access.redis_connector_service.RedisConnectorService._redis_connection",
                        fakeredis_connection)
    yield
    fakeredis_connection.flushall()


@pytest.fixture
def new_test_request_context(app):
    @contextmanager
    def _new_test_request_context(method='GET', form_data=None, stored_data=None, session_identifier='form_data'):
        with app.test_request_context() as req:
            req.request.method = method
            if stored_data:
                req.session = SecureCookieSession({session_identifier: create_session_form_data(stored_data)})
            if form_data:
                req.request.data = ImmutableMultiDict(form_data)
                req.request.form = ImmutableMultiDict(form_data)
            yield req
    return _new_test_request_context


@pytest.fixture
def new_test_request_context_with_data_in_session(app, new_test_request_context):
    @contextmanager
    def _new_test_request_context(method='GET', form_data=None, session_data=None, session_identifier='form_data'):
        from app.data_access.storage.form_storage import FormStorage
        from app.data_access.redis_connector_service import RedisConnectorService
        with new_test_request_context(method=method, form_data=form_data) as req:
            if session_data:
                RedisConnectorService().save_to_redis(CURRENT_USER_IDNR + '_' + session_identifier,
                                               FormStorage.serialize_data(session_data))
            yield req
    return _new_test_request_context


@pytest.fixture(scope="session")
def db(app):
    """Ensure tables are created and dropped at the start and end of test runs."""
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


def _truncate_all_tables(db):
    tables = db.metadata.sorted_tables
    connection = db.engine.connect()
    transaction = connection.begin()
    connection.execute('PRAGMA foreign_keys = OFF;')  # SQLite specific
    for table in tables:
        connection.execute(table.delete())
    connection.execute('PRAGMA foreign_keys = ON;')  # SQLite specific
    transaction.commit()


@pytest.fixture
def transactional_session(db):
    """Reset DB to empty state after each test, allowing faster isolated tests."""
    yield db.session
    db.session.expunge_all()
    _truncate_all_tables(db)
