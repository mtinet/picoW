import machine
import utime

# 22번 핀을 출력 모드로 설정
ssr_pin = machine.Pin(22, machine.Pin.OUT)

# SSR 켜기
def turn_on_ssr():
    ssr_pin.value(1)

# SSR 끄기
def turn_off_ssr():
    ssr_pin.value(0)

# SSR를 5초 동안 켜고 끄기
while True:
    turn_on_ssr()  # SSR 켜기
    utime.sleep(1)  # 5초 대기
    turn_off_ssr()  # SSR 끄기
    utime.sleep(1)  # 5초 대기


