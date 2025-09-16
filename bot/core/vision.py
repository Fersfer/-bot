# core/vision.py

from ultralytics import YOLO
import mss
from PIL import Image

class Vision:
    def __init__(self, model_path= r"D:/mob_detector/mob_detector/yolov8n_mob22/weights/best.pt"):
        self.model = YOLO(model_path)
        self.screen_center = (960, 540)

    def grab_screen(self):
        """
        Захоплення скріншоту з усього екрану.
        """
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            img = sct.grab(monitor)
            return Image.frombytes("RGB", img.size, img.rgb)

    def detect(self, image):
        """
        Інференс YOLO на зображенні
        """
        results = self.model.predict(image, conf=0.4)
        return results[0]

    def find_nearest(self, results, target_class='mob'):
        """
        Знаходимо найближчий об’єкт класу target_class
        """
        mobs = []
        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            name = results.names[int(cls)]
            if name == target_class:
                x1, y1, x2, y2 = box
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                dist = abs(cx - self.screen_center[0]) + abs(cy - self.screen_center[1])
                mobs.append((dist, (cx, cy)))
        if mobs:
            mobs.sort(key=lambda x: x[0])
            return mobs[0][1]
        return None

    def is_hp_bar_present(self, results, class_name='target_HP'):
        """
        Перевірка, чи ще живий моб (є HP)
        """
        return any(results.names[int(cls)] == class_name for cls in results.boxes.cls)

    def is_my_hp_low(self, results, class_name='my_HP'):
        """
        Перевірити, чи у героя мало HP
        """
        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            if results.names[int(cls)] == class_name:
                x1, _, x2, _ = box
                width = x2 - x1
                if width < 100:  # можна змінити поріг
                    return True
        return False
