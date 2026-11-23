"""Goldene Tests: Die Erwartungswerte stammen aus dem echten complex_calc."""

import json
import pathlib

import pytest

from cas.engine.core.session import Session
from cas.engine.functions import REGISTRY

CASES = json.loads((pathlib.Path(__file__).parent / "parity_cases.json").read_text(encoding="utf-8"))
# Brauchen Hardware oder eine geladene Bibliothek und liefern dort nur eine Fehlermeldung.
NOT_RUNNABLE = {"Get", "GetStr", "RefreshProbeVars", "Send", "libShortcut"}


@pytest.mark.parametrize("case", CASES, ids=lambda case: " ; ".join(case["statements"])[:70])
def test_matches_complex_calc(case):
    session = Session(input_provider=lambda prompt, is_string: "5")
    entry = None
    for statement in case["statements"]:
        entry = session.run(statement)
    assert not entry.error
    assert entry.text == case["expected"]


def test_every_command_is_covered():
    covered = {name for case in CASES for name in case["commands"]}
    canonical = {spec.name for spec in REGISTRY.values()}
    assert canonical - covered == NOT_RUNNABLE
