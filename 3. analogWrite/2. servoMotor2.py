from time import sleep
from machine import Pin, PWM

# 서보 핀, 주파수 설정
servo0 = PWM(Pin(0))
servo0.freq(50)
servo1 = PWM(Pin(1))
servo1.freq(50)

# 서보 각도를 0~180도로 입력할 수 있도록 함수를 하나 만듬
def setAngle(servoName, angle):
    servo = servoName
    a = int(((((angle) * 2)/ 180) + 0.5)/20 * 65535)
    servo.duty_u16(a)
    
# 반복동작 
while True:
    setAngle(servo0, 0)
    setAngle(servo1, 0)
    sleep(1)
    setAngle(servo0, 45)
    setAngle(servo1, 45)
    sleep(1)
    setAngle(servo0, 90)
    setAngle(servo1, 90)
    sleep(1)
    setAngle(servo0, 135)
    setAngle(servo1, 135)
    sleep(1)
    setAngle(servo0, 180)
    setAngle(servo1, 180)
    sleep(1)
