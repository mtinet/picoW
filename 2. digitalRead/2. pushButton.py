import machine
import utime

# 21번 핀을 입력 모드로 설정
signal_pin = machine.Pin(21, machine.Pin.IN)

# 디지털 신호 읽기
def read_digital_signal():
    return signal_pin.value()

# 신호를 5초마다 읽고 출력
while True:
    signal_value = read_digital_signal()  # 디지털 신호 읽기
    print("Signal value:", signal_value)  # 신호 값 출력
    utime.sleep(0.1)  # 0.1초 대기
