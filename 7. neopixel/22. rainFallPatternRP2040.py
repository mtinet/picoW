import time
import random
from neopixel import Neopixel

# 네오픽셀의 셀 갯수, PIO상태, 핀번호 정의
numpix = 25
PIO = 0
Pin = 16

# 네오픽셀이 RGB타입일 때 네오픽셀 수, PIO상태, 핀번호, 네오픽셀 타입 순으로 선택, 밝기 지정
strip = Neopixel(numpix, PIO, Pin, "RGB")

# 밝기 설정(0~255)
strip.brightness(40)

# 빗물 느낌의 파란색 정의
head_color = (0, 0, 50)  # 어두운 파란색 (머리 부분)
middle_color = (0, 0, 150)  # 중간 파란색 (중간 부분)
tail_color = (0, 0, 255)  # 밝은 파란색 (꼬리 부분)

# 물방울의 상태를 저장하는 리스트
raindrops = []

# 비 내리는 패턴 함수
def rain_pattern():
    global raindrops

    # 새로운 물방울 생성 (30% 확률)
    if random.random() < 0.3:
        start_x = random.randint(0, 4)  # 랜덤한 x 좌표에서 물방울 시작
        raindrops.append({"x": start_x, "y": 0, "timestamp": None, "fading": False, "brightness": 255})  # 물방울 추가

    # 기존 물방울 업데이트 및 표시
    new_raindrops = []
    current_time = time.time()

    for drop in raindrops:
        x = drop["x"]
        y = drop["y"]

        # 이전 위치의 물방울 끄기
        if y > 0 and not drop["fading"]:
            strip.set_pixel((y - 1) * 5 + x, (0, 0, 0))  # 이전 위치의 픽셀 끄기

        # 물방울이 매트릭스 안에 있는 경우
        if y == 0:  # 머리 부분
            strip.set_pixel(y * 5 + x, head_color)
        elif y == 1:  # 중간 부분
            strip.set_pixel(y * 5 + x, middle_color)
        elif y == 2:  # 꼬리 부분
            strip.set_pixel(y * 5 + x, tail_color)
        elif y == 3:  # 꼬리의 다음 단계가 사라짐
            strip.set_pixel(y * 5 + x, tail_color)
        elif y == 4:  # 다섯 번째 줄에서 물방울 유지 후 점점 사라짐
            if drop["timestamp"] is None:
                drop["timestamp"] = current_time  # 물방울이 도착한 시간을 기록
                strip.set_pixel(y * 5 + x, tail_color)  # 다섯 번째 줄 물방울 유지
            elif current_time - drop["timestamp"] > 1:  # 1초 동안 유지 후 점점 사라지기 시작
                drop["fading"] = True  # 사라지기 시작
                drop["brightness"] -= 30  # 밝기 감소
                if drop["brightness"] <= 0:  # 완전히 사라지면 제거
                    continue  # 물방울을 리스트에서 제거
                else:
                    fade_color = (0, 0, drop["brightness"])
                    strip.set_pixel(y * 5 + x, fade_color)  # 밝기를 줄여가며 표시
        else:
            strip.set_pixel(y * 5 + x, (0, 0, 0))  # 이전 줄 물방울 끄기

        # 물방울을 한 칸 아래로 이동
        if y < 4 and not drop["fading"]:
            new_raindrops.append({"x": x, "y": y + 1, "timestamp": drop["timestamp"], "fading": drop["fading"], "brightness": drop["brightness"]})
        else:
            # 다섯 번째 줄에서 유지되는 물방울도 리스트에 남겨둠
            new_raindrops.append(drop)

    # 업데이트된 물방울 리스트로 교체
    raindrops = new_raindrops

    # 매트릭스 업데이트
    strip.show()

# 애니메이션 실행
while True:
    rain_pattern()  # 비가 내리는 패턴
    time.sleep(0.1)  # 각 프레임 간 대기 시간
