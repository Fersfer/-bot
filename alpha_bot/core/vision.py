# core/vision.py
import numpy as np
from ultralytics import YOLO
import mss
from PIL import Image
import cv2
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

    def grab_screen_v2(self):
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            img = sct.grab(monitor)
            return img

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
        self.save_frame(results)
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

    def save_frame(self, results):
        img = results.orig_img.copy()
        annotated = results.plot()

        os.makedirs("frame_logs", exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = f"frame_logs/frame_{timestamp}.jpg"

        cv2.imwrite(path, annotated)

    def get_red_fill_percentage(self,img, x1, y1, x2, y2):
        """
        Вычисляет процент заполнения красными оттенками в заданном прямоугольнике
        на скриншоте.

        :param image_path: Путь к файлу скриншота.
        :param x1, y1: Координаты верхнего левого угла прямоугольника.
        :param x2, y2: Координаты нижнего правого угла прямоугольника.
        :return: Процент заполнения красным цветом или None в случае ошибки.
        """
        img_np = np.array(img)
        image = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
        # Проверка корректности координат
        height, width, _ = image.shape
        if not (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height):
            print("Ошибка: Некорректные координаты прямоугольника.")
            return None

        # Вырезаем область интереса (ROI)
        roi = image[y1:y2, x1:x2]

        # Если ROI пустой (например, из-за некорректных координат), возвращаем 0
        if roi.shape[0] == 0 or roi.shape[1] == 0:
            print("Ошибка: Область интереса пуста.")
            return 0.0

        # Преобразование ROI в HSV
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Определение диапазонов для красного цвета в HSV
        # Красный цвет находится на двух концах спектра HSV
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])

        # Создание маски для каждого диапазона
        mask1 = cv2.inRange(hsv_roi, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_roi, lower_red2, upper_red2)
        # Объединение масок для получения полной маски красного цвета
        red_mask = cv2.bitwise_or(mask1, mask2)

        # Подсчет количества красных пикселей в ROI
        # red_mask будет бинарным изображением (0 или 255).
        # Non-zero count вернет количество пикселей со значением 255 (красные).
        num_red_pixels = cv2.countNonZero(red_mask)

        # Общее количество пикселей в ROI
        total_pixels_in_roi = roi.shape[0] * roi.shape[1]

        # Вычисление процента
        if total_pixels_in_roi == 0:
            return 0.0
        percentage = (num_red_pixels / total_pixels_in_roi) * 100

        return percentage

    def get_HP_persantge_mob(self,image):
         # ХП моба
         rect_x1, rect_y1, rect_x2, rect_y2 = 786, 2, 1132, 7
         return self.get_red_fill_percentage(image, rect_x1, rect_y1, rect_x2, rect_y2)

    def get_HP_persantge_pers(self, image):
         # ХП перса
         rectp_x1, rectp_y1, rectp_x2, rectp_y2 = 29, 58, 240, 60
         return self.get_red_fill_percentage(image, rectp_x1, rectp_y1, rectp_x2, rectp_y2)


