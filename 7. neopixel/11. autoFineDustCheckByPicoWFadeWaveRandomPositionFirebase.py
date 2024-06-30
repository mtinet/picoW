# This code was written by Juhyun Kim.

import time
from neopixel import Neopixel
import network
import urequests 
from timezoneChange import timeOfSeoul # timezoneChange.py 파일이 같은 폴더에 있어야 동작함
import random


# 와이파이 정보 
SSID = 'U+Net03CC'
password = 'J6FDFE#490'


# 자기 정보 넣기(Open Wether Map API Key, 측정하고자 하는 곳의 위도, 경도 정보, 자신이 사용하는 WiFi정보) 
# https://openweathermap.org/appid 에서 로그인 하고 https://home.openweathermap.org/api_keys 로 이동해서 API Key를 발급받음
API_KEY = '24109ddecb29a5405afe2a8df42c5e34'

# 확인하고 싶은 위치 정보 입력 
locations = [
    ('Seoul', '37.566', '126.9784'),
    ('San Francisco', '37.77493', '-122.41942'),
    ('Sevilla', '37.38283', '-5.97317')
]


# 와이파이 연결하기
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    # 와이파이 연결하기
    wlan.connect(SSID, password)  # 12, 13번 줄에 입력한 SSID와 password가 입력됨
    print("Waiting for Wi-Fi connection", end="...")
    print()
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
else:
    print(wlan.ifconfig())
    print("WiFi is Connected")
    print()

# firebase 리얼타임 데이터베이스 주소
url = "https://iot-project-3c0b1-default-rtdb.firebaseio.com/"

print("IoT System is Started.")

# 객체 교체하기, 특정 값만 바뀜
myobj = {'AQI': ''}
urequests.patch(url+".json", json = myobj)

# 네오픽셀의 셀 갯수, PIO상태, 핀번호 정의 
numpix = 16
PIO = 0
Pin = 22

# 네오픽셀이 RGB타입일 때 네오픽셀 수, PIO상태, 핀번호, 네오픽셀 타입 순으로 선택  
strip = Neopixel(numpix, PIO, Pin, "RGB")

# 밝기 설정(0~255)
strip.brightness(255)

    
def get_air_quality_index(lat, lon, api_key):
    # 아래의 날씨 정보나 공기 오염도 조회 주소를 복사하여 브라우저의 주소창에 넣고 엔터를 누르면 JSON의 형태로 데이터를 받아볼 수 있음 
    # 날씨 정보 조회
    # http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}
    urlWeather = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = urequests.get(urlWeather)
    dataWeather = response.json()

    # 공기 오염도 조회
    # http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}
    urlAQI = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    response = urequests.get(urlAQI)
    dataAQI = response.json()
    
    # weather는 설명이 직접 넘어옴
    # WeatherID 참고 링크: https://injunech.tistory.com/178
    weatherID = dataWeather['weather'][0]['id']
    weather = dataWeather['weather'][0]['description']
    location = dataWeather['name']
    print(f'Location: {location}')
    print(f'WeatherID: {weatherID}')
    print(f'Weather: {weather}')

    # aqi는 Air Quality Index
    # aqi = 1 # 1~5까지의 인덱스로 아래의 실제 데이터 대신 테스트 해볼 수 있음 
    aqi = dataAQI['list'][0]['main']['aqi']
    print("AQI: " + str(aqi) + "[Good(1)~Bad(5)]")
    
    return aqi

def set_neopixel_color(aqi):
    # Green, Red, Blue의 순서로 되어 있음
    if aqi == 1:
        color = (0, 0, 255)  # Blue
    elif aqi == 2:
        color = (255, 0, 0)  # Green
    elif aqi == 3:
        color = (255, 255, 0)  # Yellow
    elif aqi == 4:
        color = (100, 255, 0)  # Orange
    elif aqi == 5:
        color = (0, 255, 0)  # Red
    else:
        color = (0, 128, 128)  # Purple (unknown)

    for i in range(numpix):
        strip.set_pixel(i, color)
        time.sleep(0.01)
        strip.show()
        

def blink_initial_cells(color, count):
    selected_indices = []
    while len(selected_indices) < count:
        index = random.randint(0, numpix - 1)
        if index not in selected_indices:
            selected_indices.append(index)

    for _ in range(2):  # 두 번 깜빡이기
        for i in selected_indices:
            strip.set_pixel(i, color)
        strip.show()
        time.sleep(0.2)
        strip.clear()
        strip.show()
        time.sleep(0.2)

def fade_out():
    for brightness in range(255, -1, -5):
        for i in range(numpix):
            r, g, b = strip.get_pixel(i)  # 현재 셀의 색상 가져오기
            r = int(r * (brightness / 255))
            g = int(g * (brightness / 255))
            b = int(b * (brightness / 255))
            strip.set_pixel(i, (r, g, b))
        strip.show()
        time.sleep(0.05)

def fade_in(color):
    for brightness in range(0, 256, 5):
        for i in range(numpix):
            r = int(color[0] * (brightness / 255))
            g = int(color[1] * (brightness / 255))
            b = int(color[2] * (brightness / 255))
            strip.set_pixel(i, (r, g, b))
        strip.show()
        time.sleep(0.05)

def set_neopixel_wave_custom(aqi, count):
    if aqi == 1:
        color = (0, 0, 255)  # Blue
    elif aqi == 2:
        color = (255, 0, 0)  # Green
    elif aqi == 3:
        color = (255, 255, 0)  # Yellow
    elif aqi == 4:
        color = (100, 255, 0)  # Orange
    elif aqi == 5:
        color = (0, 255, 0)  # Red
    else:
        color = (0, 128, 128)  # Purple (unknown)

    blink_initial_cells(color, count)  # 초기 셀 깜빡이기
    fade_in(color)  # 서서히 밝아지기

    fade_steps = [1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.1, 0]  # 8단계 밝기
    start_indices = [0, 8]  # 시작 위치들

    for _ in range(3):  # 반복 횟수
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
            time.sleep(0.1)  # 속도 조절

    fade_out()  # 서서히 꺼지기

while True:
    updatedTime = timeOfSeoul()
    print(updatedTime)

    for idx, (location, lat, lon) in enumerate(locations):
        try:
            air_quality_index = get_air_quality_index(lat, lon, API_KEY)
            # 객체 교체하기, 특정 값만 바뀜
            myobj = {'AQI': air_quality_index, 'Location': location}
            urequests.patch(url+".json", json = myobj)
            set_neopixel_wave_custom(air_quality_index, idx + 1)
        except Exception as e:
            print("Error:", e)
            strip.clear()
        
        print()



