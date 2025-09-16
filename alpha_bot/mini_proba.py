
import time
import serial
import numpy as np
import mss
from ultralytics import YOLO
import pyautogui
import serial

# === Налаштування ===
MODEL_PATH = r"D:/mob_detector/mob_detector/yolov8n_mob22/weights/best.pt"
COM_PORT = "COM6"
BAUD_RATE = 115200
IMG_SIZE = 512
CONFIDENCE = 0.4
MOB_CLASS_ID = 2  # ← моб у тебе під класом "2"
FPS_LIMIT = 3

# Команди
CLICK_COMMAND = {"cmd": "click", "button": "left"}
ATTACK_COMMAND = {"cmd": "key", "key": "f3"}

# === Підготовка ===
model = YOLO(MODEL_PATH)
sct = mss.mss()
monitor = sct.monitors[1]
SCREEN_W, SCREEN_H = monitor["width"], monitor["height"]
center_screen = (SCREEN_W // 2, SCREEN_H // 2)

def send_command(ser, command):
    try:
        ser.write((command + '\n').encode())
        print(f"✅ Sent: {command}")
        time.sleep(0.1)
    except Exception as e:
        print(f"❌ Send error: {e}")

def pick_nearest_mob(dets):
    best = None
    best_dist = 99999
    cx0, cy0 = center_screen

    for b in dets:
        x1, y1, x2, y2 = b.xyxy[0].tolist()
        cls_id = int(b.cls.item())
        conf = float(b.conf.item())

        if cls_id != MOB_CLASS_ID or conf < CONFIDENCE:
            continue

        cx = 0.5 * (x1 + x2)
        cy = 0.5 * (y1 + y2)
        d = np.hypot(cx - cx0, cy - cy0)

        if d < best_dist:
            best_dist = d
            best = (cx, cy)

    return best



def main():
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout = 1)
    print("[🤖 BOT] Запущено. Натисни Ctrl+C щоб зупинити.")
    try:
        while True:
            frame = np.array(sct.grab(monitor))[:, :, :3]

            results = model.predict(source=frame, conf=CONFIDENCE, imgsz=IMG_SIZE, verbose=False)
            bboxes = results[0].boxes

            if bboxes is not None and len(bboxes) > 0:
                target = pick_nearest_mob(bboxes)
                if target:
                    cx, cy = target
                    print(f"[🎯 МЕТА] Найближчий моб знайдений на координатах: ({int(cx)}, {int(cy)})")

                    # Навести мишку
                    send_command(ser,"MOVE cx, cy " )
                    time.sleep(0.1)

                    # Натиснути двічі + F3

                    send_command(ser,"F3")


                else:
                    print("[ℹ️] Моб не знайдений")
            else:
                print("[ℹ️] Детекцій немає")

            time.sleep(1.0 / FPS_LIMIT)
    except KeyboardInterrupt:
        print("[🛑 BOT] Зупинено.")
    finally:
        if ser:
            ser.close()

if __name__ == "__main__":
    main()
