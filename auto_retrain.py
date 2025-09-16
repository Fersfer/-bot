import os
import time
import pyautogui
from datetime import datetime
from ultralytics import YOLO
import cv2

def main():
    NUM_SCREENS = 10        # Кількість скрінів
    DELAY = 3               # Інтервал між скрінами (сек)
    MODEL_PATH = r"D:\mob_detector\mob_detector\yolov8n_mob22\weights\best.pt"
    IMG_SIZE = 512

    # === 2. ПАПКИ ===
    base_dir = r"/auto_datasets"
    img_dir = os.path.join(base_dir, "images")
    label_dir = os.path.join(base_dir, "labels")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)

    # === 3. МОДЕЛЬ ===
    model = YOLO(MODEL_PATH)

    print(f"📸 Починаємо скріни гри... ({NUM_SCREENS} шт кожні {DELAY} сек)")
    time.sleep(2)

    for i in range(NUM_SCREENS):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = os.path.join(img_dir, f"screen_{timestamp}.jpg")

        # Скриншот
        screenshot = pyautogui.screenshot()
        screenshot.save(img_path)
        print(f"✅ Збережено: {img_path}")

        # === 4. INFERENCE ===
        results = model.predict(img_path, conf=0.4, imgsz=IMG_SIZE, save=False, save_txt=False)

        # === 5. ЗБЕРЕЖЕННЯ АНОТАЦІЙ ===
        txt_path = os.path.join(label_dir, f"screen_{timestamp}.txt")

        with open(txt_path, "w") as f:
            for r in results:
                for box, cls in zip(r.boxes.xywhn, r.boxes.cls):  # normalized center x,y,w,h
                    class_id = int(cls)
                    cx, cy, w, h = box.tolist()
                    line = f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n"
                    f.write(line)

        print(f"🟡 Анотація записана: {txt_path}")
        time.sleep(DELAY)

    # === 6. ТРЕНУЄМО ===
    print("🔁 Запускаємо донавчання моделі...")

    model.train(
        data=r"D:\mob_detector\data.yaml",
        epochs=10,
        imgsz=512,
        batch=4,
        project="mob_detector",
        name="yolov8n_mob_retrain",
        exist_ok=True,
        amp=False,
        workers = 0,  # 🔒 Вимикає multiprocessing DataLoader (стабільніше для Windows)

    )

    print("🎉 Готово! Модель донавчена.")

if __name__ == "__main__":
    main()
