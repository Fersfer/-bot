import serial
import time


COM_PORT = "COM6"
BAUD_RATE = 115200
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout = 1)
time.sleep(2)

def send(cmd):
    ser.write((cmd + '\n').encode())
    print(f"[ESP32] {cmd}")
    time.sleep(1)