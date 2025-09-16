import numpy as np
import supervision as sv
from ultralytics import YOLO

# Завантаження моделі
model = YOLO("best.pt")

# Анотування боксу
box_annotator = sv.BoxAnnotator(thickness=7)

# Callback функція
def callback(frame: np.ndarray, _: int) -> np.ndarray:
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    return box_annotator.annotate(frame.copy(), detections=detections)

# Обробка відео
sv.process_video(
    source_path="lineage2.mp4",
    target_path="result_lineage2.mp4",
    callback=callback  # без дужок
)
