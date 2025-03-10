import network
import urequests
import time


# 와이파이 정보 
SSID = 'U+Net03CC'
password = 'J6FDFE#490'

# 와이파이 연결하기
def wifiConnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        # 와이파이 연결하기
        wlan.connect(SSID, password)  # 5, 6번 줄에 입력한 SSID와 password가 입력됨
        print("Waiting for Wi-Fi connection", end="...")
        print()
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(1)
        print()
        print(wlan.ifconfig())
        print("WiFi is Connected")
    else:
        print(wlan.ifconfig())
        print("WiFi is Connected")
        print()

# 와이파이 함수 실행
wifiConnect()

# 시간 정보 가져와서 출력하기 
time_dict = urequests.get("https://timejson.netlify.app/.netlify/functions/time")
print(time_dict.json())
print(time_dict.json()['milliseconds_since_epoch'])
print(time_dict.json()['time'])

