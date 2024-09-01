from tests import *
from app.enums import Endpoints
from unittest.mock import patch

def test_index_route(client):
    response = client.get(Endpoints.BASE.value)
    assert response.status_code == 200
    assert b'<form' in response.data

def test_download_route_valid_link(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': VALID_LINK})    
    assert response.status_code == 200

def test_download_route_invalid_link(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': INVALID_LINK})
    assert response.status_code == 500
    assert b'Error al procesar la solicitud' in response.data

def test_download_route_empty_link(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': ''})
    assert b'Por favor, inserta un link a YouTube' in response.data

def test_index_page_content(client):
    response = client.get(Endpoints.BASE.value)
    assert b'<button id="download-btn" type="button">' in response.data
    assert b'<input id="link-inp" type="text"' in response.data
    assert b'<form method="POST"' in response.data

def test_download_route_whitespace_link(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': SPACED_LINK})
    assert response.status_code == 500
    assert b'Error al procesar la solicitud' in response.data

def test_download_route_special_chars_link(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': SPECIAL_CHARS_LINK})
    assert response.status_code == 500
    assert b'Error al procesar la solicitud' in response.data

def test_download_route_service_error(client):
    with patch('app.services.youtube_downloader.download_audio_mp3_from_youtube', side_effect=Exception("Mocked error")):
        response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': INVALID_LINK})
        assert response.status_code == 500
        assert b'Error al procesar la solicitud' in response.data

def test_download_route_headers(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': VALID_LINK})
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'audio/mpeg'

def test_download_route_multiple_requests(client):
    for _ in range(3):
        response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': VALID_LINK})
        assert response.status_code == 200

def test_download_route_empty_data(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={})
    assert response.status_code == 200
    assert b'Por favor, inserta un link a YouTube' in response.data

def test_download_route_invalid_data_type(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': 12345})
    assert response.status_code == 500
    assert b'Error al procesar la solicitud' in response.data

def test_download_route_invalid_link_format(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={'kknslkn': INVALID_LINK})
    assert response.status_code == 200
    assert b'Por favor, inserta un link a YouTube' in response.data

def test_download_route_malformed_link(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': CUTTED_LINK})
    assert response.status_code == 500
    assert b'Error al procesar la solicitud' in response.data

def test_download_route_with_extra_data(client):
    response = client.post(Endpoints.DOWNLOAD.value, data={'youtube_link': VALID_LINK, 'extra_param': 'extra_value'})
    assert response.status_code == 200
    assert b'Por favor, inserta un link a YouTube' not in response.data