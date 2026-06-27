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


def test_monitor_create_duplicate_url_returns_409(client: TestClient):
    client.post("/monitors/", json=valid_payload())

    response = client.post("/monitors/", json=valid_payload())

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Monitor with url https://www.kiteschoolofkenpo.co.uk/ already exists"
    }


def test_monitor_create_duplicate_url_without_trailing_slash_returns_409(client: TestClient):
    client.post("/monitors/", json=valid_payload())

    response = client.post(
        "/monitors/",
        json={
            "name": "Kite School of Kenpo Duplicate",
            "description": "",
            "url": "https://www.kiteschoolofkenpo.co.uk",
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Monitor with url https://www.kiteschoolofkenpo.co.uk/ already exists"
    }


def test_monitor_update_endpoint(client: TestClient):
    create_response = client.post("/monitors/", json=valid_payload())
    monitor_id = create_response.json()["id"]

    payload = {
        "name": "Updated Name",
        "description": "Updated description",
        "url": "https://example.com/",
    }

    response = client.put(f"/monitors/{monitor_id}", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == monitor_id
    assert body["name"] == payload["name"]
    assert body["description"] == payload["description"]
    assert body["url"] == payload["url"]


def test_monitor_update_duplicate_url_returns_409(client: TestClient):
    first = client.post("/monitors/", json=valid_payload()).json()
    second = client.post(
        "/monitors/",
        json={
            "name": "Second Monitor",
            "description": "Second description",
            "url": "https://example.com/",
        },
    ).json()

    response = client.put(
        f"/monitors/{second['id']}",
        json={
            "name": "Second Monitor",
            "description": "Second description",
            "url": first["url"],
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Monitor with url https://www.kiteschoolofkenpo.co.uk/ already exists"
    }


def test_monitor_update_duplicate_url_without_trailing_slash_returns_409(client: TestClient):
    client.post("/monitors/", json=valid_payload())
    second = client.post(
        "/monitors/",
        json={
            "name": "Second Monitor",
            "description": "Second description",
            "url": "https://example.com/",
        },
    ).json()

    response = client.put(
        f"/monitors/{second['id']}",
        json={
            "name": "Second Monitor",
            "description": "Second description",
            "url": "https://www.kiteschoolofkenpo.co.uk",
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Monitor with url https://www.kiteschoolofkenpo.co.uk/ already exists"
    }


def test_monitor_update_missing_monitor_returns_404(client: TestClient):
    payload = {
        "name": "Updated Name",
        "description": "Updated description",
        "url": "https://example.com/",
    }

    response = client.put("/monitors/999", json=payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "Monitor 999 not found"}


def test_monitor_get_missing_monitor_returns_404(client: TestClient):
    response = client.get("/monitors/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Monitor 999 not found"}


def test_monitor_delete_missing_monitor_returns_404(client: TestClient):
    response = client.delete("/monitors/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Monitor 999 not found"}
