# Engineering Principles

This repository follows the public portfolio standard used across Abdulelah Alkhathami's flagship AI projects.

## Principles

- Separate perception from operational decision logic.
- Make calibration assumptions visible.
- Keep safety and privacy constraints explicit for camera-based systems.
- Provide API access to derived state instead of coupling everything to a local window.
- Treat local model/video assets as prototype dependencies, not production architecture.

## Applied Here

- YOLO detection feeds gate-zone assignment.
- `DecisionEngine` owns status, alerting, ETA, and staff recommendations.
- The dashboard consumes `/api/status`.
- Future work calls out configuration, tests, deployment packaging, and camera privacy.
