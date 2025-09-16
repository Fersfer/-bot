from ultralytics import YOLO
import cv2

# Завантажуємо модель
model = YOLO("mob_detector/yolov8n_mob2/weights/best.pt")
screen_name = "screen_20250911_230247.jpg"

# Вказуємо шлях до скріна
img_path = fr"D:\mob_detector\auto_new_screens\{screen_name}"  # 🔁 підстав свій

# Передбачення
results = model.predict(
    source=img_path,
    conf=0.4,
    save=True,
    save_txt=True,
    project="runs/detect",
    name="predict",  # ⚠️ Тепер буде runs/detect/predict_fixed/
    exist_ok=True           # перезаписуватиме без помилки
)

# Відкрити зображення з боксами
img_result = cv2.imread(f"runs/detect/predict/{screen_name}")  # знайди точний шлях у папці
cv2.imshow("Detected", img_result)
cv2.waitKey(0)
cv2.destroyAllWindows()
