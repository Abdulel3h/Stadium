import cv2
import numpy as np
import time
import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from flask import Flask, jsonify
from flask_cors import CORS
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

GATE_DEFINITIONS = {
    "A": {"zone": (50,  100, 320, 520), "capacity": 60, "label_pos": (60, 90)},
    "B": {"zone": (340, 100, 610, 520), "capacity": 60, "label_pos": (350, 90)},
    "C": {"zone": (630, 100, 900, 520), "capacity": 60, "label_pos": (640, 90)},
    "D": {"zone": (920, 100, 1190, 520), "capacity": 60, "label_pos": (930, 90)},
}

CROWDING_THRESHOLD_PX = 45
CRITICAL_OCCUPANCY = 80


@dataclass
class GateState:
    name: str
    capacity: int
    count: int = 0
    crowding_incidents: int = 0
    entry_rate_per_min: float = 0.0
    status: str = "NORMAL"
    alert: Optional[str] = None
    redirect_to: Optional[str] = None
    count_history: deque = field(default_factory=lambda: deque(maxlen=10))

    @property
    def occupancy_pct(self) -> float:
        return round((self.count / self.capacity) * 100, 1)

    def update_status(self):
        pct = self.occupancy_pct
        if pct < 50:
            self.status = "NORMAL"
        elif pct < 75:
            self.status = "BUSY"
        elif pct < CRITICAL_OCCUPANCY:
            self.status = "CRITICAL"
        else:
            self.status = "OVERFLOW"

    def update_entry_rate(self):
        h = list(self.count_history)
        if len(h) >= 2:
            self.entry_rate_per_min = max(0, (h[-1] - h[0]) * 12)


class DecisionEngine:
    def __init__(self):
        self.gates: Dict[str, GateState] = {
            name: GateState(name=name, capacity=cfg["capacity"])
            for name, cfg in GATE_DEFINITIONS.items()
        }
        self.total_expected = 240
        self.alerts_log: List[dict] = []
        self.lock = threading.Lock()

    def update(self, gate_counts: Dict[str, int], crowding: Dict[str, int]):
        with self.lock:
            for name, gate in self.gates.items():
                new_count = gate_counts.get(name, 0)
                gate.count_history.append(new_count)
                gate.count = new_count
                gate.crowding_incidents = crowding.get(name, 0)
                gate.update_entry_rate()
                gate.update_status()
                gate.alert = None
                gate.redirect_to = None
            self._generate_alerts()

    def _generate_alerts(self):
        sorted_by_load = sorted(self.gates.values(), key=lambda g: g.occupancy_pct)
        lightest = sorted_by_load[0]

        for gate in self.gates.values():
            if gate.crowding_incidents > 3:
                gate.alert = f"CROWDING at gate {gate.name}! Go now"
                gate.status = "OVERFLOW"
                self._log_alert(gate.name, gate.alert, "CROWDING")

            elif gate.status in ("CRITICAL", "OVERFLOW"):
                if lightest.name != gate.name:
                    gate.alert = (
                        f"Gate {gate.name} is {gate.occupancy_pct:.0f}% full "
                        f"— redirect to gate {lightest.name}"
                    )
                    gate.redirect_to = lightest.name
                    self._log_alert(gate.name, gate.alert, "OVERFLOW")

            elif gate.status == "BUSY" and gate.entry_rate_per_min > 15:
                gate.alert = (
                    f"High entry rate at {gate.name} "
                    f"({gate.entry_rate_per_min:.0f}/min) — heads up"
                )

    def _log_alert(self, gate: str, msg: str, alert_type: str):
        self.alerts_log.insert(0, {
            "time": time.strftime("%H:%M:%S"),
            "gate": gate,
            "message": msg,
            "type": alert_type,
        })
        if len(self.alerts_log) > 20:
            self.alerts_log.pop()

    def get_staff_distribution(self) -> Dict[str, int]:
        total_staff = 8
        total_load = sum(g.count for g in self.gates.values()) or 1
        dist = {}
        for name, gate in self.gates.items():
            ratio = gate.count / total_load
            dist[name] = max(1, round(ratio * total_staff))
        return dist

    def get_eta_minutes(self) -> float:
        total_in = sum(g.count for g in self.gates.values())
        remaining = max(0, self.total_expected - total_in)
        avg_rate = sum(g.entry_rate_per_min for g in self.gates.values()) or 1
        return round(remaining / avg_rate, 1)

    def to_json(self) -> dict:
        with self.lock:
            staff = self.get_staff_distribution()
            gates_data = []
            for name, gate in self.gates.items():
                gates_data.append({
                    "name": name,
                    "count": gate.count,
                    "capacity": gate.capacity,
                    "occupancy": gate.occupancy_pct,
                    "status": gate.status,
                    "alert": gate.alert,
                    "redirect_to": gate.redirect_to,
                    "crowding": gate.crowding_incidents,
                    "entry_rate": round(gate.entry_rate_per_min, 1),
                    "recommended_staff": staff.get(name, 1),
                })
            return {
                "gates": gates_data,
                "total_in": sum(g.count for g in self.gates.values()),
                "total_expected": self.total_expected,
                "eta_minutes": self.get_eta_minutes(),
                "alerts_log": self.alerts_log[:5],
                "timestamp": time.strftime("%H:%M:%S"),
            }


