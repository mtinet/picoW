# This code was written by Juhyun Kim.
# VCC는 VBUS에 GND는 GND에 연결, Trig는 0번, Echo는 1번 핀에 연결

from machine import Pin
import time

# 트리거 핀과 에코 핀 설정
trigger_pin = Pin(0, Pin.OUT)
echo_pin = Pin(1, Pin.IN)

# 초음파 센서를 이용해 거리 측정
def measure_distance():
    # 트리거 핀을 통해 10us 동안 초음파 신호 발생
    trigger_pin.low()
    time.sleep_us(2)
    trigger_pin.high()
    time.sleep_us(10)
    trigger_pin.low()

    # 에코 핀이 HIGH 상태가 될 때까지 기다림
    while echo_pin.value() == 0:
        pass
    start = time.ticks_us()

    # 에코 핀이 LOW 상태가 될 때까지 기다림
    while echo_pin.value() == 1:
        pass
    end = time.ticks_us()

    # 시간 측정
    duration = time.ticks_diff(end, start)

    # 음속(340 m/s)을 이용해 거리 계산
    # 거리 = (시간(초) * 음속(미터/초)) / 2 (왕복이므로 2로 나눔)
    distance = (duration * 340.0) / (1000000 * 2)

    return distance

# 메인 루프
while True:
    distance = measure_distance()
    print('Distance:', distance*100, 'cm')
    time.sleep(0.1)
