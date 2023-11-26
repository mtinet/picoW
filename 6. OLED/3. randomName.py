# This code was written by Juhyun Kim.

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import random
import time

i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=200000)
print("I2C : " + str(i2c))
oled = SSD1306_I2C(128, 64, i2c)

while True:
    oled.fill(0)
    cmd = ["hihi", "junse", "nini", "babo"]
    ran = random.randint(0, len(cmd)-1)
    ranX = random.randint(0, 100)
    ranY = random.randint(0, 60)
    oled.text(cmd[ran], ranX, ranY)

    oled.show()
    time.sleep(1)
