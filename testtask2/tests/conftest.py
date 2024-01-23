import pytest

from testtask2 import create_app


@pytest.fixture()
def app():  # вызов приложения
    app = create_app()

    yield app


@pytest.fixture()
def client(app):  # тестовый клиент
    return app.test_client()
