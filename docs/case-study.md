# Case Study

## Context

Stadium Gate Monitor is a computer-vision operations prototype for estimating gate occupancy, crowding, alerts, and staff distribution from video input.

## Problem

Large venue operations require fast visibility into gate congestion, but a portfolio prototype cannot claim real deployment or calibrated production accuracy. The project demonstrates the architecture of a vision-to-operations dashboard.

## Constraints

- Gate zones are hard-coded for the demo video.
- Camera privacy, angle, lighting, and latency assumptions are not production-reviewed.
- YOLO model files and videos are large and should be managed carefully.
- The dashboard must show operational state without implying real venue deployment.

## Solution

The Python system runs YOLO person detection, maps detections into configured gate zones, computes occupancy/crowding, and exposes status through Flask endpoints. A standalone HTML dashboard polls the status API.

## Architecture

See [Architecture](architecture.md). The core flow is video source -> YOLO detection -> zone assignment -> decision engine -> Flask API -> dashboard.

## Key Engineering Decisions

- Separate perception logic from decision logic.
- Keep gate definitions explicit and easy to recalibrate.
- Expose `/api/status` and `/api/health` for dashboard and integration checks.
- Make CORS origins configurable through `ALLOWED_ORIGINS`.

## Trade-Offs

- Hard-coded zones are easy to review but not portable.
- A local Flask API is simple but not a production streaming architecture.
- Model/video assets make the demo tangible but increase repository size.

## What I Learned

- Computer-vision products need calibration, privacy review, and operational feedback loops.
- Dashboards should expose decisions and uncertainty, not just detection counts.

## Current Limitations

- No automated tests for the decision engine yet.
- No camera calibration workflow.
- No privacy or retention policy for real footage.
- CORS must be configured explicitly for any deployed dashboard.

## Future Improvements

- Add unit tests for `DecisionEngine`.
- Move gate definitions to a config file.
- Add a calibration guide and privacy checklist.
- Add latency and FPS reporting.

## Reviewer Evaluation

Inspect `stadium_system.py`, `dashboard.html`, the architecture doc, and screenshot evidence. Evaluate zone logic, API shape, decision rules, and documented deployment limits.