def detect_crowding_in_gate(positions: List[tuple], threshold: int) -> int:
    incidents = 0
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if dist < threshold:
                incidents += 1
    return incidents


def point_in_zone(cx, cy, zone):
    x1, y1, x2, y2 = zone
    return x1 < cx < x2 and y1 < cy < y2


STATUS_COLORS = {
    "NORMAL":   (0, 210, 100),
    "BUSY":     (0, 165, 255),
    "CRITICAL": (0, 80, 255),
    "OVERFLOW": (0, 0, 255),
}


def draw_frame(frame, engine: DecisionEngine, gate_persons: Dict[str, List]):
    overlay = frame.copy()

    for name, cfg in GATE_DEFINITIONS.items():
        gate = engine.gates[name]
        x1, y1, x2, y2 = cfg["zone"]
        color = STATUS_COLORS[gate.status]

        cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
        cv2.addWeighted(overlay, 0.12, frame, 0.88, 0, frame)
        overlay = frame.copy()

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        bar_h = 8
        bar_fill = int(((x2 - x1) * gate.occupancy_pct) / 100)
        cv2.rectangle(frame, (x1, y2 + 5), (x2, y2 + 5 + bar_h), (60, 60, 60), -1)
        cv2.rectangle(frame, (x1, y2 + 5), (x1 + bar_fill, y2 + 5 + bar_h), color, -1)

        lx, ly = cfg["label_pos"]
        cv2.putText(frame, f"Gate {name}", (lx, ly),
                    cv2.FONT_HERSHEY_DUPLEX, 0.9, color, 2)
        cv2.putText(frame, f"{gate.count}/{gate.capacity}  {gate.occupancy_pct:.0f}%",
                    (lx, ly + 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (220, 220, 220), 1)

        if gate.alert:
            cv2.putText(frame, "!! ALERT", (lx, ly - 18),
                        cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)

        for (cx, cy) in gate_persons.get(name, []):
            cv2.circle(frame, (cx, cy), 5, color, -1)

        if gate.crowding_incidents > 3:
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(frame, (mid_x, mid_y), 40, (0, 0, 255), 3)
            cv2.putText(frame, "CROWDING", (mid_x - 50, mid_y),
                        cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)

    info = engine.to_json()
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (15, 15, 25), -1)
    cv2.putText(frame,
        f"Stadium Gate Monitor  |  "
        f"In: {info['total_in']}/{info['total_expected']}  |  "
        f"ETA: {info['eta_minutes']} min  |  "
        f"{info['timestamp']}",
        (10, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (200, 200, 200), 1)

    return frame


engine = DecisionEngine()


@app.route("/api/status")
def api_status():
    return jsonify(engine.to_json())


@app.route("/api/health")
def api_health():
    return jsonify({"status": "ok"})


def run_vision():
    model = YOLO("yolov8n.pt")

    VIDEO_SOURCE = r"scenario1.mp4"  # change to 0 for webcam

    cap = cv2.VideoCapture(VIDEO_SOURCE)

    if not cap.isOpened():
        print("can't open video — check the path")
        return

    print("video running — look for the YOLO window")
    print("press Q on the window to quit\n")

    cv2.namedWindow("Stadium Gate Monitor", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Stadium Gate Monitor", 1280, 720)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("replaying...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            time.sleep(1)
            continue

        results = model.track(frame, persist=True, classes=[0], verbose=False)[0]

        gate_counts   = {g: 0 for g in GATE_DEFINITIONS}
        gate_persons  = {g: [] for g in GATE_DEFINITIONS}
        gate_crowding = {g: 0 for g in GATE_DEFINITIONS}

        if results.boxes.id is not None:
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                for gate_name, cfg in GATE_DEFINITIONS.items():
                    if point_in_zone(cx, cy, cfg["zone"]):
                        gate_counts[gate_name] += 1
                        gate_persons[gate_name].append((cx, cy))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 100), 2)

        for gate_name, persons in gate_persons.items():
            gate_crowding[gate_name] = detect_crowding_in_gate(
                persons, CROWDING_THRESHOLD_PX
            )

        engine.update(gate_counts, gate_crowding)
        frame = draw_frame(frame, engine, gate_persons)

        cv2.imshow("Stadium Gate Monitor", frame)

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    flask_thread = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=5000, debug=False),
        daemon=True
    )
    flask_thread.start()
    print("API running at http://localhost:5000/api/status")
    run_vision()