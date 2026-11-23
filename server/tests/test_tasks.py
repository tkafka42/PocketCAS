import uuid
from datetime import UTC, datetime, timedelta


def stamp(minutes=0):
    return (datetime.now(UTC) + timedelta(minutes=minutes)).isoformat()


def task_body(**overrides):
    return {
        "id": str(uuid.uuid4()),
        "inputSource": "keypad",
        "expression": "x^2-4=0",
        "command": "solve",
        "arguments": ["x"],
        "resultText": "x=-2 or x=2",
        "updatedAt": stamp(-10),
        "createdAt": stamp(-10),
        **overrides,
    }


def update_body(task, **overrides):
    fields = {k: v for k, v in task.items() if k not in ("id", "createdAt", "hasImage")}
    return {**fields, "updatedAt": stamp(-1), **overrides}


def test_create_read_list(client):
    body = task_body(measurements={"angle": 31.5})
    assert client.post("/api/tasks", json=body).status_code == 201
    task = client.get(f"/api/tasks/{body['id']}").json()
    assert task["measurements"] == {"angle": 31.5}
    assert [t["id"] for t in client.get("/api/tasks").json()] == [body["id"]]


def test_repeated_create_is_idempotent(client):
    body = task_body()
    assert client.post("/api/tasks", json=body).status_code == 201
    assert client.post("/api/tasks", json=body).status_code == 200
    assert len(client.get("/api/tasks").json()) == 1


def test_update_and_recalculate(client):
    task = client.post("/api/tasks", json=task_body()).json()
    response = client.put(
        f"/api/tasks/{task['id']}",
        json=update_body(task, expression="x^2-9=0", recalculate=True),
    )
    assert response.status_code == 200
    assert response.json()["resultText"] == "x=-3 or x=3"


def test_failed_recalculation_changes_nothing(client):
    task = client.post("/api/tasks", json=task_body()).json()
    response = client.put(
        f"/api/tasks/{task['id']}",
        json=update_body(task, expression="(x", recalculate=True),
    )
    assert response.status_code == 422
    assert client.get(f"/api/tasks/{task['id']}").json()["expression"] == "x^2-4=0"


def test_last_write_wins(client):
    task = client.post("/api/tasks", json=task_body()).json()
    newer = update_body(task, expression="newer", updatedAt=stamp(-2))
    older = update_body(task, expression="older", updatedAt=stamp(-5))
    assert client.put(f"/api/tasks/{task['id']}", json=newer).status_code == 200
    response = client.put(f"/api/tasks/{task['id']}", json=older)
    assert response.status_code == 409
    assert response.json()["current"]["expression"] == "newer"


def test_future_clock_is_clamped(client):
    task = client.post("/api/tasks", json=task_body()).json()
    client.put(f"/api/tasks/{task['id']}", json=update_body(task, updatedAt=stamp(600)))
    saved = datetime.fromisoformat(client.get(f"/api/tasks/{task['id']}").json()["updatedAt"])
    assert saved <= datetime.now(UTC)


def test_delete_is_idempotent_and_blocks_resurrection(client):
    task = client.post("/api/tasks", json=task_body()).json()
    assert client.delete(f"/api/tasks/{task['id']}").status_code == 204
    assert client.delete(f"/api/tasks/{task['id']}").status_code == 204
    assert client.get(f"/api/tasks/{task['id']}").status_code == 404
    assert client.get("/api/tasks").json() == []
    stale = update_body(task, updatedAt=stamp(-5))
    assert client.put(f"/api/tasks/{task['id']}", json=stale).status_code == 409
    assert client.post("/api/tasks", json=task_body(id=task["id"])).status_code == 409


def test_stale_offline_delete_loses(client):
    task = client.post("/api/tasks", json=task_body()).json()
    client.put(f"/api/tasks/{task['id']}", json=update_body(task, updatedAt=stamp(-1)))
    response = client.delete(f"/api/tasks/{task['id']}", params={"updatedAt": stamp(-5)})
    assert response.status_code == 409
    assert client.get(f"/api/tasks/{task['id']}").status_code == 200


def test_filters_and_search(client):
    client.post("/api/tasks", json=task_body())
    client.post("/api/tasks", json=task_body(inputSource="camera", command="factor", expression="x^2+2x+1"))
    assert len(client.get("/api/tasks", params={"source": "camera"}).json()) == 1
    assert len(client.get("/api/tasks", params={"command": "solve"}).json()) == 1
    assert len(client.get("/api/tasks", params={"search": "2x"}).json()) == 1
    assert client.get("/api/tasks", params={"search": "%"}).json() == []


def test_validation_message_is_german(client):
    response = client.post("/api/tasks", json={"id": "nope"})
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"
    assert response.json()["message"].startswith("Ungültige Eingabe")
