import os
import cv2


# === Класи ===
CLASS_NAMES = {
    0: "mob",
    1: "my_HP",
    2: "target_HP",
    3: "char",
    4: "buf"
}

# === Ввід даних від користувача ===
images_dir = input(r"D:\mob_detector\auto_new_screens\ ").strip()
filename = input("screen_20250918_000012.jpg): ").strip()

image_path = os.path.join(images_dir, filename)
label_path = os.path.join(images_dir.replace("images", "labels"), filename.replace(".jpg", ".txt"))

# === Відкриваємо зображення ===
img = cv2.imread(image_path)
if img is None:
    print("⛔ Зображення не знайдено!")
    exit()

h, w = img.shape[:2]

# === Наносимо анотації ===
if os.path.exists(label_path):
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue

            class_id, x, y, box_w, box_h = map(float, parts)
            class_id = int(class_id)

            # нормалізовані координати → пікселі
            cx, cy = x * w, y * h
            bw, bh = box_w * w, box_h * h
            x1 = int(cx - bw / 2)
            y1 = int(cy - bh / 2)
            x2 = int(cx + bw / 2)
            y2 = int(cy + bh / 2)

            color = (0, 255, 0)
            label = CLASS_NAMES.get(class_id, str(class_id))
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, label, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
else:
    print("⚠️ Відповідний .txt файл з анотацією не знайдено.")

# === Показуємо результат ===
cv2.imshow("📍 Перевірка анотацій", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
