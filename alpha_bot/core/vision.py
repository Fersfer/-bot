# core/vision.py

from ultralytics import YOLO
import mss
from PIL import Image
import cv2
import numpy as np
import time
import os


class Vision:
    def __init__(self, model_path=r"D:/mob_detector/mob_detector/yolov8n_mob22/weights/best.pt"):
        self.model = YOLO(model_path)
        self.screen_center = (960, 540)
        self.prev_mob_hp_width = None  # Пам’ять про ширину HP моба

    def grab_screen(self):
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            img = sct.grab(monitor)
            return Image.frombytes("RGB", img.size, img.rgb)

    def detect(self, image):
        results = self.model.predict(image, conf=0.4, save=False, verbose=False)
        return results[0]

    def find_nearest(self, results, target_class='mob'):
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
            nearest = mobs[0][1]
            print(f"🎯 Найближчий моб: {nearest}")
            return nearest
        else:
            print("⚠️ Мобів не знайдено")
        return None

    def is_my_hp_low(self, results, class_name='my_HP'):
        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            if results.names[int(cls)] == class_name:
                x1, _, x2, _ = box
                width = x2 - x1
                if width < 100:
                    print(f"❤️ HP героя низький: ширина {width}")
                    return True
        return False

    def is_hp_bar_present(self, results, class_name='target_HP'):
        return any(results.names[int(cls)] == class_name for cls in results.boxes.cls)

    def is_target_hp_low_or_dead(self, results, class_name='target_HP'):
        """
        Відстежує ширину HP моба. Повертає:
        - 'dead' якщо HP-bar зник
        - 'low' якщо HP < 100
        - 'ok' якщо все добре
        """
        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            if results.names[int(cls)] == class_name:
                x1, _, x2, _ = box
                width = x2 - x1
                print(f"📉 HP моба: {width:.1f}px")

                if self.prev_mob_hp_width is not None:
                    if width < self.prev_mob_hp_width:
                        print(f"⬇️ HP зменшилось: було {self.prev_mob_hp_width:.1f}, стало {width:.1f}")

                self.prev_mob_hp_width = width

                if width < 100:
                    return 'low'

                return 'ok'

        # HP-bar відсутній
        print("💀 Моб мертвий: HP-bar зник")
        self.save_death_frame(results)
        self.prev_mob_hp_width = None
        return 'dead'

    def save_death_frame(self, results):
        img = results.orig_img.copy()
        annotated = results.plot()

        os.makedirs("death_logs", exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = f"death_logs/death_{timestamp}.jpg"

        cv2.imwrite(path, annotated)
        print(f"💾 Збережено скрін смерті моба: {path}")
