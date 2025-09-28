# core/mouse_controller.py
import time
import math

class MouseController:
    def __init__(self, esp, screen_center=(960, 540), step_max=60):
        """
        esp: екземпляр EspController з методом send(cmd)
        screen_center: центр екрану (або точка від якої робимо відліки)
        step_max: максимальний розмір одного кроку (px)
        """
        self.esp = esp
        self.center = screen_center
        # Віртуальна позиція курсора — ініціалізується як центр екрану.
        # Якщо курсор на початку в іншому місці — можна встановити через pyautogui.position()
        self.vx, self.vy = screen_center
        self.step_max = step_max

    def _send_move(self, dx, dy):
        """Надіслати одне відносне переміщення на ESP."""
        cmd = f"MOVE {int(dx)} {int(dy)}"
        self.esp.send(cmd)
        # оновити віртуальну позицію
        self.vx += dx
        self.vy += dy
        # невеликий wait для стабільності
        time.sleep(0.02)

    def move_to_zero(self):
        steps = 60
        dx_step = -1920/steps
        dy_step = -1080/steps

        for i in range(steps):
            self._send_move(dx_step, dy_step)

    def move_to_target(self, target_x, target_y):
        """
        target_x, target_y — абсолютні координати (пікселі екрану).
        Ми переводимо в відносний рух від віртуальної позиції
        і робимо серію кроків.
        """
        dx_total = target_x #- self.vx
        dy_total = target_y #- self.vy

        dist = math.hypot(dx_total, dy_total)
        if dist == 0:
            return

        # кількість кроків — залежно від step_max
        steps = max(1, int(math.ceil(dist / self.step_max)))

        dx_step = dx_total / steps
        dy_step = dy_total / steps



        for i in range(steps):
            self._send_move(dx_step, dy_step)

    def set_virtual_pos(self, x, y):
        """Якщо треба синхронізувати віртуальну позицію, викликай це."""
        self.vx = x
        self.vy = y

    def move_to_target_v2(self, target_x, target_y):
        """
        target_x, target_y — абсолютні координати (пікселі екрану).
        Ми переводимо в відносний рух від віртуальної позиції
        і робимо серію кроків.
        """
        dx_total = target_x
        dy_total = target_y
        dist = math.hypot(dx_total, dy_total)
        if dist == 0:
            return

        # кількість кроків — залежно від step_max
        steps = max(1, int(math.ceil(dist / self.step_max)))

        dx_step = dx_total / steps
        dy_step = dy_total / steps

        # лог

        for i in range(steps):
            self._send_move(dx_step, dy_step)
