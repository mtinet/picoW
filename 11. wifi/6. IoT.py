from machine import Pin, reset
import network
import time
import urequests
import gc

# 와이파이 정보 
SSID = 'U+Net03CC'
password = 'J6FDFE#490'

# 와이파이 연결하기
def wifiConnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(SSID, password)
        print("Waiting for Wi-Fi connection", end="")
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(1)
        print()
    print(wlan.ifconfig())
    print("WiFi is Connected")
    return wlan

# 주기적으로 연결 확인 및 재연결
def maintain_connection(wlan):
    if not wlan.isconnected():
        print('WiFi lost, reconnecting...')
        wlan.disconnect()
        wlan.connect(SSID, password)
        while not wlan.isconnected():
            print('Reconnecting...')
            time.sleep(1)
        print('Reconnected')

# 와이파이 함수 실행
wlan = wifiConnect()

# 22번 핀을 출력으로 설정
controlPin = Pin(22, Pin.OUT)

# firebase 리얼타임 데이터베이스 주소
url = "https://iot-project-3c0b1-default-rtdb.firebaseio.com/"

print("IoT System is Started.")

# Firebase 데이터 초기화 함수
def initialize_firebase():
    try:
        # firebase의 값을 확인하고, 아무값도 없거나 controlPin 키가 없으면 controlPin 키를 만들고 0으로 초기화 함
        response = urequests.get(url + ".json").json()
        if response is None or 'controlPin' not in response:
            print("controlPin not found in Firebase, initializing to 0")
            urequests.patch(url + ".json", json={'controlPin': 0})
            return 0
        # firebase에 controlPin 키가 있으면, 해당 값을 반환 함
        return response['controlPin']
    except Exception as e:
        print('Error occurred while initializing Firebase:', e)
        return 0

# 초기 설정, firebase에 저장된 값을 확인하고 Pico W를 초기화 
initial_controlPin_value = initialize_firebase()
controlPin.value(initial_controlPin_value)

# 메인루프
def main_loop():
    last_check = time.time()
    while True:
        try:
            # 실시간으로 Firebase 데이터 가져오기
            response = urequests.get(url + ".json").json()
            if response and 'controlPin' in response:
                if response['controlPin'] == 0:
                    controlPin.value(0)
                else:
                    controlPin.value(1)

            # 10분마다 Wi-Fi 연결 확인 및 재연결
            current_time = time.time()
            if current_time - last_check > 600:
                maintain_connection(wlan)
                last_check = current_time

            # 메모리 관리
            gc.collect()
            time.sleep(1)  # 1초마다 데이터 체크

        except Exception as e:
            print('Error occurred:', e)
            reset()  # 시스템 재시작

# 메인 프로그램 실행
main_loop()

