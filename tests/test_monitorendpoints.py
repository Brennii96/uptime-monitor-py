from fastapi.testclient import TestClient


def valid_payload():
    return {
        "name": "Kite School of Kenpo",
        "description": "",
        "url": "https://www.kiteschoolofkenpo.co.uk/",
    }


def test_monitor_create_endpoint(client: TestClient):
    response = client.post("/monitors/", json=valid_payload())
    body = response.json()

    assert response.status_code == 201
    assert body["id"] == 1
    assert body["name"] == valid_payload()["name"]
    assert body["description"] == valid_payload()["description"]
    assert body["url"] == valid_payload()["url"]
    assert body["checks"] == []
    assert "created_at" in body


def test_monitor_missing_fields_for_create_endpoint(client: TestClient):
    payload = valid_payload()
    payload.pop("url")

    response = client.post("/monitors/", json=payload)
    body = response.json()

    assert response.status_code == 422
    assert body["detail"][0]["loc"] == ["body", "url"]


def test_monitor_description_is_optional(client: TestClient):
    payload = valid_payload()
    payload.pop("description")

    response = client.post("/monitors/", json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body["description"] is None


def test_monitor_invalid_url_for_create_endpoint(client: TestClient):
    payload = valid_payload()
    payload["url"] = "some-url"

    response = client.post("/monitors/", json=payload)
    body = response.json()

    assert response.status_code == 422
    assert body["detail"][0]["type"] == "url_parsing"
