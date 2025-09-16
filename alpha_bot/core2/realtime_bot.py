from yolo_detector import grab_screen, detect_objects
from alpha_bot.core2.esp_control import send
import time

MODEL_PATH = r"/mob_detector/yolov8n_mob22/weights/best.pt"
COM_PORT = "COM6"
BAUD_RATE = 115200
TARGET_CLASS = 'mob'
HP_BAR_CLASS = 'target_HP'
MY_HP_CLASS = 'my_HP'

# Центр екрану — щоб прицілитись мишкою
SCREEN_CENTER_X = 960
SCREEN_CENTER_Y = 540

def send_command(ser, command):
    try:
        ser.write((command + '\n').encode())
        print(f"✅ Sent: {command}")
        time.sleep(0.1)
    except Exception as e:
        print(f"❌ Send error: {e}")

def get_center(box):
    x1, y1, x2, y2 = box
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

def is_my_hp_low(results):
    for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
        name = results.names[int(cls)]
        if name == MY_HP_CLASS:
            x1, y1, x2, y2 = box
            width = x2 - x1
            if width < 100:  # умовна межа для "мало HP"
                return True
    return False

def is_target_dead(results):
    for cls in results.boxes.cls:
        name = results.names[int(cls)]
        if name == HP_BAR_CLASS:
            return False
    return True

def find_nearest_mob(results):
    mobs = []
    for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
        name = results.names[int(cls)]
        if name == TARGET_CLASS:
            center = get_center(box)
            dist = abs(center[0] - SCREEN_CENTER_X) + abs(center[1] - SCREEN_CENTER_Y)
            mobs.append((dist, center))
    if mobs:
        mobs.sort(key=lambda x: x[0])
        return mobs[0][1]  # координати найближчого
    return None

def run_bot():
    while True:
        image = grab_screen()
        results = detect_objects(image)

        # Якщо HP низький — п'ємо банку
        if is_my_hp_low(results):
            print("🧪 Мало HP → пʼємо банку")
            send("1")
            time.sleep(1)
            continue

        # Якщо ціль убита — збираємо лут
        if is_target_dead(results):
            print("💰 Ціль мертва → збираємо лут")
            send("F5")
            time.sleep(1)
            continue

        # Знайти найближчого моба
        mob_coords = find_nearest_mob(results)
        if mob_coords:
            dx = mob_coords[0] - SCREEN_CENTER_X
            dy = mob_coords[1] - SCREEN_CENTER_Y

            print(f"🎯 Моб знайдено → рух миші ({dx}, {dy}) + атака")
            send(f"MOVE {dx} {dy}")
            time.sleep(0.2)
            send("F3")  # атака
            time.sleep(1)
        else:
            print("🔍 Мобів не знайдено...")
            time.sleep(1)
