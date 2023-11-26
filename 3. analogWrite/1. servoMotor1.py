from time import sleep
from machine import Pin, PWM

# 서보 핀, 주파수 설정
servo = PWM(Pin(22))
servo.freq(50)

# 서보 각도를 0~180도로 입력할 수 있도록 함수를 하나 만듬
def setAngle(servoName, angle):
    servo = servoName
    a = int(((((angle) * 2)/ 180) + 0.5)/20 * 65535)
    servo.duty_u16(a)

# 반복동작
while True:
    setAngle(servo, 0)
    print('0')
    sleep(1)
    setAngle(servo, 45)
    print('45')
    sleep(1)
    setAngle(servo, 90)
    print('90')
    sleep(1)
    setAngle(servo, 135)
    print('135')
    sleep(1)
    setAngle(servo, 180)
    print('180')
    sleep(1)
