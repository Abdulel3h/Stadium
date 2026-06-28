# Reviewer Guide

Use this guide if you are evaluating Stadium Gate Monitor for computer vision, operations tooling, or real-time dashboard roles.

## 30-Second Review

- Start with `README.md` for the vision and dashboard concept.
- Open `docs/architecture.md` to understand detection, zone assignment, decision logic, and API output.
- Inspect `stadium_system.py`, especially `DecisionEngine` and `run_vision()`.
- Open `dashboard.html` to review the operations dashboard surface.

## What This Project Demonstrates

- YOLO and OpenCV applied to an operations problem.
- Separation between perception and decision logic.
- Flask status API for dashboard consumption.
- Operational alerting and staff-distribution thinking.
- Clear documentation of calibration and privacy limits.

## Quick Technical Path

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install ultralytics opencv-python flask flask-cors numpy
python stadium_system.py
```

## Prototype Boundaries

- Gate zones are hard-coded and must be calibrated per camera.
- Camera privacy, latency, and deployment assumptions require deeper review.
- Tests are needed for status transitions and API schema.

## Related Repositories

- [Abdulelah AI Portfolio](https://github.com/Abdulel3h/Abdulelah)
- [absher-insight](https://github.com/Abdulel3h/absher-insight)
