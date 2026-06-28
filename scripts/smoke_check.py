from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []

    required_files = [
        "stadium_system.py",
        "dashboard.html",
        "requirements.txt",
        "assets/project-banner.svg",
        "assets/screenshots/stadium-dashboard.png",
    ]

    for relative_path in required_files:
        if not (ROOT / relative_path).is_file():
            errors.append(f"Missing required file: {relative_path}")

    source_path = ROOT / "stadium_system.py"
    source = source_path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        errors.append(f"stadium_system.py has invalid syntax: {exc}")
        tree = ast.Module(body=[], type_ignores=[])

    names = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef))
    }
    required_symbols = {
        "GateState",
        "DecisionEngine",
        "detect_crowding_in_gate",
        "point_in_zone",
        "draw_frame",
        "api_status",
        "api_health",
        "run_vision",
    }
    missing_symbols = sorted(required_symbols - names)
    if missing_symbols:
        errors.append(f"Missing expected symbols: {', '.join(missing_symbols)}")

    gate_definitions_found = False
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "GATE_DEFINITIONS":
                    gate_definitions_found = True
                    try:
                        gate_definitions = ast.literal_eval(node.value)
                    except (ValueError, SyntaxError):
                        errors.append("GATE_DEFINITIONS must remain a literal dictionary")
                        break

                    for gate_name in ("A", "B", "C", "D"):
                        gate = gate_definitions.get(gate_name)
                        if not isinstance(gate, dict):
                            errors.append(f"Missing gate definition for {gate_name}")
                            continue
                        if "zone" not in gate or "capacity" not in gate:
                            errors.append(f"Gate {gate_name} must define zone and capacity")
                    break

    if not gate_definitions_found:
        errors.append("GATE_DEFINITIONS was not found")

    dashboard = (ROOT / "dashboard.html").read_text(encoding="utf-8", errors="ignore")
    for endpoint in ("/api/status", "/api/health"):
        if endpoint == "/api/status" and endpoint not in dashboard:
            errors.append("dashboard.html should reference /api/status")
        if endpoint not in source:
            errors.append(f"stadium_system.py should expose {endpoint}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Validated stadium monitor structure, API routes, gate definitions, and dashboard assets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
