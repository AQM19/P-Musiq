import pytest
from app import create_app
import os

VALID_LINK = 'https://www.youtube.com/watch?v=-cHr2LayZtQ'
INVALID_LINK = 'https://www.youtube.com/watch?v=some_invalid_id'
UNDEFINED_ROUTE = '/some/undefined/route'
SPACED_LINK = '    '
SPECIAL_CHARS_LINK = '!@#$%^&*()'
CUTTED_LINK = 'https://www.youtube.com/watch?v='

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def setup_temp_file():
    # Configuración: crear un archivo temporal para la prueba
    temp_file_path = '/tmp/[Female Cover] BROTHERS OF METAL – Yggdrasil [NIGHTCORE by ANAHATA + Lyrics].mp3'
    with open(temp_file_path, 'wb') as f:
        f.write(b'some_mp3_data')
    yield temp_file_path
    # Limpieza: eliminar el archivo temporal después de la prueba
    os.remove(temp_file_path)