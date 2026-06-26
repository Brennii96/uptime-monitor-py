from fastapi.testclient import TestClient


def valid_payload():
    return {
        "name": "Kite School of Kenpo",
        "description": "",
        "url": "https://www.kiteschoolofkenpo.co.uk/",
    }


def test_monitor_create_endpoint(client: TestClient):
    response = client.post("/monitors", json=valid_payload())
    assert response.status_code == 201
    assert response.json() == {"id": 1, **valid_payload()}


def test_monitor_missing_fields_for_create_endpoint(client: TestClient):
    payload = valid_payload()
    payload.pop("description")
    payload.pop("url")

    response = client.post("/monitors", json=payload)
    body = response.json()

    assert response.status_code == 422
    assert body["detail"][0]["loc"] == ["body", "description"]


def test_monitor_invalid_url_for_create_endpoint(client: TestClient):
    payload = valid_payload()
    payload["url"] = "some-url"

    response = client.post("/monitors", json=payload)
    body = response.json()

    assert response.status_code == 422
    assert body["detail"][0]["type"] == "url_parsing"
