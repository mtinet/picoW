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

# 5x5 매트릭스 패턴 정의
patterns = {
    'diagonal': [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ],
    'border': [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ],
    'cross': [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    'x': [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ]
}

# 패턴을 매트릭스에 출력하는 함수
def display_pattern(pattern, color):
    for y in range(5):
        for x in range(5):
            if patterns[pattern][y][x] == 1:
                strip.set_pixel(y * 5 + x, color)
            else:
                strip.set_pixel(y * 5 + x, (0, 0, 0))

# 무작위 색상을 생성하는 함수
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# 패턴을 무작위로 선택하여 표시하는 함수
def show_random_pattern(wait, blink_times=2):
    pattern_keys = list(patterns.keys())  # 패턴의 키 목록
    
    for _ in range(blink_times):
        selected_pattern = random.choice(pattern_keys)  # 무작위 패턴 선택
        color = random_color()  # 각 패턴에 대한 색상
        
        clear_matrix()  # 매트릭스를 먼저 지웁니다
        display_pattern(selected_pattern, color)  # 패턴 표시
        strip.show()  # 패턴을 매트릭스에 적용
        time.sleep(wait)  # 잠시 대기
        
        clear_matrix()  # 패턴을 지웁니다
        strip.show()  # 매트릭스에서 패턴을 지운 상태로 업데이트
        time.sleep(wait)  # 잠시 대기
        
        # 모든 패턴이 끝난 후 0.5초 동안 대기
        clear_matrix()  # 매트릭스를 지웁니다
        strip.show()  # LED를 끈 상태로 적용
        time.sleep(0.5)  # 0.5초 동안 대기

# 매트릭스 초기화 함수
def clear_matrix():
    for i in range(numpix):
        strip.set_pixel(i, (0, 0, 0))
    strip.show()

# 애니메이션 실행
while True:
    show_random_pattern(0.5)  # 각 패턴에 대해 0.5초 대기 후 반짝임
