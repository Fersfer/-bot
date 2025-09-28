
import time

import pyautogui

from alpha_bot.MouseController import MouseController
from alpha_bot.core.esp_controller import EspController
from alpha_bot.core.vision import Vision


class BotStrategy:
    def __init__(self):
        self.vision = Vision()
        self.esp = EspController()
        self.mouse = MouseController(self.esp)

    def step(self):
        # 1. Зняти скрін і розпізнати
        screen = self.vision.grab_screen()
        results = self.vision.detect(screen)

        # 2. Знайти моба
        mob_coords = self.vision.find_nearest(results)
        if mob_coords:
            dx = mob_coords[0] - self.vision.screen_center[0]
            dy = mob_coords[1] - self.vision.screen_center[1]

            # 3. Навести мишу через ESP
            self.mouse.move_to_target(dx, dy)
            time.sleep(0.2)

            # 4. Клік та атака
            self.esp.send("MOUSE_LEFT")
            time.sleep(0.2)
            self.esp.send("F3")

            # 5. Чекаємо, поки зникне HP
            for _ in range(20):  # максимум ~10 секунд
                time.sleep(0.5)
                screen = self.vision.grab_screen()
                results = self.vision.detect(screen)

                if not self.vision.is_hp_bar_present(results):
                    print("💀 Моб мертвий → лутаємо")
                    self.esp.send("F5")
                    time.sleep(1)
                    return  # переходимо до наступного моба

            print("⚠️ HP моба не зник — можливо, ми не влучили")
            return

        else:
            print("🔍 Мобів не знайдено...")
            time.sleep(1)
