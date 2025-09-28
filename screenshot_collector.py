import pyautogui
import time
import os
from datetime import datetime

# 📂 Куди зберігати скріни
save_dir = r"D:\mob_detector\auto_new_screens"
os.makedirs(save_dir, exist_ok=True)

# 🕓 Як часто робити скріни (секунди)
delay = 15

# ⏱ Скільки скріншотів зробити
num_screens = 3


print(f"🚀 Починаємо збирання скріншотів... Кожні {delay} сек.")
print("🎮 Перейди у вікно гри та не чіпай мишку :)")

time.sleep(10)  # невелика пауза перед стартом

for i in range(num_screens):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/screen_{timestamp}.jpg"
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"✅ Збережено: {filename}")
    time.sleep(delay)

print("📦 Готово! Усі скріни збережені.")
