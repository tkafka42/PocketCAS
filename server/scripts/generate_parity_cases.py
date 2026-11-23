"""Erzeugt tests/parity_cases.json aus dem echten complex_calc.

Aufruf mit dem Python von complex_calc:
  ../../complex_calc/.venv/bin/python scripts/generate_parity_cases.py \
      ../../complex_calc tests/parity_cases.json extra_cases.json
"""

import ast
import json
import pathlib
import re
import signal
import sys

from complex_calc.core.session import Session
from complex_calc.functions import REGISTRY

SKIPPED_WORDS = re.compile(r"\b(wait|request|requeststr|getkey|getplatform|getlanginfo)\b", re.I)
RANDOM_WORDS = re.compile(r"\brand\w*\b", re.I)


def on_alarm(*_):
    raise TimeoutError


def harvest(repo: pathlib.Path) -> list[str]:
    found = []
    for path in sorted((repo / "tests").glob("test_*.py")):
        if path.name == "test_security.py":
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                text = node.value.strip()
                if 2 < len(text) <= 90 and "\n" not in text:
                    found.append(text)
    for line in (repo / "README.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("› "):
            found.append(line[2:].strip())
    return list(dict.fromkeys(found))


def run(statements: list[str]) -> str | None:
    session = Session(input_provider=lambda prompt, is_string: "5")
    entry = None
    try:
        signal.alarm(3)
        for statement in statements:
            entry = session.run(statement)
            if entry.error:
                return None
    except BaseException:  # noqa: BLE001
        return None
    finally:
        signal.alarm(0)
    return entry.text if entry and entry.text else None


def main() -> None:
    repo, out_path, extra_path = map(pathlib.Path, sys.argv[1:4])
    signal.signal(signal.SIGALRM, on_alarm)

    names = {}
    for spec in REGISTRY.values():
        for key in (spec.name, *spec.aliases):
            names[key.lower()] = spec.name

    cases = []
    seen = set()
    for source in sorted(harvest(repo), key=len):
        if SKIPPED_WORDS.search(source) or RANDOM_WORDS.search(source):
            continue
        words = {word.lower() for word in re.findall(r"[^\W\d][\w.]*", source)}
        hits = {names[word] for word in words if word in names}
        hits |= {name for key, name in names.items() if not key.isascii() and key in source.lower()}
        if not hits:
            continue
        expected = run([source])
        if expected is None:
            continue
        cases.append({"commands": sorted(hits), "statements": [source], "expected": expected})
        seen |= hits

    for name, statements in json.loads(extra_path.read_text(encoding="utf-8")).items():
        expected = run(statements)
        if expected is not None:
            cases.append({"commands": [name], "statements": statements, "expected": expected})
            seen.add(name)

    canonical = {spec.name for spec in REGISTRY.values()}
    out_path.write_text(json.dumps(cases, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"cases={len(cases)} covered={len(seen & canonical)}/{len(canonical)}")
    print("uncovered:", sorted(canonical - seen))


if __name__ == "__main__":
    main()
