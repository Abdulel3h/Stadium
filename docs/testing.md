# Testing and CI

This repository uses lightweight CI because the runtime path depends on OpenCV, Ultralytics YOLO, local video assets, and a GUI display.

## Local Validation

Run these checks before opening a pull request:

```bash
python -m compileall stadium_system.py
python scripts/smoke_check.py
```

For full manual testing:

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
python stadium_system.py
```

Then open `dashboard.html` while the Flask API is running.

## CI Workflow

`.github/workflows/ci.yml` runs on pull requests and pushes to `main`.

The workflow validates:

- Python syntax for `stadium_system.py`
- required dashboard, screenshot, and dependency files
- expected API route strings
- expected gate definitions and core vision/decision-engine symbols

## Current Coverage

The CI workflow intentionally avoids running YOLO inference, opening video files, or starting an OpenCV GUI window. Those steps require a local visual runtime and model files.

## Recommended Next Tests

- Split the decision engine into an import-safe module and add unit tests for crowding, occupancy, alerting, and staff allocation.
- Add a mock-frame test for gate assignment.
- Add API tests for `/api/status` and `/api/health` after app creation is separated from the video loop.
- Add a short recorded demo after model/video calibration is stable.
