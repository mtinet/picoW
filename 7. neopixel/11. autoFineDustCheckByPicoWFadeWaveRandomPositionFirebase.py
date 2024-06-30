from machine import Pin, reset
import network
import time
import urequests
import gc
import random
from neopixel import Neopixel

# 와이파이 정보 
SSID = 'U+Net03CC'
password = 'J6FDFE#490'

# 네오픽셀 설정
numpix = 16
PIO = 0
Pin = 22
strip = Neopixel(numpix, PIO, Pin, "RGB")
strip.brightness(255)

# Firebase 리얼타임 데이터베이스 주소
firebase_url = "https://iot-project-3c0b1-default-rtdb.firebaseio.com/"

# 위치 정보
locations = [
    ('Seoul', '37.566', '126.9784'),
    ('San Francisco', '37.77493', '-122.41942'),
    ('Sevilla', '37.38283', '-5.97317')
]

# 와이파이 연결
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

# 공기질 정보 가져오기
def get_air_quality_index(lat, lon, api_key):
    try:
        urlAQI = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
        response = urequests.get(urlAQI)
        dataAQI = response.json()
        aqi = dataAQI['list'][0]['main']['aqi']
        return aqi
    except Exception as e:
        print('Error fetching AQI:', e)
        return None

# 초기 셀 깜빡임
def blink_initial_cells(color, count):
    selected_indices = random.sample(range(numpix), count)
    for _ in range(2):
        for i in selected_indices:
            strip.set_pixel(i, color)
        strip.show()
        time.sleep(0.2)
        strip.clear()
        strip.show()
        time.sleep(0.2)

# 페이드 아웃
def fade_out():
    for brightness in range(255, -1, -5):
        for i in range(numpix):
            r, g, b = strip.get_pixel(i)
            r = int(r * (brightness / 255))
            g = int(g * (brightness / 255))
            b = int(b * (brightness / 255))
            strip.set_pixel(i, (r, g, b))
        strip.show()
        time.sleep(0.05)

# 페이드 인
def fade_in(color):
    for brightness in range(0, 256, 5):
        for i in range(numpix):
            r = int(color[0] * (brightness / 255))
            g = int(color[1] * (brightness / 255))
            b = int(color[2] * (brightness / 255))
            strip.set_pixel(i, (r, g, b))
        strip.show()
        time.sleep(0.05)

# 네오픽셀 웨이브
def set_neopixel_wave_custom(aqi, count):
    colors = {
        1: (0, 0, 255),    # Blue
        2: (255, 0, 0),    # Green
        3: (255, 255, 0),  # Yellow
        4: (100, 255, 0),  # Orange
        5: (0, 255, 0),    # Red
        'default': (0, 128, 128)  # Purple
    }
    color = colors.get(aqi, colors['default'])
    blink_initial_cells(color, count)
    fade_in(color)

    fade_steps = [1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.1, 0]
    start_indices = [0, 8]

    for _ in range(3):
        for i in range(numpix):
            strip.clear()
            for start in start_indices:
                index = (start + i) % numpix
                for j, step in enumerate(fade_steps):
                    fade_index = (index - j) % numpix
                    r = int(color[0] * step)
                    g = int(color[1] * step)
                    b = int(color[2] * step)
                    strip.set_pixel(fade_index, (r, g, b))
            strip.show()
            time.sleep(0.1)
    fade_out()

# Firebase에 AQI 업데이트
def update_firebase(location, aqi):
    try:
        urequests.patch(firebase_url + f"/{location}.json", json={"aqi": aqi})
        print(f"Updated AQI for {location}: {aqi}")
    except Exception as e:
        print('Error updating Firebase:', e)

# 메인 루프
def main_loop(wlan):
    last_check = time.time()
    while True:
        try:
            for idx, (location, lat, lon) in enumerate(locations):
                aqi = get_air_quality_index(lat, lon, API_KEY)
                if aqi is not None:
                    set_neopixel_wave_custom(aqi, idx + 1)
                    update_firebase(location, aqi)
                time.sleep(1)

            current_time = time.time()
            if current_time - last_check > 600:
                maintain_connection(wlan)
                last_check = current_time

            gc.collect()
            time.sleep(1)
        except Exception as e:
            print('Error occurred:', e)
            reset()

# 와이파이 연결 및 메인 프로그램 실행
wlan = wifiConnect()
main_loop(wlan)
