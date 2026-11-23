import pytest

from .conftest import TEST_PASSWORD


@pytest.mark.parametrize("method, path", [
    ("get", "/api/tasks"),
    ("get", "/api/commands"),
    ("post", "/api/evaluate"),
    ("delete", "/api/tasks/7a8f0c0e-5f55-4c70-a1fb-3c61e1d3a001"),
])
def test_protected_routes_need_login(anonymous_client, method, path):
    anonymous_client.cookies.clear()
    response = anonymous_client.request(method, path, json={"expression": "1+1"} if method == "post" else None)
    assert response.status_code == 401
    assert response.json()["code"] == "UNAUTHORIZED"


def test_wrong_password_is_rejected(anonymous_client):
    anonymous_client.cookies.clear()
    response = anonymous_client.post("/api/login", json={"password": "falsch"})
    assert response.status_code == 401
    assert "pocketcas_session" not in response.cookies


def test_forged_cookie_is_rejected(anonymous_client):
    anonymous_client.cookies.clear()
    anonymous_client.cookies.set("pocketcas_session", "9999999999.deadbeef")
    assert anonymous_client.get("/api/tasks").status_code == 401
    anonymous_client.cookies.clear()


def test_login_and_logout(anonymous_client):
    anonymous_client.cookies.clear()
    response = anonymous_client.post("/api/login", json={"password": TEST_PASSWORD})
    cookie = response.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=strict" in cookie
    assert anonymous_client.get("/api/session").json() == {"authenticated": True}
    anonymous_client.post("/api/logout")
    assert anonymous_client.get("/api/session").json() == {"authenticated": False}


def test_health_is_public(anonymous_client):
    anonymous_client.cookies.clear()
    assert anonymous_client.get("/api/health").json() == {"status": "ok"}
