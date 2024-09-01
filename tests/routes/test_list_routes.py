from tests import *
from app.enums import Endpoints
from unittest.mock import patch

def test_list_route(client):
    response = client.get(Endpoints.LIST.value)
    assert response.status_code == 200
    assert b'<div class="list-content">' in response.data

def test_list_download_valid_link(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': VALID_LINK})
    assert response.status_code == 200

def test_list_download_invalid_link(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': INVALID_LINK})
    assert response.status_code == 500
    assert b'Error al procesar la solicitud' in response.data

def test_list_download_empty_list(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': ''})
    assert response.status_code == 200
    assert b'Por favor, inserta un link a YouTube' in response.data

def test_list_page_content(client):
    response = client.get(Endpoints.LIST.value)
    assert b'<input id="input-item"' in response.data
    assert b'<button id="add-button" type="button">' in response.data
    assert b'<ul class="item-list">' in response.data
    assert b'<button type="button" class="download-btn">' in response.data

def test_list_download_route_whitespace_link(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': SPACED_LINK})
    assert response.status_code == 500
    assert b'Error al procesar la solicitud' in response.data

def test_list_download_route_special_chars_link(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': SPECIAL_CHARS_LINK})
    assert response.status_code == 500
    assert b'Error al procesar la solicitud' in response.data

def test_list_download_route_service_error(client):
    with patch('app.services.youtube_downloader.download_audio_mp3_from_youtube', side_effect=Exception("Mocked error")):
        response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': INVALID_LINK})
        assert response.status_code == 500
        assert b'Error al procesar la solicitud' in response.data

def test_list_download_route_headers(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': VALID_LINK})
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'audio/mpeg'

def test_list_download_route_multiple_requests(client):
    for _ in range(3):
        response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': VALID_LINK})
        assert response.status_code == 200

def test_list_download_route_empty_data(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={})
    assert response.status_code == 200
    assert b'Por favor, inserta un link a YouTube' in response.data

def test_list_download_route_invalid_data_type(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': 12345})
    assert response.status_code == 500
    assert b'Error al procesar la solicitud' in response.data

def test_list_download_route_invalid_link_format(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'kknslkn': INVALID_LINK})
    assert response.status_code == 200
    assert b'Por favor, inserta un link a YouTube' in response.data

def test_list_download_route_malformed_link(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': CUTTED_LINK})
    assert response.status_code == 500
    assert b'Error al procesar la solicitud' in response.data

def test_list_download_route_with_extra_data(client):
    response = client.post(Endpoints.DOWNLOAD_LIST.value, json={'item': VALID_LINK, 'extra_param': 'extra_value'})
    assert response.status_code == 200
    assert b'Por favor, inserta un link a YouTube' not in response.data