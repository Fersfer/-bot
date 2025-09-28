
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
            self.mouse.move_to_zero()
            self.mouse.move_to_target_v2(mob_coords[0], mob_coords[1])
            time.sleep(0.2)

            # 4. Клік та атака
            self.esp.send("MOUSE_LEFT")
            time.sleep(0.2)
            screen = self.vision.grab_screen_v2()
            mob_heals = self.vision.get_HP_persantge_mob(screen)
            if mob_heals > 5:
                print("моб найден атакует, по клику")
                self.esp.send("F3")
            else:
                print("моб не найден по клику, ищу по ф77")
                self.esp.send("F7")
                screen = self.vision.grab_screen_v2()
                mob_heals = self.vision.get_HP_persantge_mob(screen)
                if mob_heals > 5:
                    print("найден по ф7 атакую")
                    time.sleep(0.2)
                    self.esp.send("F3")
                else:
                    print("по ф7 моб не найден----")
                    return


            # 5. Чекаємо, поки зникне HP
            for k in range(40):  # максимум ~10 секунд
                time.sleep(0.5)
                screen = self.vision.grab_screen_v2()
                mob_heals = self.vision.get_HP_persantge_mob(screen)
                pers_health = self.vision.get_HP_persantge_pers(screen)
                if pers_health < 60:
                    self.esp.send("F6")
                    print("мобы меня пиздят")


                if mob_heals < 0.5:
                    print("💀 Моб мертвий → лутаємо")
                    self.esp.send("F2")
                    time.sleep(0.2)
                    self.esp.send("F5")
                    time.sleep(0.2)
                    self.esp.send("F5")
                    time.sleep(0.2)
                    return  # переходимо до наступного моба
            print("походу не добил я моба....")
            return

        else:
            print("🔍 АИ мобов не нашел, пробую Ф7")
            self.esp.send("F7")
            screen = self.vision.grab_screen_v2()
            mob_heals = self.vision.get_HP_persantge_mob(screen)
            if mob_heals > 5:
                print("🔍 моб найден атакую")
                self.esp.send("F3")
                time.sleep(0.5)
                for k in range(40):  # максимум ~20 секунд
                    time.sleep(0.5)
                    screen = self.vision.grab_screen_v2()
                    mob_heals = self.vision.get_HP_persantge_mob(screen)


                    if mob_heals < 0.5:
                        print("💀 Моб мертвий → лутаємо")
                        self.esp.send("F2")
                        time.sleep(0.2)
                        self.esp.send("F5")
                        time.sleep(0.2)
                        self.esp.send("F5")
                        time.sleep(0.2)

                        return  # переходимо до наступного моба