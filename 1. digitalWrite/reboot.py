import machine
import utime

# GPIO 22번 핀을 출력 모드로 설정
ssr_pin = machine.Pin(22, machine.Pin.OUT)

# 부팅 시 기본 상태로 HIGH 설정 (리셋 방지)
ssr_pin.value(0)  # 기본적으로 SSR을 비활성화(HIGH 상태 유지)

# 부팅 후 메시지 출력
print("Board booted successfully")

def trigger_ssr():
    # SSR을 동작시켜 RUN 핀을 GND로 연결
    print("SSR triggered, resetting the board...")
    ssr_pin.value(1)  # SSR에 신호 전달 (HIGH 상태)
    utime.sleep(0.1)    # 신호 지속 시간 1초로 늘림

# 5초 카운트다운 후 SSR 동작
while True:
    for i in range(5, 0, -1):
        print(f"Rebooting in {i} seconds...")
        utime.sleep(1)
    
    trigger_ssr()
