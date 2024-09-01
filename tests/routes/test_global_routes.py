from tests import *

def test_undefined_route(client):
    response = client.get(UNDEFINED_ROUTE)
    assert response.status_code == 404

