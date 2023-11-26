from time import sleep
import machine
from machine import Pin, PWM

# 아날로그 값 읽기
analog_valueV = machine.ADC(26)
analog_valueH = machine.ADC(27)
  

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
    readingV = analog_valueV.read_u16()/16
    readingH = analog_valueH.read_u16()/16
    readingV = round((readingV/4096) * 180)
    readingH = round((readingH/4096) * 180)
    print("ADCV: ",readingV, "ADCH: ", readingH)
    setAngle(servo0, readingV)
    setAngle(servo1, readingH)
    sleep(0.1)

