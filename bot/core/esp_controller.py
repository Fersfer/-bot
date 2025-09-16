# core/esp_controller.py

import serial
import time

class EspController:
    def __init__(self, port='COM4', baudrate=115200):
        """
        Клас для надсилання команд на ESP32 по серійному порту.
        """
        self.esp = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Почекати ініціалізацію

    def send(self, command):
        """
        Надіслати команду (наприклад, 'F3', 'F5', 'CLICK 200 300')
        """
        self.esp.write((command + '\n').encode())
        print(f"[ESP32] Команда: {command}")
        time.sleep(0.1)
