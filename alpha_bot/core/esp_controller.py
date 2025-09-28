# core/esp_controller.py (фрагмент)
import serial, time

class EspController:
    def __init__(self, port='COM4', baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)

    def send(self, cmd: str):
        line = (cmd.strip() + '\n').encode()
        self.ser.write(line)
        print(f"[ESP32] -> {cmd}")
        # читаємо можливу відповідь (не блокуюче)
        time.sleep(0.03)
        while self.ser.in_waiting:
            resp = self.ser.readline().decode(errors='ignore').strip()
            if resp:
                print(f"[ESP32] <- {resp}")
