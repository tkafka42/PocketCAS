"""Durchsuchbare Befehlsliste für die Autovervollständigung im Frontend."""

from functools import lru_cache

from .engine.functions import REGISTRY

_CATEGORIES = {
    "elementary": "Elementar",
    "conversions": "Elementar",
    "algebra": "Algebra",
    "cas": "Analysis",
    "extras": "Analysis",
    "lists": "Listen",
    "matrices": "Matrizen",
    "stats": "Statistik",
    "intervals": "Tests und Intervalle",
    "stattests": "Tests und Intervalle",
    "regression": "Regression",
    "finance": "Finanzen",
    "randoms": "Zufall",
    "units": "Einheiten",
    "programming": "Programmierung",
    "draw": "Zeichnen",
}

# Diese Befehle rechnet der Client offline numerisch mit math.js.
OFFLINE_COMMANDS = frozenset({
    "abs", "cos⁻¹", "cosh⁻¹", "sin⁻¹", "sinh⁻¹", "tan⁻¹", "tanh⁻¹", "ceiling", "cos", "cosh",
    "exp", "floor", "gcd", "lcm", "ln", "log", "max", "mean", "median", "min", "mod",
    "nCr", "nPr", "product", "round", "sign", "sin", "sinh", "√", "stDevSamp", "sum",
    "tan", "tanh", "varSamp", "det", "dotP", "crossP", "identity", "trace",
})


@lru_cache
def command_catalog() -> tuple[dict, ...]:
    specs = {}
    for spec in REGISTRY.values():
        specs.setdefault(spec.name, spec)
    return tuple(
        {
            "name": name,
            "signature": spec.signature,
            "summary": spec.summary,
            "aliases": list(spec.aliases),
            "category": _CATEGORIES[spec.func.__module__.rsplit(".", 1)[-1]],
            "offline": name in OFFLINE_COMMANDS,
            "no_parentheses": spec.command,
        }
        for name, spec in sorted(specs.items(), key=lambda item: item[0].lower())
    )
