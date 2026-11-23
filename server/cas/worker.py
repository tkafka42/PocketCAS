"""Isolierte Berechnung: eigener Prozess pro Anfrage mit Zeit- und Speicherlimit."""

import os

# Muss vor dem ersten Import von NumPy stehen, sonst greift das Speicherlimit schlecht.
for _variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_variable, "1")

import json  # noqa: E402
import math  # noqa: E402
import multiprocessing as mp  # noqa: E402
import resource  # noqa: E402
import threading  # noqa: E402
from dataclasses import dataclass  # noqa: E402

MAX_RESPONSE_BYTES = 1_000_000

_context = mp.get_context("forkserver")
_context.set_forkserver_preload(["cas.evaluator"])
_slots_lock = threading.Lock()
_slots: threading.BoundedSemaphore | None = None


@dataclass(frozen=True)
class WorkerLimits:
    timeout_seconds: float
    memory_mb: int
    max_workers: int


def _failure(code: str, message: str) -> dict:
    return {"ok": False, "code": code, "message": message, "position": None}


def _child(connection, job: dict, limits: WorkerLimits) -> None:
    # Der Rechenprozess bekommt weder Passwort noch Datenbank-Zugang.
    os.environ.clear()
    memory = limits.memory_mb * 1024 * 1024
    cpu = math.ceil(limits.timeout_seconds) + 1
    resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
    resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
    resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

    from .evaluator import evaluate_job

    try:
        result = evaluate_job(job)
        data = json.dumps(result, ensure_ascii=False, default=str).encode()
    except MemoryError:
        data = json.dumps(_failure("TOO_LARGE", "Die Berechnung braucht zu viel Speicher.")).encode()
    except Exception:  # noqa: BLE001 - keine internen Details nach außen geben
        data = json.dumps(_failure("MATH_ERROR", "Das lässt sich nicht berechnen.")).encode()
    if len(data) > MAX_RESPONSE_BYTES:
        data = json.dumps(_failure("TOO_LARGE", "Das Ergebnis ist zu groß.")).encode()
    connection.send_bytes(data)
    connection.close()


def _get_slots(limits: WorkerLimits) -> threading.BoundedSemaphore:
    global _slots
    with _slots_lock:
        if _slots is None:
            _slots = threading.BoundedSemaphore(limits.max_workers)
        return _slots


def run_job(job: dict, limits: WorkerLimits) -> dict:
    slots = _get_slots(limits)
    if not slots.acquire(timeout=limits.timeout_seconds):
        return _failure("BUSY", "Der Server rechnet gerade viel. Versuche es gleich noch einmal.")
    receiver, sender = _context.Pipe(duplex=False)
    process = _context.Process(target=_child, args=(sender, job, limits), daemon=True)
    try:
        process.start()
        sender.close()
        if not receiver.poll(limits.timeout_seconds):
            return _failure("TIMEOUT", "Die Berechnung dauert zu lange und wurde abgebrochen.")
        return json.loads(receiver.recv_bytes(MAX_RESPONSE_BYTES + 1024))
    except (EOFError, OSError):
        # Der Prozess wurde vom Limit beendet, bevor er antworten konnte.
        return _failure("TOO_LARGE", "Die Berechnung braucht zu viele Ressourcen.")
    finally:
        receiver.close()
        if process.pid is not None:
            process.kill()
            process.join()
            process.close()
        slots.release()
