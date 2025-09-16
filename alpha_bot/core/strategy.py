# core/strategy.py

from alpha_bot.core.vision import Vision
from alpha_bot.core.esp_controller import EspController
import time

class BotStrategy:
    def __init__(self):
        self.vision = Vision()
        self.esp = EspController()

    def step(self):
        """
        Один цикл дій: перевірка HP, пошук цілі, атака, лут
        """
        screen = self.vision.grab_screen()
        results = self.vision.detect(screen)

        # Якщо мало HP — пити банку
        if self.vision.is_my_hp_low(results):
            print("🧪 Мало HP → п'ємо банку")
            self.esp.send("1")
            time.sleep(1)
            return

        # Якщо ціль убита — лутаємо
        if not self.vision.is_hp_bar_present(results):
            print("💰 Ціль мертва → збираємо лут")
            self.esp.send("F5")
            time.sleep(1)
            return

        # Пошук найближчого моба
        mob_coords = self.vision.find_nearest(results)
        if mob_coords:
            dx = mob_coords[0] - self.vision.screen_center[0]
            dy = mob_coords[1] - self.vision.screen_center[1]

            print(f"🎯 Наводимось на моба → ({dx}, {dy})")
            self.esp.send(f"MOVE {dx} {dy}")
            time.sleep(0.2)
            self.esp.send("F3")
            time.sleep(1)
        else:
            print("🔍 Мобів не знайдено...")
            time.sleep(1)
