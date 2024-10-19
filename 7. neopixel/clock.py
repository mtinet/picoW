import network
import urequests
import utime
from timezoneChange import timeOfSeoul  # 서울 시간으로 변환하는 함수
from neopixel import Neopixel

# 네오픽셀 설정
numpix = 16  # 16개의 네오픽셀
PIO = 0
Pin = 22
strip = Neopixel(numpix, PIO, Pin, "RGB")
strip.brightness(150)

# 와이파이 정보
SSID = 'U+Net03CC'
password = 'J6FDFE#490'

# 와이파이 연결하기
def wifiConnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        # 와이파이 연결하기
        wlan.connect(SSID, password)
        print("Waiting for Wi-Fi connection", end="...")
        while not wlan.isconnected():
            print(".", end="")
            utime.sleep(1)
    else:
        print(wlan.ifconfig())
        print("WiFi is Connected")
        print()

# 와이파이 함수 실행
wifiConnect()

# 네오픽셀 시계 업데이트 함수
def clear_strip():
    """네오픽셀 모두를 끄는 함수 (초침만 업데이트할 때 호출)."""
    for i in range(numpix):
        strip.set_pixel(i, (0, 0, 0))
    strip.show()

def update_clock(hour, minute, second):
    """시, 분, 초침을 각각 네오픽셀에 나타내는 함수."""
    clear_strip()

    # 시침 위치 계산 (12시간 기준으로 12개의 픽셀에 맞춤)
    hour = hour % 12  # 12시간제로 변환
    hour_position = int(hour * 16 / 12) % 12  # 12픽셀 사용
    strip.set_pixel(hour_position, (255, 0, 0))  # 빨간색 (시침)

    # 분침 위치 계산 (60분을 12개의 픽셀에 맞춤, 5분 단위)
    minute_position = int(minute / 5) % 12
    strip.set_pixel(minute_position, (0, 255, 0))  # 초록색 (분침)

    # 초침 위치 계산 (60초를 12개의 픽셀에 맞춤, 5초 단위)
    second_position = int(second / 5) % 12
    strip.set_pixel(second_position, (0, 0, 255))  # 파란색 (초침)

    strip.show()  # 네오픽셀 업데이트

def update_seconds_only(hour, minute, second):
    """초침만 업데이트하는 함수. 시침과 분침은 유지."""
    clear_strip()

    # 시침과 분침 다시 표시
    hour = hour % 12
    hour_position = int(hour * 16 / 12) % 12
    strip.set_pixel(hour_position, (255, 0, 0))  # 빨간색 (시침)

    minute_position = int(minute / 5) % 12
    strip.set_pixel(minute_position, (0, 255, 0))  # 초록색 (분침)

    # 새로운 초침 표시
    second_position = int(second / 5) % 12
    strip.set_pixel(second_position, (0, 0, 255))  # 파란색 (초침)

    strip.show()

def get_seoul_time():
    """서울 시간을 인터넷에서 받아오는 함수. 실패하면 None을 반환."""
    try:
        response = urequests.get("http://worldtimeapi.org/api/timezone/Asia/Seoul")
        if response.status_code == 200:
            time_data = response.json()
            datetime_str = time_data['datetime']
            hour = int(datetime_str[11:13])
            minute = int(datetime_str[14:16])
            second = int(datetime_str[17:19])
            response.close()  # 응답 객체 닫기
            return hour, minute, second
    except Exception as e:
        print(f"시간 정보를 받아오는 데 실패했습니다: {e}")
    return None  # 실패 시 None을 반환

# 시간을 받아올 때까지 반복적으로 요청하는 함수
def get_time_with_retry():
    """시간 정보를 성공적으로 받아올 때까지 반복해서 요청."""
    while True:
        time_data = get_seoul_time()
        if time_data is not None:
            return time_data  # 시간이 성공적으로 받아지면 반환
        print("시간 정보를 다시 요청합니다...")
        utime.sleep(10)  # 10초 대기 후 다시 요청

# 내부 타이머로 시간을 계산하는 함수
def update_internal_time(hour, minute, second):
    """시스템 내부 타이머로 초를 계산하여 시간을 갱신."""
    utime.sleep(1)  # 1초 기다림
    second += 1
    if second >= 60:
        second = 0
        minute += 1
    if minute >= 60:
        minute = 0
        hour += 1
    if hour >= 24:
        hour = 0
    return hour, minute, second

# 처음 프로그램 시작 시 인터넷에서 현재 시간 받아오기
hour, minute, second = get_time_with_retry()

# 처음 시각과 분을 네오픽셀에 표시
update_clock(hour, minute, second)

# 메인 루프
last_checked_hour = hour  # 마지막으로 시간을 인터넷에서 받아온 시각 기록

while True:
    # 매 정각에 인터넷에서 다시 시간을 받아옴
    if minute == 0 and last_checked_hour != hour:
        updated_time = get_seoul_time()
        if updated_time:
            hour, minute, second = updated_time
        last_checked_hour = hour

    # 콘솔에 현재 시간 출력
    print(f"현재 시간: {hour:02}:{minute:02}:{second:02}")

    # 초침만 업데이트하면서 시침과 분침 유지
    update_seconds_only(hour, minute, second)

    # 내부 타이머로 시간 업데이트
    hour, minute, second = update_internal_time(hour, minute, second)

