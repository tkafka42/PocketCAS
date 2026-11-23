import pathlib
import tempfile

import pytest


def evaluate(client, expression, **extra):
    return client.post("/api/evaluate", json={"expression": expression, **extra})


def test_exact_and_decimal(client):
    body = evaluate(client, "√(8)").json()
    assert body["text"] == "2·√(2)"
    assert body["decimal"] == "2.82843"
    assert "sqrt" in body["latex"]


def test_command_is_built_with_original_syntax(client):
    body = evaluate(client, "x^2-4=0", command="solve", arguments=["x"]).json()
    assert body["source"] == "solve(x^2-4=0,x)"
    assert body["text"] == "x=-2 or x=2"
    assert body["status"] == "solved"


def test_command_without_parentheses(client):
    body = evaluate(client, "15", command="zInterval", arguments=["100", "25"]).json()
    assert body["source"] == "zInterval 15,100,25"
    assert body["table"]


def test_no_solution_status(client):
    body = evaluate(client, "x^2+1=0", command="solve", arguments=["x"]).json()
    assert body["status"] == "no_solution"


def test_context_keeps_definitions(client):
    body = evaluate(client, "f(3)", context=["Define f(x)=x^2"]).json()
    assert body["text"] == "9"


def test_german_syntax_error(client):
    response = evaluate(client, "(1+2")
    assert response.status_code == 422
    assert response.json()["code"] == "SYNTAX_ERROR"
    assert "Klammer nicht geschlossen" in response.json()["message"]


def test_unknown_command(client):
    response = evaluate(client, "1", command="doesNotExist")
    assert response.status_code == 422
    assert response.json()["code"] == "UNSUPPORTED"


def test_endless_loop_hits_engine_limit(client):
    response = evaluate(client, "While true:EndWhile")
    assert response.status_code == 422
    assert response.json()["code"] == "MATH_ERROR"


def test_slow_calculation_is_stopped(client):
    response = evaluate(client, "Wait 30")
    assert response.status_code == 504
    assert response.json()["code"] == "TIMEOUT"
    assert evaluate(client, "1+1").json()["text"] == "2"


def test_huge_calculation_does_not_kill_server(client):
    response = evaluate(client, "9^9^9^9")
    assert response.status_code in (200, 422, 504)
    assert evaluate(client, "1+1").json()["text"] == "2"


@pytest.mark.parametrize("template", ["root(8,{})", "sin({})", "nCr({},2)", "{}►_m", "nInt(#{}+x,x,0,1)"])
def test_strings_never_execute(client, template):
    with tempfile.TemporaryDirectory() as folder:
        marker = pathlib.Path(folder) / "executed"
        payload = f"\"__import__('pathlib').Path('{marker}').touch()\""
        response = evaluate(client, template.format(payload))
        assert response.status_code == 422
        assert not marker.exists()


def test_worker_has_no_secrets(client):
    from cas.worker import WorkerLimits, _context

    receiver, sender = _context.Pipe(duplex=False)
    process = _context.Process(target=_report_environment, args=(sender, WorkerLimits(5, 2048, 1)))
    process.start()
    sender.close()
    assert receiver.recv() == []
    process.join()


def _report_environment(connection, limits):
    import os
    from unittest import mock

    from cas import worker

    with mock.patch("cas.evaluator.evaluate_job", return_value={"ok": True}):
        reader, writer = worker._context.Pipe(duplex=False)
        worker._child(writer, {}, limits)
        reader.recv_bytes()
    connection.send([name for name in os.environ if name in ("APP_PASSWORD", "AUTH_SECRET", "DATABASE_URL")])
    connection.close()


def test_catalog_lists_all_commands(client):
    commands = client.get("/api/commands").json()
    names = {command["name"] for command in commands}
    assert len(commands) == 303
    assert {"solve", "normCdf", "zInterval"} <= names
    assert next(c for c in commands if c["name"] == "sin")["offline"] is True
    assert next(c for c in commands if c["name"] == "solve")["offline"] is False
