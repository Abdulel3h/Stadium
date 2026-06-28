# Technical Decisions

| Decision | Rationale | Tradeoff |
| --- | --- | --- |
| Use YOLO with OpenCV | Provides a practical computer-vision pipeline for people detection. | Model accuracy depends on camera angle, lighting, and calibration. |
| Use hard-coded gate zones initially | Makes the prototype easy to inspect and adjust. | Real deployments need configurable zones per camera. |
| Use Flask for status APIs | Keeps dashboard integration simple. | Production deployment would need auth, logging, and process management. |
| Keep dashboard as static HTML | Lowers setup friction for reviewers. | More complex operations views would benefit from a frontend app. |
