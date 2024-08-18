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

# 5x5 매트릭스의 나선형 좌표 (바깥에서부터 안쪽으로)
spiral_indices = [
    0, 1, 2, 3, 4,
    9, 14, 19,
    24, 23, 22, 21, 20,
    15, 10, 5,
    6, 7, 8,
    13, 18,
    17, 16,
    11, 12
]

# 무작위 색상을 생성하는 함수
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# 나선형으로 LED를 켜는 함수
def spiral_pattern(wait, blink_times=2):
    for _ in range(blink_times):
        color = random_color()  # 패턴에 대한 색상
        
        clear_matrix()  # 매트릭스를 먼저 지웁니다
        
        # 나선형 순서대로 LED를 켬
        for index in spiral_indices:
            strip.set_pixel(index, color)
            strip.show()  # 매트릭스에 적용
            time.sleep(wait)  # 각 단계에서 잠시 대기
        
        # 모든 LED가 켜진 후 잠시 대기
        time.sleep(wait * 10)
        
        # 매트릭스를 지움
        clear_matrix()
        strip.show()
        
        # 모든 패턴이 끝난 후 0.5초 동안 대기
        time.sleep(0.5)

# 매트릭스 초기화 함수
def clear_matrix():
    for i in range(numpix):
        strip.set_pixel(i, (0, 0, 0))
    strip.show()

# 애니메이션 실행
while True:
    spiral_pattern(0.01)  # 각 단계에서 0.1초 대기 후 나선형으로 LED를 켬
