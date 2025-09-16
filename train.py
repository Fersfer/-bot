from ultralytics import YOLO
import os
import multiprocessing

def main():
    # 🧠 Рекомендована оптимізація памʼяті на слабших GPU
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

    # 📦 Завантаження моделі YOLOv8n (найлегша версія)
    model = YOLO(r"D:\mob_detector\mob_detector\yolov8n_mob22\weights\best.pt")

    # 🚀 Тренування моделі
    model.train(
        data="data.yaml",           # Шлях до YAML з описом датасету
        epochs=20,                  # Кількість епох
        imgsz=512,                  # Розмір зображень (зменшено з 640)
        batch=4,                    # Batch size (мінімізовано)
        name="yolov8n_mob2",        # Назва експерименту
        project="mob_detector",     # Папка проекту
        workers=0,                  # 🔒 Вимикає multiprocessing DataLoader (стабільніше для Windows)
        amp=False                 # 🔕 Вимикає автоматичну змішану точність (безпечніше)
                         # 🔕 Вимикає EMA (економія GPU памʼяті)
    )

if __name__ == "__main__":
    multiprocessing.freeze_support()  # 💡 Для сумісності на Windows
    main()
